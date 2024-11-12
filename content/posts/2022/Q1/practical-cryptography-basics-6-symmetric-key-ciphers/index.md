---
title: "写给开发人员的实用密码学（六）—— 对称密钥加密算法"
date: 2022-03-06T18:44:00+08:00
draft: false

featuredImage: "symmetric-vs-asymmetric.webp"
resources:
  - name: featured-image
    src: "symmetric-vs-asymmetric.webp"
authors: ["ryan4yin"]

tags: ["Cryptography", "密码学", "对称加密", "安全", "AES", "ChaCha20"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]

seriesNavigation: true

math:
  enable: true
code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 本文主要翻译自 [Practical-Cryptography-for-Developers-Book][cryptobook]，笔者补充了部分
> 代码示例。

## 零、术语介绍

两个常用动词：

- 加密：cipher 或者 encrypt
- 解密：decipher 或者 decrypt

另外有几个名词有必要解释：

- cipher: 指用于加解密的「密码算法」，有时也被直接翻译成「密码」
- cryptographic algorithm: 密码学算法，泛指密码学相关的各类算法
- ciphertext: 密文，即加密后的信息。对应的词是明文 plaintext
- password: 这个应该不需要解释，就是我们日常用的各种字符或者数字密码，也可称作口令，通常都
  比较短（绝大部分用户密码应该都只有 8 - 16 位）。
  - 因为站点太多，密码太难记，现代社会正在逐步推荐使用生物特征（指纹、面部识别等，如 pass
    key、手机指纹识别）或者硬件密钥（U2F）来替代传统的密码。
- [passphrase](https://en.wikipedia.org/wiki/Passphrase): 翻译成「密码词组」，也就是用一个
  个单词组合而成的 Password，特点是长度比较长，而且比随机密码更容易记忆。
  - 如果你用 ssh/gnupg/openssl 等工具生成或使用过密钥，应该对它不陌生，它们的 passphrase
    长度不受限，因此可以使用类似 `you-are-not-my-enemy-but-I'm-your-father` 这样的词组方式
    作为其密码，强度高，而且好记。

在密码学里面，最容易搞混的词估计就是「密码」了，cipher/password/passphrase 都可以被翻译成
「密码」，需要注意下其中区别。

## 一、什么是对称加密

在密码学中，有两种加密方案被广泛使用：「对称加密」与「非对称加密」。

对称加密是指，使用相同的密钥进行消息的加密与解密。因为这个特性，我们也称这个密钥为「共享密
钥（Shared Secret Key）」，示意图如下：

{{< figure src="/images/practical-cryptography-basics-6-symmetric-key-ciphers/symmetric-cryptography.webp" >}}

现代密码学中广泛使用的对称加密算法（ciphers）
有：AES（AES-128、AES-192、AES-256）、ChaCha20、Twofish、IDEA、Serpent、Camelia、RC6、CAST
等。其中绝大多数都是「**块密码算法**（Block Cipher）」或者叫「**分组密码算法**」，这种算法
一次只能加密固定大小的块（例如 128 位）；少部分是「**流密码算法**（Stream Cipher）」，流密
码算法将数据逐字节地加密为密文流。

通过使用称为「分组密码工作模式」的技术，可以将「分组密码算法」转换为「流密码算法」。

### 量子安全性

即使计算机进入量子时代，仍然可以沿用当前的对称密码算法。因为大多数现代对称密钥密码算法都
是**抗量子的**（**quantum-resistant**），这意味当使用长度足够的密钥时，强大的量子计算机无
法破坏其安全性。目前来看 256 位的 AES/Twofish 在很长一段时间内都将是 **量子安全** 的。

## 二、对称加密方案的结构

我们在第一章「概览」里介绍过，单纯使用数据加密算法只能保证数据的**安全性**，并不能满足我们
对消息**真实性、完整性与不可否认性**的需求，因此通常我们会将对称加密算法跟其他算法组合成一
个「**对称加密方案**」来使用，这种多个密码学算法组成的「加密方案」能同时保证数据的安全性、
真实性、完整性与不可否认性。

一个**分组加密方案**通常会包含如下几种算法：

- 将密码转换为密钥的**密钥派生算法 KDF**（如 Scrypt 或 Argon2）：通过使用 KDF，加密方案可
  以允许用户使用字符密码作为「Shared Secret Key」，并使密码的破解变得困难和缓慢
- **分组密码工作模式**（用于将分组密码转换为流密码，如 CBC 或 CTR）+ **消息填充算法**（如
  PKCS7）：分组密码算法（如 AES）需要借助这两种算法，才能加密任意大小的数据
- **分组密码算法**（如 AES）：使用密钥安全地加密固定长度的数据块
  - 大多数流行的对称加密算法，都是分组密码算法
- **消息认证算法**（如HMAC）：用于验证消息的真实性、完整性、不可否认性

而一个**流密码加密方案**本身就能加密任意长度的数据，因此不需要「分组密码模式」与「消息填充
算法」。

如 AES-256-CTR-HMAC-SHA256 就表示一个使用 AES-256 与 Counter 分组模式进行加密，使用
HMAC-SHA256 进行消息认证的加密方案。其他流行的对称加密方案还有 ChaCha20-Poly1305 和
AES-128-GCM 等，其中 ChaCha20-Poly130 是一个流密码加密方案。我们会在后面单独介绍这两种加密
方案。

## 三、分组密码工作模式

前面简单介绍了「[**分组密码工作模式**][Block_cipher_mode_of_operation_wiki]」可以将「分组
密码算法」转换为「流密码算法」，从而实现加密任意长度的数据，这里主要就具体介绍下这个分组密
码工作模式（下文简称为「**分组模式**」或者「**XXX 模式**」）。

加密方案的名称中就带有具体的「分组模式」名称，如：

- **AES-256-GCM** - 具有 256 位加密密钥和 GCM 分组模式的 AES 密码
- **AES-128-CTR** - 具有 128 位加密密钥和 CTR 分组模式的 AES 密码
- **Serpent-128-CBC** - 具有 128 位加密密钥和 CBC 分组模式的 Serpent 密码

「分组密码工作模式」背后的主要思想是把明文分成多个长度固定的组，再在这些分组上重复应用分组
密码算法进行加密/解密，以实现安全地加密/解密任意长度的数据。

某些分组模式（如 CBC）要求将输入拆分为分组，并使用填充算法（例如添加特殊填充字符）将最末尾
的分组填充到块大小。也有些分组模式（如 CTR、CFB、OFB、CCM、EAX 和 GCM）根本不需要填充，因
为它们在每个步骤中，都直接在明文部分和内部密码状态之间执行异或（XOR）运算.

使用「分组模式」加密大量数据的流程基本如下：

- 初始化加密算法状态（使用加密密钥 + 初始向量 IV）
- 加密数据的第一个分组
- 使用加密密钥和其他参数转换加密算法的当前状态
- 加密下一个分组
- 再次转换加密状态
- 再加密下一分组
- 依此类推，直到处理完所有输入数据

解密的流程跟加密完全类似：先初始化算法，然后依次解密所有分组，中间可能会涉及到加密状态的转
换。

下面我们来具体介绍下 CTR 与 GCM 两个常见的分组模式。

### 0. 初始向量 IV

介绍具体的分组模式前，需要先了解下**初始向量 IV**（Initialization Vector）这个概念，它有时
也被称作 Salt 或者 Nonce。初始向量 IV 通常是一个随机数，主要作用是往密文中添加随机性，使同
样的明文被多次加密也会产生不同的密文，从而确保密文的不可预测性。

IV 的大小应与密码块大小相同，例如 AES、Serpent 和 Camellia 都只支持 128 位密码块，那么它们
需要的 IV 也必须也 128 位。

IV 通常无需保密，但是应当足够随机（无法预测），而且不允许重用，应该对每条加密消息使用随机
且不可预测的 IV。

一个常见错误是使用相同的对称密钥和**相同的 IV** 加密多条消息，这使得针对大多数分组模式的各
种加密攻击成为可能。

### 1. CTR (Counter) 分组模式 {#counter_mode}

> 参考文档: https://csrc.nist.gov/publications/detail/sp/800-38a/final

下图说明了「CTR 分组工作模式」的加密解密流程，基本上就是将明文/密文拆分成一个个长度固定的
分组，然后使用一定的算法进行加密与解密：

{{< figure src="/images/practical-cryptography-basics-6-symmetric-key-ciphers/CTR_encryption.svg" >}}

{{< figure src="/images/practical-cryptography-basics-6-symmetric-key-ciphers/CTR_decryption.svg" >}}

可以看到两图中左边的第一个步骤，涉及到三个参数：

- `Nonce`，初始向量 IV 的别名，前面已经介绍过了。
- `Counter`: 一个计数器，最常用的 Counter 实现是「从 0 开始，每次计算都自增 1」
- `Key`: 对称加密的密钥
- `Plaintext`: 明文的一个分组。除了最后一个分组外，其他分组的长度应该跟 `Key` 相同

CTR 模式加解密的算法使用公式来表示如下：

$$
\begin{alignedat}{2}
  C_i &= P_i \oplus O_i, \ &\text{for } i &= 1, 2 ... n-1 \\\\
  P_i &= C_i \oplus O_i, \ &\text{for } i &= 1, 2 ... n-1 \\\\
  O_i &= \text{CIPH}_{key}(\text{Nonce} + I_i), \ &\text{for } i &= 1, 2 ... n-1
\end{alignedat}
$$

公式的符号说明如下

- $C_i$ 表示密文的第 $i$ 个分组
- $P_i$ 表示明文的第 $i$ 个 分组
- $O_i$ 是一个中间量，第三个公式是它的计算方法
- $I_i$ 表示计数器返回的第 $i$ 个值，其长度应与分组的长度相同
- $\text{CIPH}_{key}$ 表示使用密钥 $key$ 的对称加密算法

上面的公式只描述了 $ 0 \ge i \le n-1$ 的场景，最后一个分组 $i = n$ 要特殊一些——它的长度可
能比 `Key` 要短。CTR 模式加解密这最后这个分组时，会直接忽略掉 $O_n$ 末尾多余的 bytes. 这种
处理方式使得 CTR 模式不需要使用填充算法对最后一个分组进行填充，而且还使密文跟明文的长度完
全一致。我们假设最后一个分组的长度为 $u$，它的加解密算法描述如下（$MSB_u(O_n)$ 表示取
$O_n$ 的 u 个最高有效位）：

$$
\begin{alignedat}{2}
  C_{n} &= P_{n} \oplus {MSB_u}(O_n) \\\\
  P_{n} &= C_{n} \oplus {MSB_u}(O_n)\\\\
  O_n &= \text{CIPH}_{key}(\text{Nonce} + I_n)
\end{alignedat}
$$

可以看到，因为异或 XOR 的对称性，加密跟解密的算法是完全相同的，直接 XOR $O_i$ 即可。

Python 中最流行的密码学库是
[cryptography](https://github.com/pyca/cryptography)，`requests` 的底层曾经就使用了它（新
版本已经换成使用标准库 ssl 了），下面我们使用这个库来演示下 AES-256-CTR 算法：

```python
# pip install cryptography==36.0.1
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

plaintext = b"this is a test message, hahahahahaha~"

# 使用 32bytes 的 key，即使用算法 AES-256-CTR
key = os.urandom(32)
# key => b'\x96\xec.\xc7\xd5\x1b/5\xa1\x10s\x9d\xd5\x10z\xdc\x90\xb5\x1cm">x\xfd \xd5\xc5\xaf\x19\xd1Z\xbb'

# AES 算法的 block 大小是固定的 128bits，即 16 bytes, IV 长度需要与 block 一致
iv = os.urandom(16)
# iv => b'\x88[\xc9\n`\xe4\xc2^\xaf\xdc\x1e\xfd.c>='

# 1. 发送方加密数据
## 构建 AES-256-CTR 的 cipher，然后加密数据，得到密文
cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
# ciphertext => b'\x9b6(\x1d\xfd\xde\x96S\x8b\x8f\x90\xc5}ou\x9e\xb1\xbd\x9af\xb8\xdc\xec\xbf\xa3"\x18^\xac\x14\xc8s2*\x1a\xcf\x1d'

# 2. 发送方将 iv + ciphertext 发送给接收方

# 3. 接收方解密数据
# 接收方使用自己的 key + 接收到的 iv，构建 cipher，然后解密出原始数据
cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
decryptor = cipher.decryptor()
decryptor.update(ciphertext) + decryptor.finalize()
```

从上面的算法描述能感觉到，CTR 算法还蛮简单的。下面我使用 Python 写一个能够 work 的 CTR 实
现：

```python
def xor_bytes(a, b):
    """Returns a new byte array with the elements xor'ed.
       if len(a) != len(b), extra parts are discard.
    """
    return bytes(i^j for i, j in zip(a, b))

def inc_bytes(a):
    """ Returns a new byte array with the value increment by 1 """
    out = list(a)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)

def split_blocks(message, block_size, require_padding=True):
    """
    Split `message` with fixed length `block_size`
    """
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def encrypt_ctr(block_cipher, plaintext, iv):
    """
    Encrypts `plaintext` using CTR mode with the given nounce/IV.
    """
    assert len(iv) == 16

    blocks = []
    nonce = iv
    for plaintext_block in split_blocks(plaintext, block_size=16, require_padding=False):
        # CTR mode encrypt: plaintext_block XOR encrypt(nonce)
        o = bytes(block_cipher.encrypt(nonce))
        block = xor_bytes(plaintext_block, o)  # extra parts of `o` are discard in this step
        blocks.append(block)
        nonce = inc_bytes(nonce)

    return b''.join(blocks)

# 加密与解密的算法完全一致
decrypt_ctr = encrypt_ctr
```

接下来验证下算法的正确性：

```python
# Python 官方库未提供 AES 实现，因此需要先装下这个库：
# pip install pyaes==1.6.1
from pyaes import AES

# AES-256-CTR - plaintext key 都与前面的测试代码完全一致
plaintext = b"this is a test message, hahahahahaha~"
key = b'\x96\xec.\xc7\xd5\x1b/5\xa1\x10s\x9d\xd5\x10z\xdc\x90\xb5\x1cm">x\xfd \xd5\xc5\xaf\x19\xd1Z\xbb'

# 1. 发送方加密数据
# 首先生成一个随机 IV，为了对比，这里使用前面生成好的数据
iv = b'\x88[\xc9\n`\xe4\xc2^\xaf\xdc\x1e\xfd.c>='
aes_cipher = AES(key)
ciphertext = encrypt_ctr(aes_cipher, plaintext, iv)
print("ciphertext =>", bytes(ciphertext)) # 输出应该与前面用 cryptography 计算出来的完全一致
# ciphertext => b'\x9b6(\x1d\xfd\xde\x96S\x8b\x8f\x90\xc5}ou\x9e\xb1\xbd\x9af\xb8\xdc\xec\xbf\xa3"\x18^\xac\x14\xc8s2*\x1a\xcf\x1d'

# 2. 发送方将 ciphertext + iv 发送给接收方

# 3. 接收方使用自己的 key 解密数据
aes_cipher = AES(key)
decrypted_bytes = decrypt_ctr(aes_cipher, ciphertext, iv)
print("decrypted_bytes =>", bytes(decrypted_bytes))
# decrypted_bytes => b"this is a test message, hahahahahaha~"
```

### 2. GCM (Galois/Counter) 分组模式

GCM (Galois/Counter) 模式在 CTR 模式的基础上，添加了消息认证的功能，而且同时还具有与 CTR
模式相同的并行计算能力。因此相比 CTR 模式，GCM 不仅速度一样快，还能额外提供对消息完整性、
真实性的验证能力。

下图直观地解释了 GCM 块模式（Galois/Counter 模式）的工作原理：

{{< figure src="/images/practical-cryptography-basics-6-symmetric-key-ciphers/gcm-galois_counter_mode.webp" >}}

GCM 模式新增的 Auth Tag，计算起来会有些复杂，我们就直接略过了，对原理感兴趣的可以看下
[Galois/Counter_Mode_wiki][Galois/Counter_Mode_wiki].

### 3. 如何选用块模式

一些 Tips:

- 常用的安全块模式是 CBC（密码块链接）、CTR（计数器）和 GCM（伽罗瓦/计数器模式），它们需要
  一个随机（不可预测的）初始化向量 (IV)，也称为 `nonce` 或 `salt`
- 「**CTR**（Counter）」块模式在大多数情况下是一个不错的选择，因为它具有很强的安全性和并行
  处理能力，允许任意输入数据长度（无填充）。但它不提供身份验证和完整性，只提供加密
- **GCM**（Galois/Counter Mode）块模式继承了 CTR 模式的所有优点，并增加了加密消息认证能
  力。GCM 是在对称密码中实现认证加密的快速有效的方法，**强烈推荐**
- CBC 模式在固定大小的分组上工作。因此，在将输入数据拆分为分组后，应使用填充算法使最后一个
  分组的长度一致。大多数应用程序使用 **PKCS7** 填充方案或 ANSI X.923. 在某些情况下，CBC 阻
  塞模式可能容易受到「padding oracle」攻击，因此**最好避免使用 CBC 模式**
- 众所周知的不安全块模式是 **ECB**（电子密码本），它将相等的输入块加密为相等的输出块（无加
  密扩散能力）。**不要使用 ECB 块模式**！它可能会危及整个加密方案。
- CBC、CTR 和 GCM 模式等大多数块都支持「随机访问」解密。比如在视频播放器中的任意时间偏移处
  寻找，播放加密的视频流

总之，建议使用 CTR (Counter) 或 GCM (Galois/Counter) 分组模式。其他的分组在某些情况下可能
会有所帮助，但很可能有安全隐患，因此除非你很清楚自己在做什么，否则不要使用其他分组模式！

CTR 和 GCM 加密模式有很多优点：它们是安全的（目前没有已知的重大缺陷），可以加密任意长度的
数据而无需填充，可以并行加密和解密分组（在多核 CPU 中）并可以直接解密任意一个密文分组。因
此它们适用于加密加密钱包、文档和流视频（用户可以按时间查找）。GCM 还提供消息认证，是一般情
况下密码块模式的推荐选择。

请注意，GCM、CTR 和其他分组模式会泄漏原始消息的长度，因为它们生成的密文长度与明文消息的长
度相同。如果您想避免泄露原始明文长度，可以在加密前向明文添加一些随机字节（额外的填充数
据），并在解密后将其删除。

## 四、对称加密算法与对称加密方案

前面啰嗦了这么多，下面进入正题：对称加密算法

### 1. 安全的对称加密算法

目前应用最广泛的对称加密算法，是 AES 跟 Salsa20 / ChaCha20 这两个系列。

#### 1. AES (Rijndael)

> wiki: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard

AES（高级加密标准，也称为 Rijndael）是现代 IT 行业中最流行和广泛使用的对称加密算法。AES 被
证明是高度安全、快速且标准化的，到目前为止没有发现任何明显的弱点或攻击手段，而且几乎在所有
平台上都得到了很好的支持。 AES 是 128 位分组密码，使用 128、192 或 256 位密钥。它通常与分
组模式组合成分组加密方案（如 AES-CTR 或 AES-GCM）以处理流数据。在大多数分组模式中，AES 还
需要一个随机的 128 位初始向量 IV。

Rijndael (AES) 算法可免费用于任何用途，而且非常流行。很多站点都选择 AES 作为 TLS 协议的一
部分，以实现安全通信。现代 CPU 硬件基本都在微处理器级别实现了 AES 指令以加速 AES 加密解密
操作。

这里有一个纯 Python 的 AES 实现可供参考: [AES encryption in pure Python -
boppreh][AES encryption in pure Python - boppreh]

我们在前面的 [CTR 分组模式](#counter_mode)中已经使用 Python 实践了 AES-256-CTR 加密方案。
而实际上更常用的是支持集成身份验证加密（AEAD）的 AES-256-GCM 加密方案，它的优势我们前面已
经介绍过了，这里我们使用 Python 演示下如何使用：

```python
# pip install cryptography==36.0.1
import os
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

def encrypt(key, plaintext, associated_data):
    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (iv, ciphertext, encryptor.tag)

def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()


# 接下来进行算法验证

plaintext = b"this is a paintext, hahahahahaha~"
key = b'\x96\xec.\xc7\xd5\x1b/5\xa1\x10s\x9d\xd5\x10z\xdc\x90\xb5\x1cm">x\xfd \xd5\xc5\xaf\x19\xd1Z\xbb'
associated_data = b"authenticated but not encrypted payload"  # 被用于消息认证的关联数据

# 1. 发送方加密消息
iv, ciphertext, tag = encrypt(
    key,
    plaintext,
    associated_data
)

# 2. 发送方将 associated_data iv ciphertext tag 打包发送给接收方

# 3. 接收方使用自己的 key 验证并解密数据
descrypt_text = decrypt(
    key,
    associated_data,
    iv,
    ciphertext,
    tag
)
```

#### 2. Salsa20 / ChaCha20

> wiki: https://en.wikipedia.org/wiki/Salsa20#ChaCha_variant

Salsa20 及其改进的变体 ChaCha（ChaCha8、ChaCha12、ChaCha20）和 XSalsa20 是由密码学家
Daniel Bernstein 设计的现代、快速的对称流密码家族。 Salsa20 密码是对称流密码设计竞赛
eSTREAM（2004-2008）的决赛选手之一，它随后与相关的 BLAKE 哈希函数一起被广泛采用。 Salsa20
及其变体是免版税的，没有专利。

Salsa20 密码将 128 位或 256 位对称密钥 + 随机生成的 64 位随机数（初始向量）和无限长度的数
据流作为输入，并生成长度相同的加密数据流作为输出输入流。

##### ChaCha20-Poly1305

Salsa20 应用最为广泛的是认证加密方
案：[ChaCha20-Poly1305](https://en.wikipedia.org/wiki/ChaCha20-Poly1305)，即组合使用
ChaCha20 与消息认证算法 Poly1305，它们都由密码学家 Bernstein 设计。

ChaCha20-Poly1305 已被证明足够安全，不过跟 GCM 一样它的安全性也依赖于足够随机的初始向量
IV，另外 ChaCha20-Poly1305 也不容易遭受计时攻击。

在没有硬件加速的情况下，ChaCha20 通常比 AES 要快得多（比如在旧的没有硬件加速的移动设备
上），这是它最大的优势。

以下是一个 ChaCha20 的 Python 示例：

```python
# pip install cryptography==36.0.1
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

plaintext = b"this is a paintext, hahahahahaha~"
key = b'\x96\xec.\xc7\xd5\x1b/5\xa1\x10s\x9d\xd5\x10z\xdc\x90\xb5\x1cm">x\xfd \xd5\xc5\xaf\x19\xd1Z\xbb'
nonce = os.urandom(16)

algorithm = algorithms.ChaCha20(key, nonce)
# ChaCha20 是一个流密码，mode 必须为 None
cipher = Cipher(algorithm, mode=None)

# 1. 加密
encryptor = cipher.encryptor()
ct = encryptor.update(plaintext)

# 2. 解密
decryptor = cipher.decryptor()
decryptor.update(ct)
```

#### 3. 其他流行的对称加密算法

还有一些其他的现代安全对称密码，它们的应用不如 AES 和 ChaCha20 这么广泛，但在程序员和信息
安全社区中仍然很流行：

- [Serpent](<https://en.wikipedia.org/wiki/Serpent_(cipher)>) - 安全对称密钥分组密码（密钥
  大小：128、192 或 256 位），公众所有（Public Domain），完全免费
- [Twofish](https://en.wikipedia.org/wiki/Twofish) - 安全对称密钥分组密码（密钥大
  小：128、192 或 256 位），公众所有（Public Domain），完全免费
- [Camellia](<https://en.wikipedia.org/wiki/Camellia_(cipher)>) - 安全对称密钥分组密码（分
  组大小：128 位；密钥大小：128、192 和 256 位），专利算法，但完全免费
  - 该算法由三菱和日本电信电话（NTT）在 2000 年共同发明
- [RC5](https://en.wikipedia.org/wiki/RC5) - 安全对称密钥分组密码（密钥大小：128 到 2040
  位；分组大小：32、64 或 128 位；轮数：1 ... 255），短密钥不安全（56 位密钥已被暴力破
  解）, 专利在 2015 年到期，现在完全免费
- [RC6](https://en.wikipedia.org/wiki/RC6) - 安全对称密钥分组密码，类似于 RC5，但更复杂
  （密钥大小：128 到 2040 位；分组大小：32、64 或 128 位；轮数：1 ... 255），专利在 2017
  年到期，现在完全免费
- [IDEA](https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm) - 安全对称
  密钥分组密码（密钥大小：128 位），所有专利在均 2012 年前过期，完全免费
- [CAST (CAST-128 / CAST5, CAST-256 / CAST6)](https://en.wikipedia.org/wiki/CAST-256) - 安
  全对称密钥分组密码系列（密钥大小：40 ... 256 位），免版税
- [ARIA](<https://en.wikipedia.org/wiki/ARIA_(cipher)>) - 安全对称密钥分组密码，类似于
  AES（密钥大小：128、192 或 256 位），韩国官方标准，免费供公众使用
- [SM4](<https://en.wikipedia.org/wiki/SM4_(cipher)>) - 安全对称密钥分组密码，类似于
  AES（密钥大小：128 位），中国官方标准，免费供公众使用
  - 由中国国家密码管理局于 2012 年 3 月 21 日发布

具体的算法内容这里就不介绍了，有兴趣或者用得到的时候，可以再去仔细了解。

### 2. 不安全的对称加密算法

如下这些对称加密算法曾经很流行，但现在被认为是不安全的或有争议的安全性，**不建议再使用**：

- DES - 56 位密钥大小，可以被暴力破解
- 3DES（三重 DES, TDES）- 64 位密码，被认为不安全，已在 2017 年被 NIST 弃用.
- RC2 - 64 位密码，被认为不安全
- RC4 - 流密码，已被破解，网上存在大量它的破解资料
- Blowfish - 旧的 64 位密码，已被破坏
  - [Sweet32: Birthday attacks on 64-bit block ciphers in TLS and OpenVPN](https://web.archive.org/web/20161009174028/https://sweet32.info/)
- GHOST - 俄罗斯 64 位分组密码，有争议的安全性，被认为有风险

### 对称认证加密算法 AE / AEAD

我们在前面第三篇文章「MAC 与密钥派生函数 KDF」中介绍过 AE 认证加密及其变体 AEAD.

一些对称加密方案提供集成身份验证加密（AEAD），比如使用了 GCM 分组模式的加密方案 AES-GCM，
而其他加密方案（如 AES-CBC 和 AES-CTR）自身不提供身份验证能力，需要额外添加。

最流行的认证加密（AEAD）方案有如下几个，我们在之前已经简单介绍过它们：

- ChaCha20-Poly1305
  - 具有集成 Poly1305 身份验证器的 ChaCha20 流密码（集成身份验证 AEAD 加密）
  - 使用 256 位密钥和 96 位随机数（初始向量）
  - 极高的性能
  - 在硬件不支持 AES 加速指令时（如路由器、旧手机等硬件上），推荐使用此算法
- AES-256-GCM
  - 我们在前面的 GCM 模式一节，使用 Python 实现并验证了这个 AES-256-GCM 加密方案
  - 使用 256 位密钥和 128 位随机数（初始向量）
  - 较高的性能
  - 在硬件支持 AES 加速时（如桌面、服务器等场景），更推荐使用此算法
- AES-128-GCM
  - 跟 AES-256-GCM 一样，区别在于它使用 128 位密钥，安全性弱于 ChaCha20-Poly1305 与
    AES-256-GCM.
  - 目前被广泛应用在 HTTPS 等多种加密场景下，但是正在慢慢被前面两种方案取代

今天的大多数应用程序应该优先选用上面这些加密方案进行对称加密，而不是自己造轮子。上述方案是
高度安全的、经过验证的、经过良好测试的，并且大多数加密库都已经提供了高效的实现，可以说是开
箱即用。

目前应用最广泛的对称加密方案应该是 AES-128-GCM，而 ChaCha20-Poly1305 因为其极高的性能，也
越来越多地被应用在 TLS1.2、TLS1.3、QUIC/HTTP3、Wireguard、SSH 等协议中。

## 五、AES 算法案例：以太坊钱包加密

在这一小节我们研究一个现实中的 AES 应用场景：以太坊区块链的标准加密钱包文件格式。我们将看
到 AES-128-CTR 密码方案如何与 Scrypt 和 MAC 相结合，通过字符密码安全地实现经过身份验证的对
称密钥加密。

#### 以太坊 UTC / JSON 钱包

在比特币和以太坊等区块链网络中，区块链资产持有者的私钥存储在称为**加密钱包**的特殊密钥库
中。通常，这些加密钱包是本地硬盘上的文件，并使用字符密码加密。

在以太坊区块链中，**加密钱包**以一种特殊的加密格式在内部存储，称为「UTC / JSON 钱包（密钥
库文件）」或「Web3 秘密存储定义」。这是一种加密钱包的文件格式，被广泛应用在 geth 和
Parity（以太坊的主要协议实现）、MyEtherWallet（流行的在线客户端以太坊钱包）、MetaMask（广
泛使用的浏览器内以太坊钱包）、ethers.js 和 Nethereum 库以及许多其他与以太坊相关的技术和工
具中。

以太坊 UTC/JSON 密钥库将加密的私钥、加密数据、加密算法及其参数保存为 JSON 文本文档。

UTC / JSON 钱包的一个示例如下：

```yaml
{
  "version": 3,
  "id": "07a9f767-93c5-4842-9afd-b3b083659f04",
  "address": "aef8cad64d29fcc4ed07629b9e896ebc3160a8d0",
  "Crypto":
    {
      "ciphertext": "99d0e66c67941a08690e48222a58843ef2481e110969325db7ff5284cd3d3093",
      "cipherparams": { "iv": "7d7fabf8dee2e77f0d7e3ff3b965fc23" },
      "cipher": "aes-128-ctr",
      "kdf": "scrypt",
      "kdfparams":
        {
          "dklen": 32,
          "salt": "85ad073989d461c72358ccaea3551f7ecb8e672503cb05c2ee80cfb6b922f4d4",
          "n": 8192,
          "r": 8,
          "p": 1,
        },
      "mac": "06dcf1cc4bffe1616fafe94a2a7087fd79df444756bb17c93af588c3ab02a913",
    },
}
```

上述 json 内容也是认证对称加密的一个典型示例，可以很容易分析出它的一些组成成分：

- `kdf`: 用于从字符密码派生出密钥的 KDF 算法名称，这里用的是 `scrypt`
  - `kdfparams`: KDF 算法的参数，如迭代参数、盐等...
- `ciphertext`: 钱包内容的密文，通常这就是一个被加密的 256 位私钥
- `cipher` + `cipherparams`: 对称加密算法的名称及参数，这里使用了 AES-128-CTR，并给出了初
  始向量 IV
- `mac`: 由 MAC 算法生成的消息认证码，被用于验证解密密码的正确性
  - 以太坊使用截取派生密钥的一部分，拼接上完整密文，然后进行 keccak-256 哈希运算得到 MAC
    值
- 其他钱包相关的信息

默认情况下，密钥派生函数是 scrypt 并使用的是弱 scrypt 参数（n=8192 成本因子，r=8 块大
小，p=1 并行化），因此建议使用长而复杂的密码以避免钱包被暴力解密。

## 参考

- [Practical-Cryptography-for-Developers-Book][cryptobook]
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)
- [AES encryption in pure Python - boppreh][AES encryption in pure Python - boppreh]
- [Block_cipher_mode_of_operation_wiki][Block_cipher_mode_of_operation_wiki]
- [Galois/Counter_Mode_wiki][Galois/Counter_Mode_wiki]

[cryptobook]: https://github.com/nakov/Practical-Cryptography-for-Developers-Book
[Block_cipher_mode_of_operation_wiki]:
  https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[Galois/Counter_Mode_wiki]: https://en.wikipedia.org/wiki/Galois/Counter_Mode
[AES encryption in pure Python - boppreh]:
  https://github.com/boppreh/aes/blob/master/aes.py
