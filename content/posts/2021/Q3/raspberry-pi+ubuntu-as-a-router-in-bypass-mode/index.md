---
title: "在 Raspberry Pi 上安装 Ubuntu 并配置为旁路网关"
date: 2021-09-21T17:14:02+08:00
draft: true

resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Linux", "网络", "树莓派"]
categories: ["tech"]
series: ["计算机网络相关"]
---

最近换了个房子，才想起自动上次搞 iscsi 炸了之后（io 性能不够），我的树莓派 4b 已经吃灰好久
了。

另外我手上的小米 AX1800 虽然通过 ShellClash 配了个全局代理，但是它存储太小了，啥也干不了。

就还是想把树莓派 4B 整上，把 Clash 换到树莓派上装好，顺便用 Caddy 搭个简单的文件服务器，把
同样吃灰好久的硬盘盒接上去。

至于为什么不整 OpenWrt，显然是因为它不够通用，树莓派单纯用来搞个旁路由感觉有点浪费哈，如果
换成 Ubuntu 的话，无聊时也可以试试折腾下别的。

## 安装 Ubuntu Server

> 官方文
> 档：[tutorials/how-to-install-ubuntu-on-your-raspberry-pi](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview)

安装步骤很简单，使用 rpi-imager 直接傻瓜式安装。

稍微复杂点的是网络配置这一步，ubuntu server 在 boot 阶段使用 cloud-init 进行网络配置，对应
的配置文件为 `system-boot` 分区的 `network-config` 文件。

> cloud-init 主要被用在云虚拟机中，我曾经写过篇相关文章
> [https://github.com/ryan4yin/knowledge/blob/master/os/virutal%20machine/KVM/%E5%9C%A8%20QEMU%20%E4%B8%AD%E4%BD%BF%E7%94%A8%20cloud-init.md](https://github.com/ryan4yin/knowledge/blob/master/os/virutal%20machine/KVM/%E5%9C%A8%20QEMU%20%E4%B8%AD%E4%BD%BF%E7%94%A8%20cloud-init.md)

该文件的示例配置如下，注意换成你自己的静态 ip，如果希望使用 wifi 也请自行修改：

```yaml
# This file contains a netplan-compatible configuration which cloud-init
# will apply on first-boot. Please refer to the cloud-init documentation and
# the netplan reference for full details:
#
# https://cloudinit.readthedocs.io/
# https://netplan.io/reference
#
# Some additional examples are commented out below

version: 2
ethernets:
  eth0:
    dhcp4: false
    addresses:
      - 192.168.31.200/24
    gateway4: 192.168.31.1
    nameservers:
      addresses: [114.114.114.114, 223.5.5.5]
    optional: true
# wifis:
#  wlan0:
#    dhcp4: false
#    optional: true
#    access-points:
#      shadow_light_5G:
#        password: "xxx"
```

总之配置好后，把卡插到树莓派上，就能正常开机，然后根据配置启用并连接 eth0/wlan0 网卡，建议
使用静态 ip.

然后通过 ssh 连接：

```shell
# 默认账号和密码都是 ubuntu，登录完成后会要求你修改
$ ssh ubuntu@192.168.31.200
```

## 安装 Clash 并配置为 TUN 模式

网上大部分的资料教的都是通过 openwrt 的 web ui 进行旁路路由的配置，我们这里使用的是 ubuntu
server，自然就不适用了。

不过基本原理是一致的，我们首先安装 Clash 并配置为 TUN 模式。

## 修改默认网关为树莓派 IP

这个有两种方法：

- 全局模式：直接修改主路由的 DHCP 配置，把默认网关地址设为树莓派 IP，网络内的所有设备就默
  认走。
- 单机模式：只修改需要使用 Clash 的设备路由表，缺点是每个客户端都得这么改一遍。

首先，对于本机而言，需要首先开启包转发：

```shell
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p
```

```shell
sudo ip route change 0.0.0.0/0 via 198.18.0.1 dev utun
```
