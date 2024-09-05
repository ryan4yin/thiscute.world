---
title: "写给开发人员的实用密码学（二）—— 哈希函数"
date: 2022-03-01T17:15:01+08:00
draft: false
resources:
  - name: "featured-image"
    src: "cryptographic_hash_function.webp"

tags: ["Cryptography", "Hash", "密码学", "哈希", "散列", "安全", "SHA-2", "SHA-3"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]

seriesNavigation: true

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，笔者额外补充了
> 「非加密哈希函数」的简单介绍。

## 一、什么是哈希函数

**哈希函数**，或者叫**散列函数**，是一种从任何一种数据中创建一个**数字指纹**（也叫数字摘
要）的方法，散列函数把数据压缩（或者放大）成一个长度固定的字符串。

哈希函数的输入空间（文本或者二进制数据）是无限大，但是输出空间（一个固定长度的摘要）却是有
限的。将「无限」映射到「有限」，不可避免的会有概率不同的输入得到相同的输出，这种情况我们称
为**碰撞**（collision）。

一个简单的哈希函数是直接对输入数据/文本的字节求和。它会导致大量的碰撞，例如 hello 和 ehllo
将具有相同的哈希值。

更好的哈希函数可以使用这样的方案：它将第一个字节作为状态，然后转换状态（例如，将它乘以像
31 这样的素数），然后将下一个字节添加到状态，然后再次转换状态并添加下一个字节等。这样的操
作可以显着降低碰撞概率并产生更均匀的分布。

## 二、加密哈希函数

加密哈希函数（也叫密码学哈希函数）是指一类有特殊属性的哈希函数。

一个好的「加密哈希函数」必须满足**抗碰撞**（collision-resistant）和**不可
逆**（irreversible）这两个条件。抗碰撞是指通过统计学方法（彩虹表）很难或几乎不可能猜出哈希
值对应的原始数据，而不可逆则是说攻击者很难或几乎不可能从算法层面通过哈希值逆向演算出原始数
据。

具体而言，一个理想的**加密哈希函数**，应当具有如下属性：

- **快速**：计算速度要足够快
- **确定性**：对同样的输入，应该总是产生同样的输出
- **难以分析**：对输入的任何微小改动，都应该使输出完全发生变化
- **不可逆**：从其哈希值逆向演算出输入值应该是不可行的。这意味着没有比暴力破解更好的破解方
  法
- **无碰撞**：找到具有相同哈希值的两条不同消息应该非常困难（或几乎不可能）

现代加密哈希函数（如 SHA2 和 SHA3）都具有上述几个属性，并被广泛应用在多个领域，各种现代编
程语言和平台的标准库中基本都包含这些常用的哈希函数。

### 量子安全性

现代密码学哈希函数（如 SHA2, SHA3, BLAKE2）都被认为是量子安全的，无惧量子计算机的发展。

### 加密哈希函数的应用

#### 1. 数据完整性校验

加密哈希函数被广泛用于文件完整性校验。如果你从网上下载的文件计算出的 SHA256 校验和
（checksum）跟官方公布的一致，那就说明文件没有损坏。

但是哈希函数自身不能保证文件的真实性，目前来讲，真实性通常是 TLS 协议要保证的，它确保你在
openssl 网站上看到的「SHA256 校验和」真实无误（未被篡改）。

{{< figure src="/images/practical-cryptography-basics-2-hash/openssl-sha256-checksum.webp" >}}

> 现代网络基本都很难遇到文件损坏的情况了，但是在古早的低速网络中，即使 TCP 跟底层协议已经
> 有多种数据纠错手段，下载完成的文件仍然是有可能损坏的。这也是以前 rar 压缩格式很流行的原
> 因之一—— rar 压缩文件拥有一定程度上的自我修复能力，传输过程中损坏少量数据，仍然能正常解
> 压。

#### 2. 保存密码

加密哈希函数还被用于密码的安全存储，现代系统使用专门设计的安全哈希算法计算用户密码的哈希摘
要，保存到数据库中，这样能确保密码的安全性。除了用户自己，没有人清楚该密码的原始数据，即使
数据库管理员也只能看到一个哈希摘要。

{{< figure src="/images/practical-cryptography-basics-2-hash/sha512-password-hash.webp" >}}

#### 3. 生成唯一 ID

加密哈希函数也被用于为文档或消息生成（绝大多数情况下）唯一的 ID，因此哈希值也被称为**数字
指纹**。

> 注意这里说的是数字指纹，而非数字签名。数字签名是与下一篇文章介绍的「MAC」码比较类似的，
> 用于验证消息的真实、完整、认证作者身份的一段数据。

加密哈希函数计算出的哈希值理论上确实有碰撞的概率，但是这个概率实在太小了，因此绝大多数系统
（如 Git）都假设哈希函数是无碰撞的（collision free）。

文档的哈希值可以被用于证明该文档的存在性，或者被当成一个索引，用于从存储系统中提取文档。

使用哈希值作为唯一 ID 的典型例子，Git 版本控制系统（如
`3c3be25bc1757ca99aba55d4157596a8ea217698`）肯定算一个，比特币地址（如
`1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2`）也算。

#### 4. 伪随机数生成

哈希值可以被当作一个随机数看待，生成一个伪随机数的简单流程如下：

- 通过随机事件得到一个熵（例如键盘点击或鼠标移动），将它作为最初的随机数种子（random
  seed）。
- 添加一个 `1` 到熵中，进行哈希计算得到第一个随机数
- 再添加一个 `2`，进行哈希计算得到第二个随机数
- 以此类推

当然为了确保安全性，实际的加密随机数生成器会比这再复杂一些，我们会在后面的「随机数生成器」
一节学习其中细节。

### 安全的加密哈希算法

#### 1. SHA-2, SHA-256, SHA-512

[SHA-2](https://zh.wikipedia.org/wiki/SHA-2)，即 Secure Hash Algorithm 2，是一组强密码哈希
函数，其成本包括：SHA-256（256位哈希）、SHA-384（384位哈希）、SHA-512（512位哈希）等。基于
密码概念「Merkle–Damgård 构造」，目前被认为高度安全。 SHA-2 是 SHA-1 的继任者，于 2001 年
在美国作为官方加密标准发布。

SHA-2 在软件开发和密码学中被广泛使用，可用于现代商业应用。其中 SHA-256 被广泛用于 HTTPS 协
议、文件完整性校验、比特币区块链等各种场景。

Python 代码示例：

```python
import hashlib, binascii

text = 'hello'
data = text.encode("utf8")

sha256hash = hashlib.sha256(data).digest()
print(f"SHA-256({text}) = ", binascii.hexlify(sha256hash).decode("utf8"))

sha384hash = hashlib.sha384(data).digest()
print(f"SHA-384({text}) = ", binascii.hexlify(sha384hash).decode("utf8"))

sha512hash = hashlib.sha512(data).digest()
print(f"SHA-512({text}) = ", binascii.hexlify(sha512hash).decode("utf8"))
```

输出如下：

```
SHA-256('hello') = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
SHA-384('hello') = 59e1748777448c69de6b800d7a33bbfb9ff1b463e44354c3553bcdb9c666fa90125a3c79f90397bdf5f6a13de828684f
SHA-512('hello') = 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043
```

#### 2. 更长的哈希值 == 更高的抗碰撞能力

按照设计，哈希函数的输出越长，就有望实现更高的安全性和抗碰撞能力（但也有一些例外）。一般来
说，128 位哈希算法比 256 位哈希算法弱，256 位哈希算法比 512 位哈希算法弱。

因此显然 SHA-512 比 SHA-256 更强。我们可以预期，SHA-512 的碰撞概率要比 SHA-256 更低。

#### 3. SHA-3, SHA3-256, SHA3-512, Keccak-256

在输出的哈希长度相同时，[SHA-3](https://zh.wikipedia.org/wiki/SHA-3)（及其变体
SHA3-224、SHA3-256、SHA3-384、SHA3-512）被认为拥有比
SHA-2（SHA-224、SHA-256、SHA-384、SHA-512）更高的加密强度。例如，对于相同的哈希长度（256
位），SHA3-256 提供比 SHA-256 更高的加密强度。

SHA-3 系列函数是 Keccak 哈希家族的代表，它基于密码学概
念[海绵函数](https://zh.wikipedia.org/wiki/%E6%B5%B7%E7%B6%BF%E5%87%BD%E6%95%B8)。而Keccak
是[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的
冠军。

与 SHA-2 不同，SHA-3 系列加密哈希函数不易受
到[长度拓展攻击 Length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack).

SHA-3 被认为是高度安全的，并于 2015 年作为美国官方推荐的加密标准发布。

以太坊（Ethereum）区块链中使用的哈希函数 Keccak-256 是 SHA3-256 的变体，在代码中更改了一些
常量。

哈希函数 `SHAKE128(msg, length)` 和 `SHAKE256(msg, length)` 是 SHA3-256 和 SHA3-512 算法的
变体，它们输出消息的长度可以变化。

SHA3 的 Python 代码示例：

```python
import hashlib, binascii

text = 'hello'
data = text.encode("utf8")

sha3_256hash = hashlib.sha3_256(data).digest()
print(f"SHA3-256({text}) = ", binascii.hexlify(sha3_256hash).decode("utf8"))

sha3_512hash = hashlib.sha3_512(data).digest()
print(f"SHA3-512({text}) = ", binascii.hexlify(sha3_512hash).decode("utf8"))
```

输出：

```
SHA3-256('hello') = 3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392
Keccak-256('hello') = 1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8
SHA3-512('hello') = 75d527c368f2efe848ecf6b073a36767800805e9eef2b1857d5f984f036eb6df891d75f72d9b154518c1cd58835286d1da9a38deba3de98b5a53e5ed78a84976

SHAKE-128('hello', 256) = 4a361de3a0e980a55388df742e9b314bd69d918260d9247768d0221df5262380
SHAKE-256('hello', 160) = 1234075ae4a1e77316cf2d8000974581a343b9eb
```

#### 4. BLAKE2 / BLAKE2s / BLAKE2b

[BLAKE](https://en.wikipedia.org/wiki/BLAKE_%28hash_function) / BLAKE2 / BLAKE2s / BLAKE2b
是一系列快速、高度安全的密码学哈希函数，提供 160 位、224 位、256 位、384 位和 512 位摘要大
小的计算，在现代密码学中被广泛应用。BLAKE 进入
了[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的
决赛。

- BLAKE2 函数是 BLAKE 的改进版本。
- BLAKE2s（通常为 256 位）是 BLAKE2 实现，针对 32 位微处理器进行了性能优化。
- BLAKE2b（通常为 512 位）是 BLAKE2 实现，针对 64 位微处理器进行了性能优化。

BLAKE2 哈希函数具有与 SHA-3 类似的安全强度，但开发人员目前仍然更倾向于使用 SHA2 和 SHA3。

BLAKE 哈希值的 Python 示例：

```python
import hashlib, binascii

text = 'hello'
data = text.encode("utf8")

blake2s = hashlib.new('blake2s', data).digest()
print("BLAKE2s({text}) = ", binascii.hexlify(blake2s).decode("utf-8"))

blake2b = hashlib.new('blake2b', data).digest()
print("BLAKE2b({text}) = ", binascii.hexlify(blake2b).decode("utf-8"))
```

输出如下：

```
BLAKE2s('hello') = 19213bacc58dee6dbde3ceb9a47cbb330b3d86f8cca8997eb00be456f140ca25
BLAKE2b('hello') = e4cfa39a3d37be31c59609e807970799caa68a19bfaa15135f165085e01d41a65ba1e1b146aeb6bd0092b49eac214c103ccfa3a365954bbbe52f74a2b3620c94
```

#### 5. RIPEMD-160

[RIPEMD-160, RIPE Message Digest](https://en.wikipedia.org/wiki/RIPEMD) 是一种安全哈希函
数，发布于 1996 年，目前主要被应用在 PGP 和比特币中。

RIPEMD 的 160 位变体在实践中被广泛使用，而 RIPEMD-128、RIPEMD-256 和 RIPEMD-320 等其他变体
并不流行，并且它们的安全优势具有争议。

建议优先使用 SHA-2 和 SHA-3 而不是 RIPEMD，因为它们输出的哈希值更长，抗碰撞能力更强。

Python 示例：

```python
import hashlib, binascii

text = 'hello'
data = text.encode("utf8")

ripemd160 = hashlib.new('ripemd160', data).digest()
print("RIPEMD-160({text}) = ", binascii.hexlify(ripemd160).decode("utf-8"))

# => RIPEMD-160({text}) =  108f07b8382412612c048d07d13f814118445acd
```

#### 6. 其他安全哈希算法

以下是目前流行的强加密哈希函数，它们都可被用于替代 SHA-2、SHA-3 和 BLAKE2：

- **Whirlpool** 发布于 2000 年，此算法输出固定的 512 位哈希值。该算法使用512位的密钥，参考
  了分组密码的思路，使用轮函数加迭代，算法结构与 AES 相似。

- **SM3** 是中国国密密码杂凑算法标准，由国家密码管理局于 2010 年 12 月公布。它类似于
  SHA-256（基于 Merkle-Damgård 结构），输出为 256 位哈希值。

- **GHOST**（GHOST R 34.11-94）哈希函数是俄罗斯的国家标准，它的输出也是 256 位哈希值。

以下函数是 SHA-2、SHA-3 和 BLAKE 的不太受欢迎的替代品，它们
是[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的
决赛入围者

- **Skein** 能够计算出 128、160、224、256、384、512 和 1024 位哈希值。
- **Grøstl** 能够计算出 224、256、384 和 512 位哈希值。
- **JH** 能够计算出 224、256、384 和 512 位哈希值。

### 不安全的加密哈希算法

一些老一代的加密哈希算法，如 MD5, SHA-0 和 SHA-1 被认为是不安全的，并且都存在已被发现的加
密漏洞（碰撞）。**不要使用 MD5、SHA-0 和 SHA-1**！这些哈希函数都已被证明不够安全。

使用这些不安全的哈希算法，可能会导致数字签名被伪造、密码泄漏等严重问题！

另外也请避免使用以下被认为不安全或安全性有争议的哈希算法： **MD2, MD4, MD5, SHA-0, SHA-1,
Panama**, **HAVAL**（有争议的安全性，在 HAVAL-128 上发现了碰撞），**Tiger**（有争议，已发
现其弱点），**SipHash**（它属于非加密哈希函数）。

### PoW 工作量证明哈希函数

区块链中的 Proof-of-Work 工作量证明挖矿算法使用了一类特殊的哈希函数，这些函数是计算密集型
和内存密集型的。这些哈希函数被设计成需要消耗大量计算资源和大量内存，并且很难在硬件设备（例
如集成电路或矿机）中实现，也就难以设计专用硬件来加速计算。这种哈希函数被称为**抗
ASIC**（ASIC-resistant）。

大部分工作量证明（Proof-of-Work）算法，都是要求计算出一个比特定值（称为挖掘难度）更大的哈
希值。因为哈希值是不可预测的，为了找出符合条件的哈希值，矿工需要计算数十亿个不同的哈希值，
再从中找出最大的那个。比如，一个工作量证明问题可能会被定义成这样：已有常数 `x`，要求找到一
个数 `p`，使 `hash(x + p)` 的前十个比特都为 `0`.

有许多哈希函数是专为工作量证明挖掘算法设计的，例如 ETHash、Equihash、CryptoNight 和 Cuckoo
Cycle. 这些哈希函数的计算速度很慢，通常使用 GPU 硬件（如 NVIDIA GTX 1080 等显卡）或强大的
CPU 硬件（如 Intel Core i7-8700K）和大量快速 RAM 内存（如 DDR4 芯片）来执行这类算法。这些
挖矿算法的目标是通过刺激小型矿工（家庭用户和小型矿场）来**最大限度地减少挖矿的集中化**，并
限制挖矿行业中高级玩家们（他们有能力建造巨型挖矿设施和数据中心）的力量。与少数的高玩相
比，**大量小玩家意味着更好的去中心化**。

目前大型虚拟货币挖矿公司手中的主要武器是 ASIC 矿机，因此，现代加密货币通常会要求使用「抗
ASIC 哈希算法」或「权益证明（proof-of-stake）共识协议」进行「工作量证明挖矿」，以限制这部
分高级玩家，达成更好的去中心化。

> 因为工作量证明算法需要消耗大量能源，不够环保，以太坊等区块链已经声明未来将会升级到权益证
> 明（Proof-of-S）这类更环保的算法。不过这里我们只关注 PoW 如何基于哈希函数实现的，不讨论
> 这个。

#### 1. ETHash

这里简要说明下以太坊区块链中使用的 ETHash 工作量证明挖掘哈希函数背后的思想。

ETHash 是以太坊区块链中的工作量证明哈希函数。它是内存密集型哈希函数（需要大量 RAM 才能快速
计算），因此它被认为是抗 ASIC 的。

ETHash 的工作流程：

- 基于直到当前区块的整个链，为每个区块计算一个「种子」
- 从种子中计算出一个 16 MB 的伪随机缓存
- 从缓存中提取 1 GB 数据集以用于挖掘
- 挖掘涉及将数据集的随机切片一起进行哈希

更多信息参见 [eth.wiki - ethash](https://eth.wiki/en/concepts/ethash/ethash)

#### 2. Equihash

简要解释一下 Zcash、Bitcoin Gold 和其他一些区块链中使用的 Equihash 工作量证明挖掘哈希函数
背后的思想。

Equihash 是 Zcash 和 Bitcoin Gold 区块链中的工作量证明哈希函数。它是内存密集型哈希函数（需
要大量 RAM 才能进行快速计算），因此它被认为是抗 ASIC 的。

Equihash 的工作流程：

- 基于直到当前区块的整个链，使用 BLAKE2b 计算出 50 MB 哈希数据集
- 在生成的哈希数据集上解决「广义生日问题」（从 2097152 中挑选 512 个不同的字符串，使得它们
  的二进制 XOR 为零）。已知最佳的解决方案（瓦格纳算法）在指数时间内运行，因此它需要大量的
  内存密集型和计算密集型计算
- 对前面得到的结果，进行双 SHA256 计算得到最终结果，即 `SHA256(SHA256(solution))`

更多信息参见 <https://github.com/tromp/equihash>

## 三、非加密哈希函数

加密哈希函数非常看重「加密」，为了实现更高的安全强度，费了非常多的心思、也付出了很多代价。

但是实际应用中很多场景是不需要这么高的安全性的，相反可能会对速度、随机均匀性等有更高的要
求。这就催生出了很多「非加密哈希函数」。

非加密哈希函数的应用场景有很多：

- 哈希表 Hash Table: 在很多语言中也被称为 map/dict，它使用的算法很简单，通常就是把对象的各
  种属性不断乘个质数（比如 31）再相加，哈希空间会随着表的变化而变化。这里最希望的是数据的
  分布足够均匀。
- 一致性哈希：目的是解决分布式缓存的问题。在移除或者添加一个服务器时，能够尽可能小地改变已
  存在的服务请求与处理请求服务器之间的映射关系。
- 高性能哈希算法：SipHash MurMurHash3 等，使用它们的目的可能是对数据进行快速去重，要求就是
  足够快。

有时我们甚至可能不太在意哈希碰撞的概率。也有的场景输入是有限的，这时我们可能会希望哈希函数
具有可逆性。

总之非加密哈希函数也有非常多的应用，但不是本文的主题。这里就不详细介绍了，有兴趣的朋友们可
以自行寻找其他资源。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [漫谈非加密哈希算法](https://segmentfault.com/a/1190000010990136)
- [开发中常见的一些Hash函数（一）](http://thomaslau.xyz/2020/05/20/2020-05-20-on_hash_1/)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
