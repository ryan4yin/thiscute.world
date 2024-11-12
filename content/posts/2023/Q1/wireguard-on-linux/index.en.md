---
title: "WireGuard on Linux - Part I"
date: 2023-03-28T22:19:25+08:00
lastmod: 2023-03-28T22:19:25+08:00
draft: true

featuredImage: "wireguard.png"
authors: ["ryan4yin"]

tags: ["WireGuard", "VPN", "Linux", "网络", "iptables", "conntrack"]
categories: ["tech"]
series: ["计算机网络相关"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

> Reading this article requires prior knowledge of Linux network basics, iptables, and
> conntrack.

> This article incorporates some prompts from Copilot and also includes analysis from
> ChatGPT's free version, which has been helpful.

Recently, due to work requirements, I delved into the WireGuard protocol and would like to
briefly share my insights in this article.

## What is WireGuard?

WireGuard is a VPN implementation based on minimalist principles that addresses many
existing issues with VPN protocols. It was designed and implemented by Jason A. Donenfeld
in 2015 and has gained widespread attention for its clean and easy-to-understand code,
simple configuration, high performance, and strong security.

In early 2020, WireGuard was introduced into the Linux mainline branch and later became a
kernel module in Linux 5.6. Following this, numerous open-source projects and related
enterprises based on WireGuard emerged. Major VPN service providers also gradually started
supporting the WireGuard protocol, and many businesses began using it to build enterprise
VPN networks.

Some notable open-source projects based on WireGuard include:

- [tailscale](https://github.com/tailscale/tailscale): A simple and easy-to-use WireGuard
  VPN private network solution, highly recommended!
- [headscale](https://github.com/juanfont/headscale): An open-source implementation of the
  tailscale control server, enabling the self-hosting of tailscale services.
- [kilo](https://github.com/squat/kilo): A WireGuard-based Kubernetes multi-cloud
  networking solution.
- ...
- Besides the ones mentioned above, there are many other WireGuard projects. If you're
  interested, you can explore the
  [awesome-wireguard](https://github.com/cedrickchee/awesome-wireguard) repository.

WireGuard itself is just a point-to-point tunneling protocol, providing the ability for
point-to-point communication (which reflects its minimalist philosophy). Other
functionalities such as network routing, NAT traversal, DNS resolution, and firewall
policies are all implemented using existing Linux system tools.

In this article, I will set up a simple single-server + single-client WireGuard network
and analyze how it utilizes existing Linux system tools to build a secure and reliable
virtual network over the WireGuard tunnel.

The servers and clients used for testing in this article are both virtual machines running
Ubuntu 20.04 with kernel version 5.15, which includes the wireguard kernel module.

## WireGuard Server Network Analysis

For simplicity, I will use `docker-compose` to start a WireGuard server, using the image
[linuxserver/docker-wireguard](https://github.com/linuxserver/docker-wireguard).

The configuration file is as follows, and the content is entirely referenced from the
official README of this image:

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
      - SERVERURL=auto # Automatically determines the server's external IP address, used when generating client configurations.
      - SERVERPORT=51820 # Port number on which the server listens.
      - PEERS=1 # Automatically generates 1 client configuration.
      - PEERDNS=auto # Automatically determines the client's DNS server address, also used when generating client configurations.
      - INTERNAL_SUBNET=10.13.13.0 # Subnet for the WireGuard virtual network.
      - ALLOWEDIPS=0.0.0.0/0 # This rule allows all clients in the virtual network to send traffic to this node.
      # Well-known NAT networks require sending periodic keep-alive packets to maintain the NAT table. This parameter, set to 'all', enables keep-alive for all clients.
      - PERSISTENTKEEPALIVE_PEERS=all
      - LOG_CONFS=true # Enable logging.
    volumes:
      - ./config:/config
      - /lib/modules:/lib/modules # Mounts the host's kernel modules into the container for loading the WireGuard kernel module.
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
```

Save the above configuration as `docker-compose.yml` and then start the WireGuard server
in the background using the following command:

```shell
docker-compose up -d
```

The WireGuard server is now running. Let's check the logs of the server container
(detailed comments added):

```shell
$ docker logs wireguard
# ...omitting some content
.:53                          # These lines of log show the startup of CoreDNS, providing the default DNS service for the virtual network.
CoreDNS-1.10.1                # In fact, CoreDNS is not mandatory; clients can use other DNS servers instead.
linux/amd64, go1.20, 055b2c3
[#] ip link add wg0 type wireguard   # Create a wireguard device.
[#] wg setconf wg0 /dev/fd/63        # Set the configuration for the wireguard device.
[#] ip -4 address add 10.13.13.1 dev wg0   # Add an IP address to the wireguard device.
[#] ip link set mtu 1420 up dev wg0        # Set the MTU for the wireguard device.
[#] ip -4 route add 10.13.13.2/32 dev wg0  # Add a route for peer1, with the address obtained from the `allowedIPs` parameter in the wireguard configuration.
# The following iptables commands add NAT rules to the wireguard device, making it the default gateway for the WireGuard virtual network.
# This allows other peers in the virtual network to access the external network through this default gateway.
[#] iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth+ -j MASQUERADE
[ls.io-init] done.
```

From the logs, we can see that the program first creates a WireGuard device `wg0` and
assigns the address `10.13.13.1` to it. As the server-side of the WireGuard network, this
`wg0` device serves as the default gateway for the entire WireGuard virtual network,
handling traffic from other peers within the virtual network and forming a star network
topology.

Next, the server adds a route for the peer it generated (`peer1` in this case), allowing
the peer's traffic to be correctly routed to the `wg0` device.

Finally, to enable other peers in the WireGuard virtual network to access the external
network or each other, the server adds the following iptables rules to the `wg0` device:

- `iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;`: Allow
  packets entering and exiting the `wg0` device to pass through the netfilter's FORWARD
  chain (the default rule is DROP, which means it does not allow packets to pass through
  by default).
- `iptables -t nat -A POSTROUTING -o eth

* -j
  MASQUERADE`: Add a MASQUERADE rule on the `eth+`network interface, which means the source addresses of the packets will be masked as the address of the`eth+`
  interface. This is to allow WireGuard packets to access the external network through
  NAT.
  - The return traffic will automatically pass through the NAT's conntrack RELATED rule,
    allowing it to pass through without explicit configuration. However, the conntrack
    table has an automatic cleanup mechanism, and if there is no traffic for a long time,
    the entry will be removed from the conntrack table. This is the issue addressed by the
    `PERSISTENTKEEPALIVE_PEERS=all` parameter in the `docker-compose.yml`, which keeps the
    connections alive by sending periodic keep-alive packets.
  - This also involves NAT traversal, which I won't delve into here, but you can explore
    it if you're interested.

WireGuard also introduces an essential concept called `AllowedIPs`, which is a list of IP
addresses indicating which IP addresses' traffic is allowed to pass through the WireGuard
virtual network. To illustrate this, let's first look at the server-side configuration
file for `wg0`:

```shell
$ cat wg0.conf
[Interface]
Address = 10.13.13.1
ListenPort = 51820
PrivateKey = kGZzt/CU2MVgq19ffXB2YMDSr6WIhlkdlL1MOeGH700=
# iptables rules added after the wg0 tunnel is up
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth+ -j MASQUERADE
# iptables rules removed after the wg0 tunnel is down
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth+ -j MASQUERADE

[Peer]
# peer1
PublicKey = HR8Kp3xWIt2rNdS3aaCk+Ss7yQqC9cn6h3WS6UK3WE0=
PresharedKey = 7mCNCZdMKeRz1Zrpl9bFS08jJAdv6/USazRVq7tjznY=
# AllowedIPs set to the virtual IP address of peer1, allowing peer1's traffic to pass through the WireGuard virtual network
AllowedIPs = 10.13.13.2/32
```

`AllowedIPs` represents the IP addresses or subnets allowed to pass through the WireGuard
virtual network for each peer. It can be a single IP address or a range, and multiple
entries can be set. This allows all peers to be responsible for forwarding one or more IP
ranges, effectively acting as routers for the VPN subnet.

WireGuard itself is just a point-to-point tunneling protocol, making it very versatile.
Through the `AllowedIPs` parameter, we can add different configurations and routing rules
for each peer, creating various complex network topologies, such as star, ring, tree, etc.

## WireGuard Client Network Analysis

Now, let's switch to another virtual machine to run the WireGuard client. First, we need
to install the `wireguard` command-line tool:

```shell
sudo apt install wireguard resolvconf
```

The second step is to find the `peer1/peer1.conf` file in the server's configuration
folder. It is the client configuration file automatically generated by the server
container based on the `PEERS=1` parameter. Let's first check its content:

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
# It is worth noting whether this Peer Endpoint IP address is correct
Endpoint = 192.168.5.198:51820
AllowedIPs = 0.0.0.0/0
```

> As an additional note, the address of this Endpoint is also worth mentioning. You can
> see from the server's wg0.conf configuration that peer1 is not assigned any specific
> Endpoint. This essentially means that the Endpoint of this peer1 is dynamic, i.e., each
> time peer1 sends data to the server's wg0, the server will use the source IP address of
> the data packet as the Endpoint for peer1 after authenticating and encrypting the data.
> This allows peer1 to change its IP address freely (Roaming), and the WireGuard tunnel
> will still function correctly (a typical scenario is frequent IP changes in mobile
> network roaming and WiFi switching). This gives WireGuard a distinct connectionless
> characteristic, meaning the WireGuard tunnel does not need to maintain a constant
> connection, and switching networks does not require reconnection. As long as the data
> packets can reach the server, the tunnel will work correctly.

Because my current environment is an intranet setup, I can directly use the server's
private IP address for the `Peer` - `Endpoint` in the configuration file, which is
`192.168.5.198`.

> If your server has a public IP address (e.g., a cloud server or using port forwarding
> with a dynamic public IP on a home broadband connection), you can also use that public
> IP address as the Endpoint, and the effect will be the same.

After confirming that the configuration file is correct, save it to the client's path
`/etc/wireguard/peer1.conf`, and then use the following command to start the WireGuard
client:

```shell
sudo wg-quick up peer1
```

The above command will automatically find the configuration file named `peer1.conf` in the
`/etc/wireguard/` directory, and then start a WireGuard device named `peer1` with the
corresponding configuration.

Here are the logs when I started it, and `wg-quick` prints all the network-related
commands it executed (detailed comments added):

```shell
$ sudo wg-quick up peer1
[#] ip link add peer1 type wireguard        # Create a WireGuard device named peer1.
[#] wg setconf peer1 /dev/fd/63             # Set the configuration for the peer1 device.
[#] ip -4 address add 10.13.13.2 dev peer1  # Assign an IP address to the peer1 device.
[#] ip link set mtu 1420 up dev peer1       # Set the MTU for the peer1 device.
[#] resolvconf -a tun.peer1 -m 0 -x  # Set DNS for the peer1 device, ensuring DNS works correctly.
[#] wg set peer1 fwmark 51820        # Set the firewall mark for the peer1 device to 51820, used to mark WireGuard outbound traffic.
                                     # In the subsequent routing policy, this mark will make the WireGuard outbound traffic use the default routing table.
[#] ip -4 route add 0.0.0.0/0 dev peer1 table 51820     # Create a separate routing table 51820 and forward all traffic to the peer1 interface.
[#] ip -4 rule add not fwmark 51820 table 51820         # Forward all traffic (ordinary traffic) without the 51820 mark to the newly created routing table 51820.
                                                        # In other words, all ordinary traffic is forwarded to the peer1 interface.
[#] ip -4 rule add table main suppress_prefixlength 0   # All traffic uses the main routing table (the default routing table), except traffic with a prefix length (mask) <= 0.
                                                        # Prefixes <= 0 only include 0.0.0.0/0, which is the default route. So, this means that all non-default routing policy traffic uses the main routing table.
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1        # Enable source address validation to prevent source address spoofing.
[#] nft -f /dev/fd/63                                   # Configure nftables rules to ensure WireGuard traffic is correctly routed and prevent malicious packets from entering the network.
```

After going through the above process, you should now be able to access the related
network through WireGuard. You can use WireShark to capture packets for confirmation.

> If the network is still not working, it means there is a problem with the configuration
> in one of the steps. You can troubleshoot it step by step by examining network
> interfaces, routing tables, routing policies, and iptables/nftables configurations. If
> necessary, you can use WireShark to capture packets and locate the issue.

Now, let's check the current system's network status. First, check the routing table, and
you will find that the routing table hasn't changed:

```shell
$ ip route ls
default via 192.168.5.201 dev eth0 proto static
192.168.5.0/24 dev eth0 proto kernel scope link src 192.168.5.197
```

However, the WireGuard tunnel is already active, indicating that the traffic is no longer
going directly through the default routing table. There are other configurations in
effect. Going back to the client startup logs, it shows that `wg-quick` created a routing
table named `51820`. Let's check this table:

```shell
ryan@ubuntu-2004-builder:~$ ip route ls table 51820
default dev peer1 scope link
```

As you can see, this table indeed forwards all traffic to the WireGuard interface `peer1`,
confirming that the traffic is now going through this routing table. So, the question is,
how is the system forwarding the traffic to this routing table? Why is the default routing
table no longer in effect?

To understand this, we need to add some knowledge. Linux has supported multiple routing
tables since version 2.2, and it uses a routing policy database to choose the correct
routing table for each packet. You can view and modify this routing policy database using
the `ip rule` command.

Now, let's take a look at the current routing policy of the system, and I have added
comments to explain it:

```shell
$ ip rule show
0:      from all lookup local   # 0 is the highest priority, `all` represents all traffic, and `lookup local` means looking up the local routing table.
32764:  from all lookup main suppress_prefixlength 0  # 32764 is currently the second-highest priority, it routes all traffic to the main routing table, but excludes the default route (prefix/mask <= 0).
                                                      # The purpose is to make all non-default routing policy traffic go through the main routing table.
                                                      # This rule was added by `wg-quick` when starting the tunnel.
32765:  not from all fwmark 0xca6c lookup 51820 # All traffic (ordinary traffic) without the 0xca6c mark (in hexadecimal format) is routed to the 51820 routing table.
                                                # This means it will be forwarded to the WireGuard `peer1` interface.
                                                # This rule was added by the `ip -4 rule add not fwmark 51820 table 51820` command earlier.
32766:  from all lookup main    # All traffic goes through the main routing table, but it is currently not in effect because the previous rules have higher priorities.
32767:  from all lookup default # All traffic goes through the default routing table, and it is also currently not in effect.
```

After analyzing the above routing policy, you should understand the WireGuard routing
rules. It added a rule with a higher priority than the default routing policy `32766`,
namely `32765`, which forwards all ordinary traffic to its custom routing table `51820`,
thus making it go through the `peer1` interface. On the other hand, the `peer1` interface
has been given a firewall mark `51820`, which is the hexadecimal format of `0xca6c`, so
outbound traffic from `peer1` to the server will not match the `32765` rule, and
therefore, it will go through the lower priority `32766` policy, i.e., it will go through
the main routing table.

In addition, the rule `

32764` is a bit special. It was explained in the previous comments—it ensures that all
non-default routing traffic goes through the main routing table, and the non-default
routes in the main routing table are usually managed automatically by other programs or
manually added, so this rule ensures that these routing policies are still effective and
not overridden by the WireGuard policy.

With the above analysis, the last line in the wg-quick log `nft -f /dev/fd/63` remains to
be explained. What exactly does it do? `nft` is the command-line tool for nftables. It
sets some nftables rules. Let's check its rules:

> Note: The chain names in nftables are entirely customizable and do not have any special
> meanings.

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

Here, a table named `wg-quick-peer1` is created, and it sets the following rules on the
netfilter:

1. `preraw` chain: This chain is used to prevent malicious packets from entering the
   network.
   1. The type line at the beginning of the rule indicates the type, which is `filter`,
      and it only matches the `prerouting` table of the `raw` chain.
   2. It drops all packets that are not from the `peer1` interface, have a destination
      address of `10.13.13.2`, and do not have a local source address.
   3. In summary, it allows only local addresses or the `peer1` interface to directly
      access the address `10.13.13.2`.
2. `premangle` chain: This chain ensures that all UDP packets can be correctly received
   from the WireGuard interface.
   1. It sets the connection tracking mark for all UDP packets (didn't quite understand
      how this mark is applied...).
3. `postmangle` chain: This chain ensures that all UDP packets can be correctly sent
   through the WireGuard interface.
   1. It sets the mark to `0xca6c` (in hexadecimal format) for all UDP packets (also not
      entirely clear how this mark is applied...).

Sure, here's the missing part:

## Final Check: WireGuard Status

Now, let's check the status of WireGuard. It was set earlier by the command
`wg setconf peer1 /dev/fd/63`:

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

With the analysis complete, now you can close the WireGuard client and restore the client
host's network to its normal state.

```shell
$ sudo wg-quick down peer1
[#] ip -4 rule delete table 51820
[#] ip -4 rule delete table main suppress_prefixlength 0
[#] ip link delete dev peer1
[#] resolvconf -d tun.peer1 -f
[#] nft -f /dev/fd/63
```

## Conclusion

After going through the analysis, do you feel that the implementation of `wg-quick` is
quite clever? With just a few iptables/nftables and iproute2 commands, it sets up a VPN
network on top of WireGuard. What's even more impressive is that simply removing these
added iptables/nftables and iproute2 rules will revert the system to its state before
WireGuard was started (as demonstrated by the `sudo wg-quick down peer1` command).

In summary, this article provides a brief analysis of the implementation of the WireGuard
virtual network on Linux, and I hope it has been helpful to you.

In the next article (if there is one...), I will delve into more details of WireGuard
implementation. Stay tuned!

## References

- [WireGuard Protocol](https://www.wireguard.com/protocol/): Official documentation and
  whitepaper, written in a clear and easy-to-understand manner.
- [WireGuard: What makes it special?](https://zhuanlan.zhihu.com/p/404402933): A deeper
  and easier-to-understand perspective, worth reading.
- [Understanding modern Linux routing (and wg-quick)](https://ro-che.info/articles/2021-02-27-linux-routing):
  Detailed explanation of the multiple routing tables and routing policy techniques used
  by the WireGuard client.
