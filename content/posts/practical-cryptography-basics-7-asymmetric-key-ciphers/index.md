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


## 一、什么是非对称加密

待续

{{< figure src="/images/practical-cryptography-basics-7-asymmetric-key-ciphers/asymmetric-cryptography.png" >}}


## 二、公钥密码学

在介绍非对称密钥加密方案和算法之前，我们首先要了解公钥密码学的概念。

公钥密码术使用不同的密钥来加密和解密数据（或签名和验证消息）。
密钥始终以公钥 + 私钥对的形式出现。
非对称密码学处理使用公钥/私钥加密和解密消息、签署消息、验证签名和安全地交换密钥。

流行的公钥密码系统（非对称密码算法），如 RSA（Rivest–Shamir–Adleman）、ECC（椭圆曲线密码学）、Diffie-Hellman、ECDH、ECDSA 和 EdDSA，广泛用于现代密码学中，我们将演示大部分他们在实践中使用代码示例。


公钥密码系统提供数学框架和算法来生成公钥+私钥对，以加密安全的方式对消息进行签名、验证、加密和解密以及交换密钥。

比较著名的公钥密码系统有：RSA、ECC 和 ElGamal。许多密码算法都基于这些密码系统的原语，例如 RSA 签名、RSA 加密/解密、ECDH 密钥交换以及 ECDSA 和 EdDSA 签名。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

