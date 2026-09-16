---
title: "Linux 桌面系统：显示、输入与图形渲染"
subtitle: ""
description:
  "沿着一次输入到画面更新的过程，理解 evdev、libinput、Wayland 合成器、Mesa 与 DRM/KMS
  的分工。"
date: 2026-09-16T01:14:00+08:00
lastmod: 2026-09-16T02:23:46+08:00
draft: false
authors: ["ryan4yin"]
tags: ["Linux", "Desktop", "Wayland", "NixOS"]
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

> AI 创作声明：本系列文章使用 gpt-5.6-sol 与 DeepSeek 4.1 Flash 辅助创作。

[登录会话篇](/posts/linux-desktop-login-session/)讲到，合成器需要在合适的会话中取得设备访问权。拿到设备之后，窗口还没有凭空出现：键鼠事件要交给应用，应用要画出内容，合成器再安排这些内容怎样出现在显示器上。

平时说「显卡驱动出问题了」，往往把好几层东西混在了一起。应用使用的图形库、内核驱动和合成器各有自己的工作。本文以普通本地 Wayland 桌面为主，沿着一次点击到画面更新的过程，把这些接口串起来。

## 从会话的设备访问权开始

在直接控制显示设备的桌面会话中，合成器需要访问输入设备及 DRM/KMS 设备。使用 logind 的实现可以通过
`TakeDevice()`
取得设备文件描述符；会话活动状态和 seat 的关系，已经在[登录会话篇](/posts/linux-desktop-login-session/)解释过。这里关心取得描述符之后的用途。Wayland 项目的[显示设备编程说明](https://wayland.freedesktop.org/docs/book/Architecture.html#display-programming)描述了这条常见路径。

下面画的是职责与数据流，不是所有程序都必须逐项调用的固定启动顺序。嵌套运行在另一个桌面窗口中的合成器，输入和输出可以来自外层窗口系统，不会照搬直接接管物理设备的路径。

```text
登录会话与设备访问管理
  └─ 合成器取得输入、显示设备访问权

键鼠 → 内核 evdev → libinput → 合成器判断焦点 → Wayland 客户端
                                                    │
                                              应用绘制 buffer
                                                    │
显示器 ← DRM/KMS ← 合成器安排输出 ← surface 状态与 buffer
```

## 内核送来输入事件，谁决定窗口收到什么

内核驱动把不同设备的输入转成 evdev 事件。常见桌面合成器通过 libinput 处理这些事件，包括指针加速、触摸板手势及设备特有的兼容处理。libinput 是合成器使用的库，普通 Wayland 应用收到的是合成器发来的协议事件，并不直接调用 libinput 读取键盘。它也不是 Wayland 协议强制要求的组件，专用合成器可以选用别的输入实现。[libinput 的职责说明](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html)给出了这层关系。

窗口的位置、缩放、遮挡和焦点由合成器掌握。鼠标在屏幕上的位置，要换算成目标 surface 内的坐标，应用才知道用户点中了哪个按钮。键盘事件则交给拥有键盘焦点的客户端。这部分可以对照 Wayland 的[输入事件流程](https://wayland.freedesktop.org/docs/book/Architecture.html#x-vs-wayland-architecture)理解。

协议里的 `wl_seat` 表示一组输入能力，客户端据此取得 `wl_pointer`、`wl_keyboard` 或
`wl_touch`。它和 logind 用于设备归属的 seat 有联系，但属于不同接口，不能把一个 Wayland 对象当成 logind
session 的替代品。键盘按键到文字、中文候选词还要经过键盘布局和输入法等处理，留到[音频、字体与输入法篇](/posts/linux-desktop-media-input/)展开。[Wayland 核心协议](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat)定义了这些输入对象。

举例来说，指针能移动、窗口也能获得焦点，却打不出中文，并不能直接归因于 evdev 没有收到按键。沿着事件实际经过的层次看，才能区分设备输入、焦点分发和文字输入。

## 合成器与客户端用 surface 交接内容

Wayland 是客户端与合成器之间的协议。在这个模型中，合成器同时承担显示服务器的工作；niri、KWin、Mutter 等是具体实现。协议约定怎样交换对象和消息，窗口布局、动画与快捷键策略仍由实现决定。

应用创建的 `wl_surface`
可以关联图像内容和输入区域，但单独创建 surface 还没有表达「这是一个普通桌面窗口」。`xdg-shell`
在它上面建立桌面窗口语义，例如 `xdg_toplevel` 和弹出菜单使用的 `xdg_popup`。参见
[xdg-shell 协议 XML（镜像）](https://raw.githubusercontent.com/wayland-mirror/wayland-protocols/main/stable/xdg-shell/xdg-shell.xml)。

buffer 保存要显示的像素，surface 保存与展示有关的状态。客户端将 buffer 附到 surface，标记哪些区域发生变化，再提交状态。`wl_surface.commit`
将待提交状态组成一次内容更新，合成器按协议约束应用它；这一请求不等于显示器已经显示了这一帧。`wl_buffer.release`
则用于通知客户端合成器不再使用这个 buffer，客户端才能据此安排复用。正式语义见[核心协议的 surface 与 buffer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface)。

图形工具包一般已经处理窗口创建、事件循环与 buffer 提交，应用不必从头实现协议。工具包选了哪个窗口后端，会影响程序实际走过的路径，所以「正在 Wayland 桌面里运行」还不足以断言一个应用就是原生 Wayland 客户端。

## 像素由应用绘制，Mesa 在哪里

应用收到点击事件后，可能要重新画一个按钮。绘制可以使用 CPU，也可以通过 OpenGL、Vulkan 等 API 使用 GPU。Mesa 提供多种图形 API 的实现和用户态驱动，也包含 LLVMpipe 这样的软件渲染器。因此，发现程序加载了 Mesa，不能直接得出它正在使用硬件加速的结论。[Mesa 的平台与驱动列表](https://docs.mesa3d.org/systems.html)同时列出了硬件、软件和建立在其他 API 之上的驱动。

在常见的硬件加速路径中，用户态驱动负责图形 API 对应的工作，并通过内核接口使用 GPU；内核 DRM 驱动负责设备侧的资源与访问管理等工作。应用用于渲染的 render
node 和合成器用于控制显示的 primary node，权限含义不同：render
node 不提供 modesetting 或其他特权 ioctl，也没有 DRM
master 的概念。参见[内核 DRM 用户态接口文档](https://docs.kernel.org/gpu/drm-uapi.html#render-nodes)。

这个区别很实用：程序能使用 GPU 计算或在屏幕之外渲染，并不意味着它有权改显示器分辨率。反过来，合成器能把桌面显示出来，也不能证明每个应用都选中了预期的 GPU 或渲染驱动。多 GPU 机器上，渲染设备与负责显示输出的设备还可能不同。

客户端与合成器可以通过 dma-buf 文件描述符共享 GPU
buffer。EGL 或 Vulkan 的窗口系统集成可以代应用完成这部分交换。共享 buffer 后仍须同步：哪一方可以写、哪一方可以读，不能只凭「提交消息已经发出」判断。具体路径可能使用隐式同步，也可能使用显式同步协议，要看客户端、合成器与驱动的支持。[Wayland 的 GPU buffer 交换说明](https://wayland.freedesktop.org/docs/book/Architecture.html#accelerated-gpu-buffer-exchange)解释了这些接口。

## 合成之后，DRM/KMS 怎样安排输出

合成器拿到各窗口的内容后，根据位置、遮挡、透明度和缩放安排最终显示。需要合成时，它可以把客户端 buffer 作为纹理，绘制输出画面。显示硬件也有自己的 plane，部分内容可以交给显示硬件组合；能否采用这样的路径取决于硬件、buffer 格式和当前场景，不能假定每一帧都经历一次完整的 GPU 桌面重绘。

DRM 的全名是 Direct Rendering Manager。KMS（Kernel Mode
Setting）是其中用于显示模式和输出配置的部分。内核用几种对象描述显示链路：

| 对象        | 可以怎样理解                              |
| ----------- | ----------------------------------------- |
| framebuffer | 描述供显示使用的图像，包括格式和存储布局  |
| plane       | 从 framebuffer 取像素，参与显示硬件的合成 |
| CRTC        | 组织显示扫描输出与时序，接收 plane 的内容 |
| connector   | 显示链路的连接端点                        |

这是便于阅读的简化，完整模型还包含 encoder 等对象。合成器通过 KMS 提交模式与 buffer 等状态；支持 atomic
modesetting 的路径把相关变更作为一组检查和提交，避免用户态逐项切换中间状态。接口与约束见[内核 KMS 概览](https://docs.kernel.org/gpu/drm-kms.html#overview)和[atomic modesetting](https://docs.kernel.org/gpu/drm-kms.html#atomic-mode-setting)。

应用窗口尺寸、合成器中的逻辑坐标与显示器实际像素，也不是同一个数值空间。缩放与旋转会影响它们的换算。`wl_output`
向客户端报告输出信息，并不提供一个任意修改显示器配置的通用按钮；实际布局配置要看合成器的配置接口。[wl_output 定义](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output)列出了它向客户端发送的信息。

所以，某个应用内容异常、所有窗口都不再刷新、外接显示器没有输出，虽然都属于「画面问题」，涉及的接口却可能相隔很远。前面的数据流能帮助缩小观察范围，但单凭症状还不能确定是哪一层出了错。

## NixOS 配置把这些组件接到哪里

作者当前的 nix-config 用 Home Manager 管理 niri 的 `config.kdl`
等配置，并在桌面会话入口中调用
`niri-session`。配置文件决定合成器怎样工作，会话入口负责把它带进用户会话；这两件事在配置仓库中有各自的位置。这里仅描述读到的实现，不把配置存在当成当前服务已经运行的证据。

对照 NixOS 26.05，`programs.niri.enable`
对应的模块会提供 niri 软件包、会话入口、systemd 集成及相关桌面服务默认配置；它还引用公共 Wayland
session 模块，启用图形桌面支持及 polkit 等集成。只安装一个 niri 可执行文件，不会自动等价于这些模块的完整结果。参见
[NixOS niri 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/programs/wayland/niri.nix)及[公共会话模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/programs/wayland/wayland-session.nix)。作者配置与发行版模块要分别阅读，具体结果还取决于使用的 Nixpkgs 版本和覆盖值。

### 一次图形选项改名留下的线索

作者配置历史中的提交 `385bcd2d` 把一台机器上的 `hardware.opengl` 改成了
`hardware.graphics`，同时把 `driSupport32Bit` 改成
`enable32Bit`，保留了启用值。去掉其他配置后，新写法是：

```nix
{
  hardware.graphics = {
    enable = true;
    enable32Bit = true;
  };
}
```

这是一条配置迁移记录，没有附带黑屏、崩溃或性能测试日志，不应把它包装成一次显卡故障修复。它适合说明另一件事：选项的名字与它提供的运行环境要分开理解。

NixOS 26.05 的
[graphics 模块](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/hardware/graphics.nix)仍保留上述旧名到新名的映射。模块默认使用 Mesa 驱动包，并建立驱动查找路径；`enable32Bit`
为需要的 32 位应用提供对应用户态驱动，在这里有 x86_64 平台和内核 32 位兼容支持的断言。这段配置不能不看平台就照搬，也不能代替特定 GPU 的内核驱动配置。

### Arch 上对应的实现

Arch 同样需要合成器、用户态图形驱动与内核显示接口配合。差别在组件的安装和配置入口：niri 的[上游入门文档](https://github.com/niri-wm/niri/wiki/Getting-Started)列出了 Arch 软件包，并说明可从显示管理器选择会话；不用显示管理器时，systemd 环境使用
`niri-session`。这里不列安装或切换会话命令，已有桌面不需要为理解机制而退出重来。

阅读 Arch 资料时，把所需组件对应回前面的职责即可。NixOS 模块提供的一组集成，在 Arch 上由软件包内容、会话入口和自己的配置共同完成。不同合成器对扩展协议、输入设置与多显示器配置的支持也不一样，不能把 niri 的选项搬给 KWin 或 Mutter。

## XWayland 补上哪一段

X11 应用可以连接 XWayland；XWayland 对它们是 X
server，对外则作为 Wayland 客户端连接合成器。于是同一个 Wayland 桌面上，可以同时看到原生 Wayland 窗口和 X11 窗口。具体启动与窗口管理集成由合成器及配套组件决定。[Wayland 的 X11 支持说明](https://wayland.freedesktop.org/docs/book/Xwayland.html)描述了这个关系。

这种兼容不会把 X11 客户端之间的访问模型自动改造成 Wayland 的模型；共享同一个 XWayland 实例的 X11 应用仍保留相互通信的能力。Wayland 本身也不等于应用沙盒。应用要请求屏幕共享或其他桌面资源时，还会涉及专门接口与权限策略，接着看[桌面应用、portal 与沙盒](/posts/linux-desktop-app-integration/)。

## 在自己的桌面上观察两条连接

下面两条只查询信息，应在自己的图形会话中执行。完整输出可能包含显示设备或驱动信息，公开分享前先筛选必要字段。

```console
wayland-info -i xdg_wm_base
glxinfo -B
```

第一条向所连接的合成器查询已公布的 Wayland globals，并只显示名称包含 `xdg_wm_base`
的项。它能帮助确认这一连接上公布的协议及版本，不能证明每个扩展功能都正常，也不能证明另一个应用连接了同一个合成器。[Arch 提供的 wayland-info 手册](https://man.archlinux.org/man/wayland-info.1.en)说明了过滤选项；Arch 中工具来自
`wayland-utils` 包。

第二条查看当前 X display 上的 OpenGL/GLX 实现，`-B`
请求简要输出。在 Wayland 桌面中，它通常观察 XWayland 提供的 GLX 路径，不能替原生 Wayland 或 Vulkan 程序报告渲染器。[glxinfo 手册](https://manpages.debian.org/testing/mesa-utils/glxinfo.1.en.html)解释了查询对象；本地
`glxinfo -h` 也确认了 `-B`
的含义。显示连接失败时，先检查这个进程能否访问目标显示服务，不能直接判断 GPU 驱动损坏。

若还需要对照会话层，先按[登录会话篇](/posts/linux-desktop-login-session/)确认目标 session，再查询它的
`Type`、`Active` 等属性。本次写作在已有明确 session ID 的前提下执行了带独立 `-p` 选项的
`loginctl show-session`，返回 `Operation not permitted`；没有读到会话状态。

本次环境没有安装 `wayland-info`，因此未执行协议查询；`glxinfo -B`
实际返回无法打开 display，退出码为 255。这些结果只说明本文的运行环境没有完成相应观察，没有验证当前桌面的 GPU、协议支持或显示输出。也没有为补齐结果而安装软件、切换会话或重启合成器。

输入事件、客户端内容和显示输出的关系到这里接上了。接下来还要解释，桌面如何找到并启动应用，以及应用怎样请求文件选择、屏幕共享等服务。这部分在[桌面应用篇](/posts/linux-desktop-app-integration/)继续；设备事件与进程通信的基础可回看[系统基础篇](/posts/linux-desktop-system-foundations/)。
