---
title: "写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议"
date: 2022-03-14T00:00:00+08:00
lastmod: 2022-03-14T00:00:00+08:00
draft: false
resources:
- name: "featured-image"
  src: "https-secure.webp"

tags: ["Cryptography", "密码学", "HTTPS", "TLS", "SSL", "OpenSSL", "PKI", "数字证书", "证书", "SSH", "QUIC", "HTTP/3",  "安全"]
categories: ["tech"]

series: ["写给开发人员的实用密码学"]
series_weight: 8
seriesNavigation: true
---

>本文基本上是一篇原创文章，但是行文有点生硬，仍然在优化中，不太适合初学者阅读。

《写给开发人员的实用密码学》系列文章目录: 

- [写给开发人员的实用密码学（一）—— 概览](/posts/practical-cryptography-basics-1/)
- [写给开发人员的实用密码学（二）—— 哈希函数](/posts/practical-cryptography-basics-2-hash/)
- [写给开发人员的实用密码学（三）—— MAC 与密钥派生函数 KDF](/posts/practical-cryptography-basics-3-key-derivation-function/)
- [写给开发人员的实用密码学（四）—— 安全随机数生成器 CSPRNG](/posts/practical-cryptography-basics-4-secure-random-generators/)
- [写给开发人员的实用密码学（五）—— 密钥交换 DHKE 与完美前向保密 PFS](/posts/practical-cryptography-basics-5-key-exchange/)
- [写给开发人员的实用密码学（六）—— 对称密钥加密算法](/posts/practical-cryptography-basics-6-symmetric-key-ciphers/)
- [写给开发人员的实用密码学（七）—— 非对称密钥加密算法 RSA/ECC](/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/)
- [写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议](/posts/about-tls-cert)
- 待续


## 更新记录

- **2021-01-17**: 完成 TLS 协议简介、数字证书介绍、数字证书的申请或生成方法、mTLS 介绍、TLS 协议的破解手段
- **2022-03-13** ~ **2022-03-14**: 重新整理补充，改写为《写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议》，整合进我的实用密码学系列文章中
  - 补充 PKI 公钥基础架构及 X509 证书标准介绍
- TODO:
  - 补充 TLS 协议的逆向手段
  - 基于 [cfssl](https://shoujo.ink/2021/11/cfssl-%E6%A0%B8%E5%BF%83%E6%A8%A1%E5%9D%97%E5%88%86%E6%9E%90/) 详细介绍 PKI 的各项组件
  - 基于 PKI 的应用服务间身份识别技术：[SPIFF ID](https://github.com/spiffe/spiffe)
    - SPIFF ID 是云原生领域的标准，[服务网格项目 Istio 就使用了 SPIFF ID 作为安全命名](https://shoujo.ink/2021/10/istio-%E5%AE%89%E5%85%A8%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90%E4%B9%8B-pki-%E4%B8%8E%E9%80%9A%E4%BF%A1%E5%AE%89%E5%85%A8/)

---

## 零、前言

现代人的日常生活中，HTTPS 协议几乎无处不在，我们每天浏览网页时、用手机刷京东淘宝时、甚至每天秀自己绿色的健康码时，都在使用 HTTPS 协议。

作为一个开发人员，我想你应该多多少少有了解一点 HTTPS 协议。
你可能知道 HTTPS 是一种加密传输协议，能保证数据传输的保密性。
如果你拥有部署 HTTPS 服务的经验，那你或许还懂如何申请权威 HTTPS 证书，并配置在 Nginx 等 Web 程序上。

但是你是否清楚 HTTPS 是由 HTTP + TLS 两种协议组合而成的呢？
更进一步你是否有抓包了解过 TLS 协议的完整流程？是否清楚它加解密的底层原理？是否清楚 Nginx 的 HTTPS 配置中一堆密码学参数的真正含义？是否知道 TLS 协议有哪些弱点、存在哪些攻击手段、如何防范？

我们在《写给开发人员的实用密码学》的前七篇文章中已经学习了许多的密码学概念与算法，接下来我们就利用这些知识，深度剖析下 HTTPS 协议中的数字证书以及 TLS 协议。


## 一、数字证书与 PKI 公钥基础架构

我们在前面已经学习了「对称密码算法」与「非对称密码算法」两个密码学体系，这里做个简单的总结。

- **对称密码算法（如 AES/ChaCha20）**: **计算速度快、安全强度高，但是缺乏安全交换密钥的手段、密钥的保存和管理也很困难**。
- **非对称密码算法（如 RSA/ECC）: 计算速度慢，但是它解决了上述对称密码算法最大的两个缺陷，一是给出了安全的密钥交换算法 DHE/ECDHE，二呢它的公钥是可公开的，这降低了密钥的保存与管理难度**。

但是非对称密码算法仍然存在一些问题: 

- **公钥该如何分发**？比如 Alice 跟 Bob 交换公钥时，如何确定收到的确实是对方的公钥，也就是说如何确认公钥的真实性、完整性、认证其来源身份？
   - 前面我们已经学习过，DH/ECDH 密钥交换协议可以防范嗅探攻击（窃听），但是**无法抵挡中间人攻击**（中继）。
- 如果 Alice 的私钥泄漏了，她该**如何作废自己旧的公钥**？

数字证书与公钥基础架构就是为了解决上述问题而设计的。

首先简单介绍下公钥基础架构（Public Key Infrastructure），它是一组由硬件、软件、参与者、管理政策与流程组成的基础架构，其目的在于创造、管理、分配、使用、存储以及撤销数字证书。
PKI 是一个总称，而并非指单独的某一个规范或标准，因此显然数字证书的规范（X.509）、存储格式（PKCS系列标准、DER、PEM）、TLS 协议等都是 PKI 的一部分。

我们下面从公钥证书开始逐步介绍 PKI 中的各种概念及架构。

### 1. 公钥证书

前面我们介绍了公钥密码系统存在的一个问题是「在分发公钥时，难以确认公钥的真实性、完整性及其来源身份」。
PKI 通过「数字证书」+「证书认证机构」来解决这个问题，下面先简单介绍下「数字证书」。

**数字证书**指的其实就是**公钥证书**（也可直接简称为**证书**）。
在现代网络通讯中通行的公钥证书标准名为 [X.509](https://zh.wikipedia.org/wiki/X.509) v3, 由 [RFC5280](https://tools.ietf.org/html/rfc5280) 定义。
X.509 v3 格式被广泛应用在 TLS/SSL 等众多加密通讯协议中，它规定公钥证书应该包含如下内容: 

- 证书
  - **序列号**（Serial Number）: 用以识别每一张证书，在作废证书的时候会用到它
  - **版本**: 证书的规范版本
  - **公钥**（Public Key）: 我们的核心目的就是分发公钥，因此显然要把公钥放在证书里面
  - **公钥指纹**: 即公钥的 Hash 值，当前大部分证书都使用 SHA256 计算此指纹
  - **公钥用途**（Key Usage + Extended Key Usage）: 记录了此证书可用于哪些用途——数字签名、身份认证等
  - **主体**（Subject）: 即姓名、组织、邮箱、地址等证书拥有者的个人信息。
    - 有了这个我们就能确认证书的拥有者了
  - **证书有效期的开始时间、结束时间**（Not Before + Not After）: 为了确保安全性，每个证书都会记录一个自身的有效期
    - 证书一旦签发并公开，随着科技的发展、时间的推移，其公钥的安全性会慢慢减弱
    - 因此每个证书都应该包含一个合理的有效期，证书的拥有者应该在有效期截止前更换自身的证书以确保安全性
  - **签发者**（Issuer）: 签发此证书的「签发者」信息
  - 其他拓展信息
- **数字签名**（Signature）: 我们还需要对上面整个证书计算一个数字签名，来确保这些数据的真实性、完整性，确保证书未被恶意篡改/伪造
  - 此数字签名由「证书签发者（Issuer）」使用其私钥+证书内容计算得出
- **数字签名算法**（Signature Algorithm）: 证书所使用的签名算法，常用的有 `RSA-SHA-256` 与 `ECDSA-SHA-256`

每个证书都有唯一的 ID，这样在私钥泄漏的情况下，我们可以通过公钥基础设施的 OCSP（Online Certificate Status Protocol）协议吊销某个证书。

吊销证书的操作还是比较罕见的，毕竟私钥泄漏并不容易遇到，因此这里就略过不提了，有需要的可以自行搜索。

使用 Firefox 查看网站 `https://www.google.com` 的证书信息如下：

{{< figure src="/images/about-tls-cert/cert-content.webp" title="Google 证书内容" >}}

### 2. 证书链

前面介绍证书内容时，提到了每个证书都包含「签发者（Issuer）」信息，并且还包含「签发者」使用「证书内容」与「签发者私钥」生成的数字签名。

那么在证书交换时，如何验证证书的真实性、完整性及来源身份呢？
根据「数字签名」算法的原理，显然需要使用「签发者公钥」来验证「被签发证书」中的签名。

仍然辛苦 Alice 与 Bob 来演示下这个流程:

- 假设现在 Alice 生成了自己的公私钥对，她想将公钥发送给远在千里之外的 Bob，以便与 Bob 进行加密通讯
- 但是如果 Alice 直接发送公钥给 Bob，Bob 并无法验证其来源是 Alice，也无法验证证书是否被篡改

PKI 引入了一个**可信赖的第三者**（Trusted third party，TTP）来解决这个问题。
在 Alice 与 Bob 的案例中，就是说还有个第三者 **Eve**，他使用自己的私钥为自己的公钥证书签了名，生成了一个「自签名证书」，并且已经提前将这个「自签名证书」分发（比如当面交付、物理分发 emmm）给了 Alice 跟 Bob.

- 现在 Alice 首先使用自己的公钥以及个人信息制作了自己的公钥证书，但是这个证书还缺乏一个 Issuer 属性以及数字签名，我们把它叫做「证书签名请求（Certificate Signing Request, CSR）」
- 为了实现将证书安全传递给远在千里之外的 Bob，Alice 找到 Eve，将这个 CSR 文件提交给 Eve
- Eve 验证了 Alice 的身份后，再使用这个 CSR 签发出完整的证书文件（Issuer 就填 Eve，然后 Eve 使用自己的私钥计算出证书的数字签名）交付给 Alice
  - Eve 可是曾经跨越千里之遥，将自己的公钥证书分发给了 Bob，所以在给 Alice 签发证书时，他显然可能会要求 Alice 给付「签名费」。目前许多证书机构就是靠这个赚钱的，当然也有非盈利的证书颁发机构如 Let's Encrypt.
- 现在 Alice 再将经 Eve 签名的证书发送给 Bob
- Bob 收到证书后，看到 Issuer 是 Eve，于是找出以前 Eve 给他的「自签名证书」，然后使用其中的公钥验证收到的证书
- 如果验证成功，就说明证书的内容是经过 Eve 认证的。如果 Eve 没老糊涂了，那这个证书应该确实就是 Alice 的。
- 如果验证失败，那说明这是某个攻击者伪造的证书。

在现实世界中，Eve 这个角色被称作「**证书认证机构**（Certification Authority, CA）」，全世界只有几十家这样的权威机构，它们都通过了各大软件厂商的严格审核，从而将根证书（CA 证书）直接内置于主流操作系统与浏览器中，也就是说早就提前分发给了因特网世界的几乎所有用户。

由于许多操作系统或软件的更新迭代缓慢（2022 年了还有人用 XP 你敢信？），根证书的有效期通常都在十年以上。

但是，如果 CA 机构直接使用自己的私钥处理各种证书签名请求，这将是非常危险的。
因为全世界有海量的 HTTPS 网站，也就是说有海量的证书需求，可一共才几十家 CA 机构。
频繁的动用私钥会产生私钥泄漏的风险，如果这个私钥泄漏了，那将直接影响海量网站的安全性。

PKI 架构使用「**数字证书链**（也叫做**信任链**）」的机制来解决这个问题:

- CA 机构首先生成自己的根证书与私钥，并使用私钥给根证书签名
  - 因为私钥跟证书本身就是一对，因此根证书也被称作「自签名证书」
- CA 根证书被直接交付给各大软硬件厂商，内置在主流的操作系统与浏览器中
- 然后 CA 机构再使用私钥签发一些所谓的「**中间证书**」，之后就把私钥雪藏了，非必要不会再拿出来使用。
  - 根证书的私钥通常**离线存储**在安全地点
  - 中间证书的有效期通常会比根证书短一些
  - 部分中间证书会被作为备份使用，平常不会启用
- CA 机构使用这些中间证书的私钥，为用户提交的所有 CSR 请求签名

画个图来表示大概是这么个样子：

{{< figure src="/images/about-tls-cert/chain-of-trust.webp" >}}

CA 机构也可能会在经过严格审核后，为其他机构签发中间证书，这样就能赋予其他机构签发证书的权利，而且根证书的安全性不受影响。

如果你访问某个 HTTPS 站点发现浏览器显示小绿锁，那就说明这个证书是由某个权威**认证机构**签发的，其信息是经过这些机构认证的。

上述这个全球互联网上，由**证书认证机构**、操作系统与浏览器内置的根证书、TLS 加密认证协议、OCSP 证书吊销协议等等组成的架构，我们可以称它为 **Web PKI**.

**Web PKI** 通常是可信的，但是并不意味着它们可靠。历史上出现过许多由于安全漏洞（[2011 DigiNotar 攻击](http://www.ip-guard.net/blog/?p=834)）或者政府要求，证书认证机构将假证书颁发给黑客或者政府机构的情况。获得假证书的人将可以随意伪造站点，而所有操作系统或浏览器都认为这些假站点是安全的（显示小绿锁）。

因为**证书认证机构**的可靠性问题以及一些其他的原因，部分个人、企业或其他机构（比如金融机构）会生成自己的根证书与中间证书，然后自行签发证书，构建出自己的 PKI 认证架构，我们可以将它称作**内部 PKI**或者**私有 PKI**。
但是这种自己生成的根证书是未内置在操作系统与浏览器中的，为了确保安全性，用户就需要先手动在设备上安装好这个数字证书。
自行签发证书的案例有：

- 微信、支付宝及各种银行客户端中的数字证书与安全性更高的 USB 硬件证书（U 盾），这种涉及海量资金安全甚至国家安全的场景，显然不能直接使用前述普通权威 CA 机构签发的证书。
- 局域网通信，通常是网络管理员生成一个本地 CA 证书安装到所有局域网设备上，再用它的私钥签发其他证书用于局域网安全通信
  - 典型的例子是各企业的内部通讯网络，比如 Kubernetes 容器集群

现在再拿出前面 `https://www.google.com` 的证书截图看看，最上方有三个标签页，从左至右依次是「服务器证书」、「中间证书」、「根证书」，可以点进去分别查看这三个证书的各项参数，各位看官可以自行尝试：

{{< figure src="/images/about-tls-cert/cert-content.webp" title="Google 证书内容" >}}

#### 交叉签名

按前面的描述，每个权威认证机构都拥有一个正在使用的根证书，使用它签发出几个中间证书后，就会把它离线存储在安全地点，平常仅使用中间证书签发终端实体证书。
这样实际上每个权威认证机构的证书都形成一颗证书树，树的顶端就是根证书。

实际上在 PKI 体系中，一些证书链上的中间证书会被使用多个根证书进行签名——我们称这为交叉签名。
交叉签名的主要目的是提升证书的兼容性——客户端只要安装有其中任何一个根证书，就能正常验证这个中间证书。
从而使中间证书在较老的设备也能顺利通过证书验证。


### 3. 证书的存储格式与编码标准

>证书的格式这一块，是真的五花八门...沉重的历史包袱...

X509 只规定了证书应该包含哪些信息，但是未定义证书该如何存储。为了解决证书的描述与编码存储问题，又出现了如下标准：

- ASN.1 结构：是一种描述证书格式的方法。
  - 它类似 protobuf 数据描述语言、SQL DDL
  - ASN.1 只规定了该如何描述证书，未定义该如何编码。
- 将 ASN.1 结构编码存储的格式有
  - DER：一种二进制编码格式
  - PEM：DER 是二进制格式，不便于复制粘贴，因此出现了 PEM，它是一个文本编码格式（其实就是把 DER 编码后的数据再 Base64 编码下...）
- 某些场景下，X.509 信息不够丰富，因此又设计了一些信息更丰富（例如可以包含证书链、公私钥对）的证书封装格式，包括 PKCS #7 和 PKCS #12
  - 仍然用 ASN.1 格式描述
  - 基本都是用 DER 编码

下面详细介绍下这些相关的标准与格式。

#### 编码存储格式 DER 与 PEM

DER 是由国际电信联盟（ITU）在 [ ITU-T X.690](https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=x.690)标准中定义的一种数据编码规则，用于将 ASN.1 结构的信息编码为二进制数据。
直接以 DER 格式存储的证书，大都使用 `.cer` `.crt` `.der` 拓展名，在 Windows 系统比较常见。

而 PEM 格式，即 Privacy-Enhanced Mail，是 openssl 默认使用的证书格式。可用于编码公钥、私钥、公钥证书等多种密码学信息。
PEM 其实就是在 DER 的基础上多做一步——使用 Base64 将 DER 编码出的二进制数据再处理一次，编码成字符串再存储。好处是存储、传输要方便很多，可以直接复制粘贴。

一个 2048 位 RSA 公钥的 PEM 文件内容如下：

```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyl6q6BkEcEUi9V1/Q7il
bngnh1YzG1tM4Hd6XCZQ35OzDN4my9eXWtjoL8YvLYqlYTJqhTHpuptgjF/lmlhg
WIMKNNcuDAbvmWExRyZateVrjO9OtgkyJCuGhaum0TIUC+dbZ9L9xsdK/fU1L5BB
nPRSYMloH8uE1CbK/DhFUiKp36aHZFfqLPicY3c6/N+k2kIJCEWBY0SROqpqy2Iz
yCIP54JSoOoGz6pdtWhd5cEeicr9e7f/WixEES6fgavqIHzhSJBVctpMgFPjFZ/x
JJhQVf23WKb3YQQ/0Uc8O7OTDXoUfuJP9UgqvKNh4hPfJA+a4nxkDYhTPfrLHfKY
YwIDAQAB
-----END PUBLIC KEY-----
```

PEM 格式的数据通常以 `.pem` `.key` `.crt` `.cer` 等拓展名存储，直接 `cat` 一下是不是字符串，就能确认该文件是否是 PEM 格式了。

因为纯文本格式处理起来很方便，大部分场景下证书、公钥、私钥等信息都会被编码成 PEM 格式再进行存储、传输。

openssl 默认使用的输入输出均 PEM 格式。

#### PKCS#1

PKCS#1 是专用于编码 RSA 公私钥的标准，通常被编码为 PEM 格式存储。openssl 生成的 RSA 密钥对默认使用此格式。

这是一个比较陈旧的格式，openssl 之所以默认使用它，主要是为了兼容性。通常建议使用更安全的 PKCS#8 而不是这个。

一个使用 PKCS#1 标准的 2048 位 RSA 公钥文件，内容如下：

```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyl6q6BkEcEUi9V1/Q7il
bngnh1YzG1tM4Hd6XCZQ35OzDN4my9eXWtjoL8YvLYqlYTJqhTHpuptgjF/lmlhg
WIMKNNcuDAbvmWExRyZateVrjO9OtgkyJCuGhaum0TIUC+dbZ9L9xsdK/fU1L5BB
nPRSYMloH8uE1CbK/DhFUiKp36aHZFfqLPicY3c6/N+k2kIJCEWBY0SROqpqy2Iz
yCIP54JSoOoGz6pdtWhd5cEeicr9e7f/WixEES6fgavqIHzhSJBVctpMgFPjFZ/x
JJhQVf23WKb3YQQ/0Uc8O7OTDXoUfuJP9UgqvKNh4hPfJA+a4nxkDYhTPfrLHfKY
YwIDAQAB
-----END PUBLIC KEY-----
```


#### PKCS#7 / CMS

>头疼...为什么这么多五花八门的格式...

[PKCS#7/CMS](https://datatracker.ietf.org/doc/html/rfc5652)，是一个多用途的证书描述格式。
它包含一个数据填充规则，这个填充规则常被用在需要数据填充的分组加密、数字签名等算法中。

另外据说 PKCS#7 也可以被用来描述证书，并以 DER/PEM 格式保存，后缀通常使用 `.p7b` 或者 `.p7c`,
这个暂时存疑吧，有需要再研究了。

#### PKCS#8

[PKCS#8](https://datatracker.ietf.org/doc/html/rfc5958) 是一个专门用于编码私钥的标准，可用于编码 DSA/RSA/ECC 私钥。它通常被编码成 PEM 格式存储。

前面介绍了专门用于编码 RSA 的 PKCS#1 标准比较陈旧，而且[曾经出过漏洞](https://web.archive.org/web/20081117042916/http://www.gemplus.com/smart/rd/publications/pdf/CJNP00pk.pdf)。因此通常建议使用更安全的 PKCS#8 来取代 PKCS#1.

C# Java 等编程语言通常要求使用此格式的私钥，而 Python 的 [pyca/cryptography](https://github.com/pyca/cryptography) 则支持多种编码格式。

一个非加密 ECC 私钥的 PKCS#8 格式如下：

```
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQglQanBRiYVPX7F2Rd
4CqyjEN0K4qfHw4tM/yMIh21wamhRANCAARsxaI4jT1b8zbDlFziuLngPcExbYzz
ePAHUmgWL/ZCeqlODF/l/XvimkjaWC2huu1OSWB9EKuG+mKFY2Y5k+vF
-----END PRIVATE KEY-----
```

一个加密 PKCS#8 私钥的 PEM 格式私钥如下：

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
Base64 编码内容
-----END ENCRYPTED PRIVATE KEY-----
```

可使用如下 openssl 命令将 RSA/ECC 私钥转换为 PKCS#8 格式：

```
# RSA
openssl pkcs8 -topk8 -inform PEM -in rsa-private-key.pem -outform PEM -nocrypt -out rsa-private-key-pkcs8.pem

# ECC 的转换命令与 RSA 完全一致
openssl pkcs8 -topk8 -inform PEM -in ecc-private-key.pem -outform PEM -nocrypt -out ecc-private-key-pkcs8.pem
```


#### PKCS#12

[PKCS#12](https://zh.wikipedia.org/wiki/PKCS_12) 是一个归档文件格式，用于实现存储多个私钥及相关的 X.509 证书。

因为保存了私钥，为了安全性它通常是加密的，需要使用 passphrase 解密后才能使用。

PKCS#12 的常用拓展名为 `.p12` `.pfx`.

PKCS#12 的主要使用场景是安全地保存、传输私钥及相关的 X.509 证书，比如：

- 微信/支付宝等支付相关的数字证书，通常使用 PKCS#12 格式存储，使用商户号做加密密码，然后编码为 base64 再提供给用户
- 安卓的 APK 签名证书通常使用 PKCS#12 格式存储，拓展名为 `.keystore` 或者 `.jks`.


PEM 格式转 PKCS#12（公钥和私钥都放里面）:

```shell
# 
openssl pkcs12 -export -in client.crt -inkey client.key -out client.p12
# 按提示输入保护密码
```

从 PKCS#12 中分别提取出 PEM 格式的公钥与私钥:

```shell
openssl pkcs12 -in xxx.p12 -out xxx.crt -clcerts -nokeys
openssl pkcs12 -in xxx.p12 -out xxx.key -nocerts -nodes
```


### 4. 证书支持保护的域名类型

TLS 证书支持配置多个域名，并且支持所谓的通配符（泛）域名。
但是通配符域名证书的匹配规则，**和 DNS 解析中的匹配规则并不一致**！

根据[证书选型和购买 - 阿里云文档](https://help.aliyun.com/document_detail/28542.html) 的解释，**通配符证书只支持同级匹配**，详细说明如下: 

1. **一级通配符域名**: 可保护该通配符域名（主域名）自身和该域名所有的一级子域名。
   - 例如: 一级通配符域名 `*.aliyun.com` 可以用于保护 `aliyun.com`、`www.aliyun.com` 以及其他所有一级子域名。
     但是不能用于保护任何二级子域名，如 `xx.aa.aliyun.com`
2. **二级或二级以上通配符域名**: 只能保护该域名同级的所有通配域名，不支持保护该通配符域名本身。
   - 例如: `*.a.aliyun.com` 只支持保护它的所有同级域名，不能用于保护三级子域名。

要想保护多个二三级子域，只能在生成 TLS 证书时，添加多个通配符域名。
因此设计域名规则时，要考虑到这点，尽量不要使用层级太深的域名！有些信息可以通过 `-` 来拼接以减少域名层级，比如阿里云的 oss 域名: 

1. 公网: `oss-cn-shenzhen.aliyuncs.com`
2. 内网: `oss-cn-shenzhen-internal.aliyuncs.com`

此外也可直接为 IP 地址签发证书，IP 地址可以记录在证书的 SAN 属性中。
在自己生成的证书链中可以为局域网 IP 或局域网域名生成本地签名证书。
此外在因特网中也有一些权威认证机构提供为公网 IP 签发证书的服务，一个例子是 Cloudflare 的 <https://1.1.1.1>, 使用 Firefox 查看其证书，可以看到是一个由 DigiCert 签发的 ECC 证书，使用了 P-256 曲线：

{{< figure src="/images/about-tls-cert/1.1.1.1-cert.webp" title=" Cloudflare 的 IP 证书" >}}

### 5. 生成自己的证书链

>[OpenSSL](https://github.com/openssl/openssl) 是目前使用最广泛的网络加密算法库，这里以它为例介绍证书的生成。
另外也可以考虑使用 CloudFalre 开源的 PKI 工具 [cfssl](https://github.com/cloudflare/cfssl).

前面介绍了，在局域网通信中通常使用本地证书链（**私有 PKI**）来保障通信安全，这通常有如下几个原因。

1. 在内网环境下，管理员将本地 CA 证书安装到所有局域网设备上，因此并无必要向权威 CA 机构申请证书
2. 内网环境使用的可能是非公网域名（`xxx.local`/`xxx.lan`/`xxx.srv` 等），甚至可能直接使用局域网 IP 通信，权威 CA 机构不签发这种类型的证书
3. 本地证书链完全受自己控制，可以自己设置安全强度、证书年限等等，而且不受权威 CA 机构影响。
4. 权威 CA 机构不签发客户端证书，因为客户端不一定有固定的 IP 地址或者域名。客户端证书需要自己签发。

下面介绍下如何使用 OpenSSL 生成一个本地 CA 证书链，并签发用于安全通信的服务端证书，可用于 HTTPS/QUIC 等协议。

#### 1. 生成 RSA 证书链

到目前为止 RSA 仍然是应用最广泛的非对称加密方案，几乎所有的根证书都是使用的 2048 位或者 4096 位的 RSA 密钥对。

对于 RSA 算法而言，越长的密钥能提供越高的安全性，当前使用最多的 RSA 密钥长度仍然是 2048 位，但是 2048 位已被一些人认为不够安全了，密码学家更建议使用 3072 位或者 4096 位的密钥。

生成一个 2048 位的 RSA 证书链的流程如下: 

>OpenSSL 的 CSR 配置文件官方文档: <https://www.openssl.org/docs/manmaster/man1/openssl-req.html>

1. 编写证书签名请求的配置文件 `csr.conf`:
    ```conf
    [ req ]
    prompt = no
    default_md = sha256  # 在签名算法中使用 SHA-256 计算哈希值
    req_extensions = req_ext
    distinguished_name = dn

    [ dn ]
    C = CN  # Contountry
    ST = Guangdong
    L = Shenzhen
    O = Xxx
    OU = Xxx-SRE
    CN = *.svc.local  # 泛域名，这个字段已经被 chrome/apple 弃用了。

    [ alt_names ]  # 备用名称，chrome/apple 目前只信任这里面的域名。
    DNS.1 = *.svc.local  # 一级泛域名
    DNS.2 = *.aaa.svc.local  # 二级泛域名
    DNS.3 = *.bbb.svc.local  # 二级泛域名

    [ req_ext ]
    subjectAltName = @alt_names

    [ v3_ext ]
    subjectAltName=@alt_names  # Chrome 要求必须要有 subjectAltName(SAN)
    authorityKeyIdentifier=keyid,issuer:always
    basicConstraints=CA:FALSE
    keyUsage=keyEncipherment,dataEncipherment,digitalSignature
    extendedKeyUsage=serverAuth,clientAuth
    ```
   - **此文件的详细文档**: [OpenSSL file formats and conventions](https://www.openssl.org/docs/man1.1.1/man5/)
2. 生成证书链与服务端证书: 
    ```shell
    # 1. 生成本地 CA 根证书的私钥
    openssl genrsa -out ca.key 2048
    # 2. 使用私钥签发出 CA 根证书
    ## CA 根证书的有效期尽量设长一点，因为不方便更新换代，这里设了 100 年
    openssl req -x509 -new -nodes -key ca.key -subj "/CN=MyLocalRootCA" -days 36500 -out ca.crt

    # 3. 生成服务端证书的 RSA 私钥（2048 位）
    openssl genrsa -out server.key 2048
    # 4. 通过第一步编写的配置文件，生成证书签名请求（公钥+申请者信息）
    openssl req -new -key server.key -out server.csr -config csr.conf
    # 5. 使用 CA 根证书直接签发服务端证书，这里指定服务端证书的有效期为 3650 天
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
      -CAcreateserial -out server.crt -days 3650 \
      -extensions v3_ext -extfile csr.conf
    ```

简单起见这里没有生成中间证书，直接使用根证书签发了用于安全通信的服务端证书。

#### 2. 生成 ECC 证书链

在上一篇文章中我们已经介绍过了，ECC 加密方案是新一代非对称加密算法，是 RSA 的继任者，在安全性相同的情况下，ECC 拥有比 RSA 更快的计算速度、更少的内存以及更短的密钥长度。

对于 ECC 加密方案而言，不同的椭圆曲线生成的密钥对提供了不同程度的安全性。
各个组织（ANSI X9.62、NIST、SECG）命名了多种曲线，可通过如下命名查看 openssl 支持的所有椭圆曲线名称: 

```shell
openssl ecparam -list_curves
```

目前在 TLS 协议以及 JWT 签名算法中，目前应该最广泛的椭圆曲线仍然是 NIST 系列：

- `P-256`: 到目前为止 P-256 应该仍然是应用最为广泛的椭圆曲线
  - 在 openssl 中对应的名称为 `prime256v1`
- `P-384`
  - 在 openssl 中对应的名称为 `secp384r1`
- `P-521`
  - 在 openssl 中对应的名称为 `secp521r1`

>此外还有新兴的 x25519 系列，这里不多介绍了，有兴趣可自行了解。

生成一个使用 `P-384` 曲线的 ECC 证书的示例如下: 

1. 编写证书签名请求的配置文件 `ecc-csr.conf`:
    ```conf
    [ req ]
    prompt = no
    default_md = sha256 # 在签名算法中使用 SHA-256 计算哈希值
    req_extensions = req_ext
    distinguished_name = dn

    [ dn ]
    C = CN  # Contountry
    ST = Guangdong
    L = Shenzhen
    O = Xxx
    OU = Xxx-SRE
    CN = *.svc.local  # 泛域名，这个字段已经被 chrome/apple 弃用了。

    [ alt_names ]  # 备用名称，chrome/apple 目前只信任这里面的域名。
    DNS.1 = *.svc.local  # 一级泛域名
    DNS.2 = *.aaa.svc.local  # 二级泛域名
    DNS.3 = *.bbb.svc.local  # 二级泛域名

    [ req_ext ]
    subjectAltName = @alt_names

    [ v3_ext ]
    subjectAltName=@alt_names  # Chrome 要求必须要有 subjectAltName(SAN)
    authorityKeyIdentifier=keyid,issuer:always
    basicConstraints=CA:FALSE
    keyUsage=keyEncipherment,dataEncipherment,digitalSignature
    extendedKeyUsage=serverAuth,clientAuth
    ```
   - **此文件的详细文档**: [OpenSSL file formats and conventions](https://www.openssl.org/docs/man1.1.1/man5/)
2. 生成证书链与服务端证书: 
    ```shell
    # 1. 生成本地 CA 根证书的私钥，使用 P-384 曲线，密钥长度 384 位
    openssl ecparam -genkey -name secp384r1 -out ecc-ca.key
    # 2. 使用私钥签发出 CA 根证书
    ## CA 根证书的有效期尽量设长一点，因为不方便更新换代，这里设了 100 年
    openssl req -x509 -new -nodes -key ecc-ca.key -subj "/CN=MyLocalRootCA" -days 36500 -out ecc-ca.crt

    # 3. 生成服务端证书的 EC 私钥，使用 P-384 曲线，密钥长度 384 位
    openssl ecparam -genkey -name secp384r1 -out ecc-server.key
    # 4. 通过第一步编写的配置文件，生成证书签名请求（公钥+申请者信息）
    openssl req -new -key ecc-server.key -out ecc-server.csr -config ecc-csr.conf
    # 5. 使用 CA 根证书直接签发 ECC 服务端证书，这里指定服务端证书的有效期为 3650 天
    openssl x509 -req -in ecc-server.csr -CA ecc-ca.crt -CAkey ecc-ca.key \
      -CAcreateserial -out ecc-server.crt -days 3650 \
      -extensions v3_ext -extfile ecc-csr.conf
    ```

简单起见这里没有生成中间证书，直接使用根证书签发了用于安全通信的服务端证书，而且根证书跟服务端证书都使用了 ECC 证书。
现实中由于根证书更新缓慢，几乎所有的根证书都还是 RSA 证书，而中间证书与终端实体证书的迭代要快得多，目前已经有不少网站在使用 ECC 证书了。


### 6. 证书的类型

按照数字证书的生成方式进行分类，证书有三种类型: 

1. **公网受信任证书** 或者叫 **Web PKI 证书**: 即由权威证书认证机构签名的的证书。
   - 几乎所有终端都预装了其的根证书，因此这类证书会被浏览器、小程序等第三方应用/服务商验证并信任。
   - 申请证书时需要验证你对域名/IP 的所有权，也就使证书无法伪造
   - 如果你的 API 需要提供给第三方应用/服务商/用户访问，那就需要向权威 CA 机构申请此类证书
2. **本地签名证书**: 即由本地 CA 证书签名的 TLS 证书
   - 本地 CA 证书，就是自己使用 `openssl` 等工具生成的 CA 证书
   - 这类证书的缺点是无法与第三方应用/服务商建立安全的连接
   - 如果客户端是完全可控的（比如是自家的 APP，或者是接入了域控的企业局域网设备），完全可以在所有客户端都安装上自己生成的 CA 证书。这种场景下使用此类证书是安全可靠的，可以不向权威 CA 机构申请证书
3. **自签名证书**: 前面介绍了根证书是一个自签名证书，它使用根证书的私钥为根证书签名
   - 这里的「自签名证书」是指**直接使用根证书进行网络通讯**，缺点是证书的更新迭代会很麻烦，而且安全性低。

总的来说，权威 CA 机构颁发的「公网受信任证书」，可以被第三方应用信任，但是自己生成的不行。
而越贵的权威证书，安全性与可信度就越高，或者可以保护更多的域名。

在客户端可控的情况下，可以考虑自己生成证书链并签发「本地签名证书」，将本地 CA 证书预先安装在客户端中用于验证。

而「自签名证书」主要是方便，能不用还是尽量不要使用。

### 7. 向权威 CA 机构申请「公网受信任证书」

向权威机构申请的公网受信任证书，可以直接应用在边界网关上，用于给公网用户提供 TLS 加密访问服务，比如各种 HTTPS 站点、API。这是需求最广的一类数字证书服务。

而证书的申请与管理方式又分为两种：

1. 通过 [ACMEv2（Automated Certificate Management Environment (ACME) ](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) 协议进行证书的自动化申请与管理。支持使用此开放协议申请证书的权威机构有：
  - 免费服务
    - Let's Encrypt: 众所周知，它提供三个月有效期的免费证书。
    - [ZeroSSL](https://zerossl.com/documentation/acme/):  貌似也是一个比较有名的 SSL 证书服务
      - 通过 ACME 协议支持不限数量的 90 天证书，也支持多域名证书与泛域名证书。
      - 它相比 Let's Encrypt 的优势是，它提供一个证书控制台，可以查看与管理用户当前的所有证书，了解其状态。
  - 付费服务
    - DigiCert: 这个非常有名（但也是相当贵），官方文档 [Digicert - Third-party ACME client automation](https://docs.digicert.com/certificate-tools/Certificate-lifecycle-automation-index/acme-user-guide/)
    - Google Trust Services: Google 推出的公网证书服务，也是三个月有效期，其根证书交叉验证了 GlobalSign。官方文档 [Automate Public Certificates Lifecycle Management via RFC 8555 (ACME)](https://cloud.google.com/blog/products/identity-security/automate-public-certificate-lifecycle-management-via--acme-client-api)
    - Entrust: 官方文档 [Entrust's ACME implementation](https://www.entrust.com/knowledgebase/ssl/how-to-use-acme-to-install-ssl-tls-certificates-in-entrust-certificate-services-apache#step1)
    - GlobalSign: 官方文档 [GlobalSign ACME Service](https://www.globalsign.com/en/acme-automated-certificate-management)
  - 相关的自动化工具
    - 很多代理工具都有提供基于 ACMEv2 协议的证书申请与自动更新，比如:
      - [Traefik](/network-proxy+web-server/traefik/README.md)
      - [Caddy](https://github.com/caddyserver/caddy)
      - [docker-letsencrypt-nginx-proxy-companion](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion)
    - **网上也有一些 [certbot](https://github.com/certbot/certbot) 插件，可以通过 DNS 提供商的 API 进行 ACMEv2 证书的申请与自动更新，比如**: 
      - [certbot-dns-aliyun](https://github.com/tengattack/certbot-dns-aliyun)
    - **terraform 也有相关 provider**: [terraform-provider-acme](https://github.com/vancluever/terraform-provider-acme)
    - [cert-manager](https://github.com/cert-manager/cert-manager): kubernetes 中的证书管理工具，支持 ACMEv2，也支持创建与管理私有证书。
1. 通过一些权威 CA 机构或代理商提供的 Web 网站，手动填写信息来申请与更新证书。
  - 这个流程相对会比较繁琐。

这些权威机构提供的证书服务，提供的证书又有不同的分级，这里详细介绍下三种不同的证书级别，以及该如何选用：

- Domain Validated（DV）证书
  - 应用最广泛的证书类型，我接触最多的就是这种。各云厂商提供的免费 SSL 证书也都是这种类型。
  - **仅验证域名所有权**，验证步骤最少，价格最低，仅需要数分钟即可签发。
  - 优点就是易于签发，很适合做自动化。
  - 各云厂商（AWS/GCP/Cloudflare，以及 Vercel/Github 的站点服务）给自家服务提供的免费证书都是 DV 证书，Let's Encrypt 的证书也是这个类型。
    - 很明显这些证书的签发都非常方便，而且仅验证域名所有权。
    - 但是 AWS/GCP/Cloudflare/Vercel/Github 提供的 DV 证书都仅能在它们的云服务上使用，不提供私钥导出功能！
- Organization Validated (OV) 证书
  - （貌似我也接触地比较少，不做评价）
  - 据说是企业 SSL 证书的首选，通过企业认证确保企业 SSL 证书的真实性。
  - 除域名所有权外，CA 机构还会审核组织及企业的真实性，包括注册状况、联系方式、恶意软件等内容。
  - 如果要做合规化，可能至少也得用 OV 这个级别的证书。
- Extended Validation（EV）证书
  - （我基本没接触过）
  - 最严格的认证方式，CA 机构会深度审核组织及企业各方面的信息。
  - 被认为适合用于大型企业、金融机构等组织或企业。
  - 而且仅支持签发单域名、多域名证书，不支持签发泛域名证书，安全性杠杠的。

完整的证书申请流程如下: 

![](/images/about-tls-cert/ca-sign-sechdule.webp "证书申请流程")

为了方便用户，图中的申请人（Applicant）自行处理的部分，目前很多证书申请网站也可以自动处理，用户只需要提供相关信息即可。

### 8. 证书的寿命

对于公开服务，服务端证书的有效期不要超过 825 天（27 个月）！
另外从 2020 年 11 月起，新申请的服务端证书有效期已经缩短到了 398 天（13 个月）。
目前 Apple/Mozilla/Chrome 都发表了相应声明，证书有效期超过上述限制的，将被浏览器/Apple设备禁止使用。

而对于其他用途的证书，如果更换起来很麻烦，可以考虑放宽条件。
比如 kubernetes 集群的加密证书，可以考虑有效期设长一些，比如 10 年。

据[云原生安全破局｜如何管理周期越来越短的数字证书？](https://mp.weixin.qq.com/s?__biz=MzA4MTQ2MjI5OA==&mid=2664079008&idx=1&sn=dede1114d5705880ea757f8d9ae4c92d)所述，大量知名企业如特斯拉/微软/领英/爱立信都曾因未及时更换 TLS 证书导致服务暂时不可用。

因此 TLS 证书最好是设置自动轮转！人工维护不可靠！

目前很多 Web 服务器/代理，都支持自动轮转 Let's Encrypt 证书。
另外 Vault 等安全工具，也支持自动轮转私有证书。

### 9. 使用 OpenSSL 验证证书、查看证书信息

```shell
# 查看证书(crt)信息
openssl x509 -noout -text -in server.crt

# 查看证书请求(csr)信息
openssl req -noout -text -in server.csr

# 查看 RSA 私钥(key)信息
openssl rsa -noout -text -in server.key

# 验证证书是否可信
## 1. 使用系统的证书链进行验证
openssl verify server.crt
## 2. 使用指定的 CA 证书进行验证
openssl verify -CAfile ca.crt server.crt
```

## 二、TLS 协议

TLS 协议，中文名为「传输层安全协议」，是一个安全通信协议，被用于在网络上进行安全通信。

TLS 协议通常与 HTTP / FTP / SMTP 等协议一起使用以实现加密通讯，这种组合协议通常被缩写为 HTTPS / SFTP / SMTPS.

在讲 [TLS 协议](https://zh.wikipedia.org/wiki/%E5%82%B3%E8%BC%B8%E5%B1%A4%E5%AE%89%E5%85%A8%E6%80%A7%E5%8D%94%E5%AE%9A)前，还是先复习下「对称密码算法」与「非对称密码算法」两个密码体系的特点。

- **对称密码算法（如 AES/ChaCha20）**: 计算速度快、安全强度高，但是缺乏安全交换密钥的手段、密钥的保存和管理也很困难
- **非对称密码算法（如 RSA/ECC）**: 解决了上述对称密码算法的两个缺陷——通过数字证书 + PKI 公钥基础架构实现了身份认证，再通过 DHE/ECDHE 实现了安全的对称密钥交换。

但是非对称密码算法要比对称密码算法更复杂，计算速度也慢得多。
因此实际使用上通常结合使用这两种密码算法，各取其长，以实现高速且安全的网络通讯。
我们通常称结合使用对称密码算法以及非对称密码算法的加密方案为「混合加密方案」。

TLS 协议就是一个「混合加密方案」，它借助数字证书与 PKI 公钥基础架构、DHE/ECDHE 密钥交换协议以及对称加密方案这三者，实现了安全的加密通讯。

基于经典 DHKE 协议的 TLS 握手流程如下：

![](/images/about-tls-cert/tls-handshake.webp "基于经典 DHKE 协议的 TLS 握手")

而在支持「完美前向保密（Perfect Forward Secrecy）」的 TLS1.2 或 TLS1.3 协议中，经典 DH 协议被 ECDHE 协议取代。
变化之一是进行最初的握手协议从经典 DHKE 换成了基于 ECC 的 ECDH 协议，
变化之二是在每次通讯过程中也在不断地进行密钥交换，生成新的对称密钥供下次通讯使用，其细节参见 [写给开发人员的实用密码学（五）—— 密钥交换 DHKE 与完美前向保密 PFS](/posts/practical-cryptography-basics-5-key-exchange/)。

TLS 协议通过应用 ECDHE 密钥交换协议，提供了「完美前向保密（Perfect Forward Secrecy）」特性，也就是说它能够保护过去进行的通讯不受密钥在未来暴露的威胁。
即使攻击者破解出了一个「对称密钥」，也只能获取到一次事务中的数据，其他事务的数据安全性完全不受影响。

另外注意一点是，CA 证书和服务端证书都只在 TLS 协议握手的前三个步骤中有用到，之后的通信就与它们无关了。

### 1. 密码套件与 TLS 历史版本


[密码套件（Cipher_suite）](https://en.wikipedia.org/wiki/Cipher_suite)是 TLS 协议中一组用于实现安全通讯的密码学算法，类似于我们前面学习过的加密方案。
不同密码学算法的组合形成不同的密码套件，算法组合的差异使这些密码套件具有不同的性能与安全性，另外 TLS 协议的更新迭代也导致各密码套件拥有不同的兼容性。
通常越新推出的密码套件的安全性越高，但是兼容性就越差（旧设备不支持）。

密码套件的名称由它使用的各种密码学算法名称组成，而且有固定的格式，以 `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` 为例介绍下：

- `TLS`: 定义了此套件适用的协议，通常固定为 `TLS`
- `ECDHE`: 密钥交换算法
- `RSA`: 数字证书认证算法
- `AES_128_GCM`: 使用的对称加密方案，这是一个基于 AES 与 GCM 模式的对称认证加密方案，使用 128 位密钥
- `SHA256`: 哈希函数，用于 HMAC 算法实现消息认证
  - TLS 固定使用 HMAC 算法进行消息认证

TLS 协议的前身是 SSL 协议，TLS/SSL 的发展历程展示如下：

{{< figure src="/images/about-tls-cert/history-of-ssl-tls.webp" title="SSL/TLS 的历史版本" >}}

SSL 协议早在 2015 年就被各大主流浏览器废除了，TLS1.0 感觉也基本没站点在用了，这俩就直接跳过了。

下面分别介绍下 TLS1.1 TLS1.2 与 TLS1.3.

#### TLS 1.1

TLS 1.1 在 RFC4346 中定义，于 2006 年 4 月发布。

TLS 1.1 是 TLS 1.0 的一个补丁，主要更新包括：

- 添加对CBC攻击的保护
  - 隐式初始向量 IV 被替换成一个显式的 IV
  - 修复分组密码模式中填充算法的 bug
- 支持 IANA 登记的参数

**TLS 1.1**及其之前的算法曾经被广泛应用，它目前已知的缺陷如下：

- 不支持 PFS 完全前向保密
- 不支持 AEAD 认证加密算法
- 为了兼容性，保留了很多不安全的算法

TLS 1.1 已经不够安全了，不过一些陈年老站点或许还在使用它。

各操作系统（Android/IOS/MacOS/Windows）与浏览器基本都在很早的版本中就已经支持 TLS1.2+ 了，站在 2022 年这个时间节点看，我们已经可以完全废止 TLS1.1 协议。
实际上各大云厂商也是这么干的，比如 AWS 自身的 API 对 TLS1.1 的支持就已确定将在 2023 年 6 月废止，2022 年就开始频繁扫描并提醒各位仍然在使用低版本 TLS 协议的客户升级。

#### TLS 1.2

TLS 1.2 在 RFC5246 中定义，于 2008 年 8 月发发布。

- 可选支持 PFS 完全前向保密
- 移除对 MD5 与 SHA-1 签名算法的支持
- 添加对 HMAC-SHA-256 及 HMAC-SHA-384 消息认证算法的支持
- 添加对 AEAD 加密认证方案的支持
- 去除 forback 回到 SSL 协议的能力，提升安全性
- 为了兼容性，保留了很多不安全的算法

如果你使用 TLS 1.2，需要小心地选择密码套件，避开不安全的套件，就能实现足够高的安全性。

#### TLS 1.3

[TLS 1.3](https://blog.cloudflare.com/rfc-8446-aka-tls-1-3/) 做了一次大刀阔斧的更新，是一个里程碑式的版本，其更新总结如下：

- 移除对如下算法的支持
  - 哈希函数 SHA1/MD5
  - 所有非 AEAD 加密认证的密码方案（CBC 模式）
  - 移除对 RC4 与 3DES 加密算法的支持
  - 移除了静态 RSA 与 DH 密钥交换算法
- 支持高性能的 Ed25519/Ed448 签名认证算法、X25519 密钥协商算法
- 支持高性能的 ChaCha20-Poly1305 对称认证加密方案
- 将密钥交换算法与公钥认证算法从密码套件中分离出来
  - 比如原来的 `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` 密码套件将被拆分为 `ECDHE` 算法、`RSA` 身份认证算法、以及 `TLS_AES_128_GCM_SHA256` 密码套件
  - 这样密码套件就只包含一个 AEAD 认证加密方案，以及一个哈希函数了
- 仅支持前向安全的密钥交换算法 DHE 或 ECDHE
- 支持最短 0-RTT 的 TLS 握手（会话恢复）

TLS 1.3 从协议中删除了所有不安全的算法或协议，可以说只要你的通讯用了 TLS 1.3，那你的数据就安全了（当然前提是你的私钥没泄漏）。

#### 如何设置 TLS 协议的版本、密码套件参数

我们前面已经学习了对称加密、非对称加密、密钥交换三部分知识，对照 TLS 套件的名称，应该能很容易判断出哪些是安全的、哪些不够安全，哪些支持前向保密、哪些不支持。

一个非常好用的「站点 HTTPS 安全检测」网站是 <https://myssl.com/>，使用它测试知乎网的检测结果如下：

{{< figure src="/images/about-tls-cert/tls-cipher.webp" title="SSL/TLS 的历史版本" >}}

能看到知乎为了兼容性，目前仍然支持 TLS1.0 与 TLS1.1，另外目前还不支持 TLS1.3.

此外，知乎仍然支持很多已经不安全的加密套件，myssl.com 专门使用黄色标识出了这些不安全的加密套件，我们总结下主要特征：

- 部分密码套件使用了不安全的对称加密算法 `3DES`
- 其他被标识为黄色的套件虽然使用了安全的对称加密算法，但是不支持 PFS 前向保密

此外 myssl.com 还列出了许多站点更详细的信息，包括 TLS1.3 的会话恢复，以及后面将会介绍的公钥固定、HTTP严格传输安全等信息：

{{< figure src="/images/about-tls-cert/other-https-info.webp" title="SSL/TLS 的历史版本" >}}


##### Nginx 的 TLS 协议配置

以前为 Nginx 等程序配置 HTTPS 协议时，我最头疼的就是其中密码套件参数 `ssl_ciphers`，为了安全性，需要配置超长的一大堆选用的密码套件名称，我可以说一个都看不懂，但是为了把网站搞好还是得硬着头皮搜索复制粘贴，实际上也不清楚安全性到底如何。

为了解决这个问题，Mozilla/DigitalOcean 都搞过流行 Web 服务器的 TLS 配置生成工具，比如 **[ssl-config - mozilla](https://ssl-config.mozilla.org/#server=nginx)，这个网站提供三个安全等级的配置**: 

1. 「Intermediate」: 查看生成出的 `ssl-cipher` 属性，发现它只支持 `ECDHE`/`DHE` 开头的算法。因此它保证前向保密。
   - 对于需要通过浏览器访问的 API，推荐选择这个等级。
2. 「Mordern」: 只支持 `TLSv1.3`，该协议废弃掉了过往所有不安全的算法，保证前向保密，安全性极高，性能也更好。
   - 对于不需要通过浏览器等旧终端访问的 API，请直接选择这个等级。
3. 「Old」: 除非你的用户使用非常老的终端进行访问，否则请不要考虑这个选项！

可以点进去查看详细的 TLS 套件配置。

#### OCSP 证书验证协议

>https://www.ssl.com/blogs/how-do-browsers-handle-revoked-ssl-tls-certificates/

>https://imququ.com/post/why-can-not-turn-on-ocsp-stapling.html

>https://www.digicert.com/help/

前面提到除了数字证书自带的有效期外，为了在私钥泄漏的情况下，能够吊销对应的证书，PKI 公钥基础设施还提供了 OCSP（Online Certificate Status Protocol）证书状态查询协议。

可以使用如下命令测试，确认站点是否启用了 ocsp stapling:

```conf
$ openssl s_client -connect www.digicert.com:443 -servername www.digicert.com -status -tlsextdebug < /dev/null 2>&1 | grep -i "OCSP response"
```

如果输出包含 `OCSP Response Status: successful` 就说明站点支持 ocsp stapling，
如果输出内容为 `OCSP response: no response sent` 则说明站点不支持ocsp stapling。

>实际上 Google/AWS 等大多数站点都不会启用也不需要启用 ocsp stapling，一是因为它们自己就是证书颁发机构，OCSP 服务器也归它们自己管，不存在隐私的问题。二是它们的 OCSP 服务器遍布全球，也不存在性能问题。
这种情况下开个 OCSP Stapling 反而是浪费流量，因为每次 TLS 握手都得发送一个 OCSP 状态信息。

>我测试发现只有 www.digicert.com/www.douban.com 等少数站点启用了 ocsp stapling，www.baidu.com/www.google.com/www.zhihu.com 都未启用 ocsp stapling.

这导致了一些问题：

- Chrome/Firefox 等浏览器都会定期通过 OCSP 协议去请求 CA 机构的 OCSP 服务器验证证书状态，这可能会拖慢 HTTPS 协议的响应速度。
  - 所谓的定期是指超过上一个 OCSP 响应的 `nextUpdate` 时间（一般为 7 天），或者如果该值为空的话，Firefox 默认 24h 后会重新查询 OCSP 状态。
- 因为客户端直接去请求 CA 机构的 OCSP 地址获取证书状态，这就导致 CA 机构可以获取到一些对应站点的用户信息（IP 地址、网络状态等）。
- 如果因为某些原因导致客户端无法访问 OCSP 服务器，会导致站点的初次访问时间用时变得很长。因为浏览器会每隔一阵时间就重新尝试去访问 OCSP 服务器！
  - 一个典型的例子就是 [提高https载入速度，记一次nginx升级优化](https://www.hawu.me/operation/2129)，因为 Let's Encrypt 的 OCSP 服务器被 GFW 屏蔽，导致国内使用该证书的站点首次访问速度非常慢。

为了解决这两个问题，[rfc6066](https://www.rfc-editor.org/rfc/rfc6066) 定义了 OCSP stapling 功能，它使服务器可以提前访问 OCSP 获取证书状态信息并缓存到本地。

在客户端使用 TLS 协议访问 HTTPS 服务时，服务端会直接在握手阶段将缓存的 OCSP 信息发送给客户端。
因为 OCSP 信息会带有 CA 证书的签名及有效期，客户端可以直接通过签名验证 OCSP 信息的真实性与有效性，这样就避免了客户端访问 OCSP 服务器带来的开销。

对于 Let's Encrypt 的 OCSP 服务器被 GFW 屏蔽这样的场景，开不开 OCSP Stapling 对站点访问速度的影响就会变得非常地大！

#### ALPN 应用层协议协商

>https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation

>https://imququ.com/post/enable-alpn-asap.html

TODO

### 2. mTLS 双向认证

TLS 协议（tls1.0+，RFC: [TLS1.2 - RFC5246](https://tools.ietf.org/html/rfc5246#section-7.4.4)）也定义了可选的服务端请求验证客户端证书的方法。这
个方法是可选的。如果使用上这个方法，那客户端和服务端就会在 TLS 协议的握手阶段进行互相认证。这种验证方式被称为双向 TLS 认证(mTLS, mutual TLS)。

传统的「TLS 单向认证」技术，只在客户端去验证服务端是否可信。
而「TLS 双向认证（mTLS）」，则添加了服务端验证客户端是否可信的步骤（第三步）: 

1. 客户端发起请求
2. 「验证服务端是否可信」: 服务端将自己的 TLS 证书发送给客户端，客户端通过自己的 CA 证书链验证这个服务端证书。
3. 「验证客户端是否可信」: 客户端将自己的 TLS 证书发送给服务端，服务端使用它的 CA 证书链验证该客户端证书。
4. 协商对称加密算法及密钥
5. 使用对称加密进行后续通信。

因为相比传统的 TLS，mTLS 只是添加了「验证客户端」这样一个步骤，所以这项技术也被称为「Client Authetication」.

mTLS 需要用到两套 TLS 证书: 

1. 服务端证书: 这个证书的内容以及申请流程，前面介绍过了。
2. 客户端证书: 客户端证书貌似对证书信息（如 CN/SAN 域名）没有任何要求，只要证书能通过服务端的 CA 签名验证就行。

使用 openssl 生成 TLS 客户端证书（ca 和 csr.conf 可以直接使用前面生成服务端证书用到的，也可以另外生成）: 

```shell
# 1. 生成 2048 位 的 RSA 密钥
openssl genrsa -out client.key 2048
# 2. 通过第一步编写的配置文件，生成证书签名请求
openssl req -new -key client.key -out client.csr -config csr.conf
# 3. 生成最终的证书，这里指定证书有效期 3650 天
### 使用前面生成的 ca 证书对客户端证书进行签名（客户端和服务端共用 ca 证书）
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
   -CAcreateserial -out client.crt -days 3650 \
   -extensions v3_ext -extfile csr.conf
```

mTLS 的应用场景主要在「零信任网络架构」，或者叫「无边界网络」中。
比如微服务之间的互相访问，就可以使用 mTLS。
这样就能保证每个 RPC 调用的客户端，都是其他微服务（或者别的可信方），防止黑客入侵后为所欲为。


目前查到如下几个Web服务器/代理支持 mTLS:

1. Traefik: [Docs - Client Authentication (mTLS)](https://docs.traefik.io/v2.0/https/tls/#client-authentication-mtls)
2. Nginx: [Using NGINX Reverse Proxy for client certificate authentication](https://community.openhab.org/t/using-nginx-reverse-proxy-for-client-certificate-authentication-start-discussion/43064)
   1. 主要参数是两个: `ssl_client_certificate /etc/nginx/client-ca.pem` 和 `ssl_verify_client on`


#### mTLS 的安全性

如果将 mTLS 用在 App 安全上，存在的风险是: 

1. 客户端中隐藏的证书是否可以被提取出来，或者黑客能否 Hook 进 App 中，直接使用证书发送信息。
2. 如果客户端私钥设置了「密码（passphrase）」，那这个密码是否能很容易被逆向出来？

mTLS 和「公钥锁定/证书锁定」对比: 

1. 公钥锁定/证书锁定: 只在客户端进行验证。
   1. 但是在服务端没有进行验证。这样就无法鉴别并拒绝第三方应用（爬虫）的请求。
   2. 加强安全的方法，是通过某种算法生成动态的签名。爬虫生成不出来这个签名，请求就被拒绝。
2. mTLS: 服务端和客户端都要验证对方。
   1. 保证双边可信，在客户端证书不被破解的情况下，就能 Ban 掉所有的爬虫或代理技术。


### 3. 其他加密通讯协议

#### SSH 协议

首先最容易想到的应该就是是 SSH 协议（Secure SHell protocol）。SSH 与 TLS 一样都能提供加密通讯，是 PKI 公钥基础设施的早期先驱者之一。

SSH 协议应用最广泛的实现是 OpenSSH，它使用 SSH Key 而非数字证书进行身份认证，这主要是因为 OpenSSH 仅用于用户与主机之间的安全通信，不需要记录 X.509 这么繁多的信息。

我们来手动生成个 OpenSSH ed25519 密钥对试试（RSA 的生成命令完全类似）：

```shell
❯ ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (/Users/admin/.ssh/id_ed25519): ed25519-key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in ed25519-key.
Your public key has been saved in ed25519-key.pub.
The key fingerprint is:
SHA256:jgeuWVflhNXXrDDzUtW6ZV1lpBWNAj0Rstizh9Lbyg0 admin@ryan-MacBook-Pro.local
The key's randomart image is:
+--[ED25519 256]--+
|          oo++ *%|
|         o =B ++B|
|        . = oO.+o|
|         . B. + +|
|      . S = o. + |
|     . + o +  .  |
|      + + E .    |
|     + o . +     |
|    o     o .    |
+----[SHA256]-----+

❯ cat ed25519-key    
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDux4KnrKXVs4iR9mPZnSpur5207ceyMiZP+CDnXdooMQAAAKDnHOSY5xzk
mAAAAAtzc2gtZWQyNTUxOQAAACDux4KnrKXVs4iR9mPZnSpur5207ceyMiZP+CDnXdooMQ
AAAEADkVL1gZHAvBx4M5+UjVVL7ltVOC4r9tdR23CoI9iV1O7HgqespdWziJH2Y9mdKm6v
nbTtx7IyJk/4IOdd2igxAAAAHGFkbWluQHJ5YW4tTWFjQm9vay1Qcm8ubG9jYWwB
-----END OPENSSH PRIVATE KEY-----

❯ cat ed25519-key.pub 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO7HgqespdWziJH2Y9mdKm6vnbTtx7IyJk/4IOdd2igx admin@ryan-MacBook-Pro.local
```

可以看到 SSH Key 的结构非常简单，仅包含如下三个部分：

- 密钥对类型: 最常见的是 `ssh-rsa`，另外由于安全性目前更推荐使用 `ssh-ed25519`
- 公钥的 Base64 字符串
- 一个 Comment，通常包含这个 Key 的用途，或者 Key 所有者的邮箱地址

通过我们前面学的非对称密码学知识可以知道，公钥能直接从私钥生成，假设你的 ssh 公钥丢失，可以通过如下命令重新生成出公钥：

```shell
ssh-keygen -y -f xxx_rsa > xxx_rsa.pub
```

#### HTTP/3 与 QUIC 协议

[QUIC 协议](https://github.com/quicwg)，是 Google 研发并推动标准化的 TCP 协议的替代品， QUIC 是基于 UDP 协议实现的。基于 QUIC 提出的 HTTP over QUIC 协议已被标准化为 [RFC 9114 - HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)，它做了很多大刀阔斧的改革：

- 传输层协议从 TCP 改成了 UDP，QUIC 自己实现的数据的可靠传输、按序到达、拥塞控制
  - 也就是说 QUIC 绕过了陈旧的内核 TCP 协议实现，直接在用户空间实现了这些功能
  - 通过另起炉灶，它解决了一些 TCP 协议的痛点：队头阻塞、握手延迟高、特性迭代慢、拥塞控制算法不佳等问题
- 在 TLS1.3 出现之前，QUIC 实现了自己的加密方案 [QUIC Crypto](https://docs.google.com/document/d/1g5nIXAIkN_Y-7XJW5K45IblHd_L2f5LTaDUDwvZ5L6g/edit) 以取代陈旧的 TLS 协议，同时兼容现有的数字证书体系
  - QUIC Crypto 的特点是它直接在应用层进行加密通讯的握手，并且恢复通信时可以通过缓存实现 0RTT 握手
  - 也就说 QUIC 通过另起炉灶，解决了 TLS 的安全问题，以及握手延迟高的问题

总结一下就是，旧的实验性 HTTP-over-QUIC 协议，重新实现了 HTTP+TLS+TCP 三种协议并将它们整合到一起，这带来了极佳的性能，但也使它变得非常复杂。

QUIC 的 0RTT 握手是一个非常妙的想法，可以显著降低握手时延，TLS1.3 的设计者们将它纳入了 TLS1.3 标准中。

由于 TLS1.3 的良好特性，在 TLS1.3 协议发布后，新的 QUIC 标准 [RFC 9001](https://datatracker.ietf.org/doc/html/rfc9001) 已经使用 TLS1.3 取代了实验阶段使用的 QUIC Crypto 加密方案，目前只有 Chromium/Chrome 仍然支持 QUIC Crypto，其他 QUIC 实现基本都只支持 TLS1.3, 详见 [QUIC Implementations](https://github.com/quicwg/base-drafts/wiki/Implementations).

### 4. TLS 协议攻防战


#### 1. 证书锁定（Certifacte Pining）技术

即使使用了 TLS 协议对流量进行加密，并且保证了前向保密，也无法保证流量不被代理！

这是因为客户端大多是直接依靠了操作系统内置的 CA 证书库进行证书验证，而 Fiddler 等代理工具可以将自己的 CA 证书添加到该证书库中。

为了防止流量被 Fiddler 等工具使用上述方式监听流量，出现了「证书锁定（Certifacte Pining, 或者 SSL Pinning）」技术。
方法是在客户端中硬编码证书的指纹（Hash值，或者直接保存整个证书的内容也行），在建立 TLS 连接前，先计算使用的证书的指纹是否匹配，否则就中断连接。

这种锁定方式需要以下几个前提才能确保流量不被监听: 

1. 客户端中硬编码的证书指纹不会被篡改。
2. 指纹验证不能被绕过。
   1. 目前有公开技术（XPosed+JustTrustMe）能破解 Android 上常见的 HTTPS 请求库，直接绕过证书检查。
   2. 针对上述问题，可以考虑加大绕过的难度。或者 App 检测自己是否运行在 Xposed 等虚拟环境下。
3. 用于 TLS 协议的证书不会频繁更换。（如果更换了，指纹就对不上了。）

而对于第三方的 API，因为我们不知道它们会不会更换 TLS 证书，就不能直接将证书指纹硬编码在客户端中。
这时可以考虑从服务端获取这些 API 的证书指纹（附带私钥签名用于防伪造）。

为了实现证书的轮转(rotation)，可以在新版本的客户端中包含多个证书指纹，这样能保证同时有多个可信证书，达成证书的轮转。（类比 JWT 的公钥轮转机制）

>证书锁定技术几乎等同于 SSH 协议的 `StrictHostKeyChecking` 选项，客户端会验证服务端的公钥指纹（key fingerprint），验证不通过则断开连接。


#### 2. 公钥锁定（Public Key Pining）技术

前面介绍过证书的结构，它其实包含了公钥、有效期与一系列的其他信息。
使用了证书锁定技术，会导致证书的有效期也被锁定，APK 内的证书指纹就必须随着证书一起更新。

更好的做法是仅锁定证书中的公钥，即「公钥锁定」技术。
「公钥锁定」比「证书锁定」更灵活，这样证书本身其实就可以直接轮转了（证书有过期时间），而不需要一个旧证书和新证书共存的中间时期。

**「公钥锁定」是更推荐的锁定技术**。

#### 3. HTTPS 严格传输安全 - HSTS

HSTS，即 HTTP Strict Transport Security，是一项安全技术，它允许服务端在返回 HTTPS 响应时，通过 Headers 明确要求客户端，在之后的一段时间内必须使用安全的 HTTPS 协议访问服务端。

举个例子，假设站点 `https://example.com/` 的响应头中有 `Strict-Transport-Security: max-age=31536000; includeSubDomains`，这表示服务端要求客户端（比如浏览器）：

- 在接下来的 31536000 秒（即一年）中，客户端向 example.com 或**其子域名**发送 HTTP 请求时，必须采用HTTPS来发起连接。
  - 比如用户在浏览器地址栏输入 `http://example.com/` 时，浏览器应自动将 http 改写为 https 再发起请求
- 在接下来的 31536000 秒（即一年）中，如果 example.com 服务器提供的证书无效，用户不能忽略浏览器的证书警告继续访问网站。
  - 也就是说一旦证书失效，站点将完全无法访问，直至服务端修复证书问题。
  - 一旦证书失效，HTTPS 其实就不是严格安全的了，可能会遭遇中间人攻击。也就是说 HSTS 通过牺牲站点的可访问性来避免中间人攻击。

#### 4. TLS 协议的逆向手段

要获取一个应用的 HTTPS 数据，有两个方向: 

1. 服务端入侵: 现代应用的服务端突破难度通常都比较客户端高，注入等漏洞底层框架就有处理。
   1. 不过如果你获得了服务器 root 权限，可以在 openssl 上做文章，比如篡改 openssl？
2. 客户端逆向+爬虫: 客户端是离用户最近的地方，也是最容易被突破的地方。
   1. mTLS 常见的破解手段，是找到老版本的安装包，发现很容易就能提取出客户端证书。。

>wiki 列出了一些 TLS 协议的安全问题：https://en.wikipedia.org/wiki/Transport_Layer_Security#Security

TO BE DONE...


### 5. 在边缘侧卸载 TLS

TLS 加密是一个安全协议，工程上虽然有 Google 等公司力推所谓「零信任加密」方案，在所有通信场景下都应用 mTLS 等加密技术。
但是为了成本与性能考量，绝大部分公司都选择仅在公网使用 HTTPS，在可信内网场景下使用纯 HTTP。其做法就是在边缘网关层卸载 TLS 协议，再将内部的 HTTP 请求负载均衡到后端服务上。

所谓卸载 TLS 协议，就是指它对外提供 TLS 协议端口，但是使用 HTTP 等裸协议与上游服务通信。

在边缘侧卸载 HTTPS 的好处主要有：

- 内网环境都使用了纯 HTTP，性能更好，延迟更低，成本更低。
- 参见 [一篇讲 TLS 的好文分享](https://0xffff.one/d/968-yi-pian-jiang-tls-de-hao-wen-fen)，如果通过 CDN 在边缘节点卸载 TLS，然后使用纯 HTTP 回源，能显著降低请求延迟。
  - 我本人就于 2022 年，在 AWS 上通过这个手段优化了一波广告业务 API 的延迟，广告收益有明显上涨。


## 三、参考

- [HTTPS 温故知新（三） —— 直观感受 TLS 握手流程(上)](https://halfrost.com/https_tls1-2_handshake/)
- [HTTPS 温故知新（五） —— TLS 中的密钥计算](https://halfrost.com/https-key-cipher/)
- [A complete overview of SSL/TLS and its cryptographic system](https://dev.to/techschoolguru/a-complete-overview-of-ssl-tls-and-its-cryptographic-system-36pd)

- [Certificates - Kubernetes Docs](https://kubernetes.io/docs/concepts/cluster-administration/certificates/)
- [证书选型和购买 - 阿里云文档](https://help.aliyun.com/document_detail/28542.html)
- [云原生安全破局｜如何管理周期越来越短的数字证书？](https://mp.weixin.qq.com/s?__biz=MzA4MTQ2MjI5OA==&mid=2664079008&idx=1&sn=dede1114d5705880ea757f8d9ae4c92d)

另外两个关于 CN(Common Name) 和 SAN(Subject Altnative Name) 的问答: 

- [Can not get rid of `net::ERR_CERT_COMMON_NAME_INVALID` error in chrome with self-signed certificates](https://serverfault.com/questions/880804/can-not-get-rid-of-neterr-cert-common-name-invalid-error-in-chrome-with-self)
- [SSL - How do Common Names (CN) and Subject Alternative Names (SAN) work together?](https://stackoverflow.com/questions/5935369/ssl-how-do-common-names-cn-and-subject-alternative-names-san-work-together)

关于证书锁定/公钥锁定技术: 

- [Certificate and Public Key Pinning - OWASP](https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning)
- [Difference between certificate pinning and public key pinning](https://security.stackexchange.com/questions/85209/difference-between-certificate-pinning-and-public-key-pinning)


其他推荐读物: 

- [图解密码技术 - [日]结城浩](https://book.douban.com/subject/26822106/)
- [给工程师：关于证书（certificate）和公钥基础设施（PKI）的一切](https://mp.weixin.qq.com/s/li3ZjfNgX5nh7AKjyyzt5A)
