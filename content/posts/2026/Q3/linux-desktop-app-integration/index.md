---
title: "Linux 桌面系统：桌面应用、portal 与沙盒"
subtitle: ""
description:
  "从桌面应用的启动入口，理解 session D-Bus、portal 后端、屏幕共享与沙盒文件访问。"
date: 2026-09-16T01:27:11+08:00
lastmod: 2026-09-16T02:23:46+08:00
draft: false
authors: ["ryan4yin"]
tags: ["Linux", "Desktop", "Wayland", "NixOS", "Flatpak"]
categories: ["tech"]
series: ["Linux 桌面系统"]
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

[图形篇](/posts/linux-desktop-graphics/)讲了应用怎样把画面交给合成器。但在日常使用中，一个能显示窗口的程序还需要打开文件、调用其他应用，或者把某个窗口共享给视频会议。这些请求会经过哪些组件？沙盒又在哪一步限制它？

本文从应用启动说起。D-Bus 的名称、对象与接口可回看[系统基础篇](/posts/linux-desktop-system-foundations/)，用户服务与图形会话的关系见[登录会话篇](/posts/linux-desktop-login-session/)。这里沿着一次应用请求，继续往桌面内部走。

## 点下应用图标之后

桌面菜单里的应用入口通常由 `.desktop` 文件描述。其中 `Name`、`Icon` 决定如何展示，`Exec`
指定程序及参数；支持 D-Bus 激活的应用还可以声明
`DBusActivatable=true`，让支持该机制的启动器发送 D-Bus 消息。因而，点一次图标未必就是直接执行一次
`Exec`。字段的具体含义见
[Desktop Entry 规范](https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html)。

登录后自动启动也使用 `.desktop` 格式，但入口来自 autostart 目录。默认的用户目录是
`~/.config/autostart/`，系统目录是
`/etc/xdg/autostart/`；同名文件按优先级覆盖，`Hidden=true` 可以禁用对应入口，`OnlyShowIn`
等字段还会限定桌面环境。[Autostart 规范](https://specifications.freedesktop.org/autostart/latest/)定义了这些规则。

至于谁执行这些入口，要看会话的实现。桌面环境可以把这项工作交给
`systemd-xdg-autostart-generator`：它把入口转换成用户 `.service` 单元，再由桌面通过
`xdg-desktop-autostart.target`
启动。这不是每个 Linux 桌面都必须采用的路径，也不能把所有 GUI 进程都当成一个独立的用户 service。[生成器手册](https://github.com/systemd/systemd/blob/main/man/systemd-xdg-autostart-generator.xml)说明了这个接口。

进程启动后，它拿到的环境仍然很重要。portal 前端和后端是可按需激活的 D-Bus 服务，继承的是激活环境。终端里的
`WAYLAND_DISPLAY`、`XDG_CURRENT_DESKTOP`
正确，不代表用户管理器启动的服务也拿到了同样的值。GNOME、KDE 等完整桌面通常由会话组件完成传递；自己组合桌面时，也需要有组件承担这项工作。见
[portal 的系统集成说明](https://flatpak.github.io/xdg-desktop-portal/docs/system-integration.html)。

## portal 把请求交给哪个后端

XDG Desktop
Portal 向应用提供一组 D-Bus 接口，文件选择、屏幕共享等各有自己的接口。应用或工具包调用这些接口，`xdg-desktop-portal`
再与适合当前桌面的后端协作。普通应用同样可以使用 portal，它并不专属于 Flatpak。[上游概览](https://flatpak.github.io/xdg-desktop-portal/docs/)介绍了前端、后端与工具包的关系。

以屏幕共享为例，可以先把控制请求和画面数据分开看：

```text
应用 ──session D-Bus 请求──> xdg-desktop-portal ──> ScreenCast 后端
                                                    │
                                                    v
                                                  合成器
                                                    │
应用 <────────────── PipeWire 视频流 ────────────────┘
```

前端可以为不同接口选择不同后端。`portals.conf` 的 `[preferred]` 段中，`default`
设置默认候选；`org.freedesktop.impl.portal.ScreenCast`
这样的键覆盖某个接口的选择。值可以是以分号分隔、按顺序尝试的后端列表。后端必须实际实现所请求的接口，不能仅凭装了包就认定所有功能都齐了。[portals.conf 手册](https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html)给出了选择规则。

配置查找也受环境影响：前端依据 `XDG_CURRENT_DESKTOP` 查找相应的
`DESKTOP-portals.conf`，并按目录优先级查找配置，用户配置可以覆盖发行版提供的配置。排查后端选择时，要对照服务使用的环境与实际配置文件，不能只数系统里有几个带
`portal`
的包。同一份[配置手册](https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html)列出了完整的查找顺序。

### NixOS 与 Arch 接在哪里

在 NixOS 26.05 中，`xdg.portal.enable` 启用相关集成，`extraPortals`
提供后端软件包；模块会把这些包加入 D-Bus 与 systemd 的包集合。`config`
描述接口到后端的选择，其中 `config.common` 生成通用
`portals.conf`，其他名称生成桌面专用文件；`configPackages`
则接入已有配置包。[NixOS portal 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/config/xdg/portal.nix)能直接看到这些配置如何落地。

这样读配置更容易看清区别：安装后端、选择后端、把激活环境传给后端，是几项各自需要成立的条件。具体桌面模块可能已经提供其中一部分，补个人配置前要先看最终合并结果。

Arch 的
[xdg-desktop-portal 包](https://archlinux.org/packages/extra/x86_64/xdg-desktop-portal/)将桌面后端列为可选依赖，后端选择仍遵循
[Arch 提供的 portals.conf 手册](https://man.archlinux.org/man/portals.conf.5.en)。对作者使用的 niri，当前[上游屏幕共享说明](https://github.com/niri-wm/niri/wiki/Screencasting)要求可用的 D-Bus
session、PipeWire、`xdg-desktop-portal-gnome`，以及按会话方式运行 niri。这是 niri 的集成方式，不能据此推断所有 Wayland 合成器都应使用 GNOME 后端。

## 一次屏幕共享怎样建立

ScreenCast 的调用有先后关系。应用先用 `CreateSession` 建立会话，再用 `SelectSources`
描述需要的来源类型，例如显示器或窗口；`Start`
通常让用户选择共享对象，成功响应中返回流信息。最后，应用通过 `OpenPipeWireRemote`
取得文件描述符，用它连接相应的 PipeWire
remote。[ScreenCast API](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html)描述了完整生命周期。

这里的异步请求要等待
`Request.Response`，拿到请求对象不等于用户已经批准。许多 portal 都使用这套[请求约定](https://flatpak.github.io/xdg-desktop-portal/docs/requests.html)。开始请求、用户选好窗口、应用收到视频帧，是不同阶段。

在这条路径里，合成器参与提供画面，后端负责与桌面集成，D-Bus 传递控制请求，PipeWire 承载视频流。portal 交给应用的连接只开放相应的屏幕共享流节点；这不等于让应用访问全部 PipeWire 节点。授权限制见
[OpenPipeWireRemote](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html#org-freedesktop-portal-screencast-openpipewireremote)
和
[portal 的 PipeWire 集成](https://flatpak.github.io/xdg-desktop-portal/docs/pipewire.html)。

有些共享授权可以持久化。ScreenCast 的 `persist_mode` 和 `restore_token`
用来请求保存与恢复选择；恢复失败时仍可能重新询问用户。不能把上次点过「允许」理解成以后永远能读到同一窗口。具体取决于接口版本、后端支持和授权状态，见
[ScreenCast 的会话持久化说明](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html#session-persistence)。

因此，看到选择窗口已经弹出，只能说明请求走到了部分桌面交互流程。它还不能证明应用随后建立了正确的 PipeWire 连接，更不能证明视频已经传到会议另一端。

## 文件选择与真正写入文件

文件对话框走的是另一条路径。`FileChooser.OpenFile` 请求打开文件，`SaveFile`
请求一个保存位置。后端负责呈现选择器，返回的 URI 让应用继续访问文件；为沙盒应用提供访问时，还可能涉及 Documents
portal。`SaveFile`
自身并不替应用写完文档内容。[FileChooser API](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.FileChooser.html)说明了方法和返回值。

Documents portal 把获准访问的文件导出到 FUSE 文件系统。典型位置是
`/run/user/$UID/doc/`，应用在沙盒里看到的视图受文档授权限制。它使用独立的总线名称
`org.freedesktop.portal.Documents` 和对象路径
`/org/freedesktop/portal/documents`。文件的 portal 权限也会反映到 FUSE 的 POSIX mode
bits 上。见
[Documents API](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Documents.html)。这里的
`$UID`、文档 ID 都是路径说明，不是需要照抄的本机值。

这就解释了一个容易忽略的地方：应用能看到宿主机某个目录，并不意味着文件选择器返回的一定是那个直接映射路径。如果返回的是文档导出路径，应用还得能经由该路径访问文件。

### 一次保存权限改动

作者的 nix-config 提交 `7826934b`，提交说明是允许 document
portal 保存。实际差异是：在 nixpak 的公共配置中，把运行时目录下的 `/doc` 从 `bind.ro`
移到可写映射列表，并删除 GUI 基础配置里重复的只读映射。新增注释还指出，FileChooser 即使面对直接映射的 XDG 目录，也可能返回 Document
Portal 路径。

这条记录适合说明文件访问的两重约束：Documents
portal 决定应用能访问哪个导出文档，沙盒的挂载方式又决定这条访问路径是否可写。把路径只读挂进去，会额外挡住写入；把映射改为可写，也不等于取消 Documents
portal 对文档的授权。挂载范围与只读设置的含义见
[bubblewrap 上游说明](https://github.com/containers/bubblewrap#sandboxing)，文档授权见前面的 Documents
API。

提交没有附上保存后的文件校验或应用日志，所以这里能确认的是配置改动及其意图，不能补写「测试后所有应用保存都恢复正常」。这也是为什么文件对话框成功返回与最终保存成功要分别验证。

## 沙盒、总线过滤和 portal 权限分别限制什么

Flatpak 使用 bubblewrap 等组件建立沙盒。bubblewrap 提供 mount
namespace、目录映射以及可选的其他 namespace 和 seccomp 限制；具体隔离强度取决于调用参数。[Flatpak 底层组件](https://docs.flatpak.org/en/latest/under-the-hood.html#underlying-technologies)和
[bubblewrap 的安全边界](https://github.com/containers/bubblewrap#sandboxing)都强调了这类配置的作用。

应用实际能访问什么，还要看授予它的权限。Flatpak 的文件系统、设备、网络与总线访问配置，和用户通过文件选择器授予某个文件的访问权，作用范围不同。直接授予宽泛的宿主机访问，可能让应用走不经过 portal 的路径。不能仅凭「应用运行在 Flatpak 中」判断某项资源一定受到逐次确认。[Flatpak 沙盒权限文档](https://docs.flatpak.org/en/latest/sandbox-permissions.html)区分了这些资源访问与 portal。

`xdg-dbus-proxy` 则过滤 D-Bus 消息。它的 `--see=NAME`、`--talk=NAME`、`--own=NAME`
分别控制名称可见性、通信、名称拥有权，后一级包含前一级。更细的调用规则写成
`--call=NAME=RULE`，其中 `RULE` 的语法是
`[METHOD][@PATH]`；接口或方法过滤放在规则部分，不能把接口名误当成目的总线名称。规则语法与
`--filter` 开关见
[xdg-dbus-proxy 上游手册](https://github.com/flatpak/xdg-dbus-proxy/blob/main/xdg-dbus-proxy.xml)。这些是参数说明，不是一套可以直接运行的沙盒配置。

允许消息到达 portal，只解决了通信这一段。接收服务仍然要处理请求和授权，屏幕共享还要经过相应的来源选择与流访问控制。Permission
Store 可以保存资源、应用与权限字符串的对应关系，但它自己不解释这些字符串，也不会仅因数据库有一条记录就替应用打开文件或采集画面。[Permission Store API](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.impl.portal.PermissionStore.html)说明了这个存储接口。

作者的 nixpak 文件保存案例属于自定义沙盒配置，不能把它当成 Flatpak 默认挂载方式。比较不同方案时，要分别看它们怎样建立文件系统视图、过滤总线，以及把应用身份交给 portal。

## 自动启动为什么会牵涉 portal

作者另一个提交 `495c3669` 的说明是把 autostart 应用排到 `xdg-desktop-portal`
之后。提交中的注释记录了一个线索：沙盒应用在登录时与 portal 竞争启动，可能导致 FileChooser/OpenURI 首次启动不可用，需要重启应用。这里的现象来自配置注释，没有独立的运行日志。

差异在 `systemd.user.units."app-@autostart.service"` 下添加 drop-in，使用 `After=` 和
`Wants=` 指向前端、GTK 后端与 GNOME 后端。`Wants` 负责把服务拉入启动事务，`After`
负责排序；等待启动作业结束，并不等于检查每个 portal 功能都已可用。这些语义见
[systemd.unit 手册](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml)，基础区别也在[系统基础篇](/posts/linux-desktop-system-foundations/)讲过。

这里用到的是保留实例名的前缀 drop-in 查找。上游生成器把文件名转换成
`app-名称@autostart.service`，systemd 查找 drop-in 时会把前缀截短为 `app-`，同时保留
`autostart` 实例名，因此会查找
`app-@autostart.service.d/`。这让该目录下的配置可以作用于这类自动启动单元。见[生成器源码](https://github.com/systemd/systemd/blob/main/src/xdg-autostart-generator/xdg-autostart-service.c)以及
[systemd v257 的查找实现](https://github.com/systemd/systemd/blob/v257/src/shared/dropin.c)；[当前实现](https://github.com/systemd/systemd/blob/main/src/shared/dropin.c)也保留了这一规则。

提交注释把它叫作「模板 drop-in」，名称不够准确：`app-@autostart.service`
是实例名，模板名才是
`app-@.service`。这里的共享范围来自前缀查找。[systemd.unit 手册](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml)分别说明了实例、模板和前缀 drop-in。

这些规则能解释配置为何可以覆盖对应的生成单元。作者机器上最终生成了哪些单元、加载了哪些 drop-in，以及调整后首次启动的 FileChooser/OpenURI 是否恢复，仍须运行证据确认。本文没有取得这些结果，不把提交意图写成已经验证的竞态修复，也不把它推广到未使用这套生成器的启动路径。

从机制上看，观察方向已经很明确：入口由谁启动、实际单元是什么、依赖有没有加载，以及激活环境是否包含当前桌面所需信息。只看到应用和 portal 同时处于运行状态，无法还原登录时的先后关系。

## 在自己的会话中观察

下面两条只读命令，分别观察用户服务和用户总线。输出可能包含应用、进程和用户名；公开分享前只保留相关服务名称与状态，不要直接贴完整清单。

```console
systemctl --user list-units --type=service --no-pager
busctl --user list --no-pager
```

`list-units`
默认列出用户管理器内存中处于活动、有等待作业或失败状态的单元，不能当作全部已安装服务的目录。`busctl list`
列出总线上的名称；看到 portal 名称不等于 FileChooser、ScreenCast 都已实际工作。参数含义见
[systemctl 手册](https://github.com/systemd/systemd/blob/main/man/systemctl.xml)、[busctl 手册](https://github.com/systemd/systemd/blob/main/man/busctl.xml)及[用户实例选项](https://github.com/systemd/systemd/blob/main/man/user-system-options.xml)。

本次写作实际运行了这两条命令，两者都以退出码 1 返回
`Operation not permitted`。因此没有取得用户服务或总线名称的运行证据，也没有实际验证屏幕共享和文档保存。为观察机制而启动屏幕采集、修改沙盒权限或重启桌面服务，都不属于这组练习。

应用发出请求以后，文件访问与视频流各自有后续路径。PipeWire 的音频图、字体选择和输入法连接，则放在[音频、字体与输入法篇](/posts/linux-desktop-media-input/)继续讲。
