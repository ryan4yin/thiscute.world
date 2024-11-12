---
title: "NAT 网关、NAT 穿越以及虚拟网络"
date: 2022-05-13T11:46:00+08:00
draft: false

featuredImage: "nat.webp"
authors: ["ryan4yin"]

tags: ["NAT", "网络", "NAT 穿越", "内网穿透", "虚拟网络", "P2P", "WebRTC"]
categories: ["tech"]
series: ["计算机网络相关"]
# 文章未完成，先不在首页显示
# hiddenFromHomePage: true
---

> 个人笔记，不一定正确...

> 当前文章完成度 - 70%

## 前言

NAT，即 Network Address Translation，是 IPv4 网络中非常重要的一个功能，用于执行 IP 地址与
端口的转换。

IPv4 的设计者没预料到因特网技术的发展会如此之快，在设计时只使用了 32bits 的地址空间，随着
因特网的飞速发展，它很快就变得不够用了。后来虽然设计了新的 IPv6 协议，但是它与 IPv4 不兼
容，需要新的硬件设备以及各种网络程序支持，无法快速普及。

NAT 就是在 IPv6 普及前，临时解决 IPv4 地址空间不够用而开发的技术，通俗地讲 NAT 就是用来给
IPv4 续命的。它解决 IPv4 地址短缺问题的方法是：

- 每个家庭、组织、企业，在内部都使用局域网通讯，不占用公网 IPv4 资源
- 在局域网与上层网络的交界处（路由器），使用 NAT 技术进行 IP/port 转换，使用户能正常访问上
  层网络

在曾经 IPv4 地址还不是特别短缺的时候，普通家庭的网络架构通常是：「家庭局域网」=>「NAT 网关
（家庭路由器）」=>「因特网」。

但是互联网主要发展于欧美，因此许多欧美的组织与机构在初期被分配了大量的 IPv4 资源，而后入场
的中国分配到的 IPv4 地址就不太能匹配上我们的人口。因此相比欧美，中国的 IPv4 地址是非常短缺
的，即使使用上述这样的网络架构——也就是给每个家庭（或组织）分配一个 IPv4 地址——都有点捉襟见
肘了。于是中国电信等运营商不得不再加一层 NAT，让多个家庭共用同一个 IP 地址，这时网络架构会
变成这样：「家庭局域网」=>「家庭 NAT 网关」=>「运营商广域网」=>「运营商 NAT 网关」=>「公共
因特网」。由于此架构通过两层 NAT 网关串联了三个不同的 IPv4 网络，它也被形象地称为
**NAT444** 技术，详见
[电信级NAT - 维基百科](https://zh.wikipedia.org/wiki/%E7%94%B5%E4%BF%A1%E7%BA%A7NAT)。

> [据 v2ex 上传闻](https://v2ex.com/t/876430)因为 IPv4 地址紧缺，国内运营商甚至开始尝试使
> 用 **NAT4444** 了，就是中间加两层运营商的私有网络...

> 不过 IPv6 也正在变得越来越流行，看 v2ex 上最近（2022-08）就很多人在聊，一些城市在试点
> ipv4 over ipv6 隧道技术，底层完全换成 IPv6 协议加 IPoE 拨号了，带来的问题是没法桥接，详
> 见
> [电信又一新动作：上网业务不再使用 PPPoE 新装宽带无法改桥接 - v2ex](https://www.v2ex.com/t/875362)。

总的来说，NAT 是一项非常成功的技术，它成功帮 IPv4 续命了几十年，甚至到如今 2022 年，全球网
络仍然是 IPv4 的天下。

## NAT 如何工作

NAT 的工作方式，使用图例描述是这样的：

{{< figure src="/images/about-nat/NAT-demo.webp" title="NAT 示例">}}

从外部网络看一个 NAT 网关（一个启用了 NAT 的路由器），它只是拥有一个 IPv4 地址的普通设备，
所有从局域网发送到公网的流量，其 IP 地址都是这个路由器的 WAN IP 地址，在上图中，这个 IP 地
址是 `138.76.29.7`.

本质上，NAT 网关隐藏了家庭网络的细节，从外部网络上看，整个家庭网络就像一台普通的网络设备。

下面我们会学习到，上述这个 NAT 工作方式实际上是 NAPT，它同时使用 L3/L4 的信息进行地址转换
工作。

## NAT 的地址映射方式

NAT 的具体实现有许多的变种，不存在统一的规范，但是大体上能分为两种模型：「一对一 NAT」与
「一对多 NAT」，下面分别进行介绍。

### 1. 一对一 NAT

一对一 NAT，这种类型的 NAT 在 [RFC2663](https://datatracker.ietf.org/doc/html/rfc2663) 中
被称为 Basic NAT。它在技术上比较简单，只利用网络层的信息，对 IP 地址进行转换。

简单的说，Basic NAT 要求每个内网 IP 都需要绑定一个唯一的公网 IP，才能连通外部网络。

其**主要应用场景是，公网用户需要访问到内网主机**。

Basic NAT 有三种类型：「**静态 NAT**」、「**动态 NAT**」以及「**NAT Server**」。

现在的很多家庭路由器都自带一个被称为 DMZ 主机的功能，它是「Demilitarized Zone」的缩写，意
为隔离区。它允许将某一台内网主机设置为 DMZ 主机（或者叫隔离区主机，仅此主机可供外网访
问），所有从外部进来的流量，都会被通过 Basic NAT 修改为对应的内网 IP 地址，然后直接发送到
该主机。路由器的这种 DMZ 技术就是「静态 NAT」，因为 DMZ 主机对应的内网 IP 需要手动配置，不
会动态变化。

{{< figure src="/images/about-nat/dmz-host-topology.webp" title="DMZ 主机拓扑结构" >}}

而「**动态 NAT**」则需要一个公网 IP 地址池，每次用户需要访问公网时，动态 NAT 会给它分配一
个动态公网 IP 并自动配置相应的 NAT 规则，使用完再回收。

第三种是「**NAT Server**」，云服务商提供的「**公网 IP**」就是通过「**NAT Server**」实现
的，在云服务器中使用 `ip addr ls` 查看你会发现，该主机上实际只配了局域网 IP 地址，但是它却
能正常使用公网 IP 通信，原因就是云服务商在「**NAT Server**」上为这些服务器配置了 IP 转发规
则。为一台云服务器绑定一个公网 IP，实际上就是请求「**NAT Server**」从公网 IP 地址池中取出
一个，并配置对应的 NAT 规则到这台云服务器的局域网 IP。

示例如下，其中的 Internet Gateway 实际上就是个一对一 NAT Server：

{{< figure src="/images/about-nat/aws-vpc-nat-internet-gateway.webp" title="AWS VPC 中的 NAT 网关以及 Internet 网关">}}

> 云服务 VPC 中的公有子网，实际上就是一个 DMZ(Demilitarized Zone) 隔离区，是不安全的。而私
> 有子网则是安全区，公网无法直接访问到其中的主机。

而「动态 NAT」则需要路由器维护一个**公网 IP 地址池**，内网服务器需要访问公网时，动态 NAT
就从地址池中拿出一个公网 IP 给它使用，用完再回收。这种场景需要一个公网 IP 地址池，每当内部
有服务需要请求外网时，就动态地为它分配一个公网 IP 地址，使用完再回收。

Basic NAT 的好处是，它仅工作在 L3 网络层，网络层上的协议都可以正常使用（比如 P2P），不需要
啥「内网穿越」技术。

### 2. 一对多 NAT - NAPT

一对多 NAT，也被称为 NAPT（network address and port translation），同样在
[RFC2663](https://datatracker.ietf.org/doc/html/rfc2663#section-4.0) 中被定义。Easy IP 是
NAPT 的一个特殊形式。

**NAPT 的主要应用场景是，内网用户需要访问到公网主机**。绝大多数的家庭网络、办公网络都是
NAPT 类型的。原因应该很好理解——家庭网络或办公网络都包含许多联网设备，但是这类网络通常只有
一个或数个公网 IP，使用一对一 NAT 的话公网 IP 显然是不够用的，所以需要使用一对多 NAT.

NAPT 通过同时利用 L3 的 IP 信息，以及 L4 传输层的端口信息，来为局域网设备提供透明的、配置
方便的、支持超高并发连接的外部网络通信，示意图如下：

{{< figure src="/images/about-nat/napt.webp" >}}

NAPT 的端口分配与转换规则（**Mapping Behavior**）以及对外来流量的过滤规则（**Filtering
Behavior**）都存在许多不同的实现，没有统一的规范与标准，但是存在两种分类规范，这种分类方法
主要用在 NAT 穿越技术中。

#### RFC3489 定义的 NAT 类型（四种）

在 [RFC3489](https://datatracker.ietf.org/doc/html/rfc3489#section-5) 中将 NAPT 分为四种类
型，这也是应用最为广泛的 NAT 分类方法，如下图：

{{< figure src="/images/about-nat/nat-types-defined-in-stun.webp" >}}

下面我们逐一介绍这四种不同的 NAPT 类型。

> 从这里开始，下文中的 NAT 特指 NAPT，如果涉及「一对一 NAT」会使用它的全名。

##### 1. Full-cone NAT

Full-cone NAT 的特点如下：

- 数据包流出：一旦内部地址（iAddr:iPort）映射到外部地址（eAddr:ePort），所有发自
  iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：任意主机发送到 eAddr:ePort 的数据包，都能通过 NAT 到达 iAddr:iPort.
  - 也就是不对外部进来的数据做任何限制，全部放行。
  - cone 圆锥，个人理解是一个比喻，任意发送进来的数据（多），都能通过 NAT 到达这个内部地址
    （一），就像一个圆锥。

允许任意主机发送到 eAddr:ePort 的数据到达内部地址是很危险的行为，因为内部主机不一定配置了
合适的安全策略。因此 **Full-cone NAT 比较少见**，就算路由器等 NAT 设备支持 Full-cone NAT，
通常也不会是默认选项。我们会在后面更详细地介绍它。

##### 2. (Address-)Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址
  （eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的**外部主机**（nAddr:**any**），发送到
  eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - 跟 Full-cone NAT 的区别在于，它**限制了外部主机的 IP 地址**。只有主动连接过的主机，才
    能发送数据到 NAT 内部。这**提升了一些安全性**。

##### 3. Port-Restricted cone NAT

- 数据包流出：（跟 Full-cone NAT 完全一致）一旦内部地址（iAddr:iPort）映射到外部地址
  （eAddr:ePort），所有发自 iAddr:iPort 的数据包都经由 eAddr:ePort 向外发送。
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的**外部程序**（nAddr:**nPort**），发送
  到 eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - 与 Address-Restricted cone NAT 的区别在于，它**同时限制了外部主机的 IP 与端口**，可以
    说是更**进一步地提升了安全性**。

##### 4. Symmetric NAT

- 数据包流出：同一个内部地址（iAddr:iPort）与不同外部主机（nAddr:nPort）的通信，会随机使用
  不同的 NAT 外部端口（eAddr:**randomPort**）。也就是说内部地址与 NAT 外部地址的关系也
  是**一对多**！
  - 为每个连接都随机选择一个不同的 NAT 端口，这实际是进一步强化了 NAT 内网的安全性。**但这
    也是 NAT 穿越最大的难点——它导致 Symmetric NAT 的端口难以预测**！
- 数据包流入：只有内部地址（iAddr:iPort）主动连接过的外部程序（nAddr:nPort），发送到
  eAddr:ePort 的数据包，才能通过 NAT 到达 iAddr:iPort.
  - 这个数据流入规则，与 Port-Restricted cone NAT 是完全一致的。

**对称 NAT 是最安全的一种 NAT 结构，限制最为严格，应该也是应用最广泛的 NAT 结构**。但是它
导致所有的 TCP 连接都只能由从内部主动发起，外部发起的 TCP 连接请求会直接被 NAT 拒绝，因此
它也是 P2P 玩家最头疼的一种 NAT 类型。解决方案是通过 UDP 迂回实现连接的建立，我们会在后面
讨论这个问题。

##### 5. Linux 中的 NAPT

Linux 的网络栈中，可通过 `iptables/netfilter` 的 `SNAT/MASQUERADE` 实现 NAPT 网关，这种方
式只能实现一个 Symmetric NAT.

也就是说绝大多数基于 Linux 实现的家庭局域网、Docker 虚拟网络、Kubernetes 虚拟网络、云服务
的虚拟网络，都是 Symmetric NAT.

只有一些有 Full-cone NAT 需求的网吧、ISP 的 LSN(Large Scale NAT) 网关等组织，会使用非
Linux 内核的企业级路由器提供 Full-cone NAT 能力，这些设备可能是基于 FPGA 等专用芯片设计
的。

想要将 Symmetric NAT 内的主机提供给外部访问，只能通过端口映射、一对一 NAT 等方式实现，后面
会详细介绍这些方法。

#### RFC5389 定义的 NAT 类型（九种）

RFC3489 这个早期 RFC 存在一些问题，问题之一就是它对 NAT 归类过于笼统，很多 NAPT 网关都无法
很好的匹配上其中某个类别。

于是后来，RFC3489 被废弃并由 [RFC5389](https://www.rfc-editor.org/rfc/rfc5389) 来替代，在
RFC5389 中，将 Mapping Behavior（映射规则）和 Filtering Behavior（过滤规则）分开来，定义了
3 种 Mapping Behavior（映射规则）和 3 种 Filtering Behavior（过滤规则），一共有 9 种组合。

##### 1. 映射规则

三种映射规则如图所示，假设一个内网主机 HostX 的内网 IP 地址为 X，端口号为 x，经 NAT 映射后
的外网 IP 地址为 M，端口号为 m。为方便描述，将内网的 Endpoint 记为 `Endpoint(X,x)`，映射后
外网的 Endpoint 记为 `Endpoint(M,m)`。内网 `Endpoint(X,x)` 发往外网 HostD1 的 IP 地址和端
口号记为目的 `Endpoint(D1,d1)`；发往外网 HostD2 的 IP 地址和端口号记为目的
`Endpoint(D2,d2)`。

{{< figure src="/images/about-nat/rfc5389-mapping-behavior.webp" title="NAT 映射规则">}}

- **EIM**(Endpoint-Independent Mapping) 外部地址无关映射
  - 对于一个内网 `Endpoint(X,x)`，其映射的外网 `Endpoint(M,m)` 是固定的。即从相同的
    `Endpoint(X,x)` 发送到任何外部 IP 地址和任何外部端口的报文在 NAT 设备上使用相同的映
    射。
- **ADM**(Address-Dependent Mapping) 外部地址相关映射：对于一个内网 `Endpoint(X,x)`，发往
  目的 `Endpoint(D1,d1)` 的报文，`Endpoint(X,x)` 被映射成 `Endpoint(M1,m1)`；发往目的
  `Endpoint(D2,d2)` 的报文，`Endpoint(X,x)` 被映射成 `Endpoint(M2,m2)`。只要D1=D2，不管d1
  和d2是多少，都有 `Endpoint(M1,m1)=Endpoint(M2,m2)`。即从相同的 `Endpoint(X,x)` 发送到相
  同外部 IP 地址和任何外部端口的报文在 NAT 设备上使用相同的映射。
- **APDM**（Address and Port-Dependent Mapping）外部地址和端口相关映射：对于一个内网
  `Endpoint(X,x)`，发往目的 `Endpoint(D1,d1)` 的报文，`Endpoint(X,x)` 被映射成
  `Endpoint(M1,m1)`；发往目的 `Endpoint(D2,d2)` 的报文， `Endpoint(X,x)` 被映射成
  `Endpoint(M2,m2)`。只有当D1=D2，且d1=d2，才有 `Endpoint(M1,m1)=Endpoint(M2,m2)`。即从相
  同的 Endpoint(X,x) 发送到相同外部IP地址和相同外部端口的报文在NAT设备上使用相同的映射。

##### 2. 过滤规则

{{< figure src="/images/about-nat/rfc5389-filtering-behavior.webp" title="NAT 过滤规则">}}

- **EIF**（Endpoint-Independent Filtering）外部地址无关过滤：对于一个内网
  `Endpoint(X,x)`，只要它曾经向外网发送过数据，外网主机就可以获取到它经 NAT 映射后的外网
  `Endpoint(M,m)` 。那么只要是发给 `Endpoint(M,m)` 的报文，不管来源于 D1 还是 D2，都能被转
  换并发往内网，其他报文被过滤掉。

- **ADF**（Address-Dependent Filtering）外部地址相关过滤：对于一个内网 `Endpoint(X,x)` ，
  只有它曾经向 IP 地址为 D1 的外网主机发送过报文，那么来自外网 HostD1 返回的任何端口的报
  文，都能被转换并发往内网，其他报文被过滤掉。

- **APDF**（Address and Port-Dependent Filtering）外部地址和端口相关过滤：对于一个内网
  `Endpoint(X,x)` ，只有它曾经向 IP 地址为 D1，端口号为 d1 的外网目的 `Endpoint(D1,d1)` 发
  送过报文，那么也只有外网 HostD1 中来自`Endpoint(D1,d1)`返回的报文，才能被转换并发往内
  网，其他报文被过滤掉。

##### 3. RFC3489 与 RFC5389 的 NAT 类型定义关系

- Full Cone NAT 是 EIM 和 EIF 的组合。
- Restricted Cone NAT 是 EIM 和 ADF 的组合。
- Port Restricted Cone NAT 是 EIM 和 APDF 的组合。
- Symmetric NAT 是 APDM 和 APDF 的组合。

## NAT 的弊端

- **IP 会话的保持时效变短**：NAT 需要维护一个会话列表，如果会话静默时间超过一个阈值，将会
  被从列表中移除。
  - 为了避免这种情况，就需要定期发送心跳包来维持 NAT 会话。俗称心跳保活
- **IP 跟踪机制失效**：一对多 NAT 使得多个局域网主机共用一个公网 IP，这导致基于公网 IP 进
  行流量分析的逻辑失去意义。
  - 比如很多站点都加了基于 IP 的访问频率限制，这会造成局域网内多个用户之间的服务抢占与排
    队。
- **NAT 的工作机制依赖于修改IP包头的信息，这会妨碍一些安全协议的工作**。
  - 因为 NAT 篡改了 IP 地址、传输层端口号和校验和，这会导致 IP 层的认证协议彻底不能工作，
    因为认证目的就是要保证这些信息在传输过程中没有变化。
  - 对于一些隧道协议，NAT 的存在也导致了额外的问题，因为隧道协议通常用外层地址标识隧道实
    体，穿过 NAT 的隧道会有 IP 复用关系，在另一端需要小心处理。
  - ICMP 是一种网络控制协议，它的工作原理也是在两个主机之间传递差错和控制消息，因为IP的对
    应关系被重新映射，ICMP 也要进行复用和解复用处理，很多情况下因为 ICMP 报文载荷无法提供
    足够的信息，解复用会失败。
  - IP 分片机制是在信息源端或网络路径上，需要发送的 IP 报文尺寸大于路径实际能承载最大尺寸
    时，IP 协议层会将一个报文分成多个片断发送，然后在接收端重组这些片断恢复原始报文。IP 这
    样的分片机制会导致传输层的信息只包括在第一个分片中，NAT难以识别后续分片与关联表的对应
    关系，因此需要特殊处理。

## NAT 穿越 - NAT Traversal

天下苦 NAT 久矣，尤其是对各种 P2P 玩家，如 NAS 玩家、P2P 游戏玩家，以及需要搭建 VPN 虚拟私
有网络的网络管理员而言。在常见的联机游戏、BitTorrent 文件共享协议、P2P 聊天等点对点通讯场
景中，通讯双方客户端通常都运行在家庭局域网中，也就是说中间隔着两层家庭路由器的 NAT，路由器
的默认配置都是安全优先的，存在很多安全限制，直接进行 P2P 通讯大概率会失败。

为了穿越这些 NAT 网关进行 P2P 通讯，就需要借助
[NAT 穿越技术](https://en.wikipedia.org/wiki/NAT_traversal)。

> 这里讨论的前提是，你的网络只有单层 NAT，如果外部还存在公寓 NAT、ISP 广域网 NAT，那下面介
> 绍的 NAT 提升技术实际上就没啥意义了。

### 1. 「DMZ 主机」或者「定向 DNAT 转发」

最简单的方法是 DMZ 主机功能，前面已经介绍过了，DMZ 可以直接给内网服务器绑定路由器的外部
IP，从该 IP 进来的所有流量都会直接被发送给这台内网服务器。被指定的 DMZ 主机，其 NAT 类型将
从 NAPT 变成一对一 NAT，而一对一 NAT 对 P2P 通讯而言是透明的，这样就可以愉快地玩耍了。

在 Linux 路由器上实现类似 DMZ 的功能，只需要两行 iptables 命令，这可以称作「定向 DNAT 转
发」：

```shell
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE # 普通的SNAT
iptables -t nat -A PREROUTING -i eth0 -j DNAT --to-destination 192.168.1.3 # 将入站流量DNAT转发到内网主机192.168.1.3
```

这两项技术的缺点是只能将一台主机提供给外网访问，而且将整台主机开放到公网实际上是很危险的，
如果不懂网络**很容易被黑客入侵**。

### 2. 静态端口转发

退一步，可以直接用静态端口转发功能，就是在路由器上手动设置某个端口号的所有 TCP/UDP 流量，
都直接 NAT 转发到到内网的指定地址。也就是往 NAT 的转发表中手动添加内容，示意图：

{{< figure src="/images/about-nat/NAPT-en.svg" title="NAPT tables">}}

设置好端口转发后，只要使用的是被设定的端口，NAT 对 P2P 通信而言将完全透明。绝大多数路由器
都支持这项功能，NAS 发烧友们想玩 P2P 下载分享，基本都是这么搞的。

### 3. UPnP 动态端口转发

> 最流行的 UPnP 实现是 <https://github.com/miniupnp/miniupnp>

静态端口转发对用户的技术要求较高，我作为一个网络小白，希望有一个傻瓜式的开关能让我愉快地玩
耍 Xbox/PS5 联机游戏，该怎么办呢？你需要的只是在路由器上启用 UPnP(Universal Plug and Play)
协议，启用它后，内网游戏设备就可以通过 UPnP 向路由器动态申请一个端口号供其使用，UPnP 会自
动配置对应的端口转发规则。 **现在新出的路由器基本都支持 UPnP 功能，它是最简单有效的 NAT 提
升方式**。

UPnP 解决了「静态端口转发」需要手动配置的问题，在启用了 UPnP 后，对所有支持 UPnP 的内网程
序而言，NAT 类型将提升到 Full-cone NAT.

### 4. NAT 穿越协议 - STUN/TURN/ICE

如果很不幸前面提到的「DMZ 主机」/「静态端口转发」/「UPnP」 三项技术，你的路由器都不支持，
那你就只能借助 NAT 穿越协议了。

目前有如下几个 NAT 穿越协议标准：

- [RFC3489](https://datatracker.ietf.org/doc/html/rfc3489) Classic STUN
  - Classic STUN 是一个早期的 STUN 规范，它定义了一整套完整的 NAT 穿越方案，但是因为存在许
    多问题，已经被废弃。
- [RFC5389 - Simple Traversal of UDP Through NATs (STUN)](https://datatracker.ietf.org/doc/html/rfc5389)
  - RFC5389 所定义的 STUN 协议是对 Classic STUN 的改进，它的定位不再是一个完整的 NAT 穿越
    解决方案，而是作为其他协议（例如SIP、FTP、DNS）处理 NAT 穿越问题的一个工具。
  - 其可以用于检查网络中NAT设备的存在，并确定两个通信端点被NAT设备分配的IP地址和端口号。然
    后，通过ICE（Interactive Connectivity Establishment），自动创建一条能够进行NAT穿越的数
    据通道。
  - STUN 支持除 Symmetric NAT 之外的另外三种 NAT 类型
- [RFC5766 - Traversal Using Relays around NAT (TURN)](https://tools.ietf.org/html/rfc5766)
  - TURN 在 STUN 协议之上添加了一个中继，以确保在无法实现 NAT 穿越的情况下，可以 fallback
    到直接使用中继服务器进行通信。
  - 这个中继的原理类似反向代理，单纯负责数据的转发
  - 在美国有一项数据表示在进行 P2P 穿越的时候，穿越成功的概率为 70%，但是在国内这个成功率
    50% 可能都到不了。因此就有必要使用 TURN 协议，这样才能保证在穿越失败的情况下，用户仍然
    能正常通信。
- [RFC8445 - Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445)
  - 一个 NAT 穿越的协商协议，它统一了 STUN 与 TURN 两种协议，会尝试遍历所有可能的连接方
    案。

总的来说，标准的 NAT 穿越协议优先使用打洞
（**[NAT Hole Pounching](<https://en.wikipedia.org/wiki/Hole_punching_(networking)>)**）技
术，如果打洞失败，就使用中继服务器技术兜底，确保能成功穿越。

#### STUN/TURN/ICE 的 NAT 类型检测

RFC5389 定义了对 NAT 映射类型以及过滤类型的检测方法。

TBD

#### STUN/TURN/ICE 协议如何实现 NAT 打洞

首先 P2P 双方如果只隔着 0-1 层 NAT，那是不需要使用 NAT 打洞技术的，可以直连或者反向连接。

下面就讨论下 P2P 双方隔着 2 层及以上 NAT 的场景下，如何利用 UDP 协议实现 NAT 打洞。

一个完整的 NAT 打洞方案，需要包含如下功能：

- A 跟 B 需要知道对方的公网 IP 以及监听的端口号
  - 解决方法：需要一个公网**中介**来介绍双方认识（交换 IP/port）
- NAT 连通性测试，需要借助公网主机，**检测双方中间网络的类型**
- 针对不同的 NAT 类型，存在哪些穿越手段？以何种顺序进行**穿越尝试**？

NAT 打洞可以使用 UDP/TCP 两种 L4 协议，但是 TCP 面向连接的特性使它在这个场景中限制性更大
（具体限制见参考文章，我有空再补充），因此各种 NAT 穿越协议通常都基于 UDP 实现。

此外，因为 NAT 的具体行为是非标准化的，路由器的防火墙策略也存在很大变动空间，再有就是
RF3489 的这种 NAT 分类方法不够精确，这些因素导致 NAT 穿透能否成功通常都是谈概率。

##### 1. A 与 B 在同一局域网中

这是最简单的情况，最佳方案是直接走内网通讯，不经过 NAT.

第二个方案是，这两个同一局域网内的客户端不走内网，仍然通过 NAT 通讯。这种通讯方式被称作
「回环 NAT(Loopback NAT)」或者「发夹 NAT(Hairpin NAT)」。对于不支持或未启用「Hairpin NAT」
的网关设备而言，这样的通讯尝试将会失败！

##### 2. A 与 B 分别在不同的局域网中

这样实际上 A 与 B 中间就隔了两个 NAT 网关，这是最普遍的一种情况。

STUN/TURN 的 NAT 穿透流程大致如下：

- 首先，A 跟 B 两个程序启动时，需要把自己的内外网 IP 及端口信息上报到一台中介服务器 S
- 现在假设 A 想要跟 B 建立一个 P2P 连接，首先他们需要从 S 获得对方的 ID
- A 将 B 的 ID 发送给中介服务器 S，请求与 B 建立 P2P 连接
- 中介服务器将 B 的内外网 IP 及端口信息发送给 A，同时将 A 的网络信息发送给 B
- A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`
  - 这肯定会失败，但是会在 A 的 NAT 网关上留下记录：A 曾经请求过这个地址，那之后这个地址发
    到 A 的 NAT 网关的流量就可以进来了。
- B 尝试请求 A 的公网地址 `A_public_ip:A_public_port`
  - 同样这肯定也会失败，但是会在 B 的 NAT 网关上流量记录：B 曾经请求过这个地址，那之后这个
    地址发到 B 的 NAT 网关的流量就可以进来了
- 中间的两层 NAT 网关均形成 NAT 穿越记录，**穿越完成**。
- 现在 A 尝试请求 B 的公网地址 `B_public_ip:B_public_port`，由于 B 的 NAT 已有记录，流量顺
  利通过 NAT 到达程序 B
- B 发送给 A 的数据也同样，可以顺利到达 A

上述流程中的关键点在于，如何查出内网服务器被 NAT 分配的外部 IP 及端口，只要有了这两个信
息，就可以通过 STUN 中介服务器交换这个信息，然后完成连接的建立了。家庭服务器通常都只有一个
公网 IP，所以基本可以认为 IP 是固定的，因此最关键的问题就是「**如何知道 NAT 为会话分配的端
口地址**」。

对端口的限制严格程度跟 NAPT 的类型有关，**Full-cone 跟 Restricted cone 对端口都没有任何限
制，所以上述流程肯定可以成功**；

TBD

一个穿越 Symmetric NATs 的 STUN 草
案：[Symmetric NAT Traversal using STUN](https://tools.ietf.org/id/draft-takeda-symmetric-nat-traversal-00.txt)

在使用 STUN/TURN 进行 NAT 穿越时，支持的的 NAT 类型如下表。行与列分别代表双方的 NAT 类
型，✅ 表示支持 UDP 穿越，❌ 表示 TURN 无法进行 UDP 穿越：

| NAT 类型        | Full Cone | Restricted | Port-Restricted | Symmetric |
| --------------- | --------- | ---------- | --------------- | --------- |
| Full Cone       | ✅        | ✅         | ✅              | ✅        |
| Restricted      | ✅        | ✅         | ✅              | ✅        |
| Port-Restricted | ✅        | ✅         | ✅              | ❌        |
| Symmetric       | ✅        | ✅         | ❌              | ❌        |

这种场景下 TURN 协议给出的解决方案是，fallback 到中继服务器策略作为兜底方案，保证连接能成
功，但是这会给中继服务器带来很大压力，延迟等参数将不可避免地变差。

##### 3. A 与 B 之间隔着三层以上的 NAT

这种情况较为常见的有：

- ISP 为了节约使用公网 IP，给用户分配了个广域网 IP，中间就多了个广域网 NAT
- 大城市的各种租房公寓通常只会从 ISP 购买一两根宽带，二次分销给整栋楼的租客共用，这就造成
  中间多了一层公寓的 NAT

这是最复杂的一种情况，基本上就没什么 NAT 穿透的希望了，只能走下面介绍的兜底策略——服务器中
继。

TBD 待续

##### 4. 特殊穿越方案 - 服务器中继

Relay 服务器中继是兼容性最佳，但是性能最差的方案，因为这个方案下，所有的 P2P 连接都需要经
过中继服务器转发，在使用人数众多时这会给中继服务器造成很大的压力。

因此这个方案通常是用于兜底的。

### 特定协议的自穿越技术

在所有方法中最复杂也最可靠的就是自己解决自己的问题。比如 IKE 和 IPsec 技术，在设计时就考虑
了到如何穿越 NAT 的问题。因为这个协议是一个自加密的协议并且具有报文防修改的鉴别能力，其他
通用方法爱莫能助。因为实际应用的 NAT 网关基本都是 NAPT 方式，所有通过传输层协议承载的报文
可以顺利通过 NAT。IKE 和 IPsec 采用的方案就是用 UDP 在报文外面再加一层封装，而内部的报文就
不再受到影响。IKE 中还专门增加了 NAT 网关是否存在的检查能力以及绕开 NAT 网关检测 IKE 协议
的方法。

### NAT ALG(Application Level Gateway)

NAT ALG 是一种解决应用层协议（例如DNS、FTP）报文穿越 NAT 的技术，已经被 NAT 设备产商广泛采
用，是 NAT 设备的必备功能。

TLDR 一句话介绍：NAT ALG 通过识别协议，直接修改报文数据部分（payload）的 IP 地址和端口信
息，解决某些应用协议的报文穿越 NAT 问题。NAT ALG 工作在 L3-L7 层。

NAT ALG 的原理是利用带有 ALG 功能的 NAT 设备对特定应用层协议的支持，当设备检测到新的连接请
求时，先根据传输层端口信息判断是否为已知应用类型。如果判断为已知应用，则调用该应用协议的
ALG 功能对报文的深层内容进行检查。若发现任何形式表达的 IP 地址和端口信息，NAT 都会将这些信
息同步进行转换，并为这个新的连接建立一个附加的转换表项。当报文到达外网侧的目的主机时，应用
层协议中携带的信息就是 NAT 设备转换后的IP地址和端口号，这样，就可以解决某些应用协议的报文
穿越 NAT 问题。

目前支持NAT ALG功能的协议包括：DNS、FTP、SIP、PPTP和RTSP。NAT ALG 在对这些特定应用层协议进
行 NAT 转换时，通过 NAT 的状态信息来改变封装在 IP 报文数据部分的特定数据，最终使应用层协议
可以跨越不同范围运行。

## 使用 Go 实验 NAT 穿透

Go 可用的 NAT 穿越库有：

- [coturn](https://github.com/coturn/coturn): 貌似是最流行的 STUN/TURN/ICE server
- [go-stun](https://github.com/ccding/go-stun): 一个简洁的 stun client 实现，大概适合用于
  学习？
- [pion/turn](https://github.com/pion/turn): 一个 STUN/TURN/ICE client/client 实现
- [pion/ice](https://github.com/pion/ice): 一个 ice 实现

TBD 待完善

## 虚拟网络、Overlay 与 Underlay

虚拟网络就是在物理网络之上，构建的逻辑网络，也被称作 overlay 网络。比如 AWS VPC、Docker 容
器网络、QEMU 的默认网络，都是虚拟网络。

而 underlay 网络，则是指承载 overlay 网络的底层网络。我个人理解，它是一个相对的概念，物理
网络一定是 underlay 网络，但是虚拟网络之上如果还承载了其他虚拟网络（套娃），那它相对上层网
络而言，也是一个 underlay 网络。

overlay 本质上就是一种隧道技术，将原生态的二层数据帧报文进行封装后通过隧道进行传输。常见的
overlay 网络协议主要是 vxlan 以及新一代的 geneve，它俩都是使用 UDP 包来封装链路层的以太网
帧。

vxlan 在 2014 年标准化，而 geneve 在 2020 年底才通过草案阶段，目前尚未形成最终标准。但是目
前 linux/cilium 都已经支持了 geneve.

geneve 相对 vxlan 最大的变化，是它更灵活——它的 header 长度是可变的。

目前所有 overlay 的跨主机容器网络方案，几乎都是基于 vxlan 实现的（例外：cilium 也支持
geneve）。

vxlan/geneve 的详细介绍，参见
[Linux 中的虚拟网络接口 - vxlan/geneve](https://thiscute.world/posts/linux-virtual-network-interfaces/#vxlan-geneve)

顺带再提一嘴，cilium/calico/kube-ovn 等 overlay 容器网络，都是 SDN 软件定义网络。

### 相关工具

有一些专门用于跨网搭建私有虚拟网络的工具，由于家庭网络设备前面通常都有至少一层 NAT（家庭路
由器），因此这些工具都重度依赖 NAT 穿越技术。如果 NAT 层数太多无法穿越，它们会 fallback 到
代理模式，也就是由一台公网服务器进行流量中继，但是这会对中继服务器造成很大压力，延迟跟带宽
通常都会差很多。

如下是两个比较流行的 VPN 搭建工具：

- [zerotier](https://github.com/zerotier/ZeroTierOne): 在 P2P 网络之上搭建的 SDN overlay
  网络，使用自定义协议。
- [tailscales](https://github.com/tailscale/tailscale): 基于 wireguard 协议快速搭建私有虚
  拟网络 VPN

### VPN 协议

主流的 VPN 协议有：PPTP、L2TP、IPSec、OpenVPN、SSTP，以及最新潮的 Wireguard.

TBD

## 拓展知识

### Symmetric NAT 允许的最大并发 TCP 连接数是多少？

TCP 并发连接数受许多参数的限制，以 Linux 服务器为例，默认参数无法满足需要，通常都会手动修
改它的参数，放宽文件描述符限制以及 TCP 连接队列、缓存相关的限制。

单纯从网络协议层面分析，对于一个仅有一个公网 IP 的 Symmetric NAT 网关，它与某个外部站点
`http://x.x.x.x:xx` 要建立连接。考虑到 TCP 连接的定义实际上是一个四元组
`(srcIP, srcPort, dstIP, dstPort)`，其中就只有 NAT 网关自己的 `srcPort` 是唯一的变量了，而
端口号是一个 16bits 数字，取值范围为 0 - 65535。此外低于 1024 的数字是操作系统的保留端口，
因此 NAT 一般只会使用 1024-65535 这个区间的端口号，也就是说这个 NAT 网关最多只能与该站点建
立 64512 个连接。

那么对于不同的协议 NAT 是如何处理的呢？NAT 肯定可以通过协议特征区分不同协议的流量，因此不
同协议通过 NAT 建立的并发连接不会相互影响。

对于家庭网络而言 64512 个连接已经完全够用了，但是对于数据中心或者云上的 VPC 而言，就不一定
够用了。举个例子，在
[AWS NAT 网关的文档](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)中
就有提到，AWS NAT 网关最高支持与每个不同的地址建立 55000 个并发连接。destination 的 IP 地
址、端口号、(TCP/UDP/ICMP) 任一个发生改变，都可以再建立其他 55000 个并发连接。如果超过这个
限制，就会发生「ErrorPortAllocation」错误。如果在 AWS 上遇到这个错误，那就说明你们的云上网
络规划有问题了。

当然除了端口限制外，受限于 NAT 硬件、以太网协议以及其他影响，NAT 网关肯定还有包处理速率、
带宽的限制，这个就略过不提了。

### AWS VPC 与 NAT

AWS VPC(virtual private cloud) 是一个逻辑隔离的虚拟私有网络，云服务架构的最佳实践之一就是
通过 VPC 搭建云上私有网络，提升网络安全性。

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
  - 默认路由到 NAT 子网，被称为「私有子网」（或者没默认路由，那就是无法访问公网的私有子
    网），连接只能由内网程序主动发起。
  - NAT 网关为流量执行「**Symmetric NAT**」
- [IGW 因特网网关](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/VPC_Internet_Gateway.html)
  - IGW 是一个高度可用的逻辑组件，不会限制 VPC 的总带宽、处理能力。
  - IGW 实例直接关联 VPC，不从属于任何可用区或子网
  - IGW 实质上是一个 NAT 设备，为绑定了公网 IP 地址的 ENI/EC2 实例，执行「**一对一 NAT**」
  - 默认路由到 IGW 的子网，被称为「公有子网」

## 参考

- [What Is Network Address Translation (NAT)? - Huawei Docs](https://info.support.huawei.com/info-finder/encyclopedia/en/NAT.html)
- [What Is STUN? - Huawei Docs](https://info.support.huawei.com/info-finder/encyclopedia/en/STUN.html)
- [NetEngine AR V300R019 配置指南-IP业务 - NAT 穿越 - 华为文档](https://support.huawei.com/enterprise/zh/doc/EDOC1100112409/fd829977#ZH-CN_CONCEPT_0227014768)
- [P2P技术详解(一)：NAT详解——详细原理、P2P简介](http://www.52im.net/thread-50-1-1.html)
- [P2P技术详解(二)：P2P中的NAT穿越(打洞)方案详解](http://www.52im.net/thread-542-1-1.html)
- [P2P技术详解(三)：P2P中的NAT穿越(打洞)方案详解(进阶分析篇)](http://www.52im.net/thread-2872-1-1.html)
- [Connect to the internet using an internet gateway - AWS VPC Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
- [从DNAT到netfilter内核子系统，浅谈Linux的Full Cone NAT实现](https://blog.chionlab.moe/2018/02/09/full-cone-nat-with-linux/)
- [Network address translation - wikipedia](https://en.wikipedia.org/wiki/Network_address_translation)
- [WebRTC NAT Traversal Methods: A Case for Embedded TURN](https://www.liveswitch.io/blog/webrtc-nat-traversal-methods-a-case-for-embedded-turn)
- [WireGuard 教程：使用 DNS-SD 进行 NAT-to-NAT 穿透 - 云原生实验室](https://icloudnative.io/posts/wireguard-endpoint-discovery-nat-traversal/)
