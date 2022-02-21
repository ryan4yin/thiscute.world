---
title: "「译」写给开发人员的实用密码学（二）—— 哈希函数"
date: 2022-02-21T11:46:00+08:00
draft: true
resources:
- name: "featured-image"
  src: "cryptographic_hash_function.png"

tags: ["Cryptography", "Hash", "密码学", "哈希"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]


在计算机中，**哈希函数**将文本或其他数据映射为一个整数。不同的输入通常映射到不同的输出，但有时可能会发生碰撞（collision）——即两个不同的输入映射到了同一个输出。

密码学散列函数将文本或二进制数据转换为一个固定长度的散列值，并且已知是抗碰撞冲突和不可逆的。下面是一个 SHA3-256 示例：

```
SHA3-256("hello") = "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392"
```

可以使用如下 Python 代码计算上面给出的 SHA3-256：

```python
import hashlib, binascii
sha3_256hash = hashlib.sha3_256(b'hello').digest()
print("SHA3-256('hello') =", binascii.hexlify(sha3_256hash))
```

或者如果你更熟悉 JavaScript，可以使用如下代码计算 SHA3-256:

```javascript
// 请首先 npm install js-sha3
sha3 = require('js-sha3');
let sha3_256hash = sha3.sha3_256('hello').toString();
console.log("SHA3-256('hello') =", sha3_256hash);
```




[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

