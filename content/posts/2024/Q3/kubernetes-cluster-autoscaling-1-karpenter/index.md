---
title: "Kubernetes 集群伸缩组件 - Karpenter"
subtitle: ""
description: ""
date: 2024-07-10T09:17:31+08:00
lastmod: 2024-09-05T16:05:00+08:00
draft: false

featuredImage: "karpenter.png"
resources:
  - name: featured-image
    src: "karpenter.png"
authors: ["ryan4yin"]

tags:
  [
    "云原生",
    "Cloud-Native",
    "Kubernetes",
    "MultiCloud",
    "多云",
    "自动扩缩容",
    "Karpenter",
    "Cluster-Autoscaler",
  ]

categories: ["tech"]
series: ["云原生相关"]
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

# 否开启表格排序
table:
  sort: false

toc:
  enable: true

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

## 前言

Kubernetes 具有非常丰富的动态伸缩能力，这体现在多个层面：

1. Workloads 的伸缩：通过 Horizontal Pod Autoscaler（HPA）和 Vertical Pod
   Autoscaler（VPA）等资源，可以根据资源使用情况自动调整 Pod 的数量和资源配置。
   - 相关项目：
     - [metrics-server](https://github.com/kubernetes-sigs/metrics-server): 采集指标数据供
       HPA 使用
     - [KEDA](https://github.com/kedacore/keda): 用于支持更多的指标数据源与触发方式
     - [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler): 提供 VPA 功能
1. Nodes 的伸缩：根据集群的负载情况，可以自动增加或减少 Nodes 的数量，以适应负载的变化。
   - 相关项目：
     - [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler): 目前最流行的
       Node 伸缩方案，支持绝大多数云厂商。
     - [karpenter](https://github.com/kubernetes-sigs/karpenter): AWS 捐给 CNCF 的一个新兴
       Node 伸缩方案，目前仅支持 AWS/Azure，但基于其核心库可以很容易地扩展支持其他云厂商。

本文主要介绍新兴 Node 伸缩与管理方案 Karpenter 的优势、应用场景及使用方法。

<!--more-->

## Karpenter 简介

Karpenter 项目由 AWS 于 2020 年创建，其目标是解决 AWS 用户在 EKS 上使用 Cluster Autoscaler
做集群伸缩时遇到的一些问题。在经历了几年发展后，Karnepnter 于 2023 年底被捐献给
CNCF（[kubernetes/org#4258](https://github.com/kubernetes/org/issues/4258)），成为目前
（2024/07/10）唯二的官方 Node 伸缩方案之一。

我于 2022 年 4 月在做 Spark 离线计算平台改造的时候尝试了 Karpenter v0.8.2，发现它的确比
Cluster Autoscaler 更好用，并在随后的两年中逐渐将它推广到了更多的项目中。目前我司在 AWS 云
平台上所有的离线计算任务与大部分在线服务都是使用 Karpenter 进行的集群伸缩。另外我还为
karpenter 适配了 K3s 与 DigitalOcean 云平台用于一些特殊业务，体验良好。

Karpenter 官方目前只有 AWS 与 Azure 两个云平台的实现，也就是说只有在这两个平台上 karpenter
才能开箱即用。但考虑到它在易用性与成本方面的优势以及在可拓展性、标准化方面的努力，我对它的
未来发展持乐观态度。

## Karpenter 与 Cluster Autoscaler 的对比

Cluster Autoscaler 是目前社区最流行的 Node 伸缩方案，基本所有云厂商的 Kubernetes 服务默认
都会集成它。

Karpenter 与 Cluster Autoscaler 的设计理念与实现方式有很大的不同。

Cluster Autoscaler 是 Kubernetes 平台上早期的集群伸缩方案，也是目前最流行的方案。但它做的
事情比较有限，**最大的问题是它本身并不直接管理集群的节点**，而是借助云厂商的伸缩组
（AutoScaling Group）或节点池（Node Pool）来间接地控制节点（云服务器）的数量。这样的设计导
致了一些问题：

1. **部署与维护比较繁琐**：需要先在云厂商的控制台上创建好伸缩组或节点池，然后再在
   Kubernetes 集群上部署 Cluster Autoscaler，并将伸缩组或节点池的名称等信息填写到 Cluster
   Autoscaler 的配置文件中。增删节点池时也需要走一遍这个流程。
1. **能力受限于云厂商的伸缩组或节点池服务**：如果云厂商的伸缩组或节点池服务不支持某些功
   能，那么 Cluster Autoscaler 也无法使用这些功能。
   - 举例来说，AWS EKS 的 Node Group 功能非常难用，毛病一大堆。但如果要用 Cluster
     Autoscaler，你就没得选，Node Group 再难用也只能忍着。

而 Karpenter 则完全从零开始实现了一套节点管理系统，它直接管理所有节点（云服务器，如 AWS
EC2），负责节点的创建、删除、修改等操作。

相较 Cluster Autoscaler, Karpenter 的优势主要体现在以下几个方面：

1. **声明式地定义节点池**: Karpenter 提供了一套 CRD 来定义节点池，用户只需要编写好 Yaml 配
   置部署到集群中，Karpenter 就会根据配置自动申请与管理节点。这比 Cluster Autoscaler 的配
   置要方便得多。
   - 以 AWS 为例，你简单地改几行 Yaml 配置，就可以修改掉节点池的实例类型、AMI 镜像、数量上
     下限、磁盘大小、节点 Labels 跟 Taints、EC2 Tags 等信息。
   - 借助 Flux 或 ArgoCD 等 GitOps 工具，你还可以实现自动化的节点池管理以及配置的版本控
     制。
1. **成本感知的节点管理**：Karpenter 不仅负责节点数量的伸缩，它还能根据节点的规格、负载情
   况、成本等因素来选择最优的节点类型，以达成成本、性能、稳定性之间的平衡。 - 具体而
   言，Karpenter 在成本优化方面具有这些 Cluster Autoscaler 不具备的功能：
   - **Spot/On-Demand 实例调整**: 在 AWS 上，Karpenter 可以设置为优先使用 Spot 实例，并在
     申请不到 Spot 实例时自动切换到 On-Demand 实例，从而大大降低成本。
   - **多节点类型支持**: Karpenter 支持在同一个集群中使用多种不同规格的节点，并且支持控制
     不同实例类型的优先级、数量或占比，以满足不同的业务需求。
   - **节点替换策略**：Karpenter 支持灵活的节点替换策略，可以通过 Yaml 控制每个节点池的节
     点替换条件、频率、比例等参数，以避免因节点替换导致的服务不可用。
   - **节点的生命周期管理**：Karpenter 支持定义节点的生命周期策略，可以根据节点的年龄、负
     载、成本等因素来决定节点的续租、下线、销毁等操作。而 Cluster Autoscaler 只能控制节点
     的数量，它不直接管理节点，也就做不到此类节点的精细管理。
   - **主动优化**：Karpenter 支持主动根据负载情况使用不同实例类型的节点替换高风险节点，或
     合并低负载节点，以节省成本。
   - **Pod 精细化调度**：Karpeneter 本身也是一个调度器，它能根据 Pod 的资源需求、优先
     级、Node Affinity、Topology Spread Constraints 等因素来申请节点并主动将 Pod 调度到该
     节点上。而 Cluster Autoscaler 只能控制节点的数量，并无调度能力。
1. **快速、高效**：因为 Karpenter 直接创建、删除节点，并且主动调度 Pod，所以它的伸缩速度与
   效率要比 Cluster Autoscaler 高很多。这是因为 Karpneter 能快速获知节点创建、删除、加入集
   群是否成功，而 Cluster Autoscaler 只能被动地等待云厂商的伸缩组或节点池服务完成这些操
   作，它无法主动感知节点的状态。

总之，个人的使用体验上，Karpenter 吊打了 Cluster Autoscaler.

## Karpenter 的使用

这部分建议直接阅读官方文档
[Karpenter - Just-in-time Nodes for Any Kubernetes Cluster](https://karpenter.sh/).

## 适配其他 Kubernetes 发行版与云服务商

如果你使用的是 Proxmox VE, Aliyun 等其他云平台，或者使用的是 K3s, Kubeadm 等非托管
Kubernetes 发行版，那么你就需要自己适配 Karpenter 了。

Karpenter 官方目前并未提供详细的适配文档，社区建议以用于测试的
[Kwok Provider](https://github.com/kubernetes-sigs/karpenter/tree/main/kwok) 为参考，自行
实现。Kwok 是一个极简的 Karpenter Provider 实现，更复杂的功能也可以参考 AWS 与 Azure 的实
现。

国内云服务方面, 目前已经有人做了 Aliyun 的适配，项目地址如下：

- [karpenter-provider-aliyun](https://github.com/cloudpilot-ai/karpenter-provider-alibabacloud)

对于个人 Homelab 玩家来说，使用 Proxmox VE + K3s 这个组合的用户应该会比较多。我个人目前正
在尝试为这个组合适配 Karpenter，希望能够在未来的文章中分享一些经验。项目地址如下：

- [ryan4yin/karpenter-provider-proxmox](https://github.com/ryan4yin/karpenter-provider-proxmox):
  因为我已经换了 KubeVirt, 这个项目缺乏开发动力,暂时搁置,并改为私有仓库了...

## Karpenter 与 Cluster API

[Cluster API (CAPI)](https://github.com/kubernetes-sigs/cluster-api) 是 Kubernetes 社区提
供的一个用于管理多集群的项目，从介绍上看，它跟 Karpenter 好像没啥交集。但如果你有真正了解
使用过 CAPI 的话，你会发现 Karpenter 与 CAPI 有一些功能上的重叠：

1. CAPI 的 Infrastructure Provider 专门负责处理云厂商相关逻辑的组件。Karpenter 的标准实现
   内也包含了 cloud provider 相关代码，还提供了 NodeClass 这个 CRD 用于设定云服务器相关的
   参数。
1. Cluster API Bootstrap Provider (CABP) 负责将云服务器初始化为 Kubernetes Node，实际上就
   是生成对应的 cloud-init user data. Karpenter 的 NodeClass 实现中同样也包含了 user data
   的生成逻辑。

Cluster API 的目标是多集群管理，并且它的设计上将 Bootstrap, ControlPlane 跟 Infrastructure
三个部分分离出来了，好处是方便各云厂商、各 Kubernetes 发行版的接入，但也导致了它的架构比较
复杂、出问题排查起来会比较麻烦。

> 历史案例：Istio 曾经就采用了微服务架构，结果因为性能差、维护难度高被不少人喷，后来才改成
> 了单体结构。

而 Karpenter 则是一个单体应用，它的核心功能被以 Go Library 的形式发布，用户需要基于这个库
来实现自己的云平台适配。这样的设计使得 Karpenter 的架构简单、易于维护。但这也意味着
Karpenter 的可扩展性、通用性不如 Cluster API.

从结果来看，现在 Cluster API 的生态相当丰富，从
[Provider Implementations - Cluster API Docs](https://cluster-api.sigs.k8s.io/reference/providers)
能看到已经有了很多云厂商、发行版的适配. 而 Karpenter 2023 年底才捐给 CNCF，目前只有 AWS 与
Azure 的实现，未来发展还有待观察。

那么有没有可能结合两者的优势呢？Kubernetes 社区其实就有类似的尝试：

- [Cluster API Karpenter Feature Group Notes](https://hackmd.io/@elmiko/ryR2VXR0n#Attendees)
- [Karpenter Provider Cluster API Open Questions](https://hackmd.io/vpC0MQr0SqaHzI_uqadVwQ?view)
- [elmiko/karpenter-provider-cluster-api](https://github.com/elmiko/karpenter-provider-cluster-api)

上面这个实验性质的项目尝试使用 Karpenter 作为 Cluster API 的 Node Autoscaler，取代掉现在的
Cluster Autoscaler.

我目前对 Cluster API 有些兴趣，但感觉它还是复杂了点。我更想试试在 Karpenter 的实现中复用
Cluster API 各个 Provider 的代码，快速适配其他云厂商与 Kubernetes 发行版。

## 参考资料

- [Cluster Autoscaling - Kubernetes Official Docs](https://kubernetes.io/docs/concepts/cluster-administration/cluster-autoscaling/)
