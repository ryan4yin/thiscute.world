---
title: "JWT 签名算法 HS256、RS256 及 ES256 及密钥生成"
date: 2020-03-03T14:09:46+08:00
draft: false

featuredImage: "jwt.webp"
resources:
  - name: featured-image
    src: "jwt.webp"
authors: ["ryan4yin"]

series: ["写给开发人员的实用密码学"]

tags: ["JWT", "算法", "OpenSSL"]
categories: ["tech"]
---

# 签名算法

介绍具体的 JWT 签名算法前，先解释一下签名、摘要/指纹、加密这几个名词的含义：

1. 数字签名(Digital Signature): 就和我们日常办理各种手续时需要在文件上签上你自己的名字一
   样，数字签名的主要用途也是用于身份认证。
   1. 更准确的讲，数字签名可保证数据的三个特性：真实性（未被伪造）、完整性（不存在缺失）、
      不可否认性（确实是由你本人认可并签名）
2. 数字摘要(digest)/数字指纹(fingerprint): 指的是数据的 Hash 值。
3. 加密算法：这个应该不需要解释，就是对数据进行加密。。

数字签名的具体实现，通常是先对数据进行一次 Hash 摘要(SHA1/SHA256/SHA512 等)，然后再使用非
对称加密算法(RSA/ECDSA 等)的私钥对这个摘要进行加密，这样得到的结果就是原始数据的一个签名。

用户在验证数据时，只需要使用公钥解密出 Hash 摘要，然后自己再对数据进行一次同样的摘要，对比
两个摘要是否相同即可。

> 注意：签名算法是使用私钥加密，确保得到的签名无法被伪造，同时所有人都可以使用公钥解密来验
> 证签名。这和正常的数据加密算法是相反的。（非对称加密算法支持使用密钥对的任何一个加密数
> 据，再用另一个密钥解密）

因为数字签名多了非对称加密这一步，就能保证只有拥有私钥的人才能生成出正确的数字签名，达到了
防止伪造签名的目的。而数字摘要（Hash）则谁都可以计算出来，通常**由可信方公布数据的 Hash
值**，用户下载数据后，可通过 Hash 值对比来判断数据是否损坏，或者被人调包。

重点在于，Hash 摘要必须由可信方公布出来，否则不能保证安全性。而数字签名可以随数据一起提
供，不需要担心被伪造。

JWT 是签名和数据一起提供的，因此必须使用签名才能保证安全性。

> P.S. 在 Android/IOS 开发中，经常会遇到各类 API 或者 APP 商店要求提供 APP 的签名，还指明
> 需要的是 MD5/SHA1 值。这个地方需要填的 MD5/SHA1 值，实际上只是你「签名证书(=公钥+证书拥
> 有者信息)」的「数字指纹/摘要」，和 JWT 的签名不是一回事。

# 前言

JWT 规范的详细说明请见「参考」部分的链接。这里主要说明一下 JWT 最常见的几种签名算法
(JWA)：HS256(HMAC-SHA256) 、RS256(RSA-SHA256) 还有 ES256(ECDSA-SHA256)。

这三种算法都是一种消息签名算法，得到的都只是一段无法还原的签名。区别在于**消息签名**与**签
名验证**需要的 「key」不同。

1. HS256 使用同一个「secret_key」进行签名与验证（对称加密）。一旦 secret_key 泄漏，就毫无
   安全性可言了。
   - 因此 HS256 只适合集中式认证，签名和验证都必须由可信方进行。
   - 传统的单体应用广泛使用这种算法，但是请不要在任何分布式的架构中使用它！
1. RS256 是使用 RSA 私钥进行签名，使用 RSA 公钥进行验证。公钥即使泄漏也毫无影响，只要确保
   私钥安全就行。
   - RS256 可以将验证委托给其他应用，只要将公钥给他们就行。
1. ES256 和 RS256 一样，都使用私钥签名，公钥验证。算法速度上差距也不大，但是它的签名长度相
   对短很多（省流量），并且算法强度和 RS256 差不多。

对于单体应用而言，HS256 和 RS256 的安全性没有多大差别。而对于需要进行多方验证的微服务架构
而言，显然只有 RS256/ES256 才能提供足够的安全性。在使用 RS256 时，只有「身份认证的微服务
(auth)」需要用 RSA 私钥生成 JWT，其他微服务使用公开的公钥即可进行签名验证，私钥得到了更好
的保护。

更进一步，「JWT 生成」和「JWT 公钥分发」都可以直接委托给第三方的通用工具，比如
[hydra](https://github.com/ory/hydra)。甚至「JWT 验证」也可以委托给「API 网关」来处理，应
用自身可以把认证鉴权完全委托给外部的平台，而应用自身只需要专注于业务。这也是目前的发展趋
势。

[RFC 7518 - JSON Web Algorithms (JWA)](https://tools.ietf.org/html/rfc7518) 中给出的 JWT
算法列表如下：

    +--------------+-------------------------------+--------------------+
    | "alg" Param  | Digital Signature or MAC      | Implementation     |
    | Value        | Algorithm                     | Requirements       |
    +--------------+-------------------------------+--------------------+
    | HS256        | HMAC using SHA-256            | Required           |
    | HS384        | HMAC using SHA-384            | Optional           |
    | HS512        | HMAC using SHA-512            | Optional           |
    | RS256        | RSASSA-PKCS1-v1_5 using       | Recommended        |
    |              | SHA-256                       |                    |
    | RS384        | RSASSA-PKCS1-v1_5 using       | Optional           |
    |              | SHA-384                       |                    |
    | RS512        | RSASSA-PKCS1-v1_5 using       | Optional           |
    |              | SHA-512                       |                    |
    | ES256        | ECDSA using P-256 and SHA-256 | Recommended+       |
    | ES384        | ECDSA using P-384 and SHA-384 | Optional           |
    | ES512        | ECDSA using P-521 and SHA-512 | Optional           |
    | PS256        | RSASSA-PSS using SHA-256 and  | Optional           |
    |              | MGF1 with SHA-256             |                    |
    | PS384        | RSASSA-PSS using SHA-384 and  | Optional           |
    |              | MGF1 with SHA-384             |                    |
    | PS512        | RSASSA-PSS using SHA-512 and  | Optional           |
    |              | MGF1 with SHA-512             |                    |
    | none         | No digital signature or MAC   | Optional           |
    |              | performed                     |                    |
    +--------------+-------------------------------+--------------------+

    The use of "+" in the Implementation Requirements column indicates
    that the requirement strength is likely to be increased in a future
    version of the specification.

目前应该所有 jwt 相关的库都支持 HS256/RS256/ES256 这三种算法。

ES256 使用 ECDSA 进行签名，它的安全性和运算速度目前和 RS256 差距不大，但是拥有更短的签名长
度。对于需要频繁发送的 JWT 而言，更短的长度长期下来可以节约大量流量。

因此更推荐使用 ES256 算法。

## 使用 OpenSSL 生成 RSA/ECC 公私钥

RS256 使用 RSA 算法进行签名，可通过如下命令生成 RSA 密钥：

```shell
# 1. 生成 2048 位（不是 256 位）的 RSA 密钥
openssl genrsa -out rsa-private-key.pem 2048

# 2. 通过密钥生成公钥
openssl rsa -in rsa-private-key.pem -pubout -out rsa-public-key.pem
```

ES256 使用 ECDSA 算法进行签名，该算法使用 ECC 密钥，生成命令如下：

```shell
# 1. 生成 ec 算法的私钥，使用 prime256v1 曲线（NIST P-256 标准），密钥长度 256 位。（强度大于 2048 位的 RSA 密钥）
openssl ecparam -genkey -name prime256v1 -out ecc-private-key.pem
# 2. 通过密钥生成公钥
openssl ec -in ecc-private-key.pem -pubout -out ecc-public-key.pem
```

密钥的使用应该就不需要介绍了，各类语言都有对应 JWT 库处理这些，请自行查看文档。

如果是调试/学习 JWT，需要手动签名与验证的话，推荐使用
[jwt 工具网站 - jwt.io](https://jwt.io/)

## 参考

- [RFC 7518 - JSON Web Algorithms (JWA)](https://tools.ietf.org/html/rfc7518)
- [什么是 JWT -- JSON WEB TOKEN](https://www.jianshu.com/p/576dbf44b2ae)
- [jwt 工具网站 - jwt.io](https://jwt.io/)
- [JWT 算法比较](https://www.cnblogs.com/langshiquan/p/10701198.html)
