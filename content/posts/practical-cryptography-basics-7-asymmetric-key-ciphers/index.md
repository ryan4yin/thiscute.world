---
title: "「译」写给开发人员的实用密码学（七）—— 非对称密钥加密算法"
date: 2022-03-01T21:34:00+08:00
draft: true
resources:
- name: "featured-image"
  src: "symmetric-vs-asymmetric.jpg"

tags: ["Cryptography", "密码学", "非对称加密", "安全"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文仍然在优化翻译质量、补充原文缺失的细节、代码示例。

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，但是笔者也补充了许多代码示例及算法细节。


《写给开发人员的实用密码学》系列文章目录：

- [「译」写给开发人员的实用密码学（一）—— 概览](/posts/practical-cryptography-basics-1/)
- [「译」写给开发人员的实用密码学（二）—— 哈希函数](/posts/practical-cryptography-basics-2-hash/)
- [「译」写给开发人员的实用密码学（三）—— MAC 与密钥派生函数 KDF](/posts/practical-cryptography-basics-3-key-derivation-function/)
- [「译」写给开发人员的实用密码学（四）—— 安全的随机数生成器](/posts/practical-cryptography-basics-4-secure-random-generators/)
- [「译」写给开发人员的实用密码学（五）—— 密钥交换与 DHKE](/posts/practical-cryptography-basics-5-key-exchange/)
- [「译」写给开发人员的实用密码学（六）—— 对称密钥加密算法](/posts/practical-cryptography-basics-6-symmetric-key-ciphers/)
- [「译」写给开发人员的实用密码学（七）—— 非对称密钥加密算法](/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/)
- 待续

## 一、公钥密码学 / 非对称密码学

在介绍非对称密钥加密方案和算法之前，我们首先要了解公钥密码学的概念。

### 密码学的历史

从第一次世界大战、第二次世界大战到 1976 年这段时期密码的发展阶段，被称为「近代密码阶段」。
在近代密码阶段，所有的密码系统都使用对称密码算法——使用相同的密钥进行加解密。
当时使用的密码算法在拥有海量计算资源的现代人看来都是非常简单的，我们经常看到各种讲述一二战的谍战片，基本都包含破译电报的片段。

密码学的发展甚至直接影响了二战的战局。

1943 年，美国从破译的日本电报中得知山本五十六将于 4 月 18 日乘中型轰炸机，由 6 架战斗机护航，到中途岛视察时，美国总统罗斯福亲自做出决定截击山本，山本乘坐的飞机在去往中途岛的路上被美军击毁，日本的战争天才山本五十六机毁人亡，日本海军从此一蹶不振。

在二次世界大战中，印第安纳瓦霍土著语言被美军用作密码，美国二战时候特别征摹使用印第安纳瓦霍通信兵。在二次世界大战日美的太平洋战场上，美国海军军部让北墨西哥和亚历桑那印第安纳瓦霍族人使用纳瓦霍语进行情报传递。纳瓦霍语的语法、音调及词汇都极为独特，不为世人所知道，当时纳瓦霍族以外的美国人中，能听懂这种语言的也就一二十人。这是**密码学**和**语言学**的成功结合，纳瓦霍语密码成为历史上从未被破译的密码。

在 1976 年 Malcolm J. Williamson 公开发表了现在被称为「Diffie–Hellman 密钥交换, DHKE」的算法，并提出了「公钥密码学」的概念，这宣告了「近代密码阶段」的终结。

言归正传，对称密码算法的问题有两点：

- 「**需要安全的通道进行密钥交换**」，早期最常见的是面对面交换密钥
- 每个点对点通信都需要使用不同的密钥，**密钥的管理会变得很困难**
  - 如果你需要跟 100 个朋友安全通信，你就要维护 100 个不同的对称密钥，而且还得确保它们不泄漏。

这会导致巨大的「密钥交换」跟「密钥保存与管理」的成本。「公钥密码学」最大的优势就是，它解决了这两个问题：

- 「公钥密码学」可以在**不安全的信道**上安全地进行密钥交换，第三方即使监听到通信过程，但是（几乎）无法破解出密钥。
- 每个人只需要公开自己的公钥，就可以跟其他任何人安全地通信。
  - 如果你需要跟 100 个朋友安全通信，你们只需要公开自己的公钥。发送消息时使用对方的公钥加密，接收消息时使用自己的公钥解密即可。
  - 只有你自己的私钥需要保密，所有的公钥都可以公开，这就显著降低了密钥的维护成本。

因此公钥密码学成为了现代密码学的基石，而「公钥密码学」的诞生时间 1976 年被认为是现代密码学的开端。


### 公钥密码学的概念

公钥密码系统的密钥始终以公钥 + 私钥对的形式出现，公钥密码系统提供数学框架和算法来生成公钥+私钥对。
公钥通常与所有人共享，而私钥则保密。
公钥密码系统在设计时就确保了几乎不可能从其公开的公钥逆向演算出对应的私钥。

公钥密码系统主要有三大用途：**加密与解密、签名与验证、密钥交换**。
每种算法都需要使用到公钥和私钥，比如由公钥加密的消息只能由私钥解密，由私钥签名消息需要用公钥验证。

由于加密解密、签名验证均需要两个不同的密钥，故「公钥密码学」也被称为「**非对称密码学**」。

比较著名的公钥密码系统有：RSA、ECC（椭圆曲线密码学）、ElGamal、Diffie-Hellman、ECDH、ECDSA 和 EdDSA。许多密码算法都基于这些密码系统的原语，例如 RSA 签名、RSA 加密/解密、ECDH 密钥交换以及 ECDSA 和 EdDSA 签名。

一张图列出所有流行的公钥密码学算法：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/asymmetric-cryptography.png" >}}


### 量子安全性

>参考文档：https://en.wikipedia.org/wiki/Post-quantum_cryptography

目前流行的公钥密码系统基本都依赖于 IFP（整数分解问题）、DLP（离散对数问题）或者 ECDLP（椭圆曲线离散对数问题），这导致这些算法都是**量子不安全**（quantum-unsafe）的。

如果人类进入量子时代，IFP / DLP / ECDLP 的难度将大大降低，目前流行的 RSA、ECC、ElGamal、Diffie-Hellman、ECDH、ECDSA 和 EdDSA 等公钥密码算法都将被淘汰。

目前已经有一些量子安全的公钥密码系统问世，但是因为它们需要更长的密钥、更长的签名等原因，目前还未被广泛使用。

一些量子安全的公钥密码算法举例：NewHope、NTRU、GLYPH、BLISS、XMSS、[Picnic](https://github.com/Microsoft/Picnic) 等，有兴趣的可以自行搜索相关文档。

## 二、非对称加密方案简介

非对称加密要比对称加密复杂，有如下几个原因：

- 使用密钥对进行加解密，导致其算法更为复杂
- 只能加密/解密很短的消息
  - 在 RSA 系统中，输入消息应该被转换为大整数（例如使用 OAEP 填充），然后才能进行加密。
- 一些非对称密码系统（如 ECC）不直接提供加密原语，需要结合使用更复杂的方案才能实现加解密

此外，非对称密码比对称密码慢非常多。比如 RSA 加密比 AES 慢 1000 倍，跟 ChaCha20 就更没法比了。

为了解决上面提到的这些困难并支持加密任意长度的消息，现代密码学使用「**非对称加密方案**」来实现消息加解密。
又因为「对称加密方案」具有速度快、支持加密任意长度消息等特性，「非对称加密方案」通常直接直接组合使用**对称加密算法**与**非对称加密算法**。比如「密钥封装机制 KEM（key encapsulation mechanisms)）」与「集成加密方案 IES（Integrated Encryption Scheme）」

### 1. 密钥封装机制 KEM

密钥封装机制 KEM 的加密流程（使用公钥加密传输对称密钥）：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/asymmetric-cryptography.png" >}}

密钥封装机制 KEM 的解密流程（使用私钥解密出对称密钥，然后再使用这个对称密钥解密数据）：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/asymmetric-cryptography.png" >}}

RSA-OAEP, RSA-KEM, ECIES-KEM 和 PSEC-KEM. 都是 KEM 加密方案。

#### 密钥封装（Key encapsulation）与密钥包裹（Key wrapping）

主要区别在于使用的是对称加密算法、还是非对称加密算法：

- 密钥封装（Key encapsulation）指使用非对称密码算法的公钥加密另一个密钥。
- 密钥包裹（Key wrapping）指使用对称密码算法加密另一个密钥。

### 2. 集成加密方案 IES

集成加密方案 (IES) 在 密钥封装机制（KEM）的基础上，添加了密钥派生算法 KDF、消息认证算法 MAC 等其他密码学算法以达成更高的安全性。

在 IES 方案中，非对称算法（如 RSA 或 ECC）跟 KEM 一样，都是用于加密或封装对称密钥，然后通过对称密钥（如 AES 或 Chacha20）来加密输入消息。

DLIES（离散对数集成加密方案）和 ECIES（椭圆曲线集成加密方案）都是 IES 方案。

## 三、RSA 密码系统

RSA 密码系统是最早的公钥密码系统之一，它基于 RSA 问题和整数分解问题 （IFP）的计算难度。
RSA 算法以其作者（Rivest–Shamir–Adleman）的首字母命名。

RSA 算法在计算机密码学的早期被广泛使用，至今仍然是数字世界应用最广泛的密码算法。
但是随着 ECC 密码学的发展，ECC 正在非对称密码系统中慢慢占据主导地位，因为它比 RSA 具有更高的安全性和更短的密钥长度。

RSA 算法提供如下几种功能：

- 密钥对生成：生成随机私钥（通常大小为 1024-4096 位）和相应的公钥。
- 加密解密：使用公钥加密消息（消息要先转换为 [0...key_length] 范围内的整数），然后使用密钥解密。
- 数字签名：签署消息（使用私钥）和验证消息签名（使用公钥）。
  - 数字签名实际上是通过 Hash 算法 + 加密解密功能实现的。后面会介绍到，它与一般加解密流程的区别，在于数字签名使用私钥加密，再使用公钥解密。
- 密钥交换：安全地传输密钥，用于以后的加密通信。

RSA 可以使用不同长度的密钥：1024、2048、3072、4096、8129、16384 甚至更多位。目前 **3072** 位及以上的密钥长度被认为是安全的，曾经大量使用的 **2048** 位 RSA 现在被破解的风险在不断提升，已经不推荐使用了。

更长的密钥提供更高的安全性，但会消耗更多的计算时间，因此需要在安全性和速度之间进行权衡。
非常长的 RSA 密钥（例如 50000 位或 65536 位）对于实际使用可能太慢，例如密钥生成可能需要几分钟到几个小时。

### RSA 密钥对生成

RSA 密钥对的生成跟前面介绍的「DHKE 密钥交换算法」会有些类似，但是要更复杂一点。

首先看下我们怎么使用 openssl 生成一个 2048 位的 RSA 密钥对：

>[OpenSSL](https://github.com/openssl/openssl) 是目前使用最广泛的网络加密算法库，支持非常多流行的现代密码学算法，几乎所有操作系统都会内置 openssl.

```shell
# 生成 2048 位的 RSA 私钥
❯ openssl genrsa -out rsa-private-key.pem 2048
Generating RSA private key, 2048 bit long modulus
.................+++
.....+++
e is 65537 (0x10001)

# 查看私钥内容
❯ cat rsa-private-key.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAtHpn91b6HUGvIpGsoZJbwE3vQb42FguTBSNRHNITQG8ztiyf
Nt7JEyHLnzi9Ta+exRa6eqhnKf8pm5Cdrf/YbGjpbkiXFS6pOGM5kDvNc2Z+5/BN
KyfDoCc/m7vptHWfDJwPTFE3/Qt2/M/rFNpMsm2cLqO55RWqH/4Z0qQ4SSzbE1hS
T7QRuoLhJDibJSz2Z+jwefz2tzRyjQZOpRGEjYQ9fyyNuIKYMPo3UjytN/7Uu2zq
mi0pYv3bFSo8lAYAKReAHcqWJ5q9wusjWKpS8dmEV3zqiiKYZz1gpuv/lZ7ajFy6
OV9FjJuWGaP20uRwQVbYg8GFH6gLNeLGgJXvTQIDAQABAoIBAB1MTbpiXUIImrTC
70JfbxOd0zxZ84/KmzhXTmCeXc+0/bESN1qB+iRn9RVI8bo9y0l1chpdYjn4GToO
1PodMXYP5e0oTZZ7t67WtM6MVsLoHavrX6ukzeYe2P2gGMVZ3tL+NqGOAcfLZ6qM
2j3NXmwMzTDpFVFyHecJqgl+7UA7iRkQMcNf8e09VywwEuI95Ba7SlOpfDvZILBJ
gPd2YVlZRxQVnyZDGf5CCRlml3dCzQ+l/mPUvrtXiSyWuwy4TO+tbzd1rWCW33Bb
3zd25YGi1B2LMaXMplfwd3C+7vV712sy9UxBekMrEkCGYlu7U3H94lifs9KHIA4r
x2koJMECgYEA3JzfrrhfX2Ek4RJDr5zc2QUcF0nPqhPQoiZ+aOp9wjxQgFUVUlbR
dDHsWkBRH4Ids/BxydF8Hd27HNX3dEDKqL2+MnsELP8Z9e0vUjgA84BXKo4FIzEy
Vq/r9lWEMR+n4/cu0vOmvcplYBl0XswsogoKkRAhCaJoiqAhKSgP510CgYEA0W13
Acgi7aiS//YP/RD+LKBkDiBrq/EBrLS6o47Y8WnyftWEwihxAhVudy3jWfrV+r1J
w1qUKBSePXY7PLREX4dljbdyfCk+MwDYlOpTclf4jSCQ/dMrHCP24iTI58nZ38VF
YFloxmbQj6q/wSuQrQCSdgY2w/WugyDjn/hbWLECgYEAhvPHuT+7x8LLJotfsFuK
lY8UogJa8DVy2N4nUdKv31O6AucJRfcp5aRsasERXu7fcKVTVhu5iyOKRJd26jyA
PDzlzkeGRGhA3zmaSvdLTaliqPt7lQ2RN4oiE+w4EzzEHSWmFRFLHKpk3SZ1E1Be
tTjjQd3V9+jLfpF59400PVkCgYAAnEAPikTHyoj7I/1x8F29RY5lGCUYMDCgDzrI
BT+OnI9vXTHw2utRZTyYLlMOTRPYkjqnzhjGcSDw7upHSAM3AA8Etbcos3oR7fuz
m2c42xbHWoPxqW7juxsaF59aRZVT+KA2IqySf3Q2Jvo+FuFqD6ldnLEGKy4iBbOE
INYrUQKBgBC8u0Sd7tPF5jEg+9QsBgsmSuB9pl9GRRfQrB6lAbgUgAqR2E5OMrWt
wJHsN9/gImTE9OOrg4/r6pbIxukb7jp8p+MPi7tOVon0tWQs5mLwUQm/xI8h5juS
eA9m5i6NaDNLgFQvf/XsRJpqe3+7zFH7zz5+Fjlr6aXC3BcPXKOk
-----END RSA PRIVATE KEY-----

# 查看私钥的详细参数
❯ openssl rsa -noout -text -in rsa-private-key.pem
Private-Key: (2048 bit)
modulus:
    00:b4:7a:67:f7:56:fa:1d:41:af:22:91:ac:a1:92:
    5b:c0:4d:ef:41:be:36:16:0b:93:05:23:51:1c:d2:
    13:40:6f:33:b6:2c:9f:36:de:c9:13:21:cb:9f:38:
    bd:4d:af:9e:c5:16:ba:7a:a8:67:29:ff:29:9b:90:
    9d:ad:ff:d8:6c:68:e9:6e:48:97:15:2e:a9:38:63:
    39:90:3b:cd:73:66:7e:e7:f0:4d:2b:27:c3:a0:27:
    3f:9b:bb:e9:b4:75:9f:0c:9c:0f:4c:51:37:fd:0b:
    76:fc:cf:eb:14:da:4c:b2:6d:9c:2e:a3:b9:e5:15:
    aa:1f:fe:19:d2:a4:38:49:2c:db:13:58:52:4f:b4:
    11:ba:82:e1:24:38:9b:25:2c:f6:67:e8:f0:79:fc:
    f6:b7:34:72:8d:06:4e:a5:11:84:8d:84:3d:7f:2c:
    8d:b8:82:98:30:fa:37:52:3c:ad:37:fe:d4:bb:6c:
    ea:9a:2d:29:62:fd:db:15:2a:3c:94:06:00:29:17:
    80:1d:ca:96:27:9a:bd:c2:eb:23:58:aa:52:f1:d9:
    84:57:7c:ea:8a:22:98:67:3d:60:a6:eb:ff:95:9e:
    da:8c:5c:ba:39:5f:45:8c:9b:96:19:a3:f6:d2:e4:
    70:41:56:d8:83:c1:85:1f:a8:0b:35:e2:c6:80:95:
    ef:4d
publicExponent: 65537 (0x10001)
privateExponent:
    1d:4c:4d:ba:62:5d:42:08:9a:b4:c2:ef:42:5f:6f:
    13:9d:d3:3c:59:f3:8f:ca:9b:38:57:4e:60:9e:5d:
    cf:b4:fd:b1:12:37:5a:81:fa:24:67:f5:15:48:f1:
    ba:3d:cb:49:75:72:1a:5d:62:39:f8:19:3a:0e:d4:
    fa:1d:31:76:0f:e5:ed:28:4d:96:7b:b7:ae:d6:b4:
    ce:8c:56:c2:e8:1d:ab:eb:5f:ab:a4:cd:e6:1e:d8:
    fd:a0:18:c5:59:de:d2:fe:36:a1:8e:01:c7:cb:67:
    aa:8c:da:3d:cd:5e:6c:0c:cd:30:e9:15:51:72:1d:
    e7:09:aa:09:7e:ed:40:3b:89:19:10:31:c3:5f:f1:
    ed:3d:57:2c:30:12:e2:3d:e4:16:bb:4a:53:a9:7c:
    3b:d9:20:b0:49:80:f7:76:61:59:59:47:14:15:9f:
    26:43:19:fe:42:09:19:66:97:77:42:cd:0f:a5:fe:
    63:d4:be:bb:57:89:2c:96:bb:0c:b8:4c:ef:ad:6f:
    37:75:ad:60:96:df:70:5b:df:37:76:e5:81:a2:d4:
    1d:8b:31:a5:cc:a6:57:f0:77:70:be:ee:f5:7b:d7:
    6b:32:f5:4c:41:7a:43:2b:12:40:86:62:5b:bb:53:
    71:fd:e2:58:9f:b3:d2:87:20:0e:2b:c7:69:28:24:
    c1
prime1:
    00:dc:9c:df:ae:b8:5f:5f:61:24:e1:12:43:af:9c:
    dc:d9:05:1c:17:49:cf:aa:13:d0:a2:26:7e:68:ea:
    7d:c2:3c:50:80:55:15:52:56:d1:74:31:ec:5a:40:
    51:1f:82:1d:b3:f0:71:c9:d1:7c:1d:dd:bb:1c:d5:
    f7:74:40:ca:a8:bd:be:32:7b:04:2c:ff:19:f5:ed:
    2f:52:38:00:f3:80:57:2a:8e:05:23:31:32:56:af:
    eb:f6:55:84:31:1f:a7:e3:f7:2e:d2:f3:a6:bd:ca:
    65:60:19:74:5e:cc:2c:a2:0a:0a:91:10:21:09:a2:
    68:8a:a0:21:29:28:0f:e7:5d
prime2:
    00:d1:6d:77:01:c8:22:ed:a8:92:ff:f6:0f:fd:10:
    fe:2c:a0:64:0e:20:6b:ab:f1:01:ac:b4:ba:a3:8e:
    d8:f1:69:f2:7e:d5:84:c2:28:71:02:15:6e:77:2d:
    e3:59:fa:d5:fa:bd:49:c3:5a:94:28:14:9e:3d:76:
    3b:3c:b4:44:5f:87:65:8d:b7:72:7c:29:3e:33:00:
    d8:94:ea:53:72:57:f8:8d:20:90:fd:d3:2b:1c:23:
    f6:e2:24:c8:e7:c9:d9:df:c5:45:60:59:68:c6:66:
    d0:8f:aa:bf:c1:2b:90:ad:00:92:76:06:36:c3:f5:
    ae:83:20:e3:9f:f8:5b:58:b1
exponent1:
    00:86:f3:c7:b9:3f:bb:c7:c2:cb:26:8b:5f:b0:5b:
    8a:95:8f:14:a2:02:5a:f0:35:72:d8:de:27:51:d2:
    af:df:53:ba:02:e7:09:45:f7:29:e5:a4:6c:6a:c1:
    11:5e:ee:df:70:a5:53:56:1b:b9:8b:23:8a:44:97:
    76:ea:3c:80:3c:3c:e5:ce:47:86:44:68:40:df:39:
    9a:4a:f7:4b:4d:a9:62:a8:fb:7b:95:0d:91:37:8a:
    22:13:ec:38:13:3c:c4:1d:25:a6:15:11:4b:1c:aa:
    64:dd:26:75:13:50:5e:b5:38:e3:41:dd:d5:f7:e8:
    cb:7e:91:79:f7:8d:34:3d:59
exponent2:
    00:9c:40:0f:8a:44:c7:ca:88:fb:23:fd:71:f0:5d:
    bd:45:8e:65:18:25:18:30:30:a0:0f:3a:c8:05:3f:
    8e:9c:8f:6f:5d:31:f0:da:eb:51:65:3c:98:2e:53:
    0e:4d:13:d8:92:3a:a7:ce:18:c6:71:20:f0:ee:ea:
    47:48:03:37:00:0f:04:b5:b7:28:b3:7a:11:ed:fb:
    b3:9b:67:38:db:16:c7:5a:83:f1:a9:6e:e3:bb:1b:
    1a:17:9f:5a:45:95:53:f8:a0:36:22:ac:92:7f:74:
    36:26:fa:3e:16:e1:6a:0f:a9:5d:9c:b1:06:2b:2e:
    22:05:b3:84:20:d6:2b:51
coefficient:
    10:bc:bb:44:9d:ee:d3:c5:e6:31:20:fb:d4:2c:06:
    0b:26:4a:e0:7d:a6:5f:46:45:17:d0:ac:1e:a5:01:
    b8:14:80:0a:91:d8:4e:4e:32:b5:ad:c0:91:ec:37:
    df:e0:22:64:c4:f4:e3:ab:83:8f:eb:ea:96:c8:c6:
    e9:1b:ee:3a:7c:a7:e3:0f:8b:bb:4e:56:89:f4:b5:
    64:2c:e6:62:f0:51:09:bf:c4:8f:21:e6:3b:92:78:
    0f:66:e6:2e:8d:68:33:4b:80:54:2f:7f:f5:ec:44:
    9a:6a:7b:7f:bb:cc:51:fb:cf:3e:7e:16:39:6b:e9:
    a5:c2:dc:17:0f:5c:a3:a4

# 使用私钥生成对应的公钥文件
❯ openssl rsa -in rsa-private-key.pem -pubout -out rsa-public-key.pem
writing RSA key

# 查看私钥内容
❯ cat rsa-public-key.pem 
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtHpn91b6HUGvIpGsoZJb
wE3vQb42FguTBSNRHNITQG8ztiyfNt7JEyHLnzi9Ta+exRa6eqhnKf8pm5Cdrf/Y
bGjpbkiXFS6pOGM5kDvNc2Z+5/BNKyfDoCc/m7vptHWfDJwPTFE3/Qt2/M/rFNpM
sm2cLqO55RWqH/4Z0qQ4SSzbE1hST7QRuoLhJDibJSz2Z+jwefz2tzRyjQZOpRGE
jYQ9fyyNuIKYMPo3UjytN/7Uu2zqmi0pYv3bFSo8lAYAKReAHcqWJ5q9wusjWKpS
8dmEV3zqiiKYZz1gpuv/lZ7ajFy6OV9FjJuWGaP20uRwQVbYg8GFH6gLNeLGgJXv
TQIDAQAB
-----END PUBLIC KEY-----

# 查看公钥的参数
❯ openssl rsa -noout -text -pubin -in rsa-public-key.pem
Public-Key: (2048 bit)
Modulus:
    00:b4:7a:67:f7:56:fa:1d:41:af:22:91:ac:a1:92:
    5b:c0:4d:ef:41:be:36:16:0b:93:05:23:51:1c:d2:
    13:40:6f:33:b6:2c:9f:36:de:c9:13:21:cb:9f:38:
    bd:4d:af:9e:c5:16:ba:7a:a8:67:29:ff:29:9b:90:
    9d:ad:ff:d8:6c:68:e9:6e:48:97:15:2e:a9:38:63:
    39:90:3b:cd:73:66:7e:e7:f0:4d:2b:27:c3:a0:27:
    3f:9b:bb:e9:b4:75:9f:0c:9c:0f:4c:51:37:fd:0b:
    76:fc:cf:eb:14:da:4c:b2:6d:9c:2e:a3:b9:e5:15:
    aa:1f:fe:19:d2:a4:38:49:2c:db:13:58:52:4f:b4:
    11:ba:82:e1:24:38:9b:25:2c:f6:67:e8:f0:79:fc:
    f6:b7:34:72:8d:06:4e:a5:11:84:8d:84:3d:7f:2c:
    8d:b8:82:98:30:fa:37:52:3c:ad:37:fe:d4:bb:6c:
    ea:9a:2d:29:62:fd:db:15:2a:3c:94:06:00:29:17:
    80:1d:ca:96:27:9a:bd:c2:eb:23:58:aa:52:f1:d9:
    84:57:7c:ea:8a:22:98:67:3d:60:a6:eb:ff:95:9e:
    da:8c:5c:ba:39:5f:45:8c:9b:96:19:a3:f6:d2:e4:
    70:41:56:d8:83:c1:85:1f:a8:0b:35:e2:c6:80:95:
    ef:4d
Exponent: 65537 (0x10001)
```

RSA 描述的私钥的结构如下：

- `modulus`: 模数 $n$
- `publicExponent`: 公指数 $e$，固定为 65537 (0x10001)
- `privateExponent`: 私钥指数 $d$
- `prime1`: 质数 p，用于计算 $n$
- `prime2`: 质数 q，用于计算 $n$
- `exponent1`: 用于加速 RSA 运算的中国剩余定理指数一，$d \mod (p-1)$
- `exponent2`: 用于加速 RSA 运算的中国剩余定理指数二，$d \mod (q-1)$
- `coefficient`: 用于加速 RSA 运算的中国剩余定理系数，$q^{-1} \mod p$

再看下 RSA 公钥的结构：

- `modulus`: 模数 $n$
- `exponent`: 公指数 $e$，固定为 65537 (0x10001)

可以看到私钥文件中就已经包含了公钥的所有参数，实际上我们也是使用 `openssl rsa -in rsa-private-key.pem -pubout -out rsa-public-key.pem` 命令通过私钥生成出的对应的公钥文件。

下面就介绍下具体的密钥对生成流程，搞清楚 openssl 生成出的这个私钥，各项参数分别是什么含义。

- 随机选择两个不相等的质数 $p$ 与 $q$
  - p 跟 q 应该非常大，但是长度相差几个整数，这样会使得破解更加困难
- 计算出模数 $n = pq$
- 计算欧拉函数的值 $\phi(n) = \phi(pq) = (p-1)(q-1)$
- 选择公指数 $e$，要求 $1 < e < \lambda (n)$，且 $e$ 与 $\phi(n)$ 互质，即 $\gcd(e, \phi(n)) = 1$。
  - 目前 openssl 默认使用 65537 (0x10001)
  - 曾经也有使用过 3 作为 e 的值，但是目前 3 已被证明不够安全
- 计算出使等式 $ed \equiv 1 \bmod \phi(n)$ 成立的值 $d$，它就是我们的私钥指数
  - 上述等式的含义：$ed$ 被 $\phi(n)$ 的余数为 $1$
  - 等式可转换为 $ed = 1 + \phi(n) \cdot k$，其中 $k$ 为整数。
  - 移项得 $e d + \phi(n) \cdot y = 1 = \gcd(e, \phi(n))$，其中 $y=-k$
  - 上面的等式可使用[拓展欧几里得算法](https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95)求解，wiki 有给出此算法的 Python 实现，非常简洁。
- 使用 $(n, e)$ 组成公钥，使用 $n, d$ 组成私钥。其他参数可以保存在私钥中，也可丢弃。
  - $p, q, \phi(n), d$ 四个参数都必须保密，绝不能泄漏！
- 在现有算力下，想要通过公钥的 $(n, e)$ 推算出 $d$ 是非常困难的，这保证了 RSA 算法的安全性。

下面我们使用 Python 来通过 $p,q,e$ 计算出 $n, d$ 来，跟 openssl 打印的对比下，看看是否一致。

```python
# pip install cryptography==36.0.1
from pathlib import Path
from cryptography.hazmat.primitives import serialization

key_path = Path("./rsa-private-key.pem")
private_key = serialization.load_pem_private_key(
    key_path.read_bytes(),
    password=None,
)
private_numbers = private_key.private_numbers()
private_numbers = private_key.private_numbers()
p = private_numbers.p
q = private_numbers.q
e = 65537
phi_n = (p-1) * (q-1)

def extended_euclidean(a, b):
    """
      拓展欧几里得算法，能在计算出 a 与 b 的最大公约数的同时，给出 ax + by = gcd(a, b) 中的 x 与 y 的值
      代码来自 wiki: https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95
    """
    old_s, s = 1, 0
    old_t, t = 0, 1
    old_r, r = a, b
    if b == 0:
        return 1, 0, a
    else:
        while(r!=0):
            q = old_r // r
            old_r, r = r, old_r-q*r
            old_s, s = s, old_s-q*s
            old_t, t = t, old_t-q*t
    return old_s, old_t, old_r

# 我们只需要 d，y 可忽略，而余数 remainder 肯定为 1，也可忽略
d, y, remainder = extended_euclidean(e, phi_n)

n = p * q
print(f"{hex(n)=}")
# => hex(n)='0xb47a67f756fa1d41af2291aca1925bc04def41be36160b930523511cd213406f33b62c9f36dec91321cb9f38bd4daf9ec516ba7aa86729ff299b909dadffd86c68e96e4897152ea9386339903bcd73667ee7f04d2b27c3a0273f9bbbe9b4759f0c9c0f4c5137fd0b76fccfeb14da4cb26d9c2ea3b9e515aa1ffe19d2a438492cdb1358524fb411ba82e124389b252cf667e8f079fcf6b734728d064ea511848d843d7f2c8db8829830fa37523cad37fed4bb6cea9a2d2962fddb152a3c9406002917801dca96279abdc2eb2358aa52f1d984577cea8a2298673d60a6ebff959eda8c5cba395f458c9b9619a3f6d2e4704156d883c1851fa80b35e2c68095ef4d'
print(f"{hex(d)=}")
# => hex(d)='0x1d4c4dba625d42089ab4c2ef425f6f139dd33c59f38fca9b38574e609e5dcfb4fdb112375a81fa2467f51548f1ba3dcb4975721a5d6239f8193a0ed4fa1d31760fe5ed284d967bb7aed6b4ce8c56c2e81dabeb5faba4cde61ed8fda018c559ded2fe36a18e01c7cb67aa8cda3dcd5e6c0ccd30e91551721de709aa097eed403b89191031c35ff1ed3d572c3012e23de416bb4a53a97c3bd920b04980f7766159594714159f264319fe42091966977742cd0fa5fe63d4bebb57892c96bb0cb84cefad6f3775ad6096df705bdf3776e581a2d41d8b31a5cca657f07770beeef57bd76b32f54c417a432b124086625bbb5371fde2589fb3d287200e2bc7692824c1'
```

对比 RSA 的输出，可以发现去掉冒号后，`d` 跟 `n` 的值是完全相同的。

### RSA 加密与解密

RSA 加密算法，一次只能加密一个小于 $n$ 的非负整数，假设明文为整数 $msg$，加密算法如下：

$$
\text{encryptedMsg} = msg^e \mod n
$$

通常的手段是，先使用 [EAOP](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)  将被加密消息编码成一个个符合条件的整数，再使用上述公式一个个加密。

解密的方法，就是对被每一段加密的数据 $encryptedMsg$，进行如下运算：

$$
\text{decryptedMsg} = \text{encryptedMsg}^d \mod n
$$

解密运算的证明如下（证明需要用到 $0 \le msg \lt n$）：

$$
\begin{alignedat}{2}
\text{decryptedMsg} &= &\text{encryptedMsg}^d &\mod n \\\\
        &= &{(msg^e \mod n)}^d &\mod n \\\\
        &= &{msg^e}^d &\mod n \\\\
        &= &msg &\mod n \\\\
        &= &msg
\end{alignedat}
$$

因为非对称加解密非常慢，对于较大的文件，通常会使用非对称加密来加密数据，RSA 只被用于加密「对称加密」的密钥。


### RSA 数字签名

前面证明了可以使用公钥加密，再使用私钥解密。

实际上从上面的证明也可以看出来，顺序是完全可逆的，先使用私钥加密，再使用公钥解密也完全是可行的。这种运算被我们用在数字签名算法中。

数字签名的方法为：

- 首先计算原始数据的 Hash 值，比如 SHA256
- 使用私钥对计算出的 Hash 值进行加密，得到数字签名
- 其他人使用公开的公钥进行解密出 Hash 值，再对原始数据计算 Hash 值对比，如果一致，就说明数据未被篡改


## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)
- [密码发展史之近现代密码 - 中国国家密码管理局][cryptography_history]


[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
[cryptography_history]: https://www.oscca.gov.cn/sca/zxfw/2017-04/24/content_1011711.shtml
[cryptograph_everyone_can_learn]: https://github.com/guoshijiang/cryptography
