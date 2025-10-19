---
title: "Linux 桌面系统故障排查指南（五） - 网络"
subtitle: ""
description: ""
date: 2025-10-19T10:21:33+08:00
lastmod: 2025-10-19T10:21:33+08:00
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

## 网络连接与管理

网络连接是现代桌面的基础功能，涉及硬件驱动、固件加载、网络管理和 DNS 解析等多个环节。

本文将从网卡驱动开始，经过内核网络栈，到达应用层，了解 Linux 网络系统的完整架构，包括如何
配置网络连接，如何设置防火墙规则，以及如何诊断各种网络问题。

---

## 前言

网络连接是现代桌面的基础功能，涉及硬件驱动、固件加载、网络管理和 DNS 解析等多个环节。网络
故障是最常见的桌面问题之一，理解其工作原理有助于快速定位和解决连接问题。

### 1.1 网络架构概览

现代 Linux 桌面大多使用 systemd-networkd 配合 iwd 进行网络管理，形成完整的网络解决方案。

> 虽然目前仍有部分系统默认使用 NetworkManager 管理网络，用 wpa_supplicant 管理 WiFi, 但这
> 已经不够「现代」了（逃

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

### 1.2 网络连接流程

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

### 1.3 IPv4 / IPv6 双栈配置

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

### 1.4 网络故障排查

**连接问题诊断流程**：

1. **硬件层面**：

```bash
# 检查接口存在
ip link show

# 查看驱动加载
dmesg | grep -i firmware
lspci | grep -i network
```

1. **链路层面**：

```bash
# 有线：检查链路状态
ethtool eth0

# 无线：扫描网络
iw dev wlan0 scan | grep SSID
```

2. **网络配置**：

```bash
# DHCP 状态
journalctl -u systemd-networkd

# IP 配置检查
ip addr show dev eth0

# 路由表
ip route
```

3. **DNS 解析**：

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

## 防火墙与网络安全

### 2.1 nftables 防火墙配置

nftables 是现代 Linux 的防火墙解决方案，它提供比 iptables 更简洁的语法和更好的性能。

**基本概念**：

- **表（Table）**：包含链和规则的容器
- **链（Chain）**：规则的有序列表
- **规则（Rule）**：匹配条件和动作
- **集合（Set）**：用于批量匹配的地址或端口列表

nftables 的四表五链、规则等概念跟 iptables 是完全一致的，这一部分可以参考我之前的文章
[iptables 及 docker 容器网络分析](/posts/iptables-and-container-networks/), 这里不再赘述。

**NixOS 配置示例**：

```nix
# configuration.nix
networking.nftables = {
  enable = true;
  ruleset = ''
    # 定义表
    table inet filter {
      # 定义链
      chain input {
        type filter hook input priority 0; policy drop;

        # 允许回环接口
        if lo accept

        # 允许已建立的连接
        ct state established,related accept

        # 允许 SSH
        tcp dport 22 accept

        # 允许 HTTP/HTTPS
        tcp dport {80, 443} accept

        # 允许 DNS
        udp dport 53 accept
        tcp dport 53 accept

        # 允许 DHCP
        udp dport 67 accept
        udp dport 68 accept

        # 允许 ICMP
        icmp type {echo-request, echo-reply, destination-unreachable} accept
        ip6 nexthdr icmpv6 icmpv6 type {echo-request, echo-reply, destination-unreachable} accept
      }

      chain forward {
        type filter hook forward priority 0; policy drop;
      }

      chain output {
        type filter hook output priority 0; policy accept;
      }
    }
  '';
};
```

**常用 nftables 命令**：

```bash
# 查看当前规则
nft list ruleset

# 查看特定表
nft list table inet filter

# 临时添加规则
nft add rule inet filter input tcp dport 8080 accept

# 删除规则
nft delete rule inet filter input handle <handle>

# 清空表
nft flush table inet filter
```

### 2.2 网络地址转换（NAT）

**端口转发配置**：

```nix
networking.nftables.ruleset = ''
  table inet nat {
    chain prerouting {
      type nat hook prerouting priority 0;

      # 端口转发：将外部 8080 端口转发到内网 192.168.1.100:80
      tcp dport 8080 dnat to 192.168.1.100:80
    }

    chain postrouting {
      type nat hook postrouting priority 100;

      # 源地址转换（SNAT）
      oifname "eth0" masquerade
    }
  }
'';
```

## 虚拟网络技术

### 3.1 VPN 连接管理

**WireGuard 配置**：

```nix
# configuration.nix
networking.wireguard.interfaces = {
  wg0 = {
    ips = [ "10.0.0.2/24" ];
    privateKeyFile = "/etc/wireguard/private.key";
    peers = [
      {
        publicKey = "peer-public-key";
        allowedIPs = [ "0.0.0.0/0" ];
        endpoint = "vpn.example.com:51820";
        persistentKeepalive = 25;
      }
    ];
  };
};
```

### 3.2 虚拟网络接口

**TUN/TAP 接口**：

```bash
# 创建 TUN 接口
ip tuntap add dev tun0 mode tun
ip addr add 10.0.0.1/24 dev tun0
ip link set tun0 up

# 创建 TAP 接口
ip tuntap add dev tap0 mode tap
ip addr add 192.168.100.1/24 dev tap0
ip link set tap0 up
```

**桥接网络**：

```bash
# 创建网桥
ip link add name br0 type bridge
ip link set dev br0 up

# 添加接口到网桥
ip link set dev eth1 master br0
ip link set dev tap0 master br0

# 配置网桥 IP
ip addr add 192.168.1.1/24 dev br0
```

### 3.3 容器网络

**Docker 网络管理**：

```bash
# 查看网络
docker network ls

# 创建自定义网络
docker network create --driver bridge --subnet=172.20.0.0/16 mynetwork

# 连接容器到网络
docker network connect mynetwork container_name

# 查看网络详情
docker network inspect mynetwork
```

**Podman 网络配置**：

```bash
# 创建网络
podman network create mynet

# 运行容器
podman run --network mynet -d nginx

# 查看网络
podman network ls
```

## 网络性能优化

### 4.1 网络参数调优

**内核网络参数**：

```nix
# configuration.nix
boot.kernel.sysctl = {
  # TCP 缓冲区大小
  "net.core.rmem_max" = 134217728;
  "net.core.wmem_max" = 134217728;
  "net.ipv4.tcp_rmem" = "4096 87380 134217728";
  "net.ipv4.tcp_wmem" = "4096 65536 134217728";

  # TCP 拥塞控制
  "net.ipv4.tcp_congestion_control" = "bbr";

  # 连接跟踪
  "net.netfilter.nf_conntrack_max" = 1048576;
  "net.netfilter.nf_conntrack_tcp_timeout_established" = 3600;

  # 网络队列
  "net.core.netdev_max_backlog" = 5000;
  "net.core.netdev_budget" = 600;
};
```

网络参数调优：

TCP 缓冲区优化：

`net.core.rmem_max = 134217728` 设置 TCP 接收缓冲区的最大值为 128MB。更大的接收缓冲区可以
处理突发的高流量，减少丢包，提高网络吞吐量，特别适合高带宽网络环境，适用于高带宽、高延迟网
络，如光纤网络、VPN 连接。

`net.core.wmem_max = 134217728` 设置 TCP 发送缓冲区的最大值为 128MB。更大的发送缓冲区可以
缓存更多待发送数据，提高发送效率，减少发送阻塞，提高网络传输效率，适用于大文件传输、流媒体
上传、高并发网络应用。

`net.ipv4.tcp_rmem = "4096 87380 134217728"` 设置 TCP 接收缓冲区的初始值、默认值和最大值。
参数说明：初始值 4KB，默认值 87KB，最大值 128MB。动态调整接收缓冲区大小，根据网络条件自动
优化，在低延迟和高吞吐量之间自动平衡。

`net.ipv4.tcp_wmem = "4096 65536 134217728"` 设置 TCP 发送缓冲区的初始值、默认值和最大值。
参数说明：初始值 4KB，默认值 64KB，最大值 128MB。动态调整发送缓冲区大小，适应不同的网络负
载，在内存使用和网络性能之间找到最佳平衡点。

TCP 拥塞控制优化：

`net.ipv4.tcp_congestion_control = "bbr"` 使用 BBR（Bottleneck Bandwidth and RTT）拥塞控制
算法。BBR 是 Google 开发的现代拥塞控制算法，基于带宽和延迟测量，在高带宽、高延迟网络环境下
性能更好，减少延迟和丢包，适用于现代网络环境，特别是高带宽网络和长距离连接。

连接跟踪优化：

`net.netfilter.nf_conntrack_max = 1048576` 增加连接跟踪表大小到 100 万条记录。支持更多并发
网络连接，避免连接跟踪表溢出，支持高并发网络应用，如 P2P 下载、多用户服务，适用于服务器环
境、高并发网络应用。

`net.netfilter.nf_conntrack_tcp_timeout_established = 3600` 设置已建立连接的超时时间为 1
小时。延长连接跟踪时间，减少连接重建的频率，减少连接重建开销，提高长连接应用的性能，适用于
长连接应用，如数据库连接、WebSocket 连接。

网络队列优化：

`net.core.netdev_max_backlog = 5000` 增加网络设备接收队列大小到 5000 个数据包。更大的接收
队列可以处理突发流量，减少丢包，提高网络处理能力，减少因队列满而导致的丢包，适用于高流量网
络环境，如服务器、网络设备。

`net.core.netdev_budget = 600` 增加每次网络处理的数据包数量到 600 个。提高网络处理效率，减
少处理开销，提高网络吞吐量，减少 CPU 使用率，适用于高负载网络环境，需要优化网络处理性能。

优化效果评估：通过缓冲区优化，网络吞吐量可提升 20-50%；BBR 拥塞控制算法可显著减少网络延
迟；连接跟踪优化支持更多并发连接；队列优化减少丢包，提高网络稳定性。

### 4.2 网络监控与分析

**网络流量监控**：

```bash
# 实时流量监控
iftop -i eth0

# 网络连接监控
netstat -tuln
ss -tuln

# 网络统计
cat /proc/net/dev
cat /proc/net/snmp

# 带宽测试
iperf3 -s  # 服务器端
iperf3 -c server_ip  # 客户端
```

**网络延迟分析**：

```bash
# ping 测试
ping -c 10 8.8.8.8

# 路由跟踪
traceroute 8.8.8.8
mtr 8.8.8.8

# 网络质量测试
qperf server_ip tcp_bw tcp_lat
```

### 4.3 网络故障诊断

**连接问题排查**：

```bash
# 检查网络接口状态
ip link show
ip addr show

# 检查路由表
ip route show
ip route get 8.8.8.8

# 检查 ARP 表
ip neigh show

# 检查网络统计
cat /proc/net/dev
cat /proc/net/snmp
```

**DNS 问题排查**：

```bash
# 测试 DNS 解析
dig @8.8.8.8 example.com
nslookup example.com

# 检查 DNS 配置
resolvectl status
cat /etc/resolv.conf

# 测试 DNS 性能
dig @8.8.8.8 example.com +stats
```

**防火墙问题排查**：

```bash
# 检查防火墙规则
nft list ruleset
iptables -L -v -n

# 测试端口连通性
telnet server_ip port
nc -zv server_ip port

# 检查连接跟踪
cat /proc/net/nf_conntrack
```

## 高级网络配置

### 5.1 多网卡绑定

**网卡绑定配置**：

```nix
# configuration.nix
networking.bonds = {
  bond0 = {
    interfaces = [ "eth0" "eth1" ];
    driverOptions = {
      mode = "802.3ad";
      lacp_rate = "fast";
      xmit_hash_policy = "layer3+4";
    };
  };
};

networking.interfaces.bond0.ipv4.addresses = [{
  address = "192.168.1.100";
  prefixLength = 24;
}];
```

### 5.2 VLAN 配置

**VLAN 网络配置**：

```nix
# configuration.nix
networking.vlans = {
  vlan100 = { id = 100; interface = "eth0"; };
  vlan200 = { id = 200; interface = "eth0"; };
};

networking.interfaces.vlan100.ipv4.addresses = [{
  address = "192.168.100.1";
  prefixLength = 24;
}];

networking.interfaces.vlan200.ipv4.addresses = [{
  address = "192.168.200.1";
  prefixLength = 24;
}];
```

### 5.3 网络命名空间

**创建网络命名空间**：

```bash
# 创建命名空间
ip netns add ns1
ip netns add ns2

# 创建 veth 对
ip link add veth1 type veth peer name veth2

# 将接口移到命名空间
ip link set veth1 netns ns1
ip link set veth2 netns ns2

# 配置命名空间内的网络
ip netns exec ns1 ip addr add 10.0.1.1/24 dev veth1
ip netns exec ns1 ip link set veth1 up
ip netns exec ns2 ip addr add 10.0.1.2/24 dev veth2
ip netns exec ns2 ip link set veth2 up

# 测试连通性
ip netns exec ns1 ping 10.0.1.2
```

## 总结

网络是计算机科学中最复杂的技术之一，数据在互联网中的流动造就了现代信息社会，现代 AI 的发展
也与现代网络中产生的超大规模数据密不可分。

本文只是对 Linux 网络的一个简单介绍，下一篇文章我们会聊聊系统关机和故障排查，看看系统是如
何优雅地关机的，以及遇到问题时该如何处理。

## 快速参考

### 常用网络管理命令

```bash
# 网络接口管理
ip link show                           # 查看网络接口
ip addr show                          # 查看 IP 地址
ip route show                         # 查看路由表
ip neigh show                         # 查看 ARP 表

# 网络连接管理
ss -tuln                              # 查看网络连接
netstat -tuln                         # 传统网络连接查看
lsof -i                               # 查看端口占用

# 网络测试
ping -c 4 8.8.8.8                    # ping 测试
traceroute 8.8.8.8                   # 路由跟踪
mtr 8.8.8.8                          # 网络质量测试
```

### 常用防火墙命令

```bash
# nftables 管理
nft list ruleset                      # 查看所有规则
nft list table inet filter            # 查看特定表
nft add rule inet filter input tcp dport 8080 accept  # 添加规则
nft delete rule inet filter input handle <handle>     # 删除规则

# iptables 管理（传统）
iptables -L -v -n                     # 查看规则
iptables -A INPUT -p tcp --dport 22 -j ACCEPT  # 添加规则
iptables -D INPUT -p tcp --dport 22 -j ACCEPT  # 删除规则
```

### 常用网络诊断命令

```bash
# DNS 解析测试
dig @8.8.8.8 example.com              # DNS 查询
nslookup example.com                  # 传统 DNS 查询
resolvectl query example.com          # systemd-resolved 查询

# 网络监控
iftop -i eth0                         # 实时流量监控
tcpdump -i eth0                       # 网络包捕获
wireshark                             # 图形化网络分析

# 带宽测试
iperf3 -s                             # 启动 iperf3 服务器
iperf3 -c server_ip                   # 客户端测试
```

### 重要配置文件位置

```bash
# 网络配置
/etc/systemd/network/                 # systemd-networkd 配置
/etc/nftables.conf                    # nftables 配置
/etc/resolv.conf                      # DNS 配置

# 网络服务
/etc/systemd/system/                  # systemd 服务配置
/etc/wireguard/                       # WireGuard 配置
/etc/openvpn/                         # OpenVPN 配置

# 网络状态
/proc/net/dev                         # 网络接口统计
/proc/net/snmp                        # 网络协议统计
/proc/net/nf_conntrack                # 连接跟踪表
```

---
