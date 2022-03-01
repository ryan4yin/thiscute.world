---
title: "「译」写给开发人员的实用密码学（六）—— 对称密钥加密算法"
date: 2022-03-01T21:34:00+08:00
draft: true
resources:
- name: "featured-image"
  src: "symmetric-vs-asymmetric.jpg"

tags: ["Cryptography", "密码学", "对称加密", "安全"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文仍然在优化翻译质量、补充原文缺失的细节、代码示例。

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，但是也补充了一些我的代码示例及思考。


《写给开发人员的实用密码学》系列文章目录：

- [「译」写给开发人员的实用密码学（一）—— 概览](/posts/practical-cryptography-basics-1/)
- [「译」写给开发人员的实用密码学（二）—— 哈希函数](/posts/practical-cryptography-basics-2-hash/)
- [「译」写给开发人员的实用密码学（三）—— MAC 与密钥派生函数 KDF](/posts/practical-cryptography-basics-3-key-derivation-function/)
- [「译」写给开发人员的实用密码学（四）—— 安全的随机数生成器](/posts/practical-cryptography-basics-4-secure-random-generators/)
- [「译」写给开发人员的实用密码学（五）—— 密钥交换与 DHKE](/posts/practical-cryptography-basics-5-key-exchange/)
- [「译」写给开发人员的实用密码学（六）—— 对称密钥加密算法](/posts/practical-cryptography-basics-6-symmetric-key-ciphers/)
- [「译」写给开发人员的实用密码学（七）—— 非对称密钥加密算法](/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/)
- 待续



## 零、术语介绍

两个常用动词：

- 加密：cipher 或者 encrypt
- 解密：decipher 或者 decrypt

另外有几个名词有必要解释：

- cipher: 指用于加解密的「密码算法」
- cryptographic algorithm: 密码学算法，泛指密码学相关的各类算法
- ciphertext: 密文，即加密后的信息。对应的词是明文 plaintext
- password: 这个应该不需要解释，就是我们日常用的各种字符或者数字密码，也可称作口令。
- [passphrase](https://en.wikipedia.org/wiki/Passphrase): 翻译成「密码词组」或者「密碼片語」，通常指用于保护密钥或者其他敏感数据的一个 password.
  - 如果你用 ssh/gpg/openssl 等工具生成或使用过密钥，应该对它不陌生。

## 一、什么是对称加密

在密码学中，有两种加密方案被广泛使用：「对称加密」与「非对称加密」。

对称加密是指，加密与解密均是使用相同的密钥，因为这个特性，我们也称这个密钥为「共享密钥（Shared Secret Key）」，示意图如下：

{{< figure src="/images/practical-cryptography-basics-6-symmetric-key-ciphers/symmetric-cryptography.png" >}}

我们在第一章「概览」里介绍过，单纯使用对称加密算法并不能满足我们对消息真实性、完整性，因此通常我们会将对称加密算法跟其他算法组合成一个对称加密方案来使用。
加密方案可以包括：密钥派生函数（带有某些参数）+对称密码算法（带有某些参数）+密码块模式算法+消息认证（MAC）算法，如 AES-256-CTR-HMAC-SHA256 就表示一个使用 AES-256 与 Counter 块模式进行加密，使用 HMAC-SHA256 进行消息认证的加密方案。

现代密码学中广泛使用的对称加密算法（ciphers）有：AES（AES-128、AES-192、AES-256）、ChaCha20、Twofish、IDEA、Serpent、Camelia等。其中大多数是块密码（通过固定大小的块加密数据，例如 128 位），而其他是流密码（将数据逐字节加密为流）。通过使用称为“密码块模式”的技术，可以将块密码转换为流密码。


## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

