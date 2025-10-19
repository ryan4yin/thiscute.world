---
title: "Linux 桌面系统故障排查指南（六） - 系统关机与电源管理"
subtitle: ""
description:
  "深入探讨 Linux 桌面系统的关机流程、休眠和挂起功能，以及电源管理的故障排查方法"
date: 2025-10-19T10:22:33+08:00
lastmod: 2025-10-19T10:22:33+08:00
draft: false

authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Linux", "Desktop", "Systemd", "D-Bus", "Power Management", "Hibernate", "Suspend"]
categories: ["tech"]
series: ["Linux 桌面系统"]
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

> **AI 创作声明**：本系列文章由笔者借助 ChatGPT, Kimi K2, 豆包和 Cursor 等 AI 工具创作，有
> 很大篇幅的内容完全由 AI 在我的指导下生成。如有错误，还请指正。

## 前言

系统关机看似简单，但背后涉及了繁杂的资源清理和状态管理过程。当你点击关机按钮，系统却卡在那
里不动，或者出现各种奇怪的错误信息时，理解关机流程和故障排查方法就显得尤为重要。

除了关机，Linux 还提供了休眠和挂起两种重要的电源管理功能，它们可以让系统快速进入低功耗状
态，同时保持工作状态，是日常使用中非常实用的功能。

作为这个系列的最后一篇文章，本文将探讨系统关机的完整流程，以及休眠和挂起功能的配置与故障排
查，从优雅关闭到强制关机，从服务停止到资源清理，从电源管理到状态恢复，全面了解系统的电源管
理机制。

---

## 系统关机流程

### 1.1 关机流程概览

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

### 1.2 用户会话清理

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

### 1.3 系统服务停止

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

### 1.4 内核资源释放

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

### 1.5 硬件关机

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

### 1.6 关机故障排查

**常见关机问题与优化**：

1. **服务停止超时**：

```bash
# 查看超时服务
journalctl -b -1 | grep -i "timeout"

# 检查特定服务配置
systemctl cat <service> | grep Timeout
```

服务停止超时优化：

TimeoutStopSec 参数控制服务停止的最大等待时间，默认值为 90 秒。systemd 在停止服务时会等待
服务自行退出，超时后强制终止。对于快速停止的服务，可以设置较短的超时时间（如 10-30 秒），
配置示例：`TimeoutStopSec=30s` 设置 30 秒超时。

服务停止优化包括：服务应该正确处理 SIGTERM 信号，完成必要的清理工作；避免在停止过程中进行
耗时的操作；确保及时释放文件句柄、网络连接等资源。

2. **文件系统卸载失败**：

```bash
# 查找占用文件系统的进程
lsof | grep <mountpoint>

# 检查文件系统状态
fsck -n /dev/<device>
```

文件系统卸载优化：

进程占用检查使用 `lsof` 命令查找仍在使用文件系统的进程。常见原因是应用程序未正确关闭文件句
柄，或进程仍在运行。解决方案是强制终止占用进程，或等待进程自然结束。

文件系统状态检查包括：使用 `fsck -n` 进行只读检查，不修复文件系统；检查文件系统是否正确挂
载，是否有错误标记；定期进行文件系统检查，及时发现和修复问题。

3. **设备繁忙**：

```bash
# 检查设备占用
lsof | grep /dev/<device>

# 查看块设备状态
lsblk -f
```

设备占用优化：

设备占用分析检查哪些进程仍在使用设备文件。常见设备包括 USB 设备、外部存储、网络设备等。解
决方案是确保应用程序正确关闭设备，或强制卸载设备。

块设备状态检查包括：使用 lsblk 查看设备挂载状态和文件系统类型；检查设备是否处于忙碌状态；
在关机前确保所有外部设备已安全移除。

**强制关机处理与优化**：

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

强制关机方法：

`systemctl poweroff -f` 强制关机，跳过某些检查和服务停止。强制终止所有进程，直接进入关机流
程，可能导致数据丢失，应谨慎使用，适用于系统响应缓慢但仍有基本功能时。

`systemctl poweroff -ff` 紧急关机，立即执行，不等待任何操作完成。立即终止所有进程，强制关
机，高数据丢失风险，仅在紧急情况下使用，适用于系统完全无响应，需要立即关机。

`echo b > /proc/sysrq-trigger` 内核级别的强制重启。直接调用内核重启功能，绕过用户空间，即
使系统完全无响应也能执行，适用于系统完全卡死，无法响应用户命令。

`echo o > /proc/sysrq-trigger` 内核级别的强制关机。直接调用内核关机功能，立即断电，最高数
据丢失风险，适用于极端紧急情况，需要立即断电。

关机优化最佳实践：

预防措施：定期检查服务配置，确保服务能正常停止；监控文件系统状态，及时处理问题；避免在关机
前进行大量 I/O 操作。

优雅关机：优先使用正常的关机命令；给系统足够时间完成清理工作；避免频繁使用强制关机。

故障预防：定期更新系统和驱动；监控系统资源使用情况；及时处理系统警告和错误。

---

## 系统休眠与挂起

除了关机，Linux 还提供了两种重要的电源管理功能：**休眠（Hibernate）**和**挂起
（Suspend）**。这两种功能可以让系统快速进入低功耗状态，同时保持工作状态，是日常使用中非常
实用的功能。

### 3.1 休眠（Hibernate）功能

休眠是将系统内存中的所有数据保存到磁盘（通常是交换分区或交换文件），然后完全关闭电源。当系
统从休眠中恢复时，会从磁盘读取保存的数据，恢复到休眠前的状态。

**休眠的工作原理**：

1. **内存数据保存**：将 RAM 中的所有数据写入到交换分区或专门的休眠文件
2. **系统状态保存**：保存 CPU 状态、设备状态、网络连接等
3. **完全断电**：系统完全关闭，所有硬件断电
4. **快速恢复**：开机时直接从磁盘恢复内存状态，跳过正常启动过程

**休眠配置**：

```bash
# 检查当前休眠配置
cat /sys/power/state
cat /sys/power/disk

# 检查交换分区大小（需要足够容纳内存数据）
swapon --show
free -h

# 检查休眠文件（如果使用文件而非交换分区）
ls -lh /swapfile
```

**启用休眠功能**：

```bash
# 方法一：使用交换分区
# 1. 确保有足够大的交换分区（建议为内存大小的 1.5-2 倍）
sudo swapon --show

# 2. 获取交换分区的 UUID
sudo blkid | grep swap

# 3. 更新 GRUB 配置
sudo nano /etc/default/grub
# 添加：GRUB_CMDLINE_LINUX_DEFAULT="resume=UUID=your-swap-uuid"

# 4. 更新 GRUB 配置
sudo update-grub

# 5. 重新生成 initramfs
sudo update-initramfs -u

# 方法二：使用交换文件
# 1. 创建交换文件（大小建议为内存的 1.5-2 倍）
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 2. 永久挂载交换文件
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 3. 配置休眠到交换文件
echo 'RESUME=UUID=$(findmnt -no UUID -T /swapfile)' | sudo tee /etc/initramfs-tools/conf.d/resume
sudo update-initramfs -u
```

**休眠故障排查**：

```bash
# 检查休眠支持
cat /sys/power/state | grep disk

# 检查休眠目标
cat /sys/power/disk

# 测试休眠功能
sudo systemctl hibernate

# 查看休眠日志
journalctl -b | grep -i hibernate
dmesg | grep -i hibernate

# 检查交换空间使用情况
swapon --show
free -h
```

**常见休眠问题**：

1. **交换空间不足**：

   - 问题：交换分区或文件太小，无法容纳内存数据
   - 解决：增加交换空间大小，建议为内存的 1.5-2 倍

2. **休眠文件损坏**：

   - 问题：休眠文件损坏导致恢复失败
   - 解决：删除损坏的休眠文件，重新创建

3. **硬件不支持**：
   - 问题：某些硬件不支持休眠功能
   - 解决：检查 BIOS/UEFI 设置，更新固件

### 3.2 挂起（Suspend）功能

挂起是将系统进入低功耗状态，保持内存供电，CPU 和大部分硬件断电。系统可以快速恢复到挂起前的
状态，但需要持续供电。

**挂起的工作原理**：

1. **内存保持供电**：RAM 继续供电，保持数据不丢失
2. **CPU 进入睡眠状态**：CPU 进入深度睡眠，功耗极低
3. **外设断电**：硬盘、USB 设备、网络设备等断电
4. **快速唤醒**：通过键盘、鼠标、网络唤醒等快速恢复

**挂起类型**：

- **S1（Power On Suspend）**：CPU 停止执行，但保持供电
- **S2（CPU Off）**：CPU 断电，但保持缓存
- **S3（Suspend to RAM）**：CPU 和缓存断电，仅内存供电
- **S4（Suspend to Disk）**：等同于休眠

**挂起配置**：

```bash
# 检查支持的挂起状态
cat /sys/power/state

# 检查当前挂起模式
cat /sys/power/mem_sleep

# 设置挂起模式（deep 为 S3，s2idle 为 S2）
echo deep | sudo tee /sys/power/mem_sleep

# 永久设置挂起模式
echo 'mem_sleep_default=deep' | sudo tee -a /etc/default/grub
sudo update-grub
```

**挂起故障排查**：

```bash
# 测试挂起功能
sudo systemctl suspend

# 查看挂起日志
journalctl -b | grep -i suspend
dmesg | grep -i suspend

# 检查挂起相关服务
systemctl status systemd-suspend
systemctl status systemd-hibernate

# 检查挂起钩子脚本
ls -la /usr/lib/systemd/system-sleep/
```

**常见挂起问题**：

1. **挂起后无法唤醒**：

   - 问题：系统挂起后无法通过键盘、鼠标唤醒
   - 解决：检查 BIOS 设置，启用 USB 唤醒功能

2. **挂起后系统重启**：

   - 问题：挂起后系统自动重启而不是恢复
   - 解决：检查硬件兼容性，更新驱动

3. **挂起功耗过高**：
   - 问题：挂起状态下功耗仍然很高
   - 解决：检查外设电源管理，禁用不必要的设备

### 3.3 电源管理模式对比

| 模式     | 功耗 | 恢复时间 | 数据保持 | 适用场景                   |
| -------- | ---- | -------- | -------- | -------------------------- |
| **关机** | 0W   | 30-60秒  | 不保持   | 长时间不使用               |
| **休眠** | 0W   | 10-30秒  | 完全保持 | 长时间不使用，需要快速恢复 |
| **挂起** | 1-5W | 1-3秒    | 完全保持 | 短时间不使用，需要快速恢复 |

**选择建议**：

- **短时间离开**（几分钟到几小时）：使用挂起
- **长时间离开**（几小时到几天）：使用休眠
- **长期不使用**（几天以上）：使用关机

**混合使用策略**：

```bash
# 设置自动挂起（当系统空闲时）
sudo systemctl enable systemd-suspend.timer

# 设置定时休眠（夜间自动休眠）
sudo systemctl edit systemd-hibernate.timer
# 添加：
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
```

在实际使用中，大多数用户通过桌面环境的设置界面来配置电源管理功能。GNOME、KDE Plasma、XFCE
等桌面环境都提供了图形化的电源管理设置，可以方便地配置自动挂起和休眠时间。

对于使用 Wayland 合成器（如 Sway、Hyprland）的用户，通常使用专门的 idle 守护进程来管理电源
状态。swayidle、hypridle 等工具可以配置系统在空闲时自动锁屏、关闭显示器或进入挂起状态。

**电源管理优化**：

```bash
# 检查电源管理配置
cat /sys/power/pm_async
cat /sys/power/pm_freeze_timeout

# 优化挂起延迟
echo 5000 | sudo tee /sys/power/pm_freeze_timeout

# 检查设备电源管理
ls /sys/bus/usb/devices/*/power/
cat /sys/bus/usb/devices/*/power/control
```

通过合理配置和使用休眠、挂起功能，可以显著提高 Linux 桌面系统的使用体验，既节省电力又保持
工作状态的连续性。

---

## 实战案例：综合故障排查

在实际使用 Linux 桌面系统时，往往会遇到多层次、多组件交织的故障。通过系统化的排查方法，可
以快速定位问题并制定解决方案。本章通过几个典型案例，讲解如何综合使用日志、调试工具和系统命
令进行故障排查。

### 2.1 案例一：桌面环境无法启动

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

**解决方法**：

- 更新或切换 GPU 驱动
- 使用默认配置启动合成器
- 检查 `$XDG_RUNTIME_DIR` 和 `$WAYLAND_DISPLAY` 是否正确

---

### 2.2 案例二：应用程序崩溃或无响应

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

**解决方法**：

- 安装或升级依赖库
- 强制应用使用 X11 或 Wayland 后端
- 检查驱动更新或使用回滚版本

---

### 2.3 案例三：系统关机或重启异常

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

**解决方法**：

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

### 2.4 案例四：网络异常导致应用无法访问

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

**解决方法**：

- 修复网络配置
- 检查防火墙规则
- 重启网络服务

---

### 2.5 综合排查方法

面对复杂问题，单靠经验可能难以定位故障，推荐遵循以下方法：

1. **日志为先**：系统日志、用户服务日志、应用日志是最直接的线索
2. **逐层排查**：从硬件 → 驱动 → 系统服务 → 用户会话 → 应用
3. **最小复现**：关闭非必要服务和应用，简化环境重现问题
4. **工具辅助**：`journalctl`、`strace`、`coredumpctl`、`lsof`、`perf` 等
5. **文档与社区**：查阅官方文档和社区经验，快速定位常见故障

通过上述方法，可以系统化地分析并解决大多数 Linux 桌面问题，提高系统稳定性和用户体验。

## 总结

至此，我们已经完成了《Linux 桌面系统故障排查指南》系列的全部六篇文章。通过这个系列，我们全
面了解了 Linux 桌面系统的各个组件，从启动安全到网络配置，从多媒体输入到会话管理，从系统服
务到电源管理。

Linux 桌面系统虽然有时候会出各种奇怪的问题，但理解其工作原理后，大部分问题都能找到解决思
路。关键是要有耐心，多实践，多总结。特别是在电源管理方面，合理使用关机、休眠和挂起功能，可
以显著提高系统的使用体验和电力效率。

这个系列到这里就结束了，希望这些内容能帮助你在 Linux 桌面的道路上走得更顺畅一些。

### 🔗 相关资源

- **技术文
  档**：[systemd 官方文档](https://systemd.io/)、[Wayland 协议规范](https://wayland.freedesktop.org/)
- **社区资
  源**：[Arch Wiki](https://wiki.archlinux.org/)、[Gentoo Wiki](https://wiki.gentoo.org/)
