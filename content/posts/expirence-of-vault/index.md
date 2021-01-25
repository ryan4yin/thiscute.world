---
title: "Vault 的介绍、安装及使用"
date: 2021-01-24T09:31:41+08:00
draft: false

resources:
- name: "featured-image"
  src: "bankvault.jpg"

tags: ["Vault", "云原生", "Secrets", "配置", "配置管理"]
categories: ["技术"]
---

[Vault](https://github.com/hashicorp/vault) 是 hashicorp 推出的 secrets 管理、加密即服务与权限管理工具。它的功能简介如下：

1. secrets 管理：支持保存各种自定义信息、自动生成各类密钥，vault 自动生成的密钥还能自动轮转(rotate)
2. 认证方式：支持接入各大云厂商的账号权限体系（比如阿里云RAM子账号体系）或者 LDAP 等进行身份验证，不需要创建额外的账号体系。
3. 权限管理：通过 policy，可以设定非常细致的 ACL 权限。
4. 密钥引擎：也支持接入各大云厂商的账号体系（比如阿里云RAM子账号体系），实现 APIKey/APISecret 的自动轮转。
5. 支持接入 kubernetes rbac 权限体系，通过 serviceaccount+role 为每个 Pod 单独配置权限。

在使用 Vault 之前，我们是以携程开源的 [Apollo](https://github.com/ctripcorp/apollo) 作为微服务的分布式配置中心。

Apollo 在国内非常流行。它功能强大，支持配置的继承，也有提供 HTTP API 方便自动化。
缺点是权限管理和 secrets 管理比较弱，也不支持信息加密，不适合直接存储敏感信息。因此我们现在切换到了 Vault.

目前我们本地的 CI/CD 流水线和云上的微服务体系，都是使用的 Vault 做 secrets 管理.

## 一、Vault 基础概念


首先看一下 Vault 的架构图：

![](/images/expirence-of-vault/vault-layers.png "vault layers")

可以看到，几乎所有的组件都从属于「安全屏障(security barrier)」，
Vault 可以简单地被划分为 Storage Backend、安全屏障(security barrier) 和 HTTP API 三个部分。

「安全屏障(security barrier)」是 Vault(金库) 周围的加密「钢铁」和「混凝土」，Storage Backend 和 Vault 之间的所有数据流动都需要经过「屏障(barrier)」。
barrier 确保只有加密数据会被写入 Storage Backend，加密数据在经过 barrier 的过程中被验证与解密。
和银行金库(bank vault)非常类似，barrier 也必须先解封，才能允许读取内部的数据。

### 1. 数据存储及加密解密

Storage Backend(后端存储): Vault 自身不存储数据，因此需要为它配置一个「Storage Backend」。
「Storage Backend」是不受信任的，只用于存储加密数据。

Initialaztion(初始化): vault 在首次启动时需要初始化，这一步生成一个「加密密钥(encryption key)」用于加密数据，加密完成的数据才能被保存到 Storage Backend.

Unseal(解封): Vault 启动后，因为不知道「加密密钥(encryption key)」，它会进入「封印(sealed)」状态，在「Unseal」前无法进行任何操作。
「加密密钥」被「master key」保护，我们必须提供「master key」才能完成 Unseal 操作。
默认情况下，vault 使用[沙米尔密钥共享算法](https://medium.com/taipei-ethereum-meetup/%E7%A7%81%E9%91%B0%E5%88%86%E5%89%B2-shamirs-secret-sharing-7a70c8abf664)
将「master key」分割成五个「Key Shares(分享密钥)」，必须要提供其中任意三个「Key Shares」才能重建出「master key」从而完成 Unseal.

![](/images/expirence-of-vault/vault-shamir-secret-sharing.svg "vault-shamir-secret-sharing")

>「Key Shares」的数量，以及重建「master key」最少需要的 key shares 数量，都是可以调整的。
沙米尔密钥共享算法也可以关闭，这样 master key 将被直接用于 Unseal.


### 2. 认证系统及权限系统

在解封完成后，Vault 就可以开始处理请求了。

HTTP 请求进入后的整个处理流程都由 vault core 管理，core 会强制进行 ACL 检查，并确保审计日志(audit logging)完成记录。

客户端首次连接 vault 时，需要先完成身份认证，vault 的「auth methods」模块有很多身份认证方法可选：

1. 用户友好的认证方法，适合管理员使用：username/password、云服务商、ldap
   1. 在创建 user 的时候，需要为 user 绑定 policy，给予合适的权限。
2. 应用友好的方法：public/private keys、tokens、kubernetes、jwt

身份验证请求流经 Core 并进入 auth methods，auth methods 确定请求是否有效并返回「关联策略(policies)」的列表。

ACL Policies 由 policy store 负责管理与存储，由 core 进行 ACL 检查。
ACL 的默认行为是拒绝，这意味着除非明确配置 Policy 允许某项操作，否则该操作将被拒绝。

在通过 auth methods 完成了身份认证，并且返回的「关联策略」也没毛病之后，「token store」将会生成并管理一个新的 token，
这个 token 会被返回给客户端，用于进行后续请求。
类似 web 网站的 cookie，token 也都存在一个 lease 租期或者说有效期，这加强了安全性。

token 关联了相关的策略 policies，策略将被用于验证请求的权限。
请求经过验证后，将被路由到 secret engine。如果 secret engine 返回了一个 secret（由 vault 自动生成的 secret），
Core 会将其注册到 expiration manager，并给它附加一个 lease ID。lease ID 被客户端用于更新(renew)或吊销(revoke)它得到的 secret.
如果客户端允许租约(lease)到期，expiration manager 将自动吊销这个 secret.

Core 负责处理审核代理(audit brok)的请求及响应日志，将请求发送到所有已配置的审核设备(audit devices)。


### 3. Secret Engine

Secret Engine 是保存、生成或者加密数据的组件，它非常灵活。

有的 Secret Engines 只是单纯地存储与读取数据，比如 kv 就可以看作一个加密的 Redis。
而其他的 Secret Engines 则连接到其他的服务并按需生成动态凭证。
还有些 Secret Engines 提供「加密即服务(encryption as a service)」 - transit、证书管理等。

常用的 engine 举例：

1. AliCloud Secrets Engine: 基于 RAM 策略动态生成 AliCloud Access Token，或基于 RAM 角色动态生成 AliCloud STS 凭据
    - Access Token 会自动更新(Renew)，而 STS 凭据是临时使用的，过期后就失效了。
1. kv: 键值存储，可用于存储一些静态的配置。它一定程度上能替代掉携程的 Apollo 配置中心。
1. Transit Secrets Engine: 提供加密即服务的功能，它只负责加密和解密，不负责存储。主要应用场景是帮 app 加解密数据，但是数据仍旧存储在 MySQL 等数据库中。


## 二、部署 Vault

官方建议[通过 Helm 部署 vault](https://www.vaultproject.io/docs/platform/k8s/helm/run)，大概流程：

1. 使用 helm/docker 部署运行 vault.
2. 初始化/解封 vault: vault 安全措施，每次重启必须解封(可设置自动解封).

### 1. docker-compose 部署

>推荐用于本地开发测试环境，或者其他不需要高可用的环境。

`docker-compose.yml` 示例如下：

```yaml
version: '3.3'
services:
  vault:
    # 文档：https://hub.docker.com/_/vault
    image: vault:1.6.0
    container_name: vault
    ports:
      # rootless 容器，内部不能使用标准端口 443
      - "443:8200"
    restart: always
    volumes:
      # 审计日志存储目录，默认不写审计日志，启用 `file` audit backend 时必须提供一个此文件夹下的路径
      - ./logs:/vault/logs
      # 当使用 file data storage 插件时，数据被存储在这里。默认不往这写任何数据。
      - ./file:/vault/file
      # 配置目录，vault 默认 `/valut/config/` 中所有以 .hcl/.json 结尾的文件
      # config.hcl 文件内容，参考 cutom-vaules.yaml
      - ./config.hcl:/vault/config/config.hcl
      # TLS 证书
      - ./certs:/certs
    # vault 需要锁定内存以防止敏感值信息被交换(swapped)到磁盘中
    # 为此需要添加如下能力
    cap_add:
      - IPC_LOCK
    # 必须手动设置 entrypoint，否则 vault 将以 development 模式运行
    entrypoint: vault server -config /vault/config/config.hcl
```

`config.hcl` 内容如下：

```hcl
ui = true

// 使用文件做数据存储（单节点）
storage "file" {
  path    = "/vault/file"
}

listener "tcp" {
  address = "[::]:8200"

  tls_disable = false
  tls_cert_file = "/certs/server.crt"
  tls_key_file  = "/certs/server.key"
}
```

将如上两份配置保存在同一非文件夹内，同时在 `./certs` 中提供 TLS 证书 `server.crt` 和私钥 `server.key`。

然后 `docker-compose up -d` 就能启动运行一个 vault 实例。

### 2. 通过 helm 部署 vault {#install-by-helm}

>推荐用于生产环境



通过 helm 部署：

```shell
# 添加 valut 仓库
helm repo add hashicorp https://helm.releases.hashicorp.com
# 查看 vault 版本号
helm search repo hashicorp/vault -l | head
# 下载某个版本号的 vault
helm pull hashicorp/vault --version 0.7.0 --untar
```

参照下载下来的 `./vault/values.yaml` 编写 `custom-values.yaml`，
部署一个以 `mysql` 为后端存储的 HA vault，配置示例如下:

```yaml
global:
  # enabled is the master enabled switch. Setting this to true or false
  # will enable or disable all the components within this chart by default.
  enabled: true
  # TLS for end-to-end encrypted transport
  tlsDisable: false

injector:
  # True if you want to enable vault agent injection.
  enabled: true

  replicas: 1

  # If multiple replicas are specified, by default a leader-elector side-car
  # will be created so that only one injector attempts to create TLS certificates.
  leaderElector:
    enabled: true
    image:
      repository: "gcr.io/google_containers/leader-elector"
      tag: "0.4"
    ttl: 60s

  # If true, will enable a node exporter metrics endpoint at /metrics.
  metrics:
    enabled: false

  # Mount Path of the Vault Kubernetes Auth Method.
  authPath: "auth/kubernetes"

  certs:
    # secretName is the name of the secret that has the TLS certificate and
    # private key to serve the injector webhook. If this is null, then the
    # injector will default to its automatic management mode that will assign
    # a service account to the injector to generate its own certificates.
    secretName: null

    # caBundle is a base64-encoded PEM-encoded certificate bundle for the
    # CA that signed the TLS certificate that the webhook serves. This must
    # be set if secretName is non-null.
    caBundle: ""

    # certName and keyName are the names of the files within the secret for
    # the TLS cert and private key, respectively. These have reasonable
    # defaults but can be customized if necessary.
    certName: tls.crt
    keyName: tls.key

server:
  # Resource requests, limits, etc. for the server cluster placement. This
  # should map directly to the value of the resources field for a PodSpec.
  # By default no direct resource request is made.

  # authDelegator enables a cluster role binding to be attached to the service
  # account.  This cluster role binding can be used to setup Kubernetes auth
  # method.  https://www.vaultproject.io/docs/auth/kubernetes.html
  authDelegator:
    enabled: true

  # Enables a headless service to be used by the Vault Statefulset
  service:
    enabled: true
    # clusterIP controls whether a Cluster IP address is attached to the
    # Vault service within Kubernetes.  By default the Vault service will
    # be given a Cluster IP address, set to None to disable.  When disabled
    # Kubernetes will create a "headless" service.  Headless services can be
    # used to communicate with pods directly through DNS instead of a round robin
    # load balancer.
    # clusterIP: None

    # Configures the service type for the main Vault service.  Can be ClusterIP
    # or NodePort.
    #type: ClusterIP

    # If type is set to "NodePort", a specific nodePort value can be configured,
    # will be random if left blank.
    #nodePort: 30000

    # Port on which Vault server is listening
    port: 8200
    # Target port to which the service should be mapped to
    targetPort: 8200


  # This configures the Vault Statefulset to create a PVC for audit
  # logs.  Once Vault is deployed, initialized and unseal, Vault must
  # be configured to use this for audit logs.  This will be mounted to
  # /vault/audit
  # See https://www.vaultproject.io/docs/audit/index.html to know more
  auditStorage:
    enabled: false
    # Size of the PVC created
    size: 10Gi
    # Name of the storage class to use.  If null it will use the
    # configured default Storage Class.
    storageClass: null
    # Access Mode of the storage device being used for the PVC
    accessMode: ReadWriteOnce
    # Annotations to apply to the PVC
    annotations: {}

  # Run Vault in "HA" mode. There are no storage requirements unless audit log
  # persistence is required.  In HA mode Vault will configure itself to use Consul
  # for its storage backend.  The default configuration provided will work the Consul
  # Helm project by default.  It is possible to manually configure Vault to use a
  # different HA backend.
  ha:
    enabled: true
    replicas: 3

    # Set the api_addr configuration for Vault HA
    # See https://www.vaultproject.io/docs/configuration#api_addr
    # If set to null, this will be set to the Pod IP Address
    apiAddr: null

    # config is a raw string of default configuration when using a Stateful
    # deployment. Default is to use a Consul for its HA storage backend.
    # This should be HCL.
    
    # Note: Configuration files are stored in ConfigMaps so sensitive data 
    # such as passwords should be either mounted through extraSecretEnvironmentVars
    # or through a Kube secret.  For more information see: 
    # https://www.vaultproject.io/docs/platform/k8s/helm/run#protecting-sensitive-vault-configurations
    config: |
      ui = true

      listener "tcp" {
        address = "[::]:8200"
        cluster_address = "[::]:8201"

        tls_disable = false
        tls_cert_file = "/etc/certs/vault.crt"
        tls_key_file  = "/etc/certs/vault.key"
      }

      storage "mysql" {
        address = "<host>:3306"
        username = "<username>"
        password = "<password>"
        database = "vault"
        ha_enabled = "true"
      }

      service_registration "kubernetes" {}

      # Example configuration for using auto-unseal, using Google Cloud KMS. The
      # GKMS keys must already exist, and the cluster must have a service account
      # that is authorized to access GCP KMS.
      #seal "gcpckms" {
      #   project     = "vault-helm-dev-246514"
      #   region      = "global"
      #   key_ring    = "vault-helm-unseal-kr"
      #   crypto_key  = "vault-helm-unseal-key"
      #}

# Vault UI
ui:
  # True if you want to create a Service entry for the Vault UI.
  #
  # serviceType can be used to control the type of service created. For
  # example, setting this to "LoadBalancer" will create an external load
  # balancer (for supported K8S installations) to access the UI.
  enabled: true
  publishNotReadyAddresses: true
  # The service should only contain selectors for active Vault pod
  activeVaultPodOnly: false
  serviceType: "ClusterIP"
  serviceNodePort: null
  externalPort: 8200
```

现在使用自定义的 `custom-values.yaml` 部署 vautl:

```shell
kubectl create namespace vault
# 安装/升级 valut
helm upgrade --install vault ./vault --namespace vault -f custom-values.yaml
```

### 3. 初始化(initalize)并解封(unseal) vault

>官方文档：[Initialize and unseal Vault - Vault on Kubernetes Deployment Guide](https://learn.hashicorp.com/tutorials/vault/kubernetes-raft-deployment-guide?in=vault/kubernetes#install-vault)

通过 helm 部署 vault，默认会部署一个三副本的 StatefulSet，但是这三个副本都会处于 NotReady 状态（docker 方式部署的也一样）。
接下来还需要手动初始化(initalize)并解封(unseal) vault，才能 `Ready`:

1. 第一步：从三个副本中随便选择一个，运行 vault 的初始化命令：`kubectl exec -ti vault-0 -- vault operator init`
   1. 初始化操作会返回 5 个 unseal keys，以及一个 Initial Root Token，这些数据非常敏感非常重要，一定要保存到安全的地方！
2. 第二步：在每个副本上，使用任意三个 unseal keys 进行解封操作。
   1. 一共有三个副本，也就是说要解封 3*3 次，才能完成 vault 的完整解封！

```shell
# 每个实例都需要解封三次！
## Unseal the first vault server until it reaches the key threshold
$ kubectl exec -ti vault-0 -- vault operator unseal # ... Unseal Key 1
$ kubectl exec -ti vault-0 -- vault operator unseal # ... Unseal Key 2
$ kubectl exec -ti vault-0 -- vault operator unseal # ... Unseal Key 3
```

这样就完成了部署，但是要注意，**vault 实例每次重启后，都需要重新解封！也就是重新进行第二步操作！**

### 4. 设置自动解封

每次重启都要手动解封所有 vault 实例，实在是很麻烦，在云上自动扩缩容的情况下，vault 实例会被自动调度，这种情况就更麻烦了。

为了简化这个流程，可以考虑配置 auto unseal 让 vault 自动解封。

自动解封目前有两种方法：

1. 使用阿里云/AWS/Azure 等云服务提供的密钥库来管理 encryption key，阿里云的相关配置方法：[alicloudkms Seal](https://www.vaultproject.io/docs/configuration/seal/alicloudkms)
2. 如果你不想用云服务，那可以考虑 [autounseal-transit](https://learn.hashicorp.com/tutorials/vault/autounseal-transit)

简单起见，也可以写个 crontab  或者在 CI 平台上加个定时任务去执行解封命令，以实现自动解封。

## 三、Vault 自身的配置管理

Vault 本身是一个复杂的 secrets 工具，它提供了 **Web UI** 和 **CLI** 用于手动管理与查看 Vault 的内容。

但是作为一名 DevOps，我们当然更喜欢自动化的方法，这有两种选择:

- 使用 vault 的 sdk: python-[hvac](https://github.com/hvac/hvac)
- 使用 [terraform-provider-vault](https://github.com/hashicorp/terraform-provider-vault) 或者 [pulumi-vault](https://github.com/pulumi/pulumi-vault) 实现 vault 配置的自动化管理。

Web UI 适合手工操作，而 sdk/`terraform-provider-vault` 则适合用于自动化管理 vault. 

我们的测试环境就是使用 `pulumi-vault` 完成的自动化配置 vault policy 和 kubernetes role，然后自动化注入所有测试用的 secrets.


### 1. 使用 pulumi 自动化配置 vault

使用 pulumi 管理 vault 配置的优势是很大的，因为云上资源的敏感信息（数据库账号密码、资源 ID、RAM子账号）都是 pulumi 创建的。

再结合使用 pulumi_valut，就能实现敏感信息自动生成后，立即保存到 vault 中，实现完全自动化。

后续微服务就可以通过 kubernetes 认证，直接从 vault 读取敏感信息。

或者是写入到本地的 vault 中留做备份，在需要的时候，管理员能登入进去查看相关敏感信息。

#### 1.1 Token 的生成

pulumi_vault 本身挺简单的，声明式的配置嘛，直接用就是了。

但是它一定要求提供 `VAULT_TOKEN` 作为身份认证的凭证（实测 userpass/approle 都不能直接使用，会报错 `no vault token found`），而且 pulumi 还会先生成临时用的 child token，然后用这个 child token
进行后续的操作。

首先安全起见，肯定不应该直接提供 root token！root token 应该封存，除了紧急情况不应该启用。

那么应该如何生成一个权限有限的 token 给 vault 使用呢？
我的方法是创建一个 userpass 账号，通过 policy 给予它有限的权限。
然后先手动(或者自动)登录获取到 token，再将 token 提供给 pulumi_vault 使用。

这里面有个坑，就是必须给 userpass 账号创建 child token 的权限：

```hcl
path "local/*" {
  capabilities = ["read", "list"]
}

// 允许创建 child token
path "auth/token/create" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

不给这个权限，pulumi_vault 就会一直报错。。


## 四、在 Kubernetes 中使用 vault 注入敏感配置

### 1. 部署并配置 vault agent

前面提到过 vault 支持通过 Kubernetes 的 ServiceAccount + Role 为每个 Pod 单独分配权限。

首先启用 Vault 的 Kubernetes 身份验证:

```shell
# 配置身份认证需要在 vault pod 中执行，启动 vault-0 的交互式会话
kubectl exec -n vault -it vault-0 -- /bin/sh
export VAULT_TOKEN='<your-root-token>'
export VAULT_ADDR='http://localhost:8200'
 
# 启用 Kubernetes 身份验证
vault auth enable kubernetes

# kube-apiserver API 配置，vault 需要通过 kube-apiserver 完成对 serviceAccount 的身份验证
vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

#### 1.1 使用集群外部的 valut 实例

>如果你没这个需求，请跳过这一节。

>详见 [Install the Vault Helm chart configured to address an external Vault](https://learn.hashicorp.com/tutorials/vault/kubernetes-external-vault?in=vault/kubernetes#install-the-vault-helm-chart-configured-to-address-an-external-vault)

kubernetes 也可以和外部的 vault 实例集成，集群中只部署 vault-agent.

这适用于多个 kubernetes 集群以及其他 APP 共用一个 vault 实例的情况，比如我们本地的多个开发测试集群，就都共用着同一个 vault 实例，方便统一管理应用的 secrets.

首先，使用 helm chart 部署 vault-agent，接入外部的 vault 实例。使用的 `custom-values.yaml` 示例如下：

```yaml
global:
  # enabled is the master enabled switch. Setting this to true or false
  # will enable or disable all the components within this chart by default.
  enabled: true
  # TLS for end-to-end encrypted transport
  tlsDisable: false

injector:
  # True if you want to enable vault agent injection.
  enabled: true

  replicas: 1

  # If multiple replicas are specified, by default a leader-elector side-car
  # will be created so that only one injector attempts to create TLS certificates.
  leaderElector:
    enabled: true
    image:
      repository: "gcr.io/google_containers/leader-elector"
      tag: "0.4"
    ttl: 60s

  # If true, will enable a node exporter metrics endpoint at /metrics.
  metrics:
    enabled: false

  # External vault server address for the injector to use. Setting this will
  # disable deployment of a  vault server along with the injector.
  # TODO 这里的 https ca.crt 要怎么设置？mTLS 又该如何配置？
  externalVaultAddr: "https://<external-vault-url>"

  # Mount Path of the Vault Kubernetes Auth Method.
  authPath: "auth/kubernetes"

  certs:
    # secretName is the name of the secret that has the TLS certificate and
    # private key to serve the injector webhook. If this is null, then the
    # injector will default to its automatic management mode that will assign
    # a service account to the injector to generate its own certificates.
    secretName: null

    # caBundle is a base64-encoded PEM-encoded certificate bundle for the
    # CA that signed the TLS certificate that the webhook serves. This must
    # be set if secretName is non-null.
    caBundle: ""

    # certName and keyName are the names of the files within the secret for
    # the TLS cert and private key, respectively. These have reasonable
    # defaults but can be customized if necessary.
    certName: tls.crt
    keyName: tls.key
```

部署命令和 [通过 helm 部署 vault](#install-by-helm) 一致，只要更换 `custom-values.yaml` 就行。

vault-agent 部署完成后，第二步是为 vault 创建 serviceAccount、secret 和 ClusterRoleBinding，以允许 vault 审查 kubernetes 的 token, 完成对 pod 的身份验证. yaml 配置如下：

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-auth
  namespace: vault
---
apiVersion: v1
kind: Secret
metadata:
  name: vault-auth
  namespace: vault
  annotations:
    kubernetes.io/service-account.name: vault-auth
type: kubernetes.io/service-account-token
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: role-tokenreview-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: vault-auth
    namespace: vault
```

现在在 vault 实例这边，启用 kubernetes 身份验证，在 vault 实例内，执行如下命令：

```shell
export VAULT_TOKEN='<your-root-token>'
export VAULT_ADDR='http://localhost:8200'
 
# 启用 Kubernetes 身份验证
vault auth enable kubernetes
 
# kube-apiserver API 配置，vault 需要通过 kube-apiserver 完成对 serviceAccount 的身份验证
# TOKEN_REVIEW_JWT: 就是我们前面创建的 secret `vault-auth`
TOKEN_REVIEW_JWT=$(kubectl get secret vault-auth -o go-template='{{ .data.token }}' | base64 --decode)
# kube-apiserver 的 ca 证书
KUBE_CA_CERT=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode)
# kube-apiserver 的 url
KUBE_HOST=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.server}')

vault write auth/kubernetes/config \
        token_reviewer_jwt="$TOKEN_REVIEW_JWT" \
        kubernetes_host="$KUBE_HOST" \
        kubernetes_ca_cert="$KUBE_CA_CERT"
```

这样，就完成了 kubernetes 与外部 vault 的集成！

### 2. 关联 k8s rbac 权限系统和 vault

接下来需要做的事：

2. 通过 vault policy 定义好每个 role（微服务）能访问哪些资源。
3. 为每个微服务生成一个 role，这个 role 需要绑定对应的 vault policy 及 kubernetes serviceaccount
   1. 这个 role 是 vault 的 kubernetes 插件自身的属性，它和 kubernetes role 没有半毛钱关系。
4. 创建一个 ServiceAccount，并使用这个 使用这个 ServiceAccount 部署微服务

其中第一步和第二步都可以通过 vault api 自动化完成.
第三步可以通过 kubectl 部署时完成。

方便起见，vault policy / role / k8s serviceaccount 这三个配置，都建议和微服务使用相同的名称。

>上述配置中，role 起到一个承上启下的作用，它关联了 k8s serviceaccount 和 vault policy 两个配置。

比如创建一个名为 `my-app-policy` 的 vault policy，内容为:

```hcl
# 命名规则："<engine-name>/data/<path>/*"
path "my-app/data/*" {
   # 只读权限
   capabilities = ["read", "list"]
}
```

然后在 vault 中创建 k8s role `my-app-role`:
1. 关联 k8s default 名字空间中的 serviceaccount `my-app-account`，并创建好这个 serviceaccount.
2. 关联 vault token policy，这就是前面创建的 `my-app-policy`
3. 设置 token period（有效期）

这之后，每个微服务就能通过 serviceaccount 从 vault 中读取 `my-app` 中的所有信息了。

### 3. 部署 Pod

>参考文档：<https://www.vaultproject.io/docs/platform/k8s/injector>

下一步就是将配置注入到微服务容器中，这需要使用到 Agent Sidecar Injector。
vault 通过 sidecar 实现配置的自动注入与动态更新。

具体而言就是在 Pod 上加上一堆 Agent Sidecar Injector 的注解，如果配置比较多，也可以使用 configmap 保存，在注解中引用。

需要注意的是 vault-inject-agent 有两种运行模式：

1. init 模式: 仅在 Pod 启动前初始化一次，跑完就退出（Completed）
2. 常驻模式: 容器不退出，持续监控 vault 的配置更新，维持 Pod 配置和 vualt 配置的同步。

示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: my-app
  name: my-app
  namespace: default
spec:
  minReadySeconds: 3
  progressDeadlineSeconds: 60
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: my-app
  strategy:
    rollingUpdate:
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-configmap: my-app-vault-config
        vault.hashicorp.com/agent-init-first: 'true'  # 是否提前初始化
        vault.hashicorp.com/agent-inject: 'true'
        vault.hashicorp.com/agent-limits-cpu: 250m
        vault.hashicorp.com/agent-requests-cpu: 100m
        vault.hashicorp.com/secret-volume-path: /app/secrets
      labels:
        app: my-app
    spec:
      containers:
      - image: registry.svc.local/xx/my-app:latest
        imagePullPolicy: IfNotPresent
        # 此处省略若干配置...
      serviceAccountName: my-app-account
```

### 4. vault agent 配置

vault-agent 的配置，需要注意的有：

1. 如果使用 configmap 提供完整的 `config.hcl` 配置，注意 `agent-init`

vautl-agent 的 template 说明：

目前来说最流行的配置文件格式应该是 json/yaml，以 json 为例，
对每个微服务的 kv 数据，可以考虑将它所有的个性化配置都保存在 `<engine-name>/<service-name>/` 下面，然后使用如下 template 注入配置(注意这里使用了自定义的左右分隔符 `[[` 和 `]]`)：

```consul-template
{
    [[ range secrets "<engine-name>/metadata/<service-name>/" ]]
        "[[ printf "%s" . ]]": 
        [[ with secret (printf "<engine-name>/<service-name>/%s" .) ]]
        [[ .Data.data | toJSONPretty ]],
        [[ end ]]
    [[ end ]]
}
```
>template 的详细语法参见: https://github.com/hashicorp/consul-template#secret

>注意：v2 版本的 kv secrets，它的 list 接口有变更，因此在遍历 v2 kv secrets 时，
必须要写成 `range secrets "<engine-name>/metadata/<service-name>/"`，也就是中间要插入 `metadata`。
官方文档完全没提到这一点，我通过 wireshark 抓包调试，对照官方的 [KV Secrets Engine - Version 2 (API)](https://www.vaultproject.io/api-docs/secret/kv/kv-v2) 才搞明白这个。

这样生成出来的内容将是 json 格式，不过有个不兼容的地方：最后一个 secrets 的末尾有逗号 `,`
渲染出的效果示例：

```json
{
    "secret-a": {
  "a": "b",
  "c": "d"
},
    "secret-b": {
  "v": "g",
  "r": "c"
},
}
```

因为存在尾部逗号(trailing comma)，直接使用 json 标准库解析它会报错。
那该如何去解析它呢？我在万能的 stackoverflow 上找到了解决方案：**yaml 完全兼容 json 语法，并且支持尾部逗号！**

以 python 为例，直接 `yaml.safe_load()` 就能完美解析 vault 生成出的 json 内容。


## 五、使用 vault 管理阿里云的 RAM 账号体系

vault 可以接入各大云厂商的账号体系，显然可以用于管理阿里云的， 实现 ACCESS_KEY/SECRET_KEY 的自动轮转。

具体配置方法，待续。。。
