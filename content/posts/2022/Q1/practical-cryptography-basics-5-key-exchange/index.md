---
title: "写给开发人员的实用密码学（五）—— 密钥交换 DHKE 与完美前向保密 PFS"
date: 2022-03-01T17:15:05+08:00
lastmod: 2022-03-13T15:26:00+08:00
draft: false
resources:
  - name: "featured-image"
    src: "dhke.webp"

tags: ["Cryptography", "密码学", "密钥交换", "安全", "DH", "DHE", "ECDH", "ECDHE"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]
series_weight: 5
seriesNavigation: true

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，笔者额外补充了
> DHKE/ECDH 的代码示例，以及「PFS 完美前向保密协议 DHE/ECDHE」一节。

## 一、前言

在密码学中**密钥交换**是一种协议，功能是在两方之间安全地交换加密密钥，其他任何人都无法获得
密钥的副本。通常各种加密通讯协议的第一步都是密钥交换。密钥交换技术具体来说有两种方案：

- 密钥协商：协议中的双方都参与了共享密钥的生成，两个代表算法是 Diffie-Hellman (DHKE) 和
  Elliptic-Curve Diffie-Hellman (ECDH)
- 密钥传输：双方中其中一方生成出共享密钥，并通过此方案将共享密钥传输给另一方。密钥传输方案
  通常都通过公钥密码系统实现。比如在 RSA 密钥交换中，客户端使用它的私钥加密一个随机生成的
  会话密钥，然后将密文发送给服务端，服务端再使用它的公钥解密出会话密钥。

密钥交换协议无时无刻不在数字世界中运行，在你连接 WiFi 时，或者使用 HTTPS 协议访问一个网
站，都会执行密钥交换协议。密钥交换有很多手段，常见手段有匿名的 DHKE 密钥协商协议、密码或预
共享密钥、数字证书等等。有些通讯协议只在开始时交换一次密钥，而有些协议则会随着时间的推移不
断地交换密钥。

认证密钥交换（ACHE）是一种会同时认证相关方身份的密钥交换协议，比如个人 WiFi 通常就会使用
password-authenticated key agreement (PAKE)，而如果你连接的是公开 WiFi，则会使用匿名密钥交
换协议。

目前有许多用于密钥交换的密码算法。其中一些使用公钥密码系统，而另一些则使用更简单的密钥交换
方案（如 Diffie-Hellman 密钥交换）；其中有些算法涉及服务器身份验证，也有些涉及客户端身份验
证；其中部分算法使用密码，另一部分使用数字证书或其他身份验证机制。下面列举一些知名的密钥交
换算法：

- Diffie-Hellman Key Exchange (DHКЕ)：传统的、应用最为广泛的密钥交换协议
- Elliptic-curve Diffie–Hellman (ECDH)：基于椭圆曲线密码学的密钥交换算法，DHKE 的继任者
- RSA-OAEP 和 RSA-KEM（RSA 密钥传输）
- PSK（预共享密钥）
- SRP（安全远程密码协议）
- FHMQV（Fully Hashed Menezes-Qu-Vanstone）
- ECMQV（Ellictic-Curve Menezes-Qu-Vanstone）
- CECPQ1（量子安全密钥协议）

## 二、Diffie–Hellman 密钥交换

迪菲-赫尔曼密钥交换（Diffie–Hellman Key Exchange）是一种安全协议，它可以让双方在完全没有对
方任何预先信息的条件下通过不安全信道安全地协商出一个安全密钥，而且任何窃听者都无法得知密钥
信息。这个密钥可以在后续的通讯中作为对称密钥来加密通讯内容。

DHKE 可以防范嗅探攻击（窃听），但是无法抵挡中间人攻击（中继）。

DHKE 有两种实现方案：

- 传统的 DHKE 算法：使用离散对数实现
- 基于椭圆曲线密码学的 ECDH

为了理解 DHKE 如何实现在「大庭广众之下」安全地协商出密钥，我们首先使用色彩混合来形象地解释
下它大致的思路。

跟编程语言的 Hello World 一样，密钥交换的解释通常会使用 Alice 跟 Bob 来作为通信双方。现在
他俩想要在公开的信道上，协商出一个**秘密色彩**出来，但是不希望其他任何人知道这个**秘密色
彩**。他们可以这样做：

{{< figure src="/images/practical-cryptography-basics-5-key-exchange/key-exchange-by-mixing-color.webp" >}}

分步解释如下：

- 首先 Alice 跟 Bob 沟通，确定一个**初始的色彩**，比如黄色。这个沟通不需要保密。
- 然后，Alice 跟 Bob 分别偷偷地选择出一个自己的**秘密色彩**，这个就得保密啦。
- 现在 Alice 跟 Bob，分别将**初始色彩**跟自己选择的**秘密色彩**混合，分别得到两个**混合色
  彩**。
- 之后，Alice 跟 Bob 再回到公开信道上，交换双方的**混合色彩**。
  - 我们假设在仅知道**初始色彩**跟**混合色彩**的情况下，很难推导出被混合的**秘密色彩**。这
    样第三方就猜不出 Bob 跟 Alice 分别选择了什么**秘密色彩**了。
- 最后 Alice 跟 Bob 再分别将**自己的秘密色彩**，跟**对方的混合色彩**混合，就得到了最终
  的**秘密色彩**。这个最终色彩只有 Alice 跟 Bob 知道，信道上的任何人都无法猜出来。

DHKE 协议也是基于类似的原理，但是使用的是离散对数（discrete logarithms）跟模幂（modular
exponentiations）而不是色彩混合。

## 三、经典 DHKE 协议

### 基础数学知识

首先介绍下「模幂（modular exponentiations）」，它是指求 $g$ 的 $a$ 次幂模 $p$ 的值 $c$ 的
过程，其中 $g$ $a$ $p$ $c$ 均为整数，公式如下：

$$
g^a \mod p = c
$$

而「离散对数（discrete logarithms）」，其实就是指模幂的逆运算，它使用如下公式表示：

$$
Ind_{g}c \equiv a {\pmod {p}}
$$

上述公式，即指在已知整数 $g$，质数 $p$，以及余数（p 的一个原根） $c$ 的情况下，求使前面的
模幂等式成立的幂指数 $a$。

已知使用计算机计算上述「模幂」是非常快速的，但是在质数 $p$ 非常大的情况下，求「离散对数」
却是非常难的，这就是「离散对数难题」。

然后为了理解 DHKE 的原理，我们还需要了解下模幂运算的一个性质：

$$
g^{ab} \mod p = {(g^a \mod p)}^b \mod p
$$

懂了上面这些基础数学知识，下面就开始介绍 DHKE 算法。

### DHKE 密钥交换流程

下面该轮到 Alice 跟 Bob 出场来介绍 DHKE 的过程了，先看图（下面<span style="color:green">绿
色</span>表示非秘密信息，<span style="color:red">**红色**</span>表示秘密信息）：

{{< figure src="/images/practical-cryptography-basics-5-key-exchange/diffle-hellman.webp" >}}

- Alice 跟 Bob 协定使用两个比较独特的正整数 <span style="color:green">$p$</span> 跟
  <span style="color:green">$g$</span>
  - 假设 <span style="color:green">$p=23$, $g=5$</span>
- Alice 选择一个秘密整数 <span style="color:red">$a$</span>，计算
  <span style="color:green">$A$</span>$\ = g^a \mod p$ 并发送给 Bob
  - 假设 <span style="color:red">$a=4$</span>，则
    <span style="color:green">$A$</span>$\ = 5^4 \mod 23 = 4$
- Bob 也选择一个秘密整数 <span style="color:red">$b$</span>，计算
  <span style="color:green">$B$</span>$\ = g^b \mod p$ 并发送给 Alice
  - 假设 <span style="color:red">$b=3$</span>，则
    <span style="color:green">$B$</span>$\ = 5^3 \mod 23 = 10$
- Alice 计算 $S_1 = B^a \mod p$
  - $S_1 = 10^4 \mod 23 = 18$
- Bob 计算 $S_2 = A^b \mod p$
  - $S_2 = 4^3 \mod 23 = 18$
- 已知 $B^a \mod p = g^{ab} \mod p = A^b \mod p$，因此
  <span style="color:red">$S_1 = S_2 = S$</span>
- 这样 Alice 跟 Bob 就协商出了密钥 <span style="color:red">$S$</span>
- 因为离散对数的计算非常难，任何窃听者都几乎不可能通过公开的 <span style="color:green">$p$
  $g$ $A$ $B$</span> 逆推出 <span style="color:red">$S$</span> 的值

在最常见的 DHKE 实现中（[RFC3526](https://tools.ietf.org/html/rfc3526)），基数是 $g = 2$，
模数 $p$ 是一个 1536 到 8192 比特的大素数。而整数 <span style="color:green">$A$ $B$</span>
通常会使用非常大的数字（1024、2048 或 4096 比特甚至更大）以防范暴力破解。

DHKE 协议基于 Diffie-Hellman 问题的实际难度，这是计算机科学中众所周知的离散对数问题（DLP）
的变体，目前还不存在有效的算法。

使用 Python 演示下大概是这样：

```python
# pip install cryptography==36.0.1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh

# 1. 双方协商使用两个独特的正整数 g 与 p
## generator => 即基数 g，通常使用 2, 有时也使用 5
## key_size => 模数 p 的长度，通常使用 2048-3072 位（2048 位的安全性正在减弱）
params = dh.generate_parameters(generator=2, key_size=2048)
param_numbers = params.parameter_numbers()
g = param_numbers.g  # => 肯定是 2
p = param_numbers.p  # => 一个 2048 位的整数
print(f"{g=}, {p=}")

# 2. Alice 生成自己的秘密整数 a 与公开整数 A
alice_priv_key = params.generate_private_key()
a = alice_priv_key.private_numbers().x
A = alice_priv_key.private_numbers().public_numbers.y
print(f"{a=}")
print(f"{A=}")

# 3. Bob 生成自己的秘密整数 b 与公开整数 B
bob_priv_key = params.generate_private_key()
b = bob_priv_key.private_numbers().x
B = bob_priv_key.private_numbers().public_numbers.y
print(f"{b=}")
print(f"{B=}")

# 4. Alice 与 Bob 公开交换整数 A 跟 B（即各自的公钥）

# 5. Alice 使用 a B 与 p 计算出共享密钥
## 首先使用 B p g 构造出 bob 的公钥对象（实际上 g 不参与计算）
bob_pub_numbers = dh.DHPublicNumbers(B, param_numbers)
bob_pub_key = bob_pub_numbers.public_key()
## 计算共享密钥
alice_shared_key = alice_priv_key.exchange(bob_pub_key)

# 6. Bob 使用 b A 与 p 计算出共享密钥
## 首先使用 A p g 构造出 alice 的公钥对象（实际上 g 不参与计算）
alice_pub_numbers = dh.DHPublicNumbers(A, param_numbers)
alice_pub_key = alice_pub_numbers.public_key()
## 计算共享密钥
bob_shared_key = bob_priv_key.exchange(alice_pub_key)

# 两者应该完全相等， Alice 与 Bob 完成第一次密钥交换
alice_shared_key == bob_shared_key

# 7. Alice 与 Bob 使用 shared_key 进行对称加密通讯
```

## 四、新一代 ECDH 协议

[Elliptic-Curve Diffie-Hellman (ECDH)](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
是一种匿名密钥协商协议，它允许两方，每方都有一个椭圆曲线公钥-私钥对，它的功能也是让双方在
完全没有对方任何预先信息的条件下通过不安全信道安全地协商出一个安全密钥。

ECDH 是经典 DHKE 协议的变体，其中模幂计算被椭圆曲线的乘法计算取代，以提高安全性。

ECDH 跟前面介绍的 DHKE 非常相似，只要你理解了椭圆曲线的数学原理，结合前面已经介绍了的
DHKE，基本上可以秒懂。我**会在后面「非对称算法」一文中简单介绍椭圆曲线的数学原理**，不过这
里也可以先提一下 ECDH 依赖的公式（其中 $a, b$ 为常数，$G$ 为椭圆曲线上的某一点的坐标
$(x, y)$）：

$$
(a * G) * b = (b * G) * a
$$

这个公式还是挺直观的吧，感觉小学生也能理解个大概。下面简单介绍下 ECDH 的流程：

- Alice 跟 Bob 协商好椭圆曲线的各项参数，以及基点 G，这些参数都是公开的。
- Alice 生成一个随机的 ECC 密钥对（公钥：$alicePrivate * G$, 私钥: $alicePrivate$）
- Bob 生成一个随机的 ECC 密钥对（公钥：$bobPrivate * G$, 私钥: $bobPrivate$）
- 两人通过不安全的信道交换公钥
- Alice 将 Bob 的公钥乘上自己的私钥，得到共享密钥
  $sharedKey = (bobPrivate * G) * alicePrivate$
- Bob 将 Alice 的公钥乘上自己的私钥，得到共享密钥
  $sharedKey = (alicePrivate * G) * bobPrivate$
- 因为前面提到的公式，Alice 与 Bob 计算出的共享密钥应该是相等的

这样两方就通过 ECDH 完成了密钥交换。

而 ECDH 的安全性，则由 ECDLP 问题提供保证。这个问题是说，「通过公开的 $kG$ 以及 $G$ 这两个
参数，目前没有有效的手段能快速求解出 $k$ 的值。」

从上面的流程中能看到，公钥就是 ECDLP 中的 $kG$，另外 $G$ 也是公开的，而私钥就是 ECDLP 中的
$k$。因为 ECDLP 问题的存在，攻击者破解不出 Alice 跟 Bob 的私钥。

代码示例：

```python
# pip install tinyec  # ECC 曲线库
from tinyec import registry
import secrets

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

curve = registry.get_curve('brainpoolP256r1')

alicePrivKey = secrets.randbelow(curve.field.n)
alicePubKey = alicePrivKey * curve.g
print("Alice public key:", compress(alicePubKey))

bobPrivKey = secrets.randbelow(curve.field.n)
bobPubKey = bobPrivKey * curve.g
print("Bob public key:", compress(bobPubKey))

print("Now exchange the public keys (e.g. through Internet)")

aliceSharedKey = alicePrivKey * bobPubKey
print("Alice shared key:", compress(aliceSharedKey))

bobSharedKey = bobPrivKey * alicePubKey
print("Bob shared key:", compress(bobSharedKey))

print("Equal shared keys:", aliceSharedKey == bobSharedKey)
```

## 五、PFS 完美前向保密协议 DHE/ECDHE

前面介绍的经典 DHKE 与 ECDH 协议流程，都是在最开始时交换一次密钥，之后就一直使用该密钥通
讯。因此如果密钥被破解，整个会话的所有信息对攻击者而言就完全透明了。

为了进一步提高安全性，密码学家提出了
「[**完全前向保密**（Perfect Forward Secrecy，PFS）](https://en.wikipedia.org/wiki/Forward_secrecy)」
的概念，并在 DHKE 与 ECDH 的基础上提出了支持 PFS 的 DHE/ECDHE 协议（末尾的 `E` 是
`ephemeral` 的缩写，即指所有的共享密钥都是临时的）。

「完全前向保密 PFS」是指长期使用的主密钥泄漏不会导致过去的会话密钥泄漏，从而保护过去进行的
通讯不受密码或密钥在未来暴露的威胁。

下面使用 Python 演示下 DHE 协议的流程（ECDHE 的流程也完全类似）：

```python
# pip install cryptography==36.0.1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh

# 1. 双方协商使用两个独特的正整数 g 与 p
## generator => 即基数 g，通常使用 2, 有时也使用 5
## key_size => 模数 p 的长度，通常使用 2048-3072 位（2048 位的安全性正在减弱）
params = dh.generate_parameters(generator=2, key_size=2048)
param_numbers = params.parameter_numbers()
g = param_numbers.g  # => 肯定是 2
p = param_numbers.p  # => 一个 2048 位的整数
print(f"{g=}, {p=}")

# 2. Alice 生成自己的秘密整数 a 与公开整数 A
alice_priv_key = params.generate_private_key()
a = alice_priv_key.private_numbers().x
A = alice_priv_key.private_numbers().public_numbers.y
print(f"{a=}")
print(f"{A=}")

# 3. Bob 生成自己的秘密整数 b 与公开整数 B
bob_priv_key = params.generate_private_key()
b = bob_priv_key.private_numbers().x
B = bob_priv_key.private_numbers().public_numbers.y
print(f"{b=}")
print(f"{B=}")

# 4. Alice 与 Bob 公开交换整数 A 跟 B（即各自的公钥）

# 5. Alice 使用 a B 与 p 计算出共享密钥
## 首先使用 B p g 构造出 bob 的公钥对象（实际上 g 不参与计算）
bob_pub_numbers = dh.DHPublicNumbers(B, param_numbers)
bob_pub_key = bob_pub_numbers.public_key()
## 计算共享密钥
alice_shared_key = alice_priv_key.exchange(bob_pub_key)

# 6. Bob 使用 b A 与 p 计算出共享密钥
## 首先使用 A p g 构造出 alice 的公钥对象（实际上 g 不参与计算）
alice_pub_numbers = dh.DHPublicNumbers(A, param_numbers)
alice_pub_key = alice_pub_numbers.public_key()
## 计算共享密钥
bob_shared_key = bob_priv_key.exchange(alice_pub_key)

# 上面的流程跟经典 DHKE 完全一致，代码也是从前面 Copy 下来的
# 但是从这里开始，进入 DHE 协议补充的部分

shared_key_1 = bob_shared_key # 第一个共享密钥

# 7. 假设 Bob 现在要发送消息 M_b_1 给 Alice
## 首先 Bob 使用对称加密算法加密消息 M_b
M_b_1 = "Hello Alice, I'm bob~"
C_b_1 = Encrypt(M_b_1, shared_key_1)  # Encrypt 是某种对称加密方案的加密算法，如 AES-256-CTR-HMAC-SHA-256
## 然后 Bob 需要生成一个新的公私钥 b_2 与 B_2（注意 g 与 p 两个参数是不变的）
bob_priv_key_2 = parameters.generate_private_key()
b_2 = bob_priv_key.private_numbers().x
B_2 = bob_priv_key.private_numbers().public_numbers.y
print(f"{b_2=}")
print(f"{B_2=}")

# 8. Bob 将 C_b_1 与 B_2 一起发送给 Alice

# 9. Alice 首先解密数据 C_b_1 得到原始消息 M_b_1
assert M_b_1 == Decrypt(C_b_1, shared_key_1)  # Dncrypt 是某种对称加密方案的解密算法，如 AES-256-CTR-HMAC-SHA-256
## 然后 Alice 也生成新的公私钥 a_2 与 A_2
alice_priv_key_2 = parameters.generate_private_key()
## Alice 使用 a_2 B_2 与 p 计算出新的共享密钥 shared_key_2
bob_pub_numbers_2 = dh.DHPublicNumbers(B_2, param_numbers)
bob_pub_key_2 = bob_pub_numbers_2.public_key()
shared_key_2 = alice_priv_key_2.exchange(bob_pub_key_2)

# 10. Alice 回复 Bob 消息时，使用新共享密钥 shared_key_2 加密消息得到 C_a_1
# 然后将密文 C_a_1 与 A_2 一起发送给 Bob

# 11. Bob 使用 b_2 A_2 与 p 计算出共享密钥 shared_key_2
# 然后再使用 shared_key_2 解密数据
# Bob 在下次发送消息时，会生成新的 b_3 与 B_3，将 B_3 随密文一起发送

## 依次类推
```

通过上面的代码描述我们应该能理解到，**Alice 与 Bob 每次交换数据，实际上都会生成新的临时共
享密钥**，公钥密钥在每次数据交换时都会更新。即使攻击者花了很大的代价破解了其中某一个临时共
享密钥 **shared_key_k**（或者该密钥因为某种原因泄漏了），TA 也只能解密出其中某一次数据交换
的信息 **M_b_k**，其他所有的消息仍然是保密的，不受此次攻击（或泄漏）的影响。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
