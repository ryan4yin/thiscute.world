---
title: "写给开发人员的实用密码学（四）—— 安全随机数生成器 CSPRNG"
date: 2022-03-01T17:15:04+08:00
draft: false
resources:
  - name: "featured-image"
    src: "random-numbers.webp"

tags: ["Cryptography", "密码学", "伪随机数", "安全", "PRNG", "CSPRNG"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]
series_weight: 4
seriesNavigation: true

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]

## 一、前言

在密码学中，随机性（熵）扮演了一个非常重要的角色，许多密码学算法都要求使用一个不可预测的随机数，只有在生成的随机数不可预测时，这些算法才能保证其安全性。

比如 MAC 算法中的 key 就必须是一个不可预测的值，在这个条件下 MAC 值才是不可伪造的。

另外许多的高性能算法如快速排序、布隆过滤器、蒙特卡洛方法等，都依赖于随机性，如果随机性可以被预测，或者能够找到特定的输入值使这些算法变得特别慢，那黑客就能借此对服务进行 DDoS 攻击，以很小的成本达到让服务不可用的目的。

## 二、PRNG 伪随机数生成器

Pseudo-Random Number Generators(PRNG) 是一种数字序列的生成算法，它生成出的数字序列的统计学属性跟真正的随机数序列非常相似，但它生成的伪随机数序列并不是真正的随机数序列！因为该序列完全依赖于提供给 PRNG 的初始值，这个值被称为 PRNG 的种子。

算法流程如下，算法的每次迭代都生成出一个新的伪随机数：

{{< figure src="/images/practical-cryptography-basics-4-secure-random-generators/pseudorandom-number-generators.webp" >}}

如果输入的初始种子是相同的，PRNG 总是会生成出相同的伪随机数序列，因此 PRNG 也被称为 Deterministic Random Bit Generator (DRBG)，即确定性随机比特生成器。

实际上目前也有所谓的「硬件随机数生成器 TRNG」能生成出真正的随机数，但是因为 PRNG 的高速、低成本、可复现等原因，它仍然被大量使用在现代软件开发中。

PRNG 可用于从一个很小的初始随机性（熵）生成出大量的伪随机性，这被称做「拉伸（Stretching）」。

PRNG 被广泛应用在前面提到的各种依赖随机性的高性能算法以及密码学算法中。

### PRNG 的实现

我们在上一篇文章的「MAC 的应用」一节中提到，一个最简单的 PRNG 可以直接使用 MAC 算法实现，用 Python 实现如下：

```python
import hmac, hashlib
def random_number_generator(seed: bytes, max_num: int):
  state = seed
  counter = 0

  while True:
    state = hmac.new(state, bytes(counter), hashlib.sha1).digest()
    counter += 1

    # 这里取余实际上是压缩了信息，某种程度上说，这可以保证内部的真实状态 state 不被逆向出来
    yield int.from_bytes(state, byteorder="big") % max_num

# 测试下，计算 20 个 100 以内的随机数
gen = random_number_generator(b"abc", 100)
print([next(gen) for _ in range(20)])
# => [71, 41, 52, 18, 51, 14, 58, 30, 70, 20, 59, 93, 3, 10, 81, 63, 48, 67, 18, 36]
```

## 三、随机性 - 熵

如果初始的 PRNG 种子是完全不可预测的，PRNG 就能保证整个随机序列都不可预测。

因此在 PRNG 中，生成出一个足够随机的种子，就变得非常重要了。

一个最简单的方法，就是收集随机性。对于桌面电脑，随机性可以从鼠标的移动点击、按键事件、网络状况等随机输入来收集。这个事情是由操作系统在内核中处理的，内核会直接为应用程序提供随机数获取的 API，比如 Linux/MacOSX 的 `/dev/random` 虚拟设备。

如果这个熵的生成有漏洞，就很可能造成严重的问题，一个现实事件就是[安卓的 `java.security.SecureRandom` 漏洞导致安卓用户的比特币钱包失窃](https://bitcoinmagazine.com/technical/critical-vulnerability-found-in-android-wallets-1376273924)。

Python 的 `random` 库默认会使用当前时间作为初始 seed，这显然是不够安全的——黑客如果知道你运行程序的大概时间，就能通过遍历的方式暴力破解出你的随机数来！

## 四、CSPRNG 密码学安全随机数生成器

Cryptography Secure Random Number Generators(CSPRNG) 是一种适用于密码学领域的 PRNG，一个 PRNG 如果能够具备如下两个条件，它就是一个 CSPRNG:

- 能通过「下一比特测试 next-bit test」：即使有人获知了该 PRNG 的 k 位，他也无法使用合理的资源预测第 k+1 位的值
- 如果攻击者猜出了 PRNG 的内部状态或该状态因某种原因而泄漏，攻击者也无法重建出内部状态泄漏之前生成的所有随机数

有许多的设计都被证明可以用于构造一个 CSPRNG:

- 基于计数器(CTR)模式下的**安全[分组密码](https://zh.wikipedia.org/wiki/%E5%88%86%E7%BB%84%E5%AF%86%E7%A0%81)**、**[流密码](https://zh.wikipedia.org/wiki/%E6%B5%81%E5%AF%86%E7%A0%81)**或**安全散列函数**的 CSPRNG
- 基于数论设计的 CSPRNG，它依靠整数分解问题（IFP）、离散对数问题（DLP）或椭圆曲线离散对数问题（ECDLP）的高难度来确保安全性
- CSPRNG 基于加密安全随机性的特殊设计，例如 Yarrow algorithm 和 Fortuna，这俩分别被用于 MacOS 和 FreeBSD.

大多数的 CSPRNG 结合使用来自 OS 的熵与高质量的 PRNG，并且一旦系统生成了新的熵（这可能来自用户输入、磁盘 IO、系统中断、或者硬件 RNG），CSPRNG 会立即使用新的熵来作为 PRNG 新的种子。
这种不断重置 PRNG 种子的行为，使随机数变得非常难以预测。

### CSPRNG 的用途

- 加密程序：因为 OS 中熵的收集很缓慢，等待收集到足够多的熵再进行运算是不切实际的，因此很多的加密程序都使用 CSPRNG 来从系统的初始熵生成出足够多的伪随机熵。
- 其他需要安全随机数的场景 emmmm

## 如何在代码中使用 CSPRNG

多数系统都内置了 CSPRNG 算法并提供了内核 API，Unix-like 系统都通过如下两个虚拟设备提供 CSPRNG:

- `/dev/random`（受限阻塞随机生成器）: 从这个设备中读取到的是内核熵池中已经收集好的熵，如果熵池空了，此设备会一直阻塞，直到收集到新的环境噪声。
- `/dev/urandom`（不受限非阻塞随机生成器）: 它可能会返回内核熵池中的熵，也可能返回使用「之前收集的熵 + CSPRNG」计算出的安全伪随机数。它不会阻塞。

编程语言的 CSPRNG 接口或库如下：

- Java: `java.security.SecureRandom`
- Python: `secrets` 库或者 `os.urandom()`
- C#: `System.Security.Cryptography.RandomNumberGenerator.Create()`
- JavaScript: 客户端可使用 `window.crypto.getRandomValues(Uint8Array)`，服务端可使用 `crypto.randomBytes()`

比如使用 Python 实现一个简单但足够安全的随机密码生成器：

```python
import secrets
import string

chars = string.digits + "your_custom_-content" +  string.ascii_letters
def random_string(length: int):
    """生成随机字符串"""
    # 注意，这里不应该使用 random 库！而应该使用 secrets
    code = "".join(secrets.choice(chars) for _ in range(length))
    return code

random_string(24)
# => _rebBfgYs4OtkrPbYtnGmc4n
```

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
