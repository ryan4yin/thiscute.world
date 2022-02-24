---
title: "「译」写给开发人员的实用密码学（五）—— 密钥交换与 DHKE"
date: 2022-02-25T00:14:00+08:00
draft: true
resources:
- name: "featured-image"
  src: "key-exchange.png"

tags: ["Cryptography", "密码学", "密钥交换", "安全"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文仍然在优化翻译质量、补充原文缺失的细节，不建议阅读！

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]


## 一、前言

在密码学中**密钥交换**是一种协议，功能是在两方之间安全地交换加密密钥，其他任何人都无法获得密钥的副本。通常各种加密通讯协议的第一步都是密钥交换。
密钥交换技术具体来说有两种方案：

- 密钥协商：协议中的双方都参与了共享密钥的生成，两个代表算法是 Diffie-Hellman (DHKE) 和 Elliptic-Curve Diffie-Hellman (ECDH)
- 密钥传输：双方中其中一方生成出共享密钥，并通过此方案将共享密钥传输给另一方。密钥传输方案通常都通过公钥密码系统实现。比如在 RSA 密钥交换中，客户端使用它的私钥加密一个随机生成的会话密钥，然后将密文发送给服务端，服务端再使用它的公钥解密出会话密钥。

密钥交换协议无时无刻不在数字世界中运行，在你连接 WiFi 时，或者使用 HTTPS 协议访问一个网站，都会执行密钥交换协议。
密钥交换可以基于匿名的密钥协商协议如 DHKE，一个密码或预共享密钥，一个数字证书等等。有些通讯协议只在开始时交换一次密钥，而有些协议则会随着时间的推移不断地交换密钥。

认证密钥交换（AKE）是一种会同时认证相关方身份的密钥交换协议，比如个人 WiFi 通常就会使用 password-authenticated key agreement (PAKE)，而如果你连接的是公开 WiFi，则会使用匿名密钥交换协议。

目前有许多用于密钥交换的密码算法。其中一些使用公钥密码系统，而另一些则使用更简单的密钥交换方案（如 Diffie-Hellman 密钥交换）；其中有些算法涉及服务器身份验证，也有些涉及客户端身份验证；其中部分算法使用密码，另一部分使用数字证书或其他身份验证机制。下面列举一些知名的密钥交换算法：

- Diffie-Hellman Key Exchange (DHКЕ) ：传统的、应用最为广泛的密钥交换协议
- 椭圆曲线 Diffie-Hellman (ECDH)
- RSA-OAEP 和 RSA-KEM（RSA 密钥传输）
- PSK（预共享密钥）
- SRP（安全远程密码协议）
- FHMQV（Fully Hashed Menezes-Qu-Vanstone）
- ECMQV（Ellictic-Curve Menezes-Qu-Vanstone）
- CECPQ1（量子安全密钥协议）

## 二、Diffie–Hellman 密钥交换



### 

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

