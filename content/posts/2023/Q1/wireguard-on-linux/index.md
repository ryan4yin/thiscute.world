---
title: "Linux 上的 WireGuard 网络分析（一）"
date: 2023-03-28T22:19:25+08:00
lastmod: 2023-03-28T22:19:25+08:00
draft: false

resources:
- name: "featured-image"
  src: "wireguard.png"

tags: ["WireGuard", "VPN", "Linux", "网络", "iptables", "conntrack"]
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

>阅读此文章需要前置知识：Linux 网络基础知识、iptables、conntrack

>本文内容部分采用了 Copilot 提示内容，也有部分内容用了 ChatGPT 免费版进行分析，确实都比较有帮助。

## WireGuard 是什么

WireGuard 是极简主义思想下的 VPN 实现，解决了很多现存 VPN 协议存在的问题。
它于 2015 年由 Jason A. Donenfeld 设计实现，因其代码实现简洁易懂、配置简单、性能高、安全强度高而受到广泛关注。

WireGuard 在 2020 年初进入 Linux 主线分支，随后成为 Linux 5.6 的一个内核模块，这之后很快就涌现出许多基于 WireGuard 的开源项目与相关企业，各大老牌 VPN 服务商也逐渐开始支持 WireGuard 协议，很多企业也使用它来组建企业 VPN 网络。

基于 WireGuard 的明星开源项目举例：

- [tailscale](https://github.com/tailscale/tailscale): 一套简单易用的 WireGuard VPN 私有网络解决方案，强烈推荐！
- [headscale](https://github.com/juanfont/headscale): tailscale 控制服务器的开源实现，使你可以自建 tailscale 服务。
- [kilo](https://github.com/squat/kilo): 基于 WireGuard 的 Kubernetes 多云网络解决方案。
- ...
- 除了上面这些，还有很多其他 WireGuard 项目，有兴趣可以去 [awesome-wireguard](https://github.com/cedrickchee/awesome-wireguard) 仓库看看。

WireGuard 本身只是一个点对点隧道协议，只提供点对点通信的能力（这也是其极简主义思想的体现）。而其他网络路由、NAT 穿越、DNS 解析、防火墙策略等功能都是基于 Linux 系统的现有工具来实现的。

在这篇文章里，我将搭建一个简单的单服务器 + 单客户端 WireGuard 网络，然后分析它如何使用 Linux 系统现有的工具，在 WireGuard 隧道上搭建出一个安全可靠的虚拟网络。
服务器与客户端均使用 Ubuntu 20.04 系统，内核版本为 5.15，也就是说都包含了 wireguard 内核模块。

## WireGuard 服务端网络分析

简单起见，这里使用 docker-compose 启动一个 WireGuard 服务端，使用的镜像是 [linuxserver/docker-wireguard](https://github.com/linuxserver/docker-wireguard)。

配置文件如下，内容完全参考自此镜像的官方 README：

```yaml
---
version: "2.1"
services:
  wireguard:
    image: lscr.io/linuxserver/wireguard:latest
    container_name: wireguard
    cap_add:           
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - SERVERURL=auto   # 自动确定服务器的外部 IP 地址，在生成客户端配置时会用到
      - SERVERPORT=51820 # 服务端监听的端口号
      - PEERS=1          # 自动生成 1 个客户端配置
      - PEERDNS=auto     # 自动确定客户端的 DNS 服务器地址，同样是在生成客户端配置时会用到
      - INTERNAL_SUBNET=10.13.13.0    # WireGuard 虚拟网络的网段
      - ALLOWEDIPS=0.0.0.0/0          # 这条规则表示允许虚拟网络内的所有客户端将流量发送到此节点
      # 众所周知，NAT 网络需要定期发送心跳包来保持 NAT 表内容不过期，俗称连接保活。
      # 这里设置为 all 表示所有客户端都开启连接保活。
      - PERSISTENTKEEPALIVE_PEERS=all 
      - LOG_CONFS=true # 开启日志
    volumes:
      - ./config:/config
      - /lib/modules:/lib/modules # 将宿主机的内核模块挂载到容器内，用于加载 WireGuard 内核模块
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
```

将上面的配置文件保存为 `docker-compose.yml`，然后通过如下命令后台启动 WireGuard 服务端：

```shell
docker-compose up -d
```

WireGuard 服务端启动好了，现在查看下服务端容器的日志（我加了详细注释说明）：

```shell
$ docker logs wireguard
# ...省略若干内容
.:53                          # 这几行日志是启动 CoreDNS，为虚拟网络提供默认的 DNS 服务
CoreDNS-1.10.1                # 实际上 CoreDNS 不是必须的，客户端可以改用其他 DNS 服务器
linux/amd64, go1.20, 055b2c3
[#] ip link add wg0 type wireguard   # 创建一个 wireguard 设备
[#] wg setconf wg0 /dev/fd/63        # 设置 wireguard 设备的配置
[#] ip -4 address add 10.13.13.1 dev wg0   # 为 wireguard 设备添加一个 ip 地址
[#] ip link set mtu 1420 up dev wg0        # 设置 wireguard 设备的 mtu
[#] ip -4 route add 10.13.13.2/32 dev wg0  # 为 wireguard peer1 添加路由，其地址来自 wireguard 配置的 `allowedIPs` 参数
# 下面这几条 iptables 命令为 wireguard 设备添加 NAT 规则，使其成为 WireGuard 虚拟网络的默认网关
# 并使虚拟网络内的其他 peers 能通过此默认网关访问外部网络。
[#] iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth+ -j MASQUERADE
[ls.io-init] done.
```

通过日志能看到，程序首先创建了 WireGuard 设备 wg0 并绑定了地址 `10.13.13.1`。作为 WireGuard 网络中的服务端，它所创建的这个 wg0 的任务是成为整个 WireGuard 虚拟网络的默认网关，处理来自虚拟网络内的其他 peers 的流量，构成一个星型网络。

然后服务端为它所生成的 peer1 添加了一个路由，使得 peer1 的流量能够被正确路由到 wg0 设备上。

最后为了让 WireGuard 虚拟网络内的其他 peers 的流量能够通过 wg0 设备访问外部网络或者互相访问，服务端为 wg0 设备添加了如下的 iptables 规则：

- `iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;`：允许进出 wg0 设备的数据包通过 netfilter 的 FORWARD 链（默认规则是 DROP，即默认是不允许通过的）
- `iptables -t nat -A POSTROUTING -o eth+ -j MASQUERADE`：在 eth+ 网卡上添加 MASQUERADE 规则，即将数据包的源地址伪装成 eth+ 网卡的地址，目的是为了允许 wireguard 的数据包通过 NAT 访问外部网络。
  - 而回来的流量会被 NAT 的 conntrack 链接追踪规则自动允许通过，不过 conntrack 表有自动清理机制，长时间没流量的话会被从 conntrack 表中移除。这就是前面 `docker-compose.yml` 中的 `PERSISTENTKEEPALIVE_PEERS=all` 参数解决的问题通过定期发送心跳包来保持 conntrack 表中的连接信息。
  - 这里还涉及到了 NAT 穿越相关内容，就不多展开了，感兴趣的可以自行了解。

WireGuard 的实现中还有一个比较重要的概念叫做 `AllowedIPs`，它是一个 IP 地址列表，表示允许哪些 IP 地址的流量通过 WireGuard 虚拟网络。
为了详细说明这一点，我们先看下服务端配置文件夹中 wg0 的配置：

```shell
$ cat wg0.conf
[Interface]
Address = 10.13.13.1
ListenPort = 51820
PrivateKey = kGZzt/CU2MVgq19ffXB2YMDSr6WIhlkdlL1MOeGH700=
# wg0 隧道启动后添加 iptables 规则
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth+ -j MASQUERADE
# wg0 隧道停止后删除前面添加的 iptables 规则
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth+ -j MASQUERADE

[Peer]
# peer1
PublicKey = HR8Kp3xWIt2rNdS3aaCk+Ss7yQqC9cn6h3WS6UK3WE0=
PresharedKey = 7mCNCZdMKeRz1Zrpl9bFS08jJAdv6/USazRVq7tjznY=
# AllowedIPs 设置为 peer1 的虚拟 IP 地址，表示允许 peer1 的流量通过 WireGuard 虚拟网络
AllowedIPs = 10.13.13.2/32
```

`AllowedIPs` 实际就是每个 peer 在服务端路由表中的 ip 地址，它既可以是 ip 也可以是网段，而且能设置多个，这使所有 peer 都可以负责一个甚至多个 ip 段的转发，也就是充当局域网的路由器——VPN 子路由。

WireGuard 本身只是一个点对点隧道协议，它非常通用。通过 `AllowedIPs` 参数，我们就能在每个 peer 上添加各 peers 的配置与不同的路由规则，构建出各种复杂的网络拓扑，比如星型、环型、树型等等。

## WireGuard 客户端网络分析

>我这里为了测试方便，客户端与服务端都在我的局域网内。

现在换台虚拟机跑 WireGuard 客户端，首先需要安装 wireguard 命令行工具：

```shell
sudo apt install wireguard resolvconf
```

第二步是从服务端的配置文件夹中找到 `peer1/peer1.conf`，它是服务端容器根据参数 `PEERS=1` 自动生成的客户端配置文件，先确认下它的内容：

```shell
$ cd ./config/peer1
$ cat peer1.conf
[Interface]
Address = 10.13.13.2
PrivateKey = +GLDb5QQOHQ2QKWvuFS/4FiWpnivaxzwlm0QmFJIHV8=
ListenPort = 51820
DNS = 10.13.13.1

[Peer]
PublicKey = t95vF4b11RLCId3ArVVIJoC5Ih9CNbI0VTNuDuEzZyw=
PresharedKey = 7mCNCZdMKeRz1Zrpl9bFS08jJAdv6/USazRVq7tjznY=
# 需要注意的是这个 Peer Endpoint 的 IP 是否正确
Endpoint = 192.168.5.198:51820
AllowedIPs = 0.0.0.0/0
```

>插入下，这个 Endpoint 的地址也很值得一说，能看到服务端 wg0.conf 的配置中，peer1 并未被设置任何 Endpoint，这实质是表示这个 peer1 的 Endpoint 是动态的，也就是说每次 peer1 发送数据到服务端 wg0 时，服务端通过认证加密技术认证了数据后，就会以数据包的来源 IP 地址作为 peer1 的 Endpoint，这样 peer1 就可以随意更换自己的 IP 地址（Roaming），而 WireGuard 隧道仍然能正常工作（IP 频繁更换的一个典型场景就是手机的网络漫游与 WiFi 切换）。这使 WireGuard 具备了比较明显的无连接特性，也就是说 WireGuard 隧道不需要保持一个什么连接，切换网络也不需要重连，只要数据包能够到达服务端，就能够正常工作。

因为我这里是内网环境测试，配置文件中的 `Peer` - `Endpoint` 的 IP 地址直接用服务端的内网 IP 地址就行，也就是 `192.168.5.198`。

配置文件确认无误后，将该配置文件保存到客户端的 `/etc/wireguard/peer1.conf` 这个路径下，然后使用如下命令启动 WireGuard 客户端：

```shell
sudo wg-quick up peer1
```

上述命令会自动在 `/etc/wireguard/` 目录下找到名为 `peer1.conf` 的配置文件，然后根据其内容启动一个名为 `peer1` 的 WireGuard 设备并完成对应配置。

我启动时的日志如下，wg-quick 打印出了它执行的所有网络相关指令（我添加了详细的注释）：

```shell
$ sudo wg-quick up peer1
[#] ip link add peer1 type wireguard             # 创建一个名为 peer1 的 WireGuard 设备
[#] wg setconf peer1 /dev/fd/63                  # 设置 peer1 设备的配置
[#] ip -4 address add 10.13.13.2 dev peer1       # 设置 peer1 设备的 IP 地址
[#] ip link set mtu 1420 up dev peer1            # 设置 peer1 设备的 MTU
[#] resolvconf -a tun.peer1 -m 0 -x              # 设置 peer1 设备的 DNS，确保 DNS 能够正常工作
[#] wg set peer1 fwmark 51820                    # 将 peer1 设备的防火墙标记设为 51820，用于标记 WireGuard 出网流量
                                                 # 该标记是一个 32bits 整数，后面 nft 表会用它追踪连接
[#] ip -4 route add 0.0.0.0/0 dev peer1 table 51820     # 创建单独的路由表 51820，默认将所有流量转发到 peer1 接口
[#] ip -4 rule add not fwmark 51820 table 51820         # 所有不带 51820 标记的流量（普通流量），都转发到前面新建的路由表 51820
                                                        # 也就是所有普通流量都转发到 peer1 接口
[#] ip -4 rule add table main suppress_prefixlength 0   # 流量全都走 main 路由表（即默认路由表），但是排除掉前缀长度（掩码） <= 0 的流量
                                                        # 掩码 <= 0 的只有 0.0.0.0/0，即默认路由。所以意思是所有非默认路由策略的流量都走 main 路由表
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1        # 启用源地址有效性检查，用于防止伪造源地址
[#] nft -f /dev/fd/63                                   # 配置 nftables 规则，用于确保 WireGuard 流量能正确路由，并防止恶意数据包进入网络
```

跑完后我们现在确认下状态，应该是能正常走 WireGuard 访问相关网络了，可以 WireShark 抓个包确认下。

>如果网络不通，那肯定是中间哪一步配置有问题，可以根据上面的日志一步步排查网络接口、路由表、路由策略、iptables/nftables 的配置，必要时可以通过 WireShark 抓包定位。

现在再检查下系统的网络状态，首先检查下路由表，会发现路由表没任何变化：

```shell
$ ip route ls
default via 192.168.5.201 dev eth0 proto static 
192.168.5.0/24 dev eth0 proto kernel scope link src 192.168.5.197 
```

但是我们的 WireGuard 隧道已经生效了，这就说明现在我们的流量已经不是直接走上面这个默认路由表了，还有其他配置在起作用。
往回看看前面的客户端启动日志，其中显示 wg-quick 创建了一个名为 51820 的路由表，我们来检查下这个表：

```shell
ryan@ubuntu-2004-builder:~$ ip route ls table 51820
default dev peer1 scope link
```

能看到这个表确实是将所有流量都转发到了 WireGuard 的 peer1 接口，基本能确认现在流量都走了这个路由表。
那么问题来了，系统的流量是如何被转发到这个路由表的呢？为什么默认的路由表现在不生效了？

要理清这个问题，需要补充点知识——Linux 从 2.2 开始支持了多路由表，并通过路由策略数据库来为每个数据包选择正确的路由表，这个路由策略数据库可以通过 `ip rule` 命令来查看、修改。

前置知识补充完毕，现在来看下系统当前的路由策略，同样我已经补充好了注释：

```shell
$ ip rule show
0:      from all lookup local                         # 0 是最高优先级，`all` 表示所有流量，`lookup local` 表示查找 local 路由表。
                                                      # local 是一个特殊路由表，包含对本地和广播地址的优先级控制路由。
32764:  from all lookup main suppress_prefixlength 0  # 32764 目前是第二优先级，将所有流量路由到　main 路由表，但是排除掉默认路由（前缀/掩码 <= 0）
                                                      # 功能是让所有非默认路由的流量都走 main 路由表
                                                      # 这条规则前面实际解释过了，它是 wg-quick 在启动隧道时添加的规则。
32765:  not from all fwmark 0xca6c lookup 51820       # 所有不带 0xca6c 标记（51820 的 16 进制格式）的流量（普通流量），都走 51820 路由表
                                                      # 也就是都转发到 WireGuard peer1 接口。
                                                      # 这条规则是前面的 `ip -4 rule add not fwmark 51820 table 51820` 命令添加的。
                                                      # 而它所匹配的防火墙标记则是由前面的 `wg set peer1 fwmark 51820` 命令设置的。
32766:  from all lookup main                          # 所有流量都走 main 路由表，当前是不生效状态，因为前面的规则优先级更高。
                                                      # main 是系统的默认路由表，通常我们使用 ip route 命令都是在这个表上操作。
32767:  from all lookup default                       # 所有流量都走 default 路由表，当前同样是不生效状态。
                                                      # default 是一个系统生成的兜底路由表，默认不包含任何路由规则，可用于自定义路由策略，也可删除。
```

结合注释看完上面的路由策略，现在你应该理清楚 WireGuard 的路由规则了，它加了条比默认路由策略 `32766` 优先级更高的路由策略 `32765`，将所有普通流量都通过它的自定义路由表路由到 peer1 接口。
另一方面 peer1 接口在前面已经被打了 fwmark 标记 `51820` 也就是 16 进制的 0xca6c，所以 peer1 出站到服务端的流量不会被 `32765` 匹配到，所以会走优先级更低的 32766 策略，也就是走了 main 路由表。

另外 `32764` 这条路由策略有点特殊，这里也简单解释下，此策略在前面注释中已经做了解释——是让所有非默认路由的流量都走 main 路由表，而 main 路由表中的非默认路由一般都是其他程序自动管理添加的，或者是我们手动添加的，所以这条规则其实就是确保这些路由策略仍然有效，避免 WireGuard 策略把它们覆盖掉而导致问题。

前面都分析完了，现在还剩下 wg-quick 日志的最后一行 `nft -f /dev/fd/63`，它到底做了什么呢？
nft 是 nftables 的命令行工具名称，所以它实际是设置了一些 nftables 规则，我们查看下它的规则内容：

>注意：nftables 的这些 chain 名称是完全自定义的，没啥特殊意义

```shell
$ sudo nft list ruleset
table ip wg-quick-peer1 {
        chain preraw {
                type filter hook prerouting priority raw; policy accept;
                iifname != "peer1" ip daddr 10.13.13.2 fib saddr type != local drop
        }

        chain premangle {
                type filter hook prerouting priority mangle; policy accept;
                meta l4proto udp meta mark set ct mark
        }

        chain postmangle {
                type filter hook postrouting priority mangle; policy accept;
                meta l4proto udp meta mark 0x0000ca6c ct mark set meta mark
        }
}
```

可以看到这里是创建了一个 `wg-quick-peer1` 表，通过该表在 netfilter 上设置了如下规则：

1. `preraw` 链：此链用于防止恶意数据包进入网络。
   1. type 开头的一行是规则的类型，这里是 `filter`，仅匹配了 `raw` 链的 `prerouting` 表。
   2. 它丢弃掉所有来源接口不是 peer1、目的地址是 10.13.13.2、且源地址不是本地地址的数据包。
   3. 总结下就是只允许本地地址或者 peer1 直接访问 10.13.13.2 这个地址。
2. `premangle` 链：此链用于确保所有 UDP 数据包都能被正确从 WireGuard 接口入站。
   1. 它将所有 UDP 数据包的标记设置为连接跟踪标记（没搞懂这个标记是如何生效的....）。
3. `postmangle` 链：此链用于确保所有 UDP 数据包都能被正确从 WireGuard 接口出站。
   1. 它将所有 UDP 数据包的标记设置为 0xca6c（51820 的 16 进制格式）（同样没理解这个标记是如何生效的...）。


最后看下 WireGuard 的状态，它是前面 `wg setconf peer1 /dev/fd/63` 设置的：

```shell
ryan@ubuntu-2004-builder:~$ sudo wg show 
interface: peer1
  public key: HR8Kp3xWIt2rNdS3aaCk+Ss7yQqC9cn6h3WS6UK3WE0=
  private key: (hidden)
  listening port: 51820
  fwmark: 0xca6c

peer: t95vF4b11RLCId3ArVVIJoC5Ih9CNbI0VTNuDuEzZyw=
  preshared key: (hidden)
  endpoint: 192.168.5.198:51820
  allowed ips: 0.0.0.0/0
  latest handshake: 18 minutes, 59 seconds ago
  transfer: 124 B received, 324 B sent
```

分析完毕，现在关闭掉 WireGuard 客户端，将客户端主机的网络恢复到正常状态。

```shell
$ sudo wg-quick down peer1
[#] ip -4 rule delete table 51820
[#] ip -4 rule delete table main suppress_prefixlength 0
[#] ip link delete dev peer1
[#] resolvconf -d tun.peer1 -f
[#] nft -f /dev/fd/63
```

## 结语

一通分析，你是否感觉到了 wg-quick 的实现十分巧妙，通过简单几行 iptables/nftables 与 iproute2 命令就在 WireGuard 隧道上实现了一个 VPN 网络，更妙的是只要把新增的这些 iptables/nftables 与 iproute2 规则删除，就能恢复到 WireGuard 未启动的状态，相当于整个工作是完全可逆的（显然前面的 `sudo wg-quick down peer1` 就是这么干的）。

其巧妙之处在于，它不需要修改主路由表，避免了在启动 WireGuard 客户端时需要删除掉原有的默认路由，也避免了在关闭 WireGuard 客户端时需要重新将旧的默认路由添加回来的麻烦。

总之这篇文章简单分析了 wireguard 虚拟网络在 Linux 上的实现，希望对你有所帮助。

下一篇文章（如果有的话...），我会带来更多的 WireGuard 实现细节，敬请期待。

## 参考

- [wireguard protocol](https://www.wireguard.com/protocol/)： 官方文档还有官方的白皮书，都写得很清晰易懂。
- [WireGuard到底好在哪？](https://zhuanlan.zhihu.com/p/404402933): 比较深入浅出的随想，值得一读。
- [Understanding modern Linux routing (and wg-quick)](https://ro-che.info/articles/2021-02-27-linux-routing): 对 WireGuard 客户端用到的多路由表与路由策略技术做了详细的介绍。
  - 它的中文翻译：[WireGuard 基础教程：wg-quick 路由策略解读 - 米开朗基扬](https://icloudnative.io/posts/linux-routing-of-wireguard/)

