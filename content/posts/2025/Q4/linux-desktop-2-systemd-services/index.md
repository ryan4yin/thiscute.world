---
title: "Linux 桌面系统故障排查指南（二） - systemd 全家桶与服务管理"
subtitle: ""
description:
  "全面介绍 systemd 服务管理、用户服务、D-Bus 通信机制和桌面环境集成，掌握现代 Linux
  系统的服务架构"
date: 2025-10-19T10:18:33+08:00
lastmod: 2025-10-19T10:18:33+08:00
draft: false

authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Linux", "Desktop", "Systemd", "D-Bus"]
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

## 概述

本文是《Linux 桌面系统故障排查指南》系列的第二篇，专注于 systemd 生态系统与服务管理。在上
一篇中，我们了解了系统启动与安全框架，现在让我们深入探讨 systemd 核心功能以及 systemd 生态
系统中的各个专门化组件。

⚙️ 本文主要介绍如下内容：

- **systemd 核心功能**：服务管理、依赖关系、并行启动、单元类型配置
- **systemd 生态系统服
  务**：systemd-journald、systemd-oomd、systemd-resolved、systemd-timesyncd、systemd-udevd
  等
- **设备管理**：udev 规则和设备权限分配、故障排查
- **D-Bus 系统总线**：进程间通信机制、权限管控、调试方法

---

## 1. systemd 核心功能

systemd 作为 PID 1，是现代 Linux 系统的初始化系统和服务管理器。它负责并行启动服务、维护依
赖关系、管理 cgroups，并提供统一的系统管理接口。

### 1.1 systemd 概览与基本操作

systemd 作为现代 Linux 系统的初始化系统和服务管理器，主要专注于服务管理和系统控制。

**核心功能**：

- **服务管理**：并行启动 units，维护依赖关系
- **资源控制**：通过 cgroups 实现进程隔离和资源限制
- **系统状态管理**：通过 target 管理不同的系统运行状态
- **单元生命周期管理**：管理各种类型单元（service、mount、timer 等）的启动、停止和重启

**常用命令**：

```bash
# 系统状态查看
systemctl get-default                     # 默认 target
systemctl list-units --type=service       # 列出服务
systemctl status sshd.service             # 服务状态

# 性能分析
systemd-analyze blame                     # 启动耗时分析
systemd-analyze critical-chain            # 关键路径分析

# 服务管理
systemctl start/stop/restart service      # 服务控制
systemctl enable/disable service          # 开机自启控制
systemctl reload service                  # 重载配置
```

**NixOS 特殊说明**：在 NixOS 中，`/etc/systemd/system` 下的配置文件都是通过声明式参数生成
的软链接，指向 `/nix/store`。修改配置应通过 NixOS 配置系统，而非直接编辑这些文件。NixOS 没
有传统的 `/usr` 和 `/lib` 等 FHS 目录，所有软件包都存储在 `/nix/store` 中，通过
`/run/current-system/sw/` 等符号链接提供访问。

**配置文件路径**：

- `/etc/systemd/system/`：系统级服务配置
- `/run/current-system/sw/lib/systemd/system/`（NixOS）或 `/usr/lib/systemd/system/`（传统
  发行版）：软件包提供的默认配置
- `/etc/systemd/user/`：用户级服务配置

### 1.2 服务单元类型与配置

systemd 支持多种单元类型，每种类型都有其特定的用途和配置方式。

**主要单元类型**：

- **service**：服务单元，管理后台进程
- **target**：目标单元，用于系统状态管理
- **mount**：挂载单元，管理文件系统挂载
- **timer**：定时器单元，替代 cron 任务
- **socket**：套接字单元，按需启动服务

**服务单元配置示例**：

```ini
[Unit]
Description=My Custom Service
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/bin/my-service
Restart=always
User=myuser
Group=mygroup

[Install]
WantedBy=multi-user.target
```

### 1.3 systemd 依赖关系与启动顺序

systemd 通过依赖关系管理服务的启动顺序，确保服务按正确的顺序启动。

**依赖关系类型**：

- **Requires**：强依赖，被依赖服务失败时，依赖服务也会失败
- **Wants**：弱依赖，被依赖服务失败时，依赖服务仍可启动
- **After**：启动顺序依赖，确保在指定服务之后启动
- **Before**：启动顺序依赖，确保在指定服务之前启动

**示例配置**：

```ini
[Unit]
Description=Web Server
After=network.target
Wants=network.target
Requires=nginx.service

[Service]
Type=forking
ExecStart=/usr/sbin/nginx
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 2. systemd 生态系统服务

除了基本的服务管理外，systemd 还提供了多个专门化的系统服务来支持现代 Linux 桌面的核心功
能，包括日志管理、内存管理、DNS 解析和时间同步等。

本节内容仅介绍最核心的几个 systemd 服务。

> systemd 全家桶，你值得拥有（

### 2.1 日志系统：systemd-journald

systemd-journald 是 systemd 内置的日志收集守护进程，统一处理内核、系统服务及应用的日志，是
现代 Linux 系统日志管理的核心组件。

#### 2.1.1 核心特性

| 特性               | 说明                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| **统一收集**       | 内核日志、systemd 单元（stdout/stderr）、普通进程、容器、第三方 syslog 均汇总到同一日志流。    |
| **二进制索引**     | 以 B+树（有序索引）+偏移量建立字段索引，支持精确查询与时间/优先级范围查询，速度远超文本 grep。 |
| **字段化存储**     | 自动生成 `_PID`、`_UID`、`_SYSTEMD_UNIT` 等可信字段（不可伪造）；支持自定义 `FOO=bar` 字段。   |
| **自动轮转与压缩** | 按「大小、时间、文件数」回收日志；轮转后默认用 LZ4 压缩，节省 60% 以上空间。                   |
| **速率限制**       | 可通过 `RateLimitIntervalSec=`/`RateLimitBurst=` 调整。                                        |
| **日志防篡改**     | 配置 `Seal=yes` 后，用 `journalctl --setup-keys` 生成密钥，之后可用该密钥验证日志完整性。      |

#### 2.1.2 日志的4个收集入口

journald 仅通过标准化入口收集日志，确保来源可追溯：

1. **内核日志**：内核 `printk()` 输出 → `/dev/kmsg` → journald（会自动添加 `_PID`/`_COMM`
   等字段）；
2. **systemd 单元 stdout/stderr**：单元进程输出自动捕获，会附加
   `_SYSTEMD_UNIT=xxx.service` 等 systemd 相关字段；
3. **本地 Socket**：`/run/systemd/journal/socket` 等，接收 `logger`/`systemd-cat` 及旧
   syslog 应用日志；
4. **显式 API**：`sd_journal_send()`，仅需自定义复杂结构化日志时使用（譬如 Docker
   daemon）, 一般直接 print 即可。

#### 2.1.3 日志优先级与核心配置

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

#### 2.1.4 实验：用 logger 验证日志收集

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

#### 2.1.5 旧日志系统与 /var/log/ 解析

##### 旧日志系统：基于 syslog 的文本管理

在 systemd 普及前，Linux 依赖 **syslog 协议+文本文件** 管理日志，核心组件是
**rsyslog**（syslog 主流实现，功能强于早期 `syslogd`）。

- **旧系统工作流**：应用通过 `syslog(3)` 接口输出日志 → rsyslog 接收 → 按「设施+优先级」写
  入 `/var/log/` 文本文件；
- **现代系统中的角色**：rsyslog 不再是核心收集器，而是作为「兼容层」——接收 journald 转发的
  日志，生成传统文本文件（如 `/var/log/auth.log`），或转发到远程日志服务器（支持 TCP/TLS
  加密）。

##### /var/log/ 常见文件及功能

现代系统中，这些文件由 rsyslog 生成（兼容旧习惯），不同发行版名称略有差异，但都为纯文本格
式：

| 文件（或目录）                                            | 主要发行版差异               | 功能说明                                                                   |
| --------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| `/var/log/messages`                                       | RHEL/CentOS/SUSE             | 系统通用日志：服务启停、内核提示、非专项应用消息。                         |
| `/var/log/syslog`                                         | Ubuntu/Debian                | 等价于 RHEL 的 `messages`，存储内核及一般系统日志。                        |
| `/var/log/auth.log`（Ubuntu） / `/var/log/secure`（RHEL） | 名称不同                     | 认证与授权事件：SSH 登录、su/sudo、用户添加/删除、PAM 告警。安全审计必看。 |
| `/var/log/kern.log`                                       | 通用                         | 仅内核环控输出：硬件故障、驱动加载、OOM、segfault。                        |
| `/var/log/cron`                                           | 通用                         | crond 执行记录：任务启动/结束、错误输出、邮件发送结果。                    |
| `/var/log/btmp`                                           | 通用                         | 二进制文件，记录**失败**登录（lastb 读取）；大小随暴力破解增长。           |
| `/var/log/wtmp`                                           | 通用                         | 二进制文件，记录**成功**登录/注销/重启（last、who 读取）。                 |
| `/var/log/lastlog`                                        | 通用                         | 二进制文件，记录每个用户最近一次登录时间（lastlog 读取）。                 |
| `/var/log/journal/`                                       | 启用 systemd-journald 后可见 | **目录**；若 `Storage=persistent`，则二进制 journal 文件存于此。           |

#### 2.1.6 日志写入最佳实践

| 场景                  | 推荐做法                                                                                 |
| --------------------- | ---------------------------------------------------------------------------------------- |
| Shell脚本（独立运行） | `logger -t 脚本名 -p daemon.err "错误：$msg"`（如 `logger -t backup -p err "备份失败"`） |
| 应用程序              | 优先考虑使用 systemd service, 少数场景可考虑直接调用 `sd_journal_send()` API             |
| 容器                  | Docker/Podman 加 `--log-driver=journald`（容器内正常输出即可）                           |
| 高频日志              | 设 `RateLimitIntervalSec=0` 关闭限制（需评估风险），或批量写入                           |
| 敏感信息              | 脱敏处理（如 `PASSWORD=***`），避免明文存储                                              |

#### 2.1.7 运维命令速查

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

### 2.2 内存管理：systemd-oomd

systemd-oomd 是 systemd 提供的内存不足（OOM）守护进程，用于在系统内存紧张时主动终止进程，
防止系统完全卡死。听起来有点"残忍"，不过总比系统彻底死机要好。

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

### 2.3 DNS 解析：systemd-resolved

systemd-resolved 提供统一的 DNS 解析服务，支持 DNSSEC 验证、DNS over TLS 等现代 DNS 特性。
名字是长了点，不过功能倒是挺全面的，基本上把 DNS 解析这件事包圆了。

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

### 2.4 时间同步：systemd-timesyncd

systemd-timesyncd 是轻量级 NTP 客户端，负责保持系统时间与网络时间服务器同步。功能简单直
接，就是确保你的系统时间不会跑偏，避免出现"时间穿越"的尴尬情况。

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

## 3. 设备管理：udev 与 systemd-udevd

udev 是 Linux 用户空间的设备管理员，负责处理内核的设备事件，创建节点并设置权限。在现代
systemd 系统中，udev 功能由 **systemd-udevd** 守护进程实现，它是 systemd 生态系统的重要组
成部分。

### 3.1 udev 与 systemd-udevd

#### 3.1.1 udev 设备管理框架

udev 是 Linux 内核的用户空间设备管理框架，负责处理内核的设备事件并管理 `/dev` 目录下的设备
节点。

**udev 的核心功能**：

- **动态设备管理**：当硬件设备插入或移除时，自动创建设备节点
- **设备命名**：提供一致的设备命名规则，如 `/dev/disk/by-uuid/`、`/dev/input/by-id/`
- **权限控制**：根据设备类型和用户需求设置适当的设备权限
- **规则系统**：通过规则文件实现复杂的设备处理逻辑

**udev 的工作原理**：

1. 内核检测到硬件变化，通过 netlink socket 发送 uevent 到用户空间
2. udev 守护进程接收 uevent，解析设备属性
3. 根据规则文件匹配设备，执行相应的动作（创建设备节点、设置权限等）

#### 3.1.2 systemd-udevd 实现

在现代 systemd 系统中，udev 用户空间的功能由 **systemd-udevd** 守护进程实现，它是 systemd
生态系统的重要组成部分。

**systemd-udevd 的优势**：

- **systemd 集成**：作为 systemd 服务运行，享受 systemd 的服务管理、日志记录、依赖管理等功
  能
- **性能优化**：相比传统的 udevd，systemd-udevd 在启动速度和资源使用上有所优化
- **统一管理**：与 systemd 的其他组件（如 systemd-logind）深度集成，提供统一的设备权限管理

**systemd-udevd 服务管理**：

```bash
# 查看服务状态
systemctl status systemd-udevd

# 重启服务
sudo systemctl restart systemd-udevd

# 查看服务日志
journalctl -u systemd-udevd -f
```

#### 3.1.3 工作流程

完整的设备管理流程如下：

1. **硬件检测**：内核检测到硬件变化（插入、移除、状态改变）
2. **事件发送**：内核通过 netlink socket 发送 uevent 到用户空间
3. **事件接收**：**systemd-udevd** 接收 uevent，解析设备属性
4. **规则匹配**：根据规则文件（`/run/current-system/sw/lib/udev/rules.d/`（NixOS）或
   `/usr/lib/udev/rules.d/`（传统发行版）、`/etc/udev/rules.d/`）匹配设备
5. **动作执行**：执行匹配规则中定义的动作（`RUN` 脚本、设置 `OWNER`/`GROUP`/`MODE`、创建
   symlink、设置权限）
6. **systemd 集成**：通知 systemd，可能触发 device units

#### 3.1.4 配置示例

**基本规则示例**：

```ini
# /etc/udev/rules.d/90-mydevice.rules
SUBSYSTEM=="input", ATTRS{idVendor}=="abcd", ATTRS{idProduct}=="1234", MODE="660", GROUP="input", TAG+="uaccess"
```

**规则说明**：

- `SUBSYSTEM=="input"`：匹配输入设备子系统
- `ATTRS{idVendor}=="abcd"`：匹配厂商 ID
- `ATTRS{idProduct}=="1234"`：匹配产品 ID
- `MODE="660"`：设置设备权限为 660
- `GROUP="input"`：设置设备组为 input
- `TAG+="uaccess"`：添加 uaccess 标签，让 systemd-logind 接管设备权限

**高级规则示例**：

```ini
# /etc/udev/rules.d/99-custom-storage.rules
# 为特定 USB 存储设备创建符号链接
SUBSYSTEM=="block", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", SYMLINK+="myusb"

# 为特定网卡设置持久化名称
SUBSYSTEM=="net", ATTRS{address}=="aa:bb:cc:dd:ee:ff", NAME="eth0"

# 为特定设备运行自定义脚本
SUBSYSTEM=="usb", ATTRS{idVendor}=="abcd", RUN+="/usr/local/bin/my-device-handler.sh"
```

`TAG+="uaccess"` 是现代桌面用来让 systemd-logind 接管设备权限与 session ACL（由 logind 配
置），确保只有当前活动会话能访问输入、音频、GPU 等设备。

### 3.2 设备权限与 ACL

现代 systemd + logind 使用 udev tag `uaccess` 或 `seat` 标签来由 logind 把设备 ACL 授予当
前的登录 session。具体流程：

- **systemd-udevd** 创建 `/dev/input/eventX` 并打上 `TAG+="uaccess"`.
- **systemd-logind** 对应的 PAM/session 系统会把该设备的 ACL 授予当前会话的用户，这样运行
  在会话内的 Wayland compositor 与其子进程可以访问设备。

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

场景：插入外接键盘后，Wayland 会话收不到键盘事件（键盘无效）

排查步骤：

1. 检查 **systemd-udevd** 服务状态：

   ```bash
   systemctl status systemd-udevd
   ```

2. 在主机上用 `udevadm monitor` 插入键盘，观察是否有 udev 事件被触发：

   ```bash
   sudo udevadm monitor --udev
   ```

3. 检查 `/dev/input/` 是否生成新节点：`ls -l /dev/input/by-id`。
4. 用 `udevadm info -a -n /dev/input/eventX` 查看该设备的属性，确认 `TAG` 是否包含
   `uaccess` 或 `seat`.
5. 使用 `loginctl seat-status seat0` 看设备是否分配给当前会话。若没有，可能是 PAM/session
   未正确建立或 udev 规则没有打上 tag。
6. 检查 **systemd-udevd** 的日志：

   ```bash
   journalctl -b -u systemd-udevd
   journalctl -k | grep -i udev
   ```

7. 临时解决：用 `chmod`/`chown` 修改设备权限验证是否恢复（不建议长期采用）：

   ```bash
   sudo chown root:input /dev/input/eventX
   sudo chmod 660 /dev/input/eventX
   ```

8. 永久修复：在 `/etc/udev/rules.d/` 中添加规则确保 `TAG+="uaccess"` 或正确的OWNER/GROUP。
   然后 `udevadm control --reload-rules && sudo udevadm trigger`。

**注意**：NixOS 下直接编辑 `/etc/udev/rules.d` 可能是临时的（Nix 管理的文件会被系统重建覆
盖），正确做法是在 `configuration.nix` 中配置 `services.udev.extraRules` 或把规则放在
`environment.etc` 并由 Nix 管理。

**配置文件路径**：

- `/etc/udev/rules.d/`：系统管理员自定义规则（优先级最高）
- `/run/current-system/sw/lib/udev/rules.d/`（NixOS）或 `/usr/lib/udev/rules.d/`（传统发行
  版）：软件包提供的默认规则

---

## 4. D-Bus 系统总线 - 应用间通信的主要通道

D-Bus 是 Linux 系统中主流的进程间通信（IPC）机制，旨在解决不同进程（尤其是桌面应用、系统服
务）间的高效、安全通信问题，广泛用于 GNOME、KDE 等桌面环境及系统服务管理（如 systemd）。它
本质是 "消息总线"，通过中心化的 "总线守护进程" 实现多进程间的消息路由。名字虽然有点奇怪，
功能倒是挺实在的。

### 4.1 D-Bus 项目背景

D-Bus 并非 systemd 社区的项目，而是 **freedesktop.org** 的独立项目。D-Bus 在 systemd 出现
之前就已经存在，是 Linux 桌面环境标准化进程间通信的重要基础设施。

**D-Bus 与 systemd 的关系**：

- **独立项目**：D-Bus 由 freedesktop.org 维护，有自己的发布周期和开发团队
- **深度集成**：systemd 将 D-Bus 作为核心依赖，深度集成到其架构中
- **服务管理**：systemd 负责启动和管理 D-Bus 守护进程（dbus-daemon）
- **统一接口**：systemd 通过 D-Bus 提供统一的服务管理接口
  - systemd 本身就是一个 D-Bus 服务，我们在使用 `systemctl` 命令与 systemd 交互时，实际上
    就是 D-Bus 与 `org.freedesktop.systemd1` 通信。

### 4.2 关键概念

D-Bus 通过 「对象 - 接口」 模型封装功能，以下结合 `systemd1` 与 `logind1` 的真实定义，对应
核心概念：

| 概念              | 定义与作用                                      | 示例（systemd1/logind1）                                                                                                                   |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 总线（Bus）       | 消息传输的 「高速公路」，分系统 / 会话两类      | 系统总线 `/var/run/dbus/system_bus_socket`（`systemd1`/`logind1` 唯一使用的总线）                                                          |
| 服务名（Name）    | 服务端在总线上的 「身份证」，唯一可请求         | `org.freedesktop.systemd1`（`systemd` 服务名）、`org.freedesktop.login1`（`logind` 服务名）                                                |
| 对象（Object）    | 服务端功能的 「实例载体」，有唯一路径           | `/org/freedesktop/systemd1`（`systemd1` 根对象）、`/org/freedesktop/login1`（`logind1` 根对象）                                            |
| 接口（Interface） | 定义对象的 「功能契约」（方法、信号、属性）     | `org.freedesktop.systemd1.Manager`（`systemd1` 核心接口）、`org.freedesktop.login1.Manager`（`logind1` 核心接口）                          |
| 方法（Method）    | 客户端可主动调用的 「同步功能」（有请求有返回） | `systemd1` 的 `StartUnit`（启动系统单元，如 `nginx.service`）、`logind1` 的 `ListSessions`（查询所有活跃用户会话）                         |
| 信号（Signal）    | 服务端主动发送的 「异步通知」（无返回）         | `systemd1` 的 `UnitActiveChanged`（单元状态变化，如 `nginx` 从 `inactive` 变为 `active`）、`logind1` 的 `SessionNew`（新用户登录创建会话） |
| 属性（Property）  | 对象的 「状态数据」，支持读取 / 写入            | `systemd1` 的 `ActiveUnits`（所有活跃系统单元列表）、`logind1` 的 `CanPowerOff`（当前系统是否允许关机，布尔值）                            |

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

### 4.3 系统总线与会话总线

| 总线类型                | 作用场景                 | 典型用途                                                                             | 运行用户     |
| ----------------------- | ------------------------ | ------------------------------------------------------------------------------------ | ------------ |
| 系统总线（System Bus）  | 系统级服务通信           | `systemd1` 单元管理（启动 / 停止服务）、`logind1` 用户会话 / 电源控制（关机 / 重启） | root（特权） |
| 会话总线（Session Bus） | 单个用户会话内的应用通信 | 桌面应用交互（如窗口切换、通知）                                                     | 当前登录用户 |

### 4.4 D-Bus 的三类角色

1. **总线守护进程（dbus-daemon）**

   架构的 「中枢」，每个总线对应一个守护进程，核心职责：

   - 管理进程的连接（如验证 `普通用户` 是否有权调用 `logind1` 的 `PowerOff` 方法）；

   - 路由消息（将客户端请求的 「启动 `nginx` 服务」 转发给 `systemd1`）；

   - 维护服务注册表（记录 `org.freedesktop.login1` 与 `logind` 进程的映射关系）。

1. **服务端（Service）**

   提供功能的进程（如 `systemd` 进程、`logind` 进程），核心操作：

   - 向总线注册 「服务名」（`systemd1` 注册 `org.freedesktop.systemd1`，`logind1` 注册
     `org.freedesktop.login1`，均为唯一标识）；

   - 暴露 「对象」 和 「接口」（如 `systemd1` 暴露 `/org/freedesktop/systemd1` 对象与
     `org.freedesktop.systemd1.Manager` 接口），供客户端调用。

1. **客户端（Client）**

   调用服务的进程（如 `systemctl` 命令、桌面电源菜单），核心操作：

   - 连接系统总线后，通过服务名（如 `org.freedesktop.login1`）找到 `logind` 服务；

   - 调用服务端暴露的方法（如通过 `logind1` 的 `ListSessions` 查询当前用户会话），或订阅信
     号（如监听 `systemd1` 的 `UnitActiveChanged` 单元状态变化）。

### 4.5 常见操作示例

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

### 4.6 调试与监控命令

```bash
# 看 systemctl 与 systemd 的完整交互（method-call + signal）
sudo busctl monitor --system | grep 'org.freedesktop.systemd1'
# 或者使用 --match 过滤，但这需要提前知道 interface 的全名
sudo busctl monitor --match='interface=org.freedesktop.systemd1.Manager'

# 跟 busctl monitor 功能几乎完全一致，也可通过 match rule 过滤
sudo dbus-monitor --system "interface='org.freedesktop.systemd1.Manager'"

# gdbus 只监听 signals，只能用来调试「服务有没有正确发出 signal」
sudo gdbus monitor --system -d org.freedesktop.systemd1.Manager
```

### 4.7 D-Bus 的权限管控

#### 4.7.1 D-Bus 的原生权限管控机制

D-Bus 本身具备多层权限管控能力，从总线接入、消息路由到敏感操作授权，形成了系统级的基础安全
保障，核心机制包括：

1. **总线配置文件（静态规则管控）**

   通过 XML 配置文件定义细粒度访问规则，实现对 「谁能访问哪些服务 / 方法」 的静态限制。例
   如：

   - 系统总线的服务级规则（如 `/etc/dbus-1/system.d/org.freedesktop.login1.conf`）可限制普
     通用户调用 `org.freedesktop.login1.Manager.PowerOff`（关机方法）；

   - 全局规则（如 `/etc/dbus-1/system.conf`）可限定仅 `root` 或 `dbus` 组用户访问
     `org.freedesktop.systemd1`（systemd 服务）的核心接口。

     规则遵循 「`deny` 优先级高于 `allow`、服务级规则高于全局规则」 的逻辑，从总线层面直接
     拦截未授权请求。

1. **PolicyKit（动态授权管控）**

   针对静态规则无法覆盖的动态场景（如普通用户临时需要执行敏感操作），D-Bus 集成
   PolicyKit（现称 `polkit`）实现动态授权。系统服务（如 `logind1`、`systemd1`）会在
   `/run/current-system/sw/share/polkit-1/actions/`（NixOS 中）或
   `/run/current-system/sw/share/polkit-1/actions/`（NixOS）或
   `/usr/share/polkit-1/actions/`（传统发行版中）定义 "可授权动作"，例如
   `org.freedesktop.login1.power-off`（对应 `logind1` 的关机方法）：

   - 普通用户调用时，会触发认证流程（如输入管理员密码），认证通过后临时获得授权；

   - 活跃控制台用户可直接授权，无需额外验证，兼顾安全性与易用性。

1. **连接层基础隔离**

   D-Bus 总线套接字（如系统总线 `/var/run/dbus/system_bus_socket`）默认仅开放 `root` 和
   `dbus` 组用户的读写权限，普通进程需通过 `dbus-daemon` 认证后才能建立连接。同时，每个连
   接会被分配唯一 ID（如 `:1.42`），并与进程的 PID/UID/GID 绑定，防止身份伪造与未授权接
   入。

#### 4.7.2 Flatpak 对 D-Bus 权限的细粒度管控

在现代 Linux 桌面中，若需将商业软件等非信任应用运行在沙箱中，同时保障 「必要 D-Bus 交互不
中断、越权访问被阻断」，Flatpak 采用 **「底层沙箱隔离 + 上层代理过滤」** 的双层方案 —— 其
中 `bubblewrap` 是 Flatpak 依赖的底层沙箱工具，负责环境隔离；`xdg-dbus-proxy` 是上层过滤组
件，负责 D-Bus 细粒度管控，两者协同实现完整安全隔离：

##### 4.7.2.1 底层基础隔离：bubblewrap 的 "socket 隐藏与代理挂载"

Flatpak 以 `bubblewrap`（简称 bwrap）为底层沙箱基础，利用其 `bind mount` 和
`user namespace` 能力完成环境初始化，核心目标是切断沙箱应用与宿主 D-Bus 总线的直接联系：

- **隐藏宿主 socket**：`bubblewrap` 会屏蔽宿主的 D-Bus 总线套接字（如不将
  `/var/run/dbus/system_bus_socket` 挂载进沙箱），避免应用绕过管控直接访问宿主总线；

- **挂载代理 socket**：同时，`bubblewrap` 会将 `xdg-dbus-proxy` 在宿主侧预先创建的 **私有
  代理 socket**，通过 `bind mount` 挂载到沙箱内的默认 D-Bus socket 路径（如沙箱内的
  `/var/run/dbus/system_bus_socket`）。

  此时沙箱应用感知到的 「D-Bus 总线」，实际是 `xdg-dbus-proxy` 提供的代理接口，无法直接接
  触宿主真实总线。

##### 4.7.2.2 上层规则过滤：xdg-dbus-proxy 的 "白名单校验"

`xdg-dbus-proxy` 作为 Flatpak 内置的 D-Bus 代理组件，会随沙箱应用启动，加载 Flatpak 根据应
用权限声明自动生成的过滤规则（粒度远细于 D-Bus 原生静态配置），例如：

```bash
--talk=org.freedesktop.portal.FileChooser  # 允许调用文件选择门户服务
--talk=org.freedesktop.Notifications       # 允许发送桌面通知
--deny=org.freedesktop.systemd1            # 拒绝访问 systemd 服务
--deny=org.freedesktop.login1.Manager.PowerOff  # 拒绝调用关机方法
```

这些规则可精确到 「服务名 + 接口 + 方法 + 对象路径」，弥补 D-Bus 原生配置在沙箱场景下 「动
态性不足、粒度较粗」 的局限。

##### 4.7.2.3 消息流转：代理的 "校验 - 转发" 逻辑

沙箱应用无需修改代码，会默认连接沙箱内的 「代理 socket」，所有 D-Bus 消息（方法调用、信号
订阅）均需经过 `xdg-dbus-proxy` 的校验：

- 若目标服务 / 方法在白名单内（如 `org.freedesktop.portal.FileChooser.OpenFile`），代理会
  将消息转发至宿主 D-Bus 总线，并把返回结果回传应用；

- 若目标不在白名单内（如 `org.freedesktop.login1.Manager.PowerOff`），代理直接返回
  `AccessDenied` 错误，不向宿主总线转发任何消息，彻底阻断越权访问。

---

## 总结

本文深入探讨了 systemd 核心功能及其生态系统，从服务管理到各个专门化组件：

1. **systemd 核心功能**：作为 PID 1 的服务管理器，专注于服务管理、依赖关系管理、资源控制和
   系统状态管理
2. **systemd 生态系统服务**：包括日志管理（journald）、内存管理（oomd）、DNS 解析
   （resolved）、时间同步（timesyncd）、设备管理（udevd）等
3. **设备管理**：udev 规则和设备权限分配，通过 systemd-udevd 确保硬件设备正确识别和访问
4. **D-Bus 系统总线**：进程间通信机制，支持系统服务和桌面应用的交互

虽然 systemd 的争议一直存在，但不可否认的是，它确实让系统管理变得更加统一和高效。掌握了这
些组件的使用方法，你在面对各种系统问题时就不会那么手足无措了。

下一篇文章我们会聊聊桌面会话和图形渲染，看看用户登录后系统是如何把漂亮的桌面呈现给你的。

---
