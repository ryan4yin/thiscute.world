---
title: "个人数据安全不完全指南"
subtitle: ""
description: ""
date: 2024-01-30T13:48:30+08:00
lastmod: 2024-02-20T11:39:30+08:00
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

1. 长期使用一个没有 passphrase 保护的 SSH 密钥（RSA 2048 位），为了方便我还把它存到了
   onedrive 里，而且在各种需要访问 GitHub/Gitee 或 SSH 权限的虚拟机跟 PC 上传来传去。
2. Homelab 跟桌面 PC 都从来没开过全盘加密。
3. 在 2022 年我的 Homelab 坏掉了两块国产固态硬盘（阿斯加特跟光威弈 Pro 各一根），都是系统
   一启动就挂，没法手动磁盘格式化，走售后直接被京东换货了。因为我的数据是明文存储的，这很
   可能导致我的个人数据泄露...
4. 几个密码在各种站点上重复使用，其中重要账号的随机密码还是我在十多年前用 lastpass 生成
   的，到处用了这么多年，很难说这些密码有没有泄露（lastpass 近几年爆出的泄漏事故就不
   少...）
5. GitHub, Google, Jetbrains 等账号的 Backup Code 被我明文存储到了百度云盘，中间发现百度云
   盘安全性太差又转存到了 OneDrive，但一直是明文存储，从来没加过密。
6. 一些银行账号之类的随机密码，因为担心遗忘，长期被我保存在一份印象笔记的笔记里，也是明文
   存储，仅做了些简单的内容替换，要猜出真正的密码感觉并不是很难。
7. 以前也有过因为对 Git 操作不熟悉或者粗心大意，在公开仓库中提交了一些包含敏感信息的
   commit，比如说 SSH 密钥、密码等等，有的甚至很长时间都没发现。

现在在 IT 行业工作了几年，从我当下的经验来看，企业后台的管理员如果真有兴趣，查看用户的数据
真的是很简单的一件事，至少国内大部分公司的用户数据，都不会做非常严格的数据加密与权限管控。
就算真有加密，那也很少是用户级别的，对运维人员或开发人员而言这些数据仍旧与未加密无异。对系
统做比较大的迭代时，把小部分用户数据导入到测试环境进行测试也是挺常见的做法...

总之对我而言，这些安全隐患在过去并不算大问题，毕竟我 GitHub, Google 等账号里也没啥重要数
据，银行卡里也没几分钱。

但随着我个人数据的积累与在 GitHub, Google 上的活动越来越多、银行卡里 Money 的增加（狗
头），这些数据的价值也越来越大。比如说如果我的 GitHub 私钥泄漏，仓库被篡改甚至删除，以前我
GitHub 上没啥数据也没啥 stars 当然无所谓，但现在我已经无法忍受丢失 GitHub 两千多个 stars
的风险了。

在 2022 年的时候我因为对区块链的兴趣顺便学习了一点应用密码学，了解了一些密码学的基础知识，
然后年底又经历了几次可能的数据泄漏，这使我意识到我的个人数据安全已经是一个不可忽视的问题。
因此，为了避免 Github 私钥泄漏、区块链钱包助记词泄漏、个人隐私泄漏等可能，我在 2023 年 5
月做了全面强化个人数据安全的决定，并在 0XFFFF 社区发了篇帖子征求意
见——[学习并强化个人的数据安全性（持续更新）](https://0xffff.one/d/1528)。

现在大半年过去，我已经在个人数据安全上做了许多工作，目前算是达到了一个比较不错的状态。

我的个人数据安全方案，有两个核心的指导思想：

1. **零信任**：不信任任何云服务提供商、本地硬盘、网络等的可靠性与安全性，因此任何数据的落
   盘、网络传输都应该加密，任何数据都应该有多个副本（本地与云端）。
   1. 基于这一点，应该尽可能使用经过广泛验证的开源工具，因为开源工具的安全性更容易被验证，
      也避免被供应商绑架。
1. **Serverless**: 尽可能利用已有的各种云服务或 Git 之类的分布式存储工具来存储数据、管理数
   据版本。
   1. 实际上我个人最近三四年都没维护过任何个人的公网服务器，这个博客以及去年搭建的 NixOS
      文档站全都是用的 Vercel 免费静态站点服务，各种数据也全都优先选用 Git 做存储与版本管
      理。
   1. 我 Homelab 算力不错，但每次往其中添加一个服务前，我都会考虑下这是否有必要，是否能使
      用已有的工具完成这些工作。毕竟跑的服务越多，维护成本越高，安全隐患也越多。

这篇文章记录下我所做的相关调研工作、我在这大半年的实践过程中逐渐摸索出的个人数据安全方案以
及未来可能的改进方向。

注意这里介绍的并不是什么能一蹴而就获得超高安全性的傻瓜式方案，它需要你需要你有一定的技术背
景跟时间投入，是一个长期的学习、实践与方案迭代的过程。另外如果你错误地使用了本文中介绍的工
具或方案，可能反而会降低你的数据安全性，由此产生的任何损失与风险皆由你自己承担。

## 一、个人数据安全包含哪些部分？

数据安全大概有这些方面：

1. 保障数据不会泄漏——也就是加密
2. 保障数据不会丢失——也就是备份

就我个人而言，我的数据安全主要考虑以下几个部分：

1. SSH 密钥管理
2. 各种网站、APP 的账号密码管理
3. 灾难恢复相关的数据存储与管理
   1. 比如说 GitHub, Twitter, Google 等重要账号的二次认证恢复代码、账号数据备份等，日常都
      不需要用到，但非常重要，建议离线加密存储
4. 需要在多端访问的重要个人数据
   1. 比如说个人笔记、图片、视频等数据，这些数据具有私密性，但又需要在多端访问。可借助支持
      将数据加密存储到云端的工具来实现
5. 个人电脑與 Homelab 的数据安全与灾难恢复
   1. 我主要使用 macOS 与 NixOS，因此主要考虑的是这两个系统的数据安全与灾难恢复

下面就分别就这几个部分展开讨论。

## 二、是否需要使用 YubiKey 等硬件密钥？

硬件密钥的好处是可以防止密钥泄漏，但 YubiKey 在国内无官方购买渠道，而且价格不菲，只买一个
YubiKey 的话还存在丢失的风险。

另一方面其实基于现代密码学算法的软件密钥安全性对我而言是足够的，而且软件密钥的使用更加方
便。或许在未来，我会考虑使用
[canokey-core](https://github.com/canokeys/canokey-core)、[OpenSK](https://github.com/google/OpenSK)、[solokey](https://github.com/solokeys/solo1)
等开源方案 DIY 几个硬件密钥，但目前我并不觉得有这必要。

## 三、SSH 密钥管理

### 2.1 SSH 密钥的生成

我们一般都是直接使用 `ssh-keygen` 命令生成 SSH 密钥对，OpenSSH 目前主要支持两种密钥算法：

1. RSA: 目前你在网上看到的大部分教程都是使用的 RSA 2048 位密钥，但其破解风险在不断提升，目
   前仅推荐使用 3072 位及以上的 RSA 密钥。
2. ED25519: 这是密码学家 Dan Bernstein 设计的一种新的签名算法，其安全性与 RSA 3072 位密钥
   相当，但其签名速度更快，且密钥更短，因此目前推荐使用 ED25519 密钥。

### 2.2 SSH 密钥的安全性

RSA 跟 ED25519 都是被广泛使用的密码学算法，其安全性都是经过严格验证的，因此我们可以放心使
用。但为了在密钥泄漏的情况下，能够尽可能减少损失，强烈建议给个人使用的密钥添加 passphrase
保护。

那这个 passphrase 保护到底有多安全呢？

有一些密码学知识的人应该知道，pssphrase 保护的实现原理通常是：通过 KDF 算法（或者叫慢哈希
算法、密码哈希算法）将用户输入的 passphrase 字符串转换成一个二进制对称密钥，然后再用这个密
钥加解密具体的数据。

因此，使用 pssphrase 加密保护的 SSH Key 的安全性，取决于：

1. passphrase 的复杂度，这对应其长度、字符集、是否包含特殊字符等。这由我们自己控制。
2. 所使用的 KDF 算法的安全性。这由 OpenSSH 的实现决定。

那么，OpenSSH 的 passphrase 是如何实现的？是否足够安全？

我首先 Google 了下，找到一些相关的文章（注意如下文章内容与其时间点相关，OpenSSH 的新版本会
有些变化）：

- [(2018)The default OpenSSH key encryption is worse than plaintext](https://news.ycombinator.com/item?id=17682946):
  OpenSSH 默认的 SSH RSA 密钥格式直接使用 MD5 来派生出用于 AES 加密的对称密钥，再用这个密
  钥加密你的 RSA 私钥，这意味着它的破解速度将会相当的快。
- [(2021)Password security of encrypted SSH private key: How to read round number or costfactor of bcrypt](https://serverfault.com/questions/1056814/password-security-of-encrypted-ssh-private-key-how-to-read-round-number-or-cost):
  这里有个老哥在回答中简单推算了下，以说明他认为 OpenSSH 默认的 passphrase 加密相当安全。

在 [OpenSSH release notes](https://www.openssh.com/releasenotes.html) 中搜索 passphrase 跟
kdf 两个关键字，找到些关键信息如下：

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

所以从 2014 年发布的 OpenSSH 6.5 开始，ed25519 密钥的 passphrase 才是使用 bcrypt KDF 生成
的。而对于其他类型的密钥，仍旧长期使用基于 MD5 hash 的密钥格式，没啥安全性可言。

即使 2023-08-10 发布的 9.4 版本增加了默认的 bcrypt KDF rounds 次数，它的安全性仍然很值得怀
疑。bcrypt 本身的安全性就越来越差，现代化的加密工具基本都已经升级到了 scrypt 甚至 argon2.
因此要想提升安全性，最好是能更换更现代的 KDF 算法，或者至少增加 bcrypt KDF 的 rounds 数
量。

我进一步看了 `man ssh-keygen` 的文档，没找到任何修改 KDF 算法的参数，不过能通过 `-a` 参数
来修改 KDF 的 rounds 数量，OpeSSh 9.4 的 man 信息中写了默认使用 16 rounds.

考虑到大部分人都使用默认参数生成 Key，而且绝大部分用户都没有密码学基础，大概率不知道
KDF、Rounds 是什么意思，我们再了解下 `ssh-keygen` 默认参数。在 release note 中我进一步找到
这个：

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

结合上面的分析可以推断出，目前绝大部分用户都是使用的 RSA 密钥，且其 passphrase 的安全性很
差，不加 passphrase 就是裸奔，加了也很容易被破解。如果你使用的也这种比较老的密钥类型，那千
万别觉得自己加了 passphrase 保护就很安全，这完全是错觉（

即使是使用最新的 ssh-keygen 生成的 ED25519 密钥，其默认也是用的 bcrypt 16 rounds 生成加密
密钥，其安全性在我看来也是不够的。

总结下，在不考虑其他硬件密钥/SSH CA 的情况下，最佳的 SSH Key 生成方式应该是：

```bash
ssh-keygen -t ed25519 -a 256 -C "xxx@xxx"
```

rounds 的值根据你本地的 CPU 性能来定，我在 Macbook Pro M2 上测了下，64 rounds 大概是
0.5s，128 rounds 大概需要 1s，256 rounds 大概 2s，用时与 rounds 值是线性关系。

考虑到我的个人电脑性能都还挺不错，而且只需要在每次重启电脑后通过 `ssh-add ~/.ssh/xxx` 解锁
一次，后续就一直使用内存中的密钥了，一两秒的时间还是可以接受的，因此我将当前使用的所有 SSH
Key 都使用上述参数重新生成了一遍。

### 2.3 SSH 密钥的分类管理

在所有机器上使用同一个 SSH 密钥，这是我过去的做法，但这样做有几个问题：

1. 一旦某台机器的密钥泄漏，那么就需要重新生成并替换所有机器上的密钥，这很麻烦。
1. 密钥需要通过各种方式传输到各个机器上，这也存在泄漏的风险。

因此，我现在的做法是：

1. 对所有桌面电脑跟笔记本，都在其本地生成一个专用的 SSH 密钥配置到 GitHub 跟常用的服务器
   上。**这个 SSH 私钥永远不会离开这台机器**。
2. 对于一些相对不重要的 Homelab 服务器，额外生成一个专用的 SSH 密钥，配置到这些服务器上。
   在一些跳板机跟测试机上会配置这个密钥方便测试与登录到其他机器。
3. 上述所有 SSH 密钥都添加了 passphrase 保护，且使用了 bcrypt 256 rounds 生成加密密钥。

我通过这种方式缩小了风险范围，即使某台机器的密钥泄漏，也只需要重新生成并替换这台机器上的密
钥即可。

### 2.4 SSH CA - 更安全合理的 SSH 密钥管理方案？

搜到些资料：

- [SSH 证书登录教程](https://www.ruanyifeng.com/blog/2020/07/ssh-certificate.html)

TODO 待研究。

## 四、个人的账号密码管理

我曾经大量使用了 Chrome/Firefox 自带的密码存储功能，但用到现在其实也发现了它们的许多弊端。
有同事推崇 1Password 的使用体验，它的自动填充跟同站点的多密码管理确实做得非常优秀，但一是
要收费，二是它是商业的在线方案，基于零信任原则，我不太想使用这种方案。

作为开源爱好者，我最近找到了一个非常适合我自己的方
案：[**password-store**](https://www.passwordstore.org/).

这套方案使用 gpg 加密账号密码，每个文件就是一个账号密码，通过文件树来组织与匹配账号密码与
APP/站点的对应关系，并且生态完善，对 firefox/chrome/android/ios 的支持都挺好。

缺点是用 GPG 加密，上手有点难度，但对咱来说完全可以接受。

我在最近使用 pass-import 从 firefox/chrome 中导入了我当前所有的账号密码，并对所有的重要账
号密码进行了一次全面的更新，一共改了二三十个账号，全部采用了随机密码。

当前的存储同步与多端使用方式：

1. pass 的加密数据使用 GitHub 私有仓库存储，pass 原生支持基于 Git 的存储方案。
   1. 因为数据全都是使用 ECC Curve 25519 GPG 加密的，即使仓库内容泄漏，数据的安全性仍然有
      保障。
1. 在浏览器与移动端，则分别使用这些客户端来读写 pass 中的密码：
   1. Android: <https://github.com/android-password-store/Android-Password-Store>
   1. IOS： <https://github.com/mssun/passforios>
   1. Brosers(Chrome/Firefox): <https://github.com/browserpass/browserpass-extension>
1. 基於雞蛋不放在同一個籃子裏的原則，otp/mfa 的動態密碼則使用 google authenticator 保存與
   多端同步，並留有一份離線備份用於災難恢復。登錄 Google 賬號目前需要我 Android 手機或短信
   驗證，因此安全性符合我的需求。

我的详细 pass 配置见
[ryan4yin/nix-config/password-store](https://github.com/ryan4yin/nix-config/tree/7e67466/home/base/desktop/password-store).

其他相关资料：

- [awesome-password-store](https://github.com/tijn/awesome-password-store)
- <https://github.com/gopasspw/gopass>: reimplement in go, with more features.

遇到过的一些问题与解法：

- [passforios - Merge conflicts](https://github.com/mssun/passforios/issues/131)

### 3.1 pass 使用的 GPG 够安全么？

GnuPG 是一个很有历史，而且使用广泛的加密工具，但它的安全性如何呢？

我找到些相关文档：

- [2021年，用更现代的方法使用PGP（上）][2021年，用更现代的方法使用PGP（上）]
- [Predictable, Passphrase-Derived PGP Keys][Predictable, Passphrase-Derived PGP Keys]
- [OpenPGP - The almost perfect key pair][OpenPGP - The almost perfect key pair]

简单总结下，GnuPG 的每个 secret key 都是随机生成的，互相之间没有关联（即不像区块链钱包那样
具有确定性）。生成出的 key 被使用 passphrase 加密保存，每次使用时都需要输入 passphrase 解
密。

那么还是之前在调研 OpenSSH 时我们提到的问题：它使用的 KDF 算法与参数是否足够安全？

OpenPGP 标准定义了
[String-to-Key (S2K)](https://datatracker.ietf.org/doc/html/rfc4880#section-3.7) 算法用于
从 passphrase 生成对称加密密钥，GnuPG 遵循该规范，并且提供了相关的参数配置选项，相关参数的
文档
[OpenPGP protocol specific options](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Options.html#OpenPGP-Options)
内容如下：

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

默认仍旧使用 AES-128 做 pssphrase 场景下的对称加密，数据签名还是用的 SHA-1，这俩都已经不太
安全了，尤其是 SHA-1，已经被证明存在安全问题。因此，使用默认参数生成的 GPG 密钥，其安全性
是不够的。

为了获得最佳安全性，我们需要：

1. 使用如下参数生成 GPG 密钥：

   ```
   gpg --s2k-mode 3 --s2k-count 65011712 --s2k-digest-algo SHA512 --s2k-cipher-algo AES256 ...
   ```

2. 加密、签名、认证都使用不同的密钥，每个密钥只用于特定的场景，这样即使某个密钥泄漏，也不
   会影响其他场景的安全性。

为了在全局使用这些参数，可以将它们添加到你的 `~/.gnupg/gpg.conf` 配置文件中。

详见我的 gpg 配置
[ryan4yin/nix-config/gpg](https://github.com/ryan4yin/nix-config/tree/7e67466/home/base/desktop/gpg)

## 五、跨平台的加密备份同步工具的选择

我日常同时在使用 macOS 与 NixOS，因此不论是需要离线存储的灾难恢复数据，还是需要在多端访问
的个人数据，都需要一个跨平台的加密备份与同步工具。

前面提到的 pass 使用 GnuPG 进行文件级别的加密，但在很多场景下这不太适用，而且 GPG 本身也太
重了，还一堆历史遗留问题，我不太喜欢。

为了其他数据备份与同步的需要，我需要一个跨平台的加密工具，目前调研到有如下这些：

1. 文件级别的加密
   1. 这个有很多现成的现代加密工具，比如 **age**/**sops**, 都挺不错，但是针对大量文件的情
      况下使用比较繁琐。
2. 全盘加密，或者支持通过 FUSE 模拟文件系统
   1. 首先 LUKS 就不用考虑了，它基本只在 Linux 上能用。
   1. 跨平台且比较活跃的项目中，我找到了 **rclone** 与 **restic** 这两个项目，都支持云同
      步，各有优缺点。
   1. restic 相对 rclone 的优势，主要是天然支持增量 snapshots 的功能，可以保存备份的历史快
      照，并设置灵活的历史快照保存策略。这对可能有回滚需求的数据而言是很重要的。比如说 PVE
      虚拟机快照的备份，有了 restic 我们就不再需要依赖 PVE 自身孱弱的快照保留功能，全交给
      restic 实现就行。
3. 多端加密同步
   1. 上面提到的 rclone 与 restic 都支持各种云存储，因此都是不错的多端加密同步工具。
   2. 最流行的开源数据同步工具貌似是 synthing，但它对加密的支持还不够完善，暂不考虑。

进一步调研后，我选择了 **age**, **rclone** 与 **restic** 作为我的跨平台加密备份与同步工
具。这三个工具都比较活跃，stars 很高，使用的也都是比较现代的密码学算法：

1. [age](https://age-encryption.org/v1): 对于对称加密的场景，使用 ChaCha20-Poly1305 AEAD
   加密方案，对称加密密钥使用 scrypt KDF 算法生成。
2. [rclone](https://rclone.org/crypt/): 使用基于 XSalsa20-Poly1305 的 AEAD 加密方案，key
   通过 scrypt KDF 算法生成，并且默认会加盐。
3. [restic](https://restic.readthedocs.io/en/stable/100_references.html#keys-encryption-and-mac):
   使用 AES-256-CTR 加密，使用 Poly1305-AES 认证数据，key 通过 scrypt KDF 算法生成。

对于 Nix 相关的 secrets 配置，我使用了 age 的一个适配库 agenix 完成其自动加解密配置，并将
相关的加密数据保存在我的 GitHub 私有仓库中。详见 [ryan4yin/nix-config/secrets]. 关于这个仓
库的详细加解密方法，在后面第八节「桌面电脑的数据安全」中会介绍。

## 六、灾难恢复相关的数据存储与管理

相关数据包括：GitHub, Twitter, Google 等重要账号的二次认证恢复代码、账号数据备份、PGP 主密
钥与吊销证书等等。

这些数据日常都不需要用到，但在账号或两步验证设备丢失时就非要使用到其中的数据才能找回账号或
吊销某个证书，是非常重要的数据。

我目前的策略是：使用 rclone + 1024bits 随机密码加密存储到两个 U 盘中（双副本），放在不同的
地方，并且每隔半年到一年检查一遍数据。

对应的 rclone 解密配置本身也设置了比较强的 passphrase 保护，并通过我的 secrets 私有 Git 仓
库多端加密同步。

## 七、需要在多端访问的重要个人数据

相关数据包括：个人笔记、重要的照片、录音、视频、等等。

因为日常就需要在多端访问，因此显然不能离线存储。

### 1. 个人笔记

不包含个人隐私的笔记，我直接用公开 GitHub 仓库 [ryan4yin/knowledge]
(https://github.com/ryan4yin/knowledge/) 存储了，不需要加密。

对于不便公开的个人笔记，有这些考虑：

1. 我的个人笔记目前主要是在移动端编辑，因此支持 Android/iOS 的客户端是必须的。
1. 要能支持 Markdown/Orgmode 等通用的纯文本格式，纯文本格式更容易编写与分析，而通用格式则
   可以避免被平台绑定。
1. 因为主要是移动端编辑，其实不需要多复杂的功能。
   - 以后可能会希望在桌面端做富文本编辑，但目前还没这种私人笔记的需求。
1. 希望具有类似 Git 的分布式存储与同步、笔记版本管理功能，如果能直接使用 Git 那肯定是最好
   的。
1. 端到端的加密存储与同步
1. 如果有类似 Git 的 Diff 功能就更好了。

我一开始考虑直接使用基于 Git 仓库的方案，能获得 Git 的所有功能，同时还避免额外自建一个笔记
服务。找到个 [GitJournal](https://github.com/GitJournal/GitJournal) ，数据存在 GitHub 私有
仓库用了一个月，功能不太多但够用。但发现它项目不咋活跃，基于 SSH 协议的 Git 同步在大仓库上
也有些毛病，而且数据明文存在 Git 仓库里，安全性相对差一些。

另外找到个 [git-crypt](https://github.com/AGWA/git-crypt) 能在 Git 上做一层透明加密，但没
找到支持它的移动端 APP，而且项目也不咋活跃。

在 <https://github.com/topics/note-taking> 下看了些流行项目，主要有这些：

1. Joplin
   - 支持 S3/WebDAV 等多种协议同步数据，支持端到端加密
2. Outline 等 Wiki 系统
   - 它直接就是个 Web 服务，主要面向公开的 Wiki，不适合私人笔记
3. Logseq/Obsidian 等双链笔记软件（其中 Obsidian 是闭源软件）
   - 都是基于本地文件的笔记系统，也没加密工具，需要借助其他工具实现数据加密与同步
   - 其中 Logseq 是大纲流，一切皆列表。而 Obsidian 是文档流，比较贴近传统的文档编辑体验。
   - Obsidian 跟 Logseq 的 Sync 功能都是按月收费，相当的贵。社区有通过 Git 同步的方案，但
     都很 trickk，也不稳定。
4. AppFlowy/Affine/apitable 等 Notion 替代品
   - 都是富文本编辑，不适合移动端设备

在移动端使用 Synthing 或 Git 等第三方工具同步笔记数据，都很麻烦，而且安全性也不够。因此目
前看在移动端也能用得舒服的话，最稳妥的选择是第一类笔记 APP，简单试用后我选择了最流行的
Joplin.

### 2. 照片、视频等其他个人数据

1. Homelab 中的 Windows-NAS-Server，两个 4TB 的硬盘，通过 SMB 局域网共享，公网所有客户端
   （包括移动端）都能通过 tailscale + rclone 流畅访问。
1. 部分重要的数据再通过 rclone 加密备份一份到云端，可选项有：
   1. [青云对象存储](https://www.qingcloud.com/products/objectstorage/) 与
      [七牛云对象存储 Kodo](https://www.qiniu.com/prices/kodo)，它们都有每月 10GB 的免费存
      储空间，以及 1GB-10GB 的免费外网流量。
   1. [阿里云 OSS](https://help.aliyun.com/zh/oss/product-overview/billing-overview) 也能
      免费存 5GB 数据以及每月 5GB 的外网流量，可以考虑使用。

## 八、桌面电脑與 Homelab 的数据安全

我的桌面电脑都是 macOS 与 NixOS，Homlab 虚拟机也已经 all in NixOS，另外我目前没有任何云上
服务器。

另外虽然也有两台 Windows 虚拟机，但极少对它们做啥改动，只要做好虚拟机快照的备份就 OK 了。

对于 NixOS 桌面系统与 Homelab 虚拟机，我当前的方案如下：

- 桌面主机
  - 启用 LUKS2 全盘加密 + Secure Boot，在系统启动阶段需要输入 passphrase 解密 NixOS 系统盘
    才能正常进入系统。
    - LUKS2 的 passphrase 为一个比较长的密码学随机字符串。
    - LUKS2 的所有安全设置全拉到能接受的最高（比较重要的是 `--iter-time`，计算出 unlock
      key 的用时，默认 2s，安全起见咱设置成了 5s）
      ```
      cryptsetup --type luks2 --cipher aes-xts-plain64 --hash sha512 --iter-time 5000 --key-size 256 --pbkdf argon2id --use-urandom --verify-passphrase luksFormat device
      ```
    - LUKS2 使用的 argon2id 是比 scrypt 更强的 KDF 算法，其安全性是足够的。
  - 桌面主機使用 tmpfs 作为根目录，所有未明确声明持久化的数据，都会在每次重启后被清空，这
    强制我去了解自己装的每个软件都存了哪些数据，是否需要持久化，使整个系统更白盒，提升了整
    个系统的环境可信度。
- Homelab
  - Proxmox VE 物理机全部重装为 NixOS，启用 LUKS 全盘加密与 btrfs + zstd 压缩，买几个便宜
    的 U 盘用于自动解密（注意解密密钥的离线加密备份）。使用 K3s + KubeVirt 管理 QEMU/KVM
    虚拟机。
- Secrets 說明
  - 重要的通用 secrets，都加密保存在我的 secrets 私有仓库中，在部署我的 nix-config 时使用
    主机本地的 SSH 系统私钥自动解密。
    - 也就是说要在一台新电脑（不論是桌面主機還是 NixOS 虛擬機）上成功部署我的 nix-config
      配置，需要的准备流程：
      - 本地生成一个新的 ssh key，将公钥配置到 GitHub，并 `ssh-add` 这个新的私钥，使其能够
        访问到我的私有 secrets 仓库。
      - 将新主机的系统公钥 `/etc/ssh/ssh_host_ed25519_key.pub` 发送到一台旧的可解密
        secrets 仓库数据的主机上。如果该文件不存在则先用 `sudo ssh-keygen -A` 生成。
      - 在旧主机上，将收到的新主机公钥添加到 secrets 仓库的 secrets.nix 配置文件中，并使用
        agenix 命令 rekey 所有 secrets 数据，然后 commit & push。
      - 现在新主机就能够通过 `nixos-rebuild switch` 或 `darwin-rebuild switch` 成功部署我
        的 nix-config 了，agenix 会自动使用新主机的系统私钥
        `/etc/ssh/ssh_host_ed25519_key` 解密 secrets 仓库中的数据并完成部署工作。
    - 这份 secrets 配置在 macOS 跟 NixOS 上通用，也与 CPU 架构无关，agenix 在这两个系统上
      都能正常工作。
  - 基于安全性考虑，对 secrets 进行分类管理与加密：
    - 桌面电脑能解密所有的 secrets
    - Homelab 中的跳板机只能解密 Homelab 相关的所有 secrets
    - 其他所有的 NixOS 虚拟机只能解密同类别的 secrets，比如一台监控机只能解密监控相关的
      secrets.

对于 macOS，它本身的磁盘安全我感觉就已经做得很 OK 了，而且它能改的东西也比较有限。我的安全
设置如下：

- 启用 macOS 的全盘加密功能
- 常用的 secrets 的部署与使用方式，与前面 NixOS 的描述完全一致

### macOS/NixOS 数据的灾难恢复？

在使用 nix-darwin 跟 NixOS 的情况下，整个 macOS/NixOS 的系统环境都是通过我的
[ryan4yin/nix-config] 声明式配置的，因此桌面电脑的灾难恢复根本不是一个问题。

只需要简单的几行命令就能在一个全新的系统上恢复出我的 macOS / NixOS 桌面环境，所有密钥也会
由 agenix 自动解密并放置到正确的位置。

要说有恢复难题的，也就是一些个人数据了，这部分已经在前面第七小节介绍过了，用 rclone/restic
就行。

## 九、总结下我的数据存在了哪些地方

1. secrets 私有仓库: 它会被我的 nix-config 自动拉取并部署到所有主力电脑上，包含了 homelab
   ssh key, GPG subkey, 以及其他一些重要的 secrets.
   1. 它通过我所有桌面电脑的 `/etc/ssh/ssh_host_ed25519_key.pub` 公钥加密，在部署时自动使
      用对应的私钥解密。
   1. 此外该仓库还添加了一个灾难恢复用的公钥，确保在我所有桌面电脑都丢失的极端情况下，仍可
      通过对应的灾难恢复私钥解密此仓库的数据。该私钥在使用 age 加密后（注：未使用 rclone
      加密）与我其他的灾难恢复数据保存在一起。
2. password-store: 我的私人账号密码存储库，通过 pass 命令行工具管理，使用 GPG 加密，GPG 密
   钥备份被通过 age/agenix 加密保存在上述 secrets 仓库中。
   1. 由于 GnuPG 自身导出的密钥备份数据安全性欠佳，因此我使用了 age + passphrase 对其进行
      了二次对称加密，然后再通过 agenix 加密（第三次加密，使用非对称加密算法）保存在
      secrets 仓库中。这保障了即使我的 GPG 密钥在我所有的桌面电脑上都存在，但安全性仍旧很
      够。
3. rclone 加密的备份 U 盘（双副本）：离线保存一些重要的数据。其配置文件被加密保存在
   secrets 仓库中，其配置文件的解密密码被加密保存在 password-store 仓库中。

这套方案的大部分部署工作都是由我的 Nix 配置自动完成的，整个流程的自动化程度很高，所以这套
方案带给我的额外负担并不大。

secrets 这个私有仓库是整个方案的核心，它包含了所有重要数据（password-store/rclone/...）的
解密密钥。如果它丢失了，那么所有的数据都无法解密。

但好在 Git 仓库本身是分布式的，我所有的桌面电脑上都有对应的完整备份，我的灾难恢复存储中也
会定期备份一份 secrets/password-store 两个仓库的数据过去以避免丢失。

另外需要注意的是，为了避免循环依赖，secrets 与 password-store 这两个仓库的备份不应该使用
rclone 再次加密，而是直接使用 age 对称加密。这样只要我还记得 age 的解密密码、gpg 密钥的
passphrase 等少数几个密码，就能顺着整条链路解密出所有的数据。

## 十、这套方案下需要记忆几个密码？这些密码该如何设计？

绝大部分密码都建议设置为包含大小写跟部分特殊字符的密码学随机字符串，通过 pass 加密保存与多
端同步与自动填充，不需要额外记忆。考虑到我们基本不会需要手动输入这些密码，因此它们的长度可
以设置得比较长，比如 16-24 位（不使用更长密码的原因是，许多站点或 APP 都限制了密码长度，这
种长度下使用 passphrase 单词组的安全性相对会差一点，因此也不推荐）。

再通过一些合理的密码复用手段，可以将需要记忆的密码数量降到 3 - 5 个，并且确保日常都会输
入，避免遗忘。

不过这里需要注意一点，就是 SSH 密钥、GPG 密钥、系统登录密码这三个密码最好不要设成一样。前
面我们已经做了分析，这三个 passphrase 的加密强度区别很大，设成一样的话，使用 bcrypt 的 SSH
密钥将会成为整个方案的短板。

而关于密码内容的设计，这个几核心 pssphrase 的长度都是不受限的，有两个思路（注意不要在密码
中包含任何个人信息）：

1. 使用由一个个单词组成的较长的 passphrase，比如
   `don't-do-evil_I-promise-this-would-become-not-a-dark-corner` 这样的。
2. 使用字母大小写加数字、特殊字符组成的密码学随机字符串，比如 `fsD!.*v_F*sdn-zFkJM)nQ` 这
   样的。

第一种方式的优点是，这些单词都是常用单词，记忆起来会比较容易，而且也不容易输错。

第二种方式的优点是，密码学随机字符串可以以更短的长度达到与第一种方式相当的安全性。但它的缺
点也比较明显——容易输错，而且记忆起来也不容易。

两种方式是都可以，如果你选择第二种方式，可以专门编些小故事来通过联想记忆它们，hint 中也能
加上故事中的一些与密码内容无直接关联的关键字帮助回忆。毕竟人类擅长记忆故事，但不擅长记忆随
机字符。举个例子，上面的密码 `fsD!.*v_F*sdn-zFkJM)nQ`，可以找出这么些联想：

- `fs`: 「佛说」这首歌里面的歌词
- `D!`: 头文字D!
- `.*`: 地面上的光斑(.)，天上的星光(\*)
- `v_`: 嘴巴张开（v）睡得很香的样子，口水都流到地上了(\_)
- `F*sdn`: F\*ck 软件定义网络(sdn)
- `zFkJM`: 在政府（zf）大门口（k），看(k) 见了 Jack Ma (JM) 在跳脱yi舞...
- `)nQ`: 宁静的夏夜，凉风习习，天上一轮弯月，你(n)问(Q)我，当下这一刻是否足够

把上面这些联想串起来，就是一个怀旧、雷人、结尾又有点温馨的无厘头小故事了，肯定能令你自己印
象深刻。故事写得够离谱的话，你可能想忘都忘不掉了。

总之就是用这种方式，然后把密码中的每个字符都与故事中的某个关键字联系起来，这样就能很容易地
记住这个密码了。如果你对深入学习如何记忆这类复杂的东西感兴趣，可以看看这
本[我最想要的记忆魔法书](https://book.douban.com/subject/6710983/).

最后一点，就是定期更新一遍这些密码、SSH 密钥、GPG 密钥。所有数据的加密安全性都是随着时间推
移而降低的，曾经安全的密码学算法在未来也可能会变得不再安全（这方面 MD5, SHA-1 都是很好的例
子），因此定期更新这些密码跟密钥是很有必要的。

几个核心密码更新起来会简单些，可以考虑每年更新一遍，而密钥可以考虑每两三年更新一遍（时间凭
感觉说的哈，没有做论证）。其他密码密钥则可以根据数据的重要性来决定更新频率。

## 十一、为了落地这套方案，我做了哪些工作？

前面已经基本都提到了，这里再总结下：

1. 重新生成了所有的 SSH Key，增强了 passphrase 强度，bcrypt rounds 增加到 256，通过
   `ssh-add` 使用，只需要在系统启动后输入一次密码即可，也不麻烦。
2. 重新生成了所有的 PGP Key，主密钥离线加密存储，本地只保留了加密、签名、认证三个 PGP 子密
   钥。
3. 重新生成了所有重要账号的密码，全部使用随机密码，一共改了二三十个账号。考虑到旧的 backup
   code 可能已经泄漏，我也重新生成了所有重要账号的 backup code.
4. 重装 NixOS，使用 LUKS2 做全盘加密，启用 Secure Boot. 同时使用 tmpfs 作为根目录，所有未
   明确声明持久化的数据，都会在每次重启后被清空。
5. 使用 nix-darwin 与 home-manager 重新声明式地配置了我的两台 MacBook Pro（Intel 跟 Apple
   Silicon 各一台），与我的 NixOS 共用了许多配置，最大程度上保持了所有桌面电脑的开发环境一
   致性，也确保了我始终能快速地在一台新电脑上部署我的整个开发环境。
6. 注销印象笔记账号，使用 evernote-backup 跟 evernote2md 两个工具将个人的私密笔记遷移到了
   Joplin + OneDrive 上，Homelab 中設了通過 restic 定期自動加密備份 OneDrive 中的 Joplin
   數據。
7. 比较有价值的 GitHub 仓库，都设置了禁止 force push 主分支，并且添加了 github action 自动
   同步到国内 Gitee.
8. All in NixOS，将 Homelab 中的 PVE 全部使用 NixOS + K3s + KubeVirt 替换。从偏黑盒且可复
   现性差的 Ubuntu、Debian, Proxmox VE, OpenWRT 等 VM 全面替换成更白盒且可复现性强的
   NixOS、KubeVirt，提升我对内网环境的掌控度，进而提升内网安全性。

## 十二、灾难恢复预案

这里考虑我的 GPG 子密钥泄漏了、pass 密码仓库泄漏了等各种情况下的灾难恢复流程。

TODO 后续再慢慢补充。

## 十三、未来可能的改进方向

目前我的主要个人数据基本都已经通过上述方案进行了安全管理。但还有这些方面可以进一步改进：

- 针对 Homelab 的虚拟机快照备份，从我旧的基于 rclone + crontab 的明文备份方案，切换到了基
  于 restic 的加密备份方案。
- 手机端的照片视频虽然已经在上面设计好了备份同步方案，但仍未实施。考虑使用 roundsync 加密
  备份到云端，实现多端访问。
- 进一步学习下 appamor, bubblewrap 等 Linux 下的安全限制方案，尝试应用在我的 NixOS PC 上。
- Git 提交是否可以使用 GnuPG 签名，目前没这么做主要是觉得 PGP 这个东西太重了，目前我也只在
  pass 上用了它，而且还在研究用 age 取代它。
- 尝试通过 [hashcat](https://github.com/hashcat/hashcat),
  [wifi-cracking](https://github.com/brannondorsey/wifi-cracking) 等手段破解自己的重要密
  码、SSH 密钥、GPG 密钥等数据，评估其安全性。
- 使用一些流行的渗透测试工具测试我的 Homelab 与内网环境，评估其安全性。

安全总是相对的，而且其中涉及的知识点不少，我 2022 年学了密码学算是为此打下了个不错的基础，
但目前看前头还有挺多知识点在等待着我。我目前仍然打算以比较 casual 的心态去持续推进这件事
情，什么时候兴趣来了就推进一点点（我从 2023-05 定下）。

这套方案也可能存在一些问题，欢迎大家审阅指正。

[2021年，用更现代的方法使用PGP（上）]:
  https://ulyc.github.io/2021/01/13/2021%E5%B9%B4-%E7%94%A8%E6%9B%B4%E7%8E%B0%E4%BB%A3%E7%9A%84%E6%96%B9%E6%B3%95%E4%BD%BF%E7%94%A8PGP-%E4%B8%8A/
[Predictable, Passphrase-Derived PGP Keys]: https://nullprogram.com/blog/2019/07/10/
[OpenPGP - The almost perfect key pair]:
  https://blog.eleven-labs.com/en/openpgp-almost-perfect-key-pair-part-1/
[ryan4yin/nix-config]: https://github.com/ryan4yin/nix-config
[ryan4yin/nix-config/secrets]: https://github.com/ryan4yin/nix-config/tree/7e67466/secrets
