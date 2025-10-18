---
title: "Linux 桌面系统组件概览与故障排查指南"
subtitle: ""
description: ""
date: 2025-09-09T20:17:33+08:00
lastmod: 2025-10-03T01:59:33+08:00
draft: false

authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Linux", "Desktop", "Systemd", "D-Bus"]
categories: ["tech"]
series: []
hiddenFromHomePage: false
hiddenFromSearch: false
license: ""

lightgallery: false

# 否开启表格排序
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
  # whether to show the copy button of the code block
  copy: true
  # the maximum number of lines of displayed code by default
  maxShownLines: 30
---

## 定位与目标

Linux 桌面包含了相当多的系统组件，这些组件组合形成了一个精密的系统，它们共同管理着从硬件设
备到用户会话的方方面面。

即使我已经有七八年的 Linux 使用经验，在遇到系统的各种大小毛病时，还是常常觉得问题的定位跟
解决很是艰难。倘若我们能像庖丁那样“目无全牛”，对整个系统的架构了如指掌，在定位问题时顺着骨
节筋脉下刀，那解决起问题来自然也将游刃有余。

而这就是这篇文章的目的——搭建起一幅 Linux 桌面系统的「解牛图」。

本文面向已经有一定 Linux 桌面使用经验的读者。我们用一条从「开机」到「APP 运行」再到「关机/
断电」的时间线为轴，讲清每一步发生了什么、哪里能看到证据（日志 / 设备节点 / D‑Bus 信号）、
可通过哪些命令排查验证，以及常见问题的修复思路。

一篇文章显然不可能涵盖太多细节，因此这篇文章主要还是起一个概览的作用。

技术栈假定为：UEFI + systemd-boot + systemd + Wayland + PipeWire + systemd-networkd +
fcitx5, 使用的发行版为 NixOS.

> **AI 创作声明**：本文由笔者借助 ChatGPT, Kimi K2, 豆包和 Cursor 创作，有很大篇幅的内容完
> 全由 AI 在我的指导下生成。如有错误，还请指正。

---

## Linux 桌面系统生命周期概览

```ascii
┌──────────────────────────────────────────────────────────────────────────────┐
│                  Linux 桌面系统生命周期                                      │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. 系统启动阶段                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ UEFI → BootLoader → 内核映像 → initramfs → systemd (PID 1)                   │
│ 固件    grub/systemd-boot  内核探测   临时根挂载   服务管理器                │
│ TPM/SEC   EFI Stub         KMS启动   根fs解压挂载   Unit依赖树+并行启动      │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. 内核 & 驱动层（硬件使能）                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ DRM/KMS  →   evdev    →    ALSA   →   网络固件   →   安全模块                │
│ 显示模式   输入事件      声卡驱动   iwlwifi/ath9k   AppArmor/SELinux         │
│ GPU初始化  权限过滤      PCM设备    Bluetooth       cgroups/Namespaces       │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. 用户空间初始化阶段                                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ systemd  →  udev  →  D-Bus  → timesyncd → resolved → networkd/iwd → oomd     │
│ 服务树    设备节点   消息总线   NTP客户端   DNS缓存   网络管理   OOM守护     │
│ ACL/权限  热插拔     激活机制   时钟同步   NSS查询   DHCP/路由   cgroup内存  │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. 图形会话阶段                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 显示管理器 → logind → Wayland Compositor/X-Server → 窗口管理器               │
│ GDM/SDDM     会话槽     i3/Niri/Hyprlland          GNOME/KDE WM+合成         │
│ 身份认证     设备ACL    DRM fd传递+输入            OpenGL/Vulkan渲染         │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 5. 多媒体 & 输入阶段                                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│ PipeWire → PulseAudio/JACK兼容层 → V4L2 → fcitx5/ibus → libinput事件         │
│ 音频/视频   兼容层路由          摄像头API   输入法框架   键盘/触摸/手势      │
│ 屏幕共享    低延迟混音          DMA-BUF     中文输入     手写板/多点触控     │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 6. 应用程序运行阶段                                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ GUI应用 → GTK/Qt → Mesa/OpenGL/Vulkan → GPU驱动                              │
│ Flatpak   工具包   渲染管线           amdgpu/nouveau/intel(驱动层)           │
│ 沙盒化    Cairo    DMA-Fence          ioctl调度(内核层)                      │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 7. 系统关机阶段                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ logind → systemd --user → 显示管理器 → systemd(PID1) → 内核 & 驱动           │
│ 广播关机   停用户服务    关闭会话      停系统服务    卸载文件系统→断电       │
│ 保存会话   PipeWire退出  释放DRM/KMS   卸载网络      同步磁盘→关声卡+屏幕    │
└──────────────────────────────────────────────────────────────────────────────┘

```

---

## 1. 系统启动：从固件到用户空间

### 1.1 UEFI 引导与内核加载

现代系统普遍使用 **UEFI 固件** 代替 BIOS。UEFI 初始化硬件后，从 EFI System Partition (ESP)
中加载启动管理器。NixOS 默认使用 grub，启用 Secure
Boot([lanzaboote](https://github.com/nix-community/lanzaboote)) 时需改用
[systemd-boot](https://www.freedesktop.org/software/systemd/man/latest/systemd-boot.html).

systemd-boot 的全局配置是 `/boot/loader/loader.conf`，具体的启动项配置需要分类讨论：

- **Type 1：手动配置
  （[Boot Loader Specification Type #1](https://uapi-group.org/specifications/specs/boot_loader_specification/#type-1-boot-loader-specification-entries)）**

  - 配置方式：`/loader/entries/*.conf`，位于 EFI 系统分区（ESP）或 Extended Boot Loader
    Partition（XBOOTLDR）下
  - 特点：
    - 可自定义启动项名称、内核参数、initrd 等
    - 描述 Linux 内核及其 initrd，也可以描述任意 EFI 可执行文件
    - 包括 fallback / rescue 内核
  - 示例：
    ```ini
    title   NixOS Linux
    linux   /vmlinuz-linux
    initrd  /initrd-linux.img
    options root=UUID=xxxx rw
    ```

- **Type 2：统一内核镜像
  （[Boot Loader Specification Type #2](https://uapi-group.org/specifications/specs/boot_loader_specification/#type-2-efi-unified-kernel-images)）**

  - 配置方式：将 EFI 格式的 UKI 镜像放在 ESP 分区的 `/EFI/Linux/` 下即可
  - 工作原理：
    1. systemd-boot 在启动时扫描 ESP 的 `/EFI/Linux/` 目录
    2. systemd-boot 会自动将扫描到的内核镜像添加到启动菜单，无需单独的 `.conf` 文件
  - 特点：
    - 免配置，自动出现在启动菜单中
    - vmlinuz-linux, initrd 跟 cmdline 等信息被统一打包成一个 EFI 镜像，一个镜像就包含了系
      统启动需要的所有数据，更方面简洁。

- **其他自动识别的启动项**
  - Microsoft Windows EFI boot manager（如果已安装）
  - Apple macOS boot manager（如果已安装）
  - EFI Shell 可执行文件（如果已安装）
  - 「Reboot Into Firmware Interface」选项（如果 UEFI 固件支持）
  - Secure Boot 变量注册（如果固件处于 setup 模式，且 ESP 提供了相关文件）

**常用命令**：

- `efibootmgr -v`：查看 / 修改固件启动顺序
- `bootctl status`：检查 systemd-boot 安装与 ESP 状态
- `bootctl list`：列出启动条目
- `ukify inspect /boot/EFI/Linux/nixos-xxx.efi`: 查看 efi 镜像中包含的信息

示例：

```bash
# 查看固件启动顺序
$ nix run nixpkgs#efibootmgr -v

BootCurrent: 0000
Timeout: 0 seconds
BootOrder: 0000,0004
Boot0000* NixOS HD(1,GPT,34286f3b-d4df-456d-bf7a-eb67f2bf1a72,0x1000,0x12b000)/EFI\BOOT\BOOTX64.EFI
...
Boot0004* Windows Boot Manager  HD(1,GPT,34286f3b-d4df-456d-bf7a-eb67f2bf1a72,0x1000,0x12b000)/\EFI\Microsoft\Boot\bootmgfw.efi0000424f

# 检查 systemd-boot 安装与 ESP 状态
$ bootctl status

System:
      Firmware: UEFI 2.80 (American Megatrends 5.27)
 Firmware Arch: x64
   Secure Boot: enabled (user)
  TPM2 Support: yes
  Measured UKI: yes
  Boot into FW: supported

Current Boot Loader:
      Product: systemd-boot 257.7
     Features: ✓ Boot counting
               ✓ Menu timeout control
               ✓ One-shot menu timeout control
               ✓ Default entry control
               ✓ One-shot entry control
               ✓ Support for XBOOTLDR partition
               ✓ Support for passing random seed to OS
               ✓ Load drop-in drivers
               ✓ Support Type #1 sort-key field
               ✓ Support @saved pseudo-entry
               ✓ Support Type #1 devicetree field
               ✓ Enroll SecureBoot keys
               ✓ Retain SHIM protocols
               ✓ Menu can be disabled
               ✓ Multi-Profile UKIs are supported
               ✓ Boot loader set partition information
    Partition: /dev/disk/by-partuuid/34286f3b-d4df-456d-bf7a-eb67f2bf1a72
       Loader: └─EFI/BOOT/BOOTX64.EFI
Current Entry: nixos-generation-848-jattq2uvv2snrigcxtdcxelgaawdb3s6lar3ualze77id46h5adq.efi
...
Available Boot Loaders on ESP:
          ESP: /boot (/dev/disk/by-partuuid/34286f3b-d4df-456d-bf7a-eb67f2bf1a72)
         File: ├─/EFI/systemd/systemd-bootx64.efi (systemd-boot 257.7)
               └─/EFI/BOOT/BOOTX64.EFI (systemd-boot 257.7)
...
Default Boot Loader Entry:
         type: Boot Loader Specification Type #2 (.efi)
        title: NixOS Xantusia 25.11.20250830.d7600c7 (Linux 6.16.4) (Generation 848, 2025-09-01)
           id: nixos-generation-848-jattq2uvv2snrigcxtdcxelgaawdb3s6lar3ualze77id46h5adq.efi
       source: /boot//EFI/Linux/nixos-generation-848-jattq2uvv2snrigcxtdcxelgaawdb3s6lar3ualze77id46h5adq.efi (on the EFI System Partition)
     sort-key: lanza
      version: Generation 848, 2025-09-01
        linux: /boot//EFI/Linux/nixos-generation-848-jattq2uvv2snrigcxtdcxelgaawdb3s6lar3ualze77id46h5adq.efi
      options: init=/nix/store/gaj3sp3hrzjhp59bvyxhc8flg5s6iimg-nixos-system-ai-25.11.20250830.d7600c7/init nvidia-drm.fbdev=1 root=fstab loglevel=4 lsm=landlock,yama,bpf nvidia-drm.modeset=1 nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1 nvidia.NVreg_OpenRmEnableUnsupportedGpus=1

# 查看上述启动项中 uki efi 文件的内容
$ nix shell nixpkgs#systemdUkify
$ ukify inspect /boot/EFI/Linux/nixos-generation-848-jattq2uvv2snrigcxtdcxelgaawdb3s6lar3ualze77id46h5adq.efi
.osrel:
  size: 141 bytes
  sha256: e486dea4910eb9262efc47464f533f96093293d37c3d25feb954c098865a4be6
  text:
    ID=lanza
    PRETTY_NAME=NixOS Xantusia 25.11.20250830.d7600c7 (Linux 6.16.4) (Generation 848, 2025-09-01)
    VERSION_ID=Generation 848, 2025-09-01
# 启动内核时使用的内核命令行参数
.cmdline:
  size: 284 bytes
  sha256: 7f94ffed08359eb1d2749176eba57e085113f46208702a8c0251376d734f19ce
  text:
    init=/nix/store/gaj3sp3hrzjhp59bvyxhc8flg5s6iimg-nixos-system-ai-25.11.20250830.d7600c7/init nvidia-drm.fbdev=1 root=fstab loglevel=4 lsm=landlock,yama,bpf nvidia-drm.modeset=1 nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1 nvidia.NVreg_OpenRmEnableUnsupportedGpus=1
# initramfs 内容的引用，实际镜像位于 ESP 的 /EFI/nixos/initrd-*.efi
.initrd:
  size: 81 bytes
  sha256: 26d9b1f52806c48c6287272cb26b8a640b62d55f09149abf3415c76c38e0b56e
# 内核映像（vmlinuz）的引用，实际镜像位于 ESP 的 /EFI/nixos/kernel-*.efi
.linux:
  size: 81 bytes
  sha256: 41ff83e4cae160fb9ce55392943e6d06dbf9f37b710bf719f7fe2c28ec312be5
```

内核启动后，会探测 CPU、内存、PCI、USB、ACPI 等硬件，加载关键驱动，然后挂载 initramfs 并执
行 option 中指定的 `init` 程序。

**观察方法**：

```bash
# 查看内核早期日志
sudo dmesg --level=err,warn,info | less

# 查看本次启动的完整日志
journalctl -b
```

### 1.2 initramfs 阶段

initramfs （即 bootloader 中的 initrd 参数对应的镜像）提供最小用户空间，负责：

1. 识别并挂载根分区（可能包含 LUKS 解密 / LVM 激活）
2. 加载额外驱动
3. 执行 `switch_root` 交给真正的 rootfs
4. 执行 `init` 程序，该程序通常是 `systemd` 的软链接。
   - 不过在 NixOS 中 `init` 这个程序会有点特殊，详见
     [NixOS 在 Lichee Pi 4A 上是如何启动的](/posts/how-nixos-start-on-licheepi4a/)

**常见故障**：

- **找不到根分区**：检查 `cat /proc/cmdline` 的 `root=` 参数与 `blkid` 输出是否一致
- **缺少驱动模块**：确保 NixOS 配置包含所需模
  块：`boot.initrd.kernelModules = [ "nvme" "dm_mod" ];`

**排查步骤**：

1. 编辑内核 cmdline，添加 `init=/bin/sh` 或 `break=mount` 进入 initramfs shell
2. 运行 `lsblk`、`blkid` 确认设备
3. 查看 `dmesg` 中的磁盘或 LVM 错误

---

## 2. 系统初始化：systemd 的核心角色

systemd 作为 PID 1，是现代 Linux 系统的初始化系统和服务管理器。它负责并行启动服务、维护依
赖关系、管理 cgroups，并提供统一的系统管理接口。

### 2.1 systemd 概览与基本操作

systemd 不仅仅是一个初始化系统，它提供了完整的系统管理生态，包括日志收集、网络管理、时间同
步等功能。

**核心功能**：

- **服务管理**：并行启动 units，维护依赖关系
- **日志系统**：统一的二进制日志格式，支持高效查询
- **会话管理**：处理用户登录、设备权限分配
- **网络管理**：现代化的网络配置管理
- **资源控制**：通过 cgroups 实现进程隔离和资源限制

**常用命令**：

```bash
# 系统状态查看
systemctl get-default                     # 默认 target
systemctl list-units --type=service       # 列出服务
systemctl status sshd.service             # 服务状态
journalctl -u sshd.service -b             # 服务日志

# 性能分析
systemd-analyze blame                     # 启动耗时分析
systemd-analyze critical-chain            # 关键路径分析

# 日志管理
journalctl -b                             # 本次启动日志
journalctl -b -1                          # 上次启动日志
journalctl --disk-usage                    # 日志占用空间
```

**NixOS 特殊说明**：在 NixOS 中，`/etc/systemd/system` 下的配置文件都是通过声明式参数生成
的软链接，指向 `/nix/store`。修改配置应通过 NixOS 配置系统，而非直接编辑这些文件。

**配置文件路径**：

- `/etc/systemd/system/`：系统级服务配置
- `/run/current-system/sw/lib/systemd/system/`（NixOS）或 `/usr/lib/systemd/system/`（其他
  发行版）：软件包提供的默认配置
- `/etc/systemd/user/`：用户级服务配置

### 2.2 日志系统

systemd-journald 是 systemd 内置的日志收集守护进程，统一处理内核、系统服务及应用的日志，是
现代 Linux 系统日志管理的核心组件。

#### 2.2.1 核心特性

| 特性               | 说明                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| **统一收集**       | 内核日志、systemd 单元（stdout/stderr）、普通进程、容器、第三方 syslog 均汇总到同一日志流。    |
| **二进制索引**     | 以 B+树（有序索引）+偏移量建立字段索引，支持精确查询与时间/优先级范围查询，速度远超文本 grep。 |
| **字段化存储**     | 自动生成 `_PID`、`_UID`、`_SYSTEMD_UNIT` 等可信字段（不可伪造）；支持自定义 `FOO=bar` 字段。   |
| **自动轮转与压缩** | 按“大小、时间、文件数”回收日志；轮转后默认用 LZ4 压缩，节省 60% 以上空间。                     |
| **速率限制**       | 可通过 `RateLimitIntervalSec=`/`RateLimitBurst=` 调整。                                        |
| **日志防篡改**     | 配置 `Seal=yes` 后，用 `journalctl --setup-keys` 生成密钥，之后可用该密钥验证日志完整性。      |

#### 2.2.2 日志的4个收集入口

journald 仅通过标准化入口收集日志，确保来源可追溯：

1. **内核日志**：内核 `printk()` 输出 → `/dev/kmsg` → journald（会自动添加 `_PID`/`_COMM`
   等字段）；
2. **systemd 单元 stdout/stderr**：单元进程输出自动捕获，会附加
   `_SYSTEMD_UNIT=xxx.service` 等 systemd 相关字段；
3. **本地 Socket**：`/run/systemd/journal/socket` 等，接收 `logger`/`systemd-cat` 及旧
   syslog 应用日志；
4. **显式 API**：`sd_journal_send()`，仅需自定义复杂结构化日志时使用（譬如 Docker
   daemon）, 一般直接 print 即可。

#### 2.2.3 日志优先级与核心配置

##### 1. 日志优先级简述

日志按严重程度分 8 级（数字越小，级别越高），常用级别：

- `err`：错误（部分功能异常），级别 3
- `warning`：警告（潜在风险），级别 4
- `info`：信息（常规运行日志），级别 6
- `debug`：调试（开发细节），级别 7

可用于筛选关键日志。

##### 2. journald 配置

主配置文件：`/etc/systemd/journald.conf`，支持通过 `/etc/systemd/journald.conf.d/*.conf`
覆盖配置，核心配置项如下：

| 配置项             | 说明                 | 示例                                                             |
| ------------------ | -------------------- | ---------------------------------------------------------------- |
| `Storage=`         | 存储策略             | `persistent`（存 `/var/log/journal`，推荐）/`volatile`（存内存） |
| `SystemMaxUse=`    | 持久存储最大占用     | `1G`                                                             |
| `MaxRetentionSec=` | 日志最大保留时间     | `1month`                                                         |
| `ForwardToSyslog=` | 是否转发到旧日志系统 | `yes`（兼容传统文本日志）                                        |
| `Seal=`            | 是否启用日志防篡改   | `yes`                                                            |

**生产配置示例**：

```ini
# /etc/systemd/journald.conf.d/00-production.conf
[Journal]
Storage=persistent
SystemMaxUse=2G
MaxRetentionSec=3month
ForwardToSyslog=yes
Seal=yes
```

配置生效需重启服务：`sudo systemctl restart systemd-journald`

#### 2.2.4 实验：用 logger 验证日志收集

下面演示如何使用 `logger` 将**结构化日志**直接写进 journal，并立即用 journalctl 检索。

首先写入日志：

```bash
logger --journald <<EOF
SYSLOG_IDENTIFIER=myapp
PRIORITY=3
MESSAGE=用户登录失败
USER_ID=alice
LOGIN_RESULT=fail
EOF
```

其中的 `SYSLOG_IDENTIFIER`, `PRIORITY`, `MESSAGE` 在 journald 中都有属性对应，而后两个
`USER_ID` 与 `LOGIN_RESULT` 则属于自定义的日志标签。

然后查询日志：

```bash
# 2. 按标识符过滤
journalctl -t myapp
# 等价于
journalctl SYSLOG_IDENTIFIER=myapp

# 3. 按优先级+自定义字段精确定位
journalctl -p err LOGIN_RESULT=fail
```

#### 2.2.5 旧日志系统与 /var/log/ 解析

##### 旧日志系统：基于 syslog 的文本管理

在 systemd 普及前，Linux 依赖 **syslog 协议+文本文件** 管理日志，核心组件是
**rsyslog**（syslog 主流实现，功能强于早期 `syslogd`）。

- **旧系统工作流**：应用通过 `syslog(3)` 接口输出日志 → rsyslog 接收 → 按“设施+优先级”写入
  `/var/log/` 文本文件；
- **现代系统中的角色**：rsyslog 不再是核心收集器，而是作为“兼容层”——接收 journald 转发的日
  志，生成传统文本文件（如 `/var/log/auth.log`），或转发到远程日志服务器（支持 TCP/TLS 加
  密）。

##### /var/log/ 常见文件及功能

现代系统中，这些文件由 rsyslog 生成（兼容旧习惯），不同发行版名称略有差异，但都为纯文本格
式：

| 文件（或目录）                                             | 主要发行版差异               | 功能说明                                                                   |
| ---------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| `/var/log/messages`                                        | RHEL/CentOS/SUSE             | 系统通用日志：服务启停、内核提示、非专项应用消息。                         |
| `/var/log/syslog`                                          | Ubuntu/Debian                | 等价于 RHEL 的 `messages`，存储内核及一般系统日志。                        |
| `/var/log/auth.log`（Ubuntu）<br>`/var/log/secure`（RHEL） | 名称不同                     | 认证与授权事件：SSH 登录、su/sudo、用户添加/删除、PAM 告警。安全审计必看。 |
| `/var/log/kern.log`                                        | 通用                         | 仅内核环控输出：硬件故障、驱动加载、OOM、segfault。                        |
| `/var/log/cron`                                            | 通用                         | crond 执行记录：任务启动/结束、错误输出、邮件发送结果。                    |
| `/var/log/btmp`                                            | 通用                         | 二进制文件，记录**失败**登录（lastb 读取）；大小随暴力破解增长。           |
| `/var/log/wtmp`                                            | 通用                         | 二进制文件，记录**成功**登录/注销/重启（last、who 读取）。                 |
| `/var/log/lastlog`                                         | 通用                         | 二进制文件，记录每个用户最近一次登录时间（lastlog 读取）。                 |
| `/var/log/journal/`                                        | 启用 systemd-journald 后可见 | **目录**；若 `Storage=persistent`，则二进制 journal 文件存于此。           |

#### 2.2.6 日志写入最佳实践

| 场景                  | 推荐做法                                                                                 |
| --------------------- | ---------------------------------------------------------------------------------------- |
| Shell脚本（独立运行） | `logger -t 脚本名 -p daemon.err "错误：$msg"`（如 `logger -t backup -p err "备份失败"`） |
| 应用程序              | 优先考虑使用 systemd service, 少数场景可考虑直接调用 `sd_journal_send()` API             |
| 容器                  | Docker/Podman 加 `--log-driver=journald`（容器内正常输出即可）                           |
| 高频日志              | 设 `RateLimitIntervalSec=0` 关闭限制（需评估风险），或批量写入                           |
| 敏感信息              | 脱敏处理（如 `PASSWORD=***`），避免明文存储                                              |

#### 2.2.7 运维命令速查

```bash
# 一、日志查询（含优先级过滤）
# 实时跟踪服务日志（仅看 err 及以上级别）
journalctl -f -p err -u sshd.service
# 等价于
journalctl -f -p err _SYSTEMD_UNIT=sshd.service
# 按时间+优先级过滤（过去1小时 warning 及以上）
journalctl --since "1h ago" -p warning
# -p 的参数既可使用名称，也可使用对应的数字，warning 对应 4
journalctl --since "1h ago" -p 4
# 内核日志（本次启动的 err 日志）
journalctl -k -p err -b
# 按自定义字段过滤（USER_ID=1001 + 优先级 err）
journalctl USER_ID=1001 -p err
# 通过 Perl 格式的正则表达式搜索日志
journalctl --grep "Auth"

# 二、日志管理
# 查看 journal 占用空间
sudo journalctl --disk-usage
# 清理日志（保留最近2周/500M）
sudo journalctl --vacuum-time=2weeks
sudo journalctl --vacuum-size=500M
# 手动轮转日志
sudo journalctl --rotate

# 三、旧日志文件操作
# 实时查看认证日志（Ubuntu）
tail -f /var/log/auth.log
# 实时查看认证日志（CentOS）
tail -f /var/log/secure

# 四、日志防篡改验证
sudo journalctl --setup-keys > /etc/journal-seal-key
sudo chmod 600 /etc/journal-seal-key
sudo journalctl --verify --verify-key=$(cat /etc/journal-seal-key)
```

### 2.3 设备管理：udev 的角色

udev 是 Linux 用户空间的设备管理员，负责处理内核的设备事件，创建节点并设置权限。

**工作流程**：

1. 内核检测到硬件变化，发出 uevent
2. udevd 接收事件，根据规则文件（`/run/current-system/sw/lib/udev/rules.d/`（NixOS）或
   `/usr/lib/udev/rules.d/`（其他发行版）、`/etc/udev/rules.d/`）匹配并执行动作（`RUN` 脚
   本、设置 `OWNER`/`GROUP`/`MODE`、创建 symlink、设置权限）。
3. 通知 systemd，可能触发 device units

**规则示例**：

```ini
# /etc/udev/rules.d/90-mydevice.rules
SUBSYSTEM=="input", ATTRS{idVendor}=="abcd", ATTRS{idProduct}=="1234", MODE="660", GROUP="input", TAG+="uaccess"
```

`TAG+="uaccess"` 是现代桌面用来让 systemd-logind 接管设备权限与 session ACL（由 logind 配
置），确保只有当前活动会话能访问输入、音频、GPU 等设备。

#### 设备权限与 ACL

现代 systemd + logind 使用 udev tag `uaccess` 或 `seat` 标签来由 logind 把设备 ACL 授予当
前的登录 session。具体流程：

- udev 创建 `/dev/input/eventX` 并打上 `TAG+="uaccess"`.
- systemd-logind 对应的 PAM/session 系统会把该设备的 ACL 授予当前会话的用户，这样运行在会
  话内的 Wayland compositor 与其子进程可以访问设备。

**检查设备权限分配**：

```bash
# 查看某设备的 udev 属性
$ udevadm info -a -n /dev/input/event5

# 实时监控 udev 事件
$ sudo udevadm monitor --udev --property

# 查看 seat 状态与 ACL
$ loginctl seat-status seat0
# 或
$ loginctl show-session <id> -p Remote -p Display -p Name
```

#### 故障排查

场景：插入外接键盘后，Wayland 会话收不到键盘事件（键盘无效）

排查步骤：

1. 在主机上用 `udevadm monitor` 插入键盘，观察是否有 udev 事件被触发：

   ```bash
   sudo udevadm monitor --udev
   ```

2. 检查 `/dev/input/` 是否生成新节点：`ls -l /dev/input/by-id`。
3. 用 `udevadm info -a -n /dev/input/eventX` 查看该设备的属性，确认 `TAG` 是否包含
   `uaccess` 或 `seat`.
4. 使用 `loginctl seat-status seat0` 看设备是否分配给当前会话。若没有，可能是 PAM/session
   未正确建立或 udev 规则没有打上 tag。
5. 检查 `journalctl` 中关于 udev 的日志：`journalctl -b -u systemd-udevd` 或
   `journalctl -k | grep -i udev`。
6. 临时解决：用 `chmod`/`chown` 修改设备权限验证是否恢复（不建议长期采用）。

   ```bash
   sudo chown root:input /dev/input/eventX
   sudo chmod 660 /dev/input/eventX
   ```

7. 永久修复：在 `/etc/udev/rules.d/` 中添加规则确保 `TAG+="uaccess"` 或正确的OWNER/GROUP。
   然后 `udevadm control --reload-rules && sudo udevadm trigger`。

**注意**：NixOS 下直接编辑 `/etc/udev/rules.d` 可能是临时的（Nix 管理的文件会被系统重建覆
盖），正确做法是在 `configuration.nix` 中配置 `services.udev.extraRules` 或把规则放在
`environment.etc` 并由 Nix 管理。

**配置文件路径**：

- `/etc/udev/rules.d/`：系统管理员自定义规则（优先级最高）
- `/run/current-system/sw/lib/udev/rules.d/`（NixOS）或 `/usr/lib/udev/rules.d/`（其他发行
  版）：软件包提供的默认规则

---

## 3. PolicyKit - 细粒度的系统权限管理

PolicyKit（现称 polkit）是一个用于控制系统级权限的框架，它提供了一种比传统 Unix 权限更细粒
度的授权机制。在现代 Linux 桌面系统中，PolicyKit 允许非特权用户执行某些需要特权的系统操作
（如关机、重启、挂载设备、修改系统时间等），而无需获取完整的 root 权限。

### 3.1 PolicyKit 的核心概念

**配置文件路径**：

- `/etc/polkit-1/`：NixOS 声明式配置中定义的自定义规则（优先级最高）
- `/run/current-system/sw/share/polkit-1/`（NixOS）或 `/usr/share/polkit-1/`（其他发行
  版）：软件包提供的默认规则

上述文件夹中又包含两类配置：

- **动作（Actions）**
  - 定义在配置文件夹的 `actions` 目录中的 XML 文件（如 `/etc/polkit-1/actions/`），描述可
    授权的操作。每个动作都有唯一的标识符，如 `org.freedesktop.login1.power-off` 表示关机操
    作。
- **规则（Rules）**
  - JavaScript 文件，定义授权决策逻辑，位于上述配置文件夹的 `rules.d/` 目录中（如
    `/etc/polkit-1/rules.d/`）。规则决定了在特定条件下是否授权某个操作。在 NixOS 中，推荐
    使用声明式配置而非直接修改 `/etc` 目录。

**身份认证代理（Authentication Agents）**：桌面环境提供的图形界面组件，用于在用户需要身份
验证时弹出认证对话框。例如，当普通用户尝试关机时，认证代理会提示输入管理员密码。

> 举例来说，我使用的是 Niri 窗口管理器，它的 Nix Flake 启用了 pokit-kde-agent-1 作为其
> Authentication Agent, 配置参见
> [sodiboo/niri-flake](https://github.com/sodiboo/niri-flake/blob/27e012b4cd49e9ac438573ec7a6db3e5835828c3/flake.nix#L497-L509).

### 3.2 PolicyKit 的工作原理

当应用程序请求执行需要特权的操作时，系统服务会询问 PolicyKit 是否授权。PolicyKit 的评估过
程如下：

1. **身份识别**：确定请求者的身份（用户、组、会话等）
2. **规则匹配**：检查是否有适用的规则文件
3. **权限评估**：根据规则返回以下结果之一：
   - `yes`：直接允许，无需认证
   - `no`：直接拒绝
   - `auth_self`：需要用户自己认证（输入当前用户密码）
   - `auth_admin`：需要管理员认证（输入 root 密码）
   - `auth_self_keep`/`auth_admin_keep`：认证后在一段时间内保持授权

### 3.3 PolicyKit 的配置示例

在传统的 Linux 发行版中，管理员可以通过创建自定义规则来修改默认行为。例如，允许 `wheel` 组
的用户无需密码即可关机：

```javascript
// /etc/polkit-1/rules.d/10-shutdown.rules
polkit.addRule(function (action, subject) {
  if (action.id == "org.freedesktop.login1.power-off" && subject.isInGroup("wheel")) {
    return polkit.Result.YES
  }
})
```

**NixOS 中的配置方法**：在 NixOS 中，推荐使用声明式配置而非直接修改 `/etc` 目录。可以通过
`security.polkit` 配置项来管理 PolicyKit 规则：

````nix
# configuration.nix
{
  security.polkit.enable = true;

  # 添加自定义规则
  security.polkit.extraConfig = ''
    polkit.addRule(function(action, subject) {
      if (action.id == "org.freedesktop.login1.power-off" &&
          subject.isInGroup("wheel")) {
        return polkit.Result.YES;
      }
    });
  '';
}

### 3.4 PolicyKit 与 D-Bus 的集成

PolicyKit 与 D-Bus 深度集成，为 D-Bus 服务提供动态授权机制。许多系统服务（如 systemd、NetworkManager、udisks 等）都使用 PolicyKit 来控制对其 D-Bus 接口的访问。当客户端通过 D-Bus 调用需要特权的方法时，服务会调用 PolicyKit 进行授权检查。

**常用调试命令**：
```bash
# 查看 PolicyKit 服务状态
systemctl status polkit

# 检查特定动作的授权情况
pkcheck --action-id org.freedesktop.login1.power-off --process $$ --allow-user-interaction

# 查看 PolicyKit 日志
journalctl -u polkit -f

# 查看 NixOS 中的 PolicyKit 动作定义
ls -la /run/current-system/sw/share/polkit-1/actions/

# 查看当前生效的 PolicyKit 规则
ls -la /etc/polkit-1/rules.d/
````

**NixOS 注意事项**：在 NixOS 中，PolicyKit 的动作定义和系统级规则都存储在
`/run/current-system/sw/share/polkit-1/` 目录下，这是当前系统配置的一部分。由于 NixOS 的纯
函数式特性，这些路径是只读的，所有的配置都应该通过 NixOS 的配置文件（如
`configuration.nix`）来管理，而不是直接修改这些目录。这种设计确保了系统配置的可重现性和原
子性更新。

---

## 4. D-Bus 系统总线 - 应用间通信的主要通道

D-Bus 是 Linux 系统中主流的进程间通信（IPC）机制，旨在解决不同进程（尤其是桌面应用、系统服
务）间的高效、安全通信问题，广泛用于 GNOME、KDE 等桌面环境及系统服务管理（如 systemd）。它
本质是 “消息总线”，通过中心化的 “总线守护进程” 实现多进程间的消息路由。

D-Bus 作为 systemd 的依赖被安装，并且 system bus 和 user/session bus 会在系统启动与用户登
录时自动创建。

systemd 本身就是一个 D-Bus 服务，我们在使用 `systemctl` 命令与 systemd 交互时，实际上就是
通过 D-Bus 与 `org.freedesktop.systemd1` 通信。

### 关键概念

D-Bus 通过 “对象 - 接口” 模型封装功能，以下结合 `systemd1` 与 `logind1` 的真实定义，对应核
心概念：

| 概念              | 定义与作用                                    | 示例（systemd1/logind1）                                                                                                                   |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 总线（Bus）       | 消息传输的 “高速公路”，分系统 / 会话两类      | 系统总线 `/var/run/dbus/system_bus_socket`（`systemd1`/`logind1` 唯一使用的总线）                                                          |
| 服务名（Name）    | 服务端在总线上的 “身份证”，唯一可请求         | `org.freedesktop.systemd1`（`systemd` 服务名）、`org.freedesktop.login1`（`logind` 服务名）                                                |
| 对象（Object）    | 服务端功能的 “实例载体”，有唯一路径           | `/org/freedesktop/systemd1`（`systemd1` 根对象）、`/org/freedesktop/login1`（`logind1` 根对象）                                            |
| 接口（Interface） | 定义对象的 “功能契约”（方法、信号、属性）     | `org.freedesktop.systemd1.Manager`（`systemd1` 核心接口）、`org.freedesktop.login1.Manager`（`logind1` 核心接口）                          |
| 方法（Method）    | 客户端可主动调用的 “同步功能”（有请求有返回） | `systemd1` 的 `StartUnit`（启动系统单元，如 `nginx.service`）、`logind1` 的 `ListSessions`（查询所有活跃用户会话）                         |
| 信号（Signal）    | 服务端主动发送的 “异步通知”（无返回）         | `systemd1` 的 `UnitActiveChanged`（单元状态变化，如 `nginx` 从 `inactive` 变为 `active`）、`logind1` 的 `SessionNew`（新用户登录创建会话） |
| 属性（Property）  | 对象的 “状态数据”，支持读取 / 写入            | `systemd1` 的 `ActiveUnits`（所有活跃系统单元列表）、`logind1` 的 `CanPowerOff`（当前系统是否允许关机，布尔值）                            |

可使用 `busctl list` 查看系统中的所有 D-Bus 对象：

```bash
# 所有 system bus 对象
› busctl --system list --no-pager | grep org.
org.blueman.Mechanism                     - -               -                (activatable) -                         -       -
org.bluez                              1421 bluetoothd      root             :1.6          bluetooth.service         -       -
org.bluez.mesh                            - -               -                (activatable) -                         -       -
org.freedesktop.Avahi                  1420 avahi-daemon    avahi            :1.7          avahi-daemon.service      -       -
org.freedesktop.DBus                      1 systemd         root             -             init.scope                -       -
org.freedesktop.Flatpak.SystemHelper      - -               -                (activatable) -                         -       -
org.freedesktop.GeoClue2                  - -               -                (activatable) -                         -       -
org.freedesktop.PolicyKit1             2216 polkitd         polkituser       :1.22         polkit.service            -       -
org.freedesktop.RealtimeKit1           2539 rtkit-daemon    root             :1.41         rtkit-daemon.service      -       -
org.freedesktop.UDisks2                2492 udisksd         root             :1.31         udisks2.service           -       -
org.freedesktop.home1                     - -               -                (activatable) -                         -       -
org.freedesktop.hostname1                 - -               -                (activatable) -                         -       -
org.freedesktop.import1                   - -               -                (activatable) -                         -       -
org.freedesktop.locale1                   - -               -                (activatable) -                         -       -
org.freedesktop.login1                 1504 systemd-logind  root             :1.8          systemd-logind.service    -       -
org.freedesktop.machine1                  - -               -                (activatable) -                         -       -
org.freedesktop.network1               1292 systemd-network systemd-network  :1.3          systemd-networkd.service  -       -
org.freedesktop.oom1                    934 systemd-oomd    systemd-oom      :1.1          systemd-oomd.service      -       -
org.freedesktop.portable1                 - -               -                (activatable) -                         -       -
org.freedesktop.resolve1               1293 systemd-resolve systemd-resolve  :1.0          systemd-resolved.service  -       -
org.freedesktop.systemd1                  1 systemd         root             :1.4          init.scope                -       -
org.freedesktop.sysupdate1                - -               -                (activatable) -                         -       -
org.freedesktop.timedate1                 - -               -                (activatable) -                         -       -
org.freedesktop.timesync1              1148 systemd-timesyn systemd-timesync :1.2          systemd-timesyncd.service -       -
org.opensuse.CupsPkHelper.Mechanism       - -               -                (activatable) -                         -       -

# 所有 session bus 对象
› busctl --user list --no-pager | grep org.
...
org.fcitx.Fcitx-0                                                                 76699 fcitx5          ryan :1.284        user@1000.service -       -
org.fcitx.Fcitx5                                                                  76699 fcitx5          ryan :1.282        user@1000.service -       -
org.freedesktop.DBus                                                               2127 systemd         ryan -             user@1000.service -       -
org.freedesktop.FileManager1                                                          - -               -    (activatable) -                 -       -
org.freedesktop.Notifications                                                      3539 .mako-wrapped   ryan :1.81         user@1000.service -       -
org.freedesktop.ReserveDevice1.Audio0                                              2542 wireplumber     ryan :1.50         user@1000.service -       -
org.freedesktop.ReserveDevice1.Audio1                                              2542 wireplumber     ryan :1.50         user@1000.service -       -
org.freedesktop.ScreenSaver                                                        2192 niri            ryan :1.9          user@1000.service -       -
org.freedesktop.a11y.Manager                                                       2192 niri            ryan :1.13         user@1000.service -       -
org.freedesktop.impl.portal.PermissionStore                                        2410 .xdg-permission ryan :1.28         user@1000.service -       -
org.freedesktop.impl.portal.Secret                                                    - -               -    (activatable) -                 -       -
org.freedesktop.impl.portal.desktop.gnome                                             - -               -    (activatable) -                 -       -
org.freedesktop.impl.portal.desktop.gtk                                            2475 .xdg-desktop-po ryan :1.33         user@1000.service -       -
org.freedesktop.portal.Desktop                                                     2350 .xdg-desktop-po ryan :1.26         user@1000.service -       -
org.freedesktop.portal.Documents                                                   2428 .xdg-document-p ryan :1.30         user@1000.service -       -
org.freedesktop.portal.Fcitx                                                      76699 fcitx5          ryan :1.283        user@1000.service -       -
org.freedesktop.portal.Flatpak                                                        - -               -    (activatable) -                 -       -
org.freedesktop.portal.IBus                                                       76699 fcitx5          ryan :1.285        user@1000.service -       -
org.freedesktop.secrets                                                            2161 .gnome-keyring- ryan :1.55         session-1.scope   1       -
org.freedesktop.systemd1                                                           2127 systemd         ryan :1.1          user@1000.service -       -
...
```

### 系统总线与会话总线

| 总线类型                | 作用场景                 | 典型用途                                                                             | 运行用户     |
| ----------------------- | ------------------------ | ------------------------------------------------------------------------------------ | ------------ |
| 系统总线（System Bus）  | 系统级服务通信           | `systemd1` 单元管理（启动 / 停止服务）、`logind1` 用户会话 / 电源控制（关机 / 重启） | root（特权） |
| 会话总线（Session Bus） | 单个用户会话内的应用通信 | 桌面应用交互（如窗口切换、通知）                                                     | 当前登录用户 |

### D-Bus 的三类角色

1.  **总线守护进程（dbus-daemon）**

    架构的 “中枢”，每个总线对应一个守护进程，核心职责：

    - 管理进程的连接（如验证 `普通用户` 是否有权调用 `logind1` 的 `PowerOff` 方法）；

    - 路由消息（将客户端请求的 “启动 `nginx` 服务” 转发给 `systemd1`）；

    - 维护服务注册表（记录 `org.freedesktop.login1` 与 `logind` 进程的映射关系）。

1.  **服务端（Service）**

    提供功能的进程（如 `systemd` 进程、`logind` 进程），核心操作：

    - 向总线注册 “服务名”（`systemd1` 注册 `org.freedesktop.systemd1`，`logind1` 注册
      `org.freedesktop.login1`，均为唯一标识）；

    - 暴露 “对象” 和 “接口”（如 `systemd1` 暴露 `/org/freedesktop/systemd1` 对象与
      `org.freedesktop.systemd1.Manager` 接口），供客户端调用。

1.  **客户端（Client）**

    调用服务的进程（如 `systemctl` 命令、桌面电源菜单），核心操作：

    - 连接系统总线后，通过服务名（如 `org.freedesktop.login1`）找到 `logind` 服务；

    - 调用服务端暴露的方法（如通过 `logind1` 的 `ListSessions` 查询当前用户会话），或订阅
      信号（如监听 `systemd1` 的 `UnitActiveChanged` 单元状态变化）。

### 常见操作示例

下面我们通过一些命令来演示 D-Bus 总线的用途：

```bash
# 模拟 `systemctl status dbus` 的功能
busctl --system --json=pretty call \
  org.freedesktop.systemd1 \
  /org/freedesktop/systemd1/unit/dbus_2eservice \
  org.freedesktop.DBus.Properties GetAll s org.freedesktop.systemd1.Unit

# 模拟 `systemctl stop sshd`
sudo gdbus call --system \
  --dest org.freedesktop.systemd1 \
  --object-path /org/freedesktop/systemd1 \
  --method org.freedesktop.systemd1.Manager.StopUnit \
  "sshd.service" "replace"

# 模拟 `systemctl start sshd`
sudo gdbus call --system \
  --dest org.freedesktop.systemd1 \
  --object-path /org/freedesktop/systemd1 \
  --method org.freedesktop.systemd1.Manager.StartUnit \
  "sshd.service" "replace"

# 模拟 `notify-send "The Summary" "Here’s the body of the notification"`
nix shell nixpkgs#glib
gdbus call --session \
    --dest org.freedesktop.Notifications \
    --object-path /org/freedesktop/Notifications \
    --method org.freedesktop.Notifications.Notify \
    my_app_name \
    42 \
    gtk-dialog-info \
    "The Summary" \
    "Here’s the body of the notification" \
    [] \
    {} \
    5000

# 获取当前时区
busctl get-property org.freedesktop.timedate1 /org/freedesktop/timedate1 \
    org.freedesktop.timedate1 Timezone

# 查询主机名
busctl get-property org.freedesktop.hostname1 /org/freedesktop/hostname1 \
    org.freedesktop.hostname1 Hostname

```

### 调试与监控命令

```
# 看 systemctl 与 systemd 的完整交互（method-call + signal）
sudo busctl monitor --system | grep 'org.freedesktop.systemd1'
# 或者使用 --match 过滤，但这需要提前知道 interface 的全名
sudo busctl monitor --match='interface=org.freedesktop.systemd1.Manager'

# 跟 busctl monitor 功能几乎完全一致，也可通过 match rule 过滤
sudo dbus-monitor --system "interface='org.freedesktop.systemd1.Manager'"

# gdbus 只监听 signals，只能用来调试「服务有没有正确发出 signal」
sudo gdbus monitor --system -d org.freedesktop.systemd1.Manager
```

### D-Bus 的权限管控

#### D-Bus 的原生权限管控机制

D-Bus 本身具备多层权限管控能力，从总线接入、消息路由到敏感操作授权，形成了系统级的基础安全
保障，核心机制包括：

1.  **总线配置文件（静态规则管控）**

    通过 XML 配置文件定义细粒度访问规则，实现对 “谁能访问哪些服务 / 方法” 的静态限制。例
    如：

    - 系统总线的服务级规则（如 `/etc/dbus-1/system.d/org.freedesktop.login1.conf`）可限制
      普通用户调用 `org.freedesktop.login1.Manager.PowerOff`（关机方法）；

    - 全局规则（如 `/etc/dbus-1/system.conf`）可限定仅 `root` 或 `dbus` 组用户访问
      `org.freedesktop.systemd1`（systemd 服务）的核心接口。

      规则遵循 “`deny` 优先级高于 `allow`、服务级规则高于全局规则” 的逻辑，从总线层面直接
      拦截未授权请求。

1.  **PolicyKit（动态授权管控）**

    针对静态规则无法覆盖的动态场景（如普通用户临时需要执行敏感操作），D-Bus 集成
    PolicyKit（现称 `polkit`）实现动态授权。系统服务（如 `logind1`、`systemd1`）会在
    `/run/current-system/sw/share/polkit-1/actions/`（NixOS 中）或
    `/run/current-system/sw/share/polkit-1/actions/`（NixOS）或
    `/usr/share/polkit-1/actions/`（传统发行版中）定义 "可授权动作"，例如
    `org.freedesktop.login1.power-off`（对应 `logind1` 的关机方法）：

    - 普通用户调用时，会触发认证流程（如输入管理员密码），认证通过后临时获得授权；

    - 活跃控制台用户可直接授权，无需额外验证，兼顾安全性与易用性。

1.  **连接层基础隔离**

    D-Bus 总线套接字（如系统总线 `/var/run/dbus/system_bus_socket`）默认仅开放 `root` 和
    `dbus` 组用户的读写权限，普通进程需通过 `dbus-daemon` 认证后才能建立连接。同时，每个连
    接会被分配唯一 ID（如 `:1.42`），并与进程的 PID/UID/GID 绑定，防止身份伪造与未授权接
    入。

#### Flatpak 对 D-Bus 权限的细粒度管控

在现代 Linux 桌面中，若需将商业软件等非信任应用运行在沙箱中，同时保障 “必要 D-Bus 交互不中
断、越权访问被阻断”，Flatpak 采用 **“底层沙箱隔离 + 上层代理过滤”** 的双层方案 —— 其中
`bubblewrap` 是 Flatpak 依赖的底层沙箱工具，负责环境隔离；`xdg-dbus-proxy` 是上层过滤组
件，负责 D-Bus 细粒度管控，两者协同实现完整安全隔离：

##### 1. 底层基础隔离：bubblewrap 的 “socket 隐藏与代理挂载”

Flatpak 以 `bubblewrap`（简称 bwrap）为底层沙箱基础，利用其 `bind mount` 和
`user namespace` 能力完成环境初始化，核心目标是切断沙箱应用与宿主 D-Bus 总线的直接联系：

- **隐藏宿主 socket**：`bubblewrap` 会屏蔽宿主的 D-Bus 总线套接字（如不将
  `/var/run/dbus/system_bus_socket` 挂载进沙箱），避免应用绕过管控直接访问宿主总线；

- **挂载代理 socket**：同时，`bubblewrap` 会将 `xdg-dbus-proxy` 在宿主侧预先创建的 **私有
  代理 socket**，通过 `bind mount` 挂载到沙箱内的默认 D-Bus socket 路径（如沙箱内的
  `/var/run/dbus/system_bus_socket`）。

  此时沙箱应用感知到的 “D-Bus 总线”，实际是 `xdg-dbus-proxy` 提供的代理接口，无法直接接触
  宿主真实总线。

##### 2. 上层规则过滤：xdg-dbus-proxy 的 “白名单校验”

`xdg-dbus-proxy` 作为 Flatpak 内置的 D-Bus 代理组件，会随沙箱应用启动，加载 Flatpak 根据应
用权限声明自动生成的过滤规则（粒度远细于 D-Bus 原生静态配置），例如：

```
\--talk=org.freedesktop.portal.FileChooser  # 允许调用文件选择门户服务

\--talk=org.freedesktop.Notifications       # 允许发送桌面通知

\--deny=org.freedesktop.systemd1            # 拒绝访问 systemd 服务

\--deny=org.freedesktop.login1.Manager.PowerOff  # 拒绝调用关机方法
```

这些规则可精确到 “服务名 + 接口 + 方法 + 对象路径”，弥补 D-Bus 原生配置在沙箱场景下 “动态
性不足、粒度较粗” 的局限。

##### 3. 消息流转：代理的 “校验 - 转发” 逻辑

沙箱应用无需修改代码，会默认连接沙箱内的 “代理 socket”，所有 D-Bus 消息（方法调用、信号订
阅）均需经过 `xdg-dbus-proxy` 的校验：

- 若目标服务 / 方法在白名单内（如 `org.freedesktop.portal.FileChooser.OpenFile`），代理会
  将消息转发至宿主 D-Bus 总线，并把返回结果回传应用；

- 若目标不在白名单内（如 `org.freedesktop.login1.Manager.PowerOff`），代理直接返回
  `AccessDenied` 错误，不向宿主总线转发任何消息，彻底阻断越权访问。

---

## 5. 用户会话：登录与桌面环境

用户从登录到进入桌面环境的过程涉及多个组件的协调：display manager 负责认证，systemd-logind
管理会话，window compositor 提供图形环境。这个阶段的故障往往表现为登录失败、权限错误或图形
界面异常。

### 5.1 登录流程解析

典型的图形登录流程：

1. **显示管理器启动**：greetd / GDM 等显示管理器显示登录界面
2. **用户认证**：通过 PAM 验证用户名 / 密码
3. **会话创建**：Display Manager 请求 logind 创建 session
4. **用户服务启动**：systemd 用户实例启动，运行用户配置的服务
5. **合成器启动**：获得环境变量和设备访问权限

**关键观察点**：

```bash
# 查看显示管理器日志
journalctl -u greetd
journalctl -b _COMM=greetd

# 检查会话状态
loginctl list-sessions
loginctl show-session <id> --property=Name,UID,State

# 查看用户服务日志
journalctl --user -b
```

**故障排查示例**：用户登录后合成器未启动

1. 检查用户服务日志：`journalctl --user -u hyprland.service`
2. 验证会话状态：`loginctl show-session <id> -p Active -p State`
3. 查看 PAM 认证日志：`journalctl -t login`

### 5.2 会话管理与 logind

systemd-logind 是连接登录、会话、设备权限和电源管理的核心服务。它通过 D-Bus 暴露 API，管理
用户会话并分配设备 ACL。

**核心职责**：

- **会话管理**：创建和维护用户会话，映射 session -> UID -> TTY / seat
- **设备访问**：基于 udev 标签分配设备 ACL 给当前会话
- **电源管理**：处理电源键事件，根据策略触发 suspend / shutdown
- **多座席支持**：支持 seat 概念，管理多用户场景

#### seat（座席）概念

> <https://www.freedesktop.org/wiki/Software/systemd/multiseat/>

- **seat**（座席）是 systemd/logind 引入的术语，用来表示“一组物理设备的集合”（例如一个显示
  器 + 一套键盘和鼠标 + 音频设备），以及与之关联的会话（sessions）。
- 所有设备默认都会被分配给 **seat0**, 想再搞一个 seat1 实现多人图形化登录，必须通过 udev
  规则完成如下操作：
  1. 必须拥有第二张显卡，这是硬性的前提！为了让 seat1 实际可用，还必须拥有第二套键鼠与声
     卡：
  1. 给第二块显卡写 udev 规则，打上 `TAG+="master-of-seat"` 并设置
     `ENV{ID_SEAT}="seat1"`；
  1. 把第二套键盘、鼠标、声卡等设备也写规则改成 `ENV{ID_SEAT}="seat1"`；
  1. 重启系统
- logind 会把 VT/图形会话绑定到具体 seat，从而按 seat 粒度做电源管理、设备访问控制、空闲检
  测等策略。
- **远程 SSH 登录不生成也不归属任何 seat**；logind 仅为其建立会话对象，seat 字段留空。因此
  seat 概念对 SSH 完全透明。

现代 Linux 桌面系统基本都是单用户使用，因此后续讨论默认聚焦单 seat 场景。

#### **常用命令**

```bash
# 会话管理
loginctl list-sessions                    # 列出所有会话
loginctl show-session <id> -p Name -p UID -p Seat  # 会话详情
loginctl terminate-session <id>           # 终止会话

# seat 管理
loginctl seat-status                      # 查看 seat 状态
loginctl seat-status seat0                # 特定 seat 详情

# D-Bus 接口调试
busctl --system call org.freedesktop.login1 \
  /org/freedesktop/login1 org.freedesktop.login1.Manager \
  ListSessions
```

#### **设备权限问题排查**

##### **Wayland compositor 启动但无法打开 `/dev/dri/card0`（GPU 权限问题）**

排查：

1. 确认 `ls -l /dev/dri/card0` 的 owner/group。通常应为 `root:video`，并且当前会话应被授予
   设备 ACL。
2. `loginctl seat-status seat0` 查看是否列出 `/dev/dri/card0` 并显示 ACL 给当前 session。
3. 若无，通过 `udevadm info /dev/dri/card0` 检查 udev 是否为 GPU 设备打上了
   `TAG+="uaccess"` 或 `TAG+="seat"`。
4. 查看 `journalctl -u systemd-logind`，看是否在用户登录时有关于设备分配的错误。
5. 若服务是以 system user 的方式启动，确保 compositor 的进程是在用户 session 下，而不是
   systemd 服务或 root 启动的进程（起进程身份不同会导致权限问题）。

##### 意外挂起/关机（电源键/睡眠按钮不按用户设置工作）

- 检查 `logind.conf`（NixOS 对应位置请用 NixOS config 来覆写）中 `HandlePowerKey`,
  `HandleLidSwitch` 的配置。
- `journalctl -u systemd-logind` 查看触发事件时间点；通常按键会以 D-Bus 事件或 ACPI 事件入
  日志。
- 若某桌面环境或应用拦截了按键，会阻止 logind 行为。可以通过 `busctl monitor` 监听
  `org.freedesktop.login1` 的消息，看是否收到请求。

- 若需要监控 logind 在登录/登出时做了什么，可以用
  `busctl monitor --system org.freedesktop.login1` 或：

  ```bash
  sudo dbus-monitor --system "interface='org.freedesktop.login1.Manager'"
  ```

  这能观察到 session 创建、移除、seat 分配、锁屏请求等信号。

### 5.3 Wayland 合成器架构

Wayland 采用客户端-服务器模型，合成器同时扮演显示服务器和窗口管理器的角色，直接与内核的DRM
/ KMS 和输入设备交互。

#### 架构对比：X11 vs Wayland

- **X11（传统）**：在 X11 架构中，**X Server**（例如 `Xorg`）是显示服务器，直接与显卡驱动
  和输入设备交互； **窗口管理器 / 桌面环境**（例如 i3、GNOME）则作为 **X client** 连接到 X
  Server，负责窗口摆放、装饰以及用户界面。使用 `startx`（实际上调用 `xinit`）启动图形会话
  时，本质流程是：先启动 X Server，再在其中运行窗口管理器或桌面环境（如 `exec i3`）。
  **Display Manager**（如 GDM、SDDM）在图形登录时会自动启动 X Server，并完成用户认证、设置
  `DISPLAY` 等环境变量，然后再运行会话。

- **Wayland（现代）**： **Wayland 合成器**本身既是显示服务器，又是窗口管理器和合成器的结合
  体。它直接通过内核的 **DRM/KMS** 控制显示模式，通过 **evdev/libinput** 采集并分发输入事
  件。Wayland 客户端应用通过 **Wayland socket**（通常位于 `$XDG_RUNTIME_DIR/wayland-0`，但
  具体名字可变）与合成器通信。因为合成器本身直接控制显示和输入设备，所以它可以**直接从一个
  已登录的 TTY 启动**，作为该 TTY 的图形会话的 “display server”，无需先用 `startx` 启动一
  个独立的 X Server。如果使用 Display Manager 登录 Wayland 会话，则由 DM 在合适的 TTY 启动
  合成器并准备会话环境。

#### 架构差异带来的实际影响

- **安全与权限**：Wayland 把合成器放在更核心的位置（它有直接设备访问），因此确保合成器运行
  在正确会话（由 logind 管理）下至关重要。错误地以 root 或 system service 启动合成器会导致
  权限/ACL 不一致（compositor 无法访问设备或安全级别问题）。
- **简化流程**：Wayland 把多个角色合并到合成器进程，消除了 X11 时代客户端/窗口管理器与服务
  器的分离复杂度，令直接从 tty 启动合成器成为可行且常见的做法。
- **兼容性**：Xwayland 提供对 legacy X11 应用的兼容，合成器负责在启动时/按需启动 Xwayland
  以支持老应用。

#### 图形栈组件

**输入处理组件**：

- **libinput**：从 `/dev/input/*` 读取事件并做预处理（手势识别、触摸板边缘、键盘元键处理
  等）
- 合成器使用 libinput 的 API 进行设备枚举与事件回调
- 可用 `libinput list-devices` 查看被 libinput 管理的设备（需 root 或在 session 中运行）

**图形渲染组件**：

- **Mesa**：提供 OpenGL/Vulkan 的开源实现
- **EGL**：Khronos 组织定义的接口，将 OpenGL/Vulkan 与窗口系统连接
- **GBM**(Generic Buffer Manager)：Mesa 的缓冲管理接口，用于分配图形缓冲区给 GPU
- **DRM**：内核中的 Direct Rendering Manager，控制显示模式设置（KMS）和页面翻转

**设备访问**：

- 合成器通过 `/dev/dri/card0` 与内核 DRM 交互
- 通过 `/dev/input/event*` 访问输入设备

**常用调试命令**：

```bash
# GPU device
$ ls /dev/dri
# 查看 Mesa/OpenGL renderer
$ glxinfo | grep "OpenGL renderer"
# 列出 libinput 管理设备（需要 root）
$ sudo libinput list-devices
```

---

## 6. 网络连接：从硬件到互联网

网络连接是现代桌面的基础功能，涉及硬件驱动、固件加载、网络管理和 DNS 解析等多个环节。网络
故障是最常见的桌面问题之一，理解其工作原理有助于快速定位和解决连接问题。

### 6.1 网络架构概览

现代 Linux 桌面使用 systemd-networkd 配合 iwd 进行网络管理，形成完整的网络解决方案。

**网络协议栈**：

- **硬件层**：网卡驱动和固件
- **链路层**：MAC 地址管理和链路检测
- **网络层**：IP 地址配置和路由管理
- **传输层**：TCP / UDP 连接管理
- **应用层**：DNS 解析和服务发现

**主要组件**：

- **systemd-networkd**：网络接口管理，处理 DHCP 和静态配置
- **iwd**：无线网络管理，支持 WPA2 / WPA3
- **systemd-resolved**：DNS 解析和缓存

### 6.2 网络连接流程

**有线网络**：

1. 内核加载网卡驱动
2. 检测链路状态（网线连接）
3. systemd-networkd 通过 DHCP 获取 IP 配置
4. 配置路由和 DNS

**无线网络**：

1. 加载无线网卡驱动和固件
2. iwd 扫描可用网络
3. 选择网络并进行认证（WPA2 / WPA3）
4. 建立连接后通过 DHCP 获取 IP

**网络管理命令**：

```bash
# 查看接口状态
ip link show
ip addr show

# 无线网络管理(iwd)
iwctl station wlan0 scan
iwctl station wlan0 connect "SSID"

# 网络服务状态
systemctl status systemd-networkd iwd

# DNS 解析测试
resolvectl query example.com
resolvectl status
```

### 6.3 IPv4 / IPv6 双栈配置

现代网络正在往 IPv6 迁移的过程中，目前仍有许多站点都只支持 IPv6，因此 IPv4+IPv6 双栈成为一
个过渡方案，systemd-networkd 提供完整的双栈支持。

**双栈特点**：

- **IPv4**：通过 DHCP 获取配置，32 位地址
- **IPv6**：通过 Router Advertisement 获取，128 位地址
- **并行工作**：两个协议栈同时运行
- **IPv6 优先**：通常有 IPv6 的会优先走 IPv6 网络，没有才走 IPv4.
  - Linux 中通过 glibc 的 `getaddrinfo()` 来实现该逻辑，可通过 `/etc/gai.conf` 调整该函数
    的地址排序算法。因为 APP 通常直接使用第一条记录发起连接，所以 `/etc/gai.conf` 通常能直
    接决定系统中是 IPv6 优先还是 IPv4 优先。

**双栈验证**：

```bash
# 查看 IPv4 配置
ip -4 addr show
ip -4 route

# 查看 IPv6 配置
ip -6 addr show
ping -6 2001:4860:4860::8888

# DNS 双栈测试
nslookup -type=A google.com
nslookup -type=AAAA google.com
```

### 6.4 网络故障排查

**连接问题诊断流程**：

1. **硬件层面**：

```bash
# 检查接口存在
ip link show

# 查看驱动加载
dmesg | grep -i firmware
lspci | grep -i network
```

2. **链路层面**：

```bash
# 有线：检查链路状态
ethtool eth0

# 无线：扫描网络
iw dev wlan0 scan | grep SSID
```

3. **网络配置**：

```bash
# DHCP 状态
journalctl -u systemd-networkd

# IP 配置检查
ip addr show dev eth0

# 路由表
ip route
```

4. **DNS 解析**：

```bash
# DNS 配置
resolvectl status
cat /etc/resolv.conf

# 解析测试
dig @8.8.8.8 example.com
nslookup example.com
```

**常见问题与解决**：

- **无法获取 IP**：检查 DHCP 服务、网线连接、无线密码
- **DNS 解析失败**：验证 DNS 服务器配置、检查 systemd-resolved 状态
- **IPv6 无连接**：确认路由器支持 IPv6、检查 `IPv6AcceptRA` 配置
- **连接不稳定**：查看信号强度、检查驱动兼容性

---

## 7. 系统服务：核心功能支持

除了基本的服务管理外，systemd 还提供了多个专门化的系统服务来支持现代 Linux 桌面的核心功
能，包括内存管理、DNS 解析和时间同步等。

> systemd 全家桶，你值得拥有（

### 7.1 内存管理：systemd-oomd

systemd-oomd 是 systemd 提供的内存不足（OOM）守护进程，用于在系统内存紧张时主动终止进程，
防止系统完全卡死。

**工作原理**：

- **内存监控**：实时监控系统内存使用情况和内存压力
- **智能选择**：基于 cgroup 层次结构和内存使用量选择要终止的进程
- **用户空间保护**：优先终止用户空间进程，保护系统关键服务
- **渐进式处理**：逐步释放内存，避免过度 kill 进程

**配置示例**：

```nix
# NixOS 配置
systemd.oomd.enable = true;

systemd.oomd.extraConfig = ''
  [OOM]
  DefaultMemoryPressureLimitSec=20s
  DefaultMemoryPressureLimit=60%
'';
```

**配置文件路径**：`/etc/systemd/oomd.conf`

**监控与调试**：

```bash
# 查看 oomd 状态
systemctl status systemd-oomd

# 内存压力信息
cat /proc/pressure/memory

# 查看 oomd 日志
journalctl -u systemd-oomd -f

# 内存使用统计
systemctl status user@$(id -u).service
```

### 7.2 DNS 解析：systemd-resolved

systemd-resolved 提供统一的 DNS 解析服务，支持 DNSSEC 验证、DNS over TLS 等现代 DNS 特性。

**主要功能**：

- **统一接口**：为系统提供单一的 DNS 解析入口
- **本地缓存**：缓存 DNS 查询结果，提高解析速度
- **DNSSEC 支持**：验证 DNS 响应的真实性
- **隐私保护**：支持 DNS over TLS(DoT), 但截止目前（2025 年）尚未支持 DNS over HTTPS(DoH).

**配置方法**：

```nix
# 启用 systemd-resolved
services.resolved.enable = true;

# 配置 DNS 服务器
networking.nameservers = [
  "8.8.8.8" "1.1.1.1"                    # IPv4
  "2001:4860:4860::8888" "2606:4700:4700::1111"  # IPv6
];

# 高级配置
services.resolved.extraConfig = ''
  [Resolve]
  DNSSEC=yes
  DNSOverTLS=yes
  Cache=yes
'';
```

**配置文件路径**：`/etc/systemd/resolved.conf`

**使用命令**：

```bash
# DNS 状态查看
resolvectl status

# DNS 查询测试
resolvectl query example.com
resolvectl query -t AAAA ipv6.google.com

# 缓存管理
resolvectl flush-caches
resolvectl statistics

# DNS 服务器状态
resolvectl dns
```

### 7.3 时间同步：systemd-timesyncd

systemd-timesyncd 是轻量级 NTP 客户端，负责保持系统时间与网络时间服务器同步。

**功能特点**：

- **轻量级设计**：相比完整 NTP 服务占用更少资源
- **自动同步**：定期与时间服务器同步
- **SNTP 协议**：使用简单网络时间协议
- **systemd 集成**：与 systemd 服务管理深度集成

**NixOS 配置**：

```nix
# 启用时间同步
services.timesyncd.enable = true;

# 配置 NTP 服务器
services.timesyncd.servers = [
  "pool.ntp.org"
  "time.google.com"
  "ntp.aliyun.com"
];
```

**配置文件路径**：`/etc/systemd/timesyncd.conf`

**时间同步管理**：

```bash
# 时间状态查看
timedatectl status
timedatectl timesync-status

# 手动控制
timedatectl set-ntp true   # 启用 NTP
timedatectl set-timezone Asia/Shanghai

# 查看同步日志
journalctl -u systemd-timesyncd -f

# 时间精度检查
chronyc tracking  # 如果安装了 chrony
```

---

## 8. 多媒体处理：音频与视频

现代 Linux 桌面使用 PipeWire 统一处理音频、视频和屏幕共享，取代了传统的 PulseAudio 和
JACK。PipeWire 提供了更低的延迟、更好的硬件兼容性，以及统一的媒体处理框架。

### 8.1 PipeWire 架构概览

PipeWire 作为媒体服务器的核心，连接应用程序和硬件设备，提供音频混合、视频处理和路由功能。

**核心组件**：

- **pipewire**：核心守护进程，管理媒体流图
- **wireplumber**：会话管理器，处理设备连接和路由策略
- **pipewire-pulse**：PulseAudio 兼容层
- **pipewire-jack**：JACK 专业音频兼容层
- **pipewire-alsa**：ALSA 兼容层

**技术特点**：

- **统一架构**：同时处理音频、视频、MIDI
- **低延迟**：相比 PulseAudio 显著降低音频延迟
- **硬件兼容**：支持专业音频设备和消费级硬件
- **安全隔离**：通过权限控制保护媒体数据

**NixOS 配置**：

```nix
services.pipewire = {
  enable = true;
  alsa.enable = true;      # ALSA 兼容
  pulse.enable = true;     # PulseAudio 兼容
  jack.enable = true;      # JACK 兼容
};

services.pipewire.wireplumber.enable = true;

# 禁用 PulseAudio 避免冲突
hardware.pulseaudio.enable = false;
```

**配置文件路径**：

- `/etc/pipewire/pipewire.conf`：主配置文件
- `/etc/pipewire/pipewire-pulse.conf`：PulseAudio 兼容配置
- `/etc/wireplumber/`：WirePlumber 会话管理器配置

### 8.2 音频处理流程

**应用播放音频的典型流程**：

1. **API 连接**：应用通过 ALSA / PulseAudio / JACK API 连接到 PipeWire
2. **流创建**：在 PipeWire 图中创建音频流节点
3. **路由决策**：WirePlumber 根据策略路由到输出设备
4. **音频处理**：混合多个应用流，执行格式转换、音量调节、调整音频效果
5. **硬件输出**：通过 ALSA 驱动将 PCM 数据发送给声卡 DAC，最终输出模拟音频输出

**音频节点管理**：

```bash
# 查看音频设备
pw-cli list-objects | grep -E "(Audio|Sink|Source)"

# 实时监控音频流
pw-top

# 图形界面管理
pavucontrol

# 查看 ALSA 设备
aplay -l
arecord -l
```

**音频路由控制**：

```bash
# 设置默认输出设备
pactl set-default-sink alsa_output.pci-0000_00_1f.3.analog-stereo

# 应用音量控制
pactl list sink-inputs
pactl set-sink-input-volume 123 50%

# 创建自定义连接
pw-cli create-link <source-node> <sink-node>
```

### 8.3 视频与屏幕共享

在 wayland 环境中，屏幕共享功能是通过 PipeWire 的 screen-capture 协议实现的。这与 X11 有很
大的不同，后者是通过其自身的扩展（如 X11R6 的 XFIXES 扩展）实现的。

目前主流的 OBS、Discord、Zoom 等应用都已经支持了 wayland 下的 screen-capture 协议。

**摄像头管理**：

```bash
# 查看视频设备
pw-cli list-objects | grep -i video
v4l2-ctl --list-devices

# 摄像头格式查询
v4l2-ctl --device=/dev/video0 --list-formats

# 权限检查
ls -l /dev/video*
groups $USER
```

**屏幕共享配置**：

```bash
# Wayland 环境检查
echo $WAYLAND_DISPLAY

# 设置桌面环境标识
export XDG_CURRENT_DESKTOP=sway

# 检查 PipeWire 服务
systemctl --user status pipewire-session-manager
```

### 8.4 故障排查与优化

**音频设备识别问题**：

1. **检查设备存在**：

```bash
aplay -l
arecord -l
```

2. **验证 PipeWire 运行**：

```bash
systemctl --user status pipewire wireplumber
journalctl --user -u pipewire -f
```

3. **权限检查**：

```bash
ls -l /dev/snd/
groups $USER  # 确认在 audio 组
```

**音频延迟优化**：

```bash
# 编辑用户配置
vim ~/.config/pipewire/pipewire.conf

# 低延迟配置示例
context.properties = {
    default.clock.rate = 48000
    default.clock.quantum = 32
    default.clock.min-quantum = 32
    default.clock.max-quantum = 32
}
```

**屏幕共享问题解决**：

1. **Wayland 协议支持**：确认合成器支持 screen-capture 协议
2. **环境变量设置**：正确设置 `XDG_CURRENT_DESKTOP`
3. **权限配置**：检查摄像头和屏幕录制权限
4. **应用兼容性**：部分应用需要特定版本的 PipeWire

---

## 9. 中文支持：字体渲染与输入法

中文支持是中文用户桌面体验的核心组成部分，包括字体渲染配置和中文输入法设置。本章节将详细介
绍如何在 Linux 桌面环境中正确配置中文字体和输入法，解决常见的显示和输入问题。

### 9.1 字体渲染与配置

字体渲染是桌面应用显示质量的关键因素，特别是对于中文用户，CJK（中日韩）字体的正确配置直接
影响阅读体验。Linux 桌面通过 fontconfig 系统统一管理字体配置，解决字体匹配、渲染和显示问
题。

#### 9.1.1 fontconfig 架构概览

fontconfig 是 Linux 桌面系统的字体配置框架，负责：

- **字体发现**：扫描系统字体目录，建立字体索引
- **字体匹配**：根据应用请求的字体特征（族名、样式、语言等）选择最合适的字体
- **字体渲染**：配置字体渲染参数（抗锯齿、子像素渲染、提示等）
- **字体替换**：当请求的字体不存在时，提供合适的替代字体

**核心组件**：

- **fc-cache**：字体缓存生成工具
- **fc-list**：字体列表查询工具
- **fc-match**：字体匹配测试工具
- **配置文件**：XML 格式的字体配置规则

**配置文件层次**：

```bash
# 系统级配置（优先级从高到低）
/etc/fonts/fonts.conf                    # 主配置文件
/etc/fonts/conf.d/                       # 配置片段目录

# 用户级配置
~/.config/fontconfig/fonts.conf          # 用户主配置
~/.config/fontconfig/conf.d/             # 用户配置片段
```

#### 9.1.2 CJK 字体配置基础

**常见 CJK 字体族**：

| 字体族               | 特点                                  | 适用场景           |
| -------------------- | ------------------------------------- | ------------------ |
| **Source Han Sans**  | Adobe 开源，专业设计                  | 现代应用，网页显示 |
| **Source Han Serif** | Adobe 开源，衬线字体                  | 设计软件，印刷     |
| **Source Han Mono**  | 思源等宽字体                          | 编程，代码显示     |
| **Noto Sans CJK**    | Google 开源，与 Source Han 为同一字体 | 系统界面，兼容性   |
| **WenQuanYi**        | 文泉驿，轻量级                        | 系统界面，终端     |

> **说明**：Source Han 系列和 Noto CJK 系列实际上是同一套字体，只是分别由 Adobe 和 Google
> 以自己的品牌名发布。

以及一些新兴的开源字体：

| 字体族                 | 特点           | 适用场景       |
| ---------------------- | -------------- | -------------- |
| **LXGW WenKai Screen** | 霞鹜文楷屏幕版 | 屏幕阅读，文档 |
| **Maple Mono NF CN**   | 中英文等宽字体 | 编程，终端     |

**NixOS 字体配置示例**：

```nix
# configuration.nix
fonts = {
  # 禁用默认字体包，使用自定义配置
  enableDefaultPackages = false;
  fontDir.enable = true;

  # 安装常用 CJK 字体和图标字体
  packages = with pkgs; [
    # 图标字体
    material-design-icons
    font-awesome
    nerd-fonts.symbols-only
    nerd-fonts.jetbrains-mono

    # Noto 是 Google 开发的开源字体家族
    # 名字的含义是「没有豆腐」（no tofu），因为缺字时显示的方框或者方框被叫作 tofu
    #
    # Noto 系列字族只支持西文，命名规则是 Noto + Sans 或 Serif + 文字名称。
    noto-fonts # 大部分文字的常见样式，不包含汉字
    noto-fonts-color-emoji # 彩色的表情符号字体
    # Noto CJK 为「思源」系列汉字字体，由 Adobe + Google 共同开发
    # Google 以 Noto Sans/Serif CJK SC/TC/HK/JP/KR 的名称发布该系列字体。
    # 这俩跟 noto-fonts-cjk-sans/serif 实际为同一字体，只是分别由 Adobe/Google 以自己的品牌名发布
    # noto-fonts-cjk-sans # 思源黑体
    # noto-fonts-cjk-serif # 思源宋体

    # Adobe 以 Source Han Sans/Serif 的名称发布此系列字体
    source-sans # 无衬线字体，不含汉字。字族名叫 Source Sans 3，以及带字重的变体（VF）
    source-serif # 衬线字体，不含汉字。字族名叫 Source Serif 4，以及带字重的变体
    # Source Hans 系列汉字字体由 Adobe + Google 共同开发
    source-han-sans # 思源黑体
    source-han-serif # 思源宋体
    source-han-mono # 思源等宽
  ];

  # 字体渲染配置
  fontconfig = {
    enable = true;
    antialias = true;        # 启用抗锯齿
    hinting.enable = false;  # 高分辨率下禁用字体微调
    subpixel.rgba = "rgb";   # IPS 屏幕使用 RGB 子像素排列

    # 默认字体族配置
    defaultFonts = {
      serif = [
        "Source Serif 4"        # 西文衬线字体
        "Source Han Serif SC"   # 中文宋体
        "Source Han Serif TC"   # 繁体宋体
      ];
      sansSerif = [
        "Source Sans 3"         # 西文无衬线字体
        "Source Han Sans SC"    # 中文黑体
        "Source Han Sans TC"    # 繁体黑体
      ];
      monospace = [
        "Maple Mono NF CN"      # 中英文等宽字体
        "Source Han Mono SC"    # 中文等宽
        "JetBrainsMono Nerd Font"  # 西文等宽
      ];
      emoji = [ "Noto Color Emoji" ];
    };
  };
};
```

> **重要说明**：Source Han 系列（Adobe 发布）和 Noto CJK 系列（Google 发布）实际上是同一套
> 字体，只是分别由 Adobe 和 Google 以自己的品牌名发布。在 NixOS 中，`source-han-sans` 和
> `noto-fonts-cjk-sans` 指向的是同一套字体文件。

#### 9.1.3 常见 CJK 字体问题与解决方案

**问题 1：中文字符显示为方块或问号**

**原因**：系统缺少中文字体或字体匹配规则不正确

**排查步骤**：

```bash
# 1. 检查已安装的 CJK 字体
fc-list :lang=zh-cn

# 2. 测试字体匹配
fc-match "sans-serif:lang=zh-cn"
fc-match "serif:lang=zh-cn"

# 3. 查看字体详细信息
fc-list | grep -i "noto\|source\|wqy"
```

使用上面提供的示例配置通常可解决问题。

**问题 2：中文字体中夹杂日语字体**

**原因**：CJK 字体通常包含中文、日文、韩文字符，当系统缺少专门的中文字体时，会使用包含日文
字符的 CJK 字体，导致中文字符显示为日语字形。

**排查步骤**：

```bash
# 检查当前使用的字体
fc-match "sans-serif:lang=zh-cn"
fc-match "serif:lang=zh-cn"

# 查看字体包含的语言支持
fc-list :lang=zh-cn
fc-list :lang=ja
```

**解决方案**：

```nix
# configuration.nix
fonts.fontconfig = {
  enable = true;
  defaultFonts = {
    sansSerif = [
      "Source Han Sans SC"    # 简体中文优先
      "Source Han Sans TC"    # 繁体中文备选
      "Source Sans 3"         # 西文备选
    ];
    serif = [
      "Source Han Serif SC"   # 简体中文优先
      "Source Han Serif TC"   # 繁体中文备选
      "Source Serif 4"        # 西文备选
    ];
  };
};
```

#### 9.1.4 字体调试与优化工具

**字体信息查询**：

```bash
# 列出所有字体
fc-list

# 按语言过滤字体
fc-list :lang=zh-cn
fc-list :lang=en

# 查看字体详细信息
fc-list -v "Source Han Sans SC"
fc-list -v "LXGW WenKai Screen"

# 测试字体匹配
fc-match -v "sans-serif:lang=zh-cn"
fc-match -v "serif:lang=zh-cn"
fc-match -v "monospace:lang=zh-cn"
```

**字体渲染测试**：

```bash
# 临时安装字体测试工具
nix shell nixpkgs#pango

# 创建测试文本文件
echo "中文测试 Chinese Test 123" > test.txt

# 使用不同字体渲染测试
pango-view --font="Source Han Sans SC 12" test.txt
pango-view --font="LXGW WenKai Screen 12" test.txt
pango-view --font="Maple Mono NF CN 12" test.txt
```

### 9.2 中文输入法配置

现代 Linux 桌面主要使用 fcitx5 作为中文输入解决方案，它通过插件系统支持多种输入引擎，并与
图形环境深度集成。

#### 9.2.1 输入法框架架构

**核心组件**：

- **fcitx5-daemon**：主守护进程，管理输入法状态
- **输入引擎**：拼音、五笔、仓颉等具体输入法实现
- **图形前端**：负责候选词界面显示
- **配置工具**：fcitx5-configtool 提供图形化配置

**配置文件路径**：

- `~/.config/fcitx5/config`：主配置文件
- `~/.config/fcitx5/profile`：输入法引擎配置
- `~/.config/fcitx5/conf/`：各输入法引擎的详细配置

#### 9.2.2 Wayland 原生输入法流程

**Wayland text-input 协议流程**：

1. **按键捕获**：键盘事件首先到达 Wayland 合成器
2. **协议通信**：合成器通过 text-input 协议与客户端应用通信
3. **输入法服务**：fcitx5 作为 Wayland 输入法服务接收事件
4. **候选生成**：fcitx5 处理按键并生成候选词
5. **候选显示**：通过 Wayland 协议在光标位置显示候选窗口
6. **文本提交**：用户选择后通过 text-input 协议提交最终文本

text-input 协议有 v1 跟 v3 两个版本，目前（2025-09）Electron/Chrome 以及其他大部分程序框架
都已经支持了 text-input-v3. 桌面环境方面所有主流 Compositor 也都支持 text-input-v3. 所以目
前 wayland 下输入法的可用性已经很高了。

#### 9.2.3 X11 / XWayland 输入法流程

**XWayland 使用场景**：

- 尚未支持 Wayland 的旧版应用
- 需要特定 X11 功能的专业软件
- 通过应用启动脚本单独设置环境变量

**XWayland 应用输入流程**：

1. **按键捕获**：键盘事件首先进入 **Wayland 合成器**（Hyprland、KWin 等）。
2. **事件转发给 XWayland**（例如
   [xwayland-satellite](https://github.com/Supreeeme/xwayland-satellite)）
   - 如果目标是 X11 应用窗口，合成器会将事件交给 **XWayland**。
   - **XWayland 将 Wayland 输入事件转换为 X11 协议事件**（如 `KeyPress/KeyRelease`），并交
     付给目标应用。
3. **应用侧的输入法模块拦截事件**
   - X11 应用（GTK/Qt 程序）内部加载了 **fcitx5-gtk / fcitx5-qt 插件**（通常根据环境变量加
     载，后面会介绍这些环境变量）。
   - 这些插件拦截来自 XWayland 的键盘事件，并通过 **D-Bus** 将事件上报给 **fcitx5**。
   - 此时应用相当于是「把键盘输入交给 fcitx5 代管」。
4. **fcitx5 处理输入逻辑**
   - fcitx5 收到键盘序列后，进入输入法逻辑：拼音解析、候选词生成。
   - fcitx5 控制候选窗口的显示位置（通常跟随输入光标），候选窗口本身可能是 X11 窗口（由
     fcitx5 自己创建，并通过 XWayland 显示）。
5. **输入结果返回应用**
   - 当用户选定候选词后，fcitx5 通过 **D-Bus 调用 IM 插件接口**直接把确认后的字符串传给应
     用。
   - 应用的 IM 插件收到字符串后，调用应用内的「输入上下文 API」插入文本。
   - 在应用看来，它就像直接得到了「输入了一串中文」的事件。

**XWayland 环境变量设置**：

```bash
# GTK 应用使用 fcitx（通过 GTK IM 模块）
export GTK_IM_MODULE=fcitx

# Qt 应用使用 fcitx（通过 Qt IM 模块）
export QT_IM_MODULE=fcitx

# X11 应用使用 fcitx（通过 XIM 协议）
export XMODIFIERS=@im=fcitx
```

**输入法机制说明**：

GTK IM 模块、Qt IM 模块以及 XIM 协议，都是 X11 下的东西，在 wayland 下只需要 text-input 协
议即可，不需要这些幺蛾子。

#### 9.2.4 混合环境管理策略

**推荐配置策略**：

1. **默认 Wayland 优先**：

   - 让现代应用使用原生 Wayland text-input 协议

2. **按需 XWayland**：

   - 使用 `GDK_BACKEND=x11` 强制特定应用使用 XWayland
   - 为特定应用创建启动脚本设置 IM_MODULE 相关环境变量

3. **应用启动脚本示例**：

```bash
#!/bin/bash
# 强制特定应用使用 XWayland
export GTK_IM_MODULE=fcitx  # 使用 GTK IM 模块
export QT_IM_MODULE=fcitx   # 使用 Qt IM 模块
export GDK_BACKEND=x11      # 强制使用 X11 后端
your-application
```

#### 9.2.5 故障排查与优化

**输入法无响应问题**：

1. **进程状态检查**：

   ```bash
   ps aux | grep fcitx5
   systemctl --user status fcitx5
   ```

2. **环境变量验证**（仅 xwayland 场景）：

   ```bash
   echo $GTK_IM_MODULE $QT_IM_MODULE $XMODIFIERS
   echo $XDG_RUNTIME_DIR $DBUS_SESSION_BUS_ADDRESS
   ```

3. **D-Bus 通信检查**：

   ```bash
   busctl --user tree org.fcitx.Fcitx5
   dbus-monitor --session "interface='org.fcitx.Fcitx5'"
   ```

4. **诊断工具使用**：

   ```bash
   fcitx5-diagnose
   fcitx5-configtool
   ```

**候选框显示问题**：

1. **Wayland 原生应用排查**：

   ```bash
   # 检查 Wayland 环境
   echo $WAYLAND_DISPLAY $XDG_RUNTIME_DIR

   # 检查 text-input 协议支持
   wayland-info | grep text-input

   # 查看合成器日志中 text-input 相关错误
   journalctl --user -u fcitx5
   ```

2. **XWayland 应用排查**：

   ```bash
   # 检查 XWayland 环境变量
   echo $GTK_IM_MODULE $QT_IM_MODULE $XMODIFIERS

   # 检查 XWayland 连接
   echo $DISPLAY

   # 验证 XIM 连接
   xdpyinfo | grep -i input
   ```

3. **权限和会话检查**：

   ```bash
   # 确认 fcitx5 在正确的用户会话中运行
   loginctl show-session $(loginctl | grep $USER | awk '{print $1}')

   # 检查 D-Bus 会话
   echo $DBUS_SESSION_BUS_ADDRESS
   ```

4. **应用兼容性**：

   - **Wayland 应用**：部分应用需要重新启动才能识别输入法
   - **XWayland 应用**：需要正确设置 XMODIFIERS 环境变量
   - **混合环境**：某些应用可能在不同环境下表现不同

**性能优化**：

```bash
# 调整 fcitx5 配置
vim ~/.config/fcitx5/profile

# 禁用不需要的输入引擎
# 减少候选词数量提高响应速度

# 云拼音配置
vim ~/.config/fcitx5/conf/cloudpinyin.conf
```

**特殊场景处理**：

1. **多显示器环境**：

   - **Wayland**：候选框通常能正确跟随光标位置
   - **XWayland**：候选框可能在错误屏幕显示，需要调整 X11 配置

2. **高分屏适配**：

   - **Wayland**：自动适配系统缩放比例
   - **XWayland**：可能需要手动设置 `GDK_SCALE` 或 `QT_SCALE_FACTOR`

3. **游戏和全屏应用**：

   - **Wayland**：部分游戏可能需要 `gamescope` 等工具
   - **XWayland**：传统全屏游戏通常工作正常

4. **终端应用**：
   - **Wayland 终端**：需要终端模拟器支持 text-input 协议
   - **XWayland 终端**：使用 X11 的 XIM 协议或 GTK/Qt IM 模块

---

## 10. 应用程序：从启动到交互

GUI 应用程序是用户与 Linux 桌面交互的主要方式。在 Wayland 环境下，应用通过标准化的协议与合
成器通信，实现窗口管理、输入处理和图形渲染。

### 10.1 应用架构概览

现代 Linux 桌面应用采用分层架构，从底层的图形驱动到高层的用户界面，各层协同工作提供完整的
用户体验。

**架构层次**：

- **硬件层**：GPU 和显示设备
- **驱动层**：Mesa 图形驱动和内核 DRM
- **系统层**：Wayland 协议和合成器
- **工具包层**：GTK、Qt 等图形界面库
- **应用层**：具体的桌面应用程序

**Wayland 客户端模型**：

- **客户端-服务器架构**：应用作为客户端，合成器作为服务器
- **Unix 域套接字**：通过 `$XDG_RUNTIME_DIR/wayland-0` 进行通信
- **协议扩展**：支持 xdg-shell、text-input 等扩展协议
- **安全隔离**：应用只能访问自己的窗口和输入事件

**图形渲染管线**：

1. 应用创建 OpenGL/Vulkan 渲染上下文
2. 在 GPU 上执行渲染命令
3. 将渲染结果提交给合成器
4. 合成器组合多个应用的输出
5. 通过 DRM/KMS 显示到屏幕

### 10.2 应用启动流程

**标准启动过程**：

1. **环境准备**：

   - 设置 `WAYLAND_DISPLAY` 和 `XDG_RUNTIME_DIR`
   - 加载图形工具包库（GTK/Qt）
   - 初始化 Wayland 连接

2. **窗口创建**：

   - 创建 Wayland 表面（surface）
   - 设置窗口属性和装饰
   - 注册事件监听器

3. **渲染初始化**：

   - 创建 EGL 上下文
   - 加载 Mesa 驱动
   - 配置图形缓冲区

4. **内容绘制**：

   - 应用调用 OpenGL/Vulkan API 绘制界面内容
   - Mesa 将 API 调用转换为 GPU 指令
   - 在 GPU 上执行渲染，生成帧缓冲数据
   - 应用将渲染完成的缓冲区提交给合成器

5. **合成与展示**：
   - 合成器接收缓冲区后进行最终合成和显示
   - 合成器将多个应用的缓冲区组合成最终帧
   - 通过 DRM/KMS 将最终帧提交到显示设备

**调试启动问题**：

```bash
# 查看 Wayland 环境
echo $WAYLAND_DISPLAY $XDG_RUNTIME_DIR

# 检查应用日志
journalctl --user -u <application>.service

# Wayland 调试变量
export WAYLAND_DEBUG=1
export MESA_DEBUG=1

# 跟踪系统调用
strace -f -e trace=network,ipc <application>
```

### 10.3 图形驱动与兼容性

**驱动信息查询**：

```bash
# OpenGL 信息
glxinfo | grep "OpenGL renderer"

# Vulkan 信息
vulkaninfo | grep "GPU id"

# DRM 设备
ls -la /dev/dri/

# 内核驱动
lspci -k | grep -A 3 -i vga
```

### 10.4 工具包支持

**GTK 应用**：

- GTK3/4 原生支持 Wayland
- 自动检测运行环境
- 可通过 `GDK_BACKEND` 强制指定后端

```bash
# 强制使用 Wayland
GDK_BACKEND=wayland gtk-application

# 强制使用 X11（通过 Xwayland）
GDK_BACKEND=x11 gtk-application
```

**Qt 应用**：

- Qt5/6 支持 Wayland
- 需要安装 Wayland 平台插件
- 自动选择最佳后端

```bash
# 查看 Qt 平台插件（NixOS）
ls /run/current-system/sw/lib/qt*/plugins/platforms/
# 其他发行版
ls /usr/lib/qt*/plugins/platforms/

# Qt 调试信息
export QT_LOGGING_RULES="qt.qpa.*=true"
```

**SDL 应用**：

- SDL2 内置 Wayland 支持
- 主要用于游戏和多媒体应用
- 自动适配运行环境

**图形渲染问题排查**：

当遇到应用闪退、渲染异常等问题时，可以尝试切换不同的渲染后端：

```bash
# GTK 应用渲染器选择
export GSK_RENDERER=vulkan    # 使用 Vulkan 渲染
export GSK_RENDERER=opengl    # 使用 OpenGL 渲染
export GSK_RENDERER=cairo     # 使用软件渲染

# Qt 应用渲染器选择
export QT_OPENGL=desktop      # 使用桌面 OpenGL
export QT_OPENGL=software     # 使用软件渲染
export QT_OPENGL=angle        # 使用 ANGLE（Windows 兼容层）

# Mesa 驱动选择
export MESA_GL_VERSION_OVERRIDE=4.5
export MESA_GLSL_VERSION_OVERRIDE=450

# 调试信息
export MESA_DEBUG=1           # 启用 Mesa 调试信息
export LIBGL_DEBUG=verbose    # 启用 OpenGL 调试信息
```

**常见问题与解决方案**：

- **应用闪退**：尝试 `GSK_RENDERER=cairo` 或 `QT_OPENGL=software`
- **渲染异常**：检查 GPU 驱动，尝试不同的 `GSK_RENDERER` 值
- **性能问题**：优先使用 `vulkan` 或 `opengl` 硬件加速
- **兼容性问题**：某些老旧应用可能需要软件渲染模式

### 10.5 故障排查与调试

**应用崩溃诊断**：

1. **核心转储分析**：

```bash
# 查看核心转储
coredumpctl list
coredumpctl info <pid>

# 调试核心文件
coredumpctl debug <pid>
```

2. **GPU 问题诊断**：

```bash
# 检查 GPU 重置
dmesg | grep -i "gpu hang\|reset"

# Mesa 调试信息
export MESA_DEBUG=1
export LIBGL_DEBUG=verbose
```

3. **Wayland 协议错误**：

```bash
# Wayland 调试输出
export WAYLAND_DEBUG=1

# 合成器日志
journalctl --user -u <compositor> -f
```

**性能问题分析**：

```bash
# GPU 使用率
nvidia-smi  # NVIDIA
radeontop   # AMD

# CPU 使用率分析
perf top -p <pid>

# 内存使用
smem -p | grep <application>

# 帧率监控
export __GL_SHOW_GRAPHICS_OSD=1  # NVIDIA
```

**兼容性问题**：

- **Xwayland 问题**：部分 X11 应用在 Xwayland 下运行异常
- **Wayland 协议缺失**：某些功能需要特定的 Wayland 扩展
- **驱动兼容性**：GPU 驱动可能不完全支持某些 Wayland 特性

**解决方案**：

- 更新 Mesa 和 GPU 驱动
- 检查合成器对必要 Wayland 扩展的支持
- 对于顽固问题，可临时使用 X11 会话

---

## 11. 系统关机：优雅的生命周期结束

### 11.1 关机流程概览

systemd 管理的关机过程分为四个主要阶段，每个阶段都有明确的目标和顺序，确保数据完整性和系统
稳定性。

**关机阶段**：

1. **用户会话清理阶段**（约 1-5 秒）：

   - 通知所有用户会话即将关机
   - 优雅关闭用户应用程序
   - 回收用户设备权限

2. **系统服务停止阶段**（约 2-10 秒）：

   - 按依赖关系逆向停止系统服务
   - 卸载文件系统（除根文件系统外）
   - 网络服务断开连接

3. **内核资源释放阶段**（约 1-3 秒）：

   - 同步所有文件系统到磁盘
   - 卸载根文件系统为只读
   - 终止所有剩余进程

4. **硬件关机阶段**（约 1-2 秒）：

   - 通过 ACPI 发送关机信号
   - 固件接管系统控制权
   - 所有硬件设备断电

### 11.2 用户会话清理

当用户发起关机时，systemd 首先处理用户会话的清理工作，确保用户数据得到妥善保存。

**会话清理流程**：

```bash
# systemd 发送关机信号
systemctl start shutdown.target

# 用户会话收到终止信号
loginctl terminate-session <session_id>

# 用户服务停止
systemctl --user stop graphical-session.target
```

**关键操作**：

- **会话通知**：通过 D-Bus 向桌面环境发送关机信号
- **应用关闭**：等待应用保存未保存的数据
- **权限回收**：logind 回收分配给用户的设备访问权限
- **服务停止**：用户 systemd 实例停止所有用户服务

**监控用户会话清理**：

```bash
# 查看会话状态变化
journalctl -b | grep -E "(session|Session)"

# 用户服务停止日志
journalctl --user -b | grep -E "(Stopping|Stopped)"

# 设备权限回收
journalctl -u systemd-logind -b | grep -i "device"
```

### 11.3 系统服务停止

用户会话清理完成后，systemd 开始按依赖关系的逆向顺序停止系统服务。

**服务停止顺序**：

- **图形服务**：合成器、显示管理器
- **网络服务**：网络管理器、DNS 解析器
- **存储服务**：磁盘管理、LVM
- **基础服务**：日志、设备管理

**关键服务处理**：

```bash
# 查看关机时的服务停止顺序
systemd-analyze critical-chain shutdown.target

# 监控服务停止状态
watch -n 1 'systemctl list-units --state=deactivating'

# 检查服务停止日志
journalctl -b -1 | grep -E "(Stopping|Stopped)" | tail -20
```

**文件系统卸载**：

```bash
# 查看挂载点卸载情况
mount | grep -v "on / type"

# 文件系统同步状态
sync
echo 3 > /proc/sys/vm/drop_caches

# 检查卸载错误
journalctl -b -1 | grep -i "unmount\|busy"
```

### 11.4 内核资源释放

当所有用户空间服务停止后，systemd 执行最终的系统清理：

**文件系统操作**：

- 调用 `sync()` 同步所有已挂载文件系统的数据到磁盘
- 按照逆向挂载顺序卸载所有挂载点
- 卸载外接硬盘分区等外部存储设备

**进程管理**：

- 向所有剩余进程发送 SIGTERM，给它们最后清理机会
- 等待超时后，对顽固进程发送 SIGKILL 强制终止
- 清理僵尸进程和孤儿进程

**Watchdog 监控**：

- systemd 的看门狗机制监控服务关闭进度
- 如果服务停止超过 `TimeoutStopSec`，强制终止服务
- 防止系统在关机过程中无限挂起

**资源清理**：

- GPU 驱动重置显卡状态，释放 VRAM
- 网络设备完全断电
- 音频设备硬件重置

### 11.5 硬件关机

当所有用户空间和内核资源处理完毕后，系统进入硬件关机：

**ACPI 操作**：

- systemd 通过 ACPI 向固件发出关机指令
- 进入 ACPI S5 状态，告诉固件关闭电源

**固件接管**：

- BIOS/UEFI 接管系统控制权
- 执行电源关断，所有设备（CPU、内存、GPU、外部设备）断电
- 固件执行最后的清理工作

**强制关机保护**：

- 如果系统未能正常关机，硬件看门狗可能强制切断电源
- 用户长按电源键也会触发强制关机

此时机器完全断电，关机过程结束。下次开机将重新开始完整的启动周期。

### 11.6 关机问题排查

**常见关机问题**：

1. **服务停止超时**：

```bash
# 查看超时服务
journalctl -b -1 | grep -i "timeout"

# 检查特定服务配置
systemctl cat <service> | grep Timeout
```

2. **文件系统卸载失败**：

```bash
# 查找占用文件系统的进程
lsof | grep <mountpoint>

# 检查文件系统状态
fsck -n /dev/<device>
```

3. **设备繁忙**：

```bash
# 检查设备占用
lsof | grep /dev/<device>

# 查看块设备状态
lsblk -f
```

**强制关机处理**：

当正常关机失败时，可以使用以下方法：

```bash
# 安全强制关机
systemctl poweroff -f

# 紧急关机（立即执行）
systemctl poweroff -ff

# 内核强制重启
echo b > /proc/sysrq-trigger

# 内核强制关机
echo o > /proc/sysrq-trigger
```

---

## 12. 实战案例：综合故障排查

在实际使用 Linux 桌面系统时，往往会遇到多层次、多组件交织的故障。通过系统化的排查方法，可
以快速定位问题并制定解决方案。本章通过几个典型案例，讲解如何综合使用日志、调试工具和系统命
令进行故障排查。

### 12.1 案例一：桌面环境无法启动

**现象**：用户登录后，屏幕闪烁后回到登录界面，桌面无法显示。

**排查步骤**：

1. **检查显示管理器状态**：

```bash
systemctl status display-manager
journalctl -u display-manager -b
```

2. **确认用户会话**：

```bash
loginctl list-sessions
loginctl show-session <session_id>
```

3. **检查合成器日志**（Wayland 示例）：

```bash
journalctl --user -u sway -f
export WAYLAND_DEBUG=1
```

4. **检查 GPU 驱动状态**：

```bash
lspci -k | grep -A 3 -i vga
dmesg | grep -i drm
```

**常见原因**：

- 驱动不匹配或未加载
- 合成器启动失败
- 用户环境变量设置错误

**解决方案**：

- 更新或切换 GPU 驱动
- 使用默认配置启动合成器
- 检查 `$XDG_RUNTIME_DIR` 和 `$WAYLAND_DISPLAY` 是否正确

---

### 12.2 案例二：应用程序崩溃或无响应

**现象**：某些应用程序启动后立即崩溃，或运行中无响应。

**排查步骤**：

1. **查看用户服务日志**：

```bash
journalctl --user -b -u <application>.service
```

2. **启用应用调试信息**：

```bash
export GDK_DEBUG=all    # GTK 应用
export QT_LOGGING_RULES="qt.qpa.*=true"  # Qt 应用
export WAYLAND_DEBUG=1
```

3. **分析核心转储**：

```bash
coredumpctl list
coredumpctl info <pid>
coredumpctl debug <pid>
```

4. **检查依赖库版本**：

```bash
ldd $(which <application>)
```

**常见原因**：

- 缺少或版本不匹配的库
- Wayland/Xwayland 支持不完整
- GPU 驱动异常

**解决方案**：

- 安装或升级依赖库
- 强制应用使用 X11 或 Wayland 后端
- 检查驱动更新或使用回滚版本

---

### 12.3 案例三：系统关机或重启异常

**现象**：系统关机卡住，服务停止超时，最终需要强制关机。

**排查步骤**：

1. **查看关机日志**：

```bash
journalctl -b -1 -e
systemd-analyze blame shutdown.target
```

2. **检查服务停止状态**：

```bash
systemctl list-units --state=deactivating
journalctl -b -1 | grep -E "(Stopping|Stopped)"
```

3. **文件系统状态**：

```bash
mount | grep -v "on / type"
lsof | grep <mountpoint>
```

4. **硬件设备状态**：

```bash
lsblk -f
dmesg | grep -i "error\|fail\|timeout"
```

**常见原因**：

- 某些服务或进程未能及时停止
- 文件系统被占用或损坏
- 设备驱动异常导致无法卸载

**解决方案**：

- 强制停止顽固服务：

```bash
systemctl stop <service> -i
```

- 检查并修复文件系统：

```bash
fsck -n /dev/<device>
```

- 临时使用强制关机：

```bash
systemctl poweroff -ff
```

---

### 12.4 案例四：网络异常导致应用无法访问

**现象**：应用启动正常，但无法连接网络资源。

**排查步骤**：

1. **检查网络接口和状态**：

```bash
ip addr
ip route
nmcli device status
```

2. **测试 DNS 和连通性**：

```bash
ping 8.8.8.8
dig www.example.com
```

3. **查看网络服务日志**：

```bash
journalctl -u NetworkManager -b
```

4. **检查防火墙和权限**：

```bash
sudo iptables -L -v -n
sudo nft list ruleset
```

**常见原因**：

- DHCP 或静态 IP 配置错误
- DNS 配置异常
- 防火墙阻塞访问

**解决方案**：

- 修复网络配置
- 检查防火墙规则
- 重启网络服务

---

### 12.5 综合排查方法

面对复杂问题，单靠经验可能难以定位故障，推荐遵循以下方法：

1. **日志为先**：系统日志、用户服务日志、应用日志是最直接的线索
2. **逐层排查**：从硬件 → 驱动 → 系统服务 → 用户会话 → 应用
3. **最小复现**：关闭非必要服务和应用，简化环境重现问题
4. **工具辅助**：`journalctl`、`strace`、`coredumpctl`、`lsof`、`perf` 等
5. **文档与社区**：查阅官方文档和社区经验，快速定位常见故障

通过上述方法，可以系统化地分析并解决大多数 Linux 桌面问题，提高系统稳定性和用户体验。

---

## 总结

本文从系统启动到关机，全面解析了现代 Linux 桌面系统的各个组件和工作原理。通过理解底层机
制，我们能够：

1. **快速定位问题**：根据症状迅速缩小排查范围
2. **优化系统性能**：通过合理配置各组件，获得更流畅的体验
3. **深入理解 Linux**：建立完整的桌面系统知识体系
4. **解决复杂问题**：面对棘手系统问题时，能够有条不紊地分析和解决

Linux 桌面系统虽复杂，但每个组件都有明确作用和逻辑关系。掌握这些知识不仅能提升使用效率，还
能在遇到问题时从容应对，真正做到「庖丁解牛，游刃有余」。

希望这份“解牛图”能成为你探索 Linux 桌面世界的有力工具，让你的 Linux 之旅更加顺畅与愉快。

---

_本文基于 NixOS 和 Wayland 技术栈撰写，但原理和方法同样适用于其他 Linux 发行版和桌面环境。
由于技术发展迅速，建议结合实际环境和最新文档参考。_

## 参考

- [Understanding Linux Desktop Components: Display Servers, Compositors, Window Managers, and Desktop Environments](https://thamizhelango.medium.com/understanding-linux-desktop-components-display-servers-compositors-window-managers-and-desktop-e07c9c45dcce)
