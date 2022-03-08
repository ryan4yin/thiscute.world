---
title: "「译」写给开发人员的实用密码学（九）—— 数字证书与 TLS 协议"
date: 2022-03-01T21:34:02+08:00
draft: true
resources:
- name: "featured-image"
  src: "symmetric-vs-asymmetric.jpg"

tags: ["Cryptography", "密码学", "非对称加密", "安全", "TLS", "X509"]
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
- [「译」写给开发人员的实用密码学（八）—— 数字签名](/posts/practical-cryptography-basics-8-digital-signature/)
- [「译」写给开发人员的实用密码学（九）—— 数字证书与 TLS 协议](/posts/practical-cryptography-basics-9-quantum-safe-cryptography/)


PKI X509

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

