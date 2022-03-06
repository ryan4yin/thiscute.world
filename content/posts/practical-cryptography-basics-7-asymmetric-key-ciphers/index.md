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
  - 如果你需要跟 100 个朋友安全通信，你就要维护 100 个不同的对称密钥

这会导致巨大的「密钥交换」跟「密钥保存与管理」的成本。「公钥密码学」最大的优势就是，它解决了这两个问题。
因此公钥密码学成为了现代密码学的基石，而 1976 年是现代密码学的开端。

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

RSA 算法在计算机密码学的早期被广泛使用至今，但是随着 ECC 密码学的发展，ECC 在非对称密码系统中慢慢占据主导地位，因为它比 RSA 具有更高的安全性和更短的密钥长度。

RSA 算法提供如下几种功能：

- 密钥对生成：生成随机私钥（通常大小为 1024-4096 位）和相应的公钥。
- 加密：使用公钥加密消息（消息要先转换为 [0...key_length] 范围内的整数），然后使用密钥解密。
- 数字签名：签署消息（使用私钥）和验证消息签名（使用公钥）。
- 密钥交换：安全地传输密钥，用于以后的加密通信。

RSA 可以使用不同长度的密钥：1024、2048、3072、4096、8129、16384 甚至更多位。3072 位及以上的密钥长度被认为是安全的。
更长的密钥提供更高的安全性，但会消耗更多的计算时间，因此需要在安全性和速度之间进行权衡。
非常长的 RSA 密钥（例如 50000 位或 65536 位）对于实际使用可能太慢，例如密钥生成可能需要几分钟到几个小时。

### RSA 密钥对生成

原理及代码示例、openssl 示例

### RSA 加密与解密

原理及代码示例、openssl 示例


### RSA 数字签名

在第三章我们就介绍了 MAC 消息认证算法可以验证消息的真实性（authenticity）、完整性（integrity）、不可否认性（non-repudiation）。也提到 MAC 跟数字签名的功能是一致的，区别在于**数字签名算法属于公钥密码系统**，它使用私钥签名，使用公钥验证。

数字签名如今广泛用于签署数字合同、授权银行支付和签署公共区块链系统中的交易以转移数字资产。

大多数公钥密码系统（如 RSA 和 ECC）都提供安全的数字签名方案，如 DSA、ECDSA 和 EdDSA。我们将在本节后面更详细地讨论数字签名。

原理及代码示例、openssl 示例



## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)
- [密码发展史之近现代密码 - 中国国家密码管理局][cryptography_history]
- [人人都能看懂的密码学][cryptograph_everyone_can_learn]

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
[cryptography_history]: https://www.oscca.gov.cn/sca/zxfw/2017-04/24/content_1011711.shtml
[cryptograph_everyone_can_learn]: https://github.com/guoshijiang/cryptography
