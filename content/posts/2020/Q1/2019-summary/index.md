---
title: "2019 年年终总结"
date: 2020-01-31T19:19:00+08:00
draft: false
resources:
  - name: "featured-image"
    src: "beginning-the-devops-journey.webp"

tags: ["总结"]
categories: ["life", "tech"]
series: ["年终总结"]
---

> 迟到的年终总结

## 闲言碎语

我是今年六月底到的深圳，运气很好，第一面就面上了现在所在的公司，以下就叫它 W 公司吧。
公司的技术栈也很适合我，在入职到现在的这半年里，我学到了不少知识。

但是运气也差，只有这么一家公司约了我面试，投的其他简历都石沉大海...

总之，今年尝试参加过两次技术分享，Rancher 的技术沙龙，前几天又去听了 OSChina 的源创会。

## 技术能力总结

我入职后做的是运维开发，主要负责通过 Jenkins Pipeline + Python 进行自动化的测试、构建和部署：

1. 测试：指 UI 测试、API 测试、压力测试。单元测试算在构建流程中。
1. 构建：更新依赖->单元测试->构建 Library 或镜像
   - 公司的内部代码使用分层结构，底层封装了各种第三方包，并实现了一些通用的功能，形成了所谓的**中台**。目前是通过批量任务逐级自下向上构建。
1. 部署：扫描镜像仓库中各镜像，生成最新的 k8s 部署文件，然后进行部署。

所以这半年中，我差不多熟悉了自动化运维的工作。主要包括

1. Jenkins Pipeline 的编写，我们基本都是使用 Jenkins 调用 Python 代码来进行具体的构建。
   - 公司的构建有很多自己特殊的需求，Jenkins 自带的插件无法满足。
1. 熟悉了 Python 的 subprocess 库，为了远程调用，又熟悉了 fabric（当作 library 用）。
1. 做压测时，熟悉了 locust
1. 因为基本都是通过命令行进行测试、构建，我现在比前后端组还熟悉 csharp/flutter/golang 的 cli...
1. 学会了 Dockerfile 语法。我们的后端全部都是以容器方式部署的，这个是基本技能。
1. 熟悉并且用上了 Kubernetes. 这东西基本上就是未来了，也将是我的主攻方向。

但是，也存在一些问题：

1. 对 Linux/网络/vSphere 不够了解，导致每次处理这类问题只会排除法。
1. 对监控/日志/告警不够了解，监控面板一堆参数却看不出问题，日志不知道怎么用 kibana 进行搜索，告警还没配过。。
1. 解决问题的能力还有待提升，考虑总是不够全面，老是出问题。（不能让人放心）
1. 总是想得太多，拖慢了解决问题的速度。（这倒也不能完全算是缺点。）

## 今年在技术上的感受

1. Kubernetes 和云原生正在席卷整个互联网/物联网行业。
1. Kubernetes 目前主要用于 Stateless 应用，那后端的 数据库/缓存/消息服务 要如何做分布式呢？这也是大家关注的重点。
1. 分布式、微服务模式下的**监控(prometheus)、日志分析(elk)、安全、链路追踪(jaeger)**，是运维关注的重点。
1. 服务网格正在走向成熟，Istio 很值得学习和试用。
1. 开源的分布式数据库/云数据库成为越来越多企业的选择，开源的 TiDB（HTAP）和阿里云的 PolarDB（计算存储分离）都应该了解了解。
   - Transaction Processing: **面向交易**，数据的变动(增删改)多，涉及的数据量和计算量(查)少，实时性要求高。
   - Analytical Processing：**面向分析**，数据的变动少，但涉及的数据量和计算量很多！
   - HTAP（Hybrid transaction/analytical processing）：混合型数据库，可同时被用于上述两种场景。
1. Knative/Jenkins-X 这类 Serverless 的 CI/CD 也正在快速发展，需要深入调研。

## 明年的展望

作为一名萌新运维开发，明年显然还要继续在这条路上继续向前。

我明年的任务，第一件，就是优化掉部分自己目前存在的问题（前面有提到），第二呢，就是紧跟技术潮流。重点有下面几项：

1. 充实自己网络部分欠缺的知识，尤其是 DNS 解析(CoreDNS)和 NAT(iptables)这俩玩意儿。
1. 学习数据库组件的使用和性能调优：MySQL/Redis/ElasticSearch/MongoDB，另外熟悉 PostgreSQL 和分布式数据库 TiDB/Vitess
1. Kubernetes/Istio
1. Kubernetes 上的 CI/CD：Knative, [Istio-GitOps](https://github.com/stefanprodan/gitops-istio)
1. 监控告警：Prometheus/Grafana
1. 总结一套故障排除的方法论：网络故障、CPU/RAM/Disk 性能异常等、应用故障等。

最重要的任务，是维护公司这一套微服务在阿里云上的正常运行，积累经验。

关注 [CNCF 蓝图](https://landscape.cncf.io/) 上的各项新技术。

另外呢，就是开发方面的任务：

1. 设计模式应该要学学了！
1. Python 不能止步于此，要制定源码学习计划。
1. 学习 C# 语言，阅读公司的源码，熟悉企业级的业务代码。
1. 学习 go 语言，用于 DevOps。（其实还想学 rust，不过明年可能没时间）
1. 要把 xhup 那个项目完成，也不知道能不能抽出时间。。
