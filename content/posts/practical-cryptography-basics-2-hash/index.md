---
title: "「译」写给开发人员的实用密码学（二）—— 哈希函数"
date: 2022-02-22T01:14:00+08:00
draft: false
resources:
- name: "featured-image"
  src: "cryptographic_hash_function.png"

tags: ["Cryptography", "Hash", "密码学", "哈希", "散列"]
categories: ["技术"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

>本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]

## 一、简介

**哈希函数**，或者叫**散列函数**，是一种从任何一种数据中创建一个**数字指纹**（摘要）的方法，散列函数把数据压缩压缩（或者放大）成一个长度固定的摘要。

哈希函数的输入空间（文本或者二进制数据）是可以无限大的，但是输出空间（一个固定长度的摘要）却是有限的。将「无限」映射到「有限」，不可避免的会有概率不同的输入得到相同的输出，这种情况我们称为**碰撞**（collision）。

一个好的哈希函数必须满足**抗碰撞**（collision-resistant）和**不可逆**（irreversible）这两个条件。
抗碰撞是通过统计学方法很难猜出哈希摘要对应的原始数据，而不可逆则是说攻击者很难逆向演算出原始数据。
只要找到碰撞以及逆向演算的难度足够大（比如用超级计算机需要花 10 年），我们就能认为原始数据是安全的。

但是也要注意，不同的场景对「难度足够大」的定义是不一样的。对普通人而言，用超级计算机需要花 10 年才能破解已经是「难度足够大」了，但是对国家机密而言，可能就还远远不够。
每种哈希算法，基本都会推出多种输出长度的版本，最常用的是 256 位，视场景你也可能需要使用更高级别的版本如 384/512 位。

一个简单的哈希函数是直接对输入数据/文本的字节求和。
它会导致大量的碰撞，例如 hello 和 ehllo 将具有相同的哈希值。
更好的哈希函数可以使用这样的方案，它将第一个字节作为状态，然后转换状态（例如，将它乘以像 31 这样的素数），然后将下一个字节添加到状态，然后再次转换状态并添加下一个字节等。
这样的操作可以显着降低碰撞概率并产生更均匀的分布。

一个理想的密码学哈希函数，应当具有如下属性：

- **快速**：计算速度要足够快
- **确定性**：同样的输入应该总是产生同样的输出
- **难以分析**：对输入的任何微小改动，都应该使输出完全发生变化
- **不可逆**：从其哈希值逆向演算出输入值应该是不可行的。这意味着没有比爆破更好的破解方法
- **无碰撞**：找到具有相同哈希的两条不同消息应该非常困难（或几乎不可能）

现代哈希函数（如 SHA2 和 SHA3）都具有上述几个属性，并被广泛应用在多个领域，各种现代编程语言和平台的标准库中基本都包含这些常用的哈希函数。

## 二、示例

下面是一个 SHA3-256 哈希转换的示例：

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

## 三、哈希函数的应用

哈希函数被广泛应用于数据校验、计算机编程和区块链系统中。

### 1. 数据完整性校验

哈希函数被广泛用于文件完整性校验。
如果你下载的文件计算出的 SHA256 校验和（checksum）跟官方公布的一致，那就说明文件没有损坏、也没有被篡改。

![](/images/practical-cryptography-basics-2-hash/openssl-sha256-checksum.png)

### 2. 哈希表

在编程领域，有一个使用哈希函数实现的数据结构被广泛使用——哈希表（Hash Table），或者称字典（Map, Dict）。

哈希表被用于存储键值对，它通过使用哈希函数，使得绝大多数的索引与插入的操作都可以非常快速地完成。

### 3. 保存密码

哈希函数还被用于密码的安全存储，现代系统使用专门设计的安全哈希算法计算用户密码的哈希摘要，保存到数据库中，这样能确保密码的安全性。除了用户自己，没有人清楚该密码的原始数据，即使数据库管理员也只能看到一个哈希摘要。

![](/images/practical-cryptography-basics-2-hash/sha512-password-hash.png)

### 4. 生成唯一 ID

哈希函数被用于为文档或消息生成（绝大多数情况下）唯一的 ID，因此哈希值也被称为**数字指纹**。

哈希函数计算出的哈希值理论上确实有碰撞的概率，但是这个概率实在太小了，因此绝大多数系统（如 Git）都假设哈希函数是无碰撞的（collistion free）。

通常文档的哈希值被用于证明该文档的存在性，或者被当成一个索引，用于从存储系统中提取文档。

使用哈希值作为唯一 ID 的典型例子，Git 版本控制系统（如 `3c3be25bc1757ca99aba55d4157596a8ea217698`）肯定算一个，比特币地址（如 `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2`）也算。


### 5. 伪随机数生成 - Pseudorandom Number Generation

哈希值可以被当作一个随机数看待，生成一个伪随机数的简单流程如下：

- 通过随机事件得到一个熵（例如键盘点击或鼠标移动），将它作为最初的随机数种子（random seed）。
- 添加一个 '1' 到熵中，得到第一个随机数
- 再添加一个 '2'，计算出第二个随机数
- 以此类推

### 6. PoW 工作量证明算法 - Proof-of-Work Algorithms

大部分工作量证明算法，都是要求计算出一个比特定值（称为挖掘难度）更大的哈希值。
因为哈希值是不可预测的，为了找出符合条件的哈希值，矿工需要计算数十亿个不同的哈希值，再从中找出最大的那个。
比如，一个工作量证明问题可能会被定义成这样：已有常数 `x`，要求找到一个数 `p`，使 `hash(x + p)` 的前十个比特都为 `0`.

## 四、哈希算法的安全性

过去，许多的加密哈希算法被提出，并被开发人员广泛使用。
其中一些已经被证明不安全啦（如 MD5 和 SHA1），而另一些则仍然被认为是安全的（如 SHA-2、SHA-3 和 BLAKE2）。让我们回顾一下使用最广泛的加密哈希函数（算法）。


### 安全的哈希算法

#### 1. SHA-2, SHA-256, SHA-512

[SHA-2](https://zh.wikipedia.org/wiki/SHA-2)，即 Secure Hash Algorithm 2，是一组强密码哈希函数：SHA-256（256位哈希）、SHA-384（384位哈希）、SHA-512（512位哈希）等。基于密码概念「Merkle–Damgård construction」，目前被认为是高度安全。 SHA-2 是 SHA-1 的继任者，于 2001 年在美国作为官方加密标准发布。

SHA-2 在软件开发和密码学中被广泛使用，它被认为在密码学上足够强大，可用于现代商业应用。

SHA-256 被广泛用于比特币区块链，例如用于识别交易哈希和矿工执行的工作证明挖掘。


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

按照设计，哈希函数的输出越长，就有望实现更高的安全性和抗碰撞能力（但也有一些例外）。
一般来说，128 位哈希算法比 256 位哈希算法弱，256 位哈希算法比 512 位哈希算法弱。

因此显然 SHA-512 比 SHA-256 更强。我们可以预期，SHA-512 的碰撞概率要比 SHA-256 更低。

#### 3. SHA-3, SHA3-256, SHA3-512, Keccak-256

在输出的哈希长度相同时，[SHA-3](https://zh.wikipedia.org/wiki/SHA-3)（及其变体 SHA3-224、SHA3-256、SHA3-384、SHA3-512）被认为拥有比 SHA-2（SHA-224、SHA-256、SHA-384、SHA-512）更高的加密强度。
例如，对于相同的哈希长度（256 位），SHA3-256 提供比 SHA-256 更高的加密强度。

SHA-3 系列函数是 Keccak 哈希家族的代表，它基于密码学概念[海绵函数](https://zh.wikipedia.org/wiki/%E6%B5%B7%E7%B6%BF%E5%87%BD%E6%95%B8)。Keccak 是[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的冠军。

与 SHA-2 不同，SHA-3 系列加密哈希函数不易受到[长度拓展攻击 Length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack).

SHA-3 被认为是高度安全的，并于 2015 年作为美国官方推荐的加密标准发布。

以太坊（Ethereum）区块链中使用的哈希函数 Keccak-256 是 SHA3-256 的变体，在代码中更改了一些常量。

哈希函数 `SHAKE128(msg, length)` 和 `SHAKE256(msg, length)` 是 SHA3-256 和 SHA3-512 算法的变体，它们输出消息的长度可以变化。

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

[BLAKE](https://en.wikipedia.org/wiki/BLAKE_%28hash_function) / BLAKE2 / BLAKE2s / BLAKE2b 是一系列快速、高度安全的密码学哈希函数，提供 160 位、224 位、256 位、384 位和 512 位摘要大小的计算，在现代密码学中被广泛应用。BLAKE 进入了[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的决赛。

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

[RIPEMD-160, RIPE Message Digest](https://en.wikipedia.org/wiki/RIPEMD) 是一种安全哈希函数，发布于 1996 年，目前主要被应用在 PGP 和比特币中。

RIPEMD 的 160 位变体在实践中被广泛使用，而 RIPEMD-128、RIPEMD-256 和 RIPEMD-320 等其他变体并不流行，并且它们的安全优势具有争议。

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

### 不安全的哈希算法

一些老一代的哈希算法，如 MD5, SHA-0 和 SHA-1 被认为是不安全的，并且由于加密漏洞（发现碰撞）而被撤回。**不要使用 MD5、SHA-0 和 SHA-1**！这些哈希函数都被证明在密码学上是不安全的。

使用这些不安全的哈希算法，可能会导致数字签名被伪造、密码泄漏等严重问题！

另外也请避免使用以下被认为不安全或安全性有争议的哈希算法： MD2, MD4, MD5, SHA-0, SHA-1, Panama, HAVAL（有争议的安全性，在 HAVAL-128 上发现了碰撞），Tiger（有争议，已发现其弱点），SipHash（假的加密哈希函数）。


### 其他安全哈希算法

以下是目前流行的强加密哈希函数，它们都可被用于替代 SHA-2、SHA-3 和 BLAKE2：

- Whirlpool 发布于 2000 年，此算法输出固定的 512 位哈希值。该算法使用512位的密钥，参考了分组密码的思路，使用轮函数加迭代，算法结构与 AES 相似。

- SM3 是中国国密密码杂凑算法标准，由国家密码管理局于 2010 年 12 月公布。它类似于 SHA-256（基于 Merkle-Damgård 结构），输出为 256 位哈希值。

- GOST（GOST R 34.11-94）哈希函数是俄罗斯的国家标准，它的输出也是 256 位哈希值。

以下函数是 SHA-2、SHA-3 和 BLAKE 的不太受欢迎的替代品，它们是[SHA3 NIST 比赛](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)的决赛入围者

- Skein 能够计算出 128、160、224、256、384、512 和 1024 位哈希值。
- Grøstl 能够计算出 224、256、384 和 512 位哈希值。
- JH 能够计算出 224、256、384 和 512 位哈希值。

### SHA-256、SHA3-256、BLAKE2s 和 RIPEMD-160 没有已知冲突

截至 2018 年 10 月，如下哈希算法仍然没有发现已知碰撞：SHA256、SHA3-256、Keccak-256、BLAKE2s、RIPEMD160 和其他一些算法。

## 五、PoW 工作量证明哈希函数 - Proof-of-Work Hash Functions

区块链中的 PoW 工作量证明挖矿算法使用了一类特殊的哈希函数，这些函数是计算密集型和内存密集型的。
这些哈希函数被设计成需要消耗大量计算资源和大量内存，并且很难在硬件设备（例如集成电路或矿机）中实现，也就难以设计专用硬件来加速计算。这种哈希函数被称为**抗 ASIC**，英文是 ASIC-resistant.

有许多哈希函数是专为工作量证明挖掘算法设计的，例如 ETHash、Equihash、CryptoNight 和 Cookoo Cycle. 
这些哈希函数的计算速度很慢，通常使用 GPU 硬件（如 NVIDIA GTX 1080 等显卡）或强大的 CPU 硬件（如 Intel Core i7-8700K）和大量快速 RAM 内存（如 DDR4 芯片）来执行这类算法。
这些挖矿算法的目标是通过刺激小型矿工（家庭用户和小型矿场）来**最大限度地减少挖矿的集中化**，并限制挖矿行业中高级玩家们（他们有能力建造巨型挖矿设施和数据中心）的力量。
与少数的高玩相比，**大量小玩家意味着更好的去中心化**。

目前大型虚拟货币挖矿公司手中的主要武器是 ASIC 矿机，因此，现代加密货币通常会要求使用「抗 ASIC 哈希算法」或「权益证明（proof-of-stake）共识协议」进行「工作量证明挖矿」，以限制这部分高级玩家，达成更好的去中心化。

### 1. ETHash

这里简要说明下以太坊区块链中使用的 ETHash 工作量证明挖掘哈希函数背后的思想。

ETHash 是以太坊区块链中的工作量证明哈希函数。它是内存密集型哈希函数（需要大量 RAM 才能快速计算），因此它被认为是抗 ASIC 的。

ETHash 的工作流程：

- 基于直到当前区块的整个链，为每个区块计算一个「种子」
- 从种子中计算出一个 16 MB 的伪随机缓存
- 从缓存中提取 1 GB 数据集以用于挖掘
- 挖掘涉及将数据集的随机切片一起进行哈希

更多信息参见 [eth.wiki - ethash](https://eth.wiki/en/concepts/ethash/ethash)

### 2. Equihash

简要解释一下 Zcash、Bitcoin Gold 和其他一些区块链中使用的 Equihash 工作量证明挖掘哈希函数背后的思想。

Equihash 是 Zcash 和 Bitcoin Gold 区块链中的工作量证明哈希函数。它是内存密集型哈希函数（需要大量 RAM 才能进行快速计算），因此它被认为是抗 ASIC 的。

Equihash 的工作流程：

- 基于直到当前区块的整个链，使用 BLAKE2b 计算出 50 MB 哈希数据集
- 在生成的哈希数据集上解决「广义生日问题」（从 2097152 中挑选 512 个不同的字符串，使得它们的二进制 XOR 为零）。已知最佳的解决方案（瓦格纳算法）在指数时间内运行，因此它需要大量的内存密集型和计算密集型计算
- 对前面得到的结果，进行双 SHA256 计算得到最终结果，即 `SHA256(SHA256(solution))`

更多信息参见 <https://github.com/tromp/equihash>


[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book

