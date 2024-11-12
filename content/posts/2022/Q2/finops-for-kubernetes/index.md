---
title: "FinOps for Kubernetes - 如何拆分 Kubernetes 成本"
date: 2022-05-04T23:15:00+08:00
lastmod: 2022-05-05T19:31:00+08:00
draft: false

featuredImage: "finops-for-kubernetes.webp"
authors: ["ryan4yin"]

tags:
  [
    "云原生",
    "Kubernetes",
    "FinOps",
    "成本分析",
    "Kubecost",
    "MultiCloud",
    "多云",
    "多云财务管控",
  ]
categories: ["tech"]
series: ["云原生相关"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

> FinOps 是一种不断发展的云财务管理学科和文化实践，通过帮助工程、财务、技术和业务团队在数
> 据驱动的预算分配上进行协作，使成本预算能够产生最大的业务价值。

## 云计算成本管控

随着越来越多的企业上云，云计算的成本管控也越来越受关注。在讨论 Kubernetes 成本之前，先简单
聊下如何管控云计算成本，有一个新名词被用于形容这项工作——FinOps.

传统的数据中心的成本是比较固定的，所有的成本变动通常都伴随着硬件更替。而在云上环境就很不一
样了，由于云服务的按量收费特性，以及五花八门的计费规则，开发人员稍有不慎，云成本就可能会出
现意料之外的变化。另一方面由于计费的复杂性，业务扩容对成本的影响也变得难以预测。

目前的主流云服务商（AWS/GCP/Alicloud/...）基本都提供基于资源标签的成本查询方法，也支持将成
本导出并使用 SQL 进行细致分析。因此其实要做到快速高效的**云成本分析与管控**，主要就涉及到
如下几个点：

- **契合需求的标签规范**: 从公司业务侧需求出发，制定出合理的、多维度的
  （Department/Team/Product/...）、有扩展空间的标签规范，这样才能按业务侧需要进行成本分
  析。
- **资源标签的准确率**: 随着公司业务的发展，标签规范的迭代，标签的准确率总是会上下波动。而
  标签准确率越高，我们对云计算成本的管控能力就越强。

但是也存在许多特殊的云上资源，云服务商目前并未提供良好的成本分析手段，Kubernetes 集群成本
就是其中之一。

## Kubernetes 成本分析的难点

目前许多企业应该都面临着这样的场景：所有的服务都运行在一或多个 Kubernetes 集群上，其中包含
多条业务线、多个产品、多个业务团队的服务，甚至除了业务服务，可能还包含 CICD、数据分析、机
器学习等多种其他工作负载。而这些 Kubernetes 集群通常都由一个独立的 SRE 部门管理。

但是 Kubernetes 集群本身并不提供成本拆分的能力，我们只能查到集群的整体成本、每个节点组的成
本等这样粗粒度的成本信息，缺乏细粒度的成本分析能力。此外，Kubernetes 集群是一个非常动态的
运行环境，其节点的数量、节点规格、Pod 所在的节点/Zone/Region，都可能会随着时间动态变动，这
为成本分析带来了更大的困难。

这就导致我们很难回答这些问题：**每条业务线、每个产品、每个业务团队、或者每个服务分别花了多
少钱？是否存在资源浪费？有何优化手段**？

而 FinOps for Kubernetes，就是通过工程化分析、可视化成本分析等手段，来回答这些成本问题，分
析与管控 Kubernetes 的成本。

接下来我会先介绍下云上 Kubernetes 成本分析的思路与手段，最后再介绍如何使用 Kubecost 分析
Kubernetes 集群的成本。

要做好 Kubernetes 成本工作，有如下三个要点：

- 理解 Kubernetes 成本的构成，搞懂准确分析 Kubernetes 成本有哪些难点
- 寻找优化 Kubernetes 集群、业务服务的手段
- 确定 Kubernetes 集群的成本拆分手段，建立能快速高效地分析与管控集群成本的流程

## Kubernetes 成本的构成

以 AWS EKS 为例，它的成本有这些组成部分：

- AWS EKS 本身有 $0.1 per hour 的固定费用，这个很低
- EKS 的所有节点会收对应的 EC2 实例运行费用、EBS 数据卷费用
- EKS 中使用的 PV 会带来 EBS 数据卷的费用
- 跨区流量传输费用
  - 所有节点之间的通讯（主要是服务之间的互相访问），如果跨了可用区，会收跨区流量传输费用
  - EKS 中的服务访问其他 AWS 服务如 RDS/ElastiCache，如果是跨可用区，会收取跨区流量费用
  - 如果使用了 Istio IngressGateway 或 traefik 等网关层代理 Pod，那这些 Pod 与服务实例之
    间，有可能会产生跨区流量
- NAT 网关费用
  - EKS 中的容器如果要访问因特网，就需要通过 NAT 网关，产生 NAT 费用
  - 如果 VPC 未配置 endpoints 使访问 AWS 服务（dynamodb/s3 等）时直接走 AWS 内部网络，这些
    流量会经过 VPC 的 NAT 网关，从而产生 NAT 网关费用
  - 对于托管版 NAT 网关，费用又包含两部分：公网流量费 + NAT 数据处理费用。其中数据处理费用
    可通过自建 NAT 实例来缩减。
- 服务如果要对外提供访问，最佳实践是通过 aws-load-balancer-controller 绑定 AWS ALB, 这里会
  产生 ALB 费用
- 监控系统成本
  - Kubernetes 的监控系统是不可或缺的
  - 如果你使用的是 Datadog/NewRelic 等云服务，会造成云服务的成本；如果是自建 Prometheus，
    会造成 Prometheus 的运行成本，以及 Pull 指标造成的跨区流量成本

**总结下，其实就是三部分成本：计算、存储、网络**。其中计算与存储成本是相对固定的，而网络成
本就比较动态，跟是否跨区、是否通过 NAT 等诸多因素有关。

## Kubernetes 资源分配的方式

Kubernetes 提供了三种资源分配的方式，即服务质量 QoS，不同的分配方式，成本的计算难度也有区
别：

- Guaranteed resource allocation(保证资源分配): 即将 requests 与 limits 设置为相等，确保预
  留所有所需资源
  - 最保守的策略，服务性能最可靠，但是成本也最高
  - 这种方式分配的资源，拆分起来是最方便的，因为它的计算成本是静态的
- Burstable resource allocation(突发性能): 将 requests 设置得比 limits 低，这样相差的这一
  部分就是服务的可 Burst 资源量。
  - 最佳实践，选择合适的 requests 与 limits，可达成性能与可靠性之间的平衡
  - 这种资源，它 requests 的计算成本是静态的，Burstable 部分的计算成本是动态的
- Best effort resource allocation(尽力而为): 只设置 limits，不设置 requests，让 Pod 可以调
  度到任何可调度的节点上
  - 下策，这个选项会导致服务的性能无法保证，通常只在开发测试等资源受限的环境使用
  - 这种方式分配的资源，完全依赖监控指标进行成本拆分

## 最佳实践

要做到统一分析、拆分 Kubernetes 与其他云资源的成本，如下是一些最佳实践：

- 按产品或者业务线来划分名字空间，不允许跨名字空间互相访问。
  - 如果存在多个产品或业务线共用的服务，可以在每个产品的名字空间分别部署一个副本，并把它们
    当成不同的服务来处理。
  - 这样名字空间就是成本划分的一个维度，我们还可以在名字空间上为每个产品设置资源上限与预
    警。
- 按产品或业务线来划分节点组，通过节点组的标签来进行成本划分
  - 这是第二个维度，但是节点组划分得太细，可能会导致资源利用不够充分。
  - 这个方案仅供参考，不一定好用
- 为 Kubernetes 服务设计与其他云资源一致的成本标签，添加到 Pod 的 label 中，通过 kubecost
  等手段，基于 label 进行更细致的成本分析
  - 标签一致的好处是可以统一分析 Kubernetes 与其他云资源的成本
- 定期（比如每周一） check 云成本变化，定位并解决成本异常
- 建立自动化的成本异常检测与告警机制（部分云服务有提供类似的服务，也可自建），收到告警即触
  发成本异常分析任务
- 始终将资源标签准确率维持在较高数值，准确率低于一定数值即自动告警，触发标签修正任务
- 将成本上升的压力与成本下降的效益覆盖到开发人员，授权他们跟踪服务的 Kubernetes 利用率与成
  本，以激励开发人员与 SRE 合作管控服务成本。

成本优化实践：

- 多种工作负载混合部署，提升资源利用率。但是需要合理规划避免资源竞争
- 调节集群伸缩组件，在保障 SLA 的前提下提升资源利用率
  - 比如 aws 就可以考虑在一些场景下用 karpenter 来做扩缩容、引入
    [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler) 提
    升 Spot 实例的 SLA
- 尽量使用竞价实例，AWS 的竞价实例单价平均优惠超过 50%
- 合理地购买 Saving Plans 与 Reserved Instances，达成成本节约。

## 多云环境

上述讨论的绝大部分策略，都适用于多云环境。在这种涉及多个云服务提供商的场景，最重要的一点
是：**搭建平台无关的成本分析与管控平台**。而其核心仍然是文章最前面提到的两点，只需要补充两
个字 **一致**：

- **一致的资源标签规范**: 从公司业务侧需求出发，制定出**跨平台一致的**标签规范，这样才能统
  一分析多云成本。
- **资源标签的准确率**: 随着公司业务的发展，标签规范的迭代，标签的准确率总是会上下波动。而
  标签准确率越高，我们对云计算成本的管控能力就越强。

这样就可以把不同云服务商的数据转换成统一的格式，然后在自有的成本平台上进行统一的分析了。

搭建一个这样的成本分析平台其实并不难，许多大公司都是这么干的，小公司也可以从一个最小的平台
开始做起，再慢慢完善功能。

以我现有的经验看，其实主要就包含这么几个部分：

- 成本数据转换模块：将来自不同云的成本数据，转换成与云服务无关的格式，方便统一处理
- 折扣模块：处理不同资源的折扣
  - 比如 CDN 在用量高的时候通常会有很高的折扣比例
  - 还有 SavingPlans/CommitmentDiscounts 也需要特殊的处理
- 标签修整模块
  - 随着标签体系的发展，总会有些标签的变更，不方便直接在资源上执行，就需要在成本计算这里进
    行修正、增补或者删除
- 成本拆分模块
  - 有些资源的成本是共用的，就需要结合其他来源的数据进行成本拆分，比如 Kubernetes 集群的成
    本
- 成本报表：将最终的数据制作成符合各类人员需求的可视化图表，按需求还可以考虑添加交互式特征
  - 可使用 Grafana/Google DataStudio 等报表工具

此外这样一个跨云的成本管控平台也不一定需要完全自己来做，已经有很多公司看到了这块的前景，做
出了现成的方案，可以看看 Gartner 的如下报告：

- [Cloud Management Tooling Reviews and Ratings - Gartner](https://www.gartner.com/reviews/market/cloud-management-tooling)

多云场景下其实要考虑的还有很多，目前多云网络（multicloud networking）、多云财务
（multicloud finops）、多云应用管理（multicloud application management）领域的需求越来越强
劲，相关产品也越来越多，有需要可以自行研究。

## Kubernetes 成本分析

前面讨论的内容都很「虚」，下面来点更「务实」的：Kubernetes 成本分析实战。

目前据我所知，主要有如下两个相关的开源工具：

- [Kubecost/Opencost](https://github.com/opencost/opencost): kubecost 应该是目前最优秀的开
  源成本分析工具了，self-hosted 是免费的，支持按 deployment/service/label 等多个维度进行成
  本拆分，而且支持拆分网络成本。收费版提供更丰富的功能以及更长的数据存储时间。
  - kubecost 的核心部分已捐献给 CNCF，并改名为 opencost.
- [crane](https://github.com/gocrane/crane): 腾讯开源的一款 Kubernetes 成本优化工具，支持
  成本报表以及 EHPA 两个功能，（截止 2022-05-04）才刚开源几个月，目前还比较简陋。
  - [腾讯推出国内首个云原生成本优化开源项目 Crane](https://cloud.tencent.com/developer/article/1960014)
  - 腾讯云在国内上线了 crane 的闭源版本
    「[容器服务成本大师](https://cloud.tencent.com/document/product/457/64169)」，如果你使
    用的是腾讯云，可以体验看看（感觉跟 kubecost 很像）

其中 kubecost 是最成熟的一个，我们接下来以 kubecost 为例介绍下如何分析 Kubernetes 成本。

### 安装 kubecost

kubecost 有两种推荐的安装方法：

- 使用 helm 安装免费版
  - 包含如下组件：
    - frontend 前端 UI 面板
    - cost-model 核心组件，提供基础的成本拆分能力
    - postgres 长期存储，仅企业版支持
    - kubecost-network-costs 一个 daemonset，提供网络指标用于计算网络成本（貌似未开源）
    - cluster-controller 提供集群「大小调整（RightSizing）」以及「定时关闭集群」的能力
  - 只保留 15 天的指标，无 SSO/SAML 登录支持，无 alerts/notification, 不可保存 reporters
    报表
  - 每个 kubecost 只可管理一个集群
- 只安装 Apache License 开源的 cost-model，它仅提供基础的成本拆分功能以及 API，无 UI 面
  板、长期存储、网络成本拆分、SAML 接入及其他商业功能。

开源的 cost-model 直接使用此配置文件即可部
署：<https://github.com/kubecost/cost-model/blob/master/kubernetes/exporter/exporter.yaml>

而如果要部署带 UI 的商业版，需要首先访问
<https://www.kubecost.com/install#show-instructions> 获取到 `kubecostToken`，然后使用 helm
进行部署。

首先下载并编辑 values.yaml 配置文
件：<https://github.com/kubecost/cost-analyzer-helm-chart/blob/develop/cost-analyzer/values.yaml>，
示例如下：

```yaml
# kubecost-values.yaml

# 通过 http://kubecost.com/install 获取 token，用于跟踪商业授权状态
kubecostToken: "xxx"

global:
  # 自动部署 prometheus + nodeExporter，也可以直接对接外部 prometheus
  prometheus:
    enabled: true
    # 如果 enable=false，则使用如下地址连接外部 prometheus
    fqdn: http://cost-analyzer-prometheus-server.default.svc

  # 自动部署 grafana，也可对接外部 grafana 面板
  grafana:
    enabled: true
    # 如果 enable=false，则使用如下地址连接外部 grafana
    domainName: cost-analyzer-grafana.default.svc
    scheme: "http" # http or https, for the domain name above.
    proxy: true # If true, the kubecost frontend will route to your grafana through its service endpoint

# grafana 子 chart 的配置
## 更好的选择是单独部署 grafana，不使用 kubecost 的 subchart
grafana:
  image:
    repository: grafana/grafana # 建议替换成私有镜像仓库地址
    tag: 8.3.2

# prometheus 子 chart 的配置
## 更好的选择是单独部署 prometheus，不使用 kubecost 的 subchart
prometheus:
  server:
    persistentVolume:
      enabled: true
      size: 32Gi # 这个大小得视情况调整，集群较大的话 32Gi 肯定不够
    retention: 15d # p8s 指标保留时长
  nodeExporter:
    enabled: true
    ## If true, node-exporter pods share the host network namespace
    hostNetwork: true
    ## If true, node-exporter pods share the host PID namespace
    hostPID: true
    ## node-exporter container name
    name: node-exporter
    ## node-exporter container image
    image:
      repository: quay.io/prometheus/node-exporter # 替换成 quay 仓库避免 docker 仓库拉取限制
      tag: v0.18.1
      pullPolicy: IfNotPresent

  ## Monitors ConfigMap changes and POSTs to a URL
  ## Ref: https://github.com/jimmidyson/configmap-reload
  ##
  configmapReload:
    prometheus:
      ## If false, the configmap-reload container will not be deployed
      enabled: true
      ## configmap-reload container name
      name: configmap-reload

      ## configmap-reload container image
      image:
        repository: jimmidyson/configmap-reload # 建议替换成私有仓库避免 docker 仓库拉取限制
        tag: v0.7.1

persistentVolume:
  enabled: true
  size: 32Gi # 同前所述
  # storageClass: "-" #

# 配置 ingress 入口，供外部访问
ingress:
  enabled: false
  # className: nginx
  annotations:
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  paths: ["/"] # There's no need to route specifically to the pods-- we have an nginx deployed that handles routing
  pathType: ImplementationSpecific
  hosts:
    - cost-analyzer.local

nodeSelector: {}

# 提升网络安全性的配置
networkPolicy:
  enabled: false
  denyEgress: true # create a network policy that denies egress from kubecost
  sameNamespace: true # Set to true if cost analyser and prometheus are on the same namespace
  # namespace: kubecost # Namespace where prometheus is installed

# 分析网络成本，需要额外部署一个 daemonset
networkCosts:
  enabled: false
  config: {} # 详见 values.yaml 内容

serviceAccount:
  create: true
  annotations:
    # 如果是 aws 上的集群，可以通过 serviceAccount 授权访问 ec2 pricing API 及 cur 数据
    # 也可以直接为服务提供 AccessKeyID/Secret 进行授权
    # 与 AWS 的集成会在后面详细介绍
    eks.amazonaws.com/role-arn: arn:aws:iam:112233445566:role/KubecostRole # 注意替换这个 role-arn

# 如下配置也可通过 Kubecost product UI 调整
# 但是此处的配置优先级更高，如果在这里配置了默认值，容器重启后就会使用此默认值，UI 上的修改将失效
kubecostProductConfigs: {}
```

然后部署：

```shell
# 添加 repo
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
# 查看版本号
helm search repo kubecost/cost-analyzer -l | head
# 下载并解压某个 chart
helm pull kubecost/cost-analyzer --untar --version 1.92.0
# 使用自定义 values 配置安装或更新本地的 chart
helm upgrade --create-namespace --install kubecost ./cost-analyzer -n kubecost -f kubecost-values.yaml
```

通过 port-forward 访问：

```shell
kubectl port-forward --namespace kubecost deployment/kubecost-cost-analyzer 9090
```

现在访问 <http://localhost:9090> 就能进入 Kubecost 的 UI 面板，其中最主要的就是 Allocation
成本拆分功能。

{{< figure src="/images/finops-for-kubernetes/kubecost-demo.webp" title="Kubecost 示例" >}}

### kubecost 的成本统计原理

#### 1. CPU/RAM/GPU/Storage 成本分析

Kubecost 通过 AWS/GCP 等云服务商 API 动态获取各 region/zone 的上述四项资源的每小时成
本：CPU-hour, GPU-hour, Storage Gb-hour 与 RAM Gb-hour，或者通过 json 文件静态配置这几项资
源的成本。OD 按需实例的资源价格通常比较固定，而 AWS Spot 实例的成本波动会比较大，可以通过
SpotCPU/SpotRAM 这两个参数来设置 spot 的默认价格，也可以为 kubecost 提供权限使它动态获取这
两项资源的价格。

kubecost 根据每个容器的资源请求 requests 以及资源用量监控进行成本分配，对于未配置 requests
的资源将仅按实际用量监控进行成本分配。

kubecost 的成本统计粒度为 container，而 deployment/service/namespace/label 只是按不同的维
度进行成本聚合而已。

#### 2. 网络成本的分析

> <https://github.com/kubecost/docs/blob/b7e9d25994ce3df6b3936a06023588f2249554e5/network-allocation.md>

对提供线上服务的云上 Kubernetes 集群而言，网络成本很可能等于甚至超过计算成本。这里面最贵
的，是跨区/跨域传输的流量成本，以及 NAT 网关成本。NAT 网关成本可以通过自建 NAT 实例来部分
缩减（这里仅考察了 AWS 云服务，其他云服务商的收费模式可能存在区别）。使用单个可用区风险比
较高，资源池也可能不够用，因此我们通常会使用多个可用区，这就导致跨区流量成本激增。

kubecost 也支持使用 Pod network 监控指标对整个集群的流量成本进行拆分，kubecost 会部署一个
绑定 hostNetwork 的 daemonset 来采集需要的网络指标，提供给 prometheus 拉取，再进行进一步的
分析。

kubecost 将网络流量分成如下几类：

- in-zone: 免费流量
- in-region: 跨区流量，国外的云服务商基本都会对跨区流量收费
- cross-region: 跨域流量

更多的待研究，看 kubecost 官方文档吧。

> 另外还看到 kubecost 有忽略 s3 流量（因为不收费）的 issue:
> <https://github.com/kubecost/cost-model/issues/517>

### kubecost API

> https://github.com/kubecost/docs/blob/b7e9d25994ce3df6b3936a06023588f2249554e5/apis.md

- 成本拆分文
  档：https://github.com/kubecost/docs/blob/b7e9d25994ce3df6b3936a06023588f2249554e5/cost-allocation.md
- 成本拆分 API 文
  档：https://github.com/kubecost/docs/blob/b7e9d25994ce3df6b3936a06023588f2249554e5/allocation.md

查询成本拆分结果的 API 示例：

```python
import requests
resp = requests.get("http://localhost:9090/model/allocation", params={
  "window": "2022-05-05T00:00:00Z,2022-05-06T00:00:00Z",
  "aggregate": "namespace,label:app",  # 以这几个纬度进行成本聚合
  "external": True,     # 拆分集群外部的成本（比如 s3/rds/es 等），需要通过其他手段提供外部资源的成本
  "accumulate": True,   # 累加指定 window 的所有成本
  "shareIdle": False,   # 将空闲成本拆分到所有资源上
  "idleByNode": False,  # 基于节点进行空闲资源的统计
  "shareTenancyCosts": True,  # 在集群的多个租户之间共享集群管理成本、节点数据卷成本。这部分成本将被添加到 `sharedCost` 字段中
  "shareNamespaces": "kube-system,kubecost,istio-system,monitoring",  # 将这些名字空间的成本设为共享成本
  "shareLabels": "",
  "shareCost": None,
  "shareSplit": "weighted",  # 共享成本的拆分方法，weight 加权拆分，even 均分
})

resp_json = resp.json()
print(resp_json['code'])

result = resp_json['data']
print(result[0])
```

查询结果中有这几种特殊成本类别：

- `__idle__`: 未被占用的空闲资源消耗的成本
- `__unallocated_`: 不含有 `aggregate` 对应维度的成本，比如按 `label:app` 进行聚合，不含有
  `app` 这个 label 的 pod 成本就会被分类到此标签
- `__unmounted__`: 未挂载 PV 的成本

此外如果使用 kubecost 可视化面板，可能还会看到一个 `other` 类别，这是为了方便可视化，把成
本太低的一些指标聚合展示了。

### Kubecost 与 AWS 集成

> https://github.com/kubecost/docs/blob/b7e9d25994ce3df6b3936a06023588f2249554e5/aws-cloud-integrations.md

> https://github.com/kubecost/docs/blob/main/aws-node-price-reconcilitation-methodology.md

TBD

## 参考

- [kubecost](https://github.com/kubecost/cost-model): kubecost 应该是目前最优秀的开源成本
  分析工具了，self-hosted 是免费的，也提供收费的云上版本，值得研究。
  - 文档：https://github.com/kubecost/docs
- [crane](https://github.com/gocrane/crane): 腾讯开源的一款 Kubernetes 成本优化工具，支持
  成本报表以及 EHPA 两个功能，才刚开源几个月，目前还比较简陋。
- [Calculating Container Costs - FinOps](https://www.finops.org/projects/calculating-container-costs/)
- [CPU利用率从10%提升至60%：中型企业云原生成本优化实战指南 - 星汉未来(Galaxy-Future)](https://zhuanlan.zhihu.com/p/523045177)
- [资源利用率分析和优化建议 - 腾讯云容器服务](https://cloud.tencent.com/document/product/457/57732)
