---
title: "Linux 桌面系统：系统服务、设备与通信"
subtitle: ""
description:
  "理解 systemd 的依赖与启动顺序、journal 日志、udev 设备事件，以及 D-Bus 服务接口。"
date: 2025-10-19T10:18:33+08:00
lastmod: 2026-09-16T00:43:48+08:00
draft: false
authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"
tags: ["Linux", "Desktop", "Systemd", "D-Bus"]
categories: ["tech"]
series: ["Linux 桌面系统"]
aliases: ["/posts/linux-desktop-2-systemd-services/"]
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

[上一篇](/posts/linux-desktop-boot/)讲到，早期用户空间准备好根文件系统后，会把启动工作交给正式系统。接下来，挂载和后台服务怎样组织起来？设备插上以后，程序又怎样知道它出现了？

以本系列使用的 systemd 系统为例，PID
1 的 systemd 是系统管理器，负责启动和管理系统服务；另有用户实例管理用户自己的服务。systemd-journald、systemd-udevd 则是独立运行的服务，并不是 PID
1 里几个可随意替换的函数。先把管理器和被管理的程序分开，后面读日志或配置时就容易多了。参见
[systemd 概览](https://github.com/systemd/systemd/blob/main/man/systemd.xml)、[journald](https://github.com/systemd/systemd/blob/main/man/systemd-journald.service.xml)
与 [udev 手册](https://github.com/systemd/systemd/blob/main/man/udev.xml)。

## systemd 等待的到底是什么

systemd 把要管理的对象称为 unit（单元）。`.service` 描述服务进程，`.mount`
对应挂载点，`.device` 表示设备，`.socket` 可以参与按需启动服务；`.target`
用来组织一组单元或提供同步点。因而「启动系统」包含的工作远比启动一串后台进程多。单元也不一定都有一份手写文件，有些来自生成器或运行时状态。[systemd 手册的 Units 部分](https://github.com/systemd/systemd/blob/main/man/systemd.xml)解释了这些对象。

读依赖配置时，我建议先分开两个问题：另一个单元是否也要启动，以及两者谁先谁后。假设有两个示意单元 A 和 B：

| A 中的配置   | 启动 A 时的含义                                           |
| ------------ | --------------------------------------------------------- |
| `Wants=B`    | 一起拉起 B，但 B 启动失败本身不阻止 A 启动                |
| `Requires=B` | 一起拉起 B；若还配置了 `After=B`，B 启动失败会阻止 A 启动 |
| `After=B`    | 两者都有启动任务时，A 等 B 的启动任务结束；它本身不拉起 B |
| `Before=B`   | 两者都有启动任务时，A 的启动任务排在 B 前面               |

这里的 A、B 只是关系示意，不是可直接复制的单元名。需求依赖和顺序关系相互独立；只有
`Wants=` 或 `Requires=` 时，两者可以并行启动。`Requires=`
也不能理解成持续健康检查：例如被依赖的进程自行正常退出，不保证依赖它的单元随之停止。具体语义见
[systemd.unit 的依赖说明](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml)。

那「B 的启动任务结束」是不是说明 B 已经能用了？还要看 B 怎样向 systemd 表达就绪。`Type=simple`
在创建服务进程后就认为启动完成，甚至不等待程序成功执行；`Type=exec`
会等到执行成功，但仍不等待程序内部初始化。支持通知协议的 `Type=notify`
服务则会在初始化完成后发送 `READY=1`。随便把配置改成 `notify`
没用，程序本身也得支持它。[systemd.service](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml)逐项定义了这些启动条件。

同理，target 到达也不能当作整个桌面的健康证明。target 本身没有应用逻辑，它通过依赖组织其他单元，默认还会补充相应的排序关系。能否打开窗口、完成一次请求，仍取决于参与其中的服务与应用。[systemd.target 手册](https://github.com/systemd/systemd/blob/main/man/systemd.target.xml)说明了这种分组和同步用途。

还有一个常见混淆：启用与运行是两个状态。单元的 `[Install]` 配置参与建立启用时的链接，比如
`WantedBy=` 使目标单元获得指向它的 `Wants` 关系；systemd 平时并不直接用 `[Install]`
来决定运行状态。因此，不能看到 enabled 就推断进程正在运行。参见
[systemd.unit 的安装段说明](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml)。

NixOS 把这层配置放进声明里：`systemd.services` 下的 `after`、`requires`、`wantedBy` 和
`serviceConfig`
等字段参与生成服务定义。排查时既要读声明，也要确认运行中的状态，不能把修改了 Nix 文件当作已经应用。[NixOS 手册的 Defining custom services](https://nixos.org/manual/nixos/stable/)给出了这些字段。Arch 使用同一个上游单元格式，包提供的单元与管理员的 drop-in 则按加载路径和优先级合并，参见
[Arch 的 systemd.unit(5)](https://man.archlinux.org/man/systemd.unit.5.en)。

## journal 留下了哪一段证据

服务启动失败时，需要把「管理器认为发生了什么」和「程序自己输出了什么」放在一起看。systemd-journald 收集内核消息、syslog 消息、原生 journal 消息，以及服务的标准输出和标准错误，保存为带字段的日志。服务输出默认连接到 journal，但配置可以改变这个去向，所以不能假定每个程序的全部输出都在这里。[journald 手册](https://github.com/systemd/systemd/blob/main/man/systemd-journald.service.xml)列出了入口和默认连接方式。

`journalctl`
是读取 journal 的客户端。按启动批次与单元筛选，可以把一次启动失败缩小到相关服务；其中 `-u`
不只匹配服务自身输出，也包含 systemd 对该单元的消息等额外记录。它不等价于只匹配一个
`_SYSTEMD_UNIT`
字段。[journalctl 手册](https://github.com/systemd/systemd/blob/main/man/journalctl.xml)说明了这些过滤条件。

日志能回答的是已有记录中的事件。没有搜到一条错误，并不能说明操作成功：日志可能未被收集，也可能已经不再保留。尤其要分清易失与持久存储，前者在
`/run/log/journal/`，重启后会丢失；后者在 `/var/log/journal/`。`Storage=`
控制存储方式，容量与保留期限还受其他设置影响。参见
[journald.conf](https://github.com/systemd/systemd/blob/main/man/journald.conf.xml)。排查一次重启之前的问题，要先确认那次启动的日志还在。

## 设备节点出现以后，udev 继续做什么

在启用了 devtmpfs 的系统中，内核可以在这个文件系统里维护设备节点，udev 再根据规则调整权限等属性。设备节点提供用户空间访问设备的入口，不能把它当成普通的数据文件。devtmpfs 与 udev 的分工见[内核 DEVTMPFS 配置说明](https://github.com/torvalds/linux/blob/master/drivers/base/Kconfig)。

设备增加、移除或状态改变时，内核发出 uevent，systemd-udevd 接收后匹配规则。规则可以补充属性、设置设备节点权限、增加有意义的符号链接；处理后的信息存入 udev 数据库，并通知订阅者。[udev 手册](https://github.com/systemd/systemd/blob/main/man/udev.xml)描述了这条路径。

这也是为什么「内核看见了设备」与「应用能使用设备」之间还有距离。节点可能已经存在，但权限或规则还不符合应用的要求；有稳定别名，也不等于驱动和应用协议都正常。上一章的[挂载标识案例](/posts/linux-desktop-boot/)关注设备路径怎么选择，这里关注设备事件到了用户空间后怎样继续处理。

systemd 也可以把带有 `systemd` 标签的 udev 设备表示为 `.device`
单元，让其他单元依赖设备状态。它并不会为所有设备无条件创建同样的服务。[systemd.device 手册](https://github.com/systemd/systemd/blob/main/man/systemd.device.xml)解释了标签和设备单元的关系。具体到谁能使用当前座席的设备，还涉及登录会话，留到[登录、身份与用户会话](/posts/linux-desktop-login-session/)再说。

### 一次 Android 设备规则的调整

我的 nix-config 中有个很小的提交
`d0035905`，标题记录的是 adb 和 fastboot 的 udev 规则已经并入 systemd。实际 diff 只从
`services.udev.packages` 列表里移除了
`android-udev-rules`，旁边原有的注释说明它用于 adb。这里能证明的是规则包声明被移除了，没有当时设备连接失败或修复成功的日志。

为什么这个改动有意义？NixOS 的 `services.udev.packages`
用来收集软件包提供的规则，删除其中一个包，改变的是规则来源。[NixOS 26.05 的 udev 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/services/hardware/udev.nix)定义了这个选项。当前 systemd 上游的
[70-uaccess.rules.in](https://github.com/systemd/systemd/blob/main/rules.d/70-uaccess.rules.in)确实有针对 Android
ADB、Fastboot 接口的匹配规则。这支持标题所说的调整方向，但不能反过来证明那个历史版本生成的规则与当前上游完全相同。

因此，遇到设备访问问题时，除了确认设备有没有出现，还可以继续追规则从哪个包来、有没有被覆盖、是否匹配到了当前设备。不能单凭额外的规则包已卸载，就认定系统里没有对应规则；也不能把这个提交照抄成所有机器都应删除该包的建议。

## D-Bus 把请求交给谁

进程需要协作时，可以通过 D-Bus 发送方法调用、接收回复或订阅信号。总线根据名称把消息送到对应连接，具体工作由接收请求的服务完成。规范区分系统总线与会话总线，前者供系统范围的服务通信，后者供用户环境中的应用协作。两者是不同的总线，找到一个服务之前先要选对它所在的总线。[D-Bus 规范](https://dbus.freedesktop.org/doc/dbus-specification.html)的 Message
Bus 与 Well-known Message Bus Instances 部分定义了这些概念。

一次方法调用还要指定对象路径、接口和方法。下面借总线自身提供的标准接口说明这些名字各管什么：

| 部分     | 例子                                  | 用途                     |
| -------- | ------------------------------------- | ------------------------ |
| 总线名称 | `org.freedesktop.DBus`                | 选择消息接收方           |
| 对象路径 | `/org/freedesktop/DBus`               | 选择接收方提供的对象     |
| 接口     | `org.freedesktop.DBus.Introspectable` | 选择对象的一组接口约定   |
| 方法     | `Introspect`                          | 请求对象返回接口描述 XML |

对象路径不是磁盘目录。`Introspect`
返回对象支持的方法、信号、属性等描述；属性读取则通常通过
`org.freedesktop.DBus.Properties.Get` 完成，需要给出目标接口和属性名。这些名称和参数由
[D-Bus 标准接口规范](https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces)定义，不宜凭打印结果猜一个方法名。

总线还支持按需激活：名字尚无拥有者时，符合条件的请求可以启动提供该名字的程序。因此，观察命令也要留意是否会触发激活。[D-Bus 的服务激活规范](https://dbus.freedesktop.org/doc/dbus-specification.html#message-bus-starting-services)解释了这个过程。后续应用篇会用到这些概念，但
[portal 与沙盒的具体调用](/posts/linux-desktop-app-integration/)放在那里展开。

## 在本机做几个小观察

先确认工具版本。下面三个命令只报告客户端版本，不证明相应服务已运行；语义见
[systemd 的通用选项](https://github.com/systemd/systemd/blob/main/man/standard-options.xml)与
[udevadm 手册](https://github.com/systemd/systemd/blob/main/man/udevadm.xml)。

```console
systemctl --version
udevadm --version
busctl --version
```

本次修订的验证环境中，systemctl 和 busctl 返回 `systemd 261 (261.1)`，udevadm 返回
`261`，退出码均为 0。

接着分别向系统实例与当前用户实例查询运行中的服务。`list-units` 观察已加载单元，`--type` 与
`--state` 限定结果；`--user`
切换到用户管理器。[systemctl 手册](https://github.com/systemd/systemd/blob/main/man/systemctl.xml)及其[实例选择选项](https://github.com/systemd/systemd/blob/main/man/user-system-options.xml)说明了这些参数。

```console
systemctl list-units --type=service --state=running
systemctl --user list-units --type=service --state=running
```

这两条在当前沙箱都返回
`Operation not permitted`，退出码为 1，没有取得服务列表。权限或连接失败不能解释成「系统没有运行服务」。在自己的桌面运行时，名单可以帮助确定下一步应查哪个单元，但 running 仍不是应用功能测试的结果。

设备观察可以先选一个不含硬件标识的例子，只查 `/dev/null` 的子系统属性：

```console
udevadm info --query=property --property=SUBSYSTEM --name=/dev/null
```

本次输出 `SUBSYSTEM=mem`，退出码为 0。`info` 查询设备信息，`--property`
限定输出字段，这个选项从 systemd 250 起提供，见
[udevadm 手册](https://github.com/systemd/systemd/blob/main/man/udevadm.xml)。这个练习只验证查询路径，不能用来证明 USB 插拔事件正常。换成真实设备时，完整属性可能包含序列号等标识，分享前需要检查。

再向系统总线自身请求标准接口描述，并明确禁止自动启动服务：

```console
busctl --system --auto-start=no call org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.Introspectable Introspect
```

这里用 `call` 显式调用 `Introspect`，`--auto-start=no`
对这次调用禁用自动激活。这个选项适用于 `call` 或 `emit`，不能用它给 `busctl introspect`
禁用激活，见
[busctl 手册](https://github.com/systemd/systemd/blob/main/man/busctl.xml)。`Introspect`
没有输入参数，因此命令末尾不需要类型签名或参数值；它返回包含对象接口描述的字符串，见
[D-Bus 的 Introspectable 规范](https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces-introspectable)。本次执行这条命令同样因
`Operation not permitted`
退出，退出码为 1，没有取得接口结果；上面的名称来自规范，不能冒充本机查询结果。

日志则需要先考虑内容。本次没有执行
`journalctl -b -n 10 --no-pager`，因为当前系统最近十条日志的内容未知，可能涉及用户活动或私有信息。在自己的机器上确认可以读取后，这条命令会选择本次启动的最后十条记录并关闭分页，参数见
[journalctl 手册](https://github.com/systemd/systemd/blob/main/man/journalctl.xml)。条数限制不是脱敏，十条记录也不足以重建整个启动过程。

这些观察分别对应管理器状态、设备属性和进程通信。下一篇进入[登录、身份与用户会话](/posts/linux-desktop-login-session/)，继续看系统怎样为一个具体用户建立工作环境。
