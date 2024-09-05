---
title: "NixOS 在 Lichee Pi 4A 上是如何启动的"
subtitle: ""
description: ""
date: 2024-01-29T00:58:57+08:00
lastmod: 2024-01-29T00:58:57+08:00
draft: false

resources:
  - name: "featured-image"
    src: "lp4a-pinout-debuglog-1.webp"

tags: ["Linux", "NixOS", "LicheePi4A", "Embedded", "U-Boot", "RISC-V"]
categories: ["tech"]
series: ["NixOS 与 Nix Flakes"]

hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

toc:
  enable: true
math:
  enable: false
license: ""

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false

code:
  # whether to show the copy button of the code block
  copy: true
  # the maximum number of lines of displayed code by default
  maxShownLines: 300
---

> 文章是 2023-08-07 写的，后面就完全忘掉这回事了，今天偶然翻到它才想起要整理发布下...所以
> 注意文章中的时间线是 2023 年 8 月。

## 零、前言

我从今年 5 月份初收到了内测板的 Lichee Pi 4A，这是当下性能最高的 RISC-V 开发板之一，不过当
时没怎么折腾。

6 月初的时候我开始尝试在 Orange Pi 5 上运行 NixOS，在
[NixOS on ARM 的 Matrix 群组](https://matrix.to/#/#nixos-on-arm:nixos.org) 中得到了俄罗斯
老哥 @K900 的帮助，没费多大劲就成功了，一共就折腾了三天。

于是我接着尝试在 Lichee Pi 4A 上运行 NixOS，因为已经拥有了 Orange Pi 5 上的折腾经验，我以
为这次会很顺利。但是实际难度远远超出了我的预期，我从 6 月 13 号开始断断续续折腾到 7 月 3
号，接触了大量的新东西，包括 U-Boot、OpenSBI、SPL Flash、RISCV Boot Flows 等等，还参考了
@chainsx 的 Fedora for Lichee Pi 4A 方案，请教了 @NickCao 许多 NixOS 相关的问题，@revy 帮
我修了好几个 revyos/thead-kernel 在标准工具链上编译的 bug，期间也请教过 @HougeLangley 他折
腾 Lichee Pi 4A 的经验。我在付出了这么多的努力后，才最终成功编译出了 NixOS 的系统镜像（包
含 boot 跟 rootfs 两个分区）。

但是！现在要说「但是」了。

镜像是有了，系统却无法启动...找了各种资料也没解决，也没好意思麻烦各位大佬，搞得有点心灰意
冷，就先把这部分工作放下了。

接着就隔了一个多月没碰 Lichee Pi 4A，直到 8 月 5 号，外国友人 @JayDeLux 在
[Mainline Linux for RISC-V](https://t.me/linux4rv) TG 群组中询问我 NixOS 移植工作的进展如
何（之前有在群里提过我在尝试移植），我才决定再次尝试一下。

在之前工作的基础上一番骚操作后，我在 8 月 6 号晚上终于成功启动了 NixOS，这次意外的顺利，后
续也成功通过一份 Nix Flake 配置编译出了可用的 NixOS 镜像。

最终成果：<https://github.com/ryan4yin/nixos-licheepi4a>

整个折腾过程相当曲折，虽然最终达成了目标，但是期间遭受的折磨也真的不少。总的来说仍然是一次
很有趣的经历，既学到了许多新技术知识、认识了些有趣的外国友人（@JayDeLux 甚至还给我打了 $50
美刀表示感谢），也跟 @HougeLangley 、@chainsx 、@Rabenda(revy) 等各位大佬混了个脸熟。

这篇文章就是记录下我在这个折腾过程中学到的所有知识，以飨读者，同时也梳理一下自己的收获。

本文的写作思路是自顶向下的，先从 NixOS 镜像的 boot 分区配置、启动脚本开始分析，过渡到实际
的启动日志，再接续分析下后续的启动流程。NixOS 分析完了后，再看看与 RISC-V 相关的硬件固件与
bootloader 部分要如何与 NixOS 协同工作，使得 NixOS 能够在 Lichee Pi 4A 上正常启动。

## 一、基础知识介绍

### 1. Lichee Pi 4A 介绍

LicheePi 4A 是当前市面上性能最高的 RISC-V Linux 开发板之一，它以 TH1520 为主控核心
（4xC910@1.85G， RV64GCV，4TOPS@int8 NPU， 50GFLOP GPU），板载最大 16GB 64bit
LPDDR4X，128GB eMMC，支持 HDMI+MIPI 双4K 显示输出，支持 4K 摄像头接入，双千兆网口（其中一
个支持POE供电）和 4 个 USB3.0 接口，多种音频输入输出（由专用 C906 核心处理）。

以上来自 Lichee Pi 4A 官方文档
[Lichee Pi 4A - Sipeed Wiki](https://wiki.sipeed.com/hardware/zh/lichee/th1520/lpi4a/1_intro.html).

总之它是我手上性能最高的 RISC-V 开发板。

LicheePi 4A 官方主要支持 [RevyOS](https://github.com/revyos/revyos/)—— 一款针对 T-Head 芯
片生态的 Debian 优化定制发行版。根据猴哥（@HougeLangley）文章介绍，它也是目前唯一且确实能
够启用 Lichee Pi 4A 板载 GPU 的发行版，

### 2. NixOS 介绍

这个感觉就不用多说了，我在这几个月已经给 NixOS 写了非常多的文字了，感兴趣请直接移步
[ryan4yin/nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book).

在 4 月份接触了 NixOS 后，我成了 NixOS 铁粉。作为一名铁粉，我当然想把我手上的所有性能好点
的板子都装上 NixOS，Lichee Pi 4A 自然也不例外。

我目前主要完成了两块板子的 NixOS 移植工作，一块是 Orange Pi 5，另一块就是 Lichee Pi 4A。
Orange Pi 5 是 ARM64 架构的，刚好也遇到了拥有该板子的 NixOS 用户 @K900，在他的帮助下我很顺
利地就完成了移植工作。

而 Lichee Pi 4A 就比较曲折，也比较有话题性。所以才有了这篇文章。

## 二、移植思路

一个完整的嵌入式 Linux 系统，通常包含了 U-Boot、kernel、设备树以及根文件系统（rootfs）四个
部分。

其中 U-Boot，kernel 跟设备树，都是与硬件相关的，需要针对不同的硬件进行定制。而 rootfs 的大
部分内容（比如说 NixOS 系统的 rootfs 本身），都是与硬件无关的，可以通用。

我的移植思路是，从 LicheePi4A 官方使用的 RevyOS 中拿出跟硬件相关的部分（也就是 U-Boot,
kernel 跟设备树这三个），再结合上跟硬件无关的 NixOS rootfs，组合成一个完整的、可在
LicheePi4A 上正常启动运行的 NixOS 系统。

RevyOS 针对 LicheePi4A 定制的几个项目源码如下：

- https://github.com/revyos/thead-kernel.git
- https://github.com/revyos/thead-u-boot.git
- https://github.com/revyos/thead-opensbi.git

思路很清晰，但因为 NixOS 本身的特殊性，实际操作起来，现有的 Gentoo, Arch Linux, Fedora 的
移植仓库代码全都无法直接使用，需要做的工作还是不少的。

## 三、NixOS 启动流程分析

要做移植，首先就要了解 NixOS 系统本身的文件树结构以及系统启动流程，搞明白它跟 Arch Linux,
Fedora 等其他发行版的区别，这样才好参考其他发行版的移植工作，搞明白该如何入手。

### 1. Bootloader 配置与系统文件树分析

这里方便起见，我直接使用我自己为 LicheePi4A 构建好的 NixOS 镜像进行分析。首先参照
[ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a) 的 README 下载解
压镜像，再使用 losetup 跟 mount 直接挂载镜像中的各分区进行初步分析：

```bash
# 解压镜像
› mv nixos-licheepi4a-sd-image-*-riscv64-linux.img.zst nixos-lp4a.img.zst
› zstd -d nixos-lp4a.img.zst
# 将 img 文件作为虚拟 loop 设备连接到系统中
› sudo losetup --find --partscan nixos-lp4a.img
# 查看挂载的 loop 设备
› lsblk | grep loop
loop0               7:0    0  1.9G  0 loop
├─loop0p1         259:8    0  200M  0 part
└─loop0p2         259:9    0  1.7G  0 part
# 分别挂载镜像中的 boot 跟 rootfs 分区
› mkdir boot root
› sudo mount /dev/loop0p1 boot
› sudo mount /dev/loop0p2 root
# 查看 boot 分区内容
› ls boot/
╭───┬───────────────────────────┬──────┬─────────┬──────────────╮
│ # │           name            │ type │  size   │   modified   │
├───┼───────────────────────────┼──────┼─────────┼──────────────┤
│ 0 │ boot/extlinux             │ dir  │  4.1 KB │ 44 years ago │
│ 1 │ boot/fw_dynamic.bin       │ file │ 85.9 KB │ 24 years ago │
│ 2 │ boot/light_aon_fpga.bin   │ file │ 50.3 KB │ 24 years ago │
│ 3 │ boot/light_c906_audio.bin │ file │ 16.4 KB │ 24 years ago │
│ 4 │ boot/nixos                │ dir  │  4.1 KB │ 44 years ago │
╰───┴───────────────────────────┴──────┴─────────┴──────────────╯
# 查看 root 分区内容
› ls root/
╭───┬────────────────────────────┬──────┬──────────┬──────────────╮
│ # │            name            │ type │   size   │   modified   │
├───┼────────────────────────────┼──────┼──────────┼──────────────┤
│ 0 │ root/boot                  │ dir  │   4.1 KB │ 54 years ago │
│ 1 │ root/lost+found            │ dir  │  16.4 KB │ 54 years ago │
│ 2 │ root/nix                   │ dir  │   4.1 KB │ 54 years ago │
│ 3 │ root/nix-path-registration │ file │ 242.0 KB │ 54 years ago │
╰───┴────────────────────────────┴──────┴──────────┴──────────────╯
```

可以看到 NixOS 整个根目录（`/root`）下一共就四个文件夹，其中真正保存有系统数据的文件夹只有
`/boot` 跟 `/nix` 这两个，这与传统的 Linux 发行版大相径庭。有一点 Linux 使用经验的朋友都应
该清楚，传统的 Linux 发行版遵循 UNIX 系统的
[FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) 标准，根目录下会有很多
文件夹，比如
`/bin`、`/etc`、`/home`、`/lib`、`/opt`、`/root`、`/sbin`、`/srv`、`/tmp`、`/usr`、`/var`
等等。

那 NixOS 它这么玩，真的能正常启动么？这就是我在构建出镜像后却发现无法在 LicheePi 4A 上启动
时，最先产生的疑问。在询问 @chainsx 跟 @revy 系统无法启动的解决思路的时候，他们也一脸懵
逼，觉得这个文件树有点奇葩，很怀疑是我构建流程有问题导致文件树不完整。

但实际上 NixOS 就是这么玩的，它 rootfs 中所有的数据全都存放在 `/nix/store` 这个目录下并且
被挂载为只读，其他的文件夹以及其中的文件都是在运行时动态创建的。这是它实现声明式系统配置、
可回滚更新、可并行安装多个版本的软件包等等特性的基础。

下面继续分析，先仔细看下 `/boot` 的内容：

```bash
› tree boot
boot
├── extlinux
│   └── extlinux.conf
├── fw_dynamic.bin
├── light_aon_fpga.bin
├── light_c906_audio.bin
└── nixos
    ├── 2n6fjh4lhzaswbyacaf72zmz6mdsmm8l-initrd-k-riscv64-unknown-linux-gnu-initrd
    ├── l18cz7jd37n35dwyf8wc8divm46k7sdf-k-riscv64-unknown-linux-gnu-dtbs
    │   ├── sifive
    │   │   └── hifive-unleashed-a00.dtb
    │   └── thead
    │       ├── fire-emu-crash.dtb
    │       ├── fire-emu.dtb
    │       ├── ...... (省略)
    │       ├── light-fm-emu-audio.dtb
    │       ├── light-fm-emu-dsi0-hdmi.dtb
    │       ├── light-fm-emu-dsp.dtb
    │       ├── light-fm-emu-gpu.dtb
    │       ├── light-fm-emu-hdmi.dtb
    │       ├── light-lpi4a-ddr2G.dtb
    │       └── light_mpw.dtb
    └── l18cz7jd37n35dwyf8wc8divm46k7sdf-k-riscv64-unknown-linux-gnu-Image

6 directories, 64 files
```

可以看到：

1. 它使用 `/boot/extlinux/extlinux.conf` 作为 U-Boot 的启动项配置，据
   [U-Boot 官方的 Distro 文档](https://github.com/ARM-software/u-boot/blob/master/doc/README.distro)
   所言，这是 U-Boot 的标准配置文件。
2. 另外还有一些 `xxx.bin` 文件，这些是一些硬件固件，其中的 `light_c906_audio.bin` 显然
   是[玄铁 906](https://www.t-head.cn/product/C906?lang=zh) 这个 IP 核的音频固件，其他的后
   面再研究。
3. NixOS 的 `initrd`, `dtbs` 以及 `Image` 文件都是在 `/boot/nixos` 下，这三个文件也都是跟
   Linux 的启动相关的，现在不用管它们，下一步会分析。

再看下 `/boot/extlinux/extlinux.conf` 的内容：

```bash
› cat boot/extlinux/extlinux.conf
# Generated file, all changes will be lost on nixos-rebuild!

# Change this to e.g. nixos-42 to temporarily boot to an older configuration.
DEFAULT nixos-default

MENU TITLE ------------------------------------------------------------
TIMEOUT 50

LABEL nixos-default
  MENU LABEL NixOS - Default
  LINUX ../nixos/l18cz7jd37n35dwyf8wc8divm46k7sdf-k-riscv64-unknown-linux-gnu-Image
  INITRD ../nixos/2n6fjh4lhzaswbyacaf72zmz6mdsmm8l-initrd-k-riscv64-unknown-linux-gnu-initrd
  APPEND init=/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b/init console=ttyS0,115200 root=UUID=14e19a7b-0ae0-484d-9d54-43bd6fdc20c7 rootfstype=ext4 rootwait rw earlycon clk_ignore_unused eth=$ethaddr rootrwoptions=rw,noatime rootrwreset=yes loglevel=4
  FDT ../nixos/l18cz7jd37n35dwyf8wc8divm46k7sdf-k-riscv64-unknown-linux-gnu-dtbs/thead/light-lpi4a.dtb
```

从上述配置中能获得这些信息：

1. 它创建了一个名为 `nixos-default` 的启动项并将它设为了默认启动项，extlinux 在启动阶段会
   根据该配置启动 NixOS 系统
2. 启动项中的 `LINUX` `INITRD` `FDT` 三个参数分别指定了 kernel(Image 文件)、initrd 以及设
   备树（dtb）的位置，这三个文件我们在前面已经看到了，都在 `/boot/nixos` 下。
   1. 根据 Linux 官方文档
      [Using the initial RAM disk (initrd)](https://docs.kernel.org/admin-guide/initrd.html)
      所言，在使用了 initrd 这个内存盘的情况下，Linux 的启动流程如下：
      1. bootloader(这里是 u-boot) 根据配置加载 kernel 文件（`Image`）、dtb 设备树文件以及
         `initrd` 文件系统，然后以设备树跟 initrd 的地址为参数启动 Kernel.
      1. Kernel 将传入的 initrd 转换成一个内存盘并挂载为根文件系统，然后释放 initrd 的内
         存。
      1. Kernel 接着运行 `init` 参数指定的可执行程序，这里是
         `/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b/init`，
         这个 init 程序会挂载真正的根文件系统，并在其上执行后续的启动流程。
      1. initrd 文件系统被移除，系统启动完毕。
   1. `initrd` 这样一个临时的内存盘，通常用于在系统启动阶段加载一些内核中未内置但启动却必
      需的驱动或数据文件供 `init` 程序使用，以便后续能够挂载真正的根文件系统。
      1. 比如说挂载一个 LUKS 加密的根文件系统，这通常会涉及到提示用户输入 passphrase、从某
         个地方读取解密用的 keyfile 或者与插入的 USB 硬件密钥交互，这会需要读取内核之外的
         keyfile 文件、用到内核之外的加密模块、USB 驱动、HID 用户输入输出模块或者其他因为
         许可协议、模块大小等问题无法被静态链接到内核中的各种内核模块或程序。initrd 就是用
         来解决这些问题的。
3. `APPEND` 参数包含有许多关键信息：
   1. 系统的 init 程序，也就是传说中的 1 号进程（PID 1），被设置为
      `/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b/init`，
      这实际是一个 shell 脚本，我们下一步会重点分析它。
      1. 在传统的 Linux 发行版中，init 通常使用默认值 `/sbin/init`，它会被链接到
         `/lib/systemd/systemd`，也就是直接使用 systemd 作为 1 号进程。你可以在
         Fedora/Ubuntu 等传统发行版中运行 `ls -al /sbin/init` 确认这一点，以及检查它们的
         `/boot/grub/grub.cfs` 启动项配置，看看它们有无自定义内核的 `init` 参数。
   1. 系统的 rootfs 分区为 `/dev/disk/by-uuid/14e19a7b-0ae0-484d-9d54-43bd6fdc20c7`，使用
      的文件系统为 ext4.
   1. `earlycon`(early console) 表示在系统启动早期就启用控制台输出，这样可以在系统启动阶段
      通过 UAER/HDMI 等接口看到相关的启动日志，方便调试。
   1. 其他参数先不管。

这样一分析就能得出结论：在执行 `init` 程序之前的启动流程都未涉及到真正的根文件系统，NixOS
与其他发行版在该流程中并无明显差异。

### 2. 实际启动日志分析

为了方便后续内容的理解，先看下 NixOS 系统在 LicheePi 4A 上的实际启动日志是个很不错的选择。

按我项目中的 README 正常烧录好系统后，使用 USB 转串口工具连接到 LicheePi 4A 的 UART0 串
口，然后启动系统，就能看到 NixOS 的启动日志。

接线示例：

{{<figure src="./lp4a-pinout-debuglog-1.webp" title="LicheePi4A UART 调试接线 - 正面" width="80%">}}
{{<figure src="./lp4a-pinout-debuglog-2.webp" title="LicheePi4A UART 调试接线 - 反面" width="80%">}}

接好线后使用 minicom 查看日志：

```bash
› ls /dev/ttyUSB0
╭───┬──────────────┬─────────────┬──────┬───────────────╮
│ # │     name     │    type     │ size │   modified    │
├───┼──────────────┼─────────────┼──────┼───────────────┤
│ 0 │ /dev/ttyUSB0 │ char device │  0 B │ 6 minutes ago │
╰───┴──────────────┴─────────────┴──────┴───────────────╯

› minicom -d /dev/ttyusb0 -b 115200
```

一个正常的启动日志示例如下：

```
Welcome to minicom 2.8
brom_ver 8
[APP][E] protocol_connect failed, exit.
OpenSBI v0.9
   ____                    _____ ____ _____
  / __ \                  / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|____/_____|
        | |
        |_|

Platform Name             : T-HEAD Light Lichee Pi 4A configuration for 8GB DDR board
Platform Features         : mfdeleg
Platform HART Count       : 4
Platform IPI Device       : clint
Platform Timer Device     : clint
Platform Console Device   : uart8250
Platform HSM Device       : ---
Platform SysReset Device  : thead_reset
Firmware Base             : 0x0
Firmware Size             : 132 KB
Runtime SBI Version       : 0.3

Domain0 Name              : root
Domain0 Boot HART         : 0
Domain0 HARTs             : 0*,1*,2*,3*
Domain0 Region00          : 0x000000ffdc000000-0x000000ffdc00ffff (I)
Domain0 Region01          : 0x0000000000000000-0x000000000003ffff ()
Domain0 Region02          : 0x0000000000000000-0xffffffffffffffff (R,W,X)
Domain0 Next Address      : 0x0000000000200000
Domain0 Next Arg1         : 0x0000000001f00000
Domain0 Next Mode         : S-mode
Domain0 SysReset          : yes

Boot HART ID              : 0
Boot HART Domain          : root
Boot HART ISA             : rv64imafdcvsux
Boot HART Features        : scounteren,mcounteren,time
Boot HART PMP Count       : 0
Boot HART PMP Granularity : 0
Boot HART PMP Address Bits: 0
Boot HART MHPM Count      : 16
Boot HART MHPM Count      : 16
Boot HART MIDELEG         : 0x0000000000000222
Boot HART MEDELEG         : 0x000000000000b109
[    0.000000] Linux version 5.10.113 (nixbld@localhost) (riscv64-unknown-linux-gnu-gcc (GCC) 13.1.0, GN0
[    0.000000] OF: fdt: Ignoring memory range 0x0 - 0x200000
[    0.000000] earlycon: uart0 at MMIO32 0x000000ffe7014000 (options '115200n8')
[    0.000000] printk: bootconsole [uart0] enabled
[    2.292495] (NULL device *): failed to find vdmabuf_reserved_memory node
[    2.453953] spi-nor spi0.0: unrecognized JEDEC id bytes: ff ff ff ff ff ff
[    2.460971] dw_spi_mmio ffe700c000.spi: cs1 >= max 1
[    2.466001] spi_master spi0: spi_device register error /soc/spi@ffe700c000/spidev@1
[    2.497453] sdhci-dwcmshc ffe70a0000.sd: can't request region for resource [mem 0xffef014064-0xffef01]
[    2.509014] misc vhost-vdmabuf: failed to find vdmabuf_reserved_memory node
[    3.386036] debugfs: File 'SDOUT' in directory 'dapm' already present!
[    3.392692] debugfs: File 'Playback' in directory 'dapm' already present!
[    3.399524] debugfs: File 'Capture' in directory 'dapm' already present!
[    3.406262] debugfs: File 'Playback' in directory 'dapm' already present!
[    3.413067] debugfs: File 'Capture' in directory 'dapm' already present!
[    3.425466] aw87519_pa 5-0058: aw87519_parse_dt: no reset gpio provided failed
[    3.432752] aw87519_pa 5-0058: aw87519_i2c_probe: failed to parse device tree node

<<< NixOS Stage 1 >>>

running udev...
Starting systemd-udevd version 253.6
kbd_mode: KDSKBMODE: Inappropriate ioctl for device
Gstarting device mapper and LVM...
checking /dev/disk/by-label/NIXOS_SD...
fsck (busybox 1.36.1)
[fsck.ext4 (1) -- /mnt-root/] fsck.ext4 -a /dev/disk/by-label/NIXOS_SD
NIXOS_SD: recovering journal
NIXOS_SD: clean, 148061/248000 files, 818082/984159 blocks
mounting /dev/disk/by-label/NIXOS_SD on /...

<<< NixOS Stage 2 >>>

running activation script...
setting up /etc...
++ /nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/findm/
+ rootPart=/dev/disk/by-label/NIXOS_SD
++ lsblk -npo PKNAME /dev/disk/by-label/NIXOS_SD
+ bootDevice=/dev/mmcblk1
++ lsblk -npo MAJ:MIN /dev/disk/by-label/NIXOS_SD
++ /nix/store/zag1z2yvsh2ccpsbgsda7xhv4sfha7mj-gawk-riscv64-unknown-linux-gnu-5.2.1/bin/awk -F: '{print '
+ partNum='26 '
+ echo ,+,
+ sfdisk -N26 --no-reread /dev/mmcblk1
GPT PMBR size mismatch (8332023 != 122894335) will be corrected by write.
The backup GPT table is not on the end of the device. This problem will be corrected by write.
warning: /dev/mmcblk1: partition 26 is not defined yet
Disk /dev/mmcblk1: 58.6 GiB, 62921900032 bytes, 122894336 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 58B10C85-BB4D-F94A-9194-82020FC9DC23

Old situation:

Device          Start     End Sectors  Size Type
/dev/mmcblk1p1  16384  425983  409600  200M Microsoft basic data
/dev/mmcblk1p2 425984 8331990 7906007  3.8G Linux filesystem

/dev/mmcblk1p26: Created a new partition 3 of type 'Linux filesystem' and of size 54.6 GiB.

New situation:
Disklabel type: gpt
Disk identifier: 58B10C85-BB4D-F94A-9194-82020FC9DC23

Device           Start       End   Sectors  Size Type
/dev/mmcblk1p1   16384    425983    409600  200M Microsoft basic data
/dev/mmcblk1p2  425984   8331990   7906007  3.8G Linux filesystem
/dev/mmcblk1p3 8333312 122892287 114558976 54.6G Linux filesystem

The partition table has been altered.
Calling ioctl() to re-read partition table.
Re-reading the partition table failed.: Device or resource busy
The kernel still uses the old table. The new table will be used at the next reboot or after you run part.
Syncing disks.
+ /nix/store/wm9ynqbkqi7gagggb4y6f4l454kkga32-parted-riscv64-unknown-linux-gnu-3.6/bin/partprobe
+ /nix/store/yln7ma9dldr3f2dva4l0iq275s4brxml-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/resize2D
resize2fs 1.46.6 (1-Feb-2023)
Filesystem at /dev/disk/by-label/NIXOS_SD is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/disk/by-label/NIXOS_SD is now 988250 (4k) blocks long.

+ /nix/store/f5w7dd1f195bxkashhr5x0a788nxrxvc-nix-riscv64-unknown-linux-gnu-2.13.3/bin/nix-store --load-b
+ touch /etc/NIXOS
+ /nix/store/f5w7dd1f195bxkashhr5x0a788nxrxvc-nix-riscv64-unknown-linux-gnu-2.13.3/bin/nix-env -p /nix/vm
+ rm -f /nix-path-registration
starting systemd...

Welcome to NixOS 23.05 (Stoat)!

[  OK  ] Created slice Slice /system/getty.
[  OK  ] Created slice Slice /system/modprobe.
[  OK  ] Created slice Slice /system/serial-getty.......
......
```

简单总结下日志中的信息：

1. 整个启动流程被分成了三个阶段，分别是：
   1. OpenSBI: 这个阶段貌似进行了一些硬件相关的初始化，比如说串口、SPI、SD 卡等，貌似还有
      些报错，先不管。
   1. NixOS Stage 1: 这应该就是 `initrd` 阶段干的活，内核加载了 systemd udev 内核模块，然
      后使用 busybox 的 fsck 检查了根文件系统，接着挂载了根文件系统。
   1. NixOS Stage 2:
      1. 运行了一个什么`activation script`，它首先设置好了 `/etc` 文件夹，然后检查了根分区
         文件系统的情况，并自动执行了分区与文件系统的扩容操作。
      2. 接着通过 `nix-env -p /nix/vm...` 大概是切换了个运行环境。
      3. 最后启动了 systemd，这之后的流程就跟其他发行版没啥区别了（都是 systemd）。

### 3. init 程序分析

有了上面这些信息，我们就可以比较容易地理解 init 这个程序了，它主要对应前面日志中的 NixOS
Stage 2，即在真正挂载根文件系统之后，执行的第一个用户态程序。

在 NixOS 中这个 init 程序实际上是一个 shell 脚本，可以直接通过 `cat` 或者 `vim` 来查看它的
内容：

```bash
› cat /nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37/init
#! /nix/store/91hllz70n1b0qkb0r9iw1bg9xzx66a3b-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash

systemConfig=/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b

export HOME=/root PATH="/nix/store/fifbf1h3i83jvan2vkk7xm4fraq7drm7-coreutils-riscv64-unknown-linux-gnu-9.1/bin:/nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin"


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Process the kernel command line.
    for o in $(</proc/cmdline); do
        case $o in
            boot.debugtrace)
                # Show each command.
                set -x
                ;;
        esac
    done


    # Print a greeting.
    echo
    echo -e "\e[1;32m<<< NixOS Stage 2 >>>\e[0m"
    echo


    # Normally, stage 1 mounts the root filesystem read/writable.
    # However, in some environments, stage 2 is executed directly, and the
    # root is read-only.  So make it writable here.
    if [ -z "$container" ]; then
        mount -n -o remount,rw none /
    fi
fi


# Likewise, stage 1 mounts /proc, /dev and /sys, so if we don't have a
# stage 1, we need to do that here.
if [ ! -e /proc/1 ]; then
    specialMount() {
        local device="$1"
        local mountPoint="$2"
        local options="$3"
        local fsType="$4"

        # We must not overwrite this mount because it's bind-mounted
        # from stage 1's /run
        if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" = true ] && [ "${mountPoint}" = /run ]; then
            return
        fi

        install -m 0755 -d "$mountPoint"
        mount -n -t "$fsType" -o "$options" "$device" "$mountPoint"
    }
    source /nix/store/vn0sga6rn69vkdbs0d2njh0aig7zmzi6-mounts.sh
fi


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" = true ]; then
    echo "booting system configuration ${systemConfig}"
else
    echo "booting system configuration $systemConfig" > /dev/kmsg
fi


# Make /nix/store a read-only bind mount to enforce immutability of
# the Nix store.  Note that we can't use "chown root:nixbld" here
# because users/groups might not exist yet.
# Silence chown/chmod to fail gracefully on a readonly filesystem
# like squashfs.
chown -f 0:30000 /nix/store
chmod -f 1775 /nix/store
if [ -n "1" ]; then
    if ! [[ "$(findmnt --noheadings --output OPTIONS /nix/store)" =~ ro(,|$) ]]; then
        if [ -z "$container" ]; then
            mount --bind /nix/store /nix/store
        else
            mount --rbind /nix/store /nix/store
        fi
        mount -o remount,ro,bind /nix/store
    fi
fi


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Use /etc/resolv.conf supplied by systemd-nspawn, if applicable.
    if [ -n "" ] && [ -e /etc/resolv.conf ]; then
        resolvconf -m 1000 -a host </etc/resolv.conf
    fi


    # Log the script output to /dev/kmsg or /run/log/stage-2-init.log.
    # Only at this point are all the necessary prerequisites ready for these commands.
    exec {logOutFd}>&1 {logErrFd}>&2
    if test -w /dev/kmsg; then
        exec > >(tee -i /proc/self/fd/"$logOutFd" | while read -r line; do
            if test -n "$line"; then
                echo "<7>stage-2-init: $line" > /dev/kmsg
            fi
        done) 2>&1
    else
        mkdir -p /run/log
        exec > >(tee -i /run/log/stage-2-init.log) 2>&1
    fi
fi


# Required by the activation script
install -m 0755 -d /etc /etc/nixos
install -m 01777 -d /tmp


# Run the script that performs all configuration activation that does
# not have to be done at boot time.
echo "running activation script..."
$systemConfig/activate


# Record the boot configuration.
ln -sfn "$systemConfig" /run/booted-system


# Run any user-specified commands.
/nix/store/91hllz70n1b0qkb0r9iw1bg9xzx66a3b-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash /nix/store/cmvnjz39iq4bx4cq3lvri2jj0sjq5h24-local-cmds


# Ensure systemd doesn't try to populate /etc, by forcing its first-boot
# heuristic off. It doesn't matter what's in /etc/machine-id for this purpose,
# and systemd will immediately fill in the file when it starts, so just
# creating it is enough. This `: >>` pattern avoids forking and avoids changing
# the mtime if the file already exists.
: >> /etc/machine-id


# No need to restore the stdout/stderr streams we never redirected and
# especially no need to start systemd
if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Reset the logging file descriptors.
    exec 1>&$logOutFd 2>&$logErrFd
    exec {logOutFd}>&- {logErrFd}>&-


    # Start systemd in a clean environment.
    echo "starting systemd..."
    exec /run/current-system/systemd/lib/systemd/systemd "$@"
fi
```

简单总结下这个脚本的功能：

1. 通过 `mount -o remount,ro,bind /nix/store` 将 `/nix/store` 目录重新挂载为只读，确保 Nix
   Store 的不可变性，从而使系统状态可复现。
2. 直接开始执行 `$systemConfig/activate` 这个程序。
3. activate 完毕后，启动真正的 1 号进程 systemd，进入后续启动流程。

### 4. activate 程序分析

前面的 init 程序其实没干啥，根据我们看过的启动日志，大部分的功能应该都是在
`$systemConfig/activate` 这个程序中完成的。

再看看其中的 $systemConfig/activate 的内容，它同样是一个 shell 脚本，直接 `cat`/`vim` 查看
下：

```bash
› cat root/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b/activate
#!/nix/store/91hllz70n1b0qkb0r9iw1bg9xzx66a3b-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash

systemConfig='/nix/store/71wh9lvf94i1jcd6qpqw228fy5s8fv24-nixos-system-lp4a-23.05.20230806.240472b'

export PATH=/empty
for i in /nix/store/fifbf1h3i83jvan2vkk7xm4fraq7drm7-coreutils-riscv64-unknown-linux-gnu-9.1 /nix/store/x3hfwbwcqgl9zpqrk8kvm3p2kjns9asm-gnugrep-riscv64-unknown-linux-gnu-3.7 /nix/store/qn0yhj5d7r432rdh1885cn40gz184ww9-findutils-riscv64-unknown-linux-gnu-4.9.0 /nix/store/slwk77dzar2l1c4h9fikdw93ig4wdfy1-getent-glibc-riscv64-unknown-linux-gnu-2.37-8 /nix/store/yrf57f5h1rwmf3q70msx35a2p9f0rsjr-glibc-riscv64-unknown-linux-gnu-2.37-8-bin /nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13 /nix/store/2imxx6v9xhy8mbbx9q1r2d991m81inar-net-tools-riscv64-unknown-linux-gnu-2.10 /nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin; do
    PATH=$PATH:$i/bin:$i/sbin
done

_status=0
trap "_status=1 _localstatus=\$?" ERR

# Ensure a consistent umask.
umask 0022

#### Activation script snippet specialfs:
_localstatus=0
specialMount() {
  local device="$1"
  local mountPoint="$2"
  local options="$3"
  local fsType="$4"

  if mountpoint -q "$mountPoint"; then
    local options="remount,$options"
  else
    mkdir -m 0755 -p "$mountPoint"
  fi
  mount -t "$fsType" -o "$options" "$device" "$mountPoint"
}
source /nix/store/vn0sga6rn69vkdbs0d2njh0aig7zmzi6-mounts.sh


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "specialfs" "$_localstatus"
fi

#### Activation script snippet binfmt:
_localstatus=0
mkdir -p -m 0755 /run/binfmt



if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "binfmt" "$_localstatus"
fi

#### Activation script snippet stdio:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "stdio" "$_localstatus"
fi

#### Activation script snippet binsh:
_localstatus=0
# Create the required /bin/sh symlink; otherwise lots of things
# (notably the system() function) won't work.
mkdir -m 0755 -p /bin
ln -sfn "/nix/store/4y83vxk3mfk216d1jjfjgckkxwrbassi-bash-interactive-5.2-p15-riscv64-unknown-linux-gnu/bin/sh" /bin/.sh.tmp
mv /bin/.sh.tmp /bin/sh # atomically replace /bin/sh


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "binsh" "$_localstatus"
fi

#### Activation script snippet check-manual-docbook:
_localstatus=0
if [[ $(cat /nix/store/xzgmgymf510dicgppghq27lrh9fjpxfi-options-used-docbook) = 1 ]]; then
  echo -e "\e[31;1mwarning\e[0m: This configuration contains option documentation in docbook." \
          "Support for docbook is deprecated and will be removed after NixOS 23.05." \
          "See nix-store --read-log /nix/store/n232fhpqqqnlfjl0rj59xxms419glja2-options.json.drv"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "check-manual-docbook" "$_localstatus"
fi

#### Activation script snippet domain:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "domain" "$_localstatus"
fi

#### Activation script snippet users:
_localstatus=0
install -m 0700 -d /root
install -m 0755 -d /home

/nix/store/6fap9xv6snx5fr2m7m804v4gc23pb1jh-perl-riscv64-unknown-linux-gnu-5.36.0-env/bin/perl \
-w /nix/store/gx91fdp4a099jpfwdkbdw2imvl3lalsk-update-users-groups.pl /nix/store/1zj6fk93qkqd3z8n34s4r40xnby2ci21-users-groups.json


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "users" "$_localstatus"
fi

#### Activation script snippet groups:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "groups" "$_localstatus"
fi

#### Activation script snippet etc:
_localstatus=0
# Set up the statically computed bits of /etc.
echo "setting up /etc..."
/nix/store/habrmd12my31s9r9fdby78l2dg5p7qyx-perl-riscv64-unknown-linux-gnu-5.36.0-env/bin/perl /nix/store/rg5rf512szdxmnj9qal3wfdnpfsx38qi-setup-etc.pl /nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "etc" "$_localstatus"
fi

#### Activation script snippet hashes:
_localstatus=0
users=()
while IFS=: read -r user hash tail; do
  if [[ "$hash" = "$"* && ! "$hash" =~ ^\$(y|gy|7|2b|2y|2a|6)\$ ]]; then
    users+=("$user")
  fi
done </etc/shadow

if (( "${#users[@]}" )); then
  echo "
WARNING: The following user accounts rely on password hashing algorithms
that have been removed. They need to be renewed as soon as possible, as
they do prevent their users from logging in."
  printf ' - %s\n' "${users[@]}"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "hashes" "$_localstatus"
fi

#### Activation script snippet hostname:
_localstatus=0
hostname "lp4a"


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "hostname" "$_localstatus"
fi

#### Activation script snippet modprobe:
_localstatus=0
# Allow the kernel to find our wrapped modprobe (which searches
# in the right location in the Nix store for kernel modules).
# We need this when the kernel (or some module) auto-loads a
# module.
echo /nix/store/wv00igsmj6mkk1ybssdch52hx0hx0x67-kmod-riscv64-unknown-linux-gnu-30/bin/modprobe > /proc/sys/kernel/modprobe


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "modprobe" "$_localstatus"
fi

#### Activation script snippet nix:
_localstatus=0
install -m 0755 -d /nix/var/nix/{gcroots,profiles}/per-user


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "nix" "$_localstatus"
fi

#### Activation script snippet nix-channel:
_localstatus=0
# Subscribe the root user to the NixOS channel by default.
if [ ! -e "/root/.nix-channels" ]; then
    echo "https://nixos.org/channels/nixos-23.05 nixos" > "/root/.nix-channels"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "nix-channel" "$_localstatus"
fi

#### Activation script snippet systemd-timesyncd-init-clock:
_localstatus=0
if ! [ -f /var/lib/systemd/timesync/clock ]; then
  test -d /var/lib/systemd/timesync || mkdir -p /var/lib/systemd/timesync
  touch /var/lib/systemd/timesync/clock
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "systemd-timesyncd-init-clock" "$_localstatus"
fi

#### Activation script snippet udevd:
_localstatus=0
# The deprecated hotplug uevent helper is not used anymore
if [ -e /proc/sys/kernel/hotplug ]; then
  echo "" > /proc/sys/kernel/hotplug
fi

# Allow the kernel to find our firmware.
if [ -e /sys/module/firmware_class/parameters/path ]; then
  echo -n "/nix/store/ann0ayjx9qf296pssrk2b26fry235idz-firmware/lib/firmware" > /sys/module/firmware_class/parameters/path
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "udevd" "$_localstatus"
fi

#### Activation script snippet usrbinenv:
_localstatus=0
mkdir -m 0755 -p /usr/bin
ln -sfn /nix/store/fifbf1h3i83jvan2vkk7xm4fraq7drm7-coreutils-riscv64-unknown-linux-gnu-9.1/bin/env /usr/bin/.env.tmp
mv /usr/bin/.env.tmp /usr/bin/env # atomically replace /usr/bin/env


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "usrbinenv" "$_localstatus"
fi

#### Activation script snippet var:
_localstatus=0
# Various log/runtime directories.

mkdir -m 1777 -p /var/tmp

# Empty, immutable home directory of many system accounts.
mkdir -p /var/empty
# Make sure it's really empty
/nix/store/yln7ma9dldr3f2dva4l0iq275s4brxml-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/chattr -f -i /var/empty || true
find /var/empty -mindepth 1 -delete
chmod 0555 /var/empty
chown root:root /var/empty
/nix/store/yln7ma9dldr3f2dva4l0iq275s4brxml-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/chattr -f +i /var/empty || true


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "var" "$_localstatus"
fi

#### Activation script snippet wrappers:
_localstatus=0
chmod 755 "/run/wrappers"

# We want to place the tmpdirs for the wrappers to the parent dir.
wrapperDir=$(mktemp --directory --tmpdir="/run/wrappers" wrappers.XXXXXXXXXX)
chmod a+rx "$wrapperDir"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/chsh"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/chsh" > "$wrapperDir/chsh.real"

# Prevent races
chmod 0000 "$wrapperDir/chsh"
chown root:root "$wrapperDir/chsh"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/chsh"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/dbus-daemon-launch-helper"
echo -n "/nix/store/jqk530wxiq3832zyiqn8qi6i2pr3snnl-dbus-riscv64-unknown-linux-gnu-1.14.8/libexec/dbus-daemon-launch-helper" > "$wrapperDir/dbus-daemon-launch-helper.real"

# Prevent races
chmod 0000 "$wrapperDir/dbus-daemon-launch-helper"
chown root:messagebus "$wrapperDir/dbus-daemon-launch-helper"

chmod "u+s,g-s,u+rx,g+rx,o-rx" "$wrapperDir/dbus-daemon-launch-helper"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/fusermount"
echo -n "/nix/store/2d68cpnlqls47ijrwss83swjk2q1v953-fuse-riscv64-unknown-linux-gnu-2.9.9/bin/fusermount" > "$wrapperDir/fusermount.real"

# Prevent races
chmod 0000 "$wrapperDir/fusermount"
chown root:root "$wrapperDir/fusermount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/fusermount"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/fusermount3"
echo -n "/nix/store/06w8lm5k9i2n1xhkszsf4pa9hw9l0r5s-fuse-riscv64-unknown-linux-gnu-3.11.0/bin/fusermount3" > "$wrapperDir/fusermount3.real"

# Prevent races
chmod 0000 "$wrapperDir/fusermount3"
chown root:root "$wrapperDir/fusermount3"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/fusermount3"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/mount"
echo -n "/nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/mount" > "$wrapperDir/mount.real"

# Prevent races
chmod 0000 "$wrapperDir/mount"
chown root:root "$wrapperDir/mount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/mount"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newgidmap"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/newgidmap" > "$wrapperDir/newgidmap.real"

# Prevent races
chmod 0000 "$wrapperDir/newgidmap"
chown root:root "$wrapperDir/newgidmap"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newgidmap"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newgrp"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/newgrp" > "$wrapperDir/newgrp.real"

# Prevent races
chmod 0000 "$wrapperDir/newgrp"
chown root:root "$wrapperDir/newgrp"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newgrp"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newuidmap"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/newuidmap" > "$wrapperDir/newuidmap.real"

# Prevent races
chmod 0000 "$wrapperDir/newuidmap"
chown root:root "$wrapperDir/newuidmap"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newuidmap"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/passwd"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/passwd" > "$wrapperDir/passwd.real"

# Prevent races
chmod 0000 "$wrapperDir/passwd"
chown root:root "$wrapperDir/passwd"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/passwd"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/ping"
echo -n "/nix/store/mckzq3q58m31d8ax04gnjqx43niamis0-iputils-riscv64-unknown-linux-gnu-20221126/bin/ping" > "$wrapperDir/ping.real"

# Prevent races
chmod 0000 "$wrapperDir/ping"
chown root:root "$wrapperDir/ping"

# Set desired capabilities on the file plus cap_setpcap so
# the wrapper program can elevate the capabilities set on
# its file into the Ambient set.
/nix/store/z2gpziznsj8rnv55vyq5n287g5cvx7lg-libcap-riscv64-unknown-linux-gnu-2.68/bin/setcap "cap_setpcap,cap_net_raw+p" "$wrapperDir/ping"

# Set the executable bit
chmod u+rx,g+x,o+x "$wrapperDir/ping"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sg"
echo -n "/nix/store/9al8xczxbm72i5q63n91fli5rynrfprl-shadow-riscv64-unknown-linux-gnu-4.13/bin/sg" > "$wrapperDir/sg.real"

# Prevent races
chmod 0000 "$wrapperDir/sg"
chown root:root "$wrapperDir/sg"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sg"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/su"
echo -n "/nix/store/gbp100zp8a8gja22dyjz4nwv0qsxb7qy-shadow-riscv64-unknown-linux-gnu-4.13-su/bin/su" > "$wrapperDir/su.real"

# Prevent races
chmod 0000 "$wrapperDir/su"
chown root:root "$wrapperDir/su"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/su"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sudo"
echo -n "/nix/store/scywdc7rd6cjfvji166a6d0bsjj90vys-sudo-riscv64-unknown-linux-gnu-1.9.13p3/bin/sudo" > "$wrapperDir/sudo.real"

# Prevent races
chmod 0000 "$wrapperDir/sudo"
chown root:root "$wrapperDir/sudo"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sudo"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sudoedit"
echo -n "/nix/store/scywdc7rd6cjfvji166a6d0bsjj90vys-sudo-riscv64-unknown-linux-gnu-1.9.13p3/bin/sudoedit" > "$wrapperDir/sudoedit.real"

# Prevent races
chmod 0000 "$wrapperDir/sudoedit"
chown root:root "$wrapperDir/sudoedit"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sudoedit"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/umount"
echo -n "/nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/umount" > "$wrapperDir/umount.real"

# Prevent races
chmod 0000 "$wrapperDir/umount"
chown root:root "$wrapperDir/umount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/umount"

cp /nix/store/wl1c1dgxb1zklpy5inpk7p798pm4zcca-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/unix_chkpwd"
echo -n "/nix/store/cn72qv0n576vg61mgaran7g2vj6gdjwn-linux-pam-riscv64-unknown-linux-gnu-1.5.2/bin/unix_chkpwd" > "$wrapperDir/unix_chkpwd.real"

# Prevent races
chmod 0000 "$wrapperDir/unix_chkpwd"
chown root:root "$wrapperDir/unix_chkpwd"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/unix_chkpwd"


if [ -L /run/wrappers/bin ]; then
  # Atomically replace the symlink
  # See https://axialcorps.com/2013/07/03/atomically-replacing-files-and-directories/
  old=$(readlink -f /run/wrappers/bin)
  if [ -e "/run/wrappers/bin-tmp" ]; then
    rm --force --recursive "/run/wrappers/bin-tmp"
  fi
  ln --symbolic --force --no-dereference "$wrapperDir" "/run/wrappers/bin-tmp"
  mv --no-target-directory "/run/wrappers/bin-tmp" "/run/wrappers/bin"
  rm --force --recursive "$old"
else
  # For initial setup
  ln --symbolic "$wrapperDir" "/run/wrappers/bin"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "wrappers" "$_localstatus"
fi


# Make this configuration the current configuration.
# The readlink is there to ensure that when $systemConfig = /system
# (which is a symlink to the store), /run/current-system is still
# used as a garbage collection root.
ln -sfn "$(readlink -f "$systemConfig")" /run/current-system

# Prevent the current configuration from being garbage-collected.
mkdir -p /nix/var/nix/gcroots
ln -sfn /run/current-system /nix/var/nix/gcroots/current-system

exit $_status
```

这个脚本有点长，简单总结下它干了啥：

1. 通过 `source /nix/store/vn0sga6rn69vkdbs0d2njh0aig7zmzi6-mounts.sh` 挂载一些目录，看下
   这个文件内容就知道，挂的是 `/proc` `/sys` `/dev` `/rum` 等几个临时目录。
1. 通过 `mkdir`/`install` 等指令自动创建 `/home` `/root` `/bin` `/usr` `/usr/bin` 等目录
1. 通过
   `perl /nix/store/rg5rf512szdxmnj9qal3wfdnpfsx38qi-setup-etc.pl /nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc`
   配置生成 `/etc` 目录中的各种文件。
1. 通过 `ln` 命令添加其他各种软链接，以及一些别的设置。

其中第三步 etc 目录的设置，实际数据基本都来自该脚本的第二个参数：

```bash
› ls root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc
╭────┬──────────────────────────────────────────────────────────────────────────┬─────────┬────────┬──────────────╮
│  # │                                   name                                   │  type   │  size  │   modified   │
├────┼──────────────────────────────────────────────────────────────────────────┼─────────┼────────┼──────────────┤
│  0 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/bashrc           │ symlink │   54 B │ 54 years ago │
│  1 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/binfmt.d         │ dir     │ 4.1 KB │ 54 years ago │
│  2 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/dbus-1           │ symlink │   50 B │ 54 years ago │
│  3 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/default          │ dir     │ 4.1 KB │ 54 years ago │
│  4 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/dhcpcd.exit-hook │ symlink │   60 B │ 54 years ago │
│  5 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/fonts            │ symlink │   69 B │ 54 years ago │
│  6 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/fstab            │ symlink │   53 B │ 54 years ago │
│  7 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/fuse.conf        │ symlink │   57 B │ 54 years ago │
│  8 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/host.conf        │ symlink │   57 B │ 54 years ago │
│  9 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/hostname         │ symlink │   56 B │ 54 years ago │
│ 10 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/hosts            │ symlink │   49 B │ 54 years ago │
│ 11 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/inputrc          │ symlink │   51 B │ 54 years ago │
│ 12 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/issue            │ symlink │   49 B │ 54 years ago │
│ 13 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/kbd              │ symlink │   61 B │ 54 years ago │
│ 14 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/locale.conf      │ symlink │   55 B │ 54 years ago │
│ 15 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/login.defs       │ symlink │   54 B │ 54 years ago │
│ 16 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/lsb-release      │ symlink │   59 B │ 54 years ago │
│ 17 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/lvm              │ dir     │ 4.1 KB │ 54 years ago │
│ 18 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/man_db.conf      │ symlink │   59 B │ 54 years ago │
│ 19 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/modprobe.d       │ dir     │ 4.1 KB │ 54 years ago │
│ 20 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/modules-load.d   │ dir     │ 4.1 KB │ 54 years ago │
│ 21 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/nanorc           │ symlink │   54 B │ 54 years ago │
│ 22 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/netgroup         │ symlink │   56 B │ 54 years ago │
│ 23 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/nix              │ dir     │ 4.1 KB │ 54 years ago │
│ 24 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/nscd.conf        │ symlink │   57 B │ 54 years ago │
│ 25 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/nsswitch.conf    │ symlink │   61 B │ 54 years ago │
│ 26 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/os-release       │ symlink │   58 B │ 54 years ago │
│ 27 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/pam              │ dir     │ 4.1 KB │ 54 years ago │
│ 28 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/pam.d            │ dir     │ 4.1 KB │ 54 years ago │
│ 29 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/pki              │ dir     │ 4.1 KB │ 54 years ago │
│ 30 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/profile          │ symlink │   55 B │ 54 years ago │
│ 31 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/protocols        │ symlink │   75 B │ 54 years ago │
│ 32 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/pulse            │ dir     │ 4.1 KB │ 54 years ago │
│ 33 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/resolvconf.conf  │ symlink │   63 B │ 54 years ago │
│ 34 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/rpc              │ symlink │   90 B │ 54 years ago │
│ 35 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/samba            │ dir     │ 4.1 KB │ 54 years ago │
│ 36 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/services         │ symlink │   74 B │ 54 years ago │
│ 37 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/set-environment  │ symlink │   59 B │ 54 years ago │
│ 38 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/shells           │ symlink │   54 B │ 54 years ago │
│ 39 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/ssh              │ dir     │ 4.1 KB │ 54 years ago │
│ 40 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/ssl              │ dir     │ 4.1 KB │ 54 years ago │
│ 41 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/sudoers          │ symlink │   51 B │ 54 years ago │
│ 42 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/sudoers.gid      │ file    │    3 B │ 54 years ago │
│ 43 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/sudoers.mode     │ file    │    5 B │ 54 years ago │
│ 44 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/sudoers.uid      │ file    │    3 B │ 54 years ago │
│ 45 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/sysctl.d         │ dir     │ 4.1 KB │ 54 years ago │
│ 46 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/systemd          │ dir     │ 4.1 KB │ 54 years ago │
│ 47 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/terminfo         │ symlink │   70 B │ 54 years ago │
│ 48 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/tmpfiles.d       │ dir     │ 4.1 KB │ 54 years ago │
│ 49 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/udev             │ dir     │ 4.1 KB │ 54 years ago │
│ 50 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/vconsole.conf    │ symlink │   57 B │ 54 years ago │
│ 51 │ root/nix/store/qsbx6lnsbs54yszy7d1ni7xgz6h6ayjd-etc/etc/zoneinfo         │ symlink │   97 B │ 54 years ago │
├────┼──────────────────────────────────────────────────────────────────────────┼─────────┼────────┼──────────────┤
│  # │                                   name                                   │  type   │  size  │   modified   │
╰────┴──────────────────────────────────────────────────────────────────────────┴─────────┴────────┴──────────────╯
```

这个 perl 脚本基本就是根据这个 nix store 中的 etc 文件夹，生成 `/etc` 目录中的各种文件或软
链接。

## 四、硬件驱动部分

NixOS 要能在 LicheePi 4A 上正常启动，还需要有硬件固件的支持，因此光了解 NixOS 的启动流程还
不够，还需要了解硬件固件的启动流程。这里简要介绍下 Linux 在 RISC-V 上的启动流程。

### 1. u-boot，u-boot-spl，u-boot-tpl 的关系

U-Boot 是嵌入式领域最常用的 bootloader，

对于一般嵌入式系统而言只需要一个 u-boot 作为 bootloader 即可，但入今的嵌入式 IC 已经转向
SOC 片上系统，其内部不仅仅是一颗 CPU 核，还可能包含各种各样的其他 IP，因而相关的上层软件也
需要针对性的划分不同的功能域，操作域，安全域等上层应用。为了支持这些复杂而碎片化的应用需
求，又或者因为 SRAM 太小以致无法放下整个 bootloader，SOC 的 Boot 阶段衍生出了多级
BootLoader，u-boot 为此定义了二三级加载器:

- spl：Secondary Program Loader，二级加载器
- tpl：Tertiary Program Loader，三级加载器

spl 和 tpl 走 u-boot 完全相同的 boot 流程，不过在 spl 和 tpl 中大多数驱动和功能被去除了，
根据需要只保留一部分 spl 和 tpl 需要的功能，通过 CONFIG_SPL_BUILD 和 CONFIG_TPL_BUILD 控
制；一般只用 spl 就足够了，spl 完成 ddr 初始化，并完成一些外设驱动初始化，比如 usb，emmc，
以此从其他外围设备加载 u-boot，但是如果对于小系统 spl 还是太大了，则可以继续加入 tpl，tpl
只做 ddr 等的特定初始化保证代码体积极小，以此再次从指定位置加载 spl，spl 再去加载 u-boot。

LicheePi4A 就使用了二级加载器，它甚至写死了 eMMC 的分区表，要求我们使用 fastboot 往对应的
分区写入 u-boot-spl.bin，官方给出的命令如下：

```bash
# flash u-boot into spl partition
sudo fastboot flash ram u-boot-with-spl.bin
sudo fastboot reboot
# flash uboot partition
sudo fastboot flash uboot u-boot-with-spl.bin
```

### 2. RISC-V 的启动流程

网上找到的一个图，涉及到一些 RISC-V 指令集相关的知识点：

{{<figure src="./current-riscv-boot-flow.webp" title="RISCV 开发版当前的引导流程" width="80%">}}

根据我们前面的 NixOS 启动日志，跟这个图还是比较匹配的，但我们没观察到任何 U-Boot 日志，有
可能是因为 U-Boot 没开日志，暂时不打算细究。

### 3. OpenSBI

前面的 NixOS 启动日志跟启动流程图中都出现了 OpenSBI，那么 OpenSBI 是什么呢？为什么 ARM 开
发版的启动流程中没有这么个玩意儿？

查了下资料，大概是说因为 RISC-V 是一个开放指令集，任何人都可以基于 RISC-V 开发自己的定制指
令集，或者定制 IC 布局。这显然存在很明显的碎片化问题。OpenSBI 就是为了避免此问题而设计的，
它提供了一个标准的接口，即 Supervisor Binary Interface, SBI. 上层系统只需要适配 SBI 就可以
了，不需要关心底层硬件的细节。IC 开发商也只需要实现 SBI 的接口，就可以让任何适配了 SBI 的
上层系统能在其硬件平台上正常运行。

而 OpenSBI 则是 SBI 标准的一个开源实现，IC 开发商只需要将 OpenSBI 移植到自己的硬件平台上即
可支持 SBI 标准。

而 ARM 跟 X86 等指令集则是封闭的，不允许其他公司修改与拓展其指令集，因此不存在碎片化的问
题，也就不需要 OpenSBI 这样的东西。

### 4. fw_dynamic.bin 跟 u-boot-spl.bin 两个文件

1. `fw_dynamic.bin`: 我们 NixOS 镜像的 `/boot` 中就有这个固件，它是 OpenSBI 的编译产物。
   1. RevyOS 的定制 OpenSBI 构建方
      法：<https://github.com/revyos/thead-opensbi/blob/lpi4a/.github/workflows/build.yml>
2. `u-boot-spl.bin`: 这个文件是 u-boot 的编译产物，它是二级加载器。
   1. RevyOS 的定制 u-boot 构建方
      法：<https://github.com/revyos/thead-u-boot/blob/lpi4a/.github/workflows/build.yml>

### 5. T-Head 官方的编译工具链

因为历史原因，TH1520 设计时貌似 RVV 还没出正式的规范，因此它使用了一些非标准的指令集，GCC
官方貌似宣称了永远不会支持这些指令集...（个人理解，可能有误哈）

因此为了获得最佳性能，LicheePi4A 官方文档建议使用 T-Head 提供的工具链编译整个系统。

但我在研究了 NixOS 的工具链实现，以及咨询了 @NickCao 后，确认了在 NixOS 上这几乎是不可行
的。NixOS 因为不遵循 FHS 标准，它对 GCC 等工具链做了非常多的魔改，要在 NixOS 上使用 T-Head
的工具链，就要使这一堆魔改的东西在 T-Head 的工具链上也能 Work，这个工作量很大，也很有技术
难度。

所以最终选择了用 NixOS 的标准工具链编译系统，@revy 老师也为此帮我做了些适配工作，解决了一
些标准工具链上的编译问题。

Issue 区也有人提到了这个问题，Revy 老师也帮助补充了些相关信
息：<https://github.com/ryan4yin/nixos-licheepi4a/issues/14>

## 五、我是如何构建出一个可以在 LicheePi 4A 上运行的 NixOS 镜像的

到这里，NixOS 在 LicheePI4A 上启动的整个流程就基本讲清楚了， **NixOS 跟其他传统发行版在启
动流程中最大的区别是它自定义了一个 init 脚本，在启动 systemd 之前，它会先执行这个脚本进行
文件系统的初始化操作，准备好最基础的 FHS 目录结构，使得后续的 systemd 以及其他服务能正常启
动**。正是因为这个 init 脚本，NixOS 才能在仅有 `/boot` 与 `/nix` 这两个目录的情况下正常启
动整个系统。

> NixOS 数据的集中化只读存储使更多的骚操作成为可能，比如直接使用 tmpfs 作为根文件系统，将
> 需要持久化的目录挂载到外部存储设备上，这样每次重启系统时，所有预期之外的临时数据都会被清
> 空，进一步保证了系统的可复现性与安全性。如果你有系统洁癖，而且有兴趣折腾，那就快来看看
> @LanTian 写的
> [NixOS 系列（四）：「无状态」操作系统](https://lantian.pub/article/modify-computer/nixos-impermanence.lantian/)
> 吧~

最终在 LicheePi4A 成功启动后的登录的截图：

{{<figure src="./nixos-licheepi-neofetch.webp" title="NixOS 成功启动" width="80%">}}

那么基于我们到目前为止学到的知识，要如何构建出一个可以在 LicheePi 4A 上运行的 NixOS 镜像
呢？

这个讲起来就很费时间了，涉及到了 NixOS
的[交叉编译系统](https://nixos-and-flakes.thiscute.world/zh/development/cross-platform-compilation)，[内核 override](https://nixos-and-flakes.thiscute.world/zh/development/kernel-development),
[flakes](https://nixos-and-flakes.thiscute.world/zh/nixos-with-flakes/introduction-to-flakes),
[镜像构建](https://github.com/ryan4yin/nixos-licheepi4a/blob/main/modules/sd-image/sd-image.nix)等
等，要展开讲的话也是下一篇文章了，有兴趣的可以直接看我的 NixOS on LicheePi4A 仓
库：<https://github.com/ryan4yin/nixos-licheepi4a>.

简单的说，NixOS 跟传统 Linux 发行版的系统镜像构建思路是一致的，但因为其声明式与可复现性的
特点，实际实现时出现了非常大的区别。以我的项目仓库为例，整个项目完全使用 Nix 语言声明式编
写（内嵌了部分 Shell 脚本...），而且这份配置也可用于系统后续的持续声明式更新部署（我还给出
了一个 demo）。

最后，再推荐一波我的 NixOS 入门指
南：[ryan4yin/nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book)，
对 NixOS 感兴趣的读者们，快进我碗里来（

## 参考

- [Systemd Stage 1 - NixCon NA 2024 - California](https://github.com/nixcon/NixConContent/blob/main/NixCon%20NA%202024%20-%20California/Day%202%20-%20Keynotes/systemd-stage-1.pdf)
- [LicheePi 4A —— 这个小板有点意思（第一部分） - HougeLangley](https://litterhougelangley.club/blog/2023/05/27/licheepi-4a-%e8%bf%99%e4%b8%aa%e5%b0%8f%e6%9d%bf%e6%9c%89%e7%82%b9%e6%84%8f%e6%80%9d%ef%bc%88%e7%ac%ac%e4%b8%80%e9%83%a8%e5%88%86%ef%bc%89/)
- [Analyzing the Linux boot process - By Alison Chaiken](https://opensource.com/article/18/1/analyzing-linux-boot-process)
- [OpenSBI Platform Firmwares](https://github.com/riscv-software-src/opensbi/blob/master/docs/firmware/fw.md)
- [An Introduction to RISC-V Boot flow: Overview, Blob vs Blobfree standards](https://crvf2019.github.io/pdf/43.pdf)
- [基于 qemu-riscv 从 0 开始构建嵌入式 linux 系统 ch5-1. 什么是多级 BootLoader 与 opensbi(上)¶](https://quard-star-tutorial.readthedocs.io/zh_CN/latest/ch5-1.html)
- [Using the initial RAM disk (initrd) - kernel.org](https://docs.kernel.org/admin-guide/initrd.html)
- [Differences Between vmlinux, vmlinuz, vmlinux.bin, zimage, and bzimage](https://www.baeldung.com/linux/kernel-images)
- [U-Boot 官方的 Distro 文档](https://github.com/ARM-software/u-boot/blob/master/doc/README.distro)
