---
title: "个人数据安全不完全指南"
subtitle: ""
description: ""
date: 2024-01-30T13:48:30+08:00
lastmod: 2024-01-30T13:48:30+08:00
draft: false

resources:
  - name: "featured-image"
    src: "datasecurity.webp"

tags:
  [
    "安全",
    "密码学",
    "Linux",
    "SSH",
    "PGP",
    "密码管理",
    "LUKS",
    "全盘加密",
    "零信任",
    "rclone",
  ]
categories: ["tech"]
series: ["写给开发人员的实用密码学"]
series_weight: 11
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

toc:
  enable: true
math:
  enable: false
license: ""

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

## 零、前言

在接触电脑以来很长的一段时间里，我都没怎么在意自己的数据安全。比如说：

1. 长期使用的同一个没有 pssphrase 保护的 SSH 密钥（RSA 2048 位），为了方便我还把它存到了 onedrive 里，而且在各种需要访问 GitHub/Gitee 或SSH 权限的虚拟机跟 PC 上传来传去。
2. Homelab 跟桌面 PC 都从来没开过全盘加密。
3. 在 2022 年我的 Homelab 去年坏掉了两块国产固态硬盘（阿斯加特跟光威弈 Pro 各一根），都是系统一启动就挂，没法手动磁盘格式化，走售后直接被京东换货了。因为我的数据是明文存储的，这很可能导致我的个人数据泄露...
4. 几个密码在各种站点上重复使用，其中重要账号的随机密码还是我在十多年前用 lastpass 生成的，到处用了这么多年，很难说这些密码有没有泄露（lastpass 近几年爆出的泄漏事故就不少...）
5. GitHub, Google, Jetbrains 等账号的 Backup Code 被我明文存储到了百度云盘，中间发现百度云盘安全性太差又转存到了 OneDrive，但一直是明文存储，从来没加过密。
6. 一些银行账号之类的随机密码，因为担心遗忘，长期被我保存在一份印象笔记的笔记里，也是明文存储，仅做了些简单的内容替换，要猜出真正的密码感觉并不是很难。

现在在 IT 行业工作了几年，从我当下的经验来看，企业后台的管理员如果真有兴趣，查看用户的数据真的是很简单的一件事，至少国内绝大部分公司的用户数据，都不会做非常严格的数据加密与权限管控。
就算真有加密，那也很少是用户级别的，对运维人员或开发人员而言这些数据仍旧与未加密无异。
对系统做比较大的迭代时，把小部分用户数据导入到测试环境进行测试也是挺常见的做法...

总之对我而言，这些安全隐患在过去并不算大问题，毕竟我 GitHub, Google 等账号里也没啥重要数据，银行卡里也没几分钱。

但随着我个人数据的积累与在 GitHub, Google 上的活动越来越多、银行卡里 Money 的增加（狗头），这些数据的价值也越来越大。
比如说如果我的 GitHub 私钥泄漏，仓库被篡改甚至删除，以前我 GitHub 上没啥数据也没啥 stars 当然无所谓，
但现在我已经无法忍受丢失 GitHub 两千多个 stars 的风险了。

在 2022 年的时候因为对区块链的兴趣，顺便学习了一波应用密码学，了解了一些密码学的基础知识，然后年底又经历了几次可能的数据泄漏，这使我意识到我的个人数据安全已经是一个不可忽视的问题。
因此，为了避免 Github 私钥泄漏、区块链钱包助记词泄漏、个人隐私泄漏等可能，我在 2023 年 5 月做了全面强化个人数据安全的决定，并在 0XFFFF 社区发了篇帖子征求意见——[学习并强化个人的数据安全性（持续更新）](https://0xffff.one/d/1528)。

现在大半年过去，我已经在个人数据安全上做了许多工作，目前算是达到了一个比较不错的状态。

我的个人数据安全工作，有两个核心的指导思想：

1. **零信任**：不信任任何云服务提供商、本地硬盘、网络等的可靠性与安全性，因此任何数据的落盘、网络传输都应该加密，任何数据都应该有多个副本。
1. **Serverless**: 尽可能利用已有的各种云服务或 Git 之类的分布式存储工具来存储数据，而不是自己额外搭建一堆各种服务。减轻维护负担。
    1. 实际上我个人最近三四年都没维护过任何个人的公网服务器，这个博客以及去年搭建的 NixOS 文档站全都是用的 Vercel 免费静态站点服务，各种数据也全都优先选用 Git 做存储与版本管理。我 Homelab 算力不错，但主要都是用来做各种测试的，一想到要在里面跑什么服务然后还要确保它不挂就头疼——那不就跟每天上班做的事情一样了么 emmmm

这篇文章记录下我做的相关调研工作、我当前的数据安全方案以及未来可能的改进方向。

## 一、个人数据安全包含哪些部分？

数据安全大概有这些方面：

1. 保障数据不会泄漏——也就是加密。
2. 保障数据不会丢失——也就是备份。

就我个人而言，我的数据安全主要考虑以下几个部分：

1. SSH 密钥管理
2. 各种网站、APP 的账号密码管理
3. 灾难恢复相关的数据存储与管理
    1. 比如说 GitHub, Twitter, Google 等重要账号的二次认证恢复代码、账号数据备份等，日常都不需要用到，但非常重要，建议离线加密存储。
4. 需要在多端访问的重要个人数据
    1. 比如说个人笔记、图片、视频等数据，这些数据具有私密性，但又需要在多端访问。可借助支持将数据加密存储到云端的工具来实现。
6. 个人电脑的数据安全与灾难恢复
    1. 我主要使用 macOS 与 NixOS，因此主要考虑的是这两个系统的数据安全与灾难恢复。

下面就分别就这几个部分展开讨论。

## 二、是否需要使用 YubiKey 等硬件密钥？

硬件密钥的好处是可以防止密钥泄漏，但 YubiKey 在国内无官方购买渠道，而且价格不菲，只买一个 YubiKey 的话还存在丢失的风险。

另一方面其实基于现代密码学算法的软件密钥安全性对我而言是足够的，而且软件密钥的使用更加方便。
或许在未来，我会考虑使用 [canokey-core](https://github.com/canokeys/canokey-core)、[OpenSK](https://github.com/google/OpenSK)、[solokey](https://github.com/solokeys/solo1) 等开源方案 DIY 几个硬件密钥，但目前我并不觉得有这必要。

## 三、SSH 密钥管理

### 2.1 SSH 密钥的生成

我们一般都是直接使用 `ssh-keygen` 命令生成 SSH 密钥对，OpenSSH 目前主要支持两种密钥算法：

1. RSA: 目前你在网上看到的大部分教程都是使用的 RSA 2048 位密钥，但其破解风险在不断提升，目前仅推荐使用 3072 位及以上的 RSA 密钥。
2. ED25519: 这是密码学家 Dan Bernstein 设计的一种新的签名算法，其安全性与 RSA 3072 位密钥相当，但其签名速度更快，且密钥更短，因此目前推荐使用 ED25519 密钥。

### 2.2 SSH 密钥的安全性

RSA 跟 ED25519 都是被广泛使用的密码学算法，其安全性都是经过严格验证的，因此我们可以放心使用。
但为了在密钥泄漏的情况下，能够尽可能减少损失，强烈建议给个人使用的密钥添加 passphrase 保护。

那这个 passphrase 保护到底有多安全呢？

有一些密码学知识的人应该知道，pssphrase 保护的实现原理通常是：通过 KDF 算法将用户输入的 passphrase 字符串转换成一个二进制对称密钥，然后再用这个密钥加解密具体的数据。

因此，使用 pssphrase 加密保护的 SSH Key 的安全性，取决于：

1. passphrase 的复杂度，这对应其长度、字符集、是否包含特殊字符等。这由我们自己控制。
2. 所使用的 KDF 算法的安全性。这由 OpenSSH 的实现决定。

那么，OpenSSH 的 passphrase 是如何实现的？是否足够安全？

我首先 Google 了下，找到一些相关的文章：

- [(2018)The default OpenSSH key encryption is worse than plaintext](https://news.ycombinator.com/item?id=17682946): The default SSH RSA key format uses straight MD5 to derive the AES key used to encrypt your RSA private key, which means it's lightning fast to crack
- [(2021)Password security of encrypted SSH private key: How to read round number or costfactor of bcrypt](https://serverfault.com/questions/1056814/password-security-of-encrypted-ssh-private-key-how-to-read-round-number-or-cost)

在 [OpenSSH release notes](https://www.openssh.com/releasenotes.html) 中搜索 passphrase 跟 kdf 两个关键字，找到些关键信息如下：

```
OpenSSH 9.4/9.4p1 (2023-08-10)

 * ssh-keygen(1): increase the default work factor (rounds) for the
   bcrypt KDF used to derive symmetric encryption keys for passphrase
   protected key files by 50%.

----------------------------------

OpenSSH 6.5/6.5p1 (2014-01-30)

 * Add a new private key format that uses a bcrypt KDF to better
   protect keys at rest. This format is used unconditionally for
   Ed25519 keys, but may be requested when generating or saving
   existing keys of other types via the -o ssh-keygen(1) option.
   We intend to make the new format the default in the near future.
   Details of the new format are in the PROTOCOL.key file.
```

所以从 2014 年发布的 OpenSSH 6.5 开始，ed25519 密钥的 passphrase 才是使用 bcrypt KDF 生成的。
而对于其他类型的密钥，仍旧长期使用基于 MD5 hash 的密钥格式，没啥安全性可言。

即使 2023-08-10 发布的 9.4 版本增加了默认的 bcrypt KDF rounds 次数，它的安全性仍然很值得怀疑。
bcrypt 本身的安全性就越来越差，现代化的加密工具基本都已经升级到了 scrypt 甚至 argon2.
因此要想提升安全性，最好是能更换更现代的 KDF 算法，或者至少增加 bcrypt KDF 的 rounds 数量。

我进一步看了 `man ssh-keygen` 的文档，没找到任何修改 KDF 算法的参数，不过能通过 `-a` 参数来修改 KDF 的 rounds 数量，
OpeSSh 9.4 的 man 信息中写了默认使用 16 rounds.

考虑到大部分人都使用默认参数生成 Key，而且绝大部分用户都没有密码学基础，大概率不知道 KDF、Rounds 是什么意思，我们再了解下 `ssh-keygen` 默认参数。
在 relase note 中我进一步找到这个：

```
OpenSSH 9.5/9.5p1 (2023-10-04)

Potentially incompatible changes
--------------------------------

 * ssh-keygen(1): generate Ed25519 keys by default. Ed25519 public keys
   are very convenient due to their small size. Ed25519 keys are
   specified in RFC 8709 and OpenSSH has supported them since version 6.5
   (January 2014).
```

也就是说从 2023-10-04 发布的 9.5 开始，OpenSSH 才默认使用 ED25519。

结合上面的分析可以推断出，目前绝大部分用户都是使用的 RSA 密钥，且其 passphrase 的安全性很差，不加 passphrase 就是裸奔，加了也很容易被破解。
如果你使用的也这种比较老的密钥类型，那千万别觉得自己加了 passphrase 保护就很安全，这完全是错觉（

即使是使用最新的 ssh-keygen 生成的 ED25519 密钥，其默认也是用的 bcrypt 16 rounds 生成加密密钥，其安全性在我看来也是不够的。

总结下，在不考虑其他硬件密钥/SSH CA 的情况下，最佳的 SSH Key 生成方式应该是：

```bash
ssh-keygen -t ed25519 -a 256 -C "xxx@xxx"
```

rounds 的值根据你本地的 CPU 性能来定，我在 Macbook Pro M2 上测了下，
64 rounds 大概是 0.5s，128 rounds 大概需要 1s，256 rounds 大概 2s，用时与 rounds 值是线性关系。

考虑到我的个人电脑性能都还挺不错，而且只需要在每次重启电脑后通过 `ssh-add ~/.ssh/xxx` 解锁一次，后续就一直使用内存中的密钥了，一两秒的时间还是可以接受的，因此我将当前使用的所有 SSH Key 都使用上述参数重新生成了一遍。

### 2.3 SSH 密钥的分类管理

在所有机器上使用同一个 SSH 密钥，这是我过去的做法，但这样做有几个问题：

1. 一旦某台机器的密钥泄漏，那么就需要重新生成并替换所有机器上的密钥，这很麻烦。
1. 密钥需要通过各种方式传输到各个机器上，这也存在泄漏的风险。

因此，我现在的做法是：

1. 对所有桌面电脑跟笔记本，都在其本地生成一个专用的 SSH 密钥配置到 GitHub 跟常用的服务器上。这个 SSH 私钥永远不会离开这台机器。
2. 对于一些相对不重要的 Homelab 服务器，额外生成一个专用的 SSH 密钥，配置到这些服务器上。在一些跳板机跟测试机上会配置这个密钥方便测试与登录到其他机器。
3. 上述所有 SSH 密钥都添加了 passphrase 保护，且使用了 bcrypt 256 rounds.

我通过这种方式缩小了风险范围，即使某台机器的密钥泄漏，也只需要重新生成并替换这台机器上的密钥即可。

### 2.4 SSH CA - 更安全合理的 SSH 密钥管理方案？

搜到些资料：

- [SSH 证书登录教程](https://www.ruanyifeng.com/blog/2020/07/ssh-certificate.html)

TODO 待研究。

## 四、个人的账号密码管理

我曾经大量使用了 Chrome/Firefox 自带的密码存储功能，但用到现在其实也发现了它们的许多弊端。
有同事推崇 1Password 的使用体验，它的自动填充跟同站点的多密码管理确实做得非常优秀，但一是要收费，二是它是商业的在线方案，我不太喜欢。

作为开源爱好者，我最近找到了一个非常适合我自己的方案：[**password-store**](https://www.passwordstore.org/)

这套方案使用 gpg 加密账号密码，每个文件就是一个账号密码，通过文件树来组织与匹配账号密码与 APP/站点的对应关系，并且生态完善，对 firefox/chrome/android/ios 的支持都挺好。

缺点是用 GPG 加密，上手有点难度，但对咱来说完全可以接受。

我在最近使用 pass-import 从 firefox/chrome 中导入了我当前所有的账号密码，并对所有的重要账号密码进行了一次全面的更新，一共改了二三十个账号，全部采用了随机密码。

当前的存储同步与多端使用方式：

1. pass 的加密数据使用 GitHub 私有仓库存储，pass 原生支持基于 Git 的存储方案。
   1. 因为数据全都是使用 ECC Curve 25519 GPG 加密的，即使仓库内容泄漏，数据的安全性仍然有保障。
1. 在安卓与电脑浏览器中，分别使用这些客户端来读写 pass 中的密码：
1. Android: <https://github.com/android-password-store/Android-Password-Store>
1. Brosers(Chrome/Firefox): <https://github.com/browserpass/browserpass-extension>

其他相关资料：

- [awesome-password-store](https://github.com/tijn/awesome-password-store)
- <https://github.com/gopasspw/gopass>: reimplement in go, with more features.

### 3.1 pass 使用的 GPG 够安全么？

GnuPG 是一个很有历史，而且使用广泛的加密工具，但它的安全性如何呢？

我找到些相关文档：

- [2021年，用更现代的方法使用PGP（上）][2021年，用更现代的方法使用PGP（上）]
- [Predictable, Passphrase-Derived PGP Keys][Predictable, Passphrase-Derived PGP Keys]
- [OpenPGP - The almost perfect key pair][OpenPGP - The almost perfect key pair]

简单总结下，GnuPG 的每个 secret key 都是随机生成的，互相之间没有关联（即不像区块链钱包那样具有确定性）。
生成出的 key 被使用 passphrase 加密保存，每次使用时都需要输入 passphrase 解密。

那么还是之前在调研 OpenSSH 时我们提到的问题：它使用的 KDF 算法与参数是否足够安全？

OpenPGP 标准定义了 [String-to-Key (S2K)](https://datatracker.ietf.org/doc/html/rfc4880#section-3.7)
算法用于从 passphrase 生成对称加密密钥，GnuPG 遵循该规范，并且提供了相关的参数配置选项，
相关参数的文档 [OpenPGP protocol specific options](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Options.html#OpenPGP-Options) 内容如下：

```
--s2k-cipher-algo name

    Use name as the cipher algorithm for symmetric encryption with a passphrase if --personal-cipher-preferences and --cipher-algo are not given. The default is AES-128.
--s2k-digest-algo name

    Use name as the digest algorithm used to mangle the passphrases for symmetric encryption. The default is SHA-1.
--s2k-mode n

    Selects how passphrases for symmetric encryption are mangled. If n is 0 a plain passphrase (which is in general not recommended) will be used, a 1 adds a salt (which should not be used) to the passphrase and a 3 (the default) iterates the whole process a number of times (see --s2k-count).
--s2k-count n

    Specify how many times the passphrases mangling for symmetric encryption is repeated. This value may range between 1024 and 65011712 inclusive. The default is inquired from gpg-agent. Note that not all values in the 1024-65011712 range are legal and if an illegal value is selected, GnuPG will round up to the nearest legal value. This option is only meaningful if --s2k-mode is set to the default of 3.
```

默认还使用的是 AES-128 跟 SHA-1，这俩都已经不太安全了，尤其是 SHA-1，已经被证明存在安全问题。
因此，使用默认参数生成的 GPG 密钥，其安全性是不够的。

为了获得最佳安全性，我们需要：

1. 使用如下参数生成 GPG 密钥：

```
gpg --s2k-mode 3 --s2k-count 65011712 --s2k-digest-algo SHA512 --s2k-cipher-algo AES256 ...
```

2. 加密、签名、认证都使用不同的密钥，每个密钥只用于特定的场景，这样即使某个密钥泄漏，也不会影响其他场景的安全性。

为了在全局使用这些参数，可以将它们添加到你的 `~/.gnupg/gpg.conf` 配置文件中。

详见我的 gpg 配置 [ryan4yin/nix-config/gpg](https://github.com/ryan4yin/nix-config/tree/90cd503/home/base/desktop/gpg)

## 五、跨平台的加密备份同步工具的选择

我日常同时在使用 macOS 与 NixOS，因此不论是需要离线存储的灾难恢复数据，还是需要在多端访问的个人数据，都需要一个跨平台的加密备份与同步工具。

前面提到的 pass 使用 GnuPG 进行文件级别的加密，但在很多场景下这不太适用，而且 GPG 本身也太重了，还一堆历史遗留问题，我不太喜欢。

为了其他数据备份与同步的需要，我需要一个跨平台的加密工具，目前调研到有如下这些：

1. 文件级别的加密
   1. 这个有很多现成的工具，比如 **age**/gpg/**sops**, 都挺不错，但是文件级别的加密用起来繁琐一些，需要手动加解密。大量文件的情况下可能还得先打包成 tarball 再加密，解密后再解包，比较麻烦。
2. 全盘加密，或者支持通过 FUSE 模拟文件系统
   1. 首先 LUKS 就不用考虑了，它基本只在 Linux 上能用。
   1. 跨平台且比较活跃的项目中，我找到了 **rclone** 与 **restic** 这两个项目，都支持云同步，各有优缺点。
   1. restic 相对 rclone 的优势，主要是天然支持增量 snapshots 的功能，可以保存备份的历史快照，并设置灵活的历史快照保存策略。这对可能有回滚需求的数据而言是很重要的。比如说 PVE 虚拟机快照的备份，有了 restic 我们就不再需要依赖 PVE 自身孱弱的快照保留功能，全交给 restic 实现就行。
3. 多端加密同步
   1. 上面提到的 rclone 与 restic 都支持各种云存储，因此都是不错的多端加密同步工具。
   2. 最流行的开源数据同步工具貌似是 synthing，但它对加密的支持还不够完善，暂不考虑。

进一步调研后，我选择了 **age**, **rclone** 与 **restic** 作为我的跨平台加密备份与同步工具。
这三个工具都比较活跃，stars 很高，使用的也都是比较现代的密码学算法：

1. [age](https://age-encryption.org/v1): 对于对称加密的场景，使用 ChaCha20-Poly1305 AEAD 加密方案，对称加密密钥使用 scrypt KDF 算法生成。
2. [rclone](https://rclone.org/crypt/): 使用基于 XSalsa20-Poly1305 的 AEAD 加密方案，key 通过 scrypt KDF 算法生成，并且默认会加盐。
3. [restic](https://restic.readthedocs.io/en/stable/100_references.html#keys-encryption-and-mac): 使用 AES-256-CTR 加密，使用 Poly1305-AES 认证数据，key 通过 scrypt KDF 算法生成。

对于 Nix 相关的 secrets 配置，我使用了 age 的一个适配库 agenix 完成其自动加解密配置，并将相关的加密数据保存在我的 GitHub 私有仓库中。
详见 [ryan4yin/nix-config/secrets](https://github.com/ryan4yin/nix-config/tree/27f1d54/secrets).
关于这个仓库的详细加解密方法，在后面第八节「桌面电脑的数据安全」中会介绍。

## 六、灾难恢复相关的数据存储与管理

相关数据包括：GitHub, Twitter, Google 等重要账号的二次认证恢复代码、账号数据备份、PGP 主密钥与吊销证书等等。

这些数据日常都不需要用到，但在账号或两步验证设备丢失时就非要使用到其中的数据才能找回账号或吊销某个证书，是非常重要的数据。

我目前的策略是：使用 rclone + 1024bits 随机密码加密存储到两个 U 盘中（双副本），放在不同的地方，并且每隔半年到一年检查一遍数据。

对应的 rclone 解密配置本身也设置了比较强的 passphrase 保护，并通过我的 secrets 私有 Git 仓库多端加密同步。

## 七、需要在多端访问的重要个人数据

相关数据包括：个人笔记、重要的照片、录音、视频、等等。

因为日常就需要在多端访问，因此显然不能离线存储。

我的方案如下：

1. 个人笔记：使用 [GitJournal](https://github.com/GitJournal/GitJournal) APP，将笔记存储在 GitHub 私有仓库中，并通过该仓库做多端同步。
1. 遗憾的是目前在 Android 平台上并未找到很合适的基于 Git 的加密笔记 APP，GitJournal 本身也不支持加密，因此我的个人笔记目前是明文存储的。
1. 照片、视频等其他个人数据
1. Homelab 中的 Windows-NAS-Server，两个 4TB 的硬盘，通过 SMB 局域网共享，公网所有客户端（包括移动端）都能通过 tailscale + rclone 流畅访问。
1. 部分重要的数据再通过 rclone 加密备份一份到云端，可选项有：
    - [青云对象存储](https://www.qingcloud.com/products/objectstorage/) 与 [七牛云对象存储 Kodo](https://www.qiniu.com/prices/kodo)，它们都有每月 10GB 的免费存储空间，以及 1GB-10GB 的免费外网流量。
    - [阿里云 OSS](https://help.aliyun.com/zh/oss/product-overview/billing-overview) 也能免费存 5GB 数据以及每月 5GB 的外网流量，可以考虑使用。

## 八、桌面电脑的数据安全

我主要使用两个操作系统：macOS 与 NixOS.
另外 Windows 虽然也有使用，但基本没啥个人数据，可以忽略。

对于 NixOS，我当前的方案如下：

- 桌面主机启用 LUKS2 全盘加密 + Secure Boot，在系统启动阶段需要输入 passphrase 解密 NixOS 系统盘才能正常进入系统。
  - LUKS2 的 passphrase 为一个比较长的密码学随机字符串，包含了特殊字符、数字、大小写字母。
  - LUKS2 的所有安全设置全拉到能接受的最高（比较重要的是 `--iter-time`，计算出 unlock key 的用时，默认 2s，安全起见咱设置成了 5s）
    ```
    cryptsetup --type luks2 --cipher aes-xts-plain64 --hash sha512 --iter-time 5000 --key-size 256 --pbkdf argon2id --use-urandom --verify-passphrase luksFormat device
    ```
  - LUKS2 使用的 argon2id 是比 scrypt 更强的 KDF 算法，其安全性是足够的。
- 重要的通用 secrets，都加密保存在我的 secrets 私有仓库中，在部署我的 nix-config 时使用主机本地的 SSH 系统私钥自动解密。
  - 也就是说要在一台新电脑上成功部署我的 nix-config 配置，需要的准备流程：
    - 本地生成一个新的 ssh key，将公钥配置到 GitHub，并 `ssh-add` 这个新的私钥，使其能够访问到我的私有 secrets 仓库。
    - 将新主机的系统公钥 `/etc/ssh/ssh_host_ed25519_key.pub` 发送到一台旧的可解密 secrets 仓库数据的主机上。如果该文件不存在则先用 `sudo ssh-keygen -A` 生成。
    - 在旧主机上，将收到的新主机公钥添加到 secrets 仓库的 secrets.nix 配置文件中，并使用 agenix 命令 rekey 所有 secrets 数据，然后 commit & push。
    - 现在新主机就能够通过 `nixos-rebuild switch` 或 `darwin-rebuild switch` 成功部署我的 nix-config 了，agenix 会自动使用新主机的系统私钥 `/etc/ssh/ssh_host_ed25519_key` 解密 secrets 仓库中的数据并完成部署工作。
  - 这份 secrets 配置在 macOS 跟 NixOS 上通用，也与 CPU 架构无关，agenix 在这两个系统上都能正常工作。

对于 macOS，它本身的磁盘安全我感觉就已经做得很 OK 了，而且它能改的东西也比较有限。我的安全设置如下：

- 启用 macOS 的全盘加密功能
- 常用的 secrets 的部署与使用方式，与前面 NixOS 的描述完全一致

此外还有我 Homelab 的一些服务器、虚拟机，为了方便在所有主机上 ssh 登录，都统一使用了一个 Homelab 专用私钥，保存在我的 secrets 仓库中，在部署我的 nix-config 时，agenix 会将其解密出来并存放到特定位置。
我的 `~/.ssh/config` 会指定使用该固定位置的密钥登录 Homelab 主机。

## 九、总结下我的数据存在了哪些地方

1. secrets 私有仓库: 它会被我的 nix-config 自动拉取并部署到所有主力电脑上，包含了 homelab ssh key, GPG subkey, 以及其他一些重要的 secrets.
   1. 它通过我所有桌面电脑的 `/etc/ssh/ssh_host_ed25519_key` 公钥加密，在部署时自动使用对应的私钥解密。
   1. 此外该仓库还添加了一个灾难恢复用的公钥，确保在我所有桌面电脑都丢失的极端情况下，仍可通过对应的灾难恢复私钥解密此仓库的数据。该私钥在使用 age 加密后（注：未使用 rclone 加密），与我其他的灾难恢复数据保存在一起。
2. password-store: 我的私人账号密码存储库，通过 pass 命令行工具管理，使用 GPG 加密，GPG 密钥备份被加密保存在上述 secrets 仓库中。
3. rclone 加密的备份 U 盘（双副本）：离线保存一些重要的数据。其配置文件被加密保存在 secrets 仓库中，其配置文件的解密密码被加密保存在 password-store 仓库中。

整套方案都可使用我的 Nix 配置进行自动化部署，整个流程自动化程度很高，所以这套方案带来 的额外负担其实并不大。自动化部署，整个流程自动化程度很高，所以实施这套方案并未给我带来许多额外负担。

secrets 这个私有仓库是整个方案的核心，它包含了所有重要数据（password-store/rclone）的解密密钥。
如果它丢失了，那么所有的数据都无法解密。

但好在 Git 仓库本身是分布式的，我所有的桌面电脑上都有对应的完整备份，我的灾难恢复存储中也会定期备份一份 secrets/password-store 两个仓库的数据过去以避免丢失。

另外需要注意的是，为了避免循环依赖，secrets 与 password-store 这两个仓库的备份不应该使用 rclone 再次加密，而是直接使用 age 对称加密。
这样只要我还记得 age 的解密密码、gpg 密钥的 passphrase 等少数几个密码，就能顺着整条链路解密出所有的数据。

## 十、这套方案下需要记忆几个密码？

绝大部分密码都通过 pass 加密保存与多端同步了，不需要额外记忆。
再通过一些合理的密码复用手段，可以将需要记忆的密码数量降到 3 - 5 个，并且确保日常都会输入，避免遗忘。

此外为了方便记忆，可以专门编些小故事来记忆它们，hint 中也能加上故事中的一些关键字。
毕竟人类擅长记忆故事，但不擅长记忆随机字符。

## 十一、为了落地这套方案，我做了哪些工作？

前面以及基本都提到了，这里再总结下：

1. 重新生成了所有的 SSH Key，增强了 passphrase 强度，bcrypt rounds 增加到 256，通过 `ssh-add` 使用，只需要在系统启动后输入一次密码即可，也不麻烦。
2. 重新生成了所有的 PGP Key，主密钥离线加密存储，本地只保留了加密、签名、认证三个 PGP 子密钥。
3. 重新生成了所有重要账号的密码，全部使用随机密码，一共改了二三十个账号。考虑到旧的 backup code 可能已经泄漏，我也重新生成了所有重要账号的 backup code.
4. 重装 NixOS，使用 LUKS2 做全盘加密，启用 Secure Boot.
5. 注销印象笔记账号，使用 evernote-backup 跟 evernote2md 两个工具将个人的私密笔记迁移到了一个私有 Git 仓库，用 GitJournal APP 在手机上查看编辑笔记，电脑端则是用 Emacs/Neovim。用了三四天挺顺手的。
6. 比较有价值的 GitHub 仓库，都设置了禁止 force push 主分支，并且添加了 github action 自动同步到国内 Gitee.
7. 针对 Homelab 的虚拟机快照备份，从我旧的基于 rclone + crontab 的明文备份方案，切换到了基于 restic 的加密备份方案。

## 十二、灾难恢复预案

这里考虑我的 GPG 子密钥泄漏了、pass 密码仓库泄漏了等各种情况下的灾难恢复流程。

TODO 后续再慢慢补充。

## 十三、未来可能的改进方向

目前我的主要个人数据基本都已经通过上述方案进行了安全管理。
但还有这些方面可以进一步改进：

- 我的 Homelab 目前仍未考虑安全性，需要做安全改造，考虑使用 All in NixOS 的声明式配置管理方案。将 Homelab 中对我而言偏黑盒且可复现性差的 Ubuntu、Kubernetes 集群节点、OpenWRT 等 VM （乃至底层的 Proxmox VE）全面替换成更白盒且可复现性强的 NixOS，提升我对内网环境的掌控度，进而提升内网安全性。这是一个长期计划，没有明确的时间线，不过希望能在 2024 年完成这个工作。
- 手机端的照片视频虽然已经在上面设计好了备份同步方案，但仍未实施。考虑使用 roundsync 加密备份到云端，实现多端访问。
- 进一步学习下 appamor, bubblewrap 等 Linux 下的安全限制方案，尝试应用在我的 NixOS PC 上。
- 2FA: 目前是在我的手机与平板上分别导入了我所有的 2FA 信息。使用的是 Microsoft Authenticator，考虑替换成开源方案并研究备份方法。
- Git 提交是否可以使用 GnuPG 签名，目前没这么做主要是觉得 PGP 这个东西太重了，目前我也只在 pass 上用了它，而且还在研究用 age 取代它。

安全总是相对的，而且其中涉及的知识点不少，我 2022 年学了密码学算是为此打下了个不错的基础，但目前看前头还有挺多知识点在等待着我。
目前仍然打算以比较 casual 的心态去推进这件事情，什么时候有兴趣就推进一点点。

这套方案也可能存在一些问题，欢迎大家审阅指正。

[2021年，用更现代的方法使用PGP（上）]: https://ulyc.github.io/2021/01/13/2021%E5%B9%B4-%E7%94%A8%E6%9B%B4%E7%8E%B0%E4%BB%A3%E7%9A%84%E6%96%B9%E6%B3%95%E4%BD%BF%E7%94%A8PGP-%E4%B8%8A/
[Predictable, Passphrase-Derived PGP Keys]: https://nullprogram.com/blog/2019/07/10/
[OpenPGP - The almost perfect key pair]: https://blog.eleven-labs.com/en/openpgp-almost-perfect-key-pair-part-1/