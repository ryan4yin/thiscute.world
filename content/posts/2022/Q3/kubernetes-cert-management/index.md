---
title: "Kubernetes 中的证书管理工具 - cert-manager"
date: 2022-07-31T15:11:46+08:00
lastmod: 2022-07-31T15:11:46+08:00
draft: false

resources:
- name: "featured-image"
  src: "cert-manager.webp"

tags: ["数字证书", "证书", "TLS", "Kubernetes", "cert-manager"]
categories: ["tech"]
series: ["云原生相关"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

我在之前的文章 [写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议](https://thiscute.world/posts/about-tls-cert/) 中，介绍了如何使用 openssl 生成与管理各种用途的数字证书，也简单介绍了如何通过 certbot 等工具与 ACME 证书申请与管理协议，进行数字证书的申请与自动更新（autorenew）。

这篇文章要介绍的 cert-mangager，跟 certbot 这类工具有点类似，区别在于它是工作在 Kubernetes 中的。

cert-manager 是一个证书的自动化管理工具，用于在 Kubernetes 集群中自动化地颁发与管理各种来源、各种用途的数字证书。它将确保证书有效，并在合适的时间自动更新证书。

多的就不说了，证书相关的内容请参见我的 [写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议](https://thiscute.world/posts/about-tls-cert/) 或者其他资料，现在直接进入正题。

>注：cert-manager 的管理对象是「证书」，如果你仅需要使用非对称加密的公私钥对进行 JWT 签名、数据加解密，可以考虑直接使用 [secrets 管理工具 Vault](https://thiscute.world/posts/experience-of-vault/).

## 一、部署 {#deploy}

>https://cert-manager.io/docs/installation/helm/

官方提供了多种部署方式，使用 helm3 安装的方法如下：


```shell
# 添加 cert-manager 的 helm 仓库
helm repo add jetstack https://charts.jetstack.io
helm repo update
# 查看版本号
helm search repo jetstack/cert-manager -l | head
# 下载并解压 chart，目的是方便 gitops 版本管理
helm pull jetstack/cert-manager --untar --version 1.8.2
helm install \
  cert-manager ./cert-manager \
  --namespace cert-manager \
  --create-namespace \
  # 下面这个参数会导致使用 helm 卸载的时候，会删除所有 CRDs，可能导致所有 CRDs 资源全部丢失！要格外注意
  --set installCRDs=true
```

## 二、创建 Issuer {#create-issuer}

cert-manager 支持多种 issuer，你甚至可以通过它的标准 API 创建自己的 Issuer。

但是总的来说不外乎三种：

- 由权威 CA 机构签名的「公网受信任证书」: 这类证书会被浏览器、小程序等第三方应用/服务商信任
- 本地签名证书: 即由本地 CA 证书签名的数字证书
- 自签名证书: 即使用证书的私钥为证书自己签名

下面介绍下如何申请公网证书以及本地签名证书。

### 1. 通过权威机构创建公网受信证书 {#create-public-cert}

通过权威机构创建的公网受信证书，可以直接应用在边界网关上，用于给公网用户提供 TLS 加密访问服务，比如各种 HTTPS 站点、API。
这是需求最广的一类数字证书服务。

cert-manager 支持两种申请公网受信证书的方式：

- [ACME（Automated Certificate Management Environment (ACME) Certificate Authority server）](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment)证书自动化申请与管理协议。
- [venafi-as-a-service](https://cert-manager.io/docs/configuration/venafi/#creating-a-venafi-as-a-service-issuer): venafi 是一个证书的集中化管理平台，它也提供了 cert-manager 插件，可用于自动化申请 DigiCert/Entrust/GlobalSign/Let's Encrypt 四种类型的公网受信证书。

这里主要介绍使用 ACMEv2 协议申请公网证书，支持使用此开放协议申请证书的权威机构有：

- 免费服务
  - Let's Encrypt: 众所周知，它提供三个月有效期的免费证书。
  - [ZeroSSL](https://zerossl.com/documentation/acme/):  貌似也是一个比较有名的 SSL 证书服务
    - 通过 ACME 协议支持不限数量的 90 天证书，也支持多域名证书与泛域名证书。
    - 它提供了一个额外的 Dashboard 查看与管理所有申请的证书，这是比较方便的地方。
- 付费服务
  - DigiCert: 这个非常有名（但也是相当贵），官方文档 [Digicert - Third-party ACME client automation](https://docs.digicert.com/certificate-tools/Certificate-lifecycle-automation-index/acme-user-guide/)
  - Google Public Authority(Google Trust Services): Google 推出的公网证书服务，也是三个月有效期，其根证书交叉验证了 GlobalSign，OCSP 服务器在国内速度也很快。
    - 详见 [acme.sh/wiki/Google-Public-CA](https://github.com/acmesh-official/acme.sh/wiki/Google-Public-CA)
    - 此功能目前（2022-08-10）仍处于 beta 状态，需要提表单申请才能获得使用
    - 官方地址：https://pki.goog/
  - Entrust: 官方文档 [Entrust's ACME implementation](https://www.entrust.com/knowledgebase/ssl/how-to-use-acme-to-install-ssl-tls-certificates-in-entrust-certificate-services-apache#step1)
  - GlobalSign: 官方文档 [GlobalSign ACME Service](https://www.globalsign.com/en/acme-automated-certificate-management)

这里也顺便介绍下收费证书服务对证书的分级，以及该如何选用：

- Domain Validated（DV）证书
  - **仅验证域名所有权**，验证步骤最少，价格最低，仅需要数分钟即可签发。
  - 优点就是易于签发，很适合做自动化。
  - 各云厂商（AWS/GCP/Cloudflare，以及 Vercel/Github 的站点服务）给自家服务提供的免费证书都是 DV 证书，Let's Encrypt 的证书也是这个类型。
    - 很明显这些证书的签发都非常方便，而且仅验证域名所有权。
    - 但是 AWS/GCP/Cloudflare/Vercel/Github 提供的 DV 证书都仅能在它们的云服务上使用，不提供私钥导出功能！
- Organization Validated (OV) 证书
  - 是企业 SSL 证书的首选，通过企业认证确保企业 SSL 证书的真实性。
  - 除域名所有权外，CA 机构还会审核组织及企业的真实性，包括注册状况、联系方式、恶意软件等内容。
  - 如果要做合规化，可能至少也得用 OV 这个级别的证书。
- Extended Validation（EV）证书
  - 最严格的认证方式，CA 机构会深度审核组织及企业各方面的信息。
  - 被认为适合用于大型企业、金融机构等组织或企业。
  - 而且仅支持签发单域名、多域名证书，不支持签发泛域名证书，安全性杠杠的。

ACME 支持 HTTP01 跟 DNS01 两种域名验证方式，其中 DNS01 是最简便的方法。

下面分别演示如何使用 AWS Route53 跟 AliDNS，通过 DNS 验证方式申请一个 Let's Encrypt 证书。（其他 DNS 提供商的配置方式请直接看官方文档）

#### 1.1 使用 AWS Route53 创建一个证书签发者「Certificate Issuer」 {#1-1-aws-route53}

>非 AWS Route53 用户可忽略这一节

>https://cert-manager.io/docs/configuration/acme/dns01/route53/

##### 1.1.1 通过 IAM 授权 cert-manager 调用 AWS Route53 API {#1-1-1-iam-cert-manager-aws-route53-api}

>这里介绍一种不需要创建 ACCESS_KEY_ID/ACCESS_SECRET，直接使用 AWS EKS 官方的免密认证的方法。会更复杂一点，但是更安全可维护。

首先需要为 EKS 集群创建 OIDC provider，参见 [aws-iam-and-kubernetes](https://github.com/ryan4yin/knowledge/blob/master/kubernetes/security/aws-iam-and-kubernetes.md)，这里不再赘述。

cert-manager 需要查询与更新 Route53 记录的权限，因此需要使用如下配置创建一个 IAM Policy，可以命名为 `<ClusterName>CertManagerRoute53Access`（注意替换掉 `<ClusterName>`）：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "route53:GetChange",
      "Resource": "arn:aws:route53:::change/*"
    },
    {
      "Effect": "Allow",
      "Action": [
 "route53:ChangeResourceRecordSets",
 "route53:ListResourceRecordSets"
      ],
      "Resource": "arn:aws:route53:::hostedzone/*"
    },
    {
      "Effect": "Allow",
      "Action": "route53:ListHostedZonesByName",
      "Resource": "*"
    }
  ]
}
```

比如使用 awscli 创建此 policy：

```shell
aws iam create-policy \
  --policy-name XxxCertManagerRoute53Access \
  --policy-document file://cert-manager-route53-access.json
```

然后通过上述配置创建一个 IAM Role 并自动给 cert-manager 所在的 EKS 集群添加信任关系：

```shell
export CLUSTER_NAME="xxx"
export AWS_ACCOUNT_ID="112233445566"

# 使用 eksctl 自动创建对应的 role 并添加信任关系
# 需要先安装好 eksctl
eksctl create iamserviceaccount \
  --cluster "${CLUSTER_NAME}" --name cert-manager --namespace cert-manager \
  --role-name "${CLUSTER_NAME}-cert-manager-route53-role" \
  --attach-policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/<ClusterName>CertManagerRoute53Access" \
  --role-only \
  --approve
```

之后需要为 cert-manager 的 ServiceAccount 添加注解来绑定上面刚创建好的 IAM Role，首先创建如下 helm values 文件 `cert-manager-values.yaml`:

```yaml
# 如果把这个改成 false，也会导致 cert-manager 的所有 CRDs 及相关资源被删除！
installCRDs: true

serviceAccount:
  annotations:
    # 注意修改这里的 ${AWS_ACCOUNT_ID} 以及 ${CLUSTER_NAME}
    eks.amazonaws.com/role-arn: >-
      arn:aws:iam::${AWS_ACCOUNT_ID}:role/${CLUSTER_NAME}-cert-manager-route53-role

securityContext:
  enabled: true
  # 根据官方文档，还得修改下这个，允许 cert-manager 读取 ServiceAccount Token，从而获得授权
  fsGroup: 1001
```

然后重新部署 cert-manager:

```shell
helm upgrade -i cert-manager ./cert-manager -n cert-manager -f cert-manager-values.yaml
```

这样就完成了授权。

##### 1.1.2 创建一个使用 AWS Route53 进行验证的 ACME Issuer {#1-1-2-aws-route53-acme-issuer}

在 xxx 名字空间创建一个 Iusser：

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod-aws
  namespace: xxx
spec:
  acme:
    # 用于接受域名过期提醒的邮件地址
    email: user@example.com
    # ACME 服务器，比如 let's encrypt、Digicert 等
    # let's encrypt 的测试 URL，可用于测试配置正确性
    # server: https://acme-staging-v02.api.letsencrypt.org/directory
    # let's encrypt 的正式 URL，有速率限制
    server: https://acme-v02.api.letsencrypt.org/directory

    # 用于存放 ACME 账号私钥的 Secret 名称，Issuer 创建时会自动生成此 secret
    privateKeySecretRef:
      name: letsencrypt-prod-aws
    
    # DNS 验证设置
    solvers:
    - selector:
        # 在有多个 solvers 的情况下，会根据每个 solvers 的 selector 来确定优先级，选择其中合适的 solver 来处理证书申请事件
        # 以 dnsZones 为例，越长的 Zone 优先级就越高
        # 比如在为 www.sys.exapmle.com 申请证书时，sys.example.com 的优先级就比 example.com 更高
        dnsZones:
        - "example.com"
      dns01:
        # 使用 route53 进行验证
        route53:
          region: us-east-1
          # cert-manager 已经通过 ServiceAccount 绑定了 IAM Role
          # 这里不需要补充额外的 IAM 授权相关信息！
```


#### 1.2 使用 AliDNS 创建一个证书签发者「Certificate Issuer」 {#1-2-alidns-certificate-issuer}

>https://cert-manager.io/docs/configuration/acme/dns01/#webhook

cert-manager 官方并未提供 alidns 相关的支持，而是提供了一种基于 WebHook 的拓展机制。社区有第三方创建了对 alidns 的支持插件：

- [cert-manager-alidns-webhook](https://github.com/DEVmachine-fr/cert-manager-alidns-webhook)

下面我们使用此插件演示下如何创建一个证书签发者。

##### 1.1.1 通过 IAM 授权 cert-manager 调用 AWS Route53 API

首先需要在阿里云上创建一个子账号，名字可以使用 `alidns-acme`，给它授权 DNS 修改权限，然后为该账号生成 ACCESS_KEY_ID/ACCESS_SECRET。

完成后，使用如下命令将 key/secret 内容创建为 secret 供后续步骤使用：

```shell
# 注意替换如下命令中的 <xxx> 为你的 key/secret
kubectl -n cert-manager create secret generic alidns-secrets \
  --from-literal="access-token=<your-access-key-id>" \
  --from-literal="secret-key=<your-access-secret-key>"
```

接下来需要部署 [cert-manager-alidns-webhook](https://github.com/DEVmachine-fr/cert-manager-alidns-webhook) 这个 cert-manager 插件：

```shell
# 添加 helm 仓库
helm repo add cert-manager-alidns-webhook https://devmachine-fr.github.io/cert-manager-alidns-webhook
helm repo update

# 安装插件
## 其中的 groupName 是一个全局唯一的标识符，用于标识创建此 webhook 的组织，建议使用公司域名
## groupName 必须与后面创建的 Issuer 中的 groupName 一致，否则证书将无法通过验证！
helm -n cert-manager install alidns-webhook \
  cert-manager-alidns-webhook/alidns-webhook \
  --set groupName=example.com
```

##### 1.1.2 创建一个使用 AliDNS 进行验证的 ACME Issuer {#1-1-2-alidns-acme-issuer}

在 xxx 名字空间创建一个 Iusser：

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod-alidns
  namespace: xxx
spec:
  acme:
    # 用于接受域名过期提醒的邮件地址
    email: user@example.com
    # ACME 服务器，比如 let's encrypt、Digicert 等
    # let's encrypt 的测试 URL，可用于测试配置正确性
    # server: https://acme-staging-v02.api.letsencrypt.org/directory
    # let's encrypt 的正式 URL，有速率限制
    server: https://acme-v02.api.letsencrypt.org/directory

    # 用于存放 ACME 账号私钥的 Secret 名称，Issuer 创建时会自动生成此 secret
    privateKeySecretRef:
      name: letsencrypt-prod-alidns
    
    # DNS 验证设置
    solvers:
    - selector:
        # 在有多个 solvers 的情况下，会根据每个 solvers 的 selector 来确定优先级，选择其中合适的 solver 来处理证书申请事件
        # 以 dnsZones 为例，越长的 Zone 优先级就越高
        # 比如在为 www.sys.exapmle.com 申请证书时，sys.example.com 的优先级就比 example.com 更高
        # 适用场景：如果你拥有多个域名，使用了多个域名提供商，就可能需要用到它
        dnsZones:
        - "example.com"
      dns01:
        webhook:
            config:
              accessTokenSecretRef:
                key: access-token
                name: alidns-secrets
              regionId: cn-beijing
              secretKeySecretRef:
                key: secret-key
                name: alidns-secrets
            # 这个 groupName 必须与之前部署插件时设置的一致！
            groupName: example.com
            solverName: alidns-solver
```

#### 1.3 通过 ACME 创建证书 {#1-3-acme-certificate}

>https://cert-manager.io/docs/usage/certificate/#creating-certificate-resources

在创建证书前，先简单过一下证书的申请流程，示意图如下（出问题时需要靠这个来排查）：

```
(  +---------+  )
  (  | Ingress |  ) Optional                                              ACME Only!
  (  +---------+  )
         |                                                     |
         |   +-------------+      +--------------------+       |  +-------+       +-----------+
         |-> | Certificate |----> | CertificateRequest | ----> |  | Order | ----> | Challenge | 
             +-------------+      +--------------------+       |  +-------+       +-----------+
                                                               |
```

使用如下配置创建证书，并将证书保存到指定的 Secret 中：

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com
  namespace: xxx
spec:
  # Secret names are always required.
  # Istio Gateway/Ingress/Gateway API 都可以通过直接引用这个 secret 来添加 TLS 加密。
  secretName: tls-example.com

  # secretTemplate is optional. If set, these annotations and labels will be
  # copied to the Secret named tls-example.com. These labels and annotations will
  # be re-reconciled if the Certificate's secretTemplate changes. secretTemplate
  # is also enforced, so relevant label and annotation changes on the Secret by a
  # third party will be overwriten by cert-manager to match the secretTemplate.
  secretTemplate:
    annotations:
      my-secret-annotation-1: "foo"
      my-secret-annotation-2: "bar"
    labels:
      my-secret-label: foo

  duration: 2160h # 90d
  renewBefore: 360h # 15d
  # https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.CertificatePrivateKey
  privateKey:
    algorithm: ECDSA  # RSA/ECDSA/Ed25519，其中 RSA 应用最广泛，Ed25519 被认为最安全
    encoding: PKCS1  # 对于 TLS 加密，通常都用 PKCS1 格式
    size: 256  # RSA 默认为 2048，ECDSA 默认为 256，而 Ed25519 不使用此属性！
    rotationPolicy: Always  # renew 时总是重新创建新的私钥
  # The use of the common name field has been deprecated since 2000 and is
  # discouraged from being used.
  commonName: example.com
  # At least one of a DNS Name, URI, or IP address is required.
  dnsNames:
    - example.com
    - '*.example.com'
  isCA: false
  usages:
    - server auth
    - client auth
  # uris:  # 如果想在证书的 subjectAltNames 中添加 URI，就补充在这里
  #   - spiffe://cluster.local/ns/sandbox/sa/example
  # ipAddresses:  # 如果想在证书的 subjectAltNames 添加 ip 地址，就补充在这里
  #   - 192.168.0.5
  subject:
    # 证书的补充信息
    # 字段索引：https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.X509Subject
    organizations:
      - xxx
  # Issuer references are always required.
  issuerRef:
    name: letsencrypt-prod-aws
    # name: letsencrypt-prod-alidns  # 如果你前面创建的是 alidns 那就用这个
    kind: Issuer  # 如果你创建的是 ClusterIssuer 就需要改下这个值
    group: cert-manager.io
```

部署好 Certificate 后，describe 它就能看到当前的进度：

```
Events: 
  Type    Reason     Age   From    Message 
  ----    ------     ----  ----    ------- 
  Normal  Issuing    117s  cert-manager-certificates-trigger   Issuing certificate as Secret does not exist      
  Normal  Generated  116s  cert-manager-certificates-key-manager      Stored new private key in temporary Secret resource "example.com-f044j"     
  Normal  Requested  116s  cert-manager-certificates-request-manager  Created new CertificateRequest resource "example.com-unv3d"   
  Normal  Issuing    20s   cert-manager-certificates-issuing   The certificate has been successfully issued
```

如果发现证书长时间未 Ready，可以参照[官方文档 - Troubleshooting Issuing ACME Certificates](https://cert-manager.io/docs/faq/acme/)，按证书申请流程进行逐层排查：

- 首先 cert-manager 发现 Certificate 描述的 Secret 不存在，于是启动证书申请流程
- 首先生成私钥，存放在一个临时 Secret 中
- 然后通过私钥以及 Certificate 资源中的其他信息，生成 CSR 证书申请请求文件
  - 这也是一个 CRD 资源，可以通过 `kubectl get csr -n xxx` 查看
- 接着将 CSR 文件提交给 ACME 服务器，申请权威机构签发证书
  - 这对应 CRD 资源 `kubectl get order`
- 对于上述 ACME 证书申请流程，Order 实际上会生成一个 DNS1 Challenge 资源
  - 可以通过 `kubectl get challenge` 检查此资源
- challenge 验证通过后会逐层往回走，前面的 Order CSR 状态都会立即变成 valid
- 最终证书签发成功，Certificate 状态变成 Ready，所有 Order CSR challenge 资源都被自动清理掉。

#### 1.4 通过 csi-driver 创建证书 {#csi-driver}

>https://cert-manager.io/docs/projects/csi-driver/

直接使用 `Certificate` 资源创建的证书，会被存放在 Kubernetes Secrets 中，被认为并非足够安全。
而 cert-manager csi-driver 则避免了这个缺陷，具体而言，它提升安全性的做法有：

- 确保私钥仅保存在对应的节点上，并挂载到对应的 Pod，完全避免私钥被通过网络传输。
- 应用的每个副本都使用自己生成的私钥，并且能确保在 Pod 的生命周期中证书跟私钥始终存在。
- 自动 renew 证书
- 副本被删除时，证书就会被销毁

总的说 csi-driver 主要是用来提升安全性的，有需要可以自己看文档，就不多介绍了。

### 2. 通过私有 CA 颁发证书

Private CA 是一种企业自己生成的 CA 证书，通常企业用它来构建自己的 PKI 基础设施。

在 TLS 协议这个应用场景下，Private CA 颁发的证书仅适合在企业内部使用，必须在客户端安装上这个 CA 证书，才能正常访问由它签名的数字证书加密的 Web API 或者站点。**Private CA 签名的数字证书在公网上是不被信任的**！

cert-manager 提供的 Private CA 服务有：

- [Vault](https://cert-manager.io/docs/configuration/vault/): 鼎鼎大名了，Vault 是一个密码即服务工具，可以部署在 K8s 集群中，提供许多密码、证书相关的功能。
  - 开源免费
- [AWS Certificate Manager Private CA](https://github.com/cert-manager/aws-privateca-issuer): 跟 Vault 的 CA 功能是一致的，区别是它是托管的，由 AWS 负责维护。
  - 每个 Private CA 证书：$400/month
  - 每个签发的证书（仅读取了私钥及证书内容后才会收费）：按梯度一次性收费，0-1000 个以内是 $0.75 每个
- 其他的自己看文档...

这个因为暂时用不上，所以还没研究，之后有研究再给补上。

TO BE DONE.


## 三、cert-manager 与 istio/ingress 等网关集成 {#cert-manager-and-gateway}

cert-manager 提供的 `Certificate` 资源，会将生成好的公私钥存放在 Secret 中，而 Istio/Ingress 都支持这种格式的 Secret，所以使用还是挺简单的。

以 Istio Gateway 为例，直接在 Gateway 资源上指定 Secret 名称即可：

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: example-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 8080
      name: http
      protocol: HTTP
    hosts:
    - product.example.com
    tls:
      httpsRedirect: true # sends 301 redirect for http requests
  - port:
      number: 8443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE # enables HTTPS on this port
      credentialName: tls-example.com # This should match the Certificate secretName
    hosts:
    - product.example.com # This should match a DNS name in the Certificate
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: product
spec:
  hosts:
  - product.example.com
  gateways:
  - example-gateway
  http:
  - route:
    - destination:
        host: product
        port:
          number: 8080
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: product
  name: product
  namespace: prod
spec:
  ports:
  - name: grpc
    port: 9090
    protocol: TCP
    targetPort: 9090
  - name: http
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: product
  sessionAffinity: None
  type: ClusterIP
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: product
spec:
  host: product
  # 定义了两个 subset
  subsets:
  - labels:
      version: v1
    name: v1
  - labels:
      version: v2
    name: v2
---
# 其他 deployment 等配置
```

之后再配合 VirtualService 等资源，就可以将 Istio 跟 cert-manager 结合起来啦。

## 四、将 cert-manager 证书挂载到自定义网关中 {#cert-manager-istio-ingress}

>注意，千万别使用 `subPath` 挂载，根据[官方文档](https://kubernetes.io/docs/concepts/configuration/secret/#mounted-secrets-are-updated-automatically)，这种方式挂载的 Secret 文件不会自动更新！

既然证书被存放在 Secret 中，自然可以直接当成数据卷挂载到 Pods 中，示例如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    volumeMounts:
    - name: tls-example.com
      mountPath: "/certs/example.com"
      readOnly: true
  volumes:
  - name: tls-example.com
    secret:
      secretName: tls-example.com
      optional: false # default setting; "mysecret" must exist
```

对于 nginx 而言，可以简单地搞个 sidecar 监控下，有配置变更就 reload 下 nginx，实现证书自动更新。

或者可以考虑直接写个 k8s informer 监控 secret 的变更，有变更就直接 reload 所有 nginx 实例，总之实现的方式有很多种。

## 五、监控告警 {#monitoring-and-alerting}

证书的过期时间是一个很重要的指标，证书过期了，网站就无法正常访问了。
虽然正常情况下 cert-manager 应该能够自动更新证书，但是万一出现了问题，又没有及时发现，那就麻烦了。

因此，建议对证书的过期时间进行监控，当证书的过期时间小于一定阈值时，及时发出告警。

cert-manager 提供了 Prometheus 监控指标，可以直接使用 Prometheus 等工具进行监控告警。

官方文档是这个：<https://cert-manager.io/docs/usage/prometheus-metrics/#scraping-metrics>

文档中没详细列出所有的指标，可以直接接入到 Prometheus 中，然后通过 Grafana 查看。

比如要设置证书过期时间的告警，可以使用如下 PromQL：

```promql
(certmanager_certificate_expiration_timestamp_seconds - time())/3600/24 < 20
``````

上面这个 PromQL 表示，如果证书的过期时间小于 20 天，就会触发告警。

## 六、注意事项 {#attention}

服务端 TLS 协议的配置有许多的优化点，有些配置对性能的提升是很明显的，建议自行网上搜索相关资料，这里仅列出部分相关信息。

### OCSP 证书验证协议会大幅拖慢 HTTPS 协议的响应速度

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

为了解决这两个问题，[rfc6066](https://www.rfc-editor.org/rfc/rfc6066) 定义了 OCSP stapling 功能，它使服务器可以提前访问 OCSP 获取证书状态信息并缓存到本地，基本 Nginx/Caddy 等各大 Web 服务器或网关，都支持 OCSP stapling 协议。


在客户端使用 TLS 协议访问 HTTPS 服务时，服务端会直接在握手阶段将缓存的 OCSP 信息发送给客户端。
因为 OCSP 信息会带有 CA 证书的签名及有效期，客户端可以直接通过签名验证 OCSP 信息的真实性与有效性，这样就避免了客户端访问 OCSP 服务器带来的开销。

而另一个方法，就是选用 ocsp 服务器在目标用户区域速度快的 CA 机构签发证书。
