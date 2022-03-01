---
title: "「译」写给开发人员的实用密码学（三）—— MAC 与密钥派生函数 KDF"
date: 2022-03-01T17:15:03+08:00
draft: true
resources:
- name: "featured-image"
  src: "key-derivation-function.png"

tags: ["Cryptography", "Hash", "密码学", "哈希", "散列"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]


《写给开发人员的实用密码学》系列文章目录：

- [「译」写给开发人员的实用密码学（一）—— 概览](/posts/practical-cryptography-basics-1/)
- [「译」写给开发人员的实用密码学（二）—— 哈希函数](/posts/practical-cryptography-basics-2-hash/)
- [「译」写给开发人员的实用密码学（三）—— MAC 与密钥派生函数 KDF](/posts/practical-cryptography-basics-3-key-derivation-function/)
- [「译」写给开发人员的实用密码学（四）—— 安全的随机数生成器](/posts/practical-cryptography-basics-4-secure-random-generators/)
- [「译」写给开发人员的实用密码学（五）—— 密钥交换与 DHKE](/posts/practical-cryptography-basics-5-key-exchange/)
- 待续


## 一、MAC 消息认证码

MAC 消息认证码，即 Message Authentication Code，是用于验证消息的一小段信息。
换句话说，能用它确认消息的真实性——消息来自指定的发件人并且没有被篡改。

MAC 值通过允许验证者（也拥有密钥）检测消息内容的任何更改来保护消息的数据完整性及其真实性。

一个安全的 MAC 函数，跟加密哈希函数非常类似，也拥有如下特性：

- **快速**：计算速度要足够快
- **确定性**：对同样的消息跟密钥，应该总是产生同样的输出
- **难以分析**：对消息或密钥的任何微小改动，都应该使输出完全发生变化
- **不可逆**：从 MAC 值逆向演算出消息跟密钥应该是不可行的。
- **无碰撞**：找到具有相同哈希的两条不同消息应该非常困难（或几乎不可能）

但是 MAC 算法比加密哈希函数多一个输入值：密钥，因此也被称为 keyed hash functions，即「加密钥的哈希函数」。

如下 Python 代码使用 key 跟 消息计算出对应的 HMAC-SHA256 值：

```python
import hashlib, hmac, binascii

key = b"key"
msg = b"some msg"

mac = hmac.new(key, msg, hashlib.sha256).digest()

print(f"HMAC-SHA256({key}, {msg})", binascii.hexlify(mac).decode('utf8'))

# => HMAC-SHA256(b'key', b'some msg') = 32885b49c8a1009e6d66662f8462e7dd5df769a7b725d1d546574e6d5d6e76ad
```

HMAC 的算法实际上非常简单，我参考 [wiki/HMAC](https://en.wikipedia.org/wiki/HMAC) 给出的伪码，编写了下面这个 Python 实现，没几行代码，但是完全 work：

```python
import hashlib, binascii

def xor_bytes(b1, b2):
  return bytes(a ^ c for a, c in zip(b1, b2))

def my_hmac(key, msg, hash_name):
  # hash => (block_size, output_size)
  # 单位是 bytes，数据来源于 https://en.wikipedia.org/wiki/HMAC
  hash_size_dict = {
    "md5": (64, 16),
    "sha1": (64, 20),
    "sha224": (64, 28),
    "sha256": (64, 32),
    # "sha512/224": (128, 28),  # 这俩算法暂时不清楚在 hashlib 里叫啥名
    # "sha512/256": (128, 32),
    "sha_384": (128, 48),
    "sha_512": (128, 64),
    "sha3_224": (144, 28),
    "sha3_256": (136, 32),
    "sha3_384": (104, 48),
    "sha3_512": (72, 64),
  }
  if hash_name not in hash_size_dict:
    raise ValueError("unknown hash_name")

  block_size, output_size = hash_size_dict[hash_name]
  hash_ = getattr(hashlib, hash_name)

  # 确保 key 的长度为 block_size
  block_sized_key = key
  if len(key) > block_size:
    block_sized_key = hash_(key).digest()  # 用 hash 函数进行压缩
  if len(key) < block_size:
    block_sized_key += b'\x00' * (block_size - len(key))  # 末尾补 0
  
  o_key_pad = xor_bytes(block_sized_key, (b"\x5c" * block_size))  # Outer padded key
  i_key_pad = xor_bytes(block_sized_key, (b"\x36" * block_size))  # Inner padded key

  return hash_(o_key_pad + hash_(i_key_pad + msg).digest()).digest()


# 下面验证下
key = b"key"
msg = b"some msg"

mac_ = my_hmac(key, msg, "sha256")
print(f"HMAC-SHA256({key}, {msg})", binascii.hexlify(mac_).decode('utf8'))

# 输出跟标准库完全一致：
# => HMAC-SHA256(b'key', b'some msg') = 32885b49c8a1009e6d66662f8462e7dd5df769a7b725d1d546574e6d5d6e76ad
```

### MAC 与哈希函数、数字签名的区别

上一篇文章提到过，哈希函数只负责生成哈希值，不负责哈希值的可靠传递。

而数字签名呢，跟 MAC 非常相似，但是数字签名使用的是非对称加密系统，更复杂，计算速度也更慢。

MAC 的功能跟数字签名一致，都是验证消息的真实性（authenticity）、完整性（integrity）、不可否认性（non-repudiation），但是 MAC 使用哈希函数或者对称密码系统来做这件事情，速度要更快，算法也更简单。

### MAC 的应用

#### 1. 验证消息的真实性、完整性

这是最简单的一个应用场景，在通信双向都持有一个预共享密钥的前提下，通信时都附带上消息的 MAC 码。
接收方也使用「收到的消息+预共享密钥」计算出 MAC 码，如果跟收到的一致，就说明消息真实无误。

注意这种应用场景中，消息是不保密的！

{{< figure src="/images/practical-cryptography-basics-3-key-derivation-function/mac-message-is-authentic.png" >}}

#### 2. AE 认证加密 - Authenticated encryption

常用的加密方法只能保证数据的保密性，并不能保证数据的完整性。

而这里介绍的 MAC 算法，或者还未介绍的基于非对称加密的数字签名，都只能保证数据的真实性、完整性，不能保证数据被安全传输。

而认证加密，就是结合加密算法与 MAC 算法的一种加密传输方式。
在确保 MAC 码「强不可伪造」的前提下，首先对数据进行加密，然后计算密文的 MAC 码，再同时传输密文与 MAC 码，就能同时保证数据的保密性、完整性、真实性，这种方法叫 Encrypt-then-MAC, 缩写做 EtM.
接收方在解密前先计算密文的 MAC 码与收到的对比，就能验证密文的完整性与真实性。


#### 3. 基于 MAC 的伪随机数生成器

MAC 码的另一个用途就是伪随机数生成函数，相比直接使用熵+哈希函数的进行伪随机数计算，MAC 码因为多引入了一个变量 key，理论上它会更安全。

这种场景下，我们称 MAC 使用的密钥为 `salt`，即盐。

```
next_seed = MAC(salt, seed)
```

## 二、KDF 密钥派生函数

我们都更喜欢使用密码来保护自己的数据而不是二进制的密钥，因为相比之下二进制密钥太难记忆了，字符形式的密码才是符合人类思维习惯的东西。

可对计算机而言就刚好相反了，现代密码学的很多算法都要求输入是一个大的数字，二进制的密钥就是这样一个大的数字。
因此显然我们需要一个将字符密码（Password）转换成密钥（Key）的函数，这就是密钥派生函数 Key Derivation Function.

直接使用 SHA256 之类的加密哈希函数来生成密钥是不安全的，因为为了方便记忆，通常密码并不会很长，绝大多数人的密码长度估计都不超过 15 位。
甚至很多人都在使用非常常见的弱密码，如 123456 admin 生日等等。
这就导致如果直接使用 SHA256 之类的算法，许多密码将很容易被暴力破解、字典攻击、彩虹表攻击等手段猜测出来！

KDF 目前主要从如下三个维度提升 hash 碰撞难度：

1. 时间复杂度：对应 CPU/GPU 计算资源
2. 空间复杂度：对应 Memory 内存资源
3. 并行维度：使用无法分解的算法，锁定只允许单线程运算

主要手段是加盐，以及多次迭代。这种设计方法被称为「密钥拉伸 Key stretching」。

因为它的独特属性，KDF 也被称作慢哈希算法。

目前比较著名的 KDF 算法主要有如下几个：

1. PBKDF2：这是一个非常简单的加密 KDF 算法，目前已经不推荐使用。
2. Bcrypt：安全性在下降，用得越来越少了。不建议使用。
3. Scrypt：可以灵活地设定使用的内存大小，在 argon2 不可用时，可使用它。
4. Argon2：目前最强的密码 Hash 算法，在 2015 年赢得了密码 Hash 竞赛。

如果你正在开发一个新的程序，需要使用到 KDF，建议选用 argon2/scrypt.

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

