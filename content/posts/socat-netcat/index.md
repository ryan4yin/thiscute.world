---
title: "Linux 网络工具中的瑞士军刀 - socat"
date: 2021-01-23T16:30:13+08:00
draft: true
---

## socat vs netcat

netcat(network cat) 是一个历史悠久的网络工具包，被称作 TCP/IP 的瑞士军刀，各大 Linux 发行版中都被默认安装。但是已经很久没更新了。(最新的是 2004 年。。)

而 socat(socket cat)，官方文档描述它是 `"netcat++" (extended design, new implementation)`，项目比较活跃，kubernetes-client(kubectl) 底层就是使用的它做各种流量转发。

## 安装方法

```shell
# Debian/Ubuntu
sudo apt install socat

# CentOS/RedHat
sudo yum install socat

# 其他发行版基本也都可以使用包管理器安装 socat
```


## 常用命令

### 1. 网络调试

连接远程端口，常用于检测远程端口是否打开：

```shell
socat - TCP:192.168.1.252:3306
```

监听一个 TCP 端口，常用于测试本机的端口是否能正常被外部访问：

```shell
socat TCP-LISTEN:7000 -
```

模拟一个 TLS 服务器，监听 443 端口：

```shell
socat OPENSSL-LISTEN:443,cert=/cert.pem -
```

## 2. 数据传输

通常传输文件时，我都习惯使用 scp/ssh/rsync，但是 socat 其实也能被用于传输文件。

以将 demo.tar.gz 从主机 A 发送到主机 B 为例，
首先在数据发送方 A 执行如下命令：

```shell
socat -u open:demo.tar.gz tcp-listen:2000,reuseaddr
```

然后在数据接收方 B 执行如下命令：

```shell
socat -u tcp:192.168.1.252:2000 open:demo.tar.gz,create
```



## 3. 端口转发


## 参考

- [用好你的瑞士军刀/netcat - 韦易笑 - 知乎](https://zhuanlan.zhihu.com/p/83959309)
- [socat - Multipurpose relay](http://www.dest-unreach.org/socat/)
