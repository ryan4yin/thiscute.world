---
title: "Linux 桌面系统解析（一）"
subtitle: "概览"
description: ""
date: 2025-09-09T20:17:33+08:00
lastmod: 2025-09-09T20:17:33+08:00
draft: true

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

技术栈假定为：UEFI + systemd-boot + systemd + Wayland + PipeWire + iwd/NetworkManager +
fcitx5.

---

## 1. 引导与 initramfs

### 1.1 UEFI 与启动管理器

现代系统普遍使用 **UEFI 固件** 代替 BIOS。UEFI 初始化硬件后，从 EFI System Partition (ESP)
中加载启动管理器。NixOS 默认使用 **grub**，不过在启用 secure boot 时目前只能改用
**systemd-boot**，它读取 `/boot/loader/loader.conf` 和 `/boot/loader/entries/*.conf`，列出
可用内核并加载对应的 `vmlinuz` 与 `initrd`。

**NixOS 配置示例**：

```nix
boot.loader.systemd-boot.enable = true;
boot.loader.efi.canTouchEfiVariables = true;
```

**常用命令**：

- `efibootmgr -v`：查看/修改固件启动顺序。
- `bootctl status`：检查 systemd-boot 安装与 ESP 状态。
- `bootctl list`：列出启动条目。

---

### 1.2 内核启动

当 systemd-boot 把控制权交给内核后，内核会：

- 探测 CPU、内存、PCI、USB、ACPI 等基础硬件；
- 加载内置或 initramfs 中的关键驱动（如存储、NVMe、LUKS 加密模块）；
- 挂载 initramfs 并执行其中的 `/init`。

**观察方法**：

```bash
# 查看内核早期日志
dmesg --level=err,warn,info | less

# 查看本次启动的完整日志（内核 + 用户态）
journalctl -b
```

---

### 1.3 initramfs 工作

initramfs 提供一个最小用户空间，用于：

1. 识别并挂载根分区（可能包含 LUKS 解密 / LVM 激活）；
2. 加载额外驱动；
3. 执行 `switch_root` 交给真正的 rootfs，再启动 systemd（PID 1）。

若无法进入 rootfs，常见原因包括：

- `root=` 内核参数错误；
- 必要驱动未打入 initrd；
- 磁盘加密密钥错误。

**常见故障（initramfs 阶段）**：

- **找不到根分区**：导致 kernel panic 或重新进入 initramfs 主动 shell。原因可能是 UUID 不
  匹配、LVM 未激活、加密密钥错误。检查 `cat /proc/cmdline` 的 `root=...` 参数，确保与
  `blkid` 的输出一致。
- **缺少驱动模块**：例如 NVMe/SATA 驱动未打入 initrd，导致无法识别磁盘。解决方法是在 NixOS
  的配置里确保 `boot.initrd.luks.devices` / `boot.initrd.network` /
  `boot.initrd.kernelModules` 包含所需模块，然后 `nixos-rebuild boot` 重建 initrd。

**排查步骤示例**：

1. 在故障机器上按住 `(e)`（或借助引导菜单）编辑内核 cmdline，添加 `init=/bin/sh` 或
   `break=mount` 进入 initramfs shell。
2. 在 shell 中运行 `lsblk`, `blkid`, `cat /etc/fstab`（如果可见）确认设备。
3. 查看 `dmesg` 中关于磁盘或 LVM 的错误。

**NixOS 特殊点**：

- initramfs 在 `nixos-rebuild` 过程中自动生成；
- 可通过 `boot.initrd.kernelModules = [ "nvme" "dm_mod" ];` 指定额外模块；
- 修改配置后需通过 `nixos-rebuild switch` 部署新配置并重启测试。

**实验建议**：在虚拟机中添加内核参数 `init=/bin/sh`, `break=init` 或 `rd.break`，进入
initramfs 手动检查挂载和驱动加载过程。

---

## 2. systemd 接管

systemd（PID 1）负责并行启动 units、维护依赖关系、处理 cgroups 与环境隔离，并托管 system
与 user 的 lifecycle（包括 socket activation、timers、watchdog）。

**常用命令**：

```bash
# 默认 target
systemctl get-default

# 列出运行中的 services
systemctl list-units --type=service --state=running

# 查看某个 unit 的状态与日志
systemctl status sshd.service
journalctl -u sshd.service -b

# 启动性能分析
systemd-analyze blame
systemd-analyze critical-chain
```

**NixOS 提示**：`/etc/systemd/system` 中的所有配置文件都是借由声明式参数
`systemd.services."name".serviceConfig` 生成的，实际都是指向 `/nix/store` 的软链接，在排查
问题或学习 NixOS 时可查看这些配置的内容，但如果需要修改，应修改对应的声明式配置，而不是直
接修改这些文件。

### 2.1 日志收集

`systemd-journald` 是 systemd 提供的日志收集守护进程（daemon），它的主要职责包括：

- 收集来自内核（kmsg）、systemd、各个 system/service、user services、stdout/stderr（当
  unit 未做日志分流时）以及通过 syslog 转发来的日志。
- 将日志统一写入二进制 journal 格式（通常位于 `/run/log/journal`（临时）或
  `/var/log/journal`（持久））。
- 支持按字段索引（例如 `_PID`, `_COMM`, `_SYSTEMD_UNIT`, `SYSLOG_IDENTIFIER` 等），便于高
  效查询。
- 支持日志压缩、签名（Seal）、转发（ForwardToSyslog/ForwardToKMsg/ForwardToConsole），并对
  日志写入进行速率限制。

其配置文件位于 `/etc/systemd/journald.conf`，常见配置项包括：

- `Storage=`：`persistent|volatile|auto|none`。
  - `persistent`：写入 `/var/log/journal`（需要目录存在且有权限）。
  - `volatile`：只写入 `/run/log/journal`（不持久化）。
  - `auto`：若 `/var/log/journal` 存在则 persistent，否则 volatile（常用默认）。
- `Compress=`：是否压缩旧的 journal 文件（`yes/no`）。
- `SystemMaxUse=`：journal 在持久储存时允许占用的最大磁盘空间（例如 `1G`）。超过时会自动删
  除最旧的 journal 文件以回收空间。
- `SystemKeepFree=`：保留给系统的最小磁盘空间；journal 不会侵占超过该限制的空间。
- `SystemMaxFileSize=`：单个 journal 文件的最大大小。
- `SystemMaxFiles=`：保留的最大 journal 文件数（用于限制文件个数）。
- `RuntimeMaxUse` / `RuntimeKeepFree` / `RuntimeMaxFileSize`：对应 volatile（/run）空间的
  限制。
- `MaxRetentionSec=`：以时间为准的保留上限（可选）。
- unit 对 stdout/stderr 重定向：systemd unit 文件（`/etc/systemd/system/*.service` 或
  `/usr/lib/systemd/system`）可通过 `StandardOutput`/`StandardError` 配置。

**常用查询**：

```bash
# 本次引导日志
sudo journalctl -b

# 上一次引导
sudo journalctl -b -1

# 跟随某个 service 的实时日志
sudo journalctl -u sshd.service -f

# 过滤某个 unit 的字段
sudo journalctl -b _SYSTEMD_UNIT=hyprland.service

# 查看占用
journalctl --disk-usage

# 强制回收：只保留最近 2 周
sudo journalctl --vacuum-time=2weeks

# 手动触发日志轮转
sudo journalctl --rotate
sudo systemctl kill --kill-who=main --signal=SIGUSR1 systemd-journald
```

### 2.2 日志管理

- 如果使用 `Storage=persistent`，journal 会在 `/var/log/journal` 下以分块（.journal）文件
  存储日志。journald 会在后台根据
  `SystemMaxUse`、`SystemKeepFree`、`SystemMaxFileSize`、`SystemMaxFiles` 等约束来决定何时
  删除最旧的块（即所谓“轮转/回收”）。
- journald 不像经典 syslog 的 logrotate 那样按行和按规则轮换文本文件；它是二进制分块格式，
  轮转以文件大小和保留策略为单位。
- 管理员可以通过
  `journalctl --vacuum-size=100M`、`--vacuum-time=2weeks`、`--vacuum-files=5` 等命令强制回
  收达到指定策略。
- `journalctl --rotate` 可以手动触发 journald 进行日志切换（会使 journald 创建新的 journal
  文件并关闭当前文件句柄）。
- 若磁盘即将耗尽，journald 会优先回收最旧的 journal 使得磁盘空间达到 `SystemKeepFree` 要
  求。

---

## 3. udev 设备管理

udev 是 Linux 用户空间的设备管理员：当内核发出 uevent（设备插拔）时，udev 根据规则加载模
块、创建设备节点并设置权限。桌面系统中，udev 负责许多关键节点（/dev/input/event\*,
/dev/dri/_, /dev/snd/_）。

### 3.1 工作流与规则

**工作流**：

1. 内核（kernel）检测到硬件后发出 uevent（热插拔事件）。
2. udevd 接收事件，根据规则文件（`/usr/lib/udev/rules.d/`、`/etc/udev/rules.d/`）匹配并执
   行动作（`RUN` 脚本、设置 `OWNER`/`GROUP`/`MODE`、创建 symlink）。
3. udev 创建或移除 `/dev` 下相应的节点，并触发 systemd（通过 `udev` 的规则可激活 systemd
   的 device units）。

**常见规则示例**（使某个 USB 设备归属特定组）：

```ini
# /etc/udev/rules.d/90-mydevice.rules
SUBSYSTEM=="input", ATTRS{idVendor}=="abcd", ATTRS{idProduct}=="1234", MODE="660", GROUP="input", TAG+="uaccess"
```

`TAG+="uaccess"` 是现代桌面用来让 logind 接管设备权限与 session ACL（由 logind 配置）。

### 3.2 设备权限与 ACL

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

### 3.3 故障排查

#### 场景：插入外接键盘后，Wayland 会话收不到键盘事件（键盘无效）

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

---

## 4. logind 会话管理

systemd-logind 是连接登录、会话、seat、设备权限与电源管理的关键服务。它通过 D-Bus 暴露
API，管理登录会话并在用户登录/注销时分配/回收设备 ACL（例如音频、输入、GPU）。理解 logind
对桌面问题的定位极其重要。

### 4.1 职责与 API

**职责**：

- 管理登录会话：创建 session，维护 session->UID->TTY/seat 的映射。
- 设备访问：基于 udev 的 tag 或 seat 信息，logind 修改设备 ACL，将 `/dev/*` 的访问权授予当
  前会话。
- 电源按钮/挂起/休眠：logind 处理电源键事件并生成 D-Bus 消息，或根据策略触发
  suspend/shutdown。
- Seats 支持多用户多座席（seat0, seat1）场景。

**D-Bus 名称**：

- `org.freedesktop.login1` 是 logind 在 system bus 上的接口名称。可以用 `busctl` 或
  `gdbus` 与其交互查询状态。例如：

  ```bash
  busctl --system call org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager ListSessions
  ```

`systemd-logind` 的核心作用是把登录、会话、seat、设备许可、电源按钮处理、用户切换等系统级
桌面管理整合起来，并通过 system bus（`org.freedesktop.login1`）暴露 API。它通常监听 udev
产生的设备并根据 `TAG+="uaccess"` 或 `TAG+="seat"` 的规则，为特定会话分配 ACL（通过 POSIX
ACLs 或 device ACLs），从而让运行在会话内的合成器/应用访问设备
（`/dev/input/*`、`/dev/dri/*`、`/dev/snd/*`）。

**常见配置路径**：

- 主配置文件：`/etc/systemd/logind.conf`（在 NixOS 中通过 `services.logind` 或
  `systemd.logind` 模块设置）。
- D-Bus 名称：`org.freedesktop.login1`，对象路径：`/org/freedesktop/login1`，主要接
  口：`org.freedesktop.login1.Manager`。

### 4.2 seats 概念

#### 4.2.1 什么是 seat？

- **seat** 是 systemd/logind 引入的术语，用来表示“一组物理设备的集合”（例如一个显示器 + 一
  套键盘和鼠标 + 音频设备），以及与之关联的会话（sessions）。
- 一个现代桌面主机默认有 `seat0`（单座席系统）。在多座席（multi-seat）场景下，一台机器可以
  物理上分配多个 seat（通过额外的显卡/USB 集线器/显示器/输入设备），每个 seat 可以登录不同
  用户并同时本地使用系统（例如用于教学机、共享工作站等）。
- seat 的好处：将设备（GPU、输入设备）按逻辑分组并分配给对应会话，避免会话间互相干扰与权限
  混淆。

#### 4.2.2 seat 的设备分配原理

1. **udev** 产生设备时，规则可以指定 `TAG+="seat"` 或 `TAG+="uaccess"`。
2. **logind** 监听 udev 事件并把设备 ACL 赋予当前 active session（或特定 seat 下的
   session）。
3. 合成器（在对应用户 session 下）通过 libinput 打开 `/dev/input/*`、通过 DRM 打开
   `/dev/dri/*`，logind 保证在 ACL 层面允许该 session 的进程打开这些设备。

#### 4.2.3 常见命令与查看

- 列出 seats：

  ```bash
  loginctl seat-status
  # 或
  loginctl seat-status seat0
  ```

- 查看哪台 session 绑定到哪个 seat：

  ```bash
  loginctl list-sessions
  loginctl show-session <id> -p Name -p UID -p Seat
  ```

#### 4.2.4 多 seat 配置场景

- 在 udev 规则中给特定设备打上 `TAG+="seat"` 并使用 `X-Seat` 等属性区分（复杂场景通常需要
  自定义 udev 规则并结合 systemd-logind 的 seat API）。
- 对于需要把 GPU / monitor / USB hub 固定到某个 seat 的场景，通常在 udev 规则中通过
  `ATTRS{busnum}` / `ENV{ID_SEAT}` 等属性进行匹配并标注。
- 这类配置较复杂，生产环境中最好在测试机上先验证 `loginctl seat-status` 输出与在线用户会话
  的行为。

### 4.3 会话与设备管理

常用 `loginctl`：

```bash
# 列出会话
$ loginctl list-sessions

# 查看某 session 详细信息
$ loginctl show-session <sessid> --property=Name,UID,State,Remote,Display

# 查看 seat 状态（哪些设备分配给 seat）
$ loginctl seat-status seat0
```

`loginctl` 也可触发会话管理动作（锁屏、终止会话）。例如
`loginctl terminate-session <id>`。

### 4.4 常见问题

**问题例：Wayland compositor 启动但无法打开 `/dev/dri/card0`（GPU 权限问题）**

排查：

1. 确认 `ls -l /dev/dri/card0` 的 owner/group。通常应为 `root:video`，并且当前会话应被授予
   设备 ACL。
2. `loginctl seat-status seat0` 查看是否列出 `/dev/dri/card0` 并显示 ACL 给当前 session。
3. 若无，检查 udev 是否为 GPU 设备打上了 `TAG+="uaccess"` 或 `TAG+="seat"`。
4. 查看 `journalctl -u systemd-logind`，看是否在用户登录时有关于设备分配的错误。
5. 若服务是以 system user 的方式启动，确保 compositor 的进程是在用户 session 下，而不是
   systemd 服务或 root 启动的进程（起进程身份不同会导致权限问题）。

#### 问题例：意外挂起/关机（电源键/睡眠按钮不按用户设置工作）

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

## 5. 图形登录与会话启动

图形登录（Display Manager）负责用户认证并启动用户会话（通常交给 systemd-logind 来创会
话）。我这里使用了轻量的 greetd 作为我的 display manager。

### 5.1 登录链路

典型流程：

1. Display Manager (greetd/GDM/etc.) 启动并显示登录界面（Greeter）。
2. 用户输入用户名/密码 → PAM 验证（PAM 模块可以控制密码策略、session scripts）。
3. 认证成功后，Display Manager 请求 logind 创建 session（通过 D-Bus）。
4. logind 建立 session，分配设备 ACL，启动对应的 systemd user
   instance（`user@<UID>.service` 启动），并由该 user instance 启动
   `~/.config/environment.d`、`~/.config/autostart` 中或 `~/.config/systemd/user` 中定义的
   用户服务（例如 compositor）。
5. Display Manager 把会话的环境变量（WAYLAND_DISPLAY、XDG_RUNTIME_DIR）传递给用户服务，最
   终 compositor 启动并获得设备访问权。

**可观测点**：

- `journalctl -u greetd` 或 `journalctl -b _COMM=greetd`
- `loginctl list-sessions` 查看是否新会话被创建
- `journalctl --user -b`（在 user session 下）查看用户服务日志

### 5.2 调试方法

#### 问题示例：用户登录后 compositor 未启动或权限错误

- `journalctl -b --user -u hyprland.service` 或 `journalctl -b _UID=<UID> --no-pager` 查看
  用户日志。
- `loginctl show-session <id> -p Active -p State` 查看会话状态。
- 若 PAM 鉴权失败，检查 `/var/log/auth.log`（或 `journalctl -t login`）找 PAM 错误。

**实验（在本地复现登录链）**：

- 在测试账号下临时创建一个 systemd-user
  service（`~/.config/systemd/user/mycompositor.service`）来模拟 compositor，写入简单脚本
  `$XDG_RUNTIME_DIR/test.txt` 检查能否写入并正确获取环境。启动 greeter 登录观察 `loginctl`
  与 `journalctl --user` 的变化。

---

## 6. 桌面运行

合成器（compositor）是 Wayland 架构的核心。它直接管理输出（屏幕）、接收输入事件并将事件分
发给客户端，同时合成各个客户端的缓冲区到最终帧。libinput 处理来自 /dev/input 的原始事件，
并把处理后的事件给合成器；Mesa/EGL/GBM 负责渲染。

### 6.1 Wayland 合成器

- Wayland 使用客户端-服务器模型：合成器是服务器（wayland compositor），应用为客户端
  （wayland client）。
- 合成器通过 unix domain socket（通常路径在 `$XDG_RUNTIME_DIR/wayland-0`）与客户端通信，协
  议由 `libwayland` 实现（各种扩展如 `xdg-shell`、`ivi-surface` 等）。
- 客户端创建缓冲（EGL surface），绘制后提交给合成器；合成器决定何时将缓冲提交到 DRM。
- Wayland 设计让合成器掌控输入分配与安全：客户端不能直接读取其他客户端的内容或输入事件。

**验证点**：

```bash
# 是否处于 Wayland 会话
$ echo "$WAYLAND_DISPLAY"
# 显示当前 Wayland socket
$ ls $XDG_RUNTIME_DIR
```

#### 6.1.1 架构对比：X11 vs Wayland

- **X11（传统）**：X Server（`Xorg`）是显示服务器，窗口管理器 / 桌面环境（例如 i3、GNOME）
  作为 X client 连接到 X Server。`startx` 的流程本质上是：_启动 X Server，然后在 X Server
  中运行 window manager/compositor_。因此通常需要先启动 X Server，再通过 `exec i3` 启动窗
  口管理器。Display Manager（GDM/SDDM）为 X Server 创建合适的环境（DISPLAY 等）并做认证。
- **Wayland（现代）**：Wayland 的合成器（compositor）同时扮演**显示服务器 + 合成器**两职——
  它直接与内核的 DRM/KMS、输入设备（evdev）交互，负责输出的 mode-setting（显示模式设置）和
  输入事件采集/分发。客户端（wayland apps）通过 Wayland socket（通常在
  `$XDG_RUNTIME_DIR/wayland-0`）连接到合成器。由于合成器本身就直接控制显示与输入设备，它可
  以被**直接从一个登陆的 tty** 启动，成为该 tty 下的图形会话的 “display server”。因此并不
  需要先运行一个独立的 display server 再启动 compositor —— 合成器本身就是 display server +
  window manager 的合体。

#### 6.1.2 为什么 Wayland 合成器能直接在 tty 启动？

- 合成器通常以用户进程运行（在用户的 systemd-user 会话或由 display manager 启动），直接打
  开 `/dev/dri/card0`（DRM）和 `/dev/input/event*`（evdev），完成 KMS 设置与帧提交。因为合
  成器直接做了 X Server 在 X11 下做的事情，所以没有 `startx` 模式里的“先启动 server 再启动
  client”的必要。
- 启动方式可以是：

  - 由 display manager（greetd/GDM/SDDM）在认证成功后通过 logind 创建 session 并把环境
    （`XDG_RUNTIME_DIR`, `WAYLAND_DISPLAY` 等）传给 compositor；
  - 或者从一个登录 shell（tty）直接 `exec Hyprland`（注意：需要在登录 shell 下具备访问
    `/dev` 的权限，通常意味着要是登录到本地 console 的 session，这样 logind 会把会话与
    seat 关联并分配设备 ACL）。

- 因此常见的直接启动方式如下（在纯文本登录后的 `~/.profile` / `~/.bash_profile` 或
  systemd-user unit）：

  ```bash
  # 直接从 tty 启动 Wayland 合成器（示例）
  if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    exec Hyprland
  fi
  ```

  （在实际环境中推荐通过 display manager 或 systemd-user 管理会话，以便系统能正确分配 ACL
  与处理 PAM）

#### 6.1.3 架构差异带来的实际影响

- **安全与权限**：Wayland 把合成器放在更核心的位置（它有直接设备访问），因此确保合成器运行
  在正确会话（由 logind 管理）下至关重要。错误地以 root 或 system service 启动合成器会导致
  权限/ACL 不一致（compositor 无法访问设备或安全级别问题）。
- **简化流程**：Wayland 把多个角色合并到合成器进程，消除了 X11 时代客户端/窗口管理器与服务
  器的分离复杂度，令直接从 tty 启动合成器成为可行且常见的做法。
- **兼容性**：Xwayland 提供对 legacy X11 应用的兼容，合成器负责在启动时/按需启动 Xwayland
  以支持老应用。

### 6.2 合成器图形栈

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

### 6.3 合成器对比

虽然每个合成器的实现不同（如 Hyprland、Sway、Wayfire 等），但底层一致性高：都使用
libinput、Mesa、EGL/GBM、DRM，并遵循 Wayland 协议。区别在于窗口布局、扩展协议支持、配置方
式与插件生态。排查合成器问题时关键是关注底层资源：是否有 `/dev/dri` 权限、是否 libinput 列
出了输入设备、合成器日志中是否有 EGL/GBM 错误。

### 6.4 图形故障排查

**黑屏但登录已成功**：

1. 检查 compositor 是否仍在运行：`ps -u <user> | grep -E 'hyprland|sway|wayfire'`
2. 查看 compositor 的 user journal：`journalctl --user -u hyprland -b`
3. 检查 `/dev/dri` 权限与是否被其它进程占用（NVIDIA 私有驱动有时候会出现占用问题）。
4. 查看 kernel logs（`dmesg`) 是否有 GPU 驱动相关报错（比如 GPU hang）。

**渲染卡顿**：

- 用 `glxgears`（或更现代的 vulkan demo）做基准；观察 CPU/GPU 使用情况 `top`, `htop`,
  `perf top`。
- 若是 CPU-bound，可能是 compositor 逻辑或客户端繁忙；若 GPU-bound，可能是 Mesa 驱动缺陷或
  显存不足。
- `strace -p <pid>` 可以查看是否在做大量 syscalls（IO）。

---

## 7. 网络联网

网络是很多桌面问题的根源（更新失败、认证错误、remote resource 无法挂载等）。现代桌面常用
iwd + NetworkManager 的组合或 systemd-networkd。

### 7.1 网络启动

- 无线（Wi-Fi）需要硬件驱动、固件加载（firmware），然后由 iwd/wpa_supplicant 发起扫描/认
  证。
- 有线通常较简单：链路检测→DHCP→路由配置。

**日志点**：

- 内核固件/驱动载入：`dmesg | grep -i firmware` 或 `journalctl -k`
- iwd/NetworkManager 日志：`journalctl -u iwd`，`journalctl -u NetworkManager`，/ 或
  `nmcli` 状态输出。
- DHCP 客户端日志：`journalctl -u systemd-networkd` 或 `journalctl -u dhclient`（取决于客
  户端）。

### 7.2 网络配置

NixOS 配置示例（启用 NetworkManager + iwd 后端）：

```nix
networking.networkmanager.enable = true;
networking.networkmanager.wifi.backend = "iwd";
services.iwd.enable = true;
```

**实验**：

- 使用 `nmcli device wifi list` 与 `nmcli device wifi connect <SSID> password <PW>` 来连接
  并观察 `journalctl -u iwd` 的事件消息。

### 7.3 网络故障排查

**连接不上（Wi-Fi）**：

1. `ip link` 确认无线接口存在且 UP。
2. `iw dev wlan0 scan` 查看是否能扫描到 AP（需要 `iw` 权限）。
3. `sudo journalctl -u iwd -f` 在尝试连接时实时观察错误（如认证失败、4-way handshake
   errors）。
4. `nmcli -p dev wifi connect SSID ...` 用带显示的命令复现并观察。
5. 若是 WPA3/Enterprise 网络，检查证书与 EAP 配置。

**DNS 问题**：

- `resolvectl status`（systemd-resolved）查看当前 DNS 配置。
- `dig @<dns-server> example.com` 测试解析。
- 若 `/etc/resolv.conf` 链接被 systemd-resolved 管理，NixOS 中该行为可由配置控制。

---

## 8. 音频与视频处理

PipeWire 是现代 Linux 桌面系统的音频和视频处理核心，它统一了音频、视频和屏幕共享的处理流
程。PipeWire 替代了传统的 PulseAudio（音频）和 JACK（专业音频），同时提供了更好的低延迟和
更灵活的架构。

### 8.1 PipeWire 架构概述

**核心优势**：

- **统一架构**：同时处理音频、视频和屏幕共享
- **低延迟**：相比 PulseAudio 提供更低的音频延迟
- **向后兼容**：支持 ALSA、PulseAudio 和 JACK 客户端
- **模块化设计**：通过插件系统支持各种音频处理功能

**主要组件**：

- **pipewire**：核心守护进程，管理音频/视频流
- **wireplumber**：会话管理器，处理设备连接和路由策略
- **pipewire-pulse**：PulseAudio 兼容层
- **pipewire-jack**：JACK 兼容层
- **pipewire-alsa**：ALSA 兼容层

### 8.2 音频处理流程

当应用程序播放音频时，整个处理流程如下：

**1. 音频 API 选择**：

- 应用可以使用 ALSA、PulseAudio 或 JACK API
- NixOS 中安装了 `pipewire-pulse` 和 `pipewire-alsa` 后，系统提供兼容层
- 所有音频 API 最终都连接到 PipeWire 核心

**2. 音频流创建**：

- 每次应用播放声音时，在 PipeWire 中创建一个"流"（stream）
- 流包含音频格式、采样率、通道数等元数据
- 流被送入 PipeWire 的处理图（graph）

**3. 设备路由**：

- WirePlumber 根据用户配置和系统规则进行路由
- 将音频流路由到合适的物理设备（扬声器、耳机等）
- 支持自动切换（如插入耳机时自动切换输出）

**4. 音频处理**：

- PipeWire 混合多个应用的音频流
- 执行格式转换（采样率转换、位深度转换）
- 支持音量调节和音频效果（均衡器、回声等）

**5. 硬件输出**：

- 处理后的音频流通过 ALSA 驱动发送到物理硬件
- 内核驱动将 PCM 数据发送给声卡 DAC
- 最终转换为模拟声音输出

**6. 蓝牙音频支持**：

- PipeWire 管理蓝牙设备（A2DP 耳机、HFP 通话设备）
- 使用 BlueZ 模块实现蓝牙音频协议
- 支持 A2DP 流、HFP 通话等模式切换

### 8.3 关键概念

**核心概念**：

- **Node**：音频/视频源或目标（如麦克风、扬声器、应用）
- **Link**：节点间的连接，定义音频/视频流路径
- **Session Manager**：管理节点连接和路由策略
- **Graph**：描述当前所有节点和连接的拓扑结构

**多应用混音**：

- 多个应用同时发声时，PipeWire 将它们的流混合输出
- 用户可以通过音量控制工具（如 pavucontrol 或 wpctl）独立调节每个应用的音量
- 支持每个应用的独立音量控制和静音

### 8.4 启动与配置

**systemd 服务管理**：

```bash
# 查看 PipeWire 相关服务状态
systemctl --user status pipewire pipewire-pulse wireplumber

# 查看服务日志
journalctl --user -u pipewire -f
journalctl --user -u wireplumber -f

# 重启 PipeWire 服务
systemctl --user restart pipewire pipewire-pulse wireplumber
```

**NixOS 配置示例**：

```nix
# 启用 PipeWire
services.pipewire = {
  enable = true;
  alsa.enable = true;
  pulse.enable = true;
  jack.enable = true;
};

# 启用 WirePlumber 会话管理器
services.pipewire.wireplumber.enable = true;

# 禁用 PulseAudio（避免冲突）
hardware.pulseaudio.enable = false;
```

**环境变量检查**：

```bash
# 检查 PipeWire 环境
echo $PIPEWIRE_RUNTIME_DIR
echo $XDG_RUNTIME_DIR

# 查看 PipeWire 运行时目录
ls $XDG_RUNTIME_DIR/pipewire-*
```

### 8.5 音频设备管理

**设备查看与监控**：

```bash
# 使用 pw-cli 查看音频设备
pw-cli info

# 查看音频节点
pw-cli list-objects | grep -E "(Audio|Sink|Source)"

# 使用 pw-top 实时监控音频流
pw-top

# 使用 pavucontrol 图形界面管理音频
pavucontrol
```

**音频路由控制**：

```bash
# 创建音频连接（应用输出到扬声器）
pw-cli create-link <app-output-node-id> <speaker-input-node-id>

# 断开音频连接
pw-cli destroy-link <link-id>

# 设置默认音频设备
pactl set-default-sink <sink-name>
pactl set-default-source <source-name>
```

**音频测试**：

```bash
# 测试播放
paplay /usr/share/sounds/alsa/Front_Left.wav

# 测试录音
parecord --file-format=wav test.wav

# 检查 PulseAudio 兼容层
pactl info
```

### 8.6 视频与屏幕共享

**屏幕共享架构**：

- **X11**：通过 X11 扩展支持屏幕共享
- **Wayland**：通过 PipeWire 的 screen-capture 协议实现
- **应用支持**：OBS Studio、Discord、Zoom、Teams 等主流应用

**视频设备管理**：

```bash
# 查看视频设备
pw-cli list-objects | grep -i video

# 使用 v4l2-ctl 管理摄像头
v4l2-ctl --list-devices
v4l2-ctl --device=/dev/video0 --list-formats

# 检查摄像头权限
ls -l /dev/video*
```

**屏幕共享配置**：

```bash
# 检查 Wayland 协议支持
echo $WAYLAND_DISPLAY

# 设置桌面环境标识
export XDG_CURRENT_DESKTOP=sway  # 或其他合成器

# 检查 PipeWire 屏幕共享服务
systemctl --user status pipewire-session-manager
```

### 8.7 故障排查

#### 8.7.1 音频设备无法识别

**排查步骤**：

1. 检查 ALSA 设备：

   ```bash
   aplay -l
   arecord -l
   ```

2. 查看 PipeWire 日志：

   ```bash
   journalctl --user -u pipewire -f
   ```

3. 检查设备权限：

   ```bash
   ls -l /dev/snd/
   groups $USER  # 确认用户在 audio 组
   ```

4. 重启 PipeWire 服务：
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

**常见修复**：

- 权限问题：`sudo usermod -a -G audio $USER`
- 设备被占用：检查是否有其他音频服务运行
- 配置错误：删除用户配置重新生成

#### 8.7.2 音频延迟过高

**解决方案**：

1. 调整 PipeWire 配置（`~/.config/pipewire/pipewire.conf`）：

   ```ini
   context.properties = {
       default.clock.rate = 48000
       default.clock.quantum = 32
       default.clock.min-quantum = 32
       default.clock.max-quantum = 32
   }
   ```

2. 检查当前音频驱动：
   ```bash
   pw-cli info | grep -i driver
   ```

#### 8.7.3 应用无法播放音频

**排查步骤**：

1. 检查 PulseAudio 兼容层：`pactl info`
2. 查看音频流：`pw-top`
3. 测试音频播放：`paplay /usr/share/sounds/alsa/Front_Left.wav`

#### 8.7.4 屏幕共享在 Wayland 下不工作

**解决方案**：

1. 确认合成器支持 PipeWire 屏幕共享
2. 设置正确的环境变量：`export XDG_CURRENT_DESKTOP=sway`
3. 检查 PipeWire 屏幕共享服务状态

### 8.8 性能优化

#### 8.8.1 低延迟配置

**PipeWire 配置优化**：

```ini
# ~/.config/pipewire/pipewire.conf
context.properties = {
    default.clock.rate = 48000
    default.clock.quantum = 64
    default.clock.min-quantum = 32
    default.clock.max-quantum = 1024
}
```

**CPU 使用优化**：

```bash
# 监控 CPU 使用
pw-top

# 调整线程优先级
chrt -f 50 pipewire
```

#### 8.8.2 专业音频配置

**JACK 兼容模式**：

```bash
# 启用 JACK 兼容模式
export PIPEWIRE_LATENCY="32/48000"

# 使用专业音频应用
qjackctl  # JACK 控制面板
```

### 8.9 组件集成

#### 8.9.1 与合成器的集成

- **Hyprland**：自动支持 PipeWire 屏幕共享
- **Sway**：需要额外配置 `wlroots` 支持
- **GNOME/KDE**：内置 PipeWire 支持

#### 8.9.2 与应用的集成

- **浏览器**：Chrome/Firefox 通过 WebRTC 使用 PipeWire
- **视频会议**：Discord、Zoom、Teams 等
- **流媒体**：OBS Studio、FFmpeg 等

---

## 9. GUI 应用启动与交互

在 Wayland 模型下，每个 GUI 应用是一个 Wayland 客户端，通过 Wayland 客户端库
（libwayland-client）与合成器通信。现代 Linux 桌面应用通常使用高级图形工具包（如
GTK、Qt、SDL）来简化开发，这些工具包内部处理与 Wayland 协议的对接。

### 9.1 Wayland 应用架构

**客户端-服务器模型**：

- Wayland 使用客户端-服务器模型：合成器是服务器，应用为客户端
- 合成器通过 Unix 域 Socket（通常路径在 `$XDG_RUNTIME_DIR/wayland-0`）与客户端通信
- 协议由 `libwayland` 实现，支持各种扩展（如 `xdg-shell`、`ivi-surface` 等）

**安全特性**：

- Wayland 客户端只看到自己的窗口，无法窥视其他窗口
- 所有输入输出都通过合成器安全地分发给各客户端
- 没有像 X11 那样的全局屏幕、全局截屏等不安全功能

### 9.2 应用启动流程

**1. 建立连接**：

- 应用启动时创建 Wayland 显示连接（wl_display）
- 与合成器建立通信通道（Unix 域 Socket）
- 协商支持的协议扩展

**2. 窗口创建**：

- 应用请求创建窗口（surface）
- 合成器分配窗口 ID 和资源
- 设置窗口属性和事件监听

**3. 渲染上下文初始化**：

- 应用使用 OpenGL/ES 创建渲染上下文
- 通过 EGL 将渲染上下文与 Wayland 缓冲区关联
- 初始化 Mesa 图形驱动

### 9.3 应用渲染流程

**1. 渲染上下文创建**：

- 应用使用 OpenGL/ES 创建渲染上下文
- 通过 EGL 将渲染上下文与 Wayland 缓冲区关联
- 初始化 Mesa 图形驱动和硬件加速

**2. 内容绘制**：

- 应用调用 OpenGL/Vulkan API 绘制界面内容
- Mesa 将 API 调用转换为 GPU 指令
- 在 GPU 上执行渲染，生成帧缓冲数据

**3. 缓冲区提交**：

- 应用将渲染完成的缓冲区提交给合成器
- 通过 DMA-BUF 机制在应用和合成器间共享缓冲区
- 合成器接收缓冲区后进行最终合成和显示

**4. 页面翻转**：

- 合成器将多个应用的缓冲区组合成最终帧
- 通过 DRM/KMS 将最终帧提交到显示设备
- 完成页面翻转，用户看到更新后的画面

### 9.4 图形驱动支持

**主要驱动类型**：

- **Intel**：i965/Iris 驱动
- **AMD**：RADV/RadeonSI 驱动
- **NVIDIA**：Nouveau（开源）或专有驱动
- **ARM**：Mali、Broadcom 等驱动

**驱动功能**：

- 硬件加速渲染
- 着色器编译（GLSL/Vulkan SPIR-V）
- 缓冲区管理（通过 GBM 接口）
- 内存管理（GPU 显存与系统内存交换）

**检查驱动信息**：

```bash
# 查看 Mesa 版本和驱动信息
glxinfo | grep "OpenGL renderer"

# 输出示例：Mesa Intel® UHD Graphics 620 (LLVM ...)
```

### 9.5 图形工具包支持

**GTK**：

- GNOME 及许多应用使用的工具包
- GTK3/4 原生支持 Wayland 后端
- 在 Wayland 会话中默认使用 Wayland 后端
- 强制使用 X11 后端：`GDK_BACKEND=x11`

**Qt**：

- Qt5/6 支持 Wayland 后端
- 需要安装 `qt5-wayland` 或 `qt6-wayland` 包
- 在 Wayland 会话下自动使用 Wayland 渲染

**SDL**：

- 游戏和多媒体应用常用库
- SDL2 内部集成 Wayland 后端
- 大部分 SDL 应用在 Wayland 环境下正常渲染

### 9.6 输入事件处理

**事件流程**：

1. 用户输入（键盘、鼠标）→ 内核生成事件
2. 合成器接收输入事件
3. 根据窗口焦点分发给对应客户端
4. 客户端监听 Wayland 事件回调

**权限管理**：

- systemd-logind 确保应用对输入设备的访问权限
- 通过 ACL 机制控制设备访问
- 用户会话只能访问自己会话范围的资源

### 9.7 输入法集成

下一节将专门介绍输入法部分，这里仅做简单介绍。

**集成机制**：

- 图形工具包检查环境变量加载输入法模块
- 使用 Wayland 文本输入协议处理键盘事件
- 输入法通过 D-Bus（X11/Xwayland）或 text-input(wayland) 协议与客户端通信

### 9.8 应用启动管理

**启动方式**：

- 通过 shell/env 或桌面快捷方式（launcher）启动
- 现代桌面鼓励使用 `systemd --user` 管理长期运行的用户服务
- 优点：统一日志、自动重启、cgroups 管理

**systemd 用户服务示例**：

```ini
# ~/.config/systemd/user/my-app.service
[Unit]
Description=My Demo App

[Service]
ExecStart=/usr/bin/my-app
Restart=on-failure

[Install]
WantedBy=default.target
```

**服务管理命令**：

```bash
systemctl --user daemon-reload
systemctl --user enable --now my-app.service
journalctl --user -u my-app -f
```

**Xwayland 兼容**：

- 一些 legacy 应用仍需要 X11，通过 Xwayland 在 Wayland 上兼容
- 若 Xwayland 未启动或崩溃，旧应用会出现窗口或输入问题
- 合成器通常会自动管理 Xwayland 启动

### 9.9 应用故障排查

**调试工具**：

```bash
# 查看 core dump 列表
coredumpctl list

# 分析 core dump
coredumpctl info <PID>
coredumpctl debug <PID>

# 跟踪系统调用
strace -f -p <pid>

# 进程调试
gdb --pid <pid>
```

**常见问题诊断**：

- **应用卡死**：使用 `strace -p <pid>` 检查是否卡在 I/O 或 futex
- **GPU 问题**：查看 `dmesg` 是否报 GPU 重置（GPU hang）
- **内存泄漏**：使用 `valgrind` 或 `heaptrack` 分析内存使用
- **性能问题**：使用 `perf` 或 `htop` 分析 CPU 使用情况

---

## 10. 中文输入

输入法是 GUI 体验的重心之一。理解它如何与 Wayland 合成器、GTK/Qt、D-Bus 协作非常重要。

### 10.1 输入法框架

**总体结构**：

- 输入法通常以一个守护进程运行（例如 `fcitx5`），并通过插件/引擎（拼音、五笔等）处理候选
  词。
- 客户端（应用）通过 GTK/Qt 的 IM module 或 Wayland 的 text-input 协议与输入法交互。
- 候选词窗口：Fcitx5 负责在合适的屏幕位置显示中文候选词窗口。Wayland 约束应用只能绘制自己
  的窗口，所以候选框通常由 Fcitx5 自身或通过 GTK 等工具绘制。用户可在输入框下方看到候选列
  表，并选择想要的汉字词。
- 权限协调：systemd-logind 确保输入法进程和应用进程能够相互通信。因为它们都属于同一用户会
  话，所以可以共享一个 Wayland socket。logind 为整个会话分配了设备和通信权限。
- 键盘事件处理：当用户敲键时，键盘事件首先由 Hyprland 接收，然后传给前台窗口。如果前台窗口
  支持输入法，Hyprland 会把事件传给客户端应用的 Wayland 窗口；应用再交给 GTK/Qt 框架，由
  Fcitx5 插件拦截并处理。这样，Fcitx5 获得原始按键，生成候选后通过应用的输入接口（Wayland
  text protocol）插入文本。
- 在 Wayland 下，text-input 协议与 D-Bus 协调：应用发起文本输入会话（text-input），然后输
  入法显示候选并把最终文本发送回应用。

**观察工具**：

- `fcitx5-diagnose`（fcitx5 提供）检查配置。
- `busctl monitor` 或 `dbus-monitor`（若输入法使用 D-Bus）来监听通信。

### 10.2 环境配置

在 Xwayland 程序或只支持 X11 的老程序上，需要以下环境变量或模块：

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
```

这三个环境变量用于告诉 GTK / Qt / X11 应用使用哪种输入法模块（例如
`fcitx`、`ibus`）。`XMODIFIERS` 通常设置为 `@im=fcitx` 以便 X11 程序将输入事件转交给输入
法。

当你在 Xwayland 上运行老程序时，如果这些变量未正确设置，GTK/QT 应用会认为你未使用输入法，
也就不会将输入事件转交给 fcitx5，输入法就无法生效。

NixOS 中在 `programs.fcitx5.enable = true;` 后，确保 `environment.sessionVariables` 或
`programs.fcitx5.extraConfig` 配置正确。

### 10.3 候选词显示问题

**症状**：在某个应用中打拼音无候选词或候选框不显示。

排查步骤：

1. 确认输入法进程是否运行：`ps aux | grep fcitx5`。
2. 在终端运行 `fcitx5-diagnose` 获取诊断提示。
3. 确认应用是否使用原生 Wayland 文本协议或在 Xwayland 模式下（`echo $WAYLAND_DISPLAY` 与
   `echo $DISPLAY`）。
4. 若是 Qt/GTK 应用，确认 `QT_IM_MODULE` / `GTK_IM_MODULE` 是否正确设置（尤其针对
   Xwayland）。
5. `dbus-monitor --session` 或 `busctl --user monitor` 观察是否有输入法相关的 D-Bus 消息传
   递（例如应用请求候选）。
6. 在 compositor 日志中查看是否被定向或被阻止显示候选（某些合成器可能限制弹窗类型或层
   级）。

**常见根因**：

- 输入法进程未获得正确的 XDG_RUNTIME_DIR 或 DBUS_SESSION_BUS_ADDRESS 环境变量，导致无法通
  信。
- 应用本身没有启用输入法模块（需要重启应用/会话以继承环境变量）。
- Wayland text-input 与 compositor 的扩展版本不一致（罕见），或者应用使用内部的独立 IM 实
  现导致不兼容。

---

## 11. 系统关机流程

当用户在图形界面执行关机（或运行 `systemctl poweroff`）时，systemd 会按照严格的顺序关闭系
统。整个关机流程可以分为四个主要阶段：用户会话清理、系统服务停止、内核资源释放和硬件关机。

### 11.1 用户会话清理阶段

当用户触发关机时，systemd 首先切换到 `shutdown.target`，开始清理用户会话：

**用户应用退出**：

- 桌面环境中的应用（如 Waybar、Dunst、浏览器等）首先收到退出信号
- 用户可以通过 `journalctl --user -b` 查看用户服务的退出日志

**会话管理**：

- systemd-logind 终止所有用户会话，发送 SIGTERM 给用户进程
- 等待用户进程正常退出，超时后发送 SIGKILL 强制终止
- 日志中会显示 "Terminating user session XXX" 信息

**设备权限回收**：

- logind 回收分配给用户会话的设备访问权限（输入、音频、GPU 等）
- 确保用户进程不再保持对设备的锁定

### 11.2 系统服务停止阶段

用户会话清理完成后，systemd 开始停止系统级服务：

**图形服务停止**：

- 合成器（Hyprland）进程退出，释放显卡控制权
- Mesa 和 GPU 驱动清理上下文和分配的 GPU 内存
- `/dev/dri/card0` 等设备被释放

**音频服务停止**：

- PipeWire 和 WirePlumber 被停止，所有音频流关闭
- ALSA 驱动执行软重置，确保下次启动从干净状态开始

**网络服务停止**：

- NetworkManager、iwd、systemd-networkd 等网络管理器依次停止
- DHCP 租约被撤销，Wi-Fi 连接断开
- 网络接口最终被设置为下线状态

**其他系统服务**：

- udev 设备管理服务停止
- 各种后台守护进程按依赖关系依次退出

### 11.3 内核资源释放阶段

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

### 11.4 硬件关机阶段

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

### 11.5 关机流程观察与调试

**查看关机日志**：

```bash
# 查看上一次关机的详细日志
journalctl -b -1 -e

# 查看关机过程中的服务停止情况
journalctl -b -1 -p info | grep -E "(Stopping|Stopped)"
```

**关机故障排查**：

```bash
# 如果关机卡住，切换到另一终端查看
journalctl -f

# 查看未完成的任务
systemctl list-jobs

# 检查失败的单元
systemctl --failed
```

**常见问题**：

- 某个服务超时未停止：检查该服务的 `TimeoutStopSec` 配置
- 文件系统卸载失败：检查是否有进程仍在使用挂载点
- 硬件设备未正确释放：查看内核日志中的设备相关错误

### 11.6 注销流程

注销是关机的简化版本，只涉及用户会话的清理：

**观察点**：

- `loginctl list-sessions`：用户注销会话会从列表移除
- `journalctl --user -b -u <service>`：观察用户服务停止日志
- `systemctl --user`：列出 user units 的状态

**常见问题**：

- 注销时某个应用阻塞（例如未保存的文档）导致注销等待
- systemd 会发送 SIGTERM → 等待超时 → SIGKILL
- 通过 `journalctl` 查看哪些 service 超时并导致 logout 延迟

---

## 12. 综合故障案例

下面给出 3 个常见但复杂的实战案例，逐步演示从日志读出信息到最终修复的全过程（以便学以致
用）：

### 12.1 案例 1：输入法无响应

**症状**：桌面可用、键盘能打字但中文输入法无响应，按切换键也没有反应。

**定位**：

1. `ps aux | grep fcitx5`：确认 fcitx5 是否运行。
2. 如果未运行，则 `systemctl --user status fcitx5` 或 `journalctl --user -u fcitx5 -b`。
3. 若 fcitx5 运行但无响应，`fcitx5-diagnose` 输出检查
   DBUS_SESSION_BUS_ADDRESS、XDG_RUNTIME_DIR 等变量是否正确。
4. `busctl --user monitor` 观察是否有 text-input / fcitx5 的 D-Bus 消息。
5. 检查 compositor 日志（`journalctl --user -u hyprland -b`）是否有与 input method 相关的
   错误（例如焦点信息未传递）。

**常见修复**：

- 如果是环境变量问题（例如从 non-login shell 启动的应用未继承 IM 相关变量），重启会话或在
  NixOS 中设置 `environment.sessionVariables` 以确保变量被正确注入。
- 如果 fcitx5 脚本未安装插件（如 fcitx5-gtk、fcitx5-qt），在 `environment.systemPackages`
  中安装相应包并重建 NixOS 配置。
- 确认 `XMODIFIERS` 的设置用于 Xwayland 程序。

### 12.2 案例 2：系统启动慢

**定位**：

1. `systemd-analyze blame` 找到耗时最多的 unit（可能是
   `plymouth`、`NetworkManager-wait-online.service` 或某磁盘检查服务）。
2. `systemd-analyze critical-chain` 找阻塞链。
3. `journalctl -u <long-service>` 读日志找具体卡在哪里（等待网络、等待挂载、等待设备）。

**修复**：

- 对于 `NetworkManager-wait-online.service`，如果不需要等待网络，可禁用该 service 或把其设
  为 `wantedBy=multi-user.target` 之外，或减少 `TimeoutStartSec`。
- 对于磁盘检查（fsck）导致阻塞，检查硬盘 smart 状态并修复或跳过 fsck（风险自担）。

### 12.3 案例 3：合成器崩溃

**定位**：

1. 通过另一个 tty（Ctrl+Alt+F2）登录，执行 `journalctl -b -p err` 或
   `dmesg | tail -n 200`，搜索 GPU 相关错误（比如 i915 or amdgpu 输出）。
2. 查看 compositor 日志 `journalctl --user -u hyprland -b`，看是否报 EGL/GBM 错误。
3. `ls /dev/dri` 检查设备。
4. 若看到 GPU hang 报错，尝试降级 Mesa 或使用不同驱动（NixOS 中通过 pinning 不同 mesa
   包）。

**修复**：

- 临时：杀死合成器并使用 `XDG_SESSION_TYPE=x11` 或启用软件渲染
  （`LIBGL_ALWAYS_SOFTWARE=1`）登录以获取 GUI。
- 永久：回退/更新 Mesa 或内核，或为合成器配置软件后端；参考驱动 vendor 的固件/driver 建
  议。

### 12.4 案例 4：音频系统故障

**症状**：系统启动正常，但所有应用都无法播放音频，系统音效也没有声音。

**定位**：

1. 检查 PipeWire 服务状态：

   ```bash
   systemctl --user status pipewire pipewire-pulse wireplumber
   ```

2. 查看 PipeWire 日志：

   ```bash
   journalctl --user -u pipewire -b
   journalctl --user -u wireplumber -b
   ```

3. 检查音频设备：

   ```bash
   pw-cli info
   aplay -l
   ```

4. 测试音频流：

   ```bash
   pw-top  # 查看是否有音频流
   pactl info  # 检查 PulseAudio 兼容层
   ```

**常见修复**：

- **服务未启动**：`systemctl --user restart pipewire pipewire-pulse wireplumber`
- **权限问题**：确认用户在 `audio` 组：`sudo usermod -a -G audio $USER`
- **设备被占用**：检查是否有其他音频服务运行：`ps aux | grep -E "(pulse|alsa|jack)"`
- **配置错误**：删除用户配置重新生成：`rm -rf ~/.config/pipewire ~/.config/wireplumber`
- **NixOS 配置**：确保 `services.pipewire.enable = true` 且
  `hardware.pulseaudio.enable = false`

---

## 13. 附录

### 13.1 systemd 配置

- **路径**（优先级自高到低）：

  1. `/etc/systemd/system/`（管理员本地覆盖）
  2. `/run/systemd/system/`（运行时生成）
  3. `/usr/lib/systemd/system/`（发行版/包提供）

- **drop-in 覆盖**（修改单元的常见方法）：

  - 新建 `/etc/systemd/system/<name>.service.d/override.conf`，填写仅需要覆盖的字段，例
    如：

    ```ini
    [Service]
    Restart=always
    Environment=FOO=bar
    ```

  - `systemctl daemon-reload` 后生效。

- **在 NixOS 中**：不要直接编辑 `/etc/systemd/system`，而应在 `configuration.nix` 中用
  `systemd.services."name".serviceConfig` 或对应模块来设置。例如：

  ```nix
  systemd.services."my.service".serviceConfig = {
    ExecStart = "${pkgs.myapp}/bin/myapp";
    Restart = "on-failure";
  };
  ```

### 13.2 journald 配置

- `/etc/systemd/journald.conf`（覆盖），`/usr/lib/systemd/journald.conf`（默认）
- 常见字段：`Storage`, `Compress`, `SystemMaxUse`, `SystemKeepFree`, `RuntimeMaxUse`

### 13.3 logind 配置

- `/etc/systemd/logind.conf`（覆盖）
- 常见字段：`HandlePowerKey`, `HandleLidSwitch`, `IdleAction`, `KillUserProcesses`
- NixOS：通过 `services.logind` 或 `systemd.logind` 模块设置

### 13.4 udev 规则

- `/usr/lib/udev/rules.d/`（发行版默认）
- `/etc/udev/rules.d/`（本地规则）
- 示例（给输入设备标记 uaccess）：

  ```ini
  # /etc/udev/rules.d/90-local-input.rules
  SUBSYSTEM=="input", TAG+="uaccess"
  ```

- NixOS：在 `configuration.nix` 中使用
  `hardware.udev.rules`、`environment.etc."udev/rules.d/99-my.rules".text` 等方式管理

### 13.5 PipeWire 配置

**配置文件位置**：

- 系统配置：`/usr/share/pipewire/`
- 用户配置：`~/.config/pipewire/`
- 会话管理器：`~/.config/wireplumber/`

**常用配置示例**：

```ini
# ~/.config/pipewire/pipewire.conf
context.properties = {
    default.clock.rate = 48000
    default.clock.quantum = 32
    default.clock.min-quantum = 32
    default.clock.max-quantum = 1024
}
```

**NixOS PipeWire 配置**：

```nix
services.pipewire = {
  enable = true;
  alsa.enable = true;
  pulse.enable = true;
  jack.enable = true;

  # 低延迟配置
  extraConfig.pipewire."92-low-latency" = {
    context.properties = {
      default.clock.rate = 48000;
      default.clock.quantum = 32;
      default.clock.min-quantum = 32;
      default.clock.max-quantum = 32;
    };
  };
};
```
