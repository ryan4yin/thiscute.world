---
title: "Linux 桌面系统（八）：网络如何到达应用"
subtitle: ""
description:
  "从网卡、carrier、地址和策略路由，到 DNS、TUN
  与应用连接，理解桌面网络各层的职责，以及恢复后网络异常的配置案例。"
date: 2025-10-19T10:21:33+08:00
lastmod: 2026-09-16T23:55:00+08:00
draft: false
authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"
tags: ["Linux", "Desktop", "Network", "systemd", "DNS", "Firewall"]
categories: ["tech"]
series: ["Linux 桌面系统"]
series_weight: 8
aliases: ["/posts/linux-desktop-5-network/"]
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

桌面上的网络图标能告诉我们连接到了哪个网络，但应用访问一个网站，还需要地址、路由、名称解析，以及对端响应。后文会分析一个恢复后的网络问题：物理链路发生变化后，networkd 重新配置接口，进而影响 VPN/TUN 的路由规则。要读懂这个案例，先得分清谁负责哪一段。

本文按接口、链路、地址、路由、DNS 和应用连接的顺序展开。这是理解依赖关系的顺序；实际访问域名时，应用通常先做名称解析，再连接返回的地址，DNS 查询本身也要经过网络。前面的[系统基础篇](/posts/linux-desktop-system-foundations/)解释了设备与服务如何出现，这里从内核已经注册网络接口开始。

## 网卡出现以后，还缺什么

> Linux 内核把网络设备表示为接口，并通过 netlink 向用户空间暴露接口、地址、路由和链路状态。网络管理程序在这些接口上建立配置，应用最终仍通过内核的 socket 与路由系统通信。接口模型见
> [netdevice 文档](https://docs.kernel.org/networking/netdevices.html)。

### 接口状态与 carrier

物理网卡由驱动接入内核，用户空间通过 netlink 读取接口信息。接口有名字，并不意味着已经能传数据：管理员启用接口对应
`UP` 标志，驱动报告底层链路可用对应
`LOWER_UP`。carrier 可以理解为底层连接状态，有线网卡通常与物理链路有关，无线连接还涉及关联和认证。

`ip` 输出里的运行状态也需要结合接口类型理解。例如 `UNKNOWN`
表示没有提供明确的运行状态，不能单凭这个词判定接口坏了；虚拟接口与物理网卡的表现也未必相同。内核的
[Operational States](https://docs.kernel.org/networking/operstates.html)
文档解释了这些标志及其关系。

Wi-Fi 还需要用户空间组件完成连接管理，例如 iwd。本文采用 networkd 管地址与路由、iwd 管无线连接的组合，但这不是唯一分工：iwd 本身也能启用内置的 IP 配置与 DHCP 客户端。因此，组合多个服务时，要确认地址配置究竟由谁负责，避免两个组件同时管理同一个接口的同一项状态。见
[iwd 手册](https://man.archlinux.org/man/iwd.8.en)与
[EnableNetworkConfiguration 选项](https://man.archlinux.org/man/iwd.config.5.en)。

### networkd 怎样找到要管理的接口

systemd-networkd 读取 `.network` 文件中的 `[Match]`
条件，为匹配的接口配置地址和路由。多个文件都能匹配时，按文件名字母数字顺序采用第一个匹配项，后面的文件不会继续叠加成另一套网络配置。接口名只是匹配条件之一，也可以按其他设备属性匹配。见
[systemd.network 上游手册源码](https://github.com/systemd/systemd/blob/main/man/systemd.network.xml)。

因此，更换主板、网卡或插槽后，接口名可能变化，原有 `.network`
文件也可能不再匹配。此时应该比较 `ip link` 显示的接口与 `[Match]`
条件，不能因为 networkd 服务仍在运行，就认定新接口已经被接管。

在 NixOS 中，这部分通过声明式配置完成：`systemd.network.enable`
启用集成，`systemd.network.networks` 生成 `.network` 文件，`matchConfig` 和
`networkConfig` 分别对应其中的匹配与网络配置部分。`networking.useNetworkd` 还会把部分传统
`networking` 选项翻译给 networkd，不能把两种入口当成完全相同的开关。见
[NixOS networkd 文档](https://wiki.nixos.org/wiki/Systemd/networkd)与
[NixOS 26.05 模块实现](https://github.com/NixOS/nixpkgs/blob/nixos-26.05/nixos/modules/system/boot/networkd.nix)。

Arch 使用同一套上游机制，通常直接维护 `/etc/systemd/network/` 中的文件；`.link`
的设备属性处理交给 udev，`.netdev` 描述虚拟设备，`.network`
配置地址与路由。[Arch 提供的 networkd 手册](https://man.archlinux.org/man/systemd-networkd.service.8.en)列出了这些职责。使用 NetworkManager 的桌面则由它管理所接管的连接，两者可以各管不同接口；应先确认实际管理者，再解释配置入口。

## 有地址之后，包往哪里走

接口可以使用静态地址，也可以通过动态配置取得地址。IPv4 常见 DHCP；IPv6 则需要区分链路本地地址、路由器通告（RA）、无状态地址自动配置（SLAAC）和 DHCPv6。RA 可以提供前缀及默认路由信息，DHCPv6 与接收 RA 也有各自的配置控制。看到一个 IPv6 地址，尤其只是链路本地地址，并不足以说明已有通往互联网的路由。相关选项见
[systemd.network 的 DHCP 与 IPv6AcceptRA 部分](https://github.com/systemd/systemd/blob/main/man/systemd.network.xml)。

内核为发出的包选择路径时，需要区分两种规则。策略路由规则决定按什么条件查哪张路由表；表里的路由项再决定下一跳和出口。策略规则按优先级数字从小到大处理，可以匹配源地址、目的地址或包的 mark 等条件；查表没找到可用结果时，后续规则仍可能继续参与。见
[ip-rule 手册](https://man7.org/linux/man-pages/man8/ip-rule.8.html)。

在路由表中，目的前缀越具体，匹配范围越小；默认路由的前缀长度是零，用于没有更具体匹配的目的地址。同等条件下，metric 较低的路由通常更优先。`ip route`
默认展示的 main 表只是其中一张表，VPN 可能另外建立路由表并通过策略规则选中它。见
[ip-route 手册](https://man7.org/linux/man-pages/man8/ip-route.8.html)。

因此，「默认路由还在」只能回答一部分问题。还需要知道是哪张表里的默认路由、哪些流量会查它，以及对应出口是否可用。IPv4 与 IPv6 的规则和路由也要分别检查，不能用其中一套的结果代替另一套。

## DNS 向哪台服务器查询

应用拿到域名后，需要先得到可用于连接的地址。采用 systemd-resolved 时，应用可以经 glibc 的 NSS 配置接入它，也可以使用它提供的原生接口或本地 DNS
stub。`/etc/resolv.conf`
在不同集成方式下可能指向本地 stub，也可能列出上游服务器；只看到这个文件，无法完整还原所有应用的解析路径。见
[systemd-resolved 的接口与 resolv.conf 说明](https://github.com/systemd/systemd/blob/main/man/systemd-resolved.service.xml)。

resolved 还会按域名选择 DNS 服务器。假设某个 VPN 接口声明了
`~corp.example`，这个仅用于路由的域会让匹配的查询优先交给相关 DNS；`~.`
可以匹配所有域名，但更具体的域仍更优先。多个接口具有相同的最佳匹配域时，查询可以发往这些接口的 DNS。

这里的 DNS 路由与内核的 IP 路由是两次不同的选择：前者选「问哪台 DNS」，后者决定「怎样到达这台 DNS」。resolved 的
`DefaultRoute` 属性也属于 DNS 查询选择，不能直接当成内核默认路由。完整选择规则见
[resolved 的查询路由说明](https://github.com/systemd/systemd/blob/main/man/systemd-resolved.service.xml)。

由此可以推导出两种不同现象：域名查询交给了不该使用的 DNS，可能得到错误结果或查询失败；DNS 选对了，但通往它的隧道路由丢失，同样会失败。换一个公共 DNS 还可能让内部域名失去原本的解析路径。先确认查询去向，才知道该检查解析策略还是网络路径。

## TUN、VPN 与防火墙怎样参与

### 虚拟接口仍然需要出口

TUN 把三层 IP 包交给用户空间程序，TAP 则传递二层以太网帧。程序通过 `/dev/net/tun`
创建或接入相应设备，从文件描述符读写数据。TUN 本身不负责加密，也不自动提供一个远端出口；后续怎样封装、代理或转发，由使用它的软件决定。见
[Linux TUN/TAP 文档](https://docs.kernel.org/networking/tuntap.html)。

以下是用户空间 TUN 程序的一种典型路径，实际拦截方式由程序配置决定：

```text
应用产生 IP 流量
    ↓ 策略规则与路由表选择 TUN
TUN → 用户空间代理/VPN 程序
    ↓ 程序建立对外连接，再次经过路由选择
物理出口 → 上游网络
```

第二次路由选择需要避免把程序自己的对外连接再次送回同一条 TUN 路径。程序可能使用标记、额外路由或绑定出口等方式区分流量；具体应以其实现为准。即使 TUN 接口仍在，程序自身的对外路径也可能已经失效。

VPN 是用途，TUN 是接口机制，两者不能一一对应。例如 [WireGuard](https://www.wireguard.com/)
在 Linux 上有内核实现，并不要求所有数据先交给用户空间 TUN 进程。需要部署 WireGuard 时，可以继续读[单独的 WireGuard 文章](/posts/wireguard-on-linux/)；这里关心的是隧道与底层出口的依赖。

### 防火墙在数据路径上检查什么

nftables 通过挂在 Netfilter hook 上的基础链处理数据包。发给本机进程的入站流量经过
`input`，本机产生的流量经过 `output`，由本机转发的流量经过
`forward`。表用于组织规则，普通链需要被其他链引用才会处理流量，链名本身不会让它自动挂到某个位置。见
[nftables 链与 hook 文档](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains)。

还要区分「某条规则 accept」与「整个路径放行」。多个基础链可以位于同一个 hook，一个链接受数据包之后，后面的链仍能丢弃它。连接跟踪则让规则能区分已有连接的回包与新的入站连接；访问网站并不等于要在本机开放一个网站服务端口。规则遍历及
`ct state` 的解释见
[nftables 官方手册](https://netfilter.org/projects/nftables/manpage.html)。

排查时要把方向、协议、接口和已有连接状态对应起来。单看端口号，或者只看一条接受规则，都不足以证明防火墙放行了当前流量。直接清空规则还会同时移除过滤、转发或代理依赖的配置，使观察对象发生变化。

## 一次恢复事件怎样影响到应用

一台使用 r8169 网卡、networkd 和 TUN/VPN 策略路由的机器曾遇到这样的问题：从 S3 恢复时网卡短暂丢失 carrier，networkd 随后重配置接口，静态地址、默认路由以及其他程序创建的策略规则受到影响。TUN 程序失去原出口后，网络没有随链路一起恢复。

对应配置摘录如下，完整上下文见[作者的 NixOS 配置](https://github.com/ryan4yin/nix-config/commit/77e31bd4cbe7b7dd7a66fd8484b5446a33e626f1)：

```nix
systemd.network.config.networkConfig.ManageForeignRoutingPolicyRules = false;

systemd.network.networks."10-lan".networkConfig = {
  IgnoreCarrierLoss = "10s";
};
```

两项配置分别处理不同环节：

- `ManageForeignRoutingPolicyRules = false`：让 networkd 保留并非由 `.network`
  声明的策略规则。当前上游默认值为 `yes`，规则协议为 `kernel`
  的情况另有例外。这里改变的是规则的管理边界，不是恢复某张路由表的命令。见
  [networkd.conf](https://github.com/systemd/systemd/blob/main/man/networkd.conf.xml)。
- `IgnoreCarrierLoss = "10s"`：为短暂 carrier 丢失留出等待时间；若链路在这段时间内恢复，networkd 忽略这次丢失，避免立即撤下静态和动态配置。超过等待时间仍未恢复则不能靠它继续保留配置。见
  [IgnoreCarrierLoss 的上游定义](https://github.com/systemd/systemd/blob/main/man/systemd.network.xml)。

两个改动分别处理「谁有权清理规则」与「多快响应链路丢失」。十秒只是这台机器采用的等待时间，不是通用答案。保留外部规则也意味着需要由创建它们的组件负责清理失效规则；延后处理 carrier 丢失，则会推迟响应真正的断链。

遇到类似问题时，需要记录同一次恢复事件前后的完整状态：carrier 何时变化，networkd 是否重配置，地址与路由是否被撤下，VPN/TUN 的策略规则是否变化，程序最终选择了哪个出口。只观察最后一个「网页打不开」的结果，无法分辨这些环节。

## 应用自身还会影响连接方式

网络服务把接口与路由准备好之后，应用通过 socket 与内核通信。IPv4 和 IPv6 使用不同地址族，流式 socket 与数据报 socket 也有不同语义。能创建 socket 只是取得通信端点，连接与数据交换还在后面。见
[socket 接口手册](https://man7.org/linux/man-pages/man2/socket.2.html)。

应用也可能先连接代理。例如 curl 会读取相应的代理环境变量，并用 `NO_PROXY`
决定哪些目标绕过代理；这些是应用行为，不能推导成所有桌面软件都会采用同一设置。见
[curl 的代理环境变量文档](https://everything.curl.dev/usingcurl/proxies/env.html)。比较两个应用时，应该先确认它们连接的是同一个目标地址，还是一个直连、另一个经过代理。

双栈的选择也由客户端参与。Happy
Eyeballs 允许客户端错开、并行尝试不同候选地址，尽量避免某个地址族不可用时长时间等待。因此，不能把地址列表的第一项或一份地址排序配置理解为所有应用最终都会选中的连接。[RFC 8305](https://www.rfc-editor.org/rfc/rfc8305.html)描述了这种策略。

结合前面的依赖关系，「只有一个应用不能联网」就有了具体的检查方向：它采用哪种解析入口、是否连接代理、选中了哪个地址族，所发流量又会匹配哪条策略规则。系统当前有网络连接，只是这些检查的起点。

## 在自己的机器上观察网络状态

下面的命令已在笔者的 NixOS
PC 上完成只读验证，不发起第三方连通性测试。输出可能包含接口名、MAC/IP 地址、内部域名与 VPN 规则，因此不摘录完整结果；分享时也应删去这些信息。先确认自己所在的网络命名空间与实际管理组件。

先观察接口和地址：

```console
ip -brief link
ip -brief address
```

把同一个接口的运行状态、`UP`/`LOWER_UP`
标志与地址对应起来。这里看不到 Wi-Fi 密码，也无需读取连接配置中的认证材料。`-brief`
只是压缩输出，并不脱敏，选项见
[ip 手册](https://man7.org/linux/man-pages/man8/ip.8.html)。

接口存在但没有 carrier 时，再向下看驱动和链路：

```console
ip -details link show dev <接口名>
ethtool -i <有线接口名>
ethtool <有线接口名>
```

`ethtool -i` 关注 driver、version 和 firmware-version，普通 `ethtool` 关注
`Link detected`、协商速率和双工模式。Wi-Fi 则应使用 `iw dev`、`iw dev <接口名> link`
查看关联状态，不要把有线 carrier 的判断照搬过去。驱动已绑定、链路已建立，仍不代表网络管理器已给接口配置地址。

接着确认到底是谁管理接口。systemd-networkd 环境可用：

```console
networkctl list
networkctl status <接口名>
systemctl status systemd-networkd.service --no-pager
```

NetworkManager 环境则用 `nmcli device status` 和
`nmcli connection show --active`。同一接口不应由两套管理器同时争用；服务 active 也不能证明目标接口被它接管，要看接口状态中的 setup/managed 信息。

再看规则与路由表，分别保留 IPv4 和 IPv6 的视角：

```console
ip -4 rule show
ip -6 rule show
ip -4 route show table all
ip -6 route show table all
ip route get 1.1.1.1
```

最后一条只让内核计算到这个字面 IPv4 地址的路径，不向它发包。观察出口、源地址及下一跳，并与前面的规则、表对应。它没有重现某个应用的所有条件，例如应用的 mark、绑定地址或其他网络命名空间，所以也不是「这个应用可联网」的证明。见
[ip route get](https://man7.org/linux/man-pages/man8/ip-route.8.html)。

若机器正在使用 systemd-resolved，可查看生效中的全局与各接口 DNS 设置：

```console
resolvectl status
```

留意 DNS 服务器归属、路由域和
`DefaultRoute`，判断预期的查询去向。这条命令展示配置状态，不证明一次真实解析成功，见
[resolvectl 手册](https://github.com/systemd/systemd/blob/main/man/resolvectl.xml)。

再做一次明确的解析请求，把“配置存在”和“查询得到结果”分开：

```console
$ resolvectl query localhost
localhost: 127.0.0.1 -- link: lo
           ::1       -- link: lo
-- Data from: synthetic
```

`localhost`
不依赖外部网络，适合确认 resolved 的查询接口可达；它不能验证上游 DNS。调查真实域名时，记录返回地址、使用的协议和接口，但不要公开内部域名或搜索域。随后用
`ip route get <返回地址>` 检查内核会选择哪条路径。

应用已经发起连接时，可以从 socket 反查它实际选了谁：

```console
ss -tpn
ss -upn
```

TCP 输出关注本地/远端地址、状态和进程，UDP 没有同样的连接状态语义。完整结果会暴露正在使用的服务与远端地址，应只摘取目标进程的一行。socket 建立成功证明的是传输层状态，不保证 TLS、HTTP 或应用协议成功。

已经安装 nft、具有读取规则权限且能妥善保管输出时，还可以查看规则集：

```console
nft list ruleset
```

先找基础链的 hook、优先级与默认策略，再沿引用关系看规则。缺少权限时停在这一步，不必为了练习修改权限或清空规则。

规则很多时，先从结构入手：

```console
nft list tables
nft list table inet <表名>
```

基础链会标出 `hook input`、`output`、`forward`
等位置以及 priority、policy。TUN/VPN 问题还要把虚拟接口和策略路由放在一起看：

```console
ip -details link show type tun
ip rule show
ip route show table all
```

TUN 接口为 `UP`
只说明虚拟设备状态，不说明流量已被规则导入、VPN 进程会转发，或外层连接仍然可用。整个观察过程都不需要 flush 规则、删除路由或重启网络服务。

网络会随着设备与电源状态继续变化。[下一篇](/posts/linux-desktop-power/)讨论挂起、恢复与关机时哪些状态被保留、哪些组件需要重新工作；涉及网络恢复时，可以回到这里对照接口、地址、规则和应用出口。
