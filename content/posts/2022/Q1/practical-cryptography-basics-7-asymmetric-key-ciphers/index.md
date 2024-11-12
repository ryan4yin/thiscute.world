---
title: "写给开发人员的实用密码学（七）—— 非对称密钥加密算法 RSA/ECC"
date: 2022-03-09T20:50:00+08:00
lastmod: 2022-03-13T15:26:00+08:00
draft: false
featuredImage: "symmetric-vs-asymmetric.webp"
authors: ["ryan4yin"]

tags: ["Cryptography", "密码学", "非对称加密", "安全", "RSA", "ECC"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]

seriesNavigation: true

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 本文部分内容翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，笔者补充了
> 密码学历史以及 openssl 命令示例，并重写了 RSA/ECC 算法原理、代码示例等内容。

> 这篇文章中会涉及到一些数论知识，本文不会详细介绍这些数学知识，可以在有疑惑的时候自行查找
> 相关知识，或者选择跳过相关内容。

## 一、公钥密码学 / 非对称密码学

在介绍非对称密钥加密方案和算法之前，我们首先要了解公钥密码学的概念。

### 密码学的历史

从第一次世界大战、第二次世界大战到 1976 年这段时期密码的发展阶段，被称为「近代密码阶段」。
在近代密码阶段，所有的密码系统都使用对称密码算法——使用相同的密钥进行加解密。当时使用的密码
算法在拥有海量计算资源的现代人看来都是非常简单的，我们经常看到各种讲述一二战的谍战片，基本
都包含破译电报的片段。

第一二次世界大战期间，无线电被广泛应用于军事通讯，围绕无线电通讯的加密破解攻防战极大地影响
了战局。

公元20世纪初，第一次世界大战进行到关键时刻，英国破译密码的专门机构「40号房间」利用缴获的德
国密码本破译了著名的「齐默尔曼电报」，其内容显示德国打算联合墨西哥对抗可能会参战的美国，这
促使美国放弃中立对德宣战，从而彻底改变了一战的走势。

1943 年，美国从破译的日本电报中得知山本五十六将于 4 月 18 日乘中型轰炸机，由 6 架战斗机护
航，到中途岛视察。美国总统罗斯福亲自做出决定截击山本，山本乘坐的飞机在去往中途岛的路上被美
军击毁，战争天才山本五十六机毁人亡，日本海军从此一蹶不振。

此外，在二次世界大战中，美军将印第安纳瓦霍土著语言作为密码使用，并特别征募使用印第安纳瓦霍
通信兵。在二次世界大战日美的太平洋战场上，美国海军军部让北墨西哥和亚历桑那印第安纳瓦霍族人
使用纳瓦霍语进行情报传递。纳瓦霍语的语法、音调及词汇都极为独特，不为世人所知道，当时纳瓦霍
族以外的美国人中，能听懂这种语言的也就一二十人。这是**密码学**和**语言学**的成功结合，纳瓦
霍语密码成为历史上从未被破译的密码。

在 1976 年 Malcolm J. Williamson 公开发表了现在被称为「Diffie–Hellman 密钥交换，DHKE」的算
法，并提出了「公钥密码学」的概念，这是密码学领域一项划时代的发明，它宣告了「近代密码阶段」
的终结，是「现代密码学」的起点。

言归正传，对称密码算法的问题有两点：

- 「**需要安全的通道进行密钥交换**」，早期最常见的是面对面交换密钥
- 每个点对点通信都需要使用不同的密钥，**密钥的管理会变得很困难**
  - 如果你需要跟 100 个朋友安全通信，你就要维护 100 个不同的对称密钥，而且还得确保它们不泄
    漏。

这会导致巨大的「密钥交换」跟「密钥保存与管理」的成本。「公钥密码学」最大的优势就是，它解决
了这两个问题：

- 「公钥密码学」可以在**不安全的信道**上安全地进行密钥交换，第三方即使监听到通信过程，但是
  （几乎）无法破解出密钥。
- 每个人只需要公开自己的公钥，就可以跟其他任何人安全地通信。
  - 如果你需要跟 100 个朋友安全通信，你们只需要公开自己的公钥。发送消息时使用对方的公钥加
    密，接收消息时使用自己的私钥解密即可。
  - 只有你自己的私钥需要保密，所有的公钥都可以公开，这就显著降低了密钥的维护成本。

因此公钥密码学成为了现代密码学的基石，而「公钥密码学」的诞生时间 1976 年被认为是现代密码学
的开端。

### 公钥密码学的概念

公钥密码系统的密钥始终以公钥 + 私钥对的形式出现，公钥密码系统提供数学框架和算法来生成公钥+
私钥对。公钥通常与所有人共享，而私钥则保密。公钥密码系统在设计时就确保了在预期的算力下，几
乎不可能从其公开的公钥逆向演算出对应的私钥。

公钥密码系统主要有三大用途：**加密与解密、签名与验证、密钥交换**。每种算法都需要使用到公钥
和私钥，比如由公钥加密的消息只能由私钥解密，由私钥签名的消息需要用公钥验证。

由于加密解密、签名验证均需要两个不同的密钥，故「公钥密码学」也被称为「**非对称密码学**」。

比较著名的公钥密码系统有：RSA、ECC（椭圆曲线密码学）、ElGamal、Diffie-Hellman、ECDH、ECDSA
和 EdDSA。许多密码算法都是以这些密码系统为基础实现的，例如 RSA 签名、RSA 加密/解密、ECDH
密钥交换以及 ECDSA 和 EdDSA 签名。

### 量子安全性

> 参考文档：https://en.wikipedia.org/wiki/Post-quantum_cryptography

目前流行的公钥密码系统基本都依赖于 IFP（整数分解问题）、DLP（离散对数问题）或者 ECDLP（椭
圆曲线离散对数问题），这导致这些算法都是**量子不安全**（quantum-unsafe）的。

如果人类进入量子时代，IFP / DLP / ECDLP 的难度将大大降低，目前流行的
RSA、ECC、ElGamal、Diffie-Hellman、ECDH、ECDSA 和 EdDSA 等公钥密码算法都将被淘汰。

目前已经有一些量子安全的公钥密码系统问世，但是因为它们需要更长的密钥、更长的签名等原因，目
前还未被广泛使用。

一些量子安全的公钥密码算法举
例：NewHope、NTRU、GLYPH、BLISS、XMSS、[Picnic](https://github.com/Microsoft/Picnic) 等，
有兴趣的可以自行搜索相关文档。

## 二、非对称加密方案简介

非对称加密要比对称加密复杂，有如下几个原因：

- 使用密钥对进行加解密，导致其算法更为复杂
- 只能加密/解密很短的消息
  - 在 RSA 系统中，输入消息需要被转换为大整数（例如使用 OAEP 填充），然后才能被加密为密
    文。（密文实质上就是另一个大整数）
- 一些非对称密码系统（如 ECC）不直接提供加密能力，需要结合使用更复杂的方案才能实现加解密

此外，非对称密码比对称密码慢非常多。比如 RSA 加密比 AES 慢 1000 倍，跟 ChaCha20 就更没法比
了。

为了解决上面提到的这些困难并支持加密任意长度的消息，现代密码学使用「**非对称加密方案**」来
实现消息加解密。又因为「对称加密方案」具有速度快、支持加密任意长度消息等特性，「非对称加密
方案」通常直接直接组合使用**对称加密算法**与**非对称加密算法**。比如「密钥封装机制
KEM（key encapsulation mechanisms)）」与「集成加密方案 IES（Integrated Encryption
Scheme）」

### 1. 密钥封装机制 KEM

顾名思义，KEM 就是仅使用非对称加密算法加密另一个密钥，实际数据的加解密由该密钥完成。

密钥封装机制 KEM 的加密流程（使用公钥加密传输对称密钥）：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/hybrid-encryption.webp" >}}

密钥封装机制 KEM 的解密流程（使用私钥解密出对称密钥，然后再使用这个对称密钥解密数据）：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/hybrid-decryption.webp" >}}

RSA-OAEP, RSA-KEM, ECIES-KEM 和 PSEC-KEM. 都是 KEM 加密方案。

#### 密钥封装（Key encapsulation）与密钥包裹（Key wrapping）

主要区别在于使用的是对称加密算法、还是非对称加密算法：

- 密钥封装（Key encapsulation）指使用非对称密码算法的公钥加密另一个密钥。
- 密钥包裹（Key wrapping）指使用对称密码算法加密另一个密钥。

### 2. 集成加密方案 IES

集成加密方案 (IES) 在密钥封装机制（KEM）的基础上，添加了密钥派生算法 KDF、消息认证算法 MAC
等其他密码学算法以达成更高的安全性。

在 IES 方案中，非对称算法（如 RSA 或 ECC）跟 KEM 一样，都是用于加密或封装对称密钥，然后通
过对称密钥（如 AES 或 Chacha20）来加密输入消息。

DLIES（离散对数集成加密方案）和 ECIES（椭圆曲线集成加密方案）都是 IES 方案。

## 三、RSA 密码系统

RSA 密码系统是最早的公钥密码系统之一，它基于
[RSA 问题](https://en.wikipedia.org/wiki/RSA_problem)和[整数分解问题 （IFP）](https://en.wikipedia.org/wiki/Integer_factorization)的
计算难度。RSA 算法以其作者（Rivest–Shamir–Adleman）的首字母命名。

RSA 算法在计算机密码学的早期被广泛使用，至今仍然是数字世界应用最广泛的密码算法。但是随着
ECC 密码学的发展，ECC 正在非对称密码系统中慢慢占据主导地位，因为它比 RSA 具有更高的安全性
和更短的密钥长度。

RSA 算法提供如下几种功能：

- 密钥对生成：生成随机私钥（通常大小为 1024-4096 位）和相应的公钥。
- 加密解密：使用公钥加密消息（消息要先转换为 [0...key_length] 范围内的整数），然后使用密钥
  解密。
- 数字签名：签署消息（使用私钥）和验证消息签名（使用公钥）。
  - 数字签名实际上是通过 Hash 算法 + 加密解密功能实现的。后面会介绍到，它与一般加解密流程
    的区别，在于数字签名使用私钥加密，再使用公钥解密。
- 密钥交换：安全地传输密钥，用于以后的加密通信。

RSA 可以使用不同长度的密钥：1024、2048、3072、4096、8129、16384 甚至更多位。目前 **3072**
位及以上的密钥长度被认为是安全的，曾经大量使用的 **2048** 位 RSA 现在被破解的风险在不断提
升，已经不推荐使用了。

更长的密钥提供更高的安全性，但会消耗更多的计算时间，同时签名也会变得更长，因此需要在安全性
和速度之间进行权衡。非常长的 RSA 密钥（例如 50000 位或 65536 位）对于实际使用可能太慢，例
如密钥生成可能需要几分钟到几个小时。

### RSA 密钥对生成

RSA 密钥对的生成跟我们在本系列文章的第 5 篇介绍的「DHKE 密钥交换算法」会有些类似，但是要更
复杂一点。

首先看下我们怎么使用 openssl 生成一个 1024 位的 RSA 密钥对（**仅用做演示，实际应用中建议
3072 位**）：

> [OpenSSL](https://github.com/openssl/openssl) 是目前使用最广泛的网络加密算法库，支持非常
> 多流行的现代密码学算法，几乎所有操作系统都会内置 openssl.

```
# 生成 1024 位的 RSA 私钥
❯ openssl genrsa -out rsa-private-key.pem 1024
Generating RSA private key, 1024 bit long modulus
.................+++
.....+++
e is 65537 (0x10001)

# 使用私钥生成对应的公钥文件
❯ openssl rsa -in rsa-private-key.pem -pubout -out rsa-public-key.pem
writing RSA key

# 查看私钥内容
❯ cat rsa-private-key.pem
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDNE8QZLJZXREOeWZ2ilAzGC4Kjq/PfsFzrXGj8g3IaS4/J3JrB
o3qEq/k9XoRzOmNPyvWCj2FAY7A099d7qX4ztthBpUM2ePDIYDvhL0EpfQqbhe+Q
aagcFpuKTshGR2wBjH0Cl1/WxJkfIUMmWYU+m4iKLw9KfLX6BjmSgWB6HQIDAQAB
AoGADb5NXgKG8MI6ZdpLniGd2Yfb8WwMo+kF0SAYSRPmCa0WrciC9ocmJs3/ngU/
ixlWnnpTibRiKBaGMIaLglYRhvbvibUo8PH4woIidTho2e6swF2aqILk6YFJDpxX
FCFdbXM4Cm2MqbD4VtmhCYqbvuiyEUci83YrRP0jJGNt0GECQQDyZgdi8JlFQFH8
1QRHjLN57v5bHQamv7Qb77hlbdbg1wTYO+H8tsOB181TEHA7uN8hxkzyYZy+goRx
n0hvJcQXAkEA2JWhCb7oG1eal1aUdgofxhlWnkoFeWHay2zgDWSqmGKyDt0Cb1jq
XTdN9dchnqfptWN2/QPLDgM+/9g39/zv6wJATC1sXNeoE29nVMHNGn9JWCSXoyK4
GGdevvjTRm0Cfp6UUzBekQEO6Btd16Du5JXw6bhcLkAm9mgmH18jcGq5+QJBALnr
aDv3d0PRZdE372WMt03UfniOzjgueiVaJtMYcSEyx+reabKvvy+ZxACfVirdtU+S
PJhhYzN6MeBp+VGV/VUCQBXz0LyM08roWi6DiaRwJIbYx+WCKEOGXQ9QsZND+sGr
pOpugr3mcUge5dcZGKtsOUx2xRVmg88nSWMQVkTlsjQ=
-----END RSA PRIVATE KEY-----

# 查看私钥的详细参数
❯ openssl rsa -noout -text -in rsa-private-key.pem
Private-Key: (1024 bit)
modulus:
    00:cd:13:c4:19:2c:96:57:44:43:9e:59:9d:a2:94:
    0c:c6:0b:82:a3:ab:f3:df:b0:5c:eb:5c:68:fc:83:
    72:1a:4b:8f:c9:dc:9a:c1:a3:7a:84:ab:f9:3d:5e:
    84:73:3a:63:4f:ca:f5:82:8f:61:40:63:b0:34:f7:
    d7:7b:a9:7e:33:b6:d8:41:a5:43:36:78:f0:c8:60:
    3b:e1:2f:41:29:7d:0a:9b:85:ef:90:69:a8:1c:16:
    9b:8a:4e:c8:46:47:6c:01:8c:7d:02:97:5f:d6:c4:
    99:1f:21:43:26:59:85:3e:9b:88:8a:2f:0f:4a:7c:
    b5:fa:06:39:92:81:60:7a:1d
publicExponent: 65537 (0x10001)
privateExponent:
    0d:be:4d:5e:02:86:f0:c2:3a:65:da:4b:9e:21:9d:
    d9:87:db:f1:6c:0c:a3:e9:05:d1:20:18:49:13:e6:
    09:ad:16:ad:c8:82:f6:87:26:26:cd:ff:9e:05:3f:
    8b:19:56:9e:7a:53:89:b4:62:28:16:86:30:86:8b:
    82:56:11:86:f6:ef:89:b5:28:f0:f1:f8:c2:82:22:
    75:38:68:d9:ee:ac:c0:5d:9a:a8:82:e4:e9:81:49:
    0e:9c:57:14:21:5d:6d:73:38:0a:6d:8c:a9:b0:f8:
    56:d9:a1:09:8a:9b:be:e8:b2:11:47:22:f3:76:2b:
    44:fd:23:24:63:6d:d0:61
prime1:
    00:f2:66:07:62:f0:99:45:40:51:fc:d5:04:47:8c:
    b3:79:ee:fe:5b:1d:06:a6:bf:b4:1b:ef:b8:65:6d:
    d6:e0:d7:04:d8:3b:e1:fc:b6:c3:81:d7:cd:53:10:
    70:3b:b8:df:21:c6:4c:f2:61:9c:be:82:84:71:9f:
    48:6f:25:c4:17
prime2:
    00:d8:95:a1:09:be:e8:1b:57:9a:97:56:94:76:0a:
    1f:c6:19:56:9e:4a:05:79:61:da:cb:6c:e0:0d:64:
    aa:98:62:b2:0e:dd:02:6f:58:ea:5d:37:4d:f5:d7:
    21:9e:a7:e9:b5:63:76:fd:03:cb:0e:03:3e:ff:d8:
    37:f7:fc:ef:eb
exponent1:
    4c:2d:6c:5c:d7:a8:13:6f:67:54:c1:cd:1a:7f:49:
    58:24:97:a3:22:b8:18:67:5e:be:f8:d3:46:6d:02:
    7e:9e:94:53:30:5e:91:01:0e:e8:1b:5d:d7:a0:ee:
    e4:95:f0:e9:b8:5c:2e:40:26:f6:68:26:1f:5f:23:
    70:6a:b9:f9
exponent2:
    00:b9:eb:68:3b:f7:77:43:d1:65:d1:37:ef:65:8c:
    b7:4d:d4:7e:78:8e:ce:38:2e:7a:25:5a:26:d3:18:
    71:21:32:c7:ea:de:69:b2:af:bf:2f:99:c4:00:9f:
    56:2a:dd:b5:4f:92:3c:98:61:63:33:7a:31:e0:69:
    f9:51:95:fd:55
coefficient:
    15:f3:d0:bc:8c:d3:ca:e8:5a:2e:83:89:a4:70:24:
    86:d8:c7:e5:82:28:43:86:5d:0f:50:b1:93:43:fa:
    c1:ab:a4:ea:6e:82:bd:e6:71:48:1e:e5:d7:19:18:
    ab:6c:39:4c:76:c5:15:66:83:cf:27:49:63:10:56:
    44:e5:b2:34

# 查看公钥内容
❯ cat rsa-public-key.pem
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNE8QZLJZXREOeWZ2ilAzGC4Kj
q/PfsFzrXGj8g3IaS4/J3JrBo3qEq/k9XoRzOmNPyvWCj2FAY7A099d7qX4ztthB
pUM2ePDIYDvhL0EpfQqbhe+QaagcFpuKTshGR2wBjH0Cl1/WxJkfIUMmWYU+m4iK
Lw9KfLX6BjmSgWB6HQIDAQAB
-----END PUBLIC KEY-----

# 查看公钥的参数
❯ openssl rsa -noout -text -pubin -in rsa-public-key.pem
Public-Key: (1024 bit)
Modulus:
    00:cd:13:c4:19:2c:96:57:44:43:9e:59:9d:a2:94:
    0c:c6:0b:82:a3:ab:f3:df:b0:5c:eb:5c:68:fc:83:
    72:1a:4b:8f:c9:dc:9a:c1:a3:7a:84:ab:f9:3d:5e:
    84:73:3a:63:4f:ca:f5:82:8f:61:40:63:b0:34:f7:
    d7:7b:a9:7e:33:b6:d8:41:a5:43:36:78:f0:c8:60:
    3b:e1:2f:41:29:7d:0a:9b:85:ef:90:69:a8:1c:16:
    9b:8a:4e:c8:46:47:6c:01:8c:7d:02:97:5f:d6:c4:
    99:1f:21:43:26:59:85:3e:9b:88:8a:2f:0f:4a:7c:
    b5:fa:06:39:92:81:60:7a:1d
Exponent: 65537 (0x10001)
```

RSA 描述的私钥的结构如下（其中除 $n, d$ 之外的都是冗余信息）：

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

可以看到私钥文件中就已经包含了公钥的所有参数，实际上我们也是使用
`openssl rsa -in rsa-private-key.pem -pubout -out rsa-public-key.pem` 命令通过私钥生成出的
对应的公钥文件。

下面就介绍下具体的密钥对生成流程，搞清楚 openssl 生成出的这个私钥，各项参数分别是什么含
义：

> 这里不会详细介绍其中的各种数学证明，具体的请参考维基百科。相关数学知识包括取模运算的性
> 质、欧拉函数、模倒数（拓展欧几里得算法）

- 随机选择两个不相等的质数 $p$ 与 $q$
  - p 跟 q 应该非常大，但是长度相差几个整数，这样会使得破解更加困难
- 计算出模数 $n = pq$
- 计算欧拉函数的值 $\phi(n) = \phi(pq) = (p-1)(q-1)$
- 选择公指数 $e$，要求 $1 < e < \lambda (n)$，且 $e$ 与 $\phi(n)$ 互质，即
  $\gcd(e, \phi(n)) = 1$。
  - 目前 openssl 固定使用 65537 (0x10001) 作为 e 的值
  - 曾经也有使用过 3 作为 e 的值，但是目前 3 已被证明不够安全
- 计算出使等式 $ed \equiv 1 \bmod \phi(n)$ 成立的值 $d$，它就是我们的私钥指数
  - 上述等式的含义：$ed$ 被 $\phi(n)$ 的余数为 $1$
  - 等式可转换为 $ed = 1 + \phi(n) \cdot k$，其中 $k$ 为整数。
  - 移项得 $e d + \phi(n) \cdot y = 1 = \gcd(e, \phi(n))$，其中 $y=-k$
  - 上面的等式可使
    用[拓展欧几里得算法](https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95)求
    解，wiki 有给出此算法的 Python 实现，非常简洁。
- 使用 $(n, e)$ 组成公钥，使用 $(n, d)$ 组成私钥。其他参数可以保存在私钥中，也可丢弃。
  - $p, q, \phi(n), d$ 四个参数都必须保密，绝不能泄漏！
- 在现有算力下，想要通过公钥的 $(n, e)$ 推算出 $d$ 是非常困难的，这保证了 RSA 算法的安全
  性。

下面我们使用 Python 来通过 $p,q,e$ 计算出 $n, d$ 来，跟 openssl 打印的对比下，看看是否一
致。

```python
# pip install cryptography==36.0.1
from pathlib import Path
from cryptography.hazmat.primitives import serialization

key_path = Path("./rsa-private-key.pem")
private_key = serialization.load_pem_private_key(
    key_path.read_bytes(),
    password=None,
)
private = private_key.private_numbers()
public = private_key.public_key().public_numbers()
p = private.p
q = private.q
e = public.e
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
# => hex(n)='0xcd13c4192c965744439e599da2940cc60b82a3abf3dfb05ceb5c68fc83721a4b8fc9dc9ac1a37a84abf93d5e84733a634fcaf5828f614063b034f7d77ba97e33b6d841a5433678f0c8603be12f41297d0a9b85ef9069a81c169b8a4ec846476c018c7d02975fd6c4991f21432659853e9b888a2f0f4a7cb5fa06399281607a1d'
print(f"{hex(d)=}")
# => hex(d)='0xdbe4d5e0286f0c23a65da4b9e219dd987dbf16c0ca3e905d120184913e609ad16adc882f6872626cdff9e053f8b19569e7a5389b46228168630868b82561186f6ef89b528f0f1f8c28222753868d9eeacc05d9aa882e4e981490e9c5714215d6d73380a6d8ca9b0f856d9a1098a9bbee8b2114722f3762b44fd2324636dd061'
```

对比 RSA 的输出，可以发现去掉冒号后，`d` 跟 `n` 的值是完全相同的。

### RSA 加密与解密

RSA 加密算法，一次只能加密一个小于 $n$ 的非负整数，假设明文为整数 $msg$，加密算法如下：

$$
\text{encryptedMsg} = msg^e \mod n
$$

通常的手段是，先使用
[EAOP](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding) 将被加密消息编
码成一个个符合条件的整数，再使用上述公式一个个加密。

解密的方法，就是对被每一段加密的数据 $encryptedMsg$，进行如下运算：

$$
\text{decryptedMsg} = \text{encryptedMsg}^d \mod n
$$

#### RSA 解密运算的证明

> 这里的证明需要用到一些数论知识，觉得不容易理解的话，建议自行查找相关资料。

证明流程如下：

$$
\begin{alignedat}{2}
\text{decryptedMsg} &= &\text{encryptedMsg}^d &\mod n \\\\
        &= &{(msg^e \mod n)}^d &\mod n \\\\
        &= &{msg^{ed}} &\mod n \\\\
        &= &{msg^{ed}} &\mod {pq}
\end{alignedat}
$$

接下来将下面两个等式代入上述计算中：

- 我们在前面的「密钥对生成」一节中有给出等式：$ed = 1 + (p-1)(q-1) \cdot k$
- 因为 $0 \le msg \lt n$ 以及 $n = pq$，有 $msg \mod pq = msg$

这样就得到：

$$
\begin{alignedat}{2}
\text{decryptedMsg} &= &{msg^{ed}} &\mod {pq} \\\\
        &= &{(msg \mod pq) \cdot (msg^{ed-1} \mod pq)} &\mod {pq} \\\\
        &= &{msg \cdot (msg^{(p-1)(q-1) \cdot k} \mod pq)} &\mod {pq}
\end{alignedat}
$$

又
有[费马小定理](https://zh.wikipedia.org/wiki/%E8%B4%B9%E9%A9%AC%E5%B0%8F%E5%AE%9A%E7%90%86)指
出，在 $a$ 为整数，$p$ 为质数的情况下，有同余等式

$$a^{p-1} \equiv 1 {\pmod  p}$$

因为我们的模数 $n=pq$ 并不是质数，不能直接利用费马小定理给出的同余公式。但是 $p$, $q$ 两数
都为质数，我们可以分别计算方程 对 $p$ 以及 $q$ 取模的结果，然后再根
据[中国剩余定理](https://zhuanlan.zhihu.com/p/44591114)得出通解，也就得到我们需要的结果。

对于模 $p$ 的情况，计算方法如下：

- 当 $msg = 0 \mod p$ 时，${msg^{ed}} \mod p = 0 \equiv msg \pmod  p$
- 当 $msg \ne 0 \mod p$ 时，利用费马小定理，有
  $$
  \begin{alignedat}{2}
  msg^{ed} &= &{msg \cdot (msg^{(p-1)(q-1) \cdot k} \mod p)} &\pmod {p}  \\\\
                      &= &msg \cdot (msg^{(p-1)} \mod p)^{(q-1) \cdot k} &\pmod p \\\\
                      &= &msg \cdot 1^{(q-1) \cdot k} &\pmod p \\\\
                      &\equiv &msg \pmod  p
  \end{alignedat}
  $$

同理，对模 $q$ 的情况，也能得到等式

$$msg^{ed} \equiv msg \pmod  q$$

有了上面两个结果，根据中国剩余定理，就能得到

$$msg^{ed} \equiv msg \pmod  {pq}$$

现在再接续前面的计算：

$$
\begin{alignedat}{2}
\text{decryptedMsg} &= &{msg^{ed}} &\pmod {pq} \\\\
        &= &msg &\pmod  {pq} \\\\
        &= &msg
\end{alignedat}
$$

这样就证明了，解密操作得到的就是原始信息。

因为非对称加解密非常慢，对于较大的文件，通常会分成两步加密来提升性能：首先用使用对称加密算
法来加密数据，再使用 RSA 等非对称加密算法加密上一步用到的「对称密钥」。

下面我们用 Python 来验证下 RSA 算法的加解密流程：

```python
# pip install cryptography==36.0.1
from pathlib import Path
from cryptography.hazmat.primitives import serialization

# 私钥
key_path = Path("./rsa-private-key.pem")
private_key = serialization.load_pem_private_key(
    key_path.read_bytes(),
    password=None,
)
private = private_key.private_numbers()
public = private_key.public_key().public_numbers()
d = private.d

# 公钥
n = public.n
e = public.e

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def fast_power_modular(b: int, p: int, m: int):
    """
    快速模幂运算：b^p % m
    复杂度： O(log p)
    因为 RSA 的底数跟指数都非常大，如果先进行幂运算，最后再取模，计算结果会越来越大，导致速度非常非常慢
    根据模幂运算的性质  b^(ab) % m = (b^a % m)^b % m, 可以通过边进行幂运算边取模，极大地提升计算速度
    """
    res = 1
    while p:
        if p & 0x1: res *= b
        b = b ** 2 % m
        p >>= 1
    return res % m

# 明文
original_msg = b"an example"
print(f"{original_msg=}")

# 加密
msg_int = int_from_bytes(original_msg)
encrypt_int = msg_int ** e % n
encrypt_msg = int_to_bytes(encrypt_int)
print(f"{encrypt_msg=}")

# 解密
# decrypt_int = encrypt_int ** d % n # 因为 d 非常大，直接使用公式计算会非常非常慢，所以不能这么算
decrypt_int = fast_power_modular(encrypt_int, d, n)
decrypt_msg = int_to_bytes(decrypt_int)
print(f"{decrypt_msg=}")  # 应该与原信息完全一致
```

### RSA 数字签名

前面证明了可以使用公钥加密，再使用私钥解密。

实际上从上面的证明也可以看出来，顺序是完全可逆的，先使用私钥加密，再使用公钥解密也完全是可
行的。这种运算被我们用在数字签名算法中。

数字签名的方法为：

- 首先计算原始数据的 Hash 值，比如 SHA256
- 使用私钥对计算出的 Hash 值进行加密，得到数字签名
- 其他人使用公开的公钥进行解密出 Hash 值，再对原始数据计算 Hash 值对比，如果一致，就说明数
  据未被篡改

Python 演示：

```python
# pip install cryptography==36.0.1
from hashlib import sha512
from pathlib import Path
from cryptography.hazmat.primitives import serialization

key_path = Path("./rsa-private-key.pem")
private_key = serialization.load_pem_private_key(
    key_path.read_bytes(),
    password=None,
)
private = private_key.private_numbers()
public = private_key.public_key().public_numbers()
d = private.d
n = public.n
e = public.e

# RSA sign the message
msg = b'A message for signing'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, d, n)
print("Signature:", hex(signature))

# RSA verify signature
msg = b'A message for signing'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
hashFromSignature = pow(signature, e, n)
print("Signature valid:", hash == hashFromSignature)
```

## 四、ECC 密码系统

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/ecc.webp" >}}

ECC 椭圆曲线密码学，于 1985 年被首次提出，并于 2004 年开始被广泛应用。ECC 被认为是 RSA 的
继任者，新一代的非对称加密算法。

其最大的特点在于相同密码强度下，ECC 的密钥和签名的大小都要显著低于 RSA. 256bits 的 ECC 密
钥，安全性与 3072bits 的 RSA 密钥安全性相当。

其次 ECC 的密钥对生成、密钥交换与签名算法的速度都要比 RSA 快。

### 椭圆曲线的数学原理简介

在数学中，椭圆曲线（Elliptic Curves）是一种平面曲线，由如下方程定义的点的集合组成（$A-J$
均为常数）：

$$
Ax^3 + Bx^2y + Cxy^2 + Dy^3 + Ex^2 + Fxy + Gy^2 + Hx + Iy + J = 0
$$

而 ECC 只使用了其中很简单的一个子集（$a, b$ 均为常数）：

$$
y^2 = x^3 + ax + b
$$

比如著名的 NIST 曲线 secp256k1 就是基于如下椭圆曲线方程：

$$
y^2 = x^3 + 7
$$

椭圆曲线大概长这么个形状：

> 椭圆曲线跟椭圆的关系，就犹如雷锋跟雷峰塔、Java 跟 JavaScript...

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/elliptic-curve.webp" >}}

你可以通过如下网站手动调整 $a$ 与 $b$ 的值，拖动曲线的交点查看图形的变化情况：
<https://www.desmos.com/calculator/ialhd71we3?lang=zh-CN>

#### 椭圆曲线上的运算

数学家在椭圆曲线上定义了一些运算规则，ECC 就依赖于这些规则，下面简单介绍下我们用得到的部
分。

> 椭圆曲线上的运算跟我们所熟知的实数域运算不太一样，它在现实生活中并无实际意义，但是它的一
> 些性质使其很适合被应用在密码学中。

##### 1. 加法与负元

对于曲线上的任意两点 $A$ 与 $B$，我们定义过 $A, B$ 的直线与曲线的交点为 $-(A+B)$，而
$-(A+B)$ 相对于 x 轴的对称点即为 $A+B$:

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/ecc-add-operation.webp" >}}

上述描述一是定义了椭圆曲线的加法规则，二是定义了椭圆曲线上的负元运算。

##### 2. 二倍运算

在加法规则中，如果 $A=B$，我们定义曲线在 $A$ 点的切线与曲线的交点为 $-2A$，于是得到二倍运
算的规则：

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/ecc-2-times.webp" >}}

##### 3. 无穷远点

对于 $(-A) + A$ 这种一个值与其负元本身相加的情况，我们会发现过这两点的直线与椭圆曲线没有第
三个交点，前面定义的加法规则在这种情况下失效了。为了解决这个问题，我们假设这条直线与椭圆曲
线相交于无穷远点 $O_{\infty}$.

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/ecc-ifinite-point.webp" >}}

##### 4. k 倍运算

我们在前面已经定义了椭圆曲线上的**加法运算**、**二倍运算**以及**无穷远点**，有了这三个概
念，我们就能定义**k 倍运算** 了。

K 倍运算最简单的计算方法，就是不断地进行加法运算，但是也有许多更高效的算法。其中最简单的算
法是「double-and-add」，它要求首先 $k$ 拆分成如下形式

$$
k = k_{0}+2k_{1}+2^{2}k_{2}+\cdots +2^{m}k_{m} \\\\
\text{其中} k_{0}~..~k_{m}\in \{0,1\},m=\lfloor \log _{2}{k}\rfloor
$$

然后再迭代计算其中各项的值，它的运算复杂度为 $log_{2}(k)$.

因 Double 和 Add 的执行时间不同，根据执行时间就可以知道是执行 Double 还是 Add，间接可以推
算出 $k$. 因此这个算法会有计时攻击的风险。基于「double-and-add」修改的蒙哥马利阶梯
（Montgomery Ladder）是可以避免计时分析的作法，这里就不详细介绍了。

#### 5. 有限域上的椭圆曲线

椭圆曲线是连续且无限的，而计算机却更擅长处理离散的、存在上限的整数，因此 ECC 使用「有限域
上的椭圆曲线」进行计算。

「有限域（也被称作 Galois Filed, 缩写为 GF）」顾名思义，就是指只有有限个数值的域。

有限域上的椭圆曲线方程，通过取模的方式将曲线上的所有值都映射到同一个有限域内。有限域
$\mathbb {F} _{p}$ 上的 EC 椭圆曲线方程为：

$$
y^2 = x^3 + ax + b (\mod p), 0 \le x \le p
$$

目前主要有两种有限域在 ECC 中被广泛应用：

- 以素数为模的整数域: $\mathbb {F} _{p}$
  - 在通用处理器上计算很快
- 以 2 的幂为模的整数域: $\mathbb {F} _{2^{m}}$
  - 当使用专用硬件时，计算速度很快

通过限制 x 为整数，并使用取模进行了映射后，椭圆曲线的形状已经面目全非了，它的加减法也不再
具有几何意义。但是它的一些特性仍然跟椭圆曲线很类似，各种公式基本加个 $\mod p$ 就变成了它的
有限域版本：

- 无穷远点 $O_{\infty}$ 是零
  元，$O_{\infty} + O_{\infty} = O_{\infty}$，$O_{\infty} + P = P$
- $P_{x, y}$ 的负元为 $P_{x, -y}$,，并且有 $P + (-P) = O_{\infty}$
- $P * 0 = O_{\infty}$
- 如果 $P_{x1, y1} + Q_{x2, y2} = R_{x3, y3}$，则其坐标有如下关系
  - $x3 = (k^2 - x1 - x2) \mod p$
  - $y3 = (k(x1 - x3) - y1) \mod p$
  - 斜率 $k$ 的计算
    - 如果 $P=Q$，则 $k=\dfrac {3x^{2}+a} {2y_{1}}$
    - 否则 $k=\dfrac {y*{2}-y*{1}} {x*{2}-x*{1}} $

#### ECDLP 椭圆曲线离散对数问题

前面已经介绍了椭圆曲线上的 **k 倍运算** 及相关的高效算法，但是我们还没有涉及到除法。

椭圆曲线上的除法是一个尚未被解决的难题——「ECDLP 椭圆曲线离散对数问题」：

> 已知 $kG$ 与基点 $G$，求整数 $k$ 的值。

目前并没有有效的手段可以快速计算出 $k$ 的值。比较直观的方法应该是从基点 $G$ 开始不断进行加
法运算，直到结果与 $kG$ 相等。

目前已知的 ECDLP 最快的解法所需步骤为 $\sqrt{k}$，而 **k 倍运算**高效算法前面已经介绍过
了，所需步骤为 $log_2(k)$。在 $k$ 非常大的情况下，它们的计算用时将会有指数级的差距。

> 椭圆曲线上的 **k 倍运算**与素数上的幂运算很类似，因此 ECC 底层的数学难题 ECDLP 与 RSA 的
> 离散对数问题 DLP 也有很大相似性。

### ECC 密钥对生成

首先，跟 RSA 一样，让我们先看下怎么使用 openssl 生成一个使用 prime256v1 曲线的 ECC 密钥
对：

```shell
# 列出 openssl 支持的所有曲线名称
openssl ecparam -list_curves

# 生成 ec 算法的私钥，使用 prime256v1 算法，密钥长度 256 位。（强度大于 2048 位的 RSA 密钥）
openssl ecparam -genkey -name prime256v1 -out ecc-private-key.pem
# 通过密钥生成公钥
openssl ec -in ecc-private-key.pem -pubout -out ecc-public-key.pem

# 查看私钥内容
❯ cat ecc-private-key.pem
-----BEGIN EC PARAMETERS-----
BggqhkjOPQMBBw==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIGm3wT/m4gDaoJGKfAHDXV2BVtdyb/aPTITJR5B6KVEtoAoGCCqGSM49
AwEHoUQDQgAE5IEIorw0WU5+om/UgfyYSKosiGO6Hpe8hxkqL5GUVPyu4LJkfw/e
99zhNJatliZ1Az/yCKww5KrXC8bQ9wGQvw==
-----END EC PRIVATE KEY-----

# 查看私钥的详细参数
❯ openssl ec -noout -text -in ecc-private-key.pem
read EC key
Private-Key: (256 bit)
priv:
    69:b7:c1:3f:e6:e2:00:da:a0:91:8a:7c:01:c3:5d:
    5d:81:56:d7:72:6f:f6:8f:4c:84:c9:47:90:7a:29:
    51:2d
pub:
    04:e4:81:08:a2:bc:34:59:4e:7e:a2:6f:d4:81:fc:
    98:48:aa:2c:88:63:ba:1e:97:bc:87:19:2a:2f:91:
    94:54:fc:ae:e0:b2:64:7f:0f:de:f7:dc:e1:34:96:
    ad:96:26:75:03:3f:f2:08:ac:30:e4:aa:d7:0b:c6:
    d0:f7:01:90:bf
ASN1 OID: prime256v1
NIST CURVE: P-256

# 查看公钥内容
❯ cat ecc-public-key.pem
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5IEIorw0WU5+om/UgfyYSKosiGO6
Hpe8hxkqL5GUVPyu4LJkfw/e99zhNJatliZ1Az/yCKww5KrXC8bQ9wGQvw==
-----END PUBLIC KEY-----

# 查看公钥的参数
❯ openssl ec -noout -text -pubin -in ecc-public-key.pem
read EC key
Private-Key: (256 bit)
pub:
    04:e4:81:08:a2:bc:34:59:4e:7e:a2:6f:d4:81:fc:
    98:48:aa:2c:88:63:ba:1e:97:bc:87:19:2a:2f:91:
    94:54:fc:ae:e0:b2:64:7f:0f:de:f7:dc:e1:34:96:
    ad:96:26:75:03:3f:f2:08:ac:30:e4:aa:d7:0b:c6:
    d0:f7:01:90:bf
ASN1 OID: prime256v1
NIST CURVE: P-256
```

可以看到 ECC 算法的公钥私钥都比 RSA 小了非常多，数据量小，却能带来同等的安全强度，这是 ECC
相比 RSA 最大的优势。

私钥的参数：

- `priv`: 私钥，一个 256bits 的大整数，对应我们前面介绍的 $k 倍运算$中的 $k$
- `pub`: 公钥，是一个椭圆曲线（EC）上的坐标 ${x, y}$，也就是我们 well-known 的基点 $G$
- `ASN1 OID`: prime256v1, 椭圆曲线的名称
- `NIST CURVE`: P-256

使用安全随机数生成器即可直接生成出 ECC 的私钥 `priv`，因此 ECC 的密钥对生成速度非常快。

### ECDH 密钥交换

这个在前
面[写给开发人员的实用密码学（五）—— 密钥交换 DHKE 与完美前向保密 PFS](/posts/practical-cryptography-basics-5-key-exchange/)已
经介绍过了，不过这里再复述一遍：

- Alice 跟 Bob 协商好椭圆曲线的各项参数，以及基点 G，这些参数都是公开的。
- Alice 生成一个随机的 ECC 密钥对（公钥：$alicePrivate * G$, 私钥: $alicePrivate$）
- Bob 生成一个随机的 ECC 密钥对（公钥：$bobPrivate * G$, 私钥: $bobPrivate$）
- 两人通过不安全的信道交换公钥
- Alice 将 Bob 的公钥乘上自己的私钥，得到共享密钥
  $sharedKey = (bobPrivate * G) * alicePrivate$
- Bob 将 Alice 的公钥乘上自己的私钥，得到共享密钥
  $sharedKey = (alicePrivate * G) * bobPrivate$
- 因为 $(a * G) * b = (b * G) * a$，Alice 与 Bob 计算出的共享密钥应该是相等的

这样两方就通过 ECDH 完成了密钥交换。而 ECDH 的安全性，则由 ECDLP 问题提供保证。

### ECC 加密与解密

ECC 本身并没有提供加密与解密的功能，但是我们可以借助 ECDH 迂回实现加解密。流程如下：

1. Bob 想要将消息 `M` 安全地发送给 Alice，他手上已经拥有了 Alice 的 ECC 公钥 `alicePubKey`
1. Bob 首先使用如下算法生成出「共享密钥」+「密文公钥」
   1. 随机生成一个临时用的密文 ECC 密钥对
      - 密文私钥 `ciphertextPrivKey`：生成一个安全随机数作为私钥即可
      - 密文公钥 `ciphertextPubKey`：使用此公式从私钥生成
        `ciphertextPubKey =ciphertextPrivKey * G`
   2. 使用 ECDH 算法计算出「共享密钥」：`sharedECCKey = alicePubKey * ciphertextPrivKey`
   3. 为了确保安全性，每份密文都应该使用不同的「**临时 ECC 密钥对**」作为「密文密钥对」，
      不应该直接使用「Bob 的密钥对」！「Bob 的密钥对」只在 Alice 回复密文消息给 Bob 时才应
      该被用到。
1. Bob 使用「共享密钥」与对称加密算法加密消息，得到密文 `C`
   - 比如使用 AES-256-GCM 或者 ChaCha20-Poly1305 进行对称加密
1. Bob 将 `C` 与「密文公钥 `ciphertextPubKey`」打包传输给 Alice
1. Alice 使用「密文公钥」与自己的私钥计算出「共享密
   钥」`sharedECCKey = ciphertextPubKey * alicePrivKey`
   1. 根据 ECDH 算法可知，这里计算出的共享密钥 `sharedECCKey`，跟 Bob 加密数据使用的共享密
      钥是完全一致的
1. Alice 使用计算出的共享密钥解密 `C` 得到消息 `M`

实际上就是消息的发送方先生成一个临时的 ECC 密钥对，然后借助 ECDH 协议计算出共享密钥用于加
密。消息的接收方同样通过 ECDH 协议计算出共享密钥再解密数据。

使用 Python 演示如下：

```python
# pip install tinyec  # <= ECC 曲线库
from tinyec import registry
import secrets

# 使用这条曲线进行演示
curve = registry.get_curve('brainpoolP256r1')

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def ecc_calc_encryption_keys(pubKey):
    """
    安全地生成一个随机 ECC 密钥对，然后按 ECDH 流程计算出共享密钥 sharedECCKey
    最后返回（共享密钥, 临时 ECC 公钥 ciphertextPubKey）
    """
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    sharedECCKey = pubKey * ciphertextPrivKey
    return (sharedECCKey, ciphertextPubKey)

def ecc_calc_decryption_key(privKey, ciphertextPubKey):
    sharedECCKey = ciphertextPubKey * privKey
    return sharedECCKey

# 1. 首先生成出 Alice 的 ECC 密钥对
privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g
print("private key:", hex(privKey))
print("public key:", compress_point(pubKey))

# 2. Alice 将公钥发送给 Bob

# 3. Bob 使用 Alice 的公钥生成出（共享密钥, 临时 ECC 公钥 ciphertextPubKey）
(encryptKey, ciphertextPubKey) = ecc_calc_encryption_keys(pubKey)
print("ciphertext pubKey:", compress_point(ciphertextPubKey))
print("encryption key:", compress_point(encryptKey))

# 4. Bob 使用共享密钥 encryptKey 加密数据，然后将密文与 ciphertextPubKey 一起发送给 Alice

# 5. Alice 使用自己的私钥 + ciphertextPubKey 计算出共享密钥 decryptKey
decryptKey = ecc_calc_decryption_key(privKey, ciphertextPubKey)
print("decryption key:", compress_point(decryptKey))

# 6. Alice 使用 decryptKey 解密密文得到原始消息
```

### ECC 数字签名

前面已经介绍了 RSA 签名，这里介绍下基于 ECC 的签名算法。

基于 ECC 的签名算法主要有两种：ECDSA 与 EdDSA，以及 EdDSA 的变体。其中 ECDSA 算法稍微有点
复杂，而安全强度跟它基本一致的 EdDSA 的算法更简洁更易于理解，在使用特定曲线的情况下 EdDSA
还要比 ECDSA 更快一点，因此现在通常更推荐使用 **EdDSA** 算法。

#### EdDSA 与 Ed25519 签名算法

EdDSA（Edwards-curve Digital Signature Algorithm）是一种现代的安全数字签名算法，它使用专为
性能优化的椭圆曲线，如 255bits 曲线 edwards25519 和 448bits 曲线 edwards448.

EdDSA 签名算法及其变体 Ed25519 和 Ed448 在技术上在
[RFC8032](https://tools.ietf.org/html/rfc8032) 中进行了描述。

首先，用户需要基于 edwards25519 或者 edwards448 曲线，生成一个 ECC 密钥对。生成私钥的时
候，算法首先生成一个随机数，然后会对随机数做一些变换以确保安全性，防范计时攻击等攻击手段。
对于 edwards25519 公私钥都是 32 字节，而对于 edwards448 公私钥都是 57 字节。

对于 edwards25519 输出的签名长度为 64 字节，而对于 Ed448 输出为 114 字节。

具体的算法虽然比 ECDSA 简单，但还是有点难度的，这里就直接略过了。

下面给出个 ed25519 的计算示例：

```python
# pip install cryptography==36.0.1
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# 也可用 openssl 生成，都没啥毛病
private_key = Ed25519PrivateKey.generate()

# 签名
signature = private_key.sign(b"my authenticated message")

# 显然 ECC 的公钥 kG 也能直接从私钥 k 生成
public_key = private_key.public_key()
# 验证
# Raises InvalidSignature if verification fails
public_key.verify(signature, b"my authenticated message")
```

ed448 的代码也完全类似：

```python
# pip install cryptography==36.0.1
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey

private_key = Ed448PrivateKey.generate()
signature = private_key.sign(b"my authenticated message")
public_key = private_key.public_key()
# Raises InvalidSignature if verification fails
public_key.verify(signature, b"my authenticated message")
```

### 密码学常用椭圆曲线介绍

在介绍密码学中的常用椭圆曲线前，需要先介绍一下椭圆曲线的**阶**（order）以及**辅助因
子**（cofactor）这两个概念。

首先还得介绍下数学中「循环群」的概念，它是指能由单个元素所生成的群，在 ECC 中这就是预先定
义好的基点 $G$.

一个有限域上的椭圆曲线可以形成一个有限「循环代数群」，它由曲线上的所有点组成。椭圆曲线
的**阶**被定义为该曲线上所有点的个数（包括无穷远点）。

有些曲线加上 G 点可以形成一个单一循环群，这一个群包含了曲线上的所有点。而其他的曲线加上 G
点则形成多个不相交的循环子群，每个子群包含了曲线的一个子集。对于上述第二种情况，假设曲线上
的点被拆分到了 **h** 个循环子群中，每个子群的**阶**都是 **r**，那这时整个群的阶就是
$n = h * r$，其中子群的个数 **h** 被称为**辅助因子**。

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/elliptic-curve-subgroups.webp" >}}

有限域上的椭圆曲线的阶都是有限的，也就是说对于曲线上任意一点 $G$，我们计算它的数乘 $kG$，
随着整数 $k$ 的增大，一定会存在某个 $k$ 使 $kG = O_{\infty}$ 成立，然后 $k$ 继续增大时，因
为 $O_{\infty} * P = O_{\infty}$，$kG$ 的值就固定为 $O_{\infty}$ 了，更大的 $k$ 值已经失去
了意义。

因此 ECC 中要求 $kG$ 中的私钥 $k$ 符合条件 $0 \le k \le r$，也就是说总的私钥数量是受 $r$
限制的。

辅助因子通过用如下公式表示：

$$
h = n / r
$$

其中 $n$ 是曲线的阶，$r$ 是每个子群的阶，$h$ 是辅助因子。如果曲线形成了一个单一循环群，那
显然 $h = 1$，否则 $h > 1$

举例如下：

- `secp256k1` 的辅助因子为 1
- `Curve25519` 的辅助因子为 8
- `Curve448` 的辅助因子为 4

#### 生成点 G

生成点 G 的选择是很有讲究的，虽然每个循环子群都包含有很多个生成点，但是 ECC 只会谨慎的选择
其中一个。首先 G 点必须要能生成出整个循环子群，其次还需要有尽可能高的计算性能。

数学上已知某些椭圆曲线上，不同的生成点生成出的循环子群，阶也是不同的。如果 G 点选得不好，
可能会导致生成出的子群的阶较小。前面我们已经提过子群的阶 $r$ 会限制总的私钥数量，导致算法
强度变弱！因此不恰当的 $G$ 点可能会导致我们遭受
「[小子群攻击](https://datatracker.ietf.org/doc/html/rfc2785)」。为了避免这种风险，建议尽
量使用被广泛使用的加密库，而不是自己撸一个。

#### 椭圆曲线的域参数

ECC椭圆曲线由一组椭圆曲线域参数描述，如曲线方程参数、场参数和生成点坐标。这些参数在各种密
码学标准中指定，你可以网上搜到相应的 RFC 或 NIST 文档。

这些标准定义了一组命名曲线的参数，例如 secp256k1、P-521、brainpoolP512t1 和 SM2. 这些加密
标准中描述的有限域上的椭圆曲线得到了密码学家的充分研究和分析，并被认为具有一定的安全强度。

也有一些密码学家（如 Daniel Bernstein）认为，官方密码标准中描述的大多数曲线都是「不安全
的」，并定义了他们自己的密码标准，这些标准在更广泛的层面上考虑了 ECC 安全性。

开发人员应该仅使用各项标准文档给出的、经过密码学家充分研究的命名曲线。

##### secp256k1

此曲线被应用在比特币中，它的域参数如下：

- _**p**_ \(modulus\) =
  `0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F`
- _**n**_ \(order; size; the count of all possible EC points\) =
  `0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141`
- _**a**_ \(方程 $y^2 ≡ x^3 + a\*x + b \(\mod p\)$ 中的常数\) =
  `0x0000000000000000000000000000000000000000000000000000000000000000`
- _**b**_ \(方程 $y^2 ≡ x^3 + a\*x + b \(\mod p\)$ 中的常数\)=
  `0x0000000000000000000000000000000000000000000000000000000000000007`
- _**g**_ \(the curve generator point G {x, y}\) =
  \(`0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798`,
  `0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8`\)
- _**h**_ \(cofactor, typically 1\) = 01

##### Edwards 曲线

椭圆曲线方程除了我们前面使用的 Weierstrass 形式 $$y^2 = (x^3 + ax + b) \mod p$$ 外，还可以
被写成其他多种形式，这些不同的形式
是[双有理等价](https://zh.wikipedia.org/zh-hans/%E6%9C%89%E7%90%86%E6%98%A0%E5%B0%84)的
（别问，我也不懂什么叫「双有理等价」...）。不同的方程形式在计算机的数值计算上可能会存在区
别。

为了性能考虑，ECC 在部分场景下会考虑使用 Edwards 曲线形式进行计算，该方程形式如下：

$$
x^{2}+y^{2}=1+dx^{2}y^{2}
$$

画个图长这样：

![](/images/practical-cryptography-basics-7-asymmetric-key-ciphers/edwards-curve.webp)

知名的 Edwards 曲线有：

- Curve1174 (251-bit)
- Curve25519 (255-bit)
- Curve383187 (383-bit)
- Curve41417 (414-bit)
- Curve448 (448-bit)
- E-521 (521-bit)
- ...

##### Curve25519, X25519 和 Ed25519

> https://www.ietf.org/rfc/rfc7748.html#section-4.1

> https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/

只要域参数选得好，Edwards 就可以以非常高的性能实现 ECC 密钥交换、数字签名、混合加密方案。

一个例子就是 [Curve25519](https://en.wikipedia.org/wiki/Curve25519)，它是 Edwards 曲线，其
Montgomery 形式的定义如下：

$$
y^{2}=x^{3}+486662x^{2}+x
$$

其被定义在有限域 $\mathbb {F} _{p}$ 上，$p = 2^{255} - 19$, 其他域参数如下：

- 阶 $n = 2^{252} + 0x14def9dea2f79cd65812631a5cf5d3ed$
- 辅因子 `h = 8`

虽然此曲线并未以 Edwards 形式定义，但是它已被证明与如下扭曲 Edwards 曲线（`edwards25519`）
双有理等价：

$$
-x^2 + y^2 = 1 + 37095705934669439343138083508754565189542113879843219016388785533085940283555 x^2 y^2
$$

上面给出的这种 Edwards 形式与前文给出的 Weierstrass 形式完全等价，是专为计算速度优化而设计
成这样的。

Curve25519 由 Daniel Bernstein 领导的密码学家团队精心设计，在多个设计和实现层面上达成了非
常高的性能，同时不影响安全性。

Curve25519 的构造使其避免了许多潜在的实现缺陷。根据设计，它不受定时攻击的影响，并且它接受
任何 32 字节的字符串作为有效的公钥，并且不需要验证。它能提供 125.8bits 的安全强度（有时称
为 ~ 128bits 安全性）

Curve25519 的私钥为 251 位，通常编码为 256 位整数（32 个字节，64 个十六进制数字）。公钥通
常也编码为 256 位整数（255 位 y 坐标 + 1 位 x 坐标），这对开发人员来说非常方便。

基于 Curve25519 派生出了名为 [X25519](https://en.wikipedia.org/wiki/Curve25519) 的 ECDH 算
法，以及基于 EdDSA 的高速数字签名算法
[Ed25519](https://en.wikipedia.org/wiki/EdDSA#Ed25519).

##### Curve448, X448 和 Ed448

> https://www.ietf.org/rfc/rfc7748.html#section-4.2

> https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed448/

[Curve448](https://en.wikipedia.org/wiki/Curve448)（Curve448-Goldilocks）是一种非扭曲
Edwards 曲线，它的方程定义如下：

$$
x^2 + y^2 = 1 - 39081 x^2 y^2
$$

其被定义在有限域 $\mathbb {F} _{p}$ 上，$p = 2^{448} - 2^{224} - 1$，其他域参数：

- 阶 $n = 2^{446} - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d$
- 辅助因子 `h = 4`

与 Curve25519 一样，Curve448 也等价于前面给出的 Weierstrass 形式，选择 Edwards 形式主要是
因为它能显著提升性能。

Curve448 提供 222.8 位的安全强度。Curve448 的私钥为 446 位，通常编码为 448 位整数（56 个字
节，112 个十六进制数字）。公钥也被编码为 448 位整数。

基于 Curve448 派生出了名为 [X448](https://tools.ietf.org/html/rfc7748#section-5) 的 ECDH
算法，以及基于 EdDSA 的高速数字签名算法
[Ed448](https://tools.ietf.org/html/rfc8032#section-5.2).

##### 该选择哪种椭圆曲线

首先，Bernstein 的 SafeCurves 标准列出了符合一组 ECC 安全要求的安全曲线，可访问
<https://safecurves.cr.yp.to> 了解此标准。

此外对于我们前面介绍的 Curve448 与 Curve25519，可以从性能跟安全性方面考量：

- 要更好的性能，可以接受弱一点的安全性：选择 Curve25519
- 要更好的安全性，可以接受比 Curve25519 慢 3 倍的计算速度：选择 Curve448

如果你的应用场景中暂时还很难用上 Curve448/Curve25519，你可以考虑一些应用更广泛的其他曲线，
但是一定要遵守如下安全规范：

- 模数 p 应该至少有 256 位
  - 比如 `secp224k1` `secp192k1` 啥的就可以扫进历史尘埃里了
- 暂时没有想补充的，可以参考 <https://safecurves.cr.yp.to>

目前（2022 年）在 TLS 协议以及 JWT 签名算法中，应用最广泛的椭圆曲线仍然是 NIST 系列：

- `P-256`: 目前仍然应用最为广泛的椭圆曲线
  - 在 openssl 中对应的名称为 `prime256v1`
- `P-384`
  - 在 openssl 中对应的名称为 `secp384r1`
- `P-521`
  - 在 openssl 中对应的名称为 `secp521r1`

但是我们也看到 `Curve25519` 正在越来越流行，因为美国政府有前科（[NSA 在 RSA
加密算法中安置后门是怎么一回事，有何影响？——知乎](https://www.zhihu.com/question/22343037），NIST
标准被怀疑可能有后门，目前很多人都在推动使用 `Curve25519` 等社区方案取代掉 NIST 标准曲线。

对于 openssl，如下命令会列出 openssl 支持的所有曲线：

```shell
openssl ecparam -list_curves
```

### ECIES - 集成加密方案

在文章开头我们已经介绍了集成加密方案 (IES)，它在密钥封装机制（KEM）的基础上，添加了密钥派
生算法 KDF、消息认证算法 MAC 等其他密码学算法以达成我们对消息的安全性、真实性、完全性的需
求。

而 ECIES 也完全类似，是在 ECC + 对称加密算法的基础上，添加了许多其他的密码学算法实现的。

ECIES 是一个加密框架，而不是某种固定的算法。它可以通过插拔不同的算法，形成不同的实现。比如
「secp256k1 + Scrypt + AES-GCM + HMAC-SHA512」。

大概就介绍到这里吧，后续就请在需要用到时自行探索相关的细节咯。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)
- [密码发展史之近现代密码 - 中国国家密码管理局][cryptography_history]
- [RFC6090 - Fundamental Elliptic Curve Cryptography Algorithms](https://datatracker.ietf.org/doc/html/rfc6090)
- [Which elliptic curve should I use?](https://security.stackexchange.com/questions/78621/which-elliptic-curve-should-i-use)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
[cryptography_history]: https://www.oscca.gov.cn/sca/zxfw/2017-04/24/content_1011711.shtml
[cryptograph_everyone_can_learn]: https://github.com/guoshijiang/cryptography
