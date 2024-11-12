---
title: "Base64 编码并不唯一"
date: 2020-05-31T00:13:00+08:00
draft: false

featuredImage: "base64-encoding.webp"
resources:
  - name: featured-image
    src: "base64-encoding.webp"
authors: ["ryan4yin"]

tags: ["Base64", "编码"]
categories: ["tech"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 个人笔记，不保证正确

# 问题

我以前只知道 Base64 这个编码算法很常用，自己也经常在 JWT 等场景下使用，但是从来没了解过它
的原理，一直先入为主地认为它的编码应该是唯一的。

但是今天测试 JWT 时，发现修改 JWT 的最后一个字符（其实不是我发现的。。），居然有可能不影响
JWT 的正确性。比如下这个使用 HS256 算法的 JWT:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

把它的最后一个字符改成 `d` `e`或者 `f`，都能成功通过 `http://jwt.io` 的验证。

这让我觉得很奇怪（难道我发现了一个 Bug？），在 QQ 群里一问，就有大佬找到根本原因：**这是
Base64 编码的特性**。并且通过 python 进行了实际演示：

```python
In [1]: import base64

# 使用 jwt 的 signature 进行验证
In [2]: base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c==")
Out[2]: b'I\xf9J\xc7\x04IH\xc7\x8a(]\x90O\x87\xf0\xa4\xc7\x89\x7f~\x8f:N\xb2%V\x9dB\xcb0\xe5'

In [3]: base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5d==")
Out[3]: b'I\xf9J\xc7\x04IH\xc7\x8a(]\x90O\x87\xf0\xa4\xc7\x89\x7f~\x8f:N\xb2%V\x9dB\xcb0\xe5'

In [4]: base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5e==")
Out[4]: b'I\xf9J\xc7\x04IH\xc7\x8a(]\x90O\x87\xf0\xa4\xc7\x89\x7f~\x8f:N\xb2%V\x9dB\xcb0\xe5'

In [5]: base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5f==")
Out[5]: b'I\xf9J\xc7\x04IH\xc7\x8a(]\x90O\x87\xf0\xa4\xc7\x89\x7f~\x8f:N\xb2%V\x9dB\xcb0\xe5'

# 两个等于号之后的任何内容，都会被直接丢弃。这个是实现相关的，有的 base64 处理库对这种情况会报错。
In [6]: base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5f==fdf=df==dfd=fderwe=r")
Out[6]: b'I\xf9J\xc7\x04IH\xc7\x8a(]\x90O\x87\xf0\xa4\xc7\x89\x7f~\x8f:N\xb2%V\x9dB\xcb0\xe5'
```

可以看到有两个现象：

- 将同一个 base64 串的最后一个字母分别改成 `d` `e` `f`，解码出来的内容没有任何变化。
- 在 base64 串末尾 `==` 后面添加了一堆随机字符，对解码出的内容也没有任何影响。

## 原因分析

base64 编码将二进制内容(bytes)从左往右每 6 bits 分为一组，每一组编码为一个可打印字符。
bas64 从 ASCII 字符集中选出了 64 个字符（`=`号除外）进行编码。因为 $2^6=64$，使用 64 个字
符才能保证上述编码的唯一性。

但是被编码的二进制内容(bytes)的 bits 数不一定是 6 的倍数，无法被编码为 6 bits 一组。为了解
决这个问题，就需要在这些二进制内容的末尾填充上 2 或 4 个 bit 位，这样才能使用 base64 进行
编码。

关于这些被填充的 bits，在 RFC4648 中定义了规范行为：全部补 0. 但是这并不是一个强制的行为，
因此实际上你可以随便补，在进行 base64 解析时，被填补的 bits 会被直接忽略掉。

这就导致了上面描述的行为：修改 `JWT` 的最后一个字符(6 bits，其中可能包含 2 或 4 个填充比特
位)可能并不影响被编码的实际内容！

[RFC4648][RFC4648 - base64 定义] 中对这个 bits 填充的描述如下：

```
   3.5.  Canonical Encoding

   The padding step in base 64 and base 32 encoding can, if improperly
   implemented, lead to non-significant alterations of the encoded data.
   For example, if the input is only one octet for a base 64 encoding,
   then all six bits of the first symbol are used, but only the first
   two bits of the next symbol are used.  These pad bits MUST be set to
   zero by conforming encoders, which is described in the descriptions
   on padding below.  If this property do not hold, there is no
   canonical representation of base-encoded data, and multiple base-
   encoded strings can be decoded to the same binary data.  If this
   property (and others discussed in this document) holds, a canonical
   encoding is guaranteed.

   In some environments, the alteration is critical and therefore
   decoders MAY chose to reject an encoding if the pad bits have not
   been set to zero.  The specification referring to this may mandate a
   specific behaviour.
```

它讲到在某些环境下，base64 解析器可能会严格检查被填充的这几个 bits，要求它们全部为 0. 但是
我测试发现，Python 标准库和 `https://jwt.io` 都没有做这样的限制。因此我认为绝大部分环境
下，被填充的 bits 都是会被忽略的。

## 问题一：为什么只需要填充 2 或 4 个 bit 位？

这是看到「填充上 2 或 4 个 bit 位」时的第一想法——如果要补足到 6 的倍数，不应该是要填充 1-5
个 bit 位么？

要解答这个问题，我们得看 base64 的定义。在 [RFC4648][RFC4648 - base64 定义] 的 base64 定义
中，有如下这样一段话：

> The Base 64 encoding is designed to represent arbitrary sequences of **octets** in a
> form that allows the use of both upper- and lowercase letters but that need not be human
> readable.

注意重点：**octets**—— 和 bytes 同义，表示 8 bits 一组的位序列。这表示 **base64 只支持编码
bits 数为 8 的倍数的二进制内容，而 $8x \bmod 6$ 的结果只可能是 0/2/4 三种情况**。

因此只需要填充 2 或 4 个 bit 位。

这样的假设也并没有什么问题，因为现代计算机都是统一使用 8 bits(byte) 为最小的可读单位的。即
使是 c 语言的「位域」也是如此。因为 **Byte(8 bits) 现代 CPU 数据读写操作的基本单位**，学过
汇编的对这个应该都有些印象。

你仔细想想，所有文件的最小计量单位，是不是都是 byte？

## 问题二：为什么用 `python` 测试时可能需要在 JWT signature 的末尾添加多个 `=`，而 JWT 中不需要？

前面已经讲过，base64 的编码步骤是是将字节(byte, 8 bits)序列，从左往右每 6 个 bits 转换成一
个可打印字符。

查阅 [RFC4648][RFC4648 - base64 定义] 第 4 小节中 base64 的定义，能看到它实际上是每次处理
24 bits，因为这是 6 和 8 的最小公倍数，可以刚好用 4 个字符表示。 **在被处理的字节序列的比
特(bits)数不是 24 的整数时，就需要在序列末尾填充 0 使末尾的 bits 数是 6 的倍数(6-bit
groups)**。有可能会出现三种情况：

1. 被处理的字节序列 S 的比特数刚好是 24 的倍数：不需要补比特位，末尾也就不需要加 `=`
1. S 的比特数是 $24x+8$: 末尾需要补 4 个 bits，这样末尾剩余的 bits 才是 6-bit groups，才能
   编码成 base64。然后添加两个 `==` 使编码后的字符数为 4 的倍数。
1. S 的比特数为 $24x+16$：末尾需要添加 2 个 bits 才能编码成 base64。然后添加一个 `=` 使编
   码后的字符数为 4 的倍数。

其实可以看到，添加 `=` 的目的只是为了使编码后的字符数为 4 的倍数而已，**`=` 这个 padding
其实是冗余信息，完全可以去掉**。

在解码完成后，应用程序会自动去除掉末尾这不足 1 byte 的 2 或 4 个填充位。

因此 JWT 就去掉了它以减少传输的数据量。

可以用前面讲到的 JWT signature 进行验证：

```python
In [1]: import base64

In [2]: s = base64.b64decode("SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c==")

# len(s) * 8 得到 bits 数
In [3]: len(s) * 8 % 24
Out[3]: 8
```

可以看到这里的被编码内容比特数为 $24x+8$，所以末尾需要添加两个 `==` 号才符合 RFC4648 的定
义。

## 参考

- [Remove trailing “=” when base64 encoding](https://stackoverflow.com/questions/4492426/remove-trailing-when-base64-encoding)
- [RFC4648 - base64 定义][RFC4648 - base64 定义]
- [Difference between RFC 3548 and RFC 4648](https://stackoverflow.com/questions/37893325/difference-betweeen-rfc-3548-and-rfc-4648)
- [Base64 隐写原理和提取脚本](https://www.jianshu.com/p/f1f4e10ad10e)

[RFC4648 - base64 定义]: https://tools.ietf.org/html/rfc4648
