---
title: "Linux 桌面系统（七）：音频、字体与输入法"
subtitle: ""
description:
  "沿着声音路由、字体匹配和文字输入，理解 PipeWire、WirePlumber、fontconfig 与 Fcitx 5
  如何接入桌面应用。"
date: 2025-10-19T10:20:33+08:00
lastmod: 2026-09-16T22:41:13+08:00
draft: false
authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"
tags: ["Linux", "Desktop", "Audio", "Fonts", "Input Method", "Wayland"]
categories: ["tech"]
series: ["Linux 桌面系统"]
series_weight: 7
aliases: ["/posts/linux-desktop-4-multimedia-input/"]
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

> AI 创作声明：本系列文章使用 gpt-5.6-sol 与 DeepSeek 4.1 Flash 辅助创作。

桌面能显示窗口后，还得能听歌、看中文、打中文。这几件事用起来很自然，配置入口却散落在系统服务、用户会话和应用内部。以我的 NixOS +
Wayland 桌面为例，声音交给 PipeWire 和 WirePlumber，字体通过 fontconfig 匹配，中文输入使用 Fcitx
5。它们分别负责什么，应用又怎样使用这些服务？

本文沿这三条路径展开。[图形篇](/posts/linux-desktop-graphics/)已经讲过键盘事件和画面的传递，[桌面应用篇](/posts/linux-desktop-app-integration/)负责解释 portal 与屏幕共享。这里从音频流进入桌面开始。

## 一段声音怎样到达耳机

> PipeWire 用图来表示媒体处理过程，应用流、设备和过滤器都是图中的节点；WirePlumber 根据设备与策略决定节点怎样连接。两者的职责见
> [PipeWire 概览](https://docs.pipewire.org/page_overview.html)。

### 应用接入的是哪种接口

播放器把解码后的音频交给声音服务时，使用的接口未必是 PipeWire 原生接口。已有应用也可能使用 PulseAudio、ALSA 或 JACK
API。PipeWire 为这些接口提供兼容实现，因此「应用使用 PulseAudio
API」和「系统运行 PulseAudio 服务」不能画等号。具体接入方式见
[PipeWire 架构概览](https://docs.pipewire.org/page_overview.html)。

其中 `pipewire-pulse`
是一个使用 PipeWire 的 PulseAudio 协议兼容服务。应用连接这个入口后，音频仍进入 PipeWire 的媒体图；原有的 PulseAudio 客户端和控制工具也可以继续使用。它是可以单独出问题的一环，核心 PipeWire 正在运行，并不能证明 PulseAudio 客户端的入口正常。见
[pipewire-pulse 手册](https://docs.pipewire.org/page_man_pipewire-pulse_1.html)。

对使用 ALSA 接口的应用，还要区分用户空间的 ALSA 插件与内核设备访问。PipeWire 的 ALSA 插件可以把应用接入 PipeWire，而声卡侧也可以通过 ALSA 与硬件通信；这两个位置都出现 ALSA，并不意味着应用绕过了声音服务。蓝牙设备另有 BlueZ
monitor，不能把所有输出都画成同一条声卡路径。[WirePlumber 会话管理说明](https://pipewire.pages.freedesktop.org/wireplumber/design/understanding_session_management.html)列出了各类设备 monitor 的职责。

### PipeWire 管图，WirePlumber 决定怎样连接

PipeWire 用 node 表示处理音视频的节点，port 是节点的数据端口，link 把端口连接起来。播放流和硬件输出可以各有自己的节点。录音则反过来，从采集节点流向应用。

```text
播放：应用流节点 ──link──> Audio/Sink ──> 输出设备
录音：输入设备 ──> Audio/Source ──link──> 应用流节点
                         ↑
          WirePlumber 发现设备、配置节点、选择连接目标
```

这里的 sink 是接收播放数据的节点，source 是提供采集数据的节点。WirePlumber 是 PipeWire 的会话与策略管理器：它发现设备，选择 profile（设备的工作模式，如模拟输出）和 route（该模式下使用的端口，如耳机或扬声器），配置节点的格式与端口，再创建和维护连接。设备拔出时，它还需要重新评估连接关系。这些工作持续发生，不只在登录时做一次。上图中的角色对应
[PipeWire 对象模型](https://docs.pipewire.org/page_overview.html)和
[WirePlumber 的会话管理职责](https://pipewire.pages.freedesktop.org/wireplumber/design/understanding_session_management.html)。

普通播放流通常连接到默认输出；如果没有可用的默认输出，WirePlumber 的默认策略会考虑可用节点的会话优先级和设备 route。应用也可以请求特定目标，流的属性还可以限制移动或回退。因此，默认输出与某个应用的实际去向需要分别观察。具体规则见
[Linking Policy](https://pipewire.pages.freedesktop.org/wireplumber/policies/linking.html)。

这样一来，「没有声音」就可以拆成几个问题：应用有没有成功接入，图里有没有它的流，流连接到了哪个 sink，sink 对应的设备 route 是否可用？只看到设备名字，还不能确认应用的音频流已经正确连接。

### NixOS 怎样启用这些组件

在 NixOS 26.05 的模块中，`services.pipewire.enable`
启用服务集成，`alsa.enable`、`pulse.enable`、`jack.enable`
分别控制相应的兼容支持；`services.pipewire.package` 选择服务使用的软件包。默认的
`systemWide = false`
使用用户单元，用户管理器与登录会话的关系可以回看[登录会话篇](/posts/linux-desktop-login-session/)。这些选项的实现见
[NixOS PipeWire 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/services/desktops/pipewire/pipewire.nix)。

Arch 把这些角色拆成软件包。例如
[pipewire-pulse](https://archlinux.org/packages/extra/x86_64/pipewire-pulse/)提供 PulseAudio 兼容服务，其依赖包含 PipeWire 和会话管理器的虚拟依赖。包名与 NixOS 选项的组织不同，但客户端入口、媒体图和策略管理的边界仍然相同。安装了兼容包，也还需要核对对应的用户服务是否能工作。

「启用兼容接口」和「实际采用哪个 PipeWire 软件包」是两件事。若 `pipewire-pulse.service`
本身启动失败，应先检查失败单元、软件包版本和生成的用户单元，再去看设备路由；调音量无法解释兼容服务为什么没有启动。

### quantum 不能直接当成耳机延迟

PipeWire 的 quantum 表示一轮图处理的样本帧数。假设实际采样率是 48000
Hz、quantum 是 32，`32 / 48000` 约为 0.67
ms。这是该处理块对应的时间，不能直接当成从应用到耳机的总延迟。

`default.clock.quantum` 是没有客户端提出要求时的默认值，`min-quantum` 和 `max-quantum`
则约束相应范围。链路中的节点处理和缓冲还会增加延迟，PipeWire 另有延迟传播机制来描述它们。见
[pipewire.conf](https://docs.pipewire.org/page_man_pipewire_conf_5.html)与
[Latency support](https://docs.pipewire.org/page_latency.html)。因此，本文不把固定 quantum 的个人参数作为通用音频配置；能解释一个参数的单位，还不等于测过整条链路。

## 一串文字怎样选到字体

> fontconfig 根据应用提交的字体族、语言、样式等条件匹配已安装字体，并按规则进行替换和排序。配置模型见
> [fontconfig user documentation](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)。

音频是持续传递的数据流，字体匹配则发生在应用准备显示文字时。应用通常先提出一个请求：希望使用哪个字体族、字重、尺寸和语言。fontconfig 读取 XML 配置与字体信息，把这些条件组成的 pattern 匹配到可用字体。

匹配结果受请求和规则共同影响。`sans-serif`
是通用族名，可以经规则指向具体字体；`lang=zh-cn`
是语言条件，不能理解成「强制每个字符使用某一款中文字体」。应用还可以提供自己的字体或执行自己的匹配。见
[fontconfig 用户文档](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)。

fontconfig 也保存抗锯齿、hinting 等属性供渲染侧使用，但真正把文字排好、画出来，还需要应用的文本栈。例如
[Pango](https://docs.gtk.org/Pango/)负责国际化文本布局与渲染，并与 HarfBuzz、Fontconfig、FreeType 等组件集成。因此，查到了正确的族名，并不能同时证明字形选择、排版、缩放和最终显示都正确。

一段文字也未必只使用一个字体。主字体缺少某些字符时，文本栈需要寻找可用字形；Pango 用 fontset 表达一组可用于渲染文字的字体。排查缺字时，需要具体到字符以及应用所用的字体集合，而不只是确认系统装过一个名字带 CJK 的包。[Pango Fontset](https://docs.gtk.org/Pango/class.Fontset.html)描述了这层关系。

在 NixOS 中，`fonts.packages` 提供字体包，`fonts.fontconfig.defaultFonts` 为
`sansSerif`、`serif`、`monospace`、`emoji`
生成通用族的偏好规则；模块会把字体目录和配置接入 fontconfig。可以直接从
[NixOS fontconfig 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/config/fonts/fontconfig.nix)看到生成的 XML。这些偏好不会覆盖所有应用的独立字体选择。

Arch 的
[fontconfig 包](https://archlinux.org/packages/extra/x86_64/fontconfig/)提供相同的匹配工具。规则仍使用 fontconfig 的 XML 和配置搜索路径，例如
`/etc/fonts/fonts.conf` 与
`$XDG_CONFIG_HOME/fontconfig/fonts.conf`；文件怎样被 include 进来决定了规则何时参与匹配，不能把目录简单排成一条固定的「系统配置优先、用户配置其次」的表。完整加载规则见
[fonts-conf](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)。

## 从按键到输入框里的中文

能显示中文，说明应用有办法画出这些字；能输入中文，还需要把按键转换成文字。Fcitx
5 是输入法框架，输入引擎负责拼音、双拼等转换，frontend 负责与应用或合成器对接。这里的 frontend 指通信入口，不只是屏幕上的候选框。

框架、输入引擎和工具包模块的安装关系可以对照
[Fcitx 5 设置说明](https://fcitx-im.org/wiki/Setup_Fcitx_5)。

### text-input 是应用这一侧的协议

以应用与合成器采用 text-input-v3、合成器又能接入 Fcitx 5 的会话为例，可以把通信分成两段：

```text
应用的文本输入上下文 <-- text-input --> 合成器 <-- 输入法接口 --> Fcitx 5
```

合成器和 Fcitx
5 之间可能使用 input-method 协议，也可能采用桌面自己的接口。例如 Fcitx 文档列出的 Sway 路径使用 input-method-v2，GNOME 路径使用 IBus
D-Bus 接口。客户端支持 text-input-v3，不代表合成器到输入法的另一段就自动齐了。见
[Fcitx 的 Wayland 文档](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland)。

按键从内核输入系统进入合成器后，还要沿输入法侧的通道交给 Fcitx。以 Fcitx 的 input-method-v2 实现为例，输入上下文激活时，它请求 keyboard
grab，接收按键并交给内部输入上下文处理；生成的文字再经合成器返回应用。这里的 grab 是协议提供的按键接收接口，不是让 Fcitx 直接读取键盘设备。可对照
[Fcitx Wayland frontend 实现](https://github.com/fcitx/fcitx5/blob/master/src/frontend/waylandim/waylandimserverv2.cpp)。

文字输入还有自己的生命周期。对 text-input-v3 而言：

1. 键盘焦点进入应用 surface 后，应用收到 `enter`。当焦点落到可编辑控件，应用请求
   `enable`。
2. 应用按支持情况提交周边文本、内容类型和光标矩形等状态，用 `commit`
   使这一批请求生效。输入法据此处理当前输入上下文。
3. 输入过程可以产生
   `preedit_string`，也就是还没确认的预编辑文本。选词确认后，`commit_string`
   携带要插入的文字；应用在 `done` 事件处应用这一批更新。
4. 输入焦点离开编辑控件时，应用请求 `disable` 并提交；焦点离开 surface 还会收到
   `leave`。进入新的输入上下文后，相关状态需要重新发送。

这些请求、事件和状态边界来自
[text-input-v3 协议 XML（镜像）](https://github.com/wayland-mirror/wayland-protocols/blob/main/unstable/text-input/text-input-unstable-v3.xml)。此次无法读取 freedesktop 的托管原文，协议细节核对使用了这份镜像；输入法侧另外核对了上述 Fcitx 上游实现。这里有两个容易混淆的 commit：应用的
`commit` 提交协议状态，输入法方向的 `commit_string` 才是提交文字。

候选框还涉及显示位置。输入光标矩形属于应用的状态，合成器需要有相应接口来定位输入法弹窗；采用工具包输入模块时，也可能由应用内的 UI 显示候选框。因此，「能选词但候选框位置不对」与「按键完全没进入输入法」应从不同方向排查，前者要继续检查光标状态和候选框的显示方式。Fcitx 文档的
[Popup candidate window](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#Popup_candidate_window)专门解释了这些差异。

### 原生 Wayland 应用也可能使用输入模块

另一条路径是应用通过 GTK/Qt 的 Fcitx 输入模块与 Fcitx 通信。它并不只属于 X11：Fcitx 文档明确说明，GTK
3/4 原生 Wayland 应用既可以用 text-input，也可以使用 Fcitx
IM 模块。Qt 的选择还受版本、工具包插件和合成器支持影响。因此，我会先确认应用实际采用哪个后端和输入接口，再看环境变量；把所有 Wayland 应用都归到一种配置里，容易漏掉这层差异。

`GTK_IM_MODULE=fcitx`、`QT_IM_MODULE=fcitx`
是选择相应输入模块的设置，`XMODIFIERS=@im=fcitx`
用于 X11/XWayland 的 XIM 路径。它们不是每个应用都必须同时设置的一组开关。全局指定 IM 模块也可能使原本能用 text-input 的应用改走模块路径，候选框的实现随之变化。各工具包的条件见
[Fcitx Wayland 应用说明](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#Applications)。

Home Manager 提供了 `fcitx5.waylandFrontend` 选项。例如：

```nix
i18n.inputMethod = {
  enable = true;
  type = "fcitx5";
  fcitx5.waylandFrontend = true;
};
```

完整配置变化见[作者的修改记录](https://github.com/ryan4yin/nix-config/commit/fb0f89d975221f330f2562b11f13faa0f659b79c)。这项设置调整 Home
Manager 怎样集成 Fcitx，不能替合成器或应用补上它们不支持的协议。

对照 Home Manager 26.05 的实现，这个选项会影响模块生成的环境：启用后，模块不再自动设置全局
`GTK_IM_MODULE`、`QT_IM_MODULE`，同时为 X11 GTK 应用保留 GTK 配置入口；`XMODIFIERS`
仍然设置。见
[Home Manager Fcitx 5 模块](https://github.com/nix-community/home-manager/blob/release-26.05/modules/i18n/input-method/fcitx5.nix)。这是当前模块的实现说明，不能据此倒推历史提交当时生成的全部文件，更不能认为一个选项为合成器补齐了协议支持。

Arch 的 [fcitx5](https://archlinux.org/packages/extra/x86_64/fcitx5/)与
[fcitx5-qt](https://archlinux.org/packages/extra/x86_64/fcitx5-qt/)等包分别提供框架和集成组件；启动方式仍要对照所用桌面。例如 Fcitx 上游要求 KWin 的原生输入法路径由其虚拟键盘设置启动，以取得合成器传入的连接。换成另一种自动启动方式，并不能保证连接等价。输入法的启动方式也与[登录会话篇](/posts/linux-desktop-login-session/)讨论的进程和会话环境有关。

## 几个只读观察练习

下面的命令分别观察媒体图、字体匹配和输入法控制接口。它们不能互相代替。

### 看音频对象，而不是只数进程

在自己的桌面会话中运行：

```console
wpctl status
```

[wpctl 手册](https://pipewire.pages.freedesktop.org/wireplumber/man/wpctl.html)说明，这会列出设备、sink、source 和 stream。可以沿正在使用的应用流查看它与输出的关系。输出会含设备描述、应用名等本机信息，分享前应脱敏，因此这里不摘录笔者机器上的完整媒体图。

### 对比请求与匹配结果

```console
$ fc-match sans
SourceSans3-Regular.otf: "Source Sans 3" "Regular"

$ fc-match 'sans-serif:lang=zh-cn'
SourceSans3-Regular.otf: "Source Sans 3" "Regular"

$ fc-match 'monospace:lang=zh-cn'
MapleMono-NF-CN-Regular.ttf: "Maple Mono NF CN" "Regular"
```

[fc-match 手册](https://man.archlinux.org/man/fc-match.1.en)说明，默认输出最佳匹配的文件短名、字体族和样式。同样带
`lang=zh-cn`，请求的族名不同，匹配就可能不同。

还应注意，fontconfig 寻找的是最接近的匹配，返回一个结果并不保证满足所有条件。要确认某个中文字符最终用了什么字形，还需要观察目标应用的回退和渲染行为。本次没有用 GUI 渲染测试验证这一步，也没有遍历并发布整机字体清单。

### 查询输入法名称与验证应用输入是两件事

支持 `--check` 的版本可以这样查询已经运行的 Fcitx 5：

```console
$ fcitx5-remote --check -n
rime
```

`-n` 查询当前输入法名称；`--check` 先查服务的现有 owner，避免查询触发 D-Bus 激活。实现见
[fcitx5-remote 源码](https://github.com/fcitx/fcitx5/blob/master/src/tools/remote.cpp)。若版本没有该选项，就跳过这个练习，不把启动输入法混入观察过程。

这里的 `rime` 只说明笔者机器上当前输入法的名称。它不表示每个应用都已经建立输入上下文。

即使查询成功，它也只说明控制接口可达；某个应用是否建立输入上下文、是否送出光标状态、是否收到确认文字，还需要在那个应用里分别验证。

按这个顺序检查日常配置会更清楚：声音沿图中的连接流动，字体由应用请求与匹配规则共同选择，中文输入则随焦点建立和结束。下一篇[网络如何到达应用](/posts/linux-desktop-network/)从应用继续向外看，说明数据包怎样离开这台桌面。
