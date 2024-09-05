---
title: "KubeCon China 2024 之旅"
subtitle: ""
description: ""
date: 2024-08-27T10:10:22+08:00
lastmod: 2024-09-05T15:54:00+08:00
draft: false

resources:
  - name: "featured-image"
    src: "kubecon-china-2024-linus.webp"

tags: ["云原生", "Cloud-Native", "Kubernetes", "MultiCloud", "多云", "服务网格", "Istio"]

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

很早就有了解到今年的 KubeCon China 会在香港举办，虽然有些兴趣，但我最初是有被 KubeCon 高昂
的门票价格劝退了的。

有时候不得不相信运气的魔力，机缘巧合之下，我从朋友 @Kev 处得知了 KubeCon 的「最终用户门票
计划」并借此 0 元购了门票，又邀上了 [0xFFFF 社区](https://0xffff.one/) 的
[@Chever-John](https://0xffff.one/u/Chever-John)
[@0xdeadbeef](https://0xffff.one/u/0xdeadbeef) [@茗洛](https://0xffff.one/u/MingLLuo) 三位
朋友一起参加，在香港租了个 airbnb 住宿，期间也逛了香港城市中的不少地方，收货颇丰。

> 其实本来也尝试过邀请其他认识的朋友同事，但都因为种种原因无法参加，略感遗憾。

## TL;DR

本文多图，也挺多技术无关的内容，为了方便想了解技术的朋友，我先做个大致的总结。

从 KubeCon 回来后我又听了些 CNCF 其他的会议视频，其中比较有印象的是这几个：

- [Keynote: Cloud Native in its Next Decade - KubeCon Europe 2024](https://www.youtube.com/watch?v=9EARwoRStBY&list=PLj6h78yzYM2N8nw1YcqqKveySH6_0VnI0&index=4):
  聊了 CloudNative 的未来，结论跟这次在 KubeCon China 现场听到的内容类似。
- [Another Choice for Istio Multi-Cluster & Multi-Network Deployment Model - KubeCon Europe 2024](https://www.youtube.com/watch?v=2MFwz0WCnuE&list=PLj6h78yzYM2M3MubjXdYRsish04DcKKLT&index=7):
  提到了 Istio 多集群方案的痛点，介绍了中国移动的解决方案。我一直有想尝试多集群方案，但一
  直担心 hold 不住而不敢下手，这个视频给了我一些启发。
- [DRA in KubeVirt: Overcoming Challenges & Implementing Changes - KubeCon Europe 2024](https://www.youtube.com/watch?v=8JBwQ6T-ZKE&list=PLj6h78yzYM2NNl95W4Rtp0e0MX9FCw8RN&index=9):
  DRA 也是 K8s 中的新 API，这里介绍如何在 kubnevirt 中使用 DRA 解决一些问题。从这里能感觉
  到 K8s 这几年还是弄了不少新东西的。

结合 KubeCon China 三天的经历，以及上面这些视频的内容，我大概的感觉是：

1. （几乎）所有聊网络的人都在聊 eBPF, Envoy, Gateway API.
2. Istio 的 Ambient Mode 吸引了很多曾经因为 sidecar 性能问题而放弃使用服务网格的公司。
3. Karmada 多集群管理方案在许多公司得到了实际应用，挺多讲这个的。
4. AI 与 WASM 方面的演讲也有不少，但感觉有些无趣，可能是我对这方面不太感兴趣。
5. 蔚来汽车、中国移动等公司正在尝试将 K8s 应用在边缘计算场景（智能汽车、通信基站），但这些
   离普通互联网公司有点远。
6. 云原生的未来十年会变成什么样？
   - Kubernetes, Service Mesh 等过去十年的新兴技术，现在已经成为了「**Boring but useful
     infrastructrue**」，它们将是其他云原生技术潮流的基石，被广泛应用，但自身不会再有太多
     的变化。
   - AI, eBPF, WASM, Rust 等技术也将在未来十年走向成熟，取代 Kubernetes 当前的地位。

KubeCon China 2024 的会议视频将会陆续被添加到如下这个 Youtube Playlist 中，有兴趣的朋友可
以一观：

- [KubeCon + CloudNativeCon + Open Source Summit + AI_dev China 2024 - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2NcAGHRxgBHY8x3QTfnZQCv)

视频相关的 PPT 可以在这里下载：

- [KubeCon China 2024 - Schedule](https://kccncossaidevchn2024.sched.com/)

## 技术

这次我主要关注的是 Istio、Gateway API 相关的议题，最近在研究 Istio 的 Ambient Mode，因此希
望能够从会议中了解到更多的实现细节与其中的权衡。

三天下来听到的内容也很好的满足了我的期待，Istio / Envoy Gateway / Ingress Controller 的几
位核心贡献者分享了很多这些项目的最新进展，实现细节，以及未来的发展方向。

Ambient Mode 在最近 beta 了，是我关注的重点，总结下目前了解到的几个关键点：

1. [istio/ztunnel](https://github.com/istio/ztunnel): 一个 userspace 的 l4 proxy，仅支持处
   理 L4 流量。
   - ztunnel 会分别与上游和下游建立连接，导致 A <=> B 之间的一个连接会变成 A <=> ztunnel
     <=> ztunnel <=> B 三个连接，这也会带来性能开销。
   - 因为所有流量都经由 ztunnel 转发，更新 ztunnel 会导致短暂的流量中断。感觉比较好的解决
     方案是采用 recreate 的更新策略 + 滚动更新节点组下的所有节点来更新 ztunnel.
   - ztunnel 使用的 HBONE 协议强制启用 mTLS，无法关闭，对于不要求安全性的场景会带来额外的
     性能开销。
1. [istio/proxy](https://github.com/istio/proxy): 基于 envoy 的 l7 proxy，在 ambient mode
   下它被单独部署为一个 waypoint, 用于处理 L7 流量。
   - waypoint 架构下 proxy 与上下游 Pod 很可能在不同的节点上，这会导致比 sidecar 模式多一
     次网络跳转，可能带来性能损耗，以及跨 Zone 流量上涨。
   - waypoint 与 sidecar 都是 envoy，它是通过减少 envoy 容器的数量来达到减少资源消耗的目
     的。

以及一些其他方案：

- [kmesh](https://github.com/kmesh-net/kmesh): 架构类似 Ambient Mode，特点是完全使用 eBPF
  来实现 L4 proxy，好处是
  - eBPF 直接在内核空间修改网络包，不需要与上下游分别建立连接。因此性能更好，而且 eBPF 程
    序更新不会中断流量。
- [cilium service mesh](https://cilium.io/use-cases/service-mesh/): 特点是 per-node
  proxy，l7 的 envoy proxy 运行在每个节点上，而不是像 waypoint 一样单独通过 deployment 部
  署。但也存在一些问题：
  - per-node proxy 无法灵活地调整资源占用，可能会导致资源浪费。
  - 同一节点上的所有流量都由同一 envoy proxy 处理，无法实现 waypoint 那样的 namespace 级别
    的流量隔离。
  - 与 cilium cni 强绑定，必须使用 cilium cni 才能使用 cilium service mesh.
  - 据说使用起来较为复杂？

总体而言，KubeCon 是一次了解行业前沿技术动态、跟项目开发者及其他行业内的技术人面对面认识交
流的好机会，可以帮助自己提升技术视野，维持技术热情与动力，不至于局限在公司业务中闭门造车。

## 行程

### 1. 住宿

因为要在香港呆三天，衣食住行是必须要考虑的事情。这方面我拉上的几位朋友都比较有旅行住宿的经
验，我们最后在香港找了个离会场不远的 airbnb 住宿，最终的体验也是相当不错。房间干净整洁有格
调，虽然我觉得稍微有点小了，但朋友说这个空间在香港都是一家三四口住的标准，已经吊打同价位的
酒店了。

### Day 1

虽然提早定了住宿，做了点功课，但第一天就出了问题——深圳这边一直下雨导致 @Chever-John 的飞机
直接被取消，改订了另一趟航班也晚点。虽然正点到达了会场，但他一晚上就睡了俩小时，在深圳定的
前一晚的酒店也没住成。

说回正题，到了会场领完胸牌，我们就开始了为期三天的 KubeCon China 之旅。

具体的技术内容已经在前文总结过了，这里主要就贴些照片吧。

{{<figure src="/images/kubecon-china-2024/IMG20240821084905_20240905145523.webp" title="主会场过厅，海景不错的" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821143748_20240905145522.webp" title="去各会议室的过道，酒店的服务很到位" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821175102_20240905145522.webp" title="午休茶歇，吃饱喝足" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821181445_20240905145522.webp" title="冰镇饮料也可以随便喝，好哇" width="80%">}}
{{<figure src="/images/kubecon-china-2024/20240821-istio-and-modern-api-gateways-navigating-the-future-of-service-meshes.webp" title="几位大佬聊 Istio 与 Gateway API 的未来" width="80%">}}

然后晚上@茗洛带着我们逛了香港的诚品书店，书店好几层，但感兴趣的书不多。后面又逛了好多电子
商城、二次元周边店，我算是开了眼界，笑死。

{{<figure src="/images/kubecon-china-2024/IMG20240821192248_20240905145522.webp" title="《我推的孩子》" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821192314_20240905145522.webp" title="另一本" width="80%">}}

{{<figure src="/images/kubecon-china-2024/IMG20240821201008_20240905145523.webp" title="好多二次元钢琴谱，有《四月是我的谎言》" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821201059_20240905145522.webp" title="不知道逛到了哪，到处都是二次元周边" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202220_20240905145521.webp" title="轻小说书店 1" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202237_20240905145521.webp" title="轻小说书店 2" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202314_20240905145521.webp" title="轻小说书店 3" width="80%">}}

第一天就差不多是这样，听了点技术，晚上逛了逛香港，回去休息。

### Day 2

{{<figure src="/images/kubecon-china-2024/IMG20240822102713_20240905145521.webp" title="好多的 CNCF 贴纸，可以随便拿，我给同事也带了一些" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821215634_20240905145521.webp" title="我收获的 CNCF 贴纸" width="80%">}}

首先是听了华为的演讲，介绍了 Kmesh 的方案创新，技术细节讲得很赞。想看 PPT 与视频请移步
[用内核原生无边车架构彻底改变服务网格 - Xin Liu, Huawei Technologies Co., Ltd.](https://kccncossaidevchn2024.sched.com/event/1eYYm/revolutionizing-service-mesh-with-kernel-native-sidecarless-architecture-zhi-chang-yi-wu-jie-xin-liu-huawei-technologies-co-ltd)

{{<figure src="/images/kubecon-china-2024/IMG20240822110054_20240905145521.webp" title="华为介绍 Kmesh" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822111805_20240905145520.webp" title="介绍 Kmesh 如何借助 eBPF 实现热更新不中断连接" width="80%">}}

还听了晋涛老师的
[十年云原生之旅：容器技术和Kubernetes生态系统的演变 - Jintao Zhang, Kong Inc.](https://kccncossaidevchn2024.sched.com/event/1eYZg/a-decade-of-cloud-native-journey-the-evolution-of-container-technology-and-the-kubernetes-ecosystem-chang-daepjrekuberneteschang-xu-ni-zha-jintao-zhang-kong-inc)

{{<figure src="/images/kubecon-china-2024/IMG20240822162954_20240905145520.webp" title="晋涛不愧是行业老将，这么早就开始玩 Docker 了" width="80%">}}

然后晚上我们随便走了走逛了逛，看了看香港海边夜景。

{{<figure src="/images/kubecon-china-2024/IMG20240822213416_20240905145520.webp" title="香港夜景，相当繁华哪" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822213841_20240905145520.webp" title="灯红酒绿，游人如织" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822215218_20240905145520.webp" title="路上碰到了《商务印书馆》" width="80%">}}

### Day 3

第三天早上是我这次最期待的，Linus 的访谈，见到了本人，这次行程也圆满了。

{{<figure src="/images/kubecon-china-2024/IMG20240823093047_20240905145520.webp" title="Linus" width="80%">}}

第三天没什么我特别感兴趣的话题，听完 Linus 的访谈后随便逛了逛，跟几位 朋友合了个影，就搭地
铁回家了。

{{<figure src="/images/kubecon-china-2024/our-selfie.webp" title="咱的合影" width="80%">}}
{{<figure src="/images/kubecon-china-2024/our-pc-and-shark.webp" title="咱的 PC 与鲨鲨合影" width="80%">}}

另外朋友听了个 TiDB 的演讲，看 PPT 是有点意思的哈哈。

{{<figure src="/images/kubecon-china-2024/20240823-tidb-your-next-mysql-is-not-a-mysql.webp" title="TiDB" width="80%">}}

以及在项目展厅三天逛下来，我帆布袋领了四个，T恤领了三件，还有别的小礼品一堆，吃的喝的都不
用说了，管够。另外看网上不少信息说香港的服务业态度很差，但这家酒店可能星级比较高，体验还是
相当到位的。

总之，体验相当不错的，有机会的话明年还来！Love you, KubeCon China & Hong Kong！
