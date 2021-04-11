---
title: "Linux 网络工具中的瑞士军刀 - socat"
date: 2021-01-23T16:30:13+08:00
draft: false
---

## socat vs netcat

netcat(network cat) 是一个历史悠久的网络工具包，被称作 TCP/IP 的瑞士军刀，各大 Linux 发行版都有默认安装 openbsd 版本的 netcat，它的命令行名称为 `nc`.

而 socat(socket cat)，官方文档描述它是 `"netcat++" (extended design, new implementation)`，项目比较活跃，kubernetes-client(kubectl) 底层就是使用的它做各种流量转发。


## 一、简介

socat 的基本命令格式：

```shell
socat [参数] 地址1 地址2
```

给 socat 提供两个地址，socat 干的活就是把两个地址的流对接起来。左边地址的输出传给右边，同时又把右边地址的输出传给左边，也就是一个双向的数据管道。

听起来好像没啥特别的，但是实际上计算机网络干的活也就是数据传输而已，却影响了整个世界，不可小觑它的功能。

socat 支持非常多的地址类型：`-`/stdio，TCP, TCP-LISTEN, UDP, UDP-LISTEN, OPEN, EXEC, SOCKS, PROXY 等等，可用于端口监听、链接，文件和进程读写，代理桥接等等。

socat 的功能就是这么简单，命令行参数也很简洁，唯一需要花点精力学习的就是它各种地址的定义和搭配写法。

## 二、安装方法

各发行版都自带 netcat，包名通常为 `nc-openbsd`，因此这里只介绍 socat 的安装方法：

```shell
# Debian/Ubuntu
sudo apt install socat

# CentOS/RedHat
sudo yum install socat

# macOS
brew install socat
```

其他发行版基本也都可以使用包管理器安装 socat

## 三、常用命令

### 1. 网络调试

#### 1.1 检测远程端口的可连接性

>以前你可能学过如何用 telnet 来做这项测试，不过现在很多发行版基本都不自带 telnet 了，还需要额外安装。
telnet 差不多已经快寿终正寝了，还是建议使用更专业的 socat/netcat

使用 socat/netcat 将 stdin 发送给一个远程端口，检测远程端口的可连接性：

```shell
socat - TCP:192.168.1.252:3306

nc 192.168.1.252 3306
```

#### 1.2 测试本机端口是否能正常被外部访问（检测防火墙、路由等问题）

在本机监听一个 TCP 端口，接收到的内容传到 stdout，同时将 stdin 的输入传给客户端：

```shell
# 服务端启动命令
socat TCP-LISTEN:7000 -

# 客户端连接命令
socat TCP:192.168.31.123:7000 -
```

#### 1.3 调试 TLS 协议

模拟一个 TLS 服务器，监听 4433 端口，接收到的数据同样输出到 stdout：

```shell
# 服务端启动命令
socat openssl-listen:4433,reuseaddr,cert=$HOME/cert/server.pem,cafile=$HOME/cert/client.crt -

# 客户端连接命令
socat - openssl-connect:192.168.31.123:4433,cert=$HOME/cert/client.pem,cafile=$HOME/cert/server.crt 
```

## 2. 数据传输

通常传输文件时，我都习惯使用 scp/ssh/rsync，但是 socat 其实也可以传输文件。

以将 demo.tar.gz 从主机 A 发送到主机 B 为例，
首先在数据发送方 A 执行如下命令：

```shell
# -u 表示数据只从左边的地址单向传输给右边（socat 默认是一个双向管道）
# -U 和 -u 相反，数据只从右边单向传输给左边
socat -u open:demo.tar.gz tcp-listen:2000,reuseaddr
```

然后在数据接收方 B 执行如下命令，就能把文件接收到：

```shell
socat -u tcp:192.168.1.252:2000 open:demo.tar.gz,create
```

## 3. 担当临时的 web 服务器

使用 `fork` `reuseaddr` `EXEC` 三个命令，再用 `systemd`/`supervisor` 管理一下，就可以用几行命令实现一个简单的后台服务器。

待续

## 4. 透明代理

待续

## 参考

- [新版瑞士军刀：socat - 韦易笑 - 知乎](https://zhuanlan.zhihu.com/p/347722248)
- [用好你的瑞士军刀/netcat - 韦易笑 - 知乎](https://zhuanlan.zhihu.com/p/83959309)
- [socat - Multipurpose relay](http://www.dest-unreach.org/socat/)
