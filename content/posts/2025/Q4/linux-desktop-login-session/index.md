---
title: "Linux 桌面系统：登录、身份与用户会话"
subtitle: ""
description:
  "理解 greeter、PAM、systemd 用户实例、logind、密钥环与 polkit
  怎样衔接，以及登录之后各自保留的权限边界。"
date: 2025-10-19T10:19:33+08:00
lastmod: 2026-09-16T00:57:08+08:00
draft: false
authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"
tags: ["Linux", "Desktop", "PAM", "Systemd"]
categories: ["tech"]
series: ["Linux 桌面系统"]
aliases: ["/posts/linux-desktop-3-session-graphics/"]
hiddenFromHomePage: false
hiddenFromSearch: false
license: ""
lightgallery: false
table:
  sort: false
toc:
  enable: true
math:
  enable: false
comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
code:
  copy: true
  maxShownLines: 30
---

> AI 创作声明：本系列文章由笔者借助 ChatGPT、Kimi
> K2、豆包和 Cursor 等 AI 工具创作，有很大篇幅的内容完全由 AI 在我的指导下生成。本次重写也使用了 AI 辅助。如有错误，还请指正。

[系统基础篇](/posts/linux-desktop-system-foundations/)讲了系统服务如何启动、设备事件如何处理，以及 D-Bus 怎样连接进程。到了登录界面，系统还要完成另一组工作：确认用户身份，建立会话，再让这个用户的桌面和后台服务运行起来。

同样是弹出一个密码框，背后的要求可能完全不同。登录时确认身份，密钥环解锁时打开保存凭据的容器，polkit 则判断某个操作能不能做。弄清它们分别在问什么，比记住几条「密码不对怎么办」的命令更有用。

本文继续以 NixOS、systemd 和 greetd 为例。通过旧「桌面会话与图形渲染」链接进入的读者，可以在读完会话部分后接着看[显示、输入与图形渲染](/posts/linux-desktop-graphics/)。合成器怎样画出窗口，放在那一篇展开。

## 登录界面只是入口

greetd 是登录管理器，tuigreet、agreety 等 greeter 负责与用户交互。greeter 通过 Unix
socket 与 greetd 通信，发起登录、回应认证消息，再请求启动选定的会话命令。这个界面可以很简单，认证过程却仍然有自己的协议和状态。参见
[greetd IPC 手册](https://man.archlinux.org/man/greetd-ipc.7.en)。

以使用 PAM 的普通交互登录为例，可以把交接过程简化成下面这样。它表示职责关系，具体调用次序还由登录程序和 PAM 配置决定：

```text
greeter 收集用户输入
  → greetd 调用 PAM：认证、账户检查、打开会话
      → pam_systemd 向 logind 注册会话
      → 按需建立用户运行目录、启动 systemd 用户实例
  → greetd 启动选定的桌面会话命令
      → 合成器和用户服务继续初始化
```

这里有两条不同的接口：greeter 与 greetd 使用自己的 IPC；PAM 则是登录程序调用的模块框架。`pam_systemd`
把 PAM 的会话阶段接到 logind。不能因为它们都参与登录，就把它们合称为一个认证服务。对应关系见
[Linux-PAM 配置说明](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-desc.xml)和
[pam_systemd 手册](https://github.com/systemd/systemd/blob/main/man/pam_systemd.xml)。

## PAM 把一次登录拆成了哪些工作

PAM 的全名是 Pluggable Authentication
Modules。程序按服务名选择一组规则，例如 greetd 和 passwd 可以使用不同的 PAM 服务配置。在
`/etc/pam.d/`
中，文件名就是服务名；每行指定管理组、控制方式、模块及参数，多个模块组成一条栈。参见
[Linux-PAM 规则语法](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-syntax.xml)。

先记住四个管理组的区别：

| 管理组     | 处理什么                       | 与桌面的关系                             |
| ---------- | ------------------------------ | ---------------------------------------- |
| `auth`     | 验证声称的身份，并参与建立凭据 | 登录口令或其他认证方式在这里处理         |
| `account`  | 检查账户使用限制               | 身份验证通过，也可能仍不允许使用这项服务 |
| `password` | 更新认证令牌，常见的是修改口令 | 改密码时要让相关模块参与                 |
| `session`  | 服务开始前与结束后的会话工作   | 注册会话、准备运行环境、清理资源         |

`password`
很容易看错：它指修改口令，不是「输入密码登录」这一步。后面的密钥环案例，恰好就落在这个区别上。四组的定义与执行控制都来自上面的 PAM 手册。

模块存在还不够，得看它是否真的有机会执行，以及返回值怎样影响整条栈。比如 `required`
模块失败会使结果失败，但通常还要继续执行后面的模块；`sufficient` 成功且此前没有 `required`
失败时，可以直接结束这一层栈。这意味着把一个模块放进配置，不保证它每次都会运行。`include`
与 `substack`
又会改变规则的组合方式。理解这些词是为了读懂发行版生成的配置，不宜把几行网上的 PAM 片段直接拼进正在使用的登录栈。[控制字段的正式定义](https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-syntax.xml)值得对照着读。

## 用户、会话和用户实例是三个对象

一次登录建立一个 session。同一个用户可以同时在图形桌面、文本终端和 SSH 中登录，所以一个 UID 可以对应多个 session。`pam_systemd`
在常见的普通用户会话中向 logind 注册 session，并参与准备 `/run/user/UID`
这样的运行目录以及用户服务管理器。不同 session class 的行为有区别，例如较新 systemd 的
`user-light` 不会因此拉起用户管理器。参见
[pam_systemd 的 Description 与 Session Classes](https://github.com/systemd/systemd/blob/main/man/pam_systemd.xml)。

用户管理器由系统管理器通过 `user@UID.service`
启动，每个实例管理该用户自己的 units。同一 UID 的几个登录会话并不各自拥有一套独立的
`systemd --user`。因此，图形会话与用户服务的生命周期也不能画等号。[user@.service 手册](https://github.com/systemd/systemd/blob/main/man/user@.service.xml)解释了系统实例、用户实例与 session
scope 的组织方式。

`XDG_RUNTIME_DIR`
同样是按用户共享的运行目录，同一用户的并发会话会看到相同内容。它适合放 socket 等运行时对象，不适合保存需要长期保留的数据。应用不能只凭目录里有一个文件，就认为某次旧会话仍然存在。[pam_systemd 的环境说明](https://github.com/systemd/systemd/blob/main/man/pam_systemd.xml)专门提醒了并发会话与遗留文件的问题。

退出图形桌面之后，用户服务是否继续运行还受其他会话、linger 和退出策略影响。启用 linger 的用户可以在开机时启动用户管理器，并在退出登录后继续运行服务。这里先理解含义，不需要为观察桌面而改变它。[loginctl 的 linger 说明](https://github.com/systemd/systemd/blob/main/man/loginctl.xml)给出了这项行为的边界。

## logind 怎样连接会话与设备

logind 记录用户、session、活动状态以及 seat，并提供设备访问管理与电源操作等接口。它通常通过
`pam_systemd`
接收会话注册。它知道谁登录了、哪个会话在前台；认证口令本身由前面的 PAM 栈处理。参见
[systemd-logind 手册](https://github.com/systemd/systemd/blob/main/man/systemd-logind.service.xml)。

seat 可以理解为一个工作位置上的设备集合，例如显示设备和键鼠。一个 seat 可以关联多个 session，但同时只有一个处于活动状态。SSH 这类远程会话可以没有 seat。这里的「用户」表示身份，「session」表示一次登录，「seat」表示物理交互设备的归属，三者并不一一对应。[sd-login 的术语定义](https://github.com/systemd/systemd/blob/main/man/sd-login.xml)说明了这种关系。

设备节点可以通过 ACL（访问控制列表）给指定用户补充访问权限。以 systemd 的 `uaccess`
路径为例，udev 处理带有该标签的设备时，会查询所属 seat 的活动用户，并更新设备节点的 ACL；logind 在切换活动会话时参与触发这次更新。这个规则有适用条件，不能推成「所有设备都会自动开放」。对应实现见
[udev 的 uaccess 处理](https://github.com/systemd/systemd/blob/main/src/udev/udev-builtin-uaccess.c)与
[logind 的 seat 切换](https://github.com/systemd/systemd/blob/main/src/login/logind-seat.c)。

设备访问也不能只看一眼文件权限就结束。除了设备节点上的访问控制，使用 logind 接口的会话控制器还可以通过
`TakeDevice()`
获取设备文件描述符；对于支持的设备类型，logind 会随会话活动状态暂停或恢复访问。这个接口限于会话所属 seat 的设备，调用进程不必自己拥有直接打开设备节点的权限。具体约束见
[logind 的 TakeDevice 接口](https://github.com/systemd/systemd/blob/main/man/org.freedesktop.login1.xml)。

所以，合成器已经启动但拿不到设备时，需要先弄清它用了哪条设备访问路径，以及它所属的会话和 seat 是否符合要求。把用户加入更多组或把设备权限放宽，会改变权限边界，却不一定补上缺失的会话关系。设备拿到之后如何使用 DRM/KMS 与输入事件，接着看[图形篇](/posts/linux-desktop-graphics/)。

## 密钥环为什么还会再问一次密码

应用保存的凭据需要自己的存储服务。Secret
Service 通过用户登录会话中的 D-Bus 提供接口，GNOME
Keyring 是一种实现。规范里的 item 包含秘密值及其标签、查找属性；多个 item 放在 collection 中，也就是这里所说的密钥环。collection 可以处于锁定状态，应用需要解锁后才能读取其中的秘密值。参见
[Secret Service 简介](https://specifications.freedesktop.org/secret-service/latest/ch01.html)与
[collection 和 item](https://specifications.freedesktop.org/secret-service/latest/ch03.html)。

这层存储有自己的锁，系统登录成功不等于它已经解锁。GNOME
Keyring 的 PAM 模块会尝试用登录时取得的口令解锁 `login`
密钥环；自动登录没有提供这个口令时，就不能指望靠同一机制解锁。改口令时，该模块还可以更新
`login`
密钥环的口令，但需要参与对应的 PAM 流程。管理员重置账户口令或直接改变账户口令数据时，缺少旧口令，密钥环就无法这样同步。参见
[GNOME Keyring 的 PAM 说明](https://wiki.gnome.org/Projects/GnomeKeyring/Pam)。

还有一个细节：`login` 与 `default` 不是同一个概念。前者是 GNOME Keyring
PAM 集成针对的密钥环，后者在 Secret
Service 中是指向默认 collection 的别名。默认 collection 可以指向别处，改了 `login`
密钥环的口令，不代表其他 collection 都跟着改。[Secret Service 的 alias 定义](https://specifications.freedesktop.org/secret-service/latest/aliases.html)解释了这个间接关系。

### 一次 passwd 集成的修改

作者的 nix-config 提交 `d0cd0006`
保留了 greetd 的密钥环集成，并新增 passwd 的集成。去掉与本节无关的配置后，是下面两项：

```nix
{
  security.pam.services.greetd.enableGnomeKeyring = true;
  security.pam.services.passwd.enableGnomeKeyring = true;
}
```

提交说明与注释记录了修改口令后密钥环不同步、再次请求解锁的现象。diff 能直接证明的是新增了 passwd 这一行；没有随提交保存的运行日志，不能据此补写一次完整复现或宣称每一种解锁提示都由它造成。

这项改动为什么合理？NixOS 的 PAM 模块在启用 `enableGnomeKeyring`
后，会为相应服务生成 GNOME Keyring 规则，其中 `password` 组使用 `use_authtok`，`session`
组使用
`auto_start`。只给 greetd 配置这一项，不能代替 passwd 服务中的改口令钩子。这里对照的是
[NixOS 26.05 的 PAM 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/security/pam.nix)，它支持对选项含义的解释，不是当时主机生成文件的副本。

这段 Nix 是已有 GNOME Keyring 集成中的配置摘录，不是完整安装方案。当前 NixOS 还用
`services.gnome.gnome-keyring.enable`
提供服务集成，而 greetd 模块为其 PAM 服务设置了相关默认值；实际结果要结合自己的 Nixpkgs 版本与覆盖配置阅读。参见
[GNOME Keyring 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/services/desktops/gnome/gnome-keyring.nix)和
[greetd 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/services/display-managers/greetd.nix)。

理解这个案例后，可以按流程检查：修改口令的程序用了哪个 PAM 服务，它有没有执行密钥环的
`password` 规则，应用实际访问的是不是 `login`
collection。检查这些关系无需读取其中保存的凭据。也不要把删除密钥环当作默认修复，它会丢掉原来保存的数据。

## polkit 判断某一次操作能不能做

进入桌面后，普通应用有时需要请求系统服务执行一项有权限要求的操作。支持 polkit 的服务把调用方和操作交给 polkit
authority 判断；会话中的 authentication
agent 则在需要认证时提供交互界面。策略可以允许、拒绝，或者要求用户、管理员认证，判断还可能区分本地活动会话等条件。[polkit 架构与策略手册](https://polkit.pages.freedesktop.org/polkit/polkit.8.html)描述了这几种角色。

于是，密码框有没有出现，不只取决于系统里装没装 polkit。服务是否使用 polkit、策略要求什么、会话里有没有可用的 agent，都有影响。用户已经登录，也不代表此后所有管理操作都自动获得授权；密钥环已解锁，同样不能代替这个决定。

在完整桌面环境中，agent 往往由桌面会话提供和启动。自己组合合成器与用户服务时，则要读清楚所选组件的启动配置。没有 agent 时需要交互认证的请求可能无法完成，而策略直接允许的请求仍可能成功。手册的
[Authentication agents 部分](https://polkit.pages.freedesktop.org/polkit/polkit.8.html#polkit-authentication-agents)讨论了图形与文本交互的区别。

## 会话结束之后，登录管理器会启动什么

锁屏是在已有会话中限制交互，退出登录则结束会话。logind 提供锁定请求信号与锁定状态提示，实际桌面需要响应请求、完成锁屏；一条状态提示本身不能证明屏幕上的保护已经生效。参见
[logind 的 Lock 信号与 SetLockedHint](https://github.com/systemd/systemd/blob/main/man/org.freedesktop.login1.xml)。

这也解释了作者配置中的另一个历史修改。提交 `099752e8` 删除了一项
`services.greetd.settings.default_session.command`
的强制覆盖。被删除的命令直接启动桌面会话脚本，新增注释要求保留公共配置中的 tuigreet，并记录了桌面会话退出后无认证重入的问题。

关键在 greetd 的两个配置项：

| 配置段            | 上游定义的用途                                                 |
| ----------------- | -------------------------------------------------------------- |
| `default_session` | 通常用于 greeter；没有其他会话运行时会启动，包括用户会话结束后 |
| `initial_session` | 可选的首次自动登录；通过 runfile 判断本次启动是否已执行        |

[greetd(5)](https://man.archlinux.org/man/greetd.5.en)明确区分了它们。`default_session`
里的命令如果直接进入桌面，就改变了会话结束后的去向。原先的锁屏随着旧会话结束，下一次直接启动的桌面并不会因此自动具备一次新的用户认证。

这个提交证明了覆盖被移除，也保存了作者对风险的描述。当前手册能解释该配置为何会产生这种风险；但没有当时的有效配置、运行日志与操作记录，不能把它写成本次已经演示成功的锁屏绕过。它与上一节的密码不同步也不同：前者要检查密钥环的口令更新链，后者要检查会话退出后的启动链。

NixOS 的 `services.greetd.settings`
生成 greetd 的 TOML 配置。Arch 使用同一个上游配置格式与字段语义，可直接对照
[Arch 提供的 greetd(5)](https://man.archlinux.org/man/greetd.5.en)；区别在发行版如何提供服务及配置入口，不是
`default_session` 到了另一发行版就变成一次性自动登录。NixOS 的生成逻辑见
[greetd 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/services/display-managers/greetd.nix)。

## 在自己的桌面上观察这些边界

下面只查询状态。先在自己的交互会话中执行，不要把完整会话清单、进程参数或日志直接贴到公开场合。

```console
loginctl list-sessions
loginctl show-session self --property=Type,Class,Active,Remote,State
systemctl --user is-system-running
systemctl --system show greetd.service --property=LoadState,ActiveState,SubState
```

第一条用于理解一台机器可以同时有哪些 session，会包含用户及会话标识。第二条只选择少量状态字段；`self`
指调用进程所属的会话，从 SSH 或其他启动方式执行时，并不一定是正在显示的图形桌面。能看到
`Active=yes`
也不能证明合成器或密钥环工作正常。[loginctl 的 show-session 说明](https://github.com/systemd/systemd/blob/main/man/loginctl.xml)定义了
`self`、`auto` 和属性筛选。

第三条查询用户管理器的整体状态，`degraded`
等返回值能提示继续检查用户 units，但不等于登录失败。第四条查询系统管理器中的 greetd 单元，只适用于使用 greetd 的配置；`LoadState=not-found`
不能推广为没有任何登录管理器。状态查询与退出码见
[systemctl 手册](https://github.com/systemd/systemd/blob/main/man/systemctl.xml)，系统和用户实例的选择见
[通用选项](https://github.com/systemd/systemd/blob/main/man/user-system-options.xml)。

本次修订实际运行了上面四条命令。受运行环境限制，均返回
`Operation not permitted`，没有取得 session 或服务状态；`loginctl --version`
确认本地工具为 systemd
261。因而这里保留的是经过手册核对的观察方法，没有宣称已经验证当前机器的登录、密钥环或锁屏行为，也没有为验证文章而退出会话、改密码或重启登录服务。

从这些对象的关系出发，定位方向就有了依据：身份确认看 PAM 服务与规则，会话建立看 logind，用户后台服务看用户管理器，设备访问接着看会话控制器与 seat，凭据提示则区分密钥环解锁和 polkit 授权。下一篇进入[显示、输入与图形渲染](/posts/linux-desktop-graphics/)，继续追踪这个用户的程序怎样把画面送到显示器上。
