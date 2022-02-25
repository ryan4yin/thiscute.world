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

迪菲-赫尔曼密钥交换（Diffie–Hellman Key Exchange）是一种安全协议，它可以让双方在完全没有对方任何预先信息的条件下通过不安全信道安全地协商出一个安全密钥，而且任何窃听者都无法得知密钥信息。
这个密钥可以在后续的通讯中作为对称密钥来加密通讯内容。

DHKE 可以抵抗嗅探攻击（窃听），但是无法抵挡中间人攻击（中继）。

DHKE 有两种实现方案：

- 传统的 DHKE 算法：使用离散对数实现
- 基于椭圆曲线密码学的 ECDH

为了理解 DHKE 如何实现在「大庭广众之下」安全地协商出密钥，我们首先使用色彩混合来形象地解释下它大致的思路。

跟编程语言的 Hello World 一样，密钥交换的解释通常会使用 Alice 跟 Bob 来作为通信双方。
现在他俩想要在公开的信道上，协商出一个**秘密色彩**出来，但是不希望其他任何人知道这个**秘密色彩**。他们可以这样做：

{{< figure src="/images/practical-cryptography-basics-5-key-exchange/key-exchange-by-mixing-color.jpg" >}}

分步解释如下：

- 首先 Alice 跟 Bob 沟通，确定一个**初始的色彩**，比如黄色。这个沟通不需要保密。
- 然后，Alice 跟 Bob 分别偷偷地选择出一个自己的**秘密色彩**，这个就得保密啦。
- 现在 Alice 跟 Bob，分别将**初始色彩**跟自己选择的**秘密色彩**混合，分别得到两个**混合色彩**。
- 之后，Alice 跟 Bob 再回到公开信道上，交换双方的**混合色彩**。
  - 我们假设在仅知道**初始色彩**跟**混合色彩**的情况下，很难推导出被混合的**秘密色彩**。这样第三方就猜不出 Bob 跟 Alice 分别选择了什么**秘密色彩**了。
- 最后 Alice 跟 Bob 再分别将**自己的秘密色彩**，跟**对方的混合色彩**混合，就得到了最终的**秘密色彩**。这个最终色彩只有 Alice 跟 Bob 知道，信道上的任何人都无法猜出来。


DHKE 协议也是基于类似的原理，但是使用的是离散对数（discrete logarithms）跟模幂（modular exponentiations ）而不是色彩混合。

### 1. 基于离散对数的 DHKE 协议

首先介绍下「模幂」，它是指求 $g$ 的 $a$ 次幂模 $p$ 的值 $c$ 的过程，其中 $g$ $a$ $c$ 均为整数，公式如下：

$$
g^a \mod p = c
$$

已知使用计算机计算上述「模幂」是非常快速的，但是求它的逆运算——即离散对数，在已知 $g$ $p$ $c$ 的情况下，求幂指数 $a$——却是非常难的。

下面该轮到 Alice 跟 Bob 出场来介绍 DHKE 的过程了，先看图（下面<span style="color:green">绿色</span>表示非秘密信息，<span style="color:red">**红色**</span>表示秘密信息）：

{{< figure src="/images/practical-cryptography-basics-5-key-exchange/diffle-hellman.png" >}}

- Alice 跟 Bob 协定使用两个比较独特的正整数 <span style="color:green">$p$</span> 跟 <span style="color:green">$g$</span>
  - 假设 <span style="color:green">$p=23$, $g=5$</span>
- Alice 选择一个秘密整数 <span style="color:red">$a$</span>，计算 <span style="color:green">$A$</span>$\ = g^a \mod p$ 并发送给 Bob
  - 假设 <span style="color:red">$a=4$</span>，则 <span style="color:green">$A$</span>$\ = 5^4 \mod 23 = 4$
- Bob 也选择一个秘密整数 <span style="color:red">$b$</span>，计算 <span style="color:green">$B$</span>$\ = g^b \mod p$ 并发送给 Alice
  - 假设 <span style="color:red">$b=3$</span>，则 <span style="color:green">$B$</span>$\ = 5^3 \mod 23 = 10$
- Alice 计算  $S_1 = B^a \mod p$
  - $S_1 = 10^4 \mod 23 = 18$
- Bob 计算 $S_2 = A^b \mod p$
  - $S_2 = 4^3 \mod 23 = 18$
- 已知 $B^a \mod p = g^{ab} \mod p = A^b \mod p$，因此 <span style="color:red">$S_1 = S_2 = S$</span> 
- 这样 Alice 跟 Bob 就协商出了密钥 <span style="color:red">$S$</span>
- 因为离散对数的计算非常难，任何窃听者都几乎不可能通过公开的 <span style="color:green">$p$ $g$ $A$ $B$</span> 逆推出 <span style="color:red">$S$</span> 的值

在最常见的 DHKE 实现中（[RFC3526](https://tools.ietf.org/html/rfc3526)），基数是 $g = 2$，模数 $$ 是一个 1536 到 8192 比特的大素数。
而整数 <span style="color:green">$p$ $g$ $A$ $B$</span> 通常会使用非常大的数字（1024、2048 或 4096 比特甚至更大）以防范暴力破解。


DHKE 协议基于 Diffie-Hellman 问题的实际难度，这是计算机科学中众所周知的离散对数问题（DLP）的变体，目前还不存在有效的算法。

### 2. 基于椭圆曲线的 ECDH 协议

Elliptic-Curve Diffie-Hellman (ECDH) 是一种匿名密钥协商协议，它允许两方，每方都有一个椭圆曲线公钥-私钥对，它的功能也是让双方在完全没有对方任何预先信息的条件下通过不安全信道安全地协商出一个安全密钥。

ECDH 是经典 DHKE 协议的变体，其中模幂计算被椭圆曲线计算取代，以提高安全性。
我会在后面非对称密码系统的 ECC 部分详细介绍它。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

