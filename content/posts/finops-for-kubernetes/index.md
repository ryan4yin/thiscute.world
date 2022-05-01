---
title: "FinOps for Kubernetes - 如何拆分 Kubernetes 成本"
date: 2022-04-29T01:15:24+08:00
lastmod: 2022-04-29T01:15:24+08:00
draft: true

resources:
- name: "featured-image"
  src: "featured-image.jpg"

tags: ["云原生", "Kubernetes", "FinOps", "成本分析"]
categories: ["技术"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

我在最近的大半年里，都在负责云计算成本方面的一些工作。
目前的主流云服务商（AWS/GCP/Alicloud/...）基本都提供基于资源标签的成本查询方法，也支持将成本导出并使用 SQL 进行细致分析。

因此其实要做到快速高效的成本分析与管控，主要就涉及到如下几个点：

- **契合需求标签规范**: 从公司业务侧需求出发，制定出合理的标签规范，这样才能按业务侧需要进行成本分析。
- **资源标签的准确率**: 随着公司业务的发展，标签规范的迭代，标签的准确率总是会上下波动。而标签准确率越高，我们对云计算成本的管控能力就越强。

而这其中有点特殊的一个云上资源，就是 Kubernetes 集群。
我们所有的线上业务都运行在同一个多租户 Kubernetes 集群上，可 Kubernetes 集群本身并不提供成本拆分的能力，这就导致我们很难回答这些问题：每个产品或者每个服务分别花了多少钱？是否存在资源浪费？有何优化手段？等等

而我在成本方面的一部分工作，就是通过人工分析、工程化分析等手段，来回答这些成本问题。

接下来我会从概念讲起，介绍我做云上 Kubernetes 成本分析的思路与手段，最后再介绍一个目前业界最优秀的 Kubernetes 成本分析工具 - kubecost.

主要包含如下三个核心问题：

- 理解云服务商的 Kubernetes 服务是如何收费的，了解为什么在 Kubernetes 集群上进行准确的成本拆分很有挑战性。
- 寻找优化 Kubernetes 集群、业务服务的手段
- 确定 Kubernetes 集群的成本拆分手段，建立能快速高效地分析与管控集群成本的流程。

## 从 FinOps 的角度看待 Kubernetes 成本




草稿暂时在这：

https://github.com/ryan4yin/knowledge/tree/master/kubernetes/finops


## 参考

- [kubecost](https://github.com/kubecost/cost-model): kubecost 应该是目前最优秀的开源成本分析工具了，self-hosted 是免费的，也提供收费的云上版本，值得研究。
- [crane](https://github.com/gocrane/crane): 腾讯开源的一款 Kubernetes 成本优化工具，支持成本报表以及 EHPA 两个功能，才刚开源几个月，目前还比较简陋。
- [Calculating Container Costs - FinOps](https://www.finops.org/projects/calculating-container-costs/)
