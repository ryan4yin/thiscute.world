---
title: "Linux 网络工具中的瑞士军刀 - socat & netcat"
date: 2021-04-11T16:38:13+08:00
draft: false

resources:
  - name: "featured-image"
    src: "yume_grimgar.webp"

tags: ["网络", "Linux", "网络调试"]
categories: ["tech"]
series: ["计算机网络相关"]
---

> 文中的命令均在 macOS Big Sure 和 openSUSE Tumbleweed 上测试通过

## socat & netcat

netcat(network cat) 是一个历史悠久的网络工具包，被称作 TCP/IP 的瑞士军刀，各大 Linux 发行版都有默认安装 openbsd 版本的 netcat，它的命令行名称为 `nc`.

而 [socat(socket cat)](https://github.com/3ndG4me/socat)，官方文档描述它是 `"netcat++" (extended design, new implementation)`，项目比较活跃，kubernetes-client(kubectl) 底层就是使用的它做各种流量转发。

在不方便安装 socat 的环境中，我们可以使用系统自带的 netcat.
而在其他环境，可以考虑优先使用 socat.

## 一、简介

socat 的基本命令格式：

```shell
socat [参数] 地址1 地址2
```

给 socat 提供两个地址，socat 干的活就是把两个地址的流对接起来。左边地址的输出传给右边，同时又把右边地址的输出传给左边，也就是一个**双向的数据管道**。

听起来好像没啥特别的，但是实际上计算机网络干的活也就是数据传输而已，却影响了整个世界，不可小觑它的功能。

socat 支持非常多的地址类型：`-`/stdio，TCP, TCP-LISTEN, UDP, UDP-LISTEN, OPEN, EXEC, SOCKS, PROXY 等等，可用于端口监听、链接，文件和进程读写，代理桥接等等。

socat 的功能就是这么简单，命令行参数也很简洁，唯一需要花点精力学习的就是它各种地址的定义和搭配写法。

而 netcat 定义貌似没这么严谨，可以简单的理解为网络版的 cat 命令 2333

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

### 1. 检测远程端口的可连接性

> 很多人会用 telnet 来做这项测试，不过现在很多发行版基本都不自带 telnet 了，还需要额外安装。
> telnet 差不多已经快寿终正寝了，还是建议使用更专业的 socat/netcat

使用 socat/netcat 检测远程端口的可连接性：

```shell
# -d[ddd] 增加日志详细程度，-dd  Prints fatal, error, warning, and notice messages.
socat -dd - TCP:192.168.1.252:3306

# -v 显示详细信息
# -z 不发送数据，效果为立即关闭连接，快速得出结果
nc -vz 192.168.1.2 8080

# -vv 显示更详细的内容
# -w2 超时时间设为 2 秒
# 使用 nc 做简单的端口扫描
nc -vv -w2 -z 192.168.1.2 20-500
```

### 2. 测试本机端口是否能被外部访问

在本机监听一个 TCP 端口，接收到的内容传到 stdout，同时将 stdin 的输入传给客户端：

```shell
# 服务端启动命令，socat/nc 二选一
socat TCP-LISTEN:7000 -
# -l --listening
nc -l 7000
# 当然也可以使用 python3（注意文件安全性）
# 此命令在 7000 端口启用一个文件服务器，绑定到 0.0.0.0，以当前目录为根目录
python3 -m http.server 7000
# 或者在较老的机器上可以用 python2（注意文件安全性）
python -m SimpleHTTPServer 8000

# 客户端连接命令，socat/nc 二选一
socat TCP:192.168.31.123:7000 -
nc 192.168.11.123 7000
```

UDP 协议的测试也非常类似，使用 netcat 的示例如下：

```shell
# 服务端，只监听 ipv4
nc -u -l 8080

# 客户端
nc -u 192.168.31.123 8080
# 客户端本机测试，注意 localhost 会被优先解析为 ipv6! 这会导致服务端(ipv4)的 nc 接收不到数据！
nc -u localhost 8080
```

使用 socat 的 UDP 测试示例如下：

```shell
socat UDP-LISTEN:7000 -

socat UDP:192.168.31.123:7000 -
```

### 3. 调试 TLS 协议

> 参考 socat 官方文档：[Securing Traffic Between two Socat Instances Using SSL](http://www.dest-unreach.org/socat/doc/socat-openssltunnel.html)

> 测试证书及私钥的生成参见 [写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议](/posts/about-tls-cert/)

模拟一个 mTLS 服务器，监听 4433 端口，接收到的数据同样输出到 stdout：

```shell
# socat 需要使用同时包含证书和私钥的 pem 文件，生成方法如下
cat server.key server.crt > server.pem
cat client.key client.crt > client.pem

# 服务端启动命令
socat openssl-listen:4433,reuseaddr,cert=server.pem,cafile=client.crt -

# 客户端连接命令（使用系统的 ca.crt 或者你自己的私有 ca.cert 来验证服务端证书）
socat - openssl-connect:192.168.31.123:4433,cert=client.pem,cafile=ca.crt
# 或者使用 curl 连接（ca.crt 证书来源同上）
curl -v --cacert ca.crt --cert client.crt --key client.key --tls-max 1.2 https://192.168.31.123:4433
```

上面的命令使用了 mTLS 双向认证的协议，可通过设定 `verify=0` 来关掉客户端认证，示例如下：

```shell
# socat 需要使用同时包含证书和私钥的 pem 文件，生成方法如下
cat server.key server.crt > server.pem

# 服务端启动命令
socat openssl-listen:4433,reuseaddr,cert=server.pem,verify=0 -

# 客户端连接命令，如果 ip/域名不受证书保护，就也需要添加 verify=0
# （使用系统的 ca.crt 或者你自己的私有 ca.cert 来验证服务端证书）
socat - openssl-connect:192.168.31.123:4433,cafile=ca.crt
# 或者使用 curl 连接（ca.crt 证书来源同上）
curl -v --cacert ca.crt https://192.168.31.123:4433
```

### 4. 数据传输

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
# 如果觉得太繁琐，也可以直接通过 stdout 重定向
socat -u tcp:192.168.1.252:2000 - > demo.tar.gz
```

使用 netcat 也可以实现数据传输：

```shell
# 先在接收方启动服务端
nc -l -p 8080 > demo.tar.gz
# 再在发送方启动客户端发送数据
nc 192.168.1.2 8080 < demo.tar.gz
```

### 5. 担当临时的 web 服务器

使用 `fork` `reuseaddr` `SYSTEM` 三个命令，再用 `systemd`/`supervisor` 管理一下，就可以用几行命令实现一个简单的后台服务器。

下面的命令将监听 8080 端口，并将数据流和 web.py 的 stdio 连接起来，可以直接使用浏览器访问 `http://<ip>:8080` 来查看效果。

```shell
socat TCP-LISTEN:8080,reuseaddr,fork SYSTEM:"python3 web.py"
```

假设 `web.py` 的内容为（注意 print 的内容要与 HTTP 协议格式一致）：

```python
print("""HTTP/1.1 200 OK
Content-Type: text/plain

hello world
""")
```

那 `curl localhost:8080` 就应该会输出 `hello world`

当然，如果你仅希望快速提供一个文件服务器，也可直接使用 python 命令：

```shell
# https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler.do_GET
python3 -m http.server 8000 --directory /tmp/

# 或者在旧机器上可以直接使用 python2 提供文件服务器，默认以当前文件夹为根目录
python -m SimpleHTTPServer 8000
```

### 6. 端口转发

监听 8080 端口，建立该端口与 `baidu.com:80` 之间的双向管道:

```shell
socat TCP-LISTEN:8080,fork,reuseaddr  TCP:baidu.com:80
```

拿 curl 命令测试一下，应该能正常访问到百度：

```shell
# 注意指定 Host
curl -v -H 'Host: baidu.com' localhost:8080
```

其他用法，比如为一个仅监听了 `127.0.0.1` loopback 网卡的服务，允许通过外部网络访问（注意安全性）：

```shell
socat TCP-LISTEN:5432,fork,reuseaddr  TCP:localhost:3658
```

### 7. 端口扫描

netcat 支持简单的端口扫描功能，如下示例扫描 192.168.1.2 从 8000 到 9000 的所有端口号：

```
# -w 指定连接超时时间（秒）
# -z 只扫描正在监听的 daemons，不向其发送任何数据
nc -vv -w3 -z 192.168.1.2 8000-9000
```

socat 貌似不支持这项功能，估计是更建议使用专业的 nmap 吧。

### 其他

socat 还提供了丰富的 examples 与 tutorials，介绍了许多其他用法，包括：

- [Building TUN based virtual networks with socat](http://www.dest-unreach.org/socat/doc/socat-tun.html): 构造 TUN 虚拟网卡
- [IP Multicasting with Socat](http://www.dest-unreach.org/socat/doc/socat-multicast.html): 支持 IP 包广播，将管道另一端设为一个 CIDR 网段
- etc...

详见官方文档：

- [socat - Multipurpose relay](http://www.dest-unreach.org/socat/)
- [nc-openbsd man page](https://man.openbsd.org/nc.1)

## 参考

- [新版瑞士军刀：socat - 韦易笑 - 知乎](https://zhuanlan.zhihu.com/p/347722248)
- [用好你的瑞士军刀/netcat - 韦易笑 - 知乎](https://zhuanlan.zhihu.com/p/83959309)
- [socat - Multipurpose relay](http://www.dest-unreach.org/socat/)
