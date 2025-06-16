---
title: "KubeCon China 2025 见闻"
subtitle: "LLM, LLM, 还是 LLM"
description: ""
date: 2025-06-15T17:43:44+08:00
lastmod: 2025-06-15T17:43:44+08:00
draft: false

featuredImage: &featimg "featured-image.webp"
resources:
  - name: featured-image
    src: *featimg
authors: ["ryan4yin"]

tags: ["云原生", "Cloud-Native", "Kubernetes", "AI", "LLM", "OpenTelemetry"]

categories: ["tech"]
series: ["云原生相关"]
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

# 是否开启表格排序
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

今年 1 月底辞职后，在家过了个年，接着在上海、张家界、重庆、苏州、南京玩了一圈，4 月中旬才
回深圳开始找工作。本来看到 6 月就是 KubeCon China 2025，还不太确定自己到时候会不会有时间
去。不过很幸运，最后确定 offer 的公司非常重视技术，leader 在面试的时候就说看到我博客里写了
KubeCon 的经历，公司非常鼓励参加这种技术交流活动，去报个 Talk 也完全可以，公司报销所有费
用。

于是我在入职还没满一个月的时候，就直接公费出差去香港 KubeCon China 2025 玩了一圈（

> 也问过同事们是否有想法，但种种原因最后还是只有我一个人参加了（悲

<!--more-->

## TL;DR

简单的说，今年的 KubeCon China 几乎全都是聊 AI on Kubernetes 的，感觉都可以改名叫
CloudNative AI Con 了。

今年 KubeCon China 只有两天，Talks 明显比去年少了很多，几乎只有去年的一半，所以我也在线上
看了许多 KubeCon Europe 2025 的 Talks 作为补充。

总的来说我今年的感觉是：

- Kubernetes 已经成为一个相当成熟的基座，任何可以在 K8s 上跑的东西最终都会被搬到 K8s 上跑
  （
- AI 让 CloudNative 社区焕发了新生，围绕 AI 在过去两年间涌现了许多新的 CloudNative 项
  目。AI 话题已经成为了 KubeCon 绝对的主旋律。
  - AI 部署部分主要在讨论 AI 推理，关键技术点：分布式推理、扩缩容与 LLM-Aware 的负载均衡以
    及 AI 模型分发
  - AIOps 也有好几个讨论，简单的用法就是 ChatBot，复杂点的会尝试使用 Multi-Agent 完成更复
    杂的任务（比如云成本分析优化）。
    - 快手尝试在超大规模集群中利用 Logs/Metrcis 为每个服务训练一个模型用于动态调整 HPA，实
      现 SLA 与成本的平衡。
- OpenTelemetry 日渐成熟，已经很接近它统一 Logs/Traces/Metrics 三大 Signals 的目标了。
  - 目前已经出现了 Uptrace 之类的大一统观测平台，充分利用了 OTel 的标签来关联 Logs/Traces.
  - 当前的最佳实践是，在 Infra 层面仍然使用传统方式采集 Logs 与 Metrics，而在 APP 层面则改
    由 OTel 统一采集所有 Logs, Traces 与 Metrics，OTel 会通过 Span ID 把这些数据关联起来，
    而且标签语义完全一致。
- WASM 仍在探寻自己的应用场景，今年介绍的场景主要是在边缘侧跑小模型。

KubeCon China 2025 与 KubeCon Europe 2025 的视频列表如下：

- [KubeCon + CloudNativeCon China 2025 (Hong Kong) - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2P1xtALqTcCmRAa6142uERl)
- [KubeCon + CloudNativeCon Europe 2025(London) - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc)

视频相关的 PPT 可以在这里下载（NOTE: 不是所有 Talks 都会上传 PDF）：

- [KubeCon + CloudNativeCon China 2025 - Schedule](https://kccncchn2025.sched.com/)
- [KubeCon + CloudNativeCon Europe 2025 - Schedule](https://kccnceu2025.sched.com/)

接下来我会把我听过的一些比较有意思的内容分 Topic 大概介绍下，也会附上对应的视频跟可能的
PPT 链接。

## Talks

### 大一统的 LLM 推理解决方案

[Introducing AIBrix: Cost-Effective and Scalable Kubernetes Control Plane for VLLM - Jiaxin Shan & Liguang Xie, ByteDance](https://kccncchn2025.sched.com/event/1x5im/introducing-aibrix-cost-effective-and-scalable-kubernetes-control-plane-for-vllm-jiaxin-shan-liguang-xie-bytedance?iframe=no)

AIBrix 是一整套在 K8s 上跑 LLM 分布式推理的解决方案，它包含了：

- 分布式推理的部署
- LLM 扩缩容
- LLM 请求路由（负载均衡）
- 分布式 KV 缓存
  - 主要是中心化存储这些数据，减少对 HBM 显存的使用，降低显存需求。
- LoRa 的动态加载
- ...

AIBrix 目前放在了 vllm-project 项目下，stars 也不少，感觉项目还是挺健康的，值得关注。

### 分布式 LLM 推理的部署

[More Than Model Sharding: LWS & Distributed Inference - Peter Pan & Nicole Li, DaoCloud & Shane Wang, Intel ](https://kccncchn2025.sched.com/event/1x5i6/more-than-model-sharding-lws-distributed-inference-peter-pan-nicole-li-daocloud-shane-wang-intel?iframe=no&w=100%&sidebar=yes&bg=no)

全场最有意思的 Talks 之一，大概介绍了分布式推理的架构、优化点，以及 LWS 的优点与用法。

简单的说 LWS 是一个专门为 LLM 分布式推理的部署而设计的 CRD, 主要是支持了 LLM 任务的分组调
度。

NOTE: 看 issue AIBrix 还有跟 LWS 结合使用的可能性（甚至可能被官方支持）:
https://github.com/vllm-project/aibrix/issues/843#issuecomment-2728305020

### LLM 扩缩容与负载均衡

- [KubeCon EU 2025 - Optimizing Metrics Collection & Serving When Autoscaling LLM Workloads](https://www.youtube.com/watch?v=lefjb4Vnd8k&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=326)
  - 讲得挺风趣，不过可能我对这块比较熟悉，基本能猜到就是自定义业务 metrics + 用 KEDA 做
    custom metrics based scaling，所以就只是简单看了看。
- [KubeCon EU 2025 - Keynote: LLM-Aware Load Balancing in Kubernetes: A New Era of Efficiency - Clayton Coleman, Distinguished Engineer, Google & Jiaxin Shan, Software Engineer, Bytedance](https://www.youtube.com/watch?v=BBqDpqATcI0&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=26)
  - 很有意思，LLM 的请求跟传统的 API 请求区别非常大，主要点在于：
    - input 长度区别就非常大，有的请求 input 很简单，相对就很轻量，而有的可能直接丢一份
      PDF 或者别的超长文本输入。输出也同样如此，如果用户明确要求深度推理，可能会导致大量性
      能消耗。
    - 不同机器可能会使用不同的 GPU 类型，而这些 GPU 的性能各异。
    - 在一个支持多模型的平台上，不同模型的高低峰期也存在比较明显的区别。
  - 上面这些特征导致传统的负载均衡策略完全失效。

### AI 模型分发

[AI Model Distribution Challenges and Best Practices](https://kccncchn2025.sched.com/event/1x5hl/ai-model-distribution-challenges-and-best-practices-wenbo-qi-xiaoya-xia-peng-tao-ant-group-wenpeng-li-alibaba-cloud-han-jiang-kuaishou?iframe=no&w=100%&sidebar=yes&bg=no)

几位开发者聊怎么在集群里分发数百 GB 大小的 LLM 模型，业界目前的手段：

- dragonfly
- juicefs
- oci model spec + oci volume (k8s 1.33+)

### 可观测性

- [Antipatterns in Observability: Lessons Learned and How OpenTelemetry Solves Them - Steve Flanders, Splunk ](https://kccncchn2025.sched.com/event/1x5i3/antipatterns-in-observability-lessons-learned-and-how-opentelemetry-solves-them-steve-flanders-splunk?iframe=no&w=100%&sidebar=yes&bg=no)
  - 这位也讲得挺有意思，而且有干货。他列举的可观测性方面的 Antipatterns 有
    - Telemetry Data
      - Incomplete
        [Instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/) - 需要
        引入
        [zero-code](https://opentelemetry.io/docs/concepts/instrumentation/zero-code/) 的
        otel sdk 实现自动数据采集
        - metrcis/logs/metrics 三类 signals 不一定都默认启用，具体得看对应的 agent 实现情
          况
        - 在 k8s 中建议同时禁用将日志输出到 stdout 的功能以及传统的给 prometheus pull 的
          /metrics 端点，由 otel agent 全权负责 App-level 三大信号的处理。daemonset 模式的
          otel （或者 vector/fluentbit）则主要用于采集 sidecar/k8s 等 Infra-level 的日志。
      - Over-Instrumentation - 需要在 otel-collector 层过滤精简指标，再发送到对应的后端存
        储。
      - Inconsistent Naming Conventions - 全盘替换为 OpenTelemetry 方案，即可享受统一的命
        名。
    - Observability Platform
      - Vendor Lock-in - 只选用支持 OTel 标准的平台并使用 Otel 命名规范。
      - Tool Sprawl - 使用大一统的观测平台，如 Uptrace, 支持自动关联 Logs 与 Traces.
      - Underestimating Scalability Requirements - 使用 OTel 采集信号，并选用可拓展性好的
        后端存储，如 VictoriaMetrics.
    - Company Culture
      - Silos and Lack of Collaboration
      - Lack of Ownership & Accountability
- [KubeCon EU 2025 - From Logs To Insights: Real-time Conversational Troubleshooting for Kubernetes With GenAI - Tiago Reichert & Lucas Duarte, AWS](https://www.youtube.com/watch?v=7yhBBzVmPks)
  - 开场的 OnCall 小品就很真实... 不过 pod pending 1 分钟就电话告警有点夸张了...
  - 演完小品才开始讲正式内容，大体上就是把日志用 embed 模型编码后存在 OpenSearch 里做
    RAG，还给了 ChatBot k8s readonly 的权限（ban 掉了 secrets access），然后通过
    Deepseek/Claude 问答来解决问题。
  - 代码: <https://github.com/aws-samples/sample-eks-troubleshooting-rag-chatbot>
- [Portrait Service: AI-Driven PB-Scale Data Mining for Cost Optimization and Stability Enhancement - Yuji Liu & Zhiheng Sun, Kuaishou](https://kccncchn2025.sched.com/event/1x5jD/portrait-service-ai-driven-pb-scale-data-mining-for-cost-optimization-and-stability-enhancement-yuji-liu-zhiheng-sun-kuaishou?iframe=no)
  - 讲快手怎么在 20 万台机器的超大规模集群上做稳定性管理与性能优化。
  - 介绍得比较浅，大概就是会收集集群中非常多的信息，用一套大数据系统持续处理，再丢给后面训
    练专用模型，每个服务都可能有一个专门的资源优化模型，用它来做最终的资源优化。
  - 这一套可能太重了，可以借鉴，但是在我目前的工作场景中不太有用（规模太小）。

### Service Mesh

- [Revolutionizing Sidecarless Service Mesh With eBPF - Zhonghu Xu & Muyang Tian, Huawei ](https://kccncchn2025.sched.com/event/1x5iI/revolutionizing-sidecarless-service-mesh-with-ebpf-zhonghu-xu-muyang-tian-huawei)
  - 主要就讲 Huawei 自己搞的 Kmesh，有比较详细的讲底层的实现架构（其实跟去年 KubeCon 听过
    的内容几乎一样）。
  - 简单讲就是 Ambient Mode 通过 istio-cni（底层是 iptables）将流量拦截到用户态的 ztunnel
    进行 L4 流量处理，而 Kmesh 使用 eBPF 在内核层实现了这些 L4 的功能。另外还简单介绍了
    Cilium Service Mesh，是一个 Per-Node 的 Proxy，主要缺点是必须用 Cilium 网络插件，以及
    它的 CRD 过于原始，使用复杂。
  - Kmesh 也尝试用 eBPF 实现了 HTTP 协议的解析，但是这需要对内核打补丁，代价比较高。
- [KubeCon EU 2025 - Choosing a Service Mesh - Alex McMenemy & Dimple Thoomkuzhy, Compare the Market](https://www.youtube.com/watch?v=hegNjjatNTU)
  - 虽然我接触过的基本都用的 Istio，不过看看别人怎么做选择总没坏处
- [KubeCon EU 2025 - Navigating the Maze of Multi-Cluster Istio: Lessons Learned at Scale - Pamela Hernandez, BlackRock](https://www.youtube.com/watch?v=WpEkfVGWmd8)
  - Istio 多集群在挺多大公司有应用，之前面试就被问到过，可以玩玩看。
- [KubeCon EU 2025 - A Service Mesh Benchmark You Can Trust - Denis Jannot, solo.io ](https://www.youtube.com/watch?v=oi4TpxuIYXk)
  - 做一个好的 Benchmark 对比还挺费时间费精力的，还是直接看人家给的结果最方便（

### 安全性

[Keynote: Who Owns Your Pod? Observing and Blocking Unwanted Behavior at eBay With eBPF](https://kccncchn2025.sched.com/event/1x5jM/keynote-who-owns-your-pod-observing-and-blocking-unwanted-behavior-at-ebay-with-ebpf-jianlin-lv-ebay-liyi-huang-isovalent-at-cisco?iframe=no&w=100%&sidebar=yes&bg=no)

主要就介绍 cilium 家的 tetragon, 一个基于 eBPF 的 K8S 安全工具，跟 apparmor 感觉会有点类
似，但是能做到更精细的权限管理。

朋友跟我 Argue 这种工具不是很有必要，应该用 GitOps 流程，然后将安全检查前置在 CICD 流水线
中。

### 云成本分析与优化

[KubeCon EU 2025 - Autonomous Al Agents for Cloud Cost Analysis - Ilya Lyamkin, Spotify](https://www.youtube.com/watch?v=sTbJ1-x3_yc&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=345)

实现一个会自动做 Plan，编写 SQL 与 Python 进行云成本分析的 Multi-Agent 系统，很有参考价
值。

### WASM 相关

[Keynote: An Optimized Linux Stack for GenAI Workloads - Michael Yuan, WasmEdge](https://kccncchn2025.sched.com/event/1x5jJ/keynote-an-optimized-linux-stack-for-genai-workloads-michael-yuan-wasmedge?iframe=no&w=100%&sidebar=yes&bg=no)

讲怎么用 WasmEdge + LlamaEdge 在边缘设备上跑 LLM 小模型，还是挺有意思的。

### 如何搭建一个 AI 工作流

[KubeCon EU 2025 - Tutorial: Build, Operate, and Use a Multi-Tenant AI Cluster Based Entirely on Open Source](https://www.youtube.com/watch?v=Ab7mRoJYsMo&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=365)

长度超过一个小时的教程，IBM 出品。装了一堆东西，包括 Kueue, Kubeflow, PyTorch, Ray, vLLM,
and Autopilot

## Non-Tech

参加 KubeCon 其实不仅仅是听一听过去一年技术方面的变化与进展，还有个很重要的目的是跟各个方
向的开发者们 Social, 也可以说是某种大型网友见面会（

今年拉到了 [@scruelt], [@ox-warrior] 等几位朋友一起去 KubeCon 玩，然后在会场又陆续跟
[@cookie], [@rizumu], [@ayakaneko] 以及 [@dotnetfx35] 见面闲聊瞎扯了一波，收获了 [@rizumu]
跟 [@ayakaneko] 用 3D 打印机打印的 Kubernetes 跟 Go 小饼干各一枚，顺便传教了 NixOS（

{{<figure src="/images/kubecon-china-2025/istio-book-and-badge.jpg" title="拿到的 K8s/Go 小饼干以及 Istio 冰箱贴" width="80%">}}

Day 2 上午发现没啥想听的，发现有个 Peer Group Meeting 参加，不过需要先 sign up. 跟
[@scruelt] 一起去报了名，本来还担心只提前 20 分钟 sign up 会不会没机会了，结果到会议室发现
只有 3 个 mentors 在场，于是就我们俩跟他们随便闲聊 emmm 三位 mentors 分别是 [Nate
Waddington] （Head of Mentorship & Documentatio, Canada），[Kohei Ota]（CNCF Ambassador,
Japan）以及 [Amit DSouza]（co-founder of Odyssey Cloud, Australia），另外聊到半途一位
Cisico 的老哥也加入了进来。

基本就是闲聊，[@scruelt] 口语比我好，而且刚辞职也有许多问题想问，绝大部分话题都是他提出来
的。我因为最近诸事皆顺，反而没啥想问的。

{{<figure src="/images/kubecon-china-2025/peer_group_meeting.jpg" title="进了 Peer Group Meeting 发现只有 Mentors hhh" width="80%">}}

最后就放些图吧。

{{<figure src="/images/kubecon-china-2025/kubecon-china-welcome.jpg" title="欢迎光临 KubeCon China 2025" width="80%">}}
{{<figure src="/images/kubecon-china-2025/kubecon-t-shirts.jpg" title="先领个 T 恤嘿嘿" width="80%">}}
{{<figure src="/images/kubecon-china-2025/kubecon-china-coffee-break.jpg" title="茶歇时间" width="80%">}}
{{<figure src="/images/kubecon-china-2025/suse-mascot-plush-doll-2.jpg" title="SUSE 的毛绒玩具好想要！" width="80%">}}
{{<figure src="/images/kubecon-china-2025/suse-mascot-plush-doll.jpg" title="大 SUSE 上一只小 SUSE" width="80%">}}

{{<figure src="/images/kubecon-china-2025/talk-tetragon-observibility.jpg" title="用 tetragon 限制文件访问" width="80%">}}
{{<figure src="/images/kubecon-china-2025/llm-disaggregated-serving.jpg" title="LWS 的 Talk，在讲 PD 分离" width="80%">}}
{{<figure src="/images/kubecon-china-2025/status-of-ingress-nginx.jpg" title="Ingress-NGINX 终于要寿终正寝了" width="80%">}}

{{<figure src="/images/kubecon-china-2025/nitendo-switch-store-miku.jpg" title="Switch 店在宣传 Miku Boxing" width="80%">}}
{{<figure src="/images/kubecon-china-2025/nitendo-switch-store.jpg" title="累计有三个朋友 KubeCon 期间在这里买了 Switch 2，它这波血赚" width="80%">}}
{{<figure src="/images/kubecon-china-2025/photo_friends.jpg" title="面基成功！顺便传教 NixOS" width="80%">}}

{{<figure src="/images/kubecon-china-2025/kubecon-china-2025-gifts.jpg" title="我的所有'战利品' hhh" width="80%">}}

{{<figure src="/images/kubecon-china-2025/airplane-boarding.jpg" title="登机了，再见深圳" width="80%">}}
{{<figure src="/images/kubecon-china-2025/airplane-1.jpg" title="这是我第几次坐飞机来着？" width="80%">}}

总之玩得很开心，明年再见！

[@scruelt]: https://x.com/scruelt
[@cookie]: https://x.com/nowaits1
[@ox-warrior]: https://github.com/ox-warrior
[@rizumu]: https://x.com/OikawaRizumu
[@ayakaneko]: https://x.com/ayakaneko
[@dotnetfx35]: https://x.com/dotnetfx35
[Nate Waddington]: https://www.cncf.io/people/staff/?p=nate-waddington
[Kohei Ota]: https://www.cncf.io/people/ambassadors/?_sft_lf-country=jp&p=kohei-ota
[Amit DSouza]:
  https://events.linuxfoundation.org/kubecon-cloudnativecon-china/?p=amit-dsouza
