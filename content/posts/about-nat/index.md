---
title: "关于 NAT 网关、NAT 类型提升、NAT 穿透以及虚拟网络"
date: 2022-05-09T00:59:00+08:00
draft: false

resources:
- name: "featured-image"
  src: "nat.webp"

tags: ["NAT", "网络", "内网穿透", "虚拟网络", "P2P"]
categories: ["技术"]
---

>本文还处于草稿阶段，暂时不建议阅读。

>个人笔记，不一定正确...

NAT，即 Network Address Translation，是 IPv4 网络中非常重要的一个功能，用于执行 IP 地址与端口的转换。

IPv4 的设计者没预料到因特网技术的发展会如此之快，在设计时只使用了 32bits 的地址空间，随着因特网的飞速发展，它很快就变得不够用了。
后来虽然设计了新的 IPv6 协议，但是它与 IPv4 不兼容，需要新的硬件设备以及各种网络程序支持，无法快速普及。

NAT 就是在 IPv6 普及前，临时解决 IPv4 地址空间不够用而开发的技术，有网友戏称 NAT 就是用来给 IPv4 续命的。它解决 IPv4 地址短缺问题的方法是：

- 每个家庭、组织、企业，在内部都使用通用的私有 IP 地址进行通讯。不同的家庭、组织、企业，都可以使用相同的私有 IP 地址段，不会互相影响
  - 路由器通过 DHCP 为局域网中的设备分配私有 IP 地址
  - 在局域网内部，路由器使用适用于局域网的路由算法进行数据路由。比如 OSPF.
- 在局域网与上层网络的交界处（路由器），使用 NAT 技术进行 IP/port 转换，使用户能正常访问上层网络。

在曾经 IPv4 地址还不是特别短缺的时候，普通家庭的网络架构通常是：「家庭局域网」=>「NAT 网关（家庭路由器）」=>「因特网」。

但是互联网主要发展于欧美，因此许多欧美的组织与机构在初期被分配了大量的 IPv4 资源，而后入场的中国分配到的 IPv4 地址就不太能匹配上我们的人口。
因此相比欧美，中国的 IPv4 地址是非常短缺的，即使使用上述这样的网络架构——也就是给每个家庭（或组织）分配一个 IPv4 地址——都有点捉襟见肘了。
于是中国电信等运营商不得不再加一层 NAT，让多个家庭共用同一个 IP 地址，这时网络架构会变成这样：「家庭局域网」=>「NAT 网关（家庭路由器）」=>「广域网（由 ISP 管理）」=>「NAT 网关」=>「因特网」。

不过总的来说，NAT 仍然是一项非常成功的技术，它成功帮 IPv4 续命了几十年，甚至到如今 2022 年，全球网络仍然是 IPv4 的天下。

## NAT 如何工作

NAT 的工作方式，使用图例描述是这样的：

{{< figure src="/images/about-nat/NAT-demo.webp" >}}

从外部网络看一个 NAT 网关（一个启用了 NAT 的路由器），它只是拥有一个 IPv4 地址的普通设备，所有从局域网发送到公网的流量，其 IP 地址都是这个路由器的 WAN IP 地址，在上图中，这个 IP 地址是 `138.76.29.7`.

本质上，NAT 网关隐藏了家庭网络的细节，从外部网络上看，整个家庭网络就像一台普通的网络设备。

NAT 网关会维护一个 NAT 翻译表，它负责记录 IP/port 的映射关系。

## NAT 的地址映射方式

### 1. 一对一 NAT

一对一 NAT，也被称为 Basic NAT，在 [RFC2663](https://datatracker.ietf.org/doc/html/rfc2663#section-4.0) 中被定义，在技术上比较简单，只利用网络层的信息，对 IP 地址进行转换。

简单的说，Basic NAT 要求每个内网 IP 都需要绑定一个唯一的外网 IP，才能连通外部网络。
通常路由器只有一个 IP，这种场景下 Basic NAT 只允许同时有一台内网主机访问外部网络。

Basic NAT 有两种类型：「静态 NAT」与「动态 NAT」。

现在的很多家庭路由器都自带一个被称为 DMZ 主机的功能，它是「Demilitarized Zone」的缩写，意为隔离区。
它允许将某一台内网主机设置为 DMZ 主机（或者叫隔离区主机，仅此主机可供外网访问），所有从外部进来的流量，都会被通过 Basic NAT 修改为对应的内网 IP 地址，然后直接发送到该主机。
路由器的这种 DMZ 技术就是「静态 NAT」，因为 DMZ 对应的内网 IP 需要手动配置，不会动态变化。

而「动态 NAT」则需要路由器维护一个公网 IP 地址池，内网服务器需要访问公网时，动态 NAT 就从地址池中拿出一个公网 IP 给它使用，用完再回收。
这种场景需要一个公网 IP 地址池，我就没接触过了，应用场景或许主要是某些数据中心。

Basic NAT 的好处是，它仅工作在 L3 网络层，网络层上的协议都可以正常使用（比如 P2P），不需要啥「内网穿透」技术。 

### 2. 一对多 NAT - NAPT

一对多 NAT，也被称为 NAPT（network address and port translation），同样在 [RFC2663](https://datatracker.ietf.org/doc/html/rfc2663#section-4.0) 中被定义。

**绝大多数的 NAT 网络都是 NAPT**，原因应该很好理解——一对一 NAT 的局限性太大，静态 NAT 需要手动配置，动态 NAT 的并发会话数也受公网 IP 的数量限制。

NAPT 通过同时利用 L3 的 IP 信息，以及 L4 传输层的端口信息，来为局域网设备提供透明的、配置方便的、支持超高并发连接的外部网络通信。

NAPT 的端口分配与转换，以及对外来流量的处理，有四种不同的方法，被称作四种不同的 NAPT 类型，下面逐一介绍。

>从这里开始，下文中的 NAT 特指 NAPT，如果涉及「一对一 NAT」会使用它的全名。

#### 1. Full-cone NAT

Full-cone NAT 的特点如下：

- 数据包流出：一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：任意主机发送到 eAddr:ePort 的数据包，都能通过 NAT 到达 iAddr:iPort.
  - 也就是不对外部进来的数据做任何限制，全部放行。
  - cone 圆锥，个人理解是一个比喻，任意发送进来的数据（多），都能通过 NAT 到达这个内部地址（一），就像一个圆锥。

允许任意主机发送到 eAddr:ePort 的数据到达内部地址是很危险的行为，因为内部主机不一定配置了合适的安全策略。
因此 **Full-cone NAT 比较少见**，就算路由器等 NAT 设备支持 Full-cone NAT，通常也不会是默认选项。我们会在会面更详细地介绍它。

#### 2. Address-Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部主机（nAddr:any），发送到 eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - **跟 Full-cone NAT 的区别在于，它限制了外部主机的 IP 地址。只有主动连接过的主机，才能发送数据到 NAT 内部。这提升了一些安全性**。

#### 3. Port-Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部主机（nAddr），通过一个指定的端口 hPort 发送到 eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - **与 Address-Restricted cone NAT 的区别在于，它同时限制了外部主机的 IP 与端口，可以说是更进一步地提升了安全性。**

#### 4. Symmetric NAT

- 数据包流出：每个内部地址（iAddr:iPort）都映射到一个唯一的外部地址（eAddr:ePort）。同一个内部地址与不同的外部地址的通信，会使用不同的 NAT 端口。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部地址（nAddr:nPort），可以给这个内部地址回消息。

**对称 NAT 是最安全的一种 NAT 结构，限制最为严格，应该也是应用最广泛的 NAT 结构**。
但是它导致所有的 TCP 连接都只能由从内部主动发起，外部发起的 TCP 连接请求会直接被 NAT 拒绝，因此它也是 P2P 玩家最头疼的一种 NAT 类型。
解决方案是通过 UDP 迂回实现连接的建立，我们会在后面讨论这个问题。

## 各 NAT 类型的应用场景

Linux 的网络栈中，可通过 `iptables/netfilter` 的 `SNAT/MASQUERADE` 实现 NAT 网关能力，这种方式实现的是一个 Symmetric NAT.

也就是说绝大多数基于 Linux 实现的家庭局域网、Docker 虚拟网络、Kubernetes 虚拟网络、云服务的虚拟网络，都是 Symmetric NAT.

只有一些有 Full-cone NAT 需求的网吧、ISP 的 LSN(Large Scale NAT) 网关等组织，会使用非 Linux 内核的企业级路由器提供 Full-cone NAT 能力，这些设备可能是基于 FPGA 等专用芯片设计的。

## NAT 类型提升

天下苦 Symmetric NAT 久矣，尤其是各种 P2P 玩家，如 NAS 玩家、P2P 游戏玩家。
那么到底有哪些技术手段可以用来提升 NAT 类型，将 Symmetric NAT 提升到「部分受限 NAT」或者「Full-cone NAT」呢？这里就来聊一聊。

>这里讨论的前提是，你的网络只有单层 NAT，如果外部还存在公寓 NAT、ISP 广域网 NAT，那下面介绍的 NAT 提升技术实际上就没啥意义了。

#### 1. 「DMZ 主机」或者「定向 DNAT 转发」

最简单的方法是 DMZ 主机功能，前面已经介绍过了，DMZ 可以直接给内网服务器绑定路由器的外部 IP，从该 IP 进来的所有流量都会直接被发送给这台内网服务器。
被指定的 DMZ 主机的网络特征，将完全符合 Full-cone NAT 的定义，因此这项技术可以将 DMZ 主机的 NAT 类型从 Symmetric NAT 提升到 Full-cone NAT（实际上比 Full-cone NAT 还要宽松，因为 DMZ 完全不限制端口，仅工作在 L3 网络层）

在 Linux 上实现类似 DMZ 的功能，只需要两行 iptables 命令，这可以称作「定向 DNAT 转发」：

```shell
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE # 普通的SNAT
iptables -t nat -A PREROUTING -i eth0 -j DNAT --to-destination 192.168.1.3 # 将入站流量DNAT转发到内网主机192.168.1.3
```

这两项技术的缺点是只能将一台主机提供给外网访问，而且将整台主机开放到公网实际上是很危险的，如果不懂网络**很容易被黑客入侵**。

#### 2. 静态端口转发

退一步，可以直接用静态端口转发功能，就是在路由器上手动设置某个端口号的所有 TCP/UDP 流量，都直接 NAT 转发到到内网的指定地址。

「静态端口转发」设置好后，对应的主机地址也将符合 Full-cone NAT 的定义，缺点就是端口转发规则都得手动配置。

绝大多数路由器都支持这项功能，NAS 发烧友们想玩 P2P 下载分享，基本都是这么搞的。

#### 3. UPnP 动态端口转发

>最流行的 UPnP 实现是 <https://github.com/miniupnp/miniupnp>

静态端口转发对用户的技术要求较高，我作为一个网络小白，希望有一个傻瓜式的开关能让我愉快地玩耍 Xbox/PS5 联机游戏，该怎么办呢？
你需要的只是在路由器上启用 UPnP(Universal Plug and Play) 协议，启用它后，内网游戏设备就可以通过 UPnP 向路由器动态申请一个端口号供其使用，UPnP 会自动配置对应的端口转发规则。
**现在新出的路由器基本都支持 UPnP 功能，它是最简单有效的 NAT 提升方式**。

UPnP 解决了「静态端口转发」需要手动配置的问题，在启用了 UPnP 后，对所有支持 UPnP 的内网程序而言，NAT 类型将提升到 Full-cone NAT.

## NAT 穿透 - NAT Traversal

在常见的联机游戏、BitTorrent 文件共享协议、P2P 聊天等点对点通讯场景中，客户端通常都运行在家庭网络中，隔着一层 Symmetric NAT（路由器），在不使用前面提到的 DMZ/UPnP 等 NAT 类型提升技术的前提下，客户端之间要建立 P2P 连接，就需要借助「NAT 穿越」技术。

NAT 穿透，也被称作「NAT 打洞」，需要突破几个关键的壁垒。一个完整的 NAT 穿透方案，需要包含如下功能：

- A 跟 B 需要知道对方的公网 IP 以及监听的端口号
  - 解决方法：需要一个中介来介绍双方认识（交换 IP/port）
- NAT 连通性测试，检测出双方中间网络的类型
- 针对不同的 NAT 类型，存在哪些穿透手段？以何种顺序进行穿透尝试？

### NAT 穿透方案原理

NAT 穿越可以使用 UDP/TCP 两种 L4 协议，但是 TCP 面向连接的特性使它在这个场景中限制性更大，因此各种 NAT 穿透协议通常都基于 UDP 实现。

这里首先以 UDP 为例介绍如何穿透各种 NAT 类型，最后再介绍下为什么 TCP 面向连接的特性使它在 NAT 穿透场景中应用受限。

#### 1. A 与 B 在同一局域网中

这是最简单的情况，最佳方案是直接走内网通讯，不经过 NAT.

第二个方案是，这两个同一局域网内的客户端不走内网，仍然通过 NAT 通讯。这种通讯方式被称作「回环 NAT(Loopback NAT)」或者「发夹 NAT(Hairpin NAT)」。
对于不支持「回环 NAT」的网关设备而言，这样的通讯尝试将会失败！
目前大多数路由器都不支持回环 NAT 技术。对于这种尝试，通常建议直接使用内网地址连接普通 P2P 连接。

#### 2. A 与 B 分别在不同的局域网中

这样实际上 A 与 B 中间就隔了两个 NAT 网关，这是最普遍的一种情况。连接建立流程如下：

- 首先，A 跟 B 两个程序启动时，需要把自己的内外网 IP 及端口信息上报到一台中介服务器 S
- 现在假设 A 想要跟 B 建立一个 P2P 连接，首先他们需要从 S 获得对方的 ID
- A 将 B 的 ID 发送给中介服务器 S，请求与 B 建立 P2P 连接
- 中介服务器将 B 的内外网 IP 及端口信息发送给 A，同时将 A 的网络信息发送给 B
- A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`
  - 这肯定会失败，但是会在 A 的 NAT 网关上留下记录：A 曾经请求过这个地址，那之后这个地址发到 A 的 NAT 网关的流量就可以进来了。
- B 尝试请求 A 的公网地址 `A_public_ip:A_public_port`
  - 同样这肯定也会失败，但是会在 B 的 NAT 网关上流量记录：B 曾经请求过这个地址，那之后这个地址发到 B 的 NAT 网关的流量就可以进来了
- 中间的两层 NAT 网关均形成 NAT 穿透记录，**穿透完成**。
- 现在 A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`，由于 B 的 NAT 已有记录，流量顺利通过 NAT 到达程序 B
- B 发送给 A 的数据也同样，可以顺利到达 A

#### 3. A 与 B 之间隔着三层以上的 NAT

这种情况较为常见的有：

- ISP 为了节约使用公网 IP，给用户分配了个广域网 IP，中间就多了个广域网 NAT
- 大城市的各种租房公寓通常只会从 ISP 购买一两根宽带，二次分销给整栋楼的租客共用，这就造成中间多了一层公寓的 NAT

这是最复杂的一种情况。

TBD 待完善

#### 4. 特殊穿透方案 - 反向代理

反向代理是兼容性最佳，但是性能最差的方案，因为这个方案下，所有的 P2P 连接都需要经过反向代理，在使用人数众多时这会给反向代理造成很大的压力。

因此这个方案通常是用于兜底的。

### NAT 穿透协议标准 - STUN/TURN/ICE

前面介绍了 NAT 穿透的原理，这里介绍下相关的协议标准。

目前有如下几个 NAT 穿透协议标准：

- [RFC5389 - Simple Traversal of UDP Through NATs (STUN)](https://datatracker.ietf.org/doc/html/rfc5389)
  - STUN 是个轻量级的协议，是基于 UDP 的 NAT 穿透方案。它允许应用程序发现它们与公共互联网之间存在的 NAT 及防火墙类型。它也可以让应用程序确定 NAT 分配给它们的公网 IP 地址和端口号。
  - RFC5389 优先使用 UDP 尝试穿透，在失败的情况下会继续使用 TCP 进行尝试
- [RFC5766 - Traversal Using Relays around NAT (TURN)](https://tools.ietf.org/html/rfc5766)
  - TURN 在 STUN 协议之上添加了一个中继，以确保在无法实现 NAT 穿透的情况下，可以 fallback 到直接使用中继服务器进行通信。
  - 这个中继的原理类似反向代理，单纯负责数据的转发
  - 在美国有一项数据表示在进行 P2P 穿越的时候，穿越成功的概率为 70%，但是在国内这个成功率 50% 可能都到不了。因此就有必要使用 TURN 协议，这样才能保证在穿越失败的情况下，用户仍然能正常通信。
- [RFC8445 - Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445)
  - 一个 NAT 穿透的协商协议，它统一了 STUN 与 TURN 两种协议，会尝试遍历所有可能的连接方案。
  - ICE 的工作流程
    - 首先收集终端双方所有的通路（因为终端可能包含多个网卡，必定包含多个通路）
    - 按一定优先级，对所有通路进行连通性检测，连接建立则 ICE 结束工作
  - 优先级顺序：
    - 内网直接通讯，这肯定是优先级最高的嘛
    - 尝试使用 STUN 协议进行 NAT 穿越
    - 走 TURN 中继服务器进行代理通讯

## 虚拟网络、Overlay 与 Underlay

虚拟网络就是在物理网络之上，构建的逻辑网络，也被称作 overlay 网络。
比如 AWS VPC、Docker 容器网络、QEMU 的默认网络，都是虚拟网络。

而 underlay 网络，则是指承载 overlay 网络的底层网络。
我个人理解，它是一个相对的概念，物理网络一定是 underlay 网络，但是虚拟网络之上如果还承载了其他虚拟网络（套娃），那它相对上层网络而言，也是一个 underlay 网络。

overlay 本质上就是一种隧道技术，将原生态的二层数据帧报文进行封装后通过隧道进行传输。常见的 overlay 网络协议主要是 vxlan 以及新一代的 geneve，它俩都是使用 UDP 包来封装链路层的以太网帧。

vxlan 在 2014 年标准化，而 geneve 在 2020 年底才通过草案阶段，目前尚未形成最终标准。但是目前 linux/cilium 都已经支持了 geneve.

geneve 相对 vxlan 最大的变化，是它更灵活——它的 header 长度是可变的。

目前所有 overlay 的跨主机容器网络方案，几乎都是基于 vxlan 实现的（例外：cilium 也支持 geneve）。

顺带再提一嘴，cilium/calico/kube-ovn 等 overlay 容器网络，都是 SDN 软件定义网络。

### 相关工具

有一些专门用于跨网搭建私有虚拟网络的工具，由于家庭网络设备前面通常都有至少一层 NAT（家庭路由器），因此这些工具都重度依赖 NAT 穿透技术。
如果 NAT 层数太多无法穿透，它们会 fallback 到代理模式，也就是由一台公网服务器进行流量中继，但是这会对中继服务器造成很大压力，延迟跟带宽通常都会差很多。

如下是两个比较流行的 VPN 搭建工具：

- [zerotier](https://github.com/zerotier/ZeroTierOne): 在 P2P 网络之上搭建的 SDN overlay 网络，使用自定义协议。
- [tailscales](https://github.com/tailscale/tailscale): 基于 wireguard 协议快速搭建私有虚拟网络 VPN


## 拓展知识

### Symmetric NAT 允许的最大并发 TCP 连接数是多少？

TCP 并发连接数受许多参数的限制，以 Linux 服务器为例，默认参数无法满足需要，通常都会手动修改它的参数，放宽文件描述符限制以及 TCP 连接队列、缓存相关的限制。

单纯从网络协议层面分析，对于一个仅有一个公网 IP 的 Symmetric NAT 网关，它与某个外部站点 `http://x.x.x.x:xx` 要建立连接。
考虑到 TCP 连接的定义实际上是一个四元组 `(srcIP, srcPort, dstIP, dstPort)`，其中就只有 NAT 网关自己的 `srcPort` 是唯一的变量了，而端口号是一个 16bits 数字，取值范围为 0 - 65535。
此外低于 1024 的数字是操作系统的保留端口，因此 NAT 一般只会使用 1024-65535 这个区间的端口号，也就是说这个 NAT 网关最多只能与该站点建立 64512 个连接。

那么对于不同的协议 NAT 是如何处理的呢？NAT 肯定可以通过协议特征区分不同协议的流量，因此不同协议通过 NAT 建立的并发连接不会相互影响。

对于家庭网络而言 64512 个连接已经完全够用了，但是对于数据中心或者云上的 VPC 而言，就不一定够用了。
举个例子，在 [AWS NAT 网关的文档](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)中就有提到，AWS NAT 网关最高支持与每个不同的地址建立 55000 个并发连接。destination 的 IP 地址、端口号、(TCP/UDP/ICMP) 任一个发生改变，都可以再建立其他 55000 个并发连接。
如果超过这个限制，就会发生「ErrorPortAllocation」错误。如果在 AWS 上遇到这个错误，那就说明你们的云上网络规划有问题了。

当然除了端口限制外，受限于 NAT 硬件、以太网协议以及其他影响，NAT 网关肯定还有包处理速率、带宽的限制，这个就略过不提了。

### AWS VPC 与 NAT

AWS VPC(virtual private cloud) 是一个逻辑隔离的虚拟私有网络，云服务架构的最佳实践之一就是通过 VPC 搭建云上私有网络，提升网络安全性。

AWS VPC 提供两种网关类型：

- NAT 网关
  - 最高支持与每个不同的地址建立 55000 个并发连接
  - 支持三种协议：TCP, UDP, ICMP
  - 支持 IPv4 与 IPv6 两种 IP 协议
  - 支持 5 Gbps 带宽，可自动扩展到 45 Gbps
    - 可通过划分子网并在多个子网中添加 NAT 网关的方式，获得超过 45Gbps 的带宽
  - 每个 NAT 网关只能绑定一个 IP
    - 可通过划分子网并在多个子网中添加 NAT 网关的方式获得多个 IP
  - 可达到 100w packets 每秒的处理速度，并能自动扩展到 400w packets 每秒
    - 同样，需要更高的处理速度，请添加更多 NAT 网关
  - 按处理数据量收费
  - 默认路由到 NAT 子网，被称为「私有子网」（或者没默认路由，那就是无法访问公网的私有子网），连接只能由内网程序主动发起。
  - NAT 网关为流量执行「**Symmetric NAT**」
- IGW 因特网网关
  - IGW 是一个抽象概念，它不会限制 VPC 的总带宽、处理能力
  - IGW 为绑定了公网 IP 地址的实例，执行「**一对一 NAT**」
  - 默认路由到 IGW 的子网，被称为「公有子网」

## 参考

- [从DNAT到netfilter内核子系统，浅谈Linux的Full Cone NAT实现](https://blog.chionlab.moe/2018/02/09/full-cone-nat-with-linux/)
- [Network address translation - wikipedia](https://en.wikipedia.org/wiki/Network_address_translation)
- [P2P学习（一）NAT的四种类型以及类型探测](https://www.cnblogs.com/ssyfj/p/14791064.html)
- [P2P学习（二）P2P中的NAT穿越(打洞)方案详解](https://www.cnblogs.com/ssyfj/p/14791980.html)
- [TCP点对点穿透探索--失败](https://developer.aliyun.com/article/243173)

