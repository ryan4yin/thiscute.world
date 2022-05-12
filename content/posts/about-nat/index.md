---
title: "关于 NAT 网关、NAT 类型提升、NAT 穿越以及虚拟网络"
date: 2022-05-09T00:59:00+08:00
draft: false

resources:
- name: "featured-image"
  src: "nat.webp"

tags: ["NAT", "网络", "NAT 穿越", "内网穿透", "虚拟网络", "P2P"]
categories: ["技术"]
---

>本文还处于草稿阶段，暂时不建议阅读。

>个人笔记，不一定正确...

NAT，即 Network Address Translation，是 IPv4 网络中非常重要的一个功能，用于执行 IP 地址与端口的转换。

IPv4 的设计者没预料到因特网技术的发展会如此之快，在设计时只使用了 32bits 的地址空间，随着因特网的飞速发展，它很快就变得不够用了。
后来虽然设计了新的 IPv6 协议，但是它与 IPv4 不兼容，需要新的硬件设备以及各种网络程序支持，无法快速普及。

NAT 就是在 IPv6 普及前，临时解决 IPv4 地址空间不够用而开发的技术，通俗地讲 NAT 就是用来给 IPv4 续命的。它解决 IPv4 地址短缺问题的方法是：

- 每个家庭、组织、企业，在内部都使用局域网通讯，不占用公网 IPv4 资源
- 在局域网与上层网络的交界处（路由器），使用 NAT 技术进行 IP/port 转换，使用户能正常访问上层网络

在曾经 IPv4 地址还不是特别短缺的时候，普通家庭的网络架构通常是：「家庭局域网」=>「NAT 网关（家庭路由器）」=>「因特网」。

但是互联网主要发展于欧美，因此许多欧美的组织与机构在初期被分配了大量的 IPv4 资源，而后入场的中国分配到的 IPv4 地址就不太能匹配上我们的人口。
因此相比欧美，中国的 IPv4 地址是非常短缺的，即使使用上述这样的网络架构——也就是给每个家庭（或组织）分配一个 IPv4 地址——都有点捉襟见肘了。
于是中国电信等运营商不得不再加一层 NAT，让多个家庭共用同一个 IP 地址，这时网络架构会变成这样：「家庭局域网」=>「NAT 网关（家庭路由器）」=>「广域网（由 ISP 管理）」=>「NAT 网关」=>「因特网」。

总的来说，NAT 是一项非常成功的技术，它成功帮 IPv4 续命了几十年，甚至到如今 2022 年，全球网络仍然是 IPv4 的天下。

## NAT 如何工作

NAT 的工作方式，使用图例描述是这样的：

{{< figure src="/images/about-nat/NAT-demo.webp" title="NAT 示例">}}

从外部网络看一个 NAT 网关（一个启用了 NAT 的路由器），它只是拥有一个 IPv4 地址的普通设备，所有从局域网发送到公网的流量，其 IP 地址都是这个路由器的 WAN IP 地址，在上图中，这个 IP 地址是 `138.76.29.7`.

本质上，NAT 网关隐藏了家庭网络的细节，从外部网络上看，整个家庭网络就像一台普通的网络设备。

下面我们会学习到，上述这个 NAT 工作方式实际上是 NAPT，它同时使用 L3/L4 的信息进行地址转换工作。

## NAT 的地址映射方式

NAT 的具体实现有许多的变种，不存在统一的规范，但是大体上能分为两种模型：「一对一 NAT」与「一对多 NAT」，下面分别进行介绍。

### 1. 一对一 NAT

一对一 NAT，这种类型的 NAT 在 [RFC2663](https://datatracker.ietf.org/doc/html/rfc2663) 中被称为  Basic NAT。
它在技术上比较简单，只利用网络层的信息，对 IP 地址进行转换。

简单的说，Basic NAT 要求每个内网 IP 都需要绑定一个唯一的公网 IP，才能连通外部网络。

其**主要应用场景是，公网用户需要访问到内网主机**。

Basic NAT 有三种类型：「**静态 NAT**」、「**动态 NAT**」以及「**NAT Server**」。

现在的很多家庭路由器都自带一个被称为 DMZ 主机的功能，它是「Demilitarized Zone」的缩写，意为隔离区。
它允许将某一台内网主机设置为 DMZ 主机（或者叫隔离区主机，仅此主机可供外网访问），所有从外部进来的流量，都会被通过 Basic NAT 修改为对应的内网 IP 地址，然后直接发送到该主机。
路由器的这种 DMZ 技术就是「静态 NAT」，因为 DMZ 主机对应的内网 IP 需要手动配置，不会动态变化。

{{< figure src="/images/about-nat/dmz-host-topology.webp" title="DMZ 主机拓扑结构" >}}

而「**动态 NAT**」则需要一个公网 IP 地址池，每次用户需要访问公网时，动态 NAT 会给它分配一个动态公网 IP 并自动配置相应的 NAT 规则，使用完再回收。

第三种是「**NAT Server**」，云服务商提供的「**公网 IP**」就是通过「**NAT Server**」实现的，在云服务器中使用 `ip addr ls` 查看你会发现，该主机上实际只配了局域网 IP 地址，但是它却能正常使用公网 IP 通信，原因就是云服务商在「**NAT Server**」上为这些服务器配置了 IP 转发规则。
为一台云服务器绑定一个公网 IP，实际上就是请求「**NAT Server**」从公网 IP 地址池中取出一个，并配置对应的 NAT 规则到这台云服务器的局域网 IP。

示例如下，其中的 Internet Gateway 实际上就是个一对一 NAT Server：

{{< figure src="/images/about-nat/aws-vpc-nat-internet-gateway.webp" title="AWS VPC 中的 NAT 网关以及 Internet 网关">}}

>云服务 VPC 中的公有子网，实际上就是一个 DMZ(Demilitarized Zone) 隔离区，是不安全的。而私有子网则是安全区，公网无法直接访问到其中的主机。

而「动态 NAT」则需要路由器维护一个**公网 IP 地址池**，内网服务器需要访问公网时，动态 NAT 就从地址池中拿出一个公网 IP 给它使用，用完再回收。
这种场景需要一个公网 IP 地址池，每当内部有服务需要请求外网时，就动态地为它分配一个公网 IP 地址，使用完再回收。

Basic NAT 的好处是，它仅工作在 L3 网络层，网络层上的协议都可以正常使用（比如 P2P），不需要啥「内网穿越」技术。 

### 2. 一对多 NAT - NAPT

一对多 NAT，也被称为 NAPT（network address and port translation），同样在 [RFC2663](https://datatracker.ietf.org/doc/html/rfc2663#section-4.0) 中被定义。Easy IP 是 NAPT 的一个特殊形式。

**NAPT 的主要应用场景是，内网用户需要访问到公网主机**。绝大多数的家庭网络、办公网络都是 NAPT 类型的。
原因应该很好理解——家庭网络或办公网络都包含许多联网设备，但是这类网络通常只有一个或数个公网 IP，使用一对一 NAT 的话公网 IP 显然是不够用的，所以需要使用一对多 NAT.

NAPT 通过同时利用 L3 的 IP 信息，以及 L4 传输层的端口信息，来为局域网设备提供透明的、配置方便的、支持超高并发连接的外部网络通信，示意图如下：

{{< figure src="/images/about-nat/napt.webp" >}}

NAPT 的端口分配与转换规则（**Mapping Behavior**）以及对外来流量的过滤规则（**Filtering Behavior**）都存在许多不同的实现，没有统一的规范与标准。

#### RFC3489 定义的 NAT 类型（四种）

在 [RFC3489](https://datatracker.ietf.org/doc/html/rfc3489#section-5) 中将 NAPT 分为四种类型，这也是应用最为广泛的 NAT 分类方法，如下图：

{{< figure src="/images/about-nat/nat-types-defined-in-stun.webp" >}}

下面我们逐一介绍这四种不同的 NAPT 类型。

>从这里开始，下文中的 NAT 特指 NAPT，如果涉及「一对一 NAT」会使用它的全名。

##### 1. Full-cone NAT

Full-cone NAT 的特点如下：

- 数据包流出：一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：任意主机发送到 eAddr:ePort 的数据包，都能通过 NAT 到达 iAddr:iPort.
  - 也就是不对外部进来的数据做任何限制，全部放行。
  - cone 圆锥，个人理解是一个比喻，任意发送进来的数据（多），都能通过 NAT 到达这个内部地址（一），就像一个圆锥。

允许任意主机发送到 eAddr:ePort 的数据到达内部地址是很危险的行为，因为内部主机不一定配置了合适的安全策略。
因此 **Full-cone NAT 比较少见**，就算路由器等 NAT 设备支持 Full-cone NAT，通常也不会是默认选项。我们会在后面更详细地介绍它。

##### 2. Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部主机（nAddr:any），发送到 eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - 跟 Full-cone NAT 的区别在于，它**限制了外部主机的 IP 地址**。只有主动连接过的主机，才能发送数据到 NAT 内部。这**提升了一些安全性**。

##### 3. Port-Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部程序（nAddr:nPort），发送到 eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - 与 Address-Restricted cone NAT 的区别在于，它**同时限制了外部主机的 IP 与端口**，可以说是更**进一步地提升了安全性。**

##### 4. Symmetric NAT

- 数据包流出：每个内部地址（iAddr:iPort）都映射到一个唯一的外部地址（eAddr:ePort）。同一个内部地址与不同的外部地址的通信，会使用不同的 NAT 端口。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部地址（nAddr:nPort），可以给这个内部地址回消息。

**对称 NAT 是最安全的一种 NAT 结构，限制最为严格，应该也是应用最广泛的 NAT 结构**。
但是它导致所有的 TCP 连接都只能由从内部主动发起，外部发起的 TCP 连接请求会直接被 NAT 拒绝，因此它也是 P2P 玩家最头疼的一种 NAT 类型。
解决方案是通过 UDP 迂回实现连接的建立，我们会在后面讨论这个问题。

#### RFC5389 定义的 NAT 类型（九种）

RFC3489 的归类过于笼统，这导致即使在你已经明确了自己的 NAT 类型后，仍然无法通过查表明确自己能否进行 NAT 穿越，NAT 穿越能否成功仍然是一个概率事件...

于是后来，RFC3489 被废弃并由 [RFC5389](https://www.rfc-editor.org/rfc/rfc5389) 来替代，在 RFC5389 中，将 Mapping Behavior（映射规则）和 Filtering Behavior（过滤规则）分开来，定义了 3 种 Mapping Behavior（映射规则）和 3 种 Filtering Behavior（过滤规则），一共有 9 种组合。

TBD 待续

## NAT 的弊端

TBD

## 各 NAT 类型的应用场景

Linux 的网络栈中，可通过 `iptables/netfilter` 的 `SNAT/MASQUERADE` 实现 NAT 网关能力，这种方式实现的是一个 Symmetric NAT.

也就是说绝大多数基于 Linux 实现的家庭局域网、Docker 虚拟网络、Kubernetes 虚拟网络、云服务的虚拟网络，都是 Symmetric NAT.

只有一些有 Full-cone NAT 需求的网吧、ISP 的 LSN(Large Scale NAT) 网关等组织，会使用非 Linux 内核的企业级路由器提供 Full-cone NAT 能力，这些设备可能是基于 FPGA 等专用芯片设计的。

## NAT 穿越 - NAT Traversal

天下苦 NAT 久矣，尤其是各种 P2P 玩家，如 NAS 玩家、P2P 游戏玩家。
在常见的联机游戏、BitTorrent 文件共享协议、P2P 聊天等点对点通讯场景中，通讯双方客户端通常都运行在家庭局域网中，也就是说中间隔着两层家庭路由器的 NAT，路由器的默认配置都是安全优先的，存在很多安全限制，直接进行 P2P 通讯大概率会失败。

为了穿越这些 NAT 网关进行 P2P 通讯，就需要借助 NAT 穿越技术。

>这里讨论的前提是，你的网络只有单层 NAT，如果外部还存在公寓 NAT、ISP 广域网 NAT，那下面介绍的 NAT 提升技术实际上就没啥意义了。

### 1. 「DMZ 主机」或者「定向 DNAT 转发」

最简单的方法是 DMZ 主机功能，前面已经介绍过了，DMZ 可以直接给内网服务器绑定路由器的外部 IP，从该 IP 进来的所有流量都会直接被发送给这台内网服务器。
被指定的 DMZ 主机，其 NAT 类型将从 NAPT 变成一对一 NAT，而一对一 NAT 对 P2P 通讯而言是透明的，这样就可以愉快地玩耍了。

在 Linux 路由器上实现类似 DMZ 的功能，只需要两行 iptables 命令，这可以称作「定向 DNAT 转发」：

```shell
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE # 普通的SNAT
iptables -t nat -A PREROUTING -i eth0 -j DNAT --to-destination 192.168.1.3 # 将入站流量DNAT转发到内网主机192.168.1.3
```

这两项技术的缺点是只能将一台主机提供给外网访问，而且将整台主机开放到公网实际上是很危险的，如果不懂网络**很容易被黑客入侵**。

### 2. 静态端口转发

退一步，可以直接用静态端口转发功能，就是在路由器上手动设置某个端口号的所有 TCP/UDP 流量，都直接 NAT 转发到到内网的指定地址。也就是往 NAT 的转发表中手动添加内容，示意图：

{{< figure src="/images/about-nat/NAPT-en.svg" title="NAPT tables">}}

设置好端口转发后，只要使用的是被设定的端口，NAT 对 P2P 通信而言将完全透明。
绝大多数路由器都支持这项功能，NAS 发烧友们想玩 P2P 下载分享，基本都是这么搞的。

### 3. UPnP 动态端口转发

>最流行的 UPnP 实现是 <https://github.com/miniupnp/miniupnp>

静态端口转发对用户的技术要求较高，我作为一个网络小白，希望有一个傻瓜式的开关能让我愉快地玩耍 Xbox/PS5 联机游戏，该怎么办呢？
你需要的只是在路由器上启用 UPnP(Universal Plug and Play) 协议，启用它后，内网游戏设备就可以通过 UPnP 向路由器动态申请一个端口号供其使用，UPnP 会自动配置对应的端口转发规则。
**现在新出的路由器基本都支持 UPnP 功能，它是最简单有效的 NAT 提升方式**。

UPnP 解决了「静态端口转发」需要手动配置的问题，在启用了 UPnP 后，对所有支持 UPnP 的内网程序而言，NAT 类型将提升到 Full-cone NAT.

### 4. NAT 穿越协议 - STUN/TURN/ICE

如果很不幸前面提到的 DMZ主机/静态端口转发/UPnP 三项技术，你的路由器都不支持，那你就只能借助 NAT 穿越协议了。

目前有如下几个 NAT 穿越协议标准：

- [RFC5389 - Simple Traversal of UDP Through NATs (STUN)](https://datatracker.ietf.org/doc/html/rfc5389)
  - STUN 是个轻量级的协议，是基于 UDP 的 NAT 穿越方案。它允许应用程序发现它们与公共互联网之间存在的 NAT 及防火墙类型。它也可以让应用程序确定 NAT 分配给它们的公网 IP 地址和端口号。
  - RFC5389 优先使用 UDP 尝试穿越，在失败的情况下会继续使用 TCP 进行尝试
  - STUN 支持除 Symmetric NAT 之外的另外三种 NAT 类型
- [RFC5766 - Traversal Using Relays around NAT (TURN)](https://tools.ietf.org/html/rfc5766)
  - TURN 在 STUN 协议之上添加了一个中继，以确保在无法实现 NAT 穿越的情况下，可以 fallback 到直接使用中继服务器进行通信。
  - 这个中继的原理类似反向代理，单纯负责数据的转发
  - 在美国有一项数据表示在进行 P2P 穿越的时候，穿越成功的概率为 70%，但是在国内这个成功率 50% 可能都到不了。因此就有必要使用 TURN 协议，这样才能保证在穿越失败的情况下，用户仍然能正常通信。
- [RFC8445 - Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445)
  - 一个 NAT 穿越的协商协议，它统一了 STUN 与 TURN 两种协议，会尝试遍历所有可能的连接方案。
  - ICE 的工作流程
    - 首先收集终端双方所有的通路（因为终端可能包含多个网卡，必定包含多个通路）
    - 按一定优先级，对所有通路进行连通性检测，连接建立则 ICE 结束工作
  - 优先级顺序：
    - 内网直接通讯，这肯定是优先级最高的嘛
    - 尝试使用 STUN 协议进行 NAT 穿越
    - 走 TURN 中继服务器进行代理通讯

总的来说，标准的 NAT 穿越协议优先使用打洞（**NAT Hole Pounching**）技术，如果打洞失败，就使用中继服务器技术兜底，确保能成功穿越。

### TURN 协议如何实现 NAT 打洞

首先 P2P 双方如果只隔着 0-1 层 NAT，那是不需要使用 NAT 打洞技术的，可以直连或者反向连接。

下面就讨论下 P2P 双方隔着 2 层及以上 NAT 的场景下，如何利用 UDP 协议实现 NAT 打洞。

一个完整的 NAT 打洞方案，需要包含如下功能：

- A 跟 B 需要知道对方的公网 IP 以及监听的端口号
  - 解决方法：需要一个公网**中介**来介绍双方认识（交换 IP/port）
- NAT 连通性测试，需要借助公网主机，**检测双方中间网络的类型**
- 针对不同的 NAT 类型，存在哪些穿越手段？以何种顺序进行**穿越尝试**？

NAT 打洞可以使用 UDP/TCP 两种 L4 协议，但是 TCP 面向连接的特性使它在这个场景中限制性更大（具体限制见参考文章，我有空再补充），因此各种 NAT 穿越协议通常都基于 UDP 实现。

#### 1. A 与 B 在同一局域网中

这是最简单的情况，最佳方案是直接走内网通讯，不经过 NAT.

第二个方案是，这两个同一局域网内的客户端不走内网，仍然通过 NAT 通讯。这种通讯方式被称作「回环 NAT(Loopback NAT)」或者「发夹 NAT(Hairpin NAT)」。
对于不支持或未启用「Hairpin NAT」的网关设备而言，这样的通讯尝试将会失败！

#### 2. A 与 B 分别在不同的局域网中

这样实际上 A 与 B 中间就隔了两个 NAT 网关，这是最普遍的一种情况。

依据双方 NAT 网关的类型，有如下 NAT 穿越能否成功，可以使用下表来表示：

|       NAT 类型      | Full Cone | Restricted | Port-Restricted | Symmetric |
| ------------------ | --------- | ---------- | --------------- | --------- |
| Full Cone          | ✅         | ✅          | ✅               | ✅         |
| Restricted         | ✅         | ✅          | ✅               | ✅         |
| Port-Restricted    | ✅         | ✅          | ✅               | ❌         |
| Symmetric          | ✅         | ✅          | ❌               | ❌         |

>因为 NAT 具体行为的变数太多，路由器的防火墙策略也存在很大变动空间，再有就是 RF3489 的这种 NAT 分类方法不够精确，这些因素导致 NAT 穿透能否成功通常都是谈概率。

总的来说，只要不是 Symmetric NAT，穿越成功的概率就很大（前提是路由器上没啥特殊的防火墙规则）。
而一旦中间存在 Symmetric NAT，由于 Symmetric NAT 为每个连接提供一个映射，使得转换后的公网地址和端口对不可预测，穿越就无法成功了。
这种场景下 TURN 协议给出的解决方案是，fallback 到中继服务器策略作为兜底方案，保证连接能成功，但是这会给中继服务器带来很大压力，延迟等参数将不可避免地变差。

STUN/TURN 的 NAT 穿透流程大致如下：

- 首先，A 跟 B 两个程序启动时，需要把自己的内外网 IP 及端口信息上报到一台中介服务器 S
- 现在假设 A 想要跟 B 建立一个 P2P 连接，首先他们需要从 S 获得对方的 ID
- A 将 B 的 ID 发送给中介服务器 S，请求与 B 建立 P2P 连接
- 中介服务器将 B 的内外网 IP 及端口信息发送给 A，同时将 A 的网络信息发送给 B
- A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`
  - 这肯定会失败，但是会在 A 的 NAT 网关上留下记录：A 曾经请求过这个地址，那之后这个地址发到 A 的 NAT 网关的流量就可以进来了。
- B 尝试请求 A 的公网地址 `A_public_ip:A_public_port`
  - 同样这肯定也会失败，但是会在 B 的 NAT 网关上流量记录：B 曾经请求过这个地址，那之后这个地址发到 B 的 NAT 网关的流量就可以进来了
- 中间的两层 NAT 网关均形成 NAT 穿越记录，**穿越完成**。
- 现在 A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`，由于 B 的 NAT 已有记录，流量顺利通过 NAT 到达程序 B
- B 发送给 A 的数据也同样，可以顺利到达 A

#### 3. A 与 B 之间隔着三层以上的 NAT

这种情况较为常见的有：

- ISP 为了节约使用公网 IP，给用户分配了个广域网 IP，中间就多了个广域网 NAT
- 大城市的各种租房公寓通常只会从 ISP 购买一两根宽带，二次分销给整栋楼的租客共用，这就造成中间多了一层公寓的 NAT

这是最复杂的一种情况，基本上就没什么 NAT 穿透的希望了，只能走下面介绍的兜底策略——服务器中继。

TBD 待续

#### 4. 特殊穿越方案 - 服务器中继

Relay 服务器中继是兼容性最佳，但是性能最差的方案，因为这个方案下，所有的 P2P 连接都需要经过中继服务器转发，在使用人数众多时这会给中继服务器造成很大的压力。

因此这个方案通常是用于兜底的。

## 使用 Go 实验 NAT 穿透

Go 可用的 NAT 穿越库有：

- [coturn](https://github.com/coturn/coturn): 貌似是最流行的 STUN/TURN/ICE server
- [go-stun](https://github.com/ccding/go-stun): 一个简洁的 stun client 实现，大概适合用于学习？
- [pion/turn](https://github.com/pion/turn): 一个 STUN/TURN/ICE client/client 实现
- [pion/ice](https://github.com/pion/ice): 一个 ice 实现

TBD 待完善

## 虚拟网络、Overlay 与 Underlay

虚拟网络就是在物理网络之上，构建的逻辑网络，也被称作 overlay 网络。
比如 AWS VPC、Docker 容器网络、QEMU 的默认网络，都是虚拟网络。

而 underlay 网络，则是指承载 overlay 网络的底层网络。
我个人理解，它是一个相对的概念，物理网络一定是 underlay 网络，但是虚拟网络之上如果还承载了其他虚拟网络（套娃），那它相对上层网络而言，也是一个 underlay 网络。

overlay 本质上就是一种隧道技术，将原生态的二层数据帧报文进行封装后通过隧道进行传输。常见的 overlay 网络协议主要是 vxlan 以及新一代的 geneve，它俩都是使用 UDP 包来封装链路层的以太网帧。

vxlan 在 2014 年标准化，而 geneve 在 2020 年底才通过草案阶段，目前尚未形成最终标准。但是目前 linux/cilium 都已经支持了 geneve.

geneve 相对 vxlan 最大的变化，是它更灵活——它的 header 长度是可变的。

目前所有 overlay 的跨主机容器网络方案，几乎都是基于 vxlan 实现的（例外：cilium 也支持 geneve）。

vxlan/geneve 的详细介绍，参见 [Linux 中的虚拟网络接口 - vxlan/geneve](https://thiscute.world/posts/linux-virtual-network-interfaces/#vxlan-geneve)

顺带再提一嘴，cilium/calico/kube-ovn 等 overlay 容器网络，都是 SDN 软件定义网络。

### 相关工具

有一些专门用于跨网搭建私有虚拟网络的工具，由于家庭网络设备前面通常都有至少一层 NAT（家庭路由器），因此这些工具都重度依赖 NAT 穿越技术。
如果 NAT 层数太多无法穿越，它们会 fallback 到代理模式，也就是由一台公网服务器进行流量中继，但是这会对中继服务器造成很大压力，延迟跟带宽通常都会差很多。

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

- [NAT 网关](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/vpc-nat-gateway.html)
  - 支持三种协议：TCP, UDP, ICMP
  - 支持 IPv4 与 IPv6 两种 IP 协议
  - 支持 5 Gbps 带宽，可自动扩展到 45 Gbps
    - 可通过划分子网并在多个子网中添加 NAT 网关的方式，获得超过 45Gbps 的带宽
  - 最高支持与每个不同的地址建立 55000 个并发连接
  - NAT 网关从属于 VPC 的子网
  - 每个 NAT 网关只能绑定一个 IP
    - 可通过划分子网并在多个子网中添加 NAT 网关的方式获得多个 IP
  - 可达到 100w packets 每秒的处理速度，并能自动扩展到 400w packets 每秒
    - 同样，需要更高的处理速度，请添加更多 NAT 网关
  - 按处理数据量收费
  - 默认路由到 NAT 子网，被称为「私有子网」（或者没默认路由，那就是无法访问公网的私有子网），连接只能由内网程序主动发起。
  - NAT 网关为流量执行「**Symmetric NAT**」
- [IGW 因特网网关](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/VPC_Internet_Gateway.html)
  - IGW 是一个高度可用的逻辑组件，不会限制 VPC 的总带宽、处理能力。
  - IGW 实例直接关联 VPC，不从属于任何可用区或子网
  - IGW 实质上是一个 NAT 设备，为绑定了公网 IP 地址的 ENI/EC2 实例，执行「**一对一 NAT**」
  - 默认路由到 IGW 的子网，被称为「公有子网」

## 参考

- [What Is Network Address Translation (NAT)? - Huawei Docs](https://info.support.huawei.com/info-finder/encyclopedia/en/NAT.html)
- [[What Is STUN? - Huawei Docs](https://info.support.huawei.com/info-finder/encyclopedia/en/STUN.html)
- [P2P技术详解(一)：NAT详解——详细原理、P2P简介](http://www.52im.net/thread-50-1-1.html)
- [P2P技术详解(二)：P2P中的NAT穿越(打洞)方案详解](http://www.52im.net/thread-542-1-1.html)
- [P2P技术详解(三)：P2P中的NAT穿越(打洞)方案详解(进阶分析篇)](http://www.52im.net/thread-2872-1-1.html)
- [Connect to the internet using an internet gateway - AWS VPC Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
- [从DNAT到netfilter内核子系统，浅谈Linux的Full Cone NAT实现](https://blog.chionlab.moe/2018/02/09/full-cone-nat-with-linux/)
- [Network address translation - wikipedia](https://en.wikipedia.org/wiki/Network_address_translation)



