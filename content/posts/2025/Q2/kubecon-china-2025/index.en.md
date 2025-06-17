---
title: "KubeCon China 2025 Experience"
subtitle: "LLM, LLM, and More LLM"
description: ""
date: 2025-06-15T17:43:44+08:00
lastmod: 2025-06-15T17:43:44+08:00
draft: false

featuredImage: &featimg "featured-image.webp"
resources:
  - name: featured-image
    src: *featimg
authors: ["ryan4yin"]

tags: ["Cloud-Native", "Kubernetes", "AI", "LLM", "OpenTelemetry"]

categories: ["tech"]
series: ["Cloud-Native Related"]
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

# Enable table sorting
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

## Preface

After resigning at the end of January, I spent time at home for the Chinese New Year, then
traveled around Shanghai, Zhangjiajie, Chongqing, Suzhou, and Nanjing. I didn't return to
Shenzhen to start job hunting until mid-April. Initially, I wasn't sure if I would have
time to attend KubeCon China 2025 in June. However, I was fortunate that the company I
received an offer from highly values technology. During the interview, my leader mentioned
seeing my KubeCon experiences in my blog and said the company strongly encourages
participation in such technical exchange events, even supporting giving talks with full
expense coverage.

So, less than a month after joining, I went on a company-funded trip to KubeCon China 2025
in Hong Kong (:

> I asked my colleagues if they were interested, but for various reasons, I ended up being
> the only one attending (sad

<!--more-->

## TL;DR

In short, this year's KubeCon China was almost entirely focused on AI on Kubernetes - it
could have been renamed to CloudNative AI Con.

This year's KubeCon China was only two days long, with significantly fewer talks than last
year - almost half as many. As a result, I also watched many KubeCon Europe 2025 talks
online as a supplement.

Overall, my impressions this year were:

- Kubernetes has become a mature foundation - anything that can run on K8s will eventually
  be moved to K8s
- AI has brought new life to the CloudNative community, with many new CloudNative projects
  emerging around AI in the past two years. AI topics have become the absolute main theme
  of KubeCon.
  - The AI deployment section mainly discussed AI inference, with key technical points:
    distributed inference, scaling, and LLM-Aware load balancing, as well as AI model
    distribution
  - There were several discussions about AIOps, from simple ChatBot implementations to
    more complex Multi-Agent systems for tasks like cloud cost analysis and optimization
    - Kuaishou attempted to use Logs/Metrics to train a model for each service in their
      ultra-large-scale cluster to dynamically adjust HPA, achieving a balance between SLA
      and cost (if I remembered incorrectly, I take no responsibility hhh)
- OpenTelemetry is maturing and getting closer to its goal of unifying Logs/Traces/Metrics
  signals
  - Platforms like Uptrace have emerged as unified observability platforms, fully
    utilizing OTel's labels to correlate Logs/Traces
  - Current best practice is to still use traditional methods for collecting Logs and
    Metrics at the Infra level, while at the APP level, OTel handles all Logs, Traces, and
    Metrics, correlating them through Span ID with consistent label semantics
- WASM is still exploring its use cases, with this year's main focus being running small
  models at the edge

KubeCon China 2025 and KubeCon Europe 2025 video playlists:

- [KubeCon + CloudNativeCon China 2025 (Hong Kong) - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2P1xtALqTcCmRAa6142uERl)
- [KubeCon + CloudNativeCon Europe 2025(London) - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc)

Presentation slides can be downloaded here (NOTE: not all talks will have PDFs uploaded):

- [KubeCon + CloudNativeCon China 2025 - Schedule](https://kccncchn2025.sched.com/)
- [KubeCon + CloudNativeCon Europe 2025 - Schedule](https://kccnceu2025.sched.com/)

Next, I'll introduce some interesting content I heard, organized by topic, along with
corresponding video links and possible PPT links.

## Talks

### Unified LLM Inference Solution

[Introducing AIBrix: Cost-Effective and Scalable Kubernetes Control Plane for VLLM - Jiaxin Shan & Liguang Xie, ByteDance](https://kccncchn2025.sched.com/event/1x5im/introducing-aibrix-cost-effective-and-scalable-kubernetes-control-plane-for-vllm-jiaxin-shan-liguang-xie-bytedance?iframe=no)

AIBrix is a complete solution for running distributed LLM inference on K8s, including:

- Distributed inference deployment
- LLM scaling
- LLM request routing (load balancing)
- Distributed KV cache
  - Mainly centralized storage of this data to reduce HBM memory usage and lower memory
    requirements
- Dynamic LoRa loading
- ...

AIBrix is currently under the vllm-project, with a good number of stars, suggesting the
project is healthy and worth following.

### Distributed LLM Inference Deployment

[More Than Model Sharding: LWS & Distributed Inference - Peter Pan & Nicole Li, DaoCloud & Shane Wang, Intel](https://kccncchn2025.sched.com/event/1x5i6/more-than-model-sharding-lws-distributed-inference-peter-pan-nicole-li-daocloud-shane-wang-intel?iframe=no&w=100%&sidebar=yes&bg=no)

One of the most interesting talks, covering distributed inference architecture,
optimization points, and the advantages and usage of LWS.

Simply put, LWS is a CRD specifically designed for LLM distributed inference deployment,
mainly supporting group scheduling for LLM tasks.

NOTE: According to an issue, AIBrix might integrate with LWS (possibly with official
support): https://github.com/vllm-project/aibrix/issues/843#issuecomment-2728305020

### LLM Scaling and Load Balancing

- [KubeCon EU 2025 - Optimizing Metrics Collection & Serving When Autoscaling LLM Workloads](https://www.youtube.com/watch?v=lefjb4Vnd8k&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=326)
  - Quite entertaining, but since I'm familiar with this area, I could guess it was about
    custom business metrics + KEDA for custom metrics-based scaling, so I just skimmed
    through it
- [KubeCon EU 2025 - Keynote: LLM-Aware Load Balancing in Kubernetes: A New Era of Efficiency - Clayton Coleman, Distinguished Engineer, Google & Jiaxin Shan, Software Engineer, Bytedance](https://www.youtube.com/watch?v=BBqDpqATcI0&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=26)
  - Very interesting - LLM requests are very different from traditional API requests:
    - Input length varies greatly - some requests have simple inputs and are relatively
      lightweight, while others might include entire PDFs or other long text inputs.
      Outputs are similarly variable - if users request deep reasoning, it could lead to
      significant performance consumption
    - Different machines might use different GPU types with varying performance
    - In a multi-model platform, different models have distinct peak and off-peak periods
  - These characteristics make traditional load balancing strategies completely
    ineffective

### AI Model Distribution

[AI Model Distribution Challenges and Best Practices](https://kccncchn2025.sched.com/event/1x5hl/ai-model-distribution-challenges-and-best-practices-wenbo-qi-xiaoya-xia-peng-tao-ant-group-wenpeng-li-alibaba-cloud-han-jiang-kuaishou?iframe=no&w=100%&sidebar=yes&bg=no)

Developers discussing how to distribute LLM models of hundreds of GB in size within
clusters. Current industry approaches:

- dragonfly
- juicefs
- oci model spec + oci volume (k8s 1.33+)

### Observability

- [Antipatterns in Observability: Lessons Learned and How OpenTelemetry Solves Them - Steve Flanders, Splunk](https://kccncchn2025.sched.com/event/1x5i3/antipatterns-in-observability-lessons-learned-and-how-opentelemetry-solves-them-steve-flanders-splunk?iframe=no&w=100%&sidebar=yes&bg=no)
  - Very interesting and informative. The observability antipatterns he listed include:
    - Telemetry Data
      - Incomplete Instrumentation - need to introduce zero-code otel sdk for automatic
        data collection
        - metrics/logs/metrics signals aren't all enabled by default, depends on agent
          implementation
        - In k8s, it's recommended to disable both stdout logging and traditional
          prometheus pull /metrics endpoints, letting otel agent handle all App-level
          signals. Daemonset mode otel (or vector/fluentbit) mainly handles Infra-level
          logs
      - Over-Instrumentation - need to filter and streamline metrics at the otel-collector
        level before sending to backend storage
      - Inconsistent Naming Conventions - fully adopt OpenTelemetry solution for unified
        naming
    - Observability Platform
      - Vendor Lock-in - only choose platforms supporting OTel standards and use OTel
        naming conventions
      - Tool Sprawl - use unified observability platforms like Uptrace that support
        automatic Log-Trace correlation
      - Underestimating Scalability Requirements - use OTel for signal collection and
        choose scalable backend storage like VictoriaMetrics
    - Company Culture
      - Silos and Lack of Collaboration
      - Lack of Ownership & Accountability
- [KubeCon EU 2025 - From Logs To Insights: Real-time Conversational Troubleshooting for Kubernetes With GenAI - Tiago Reichert & Lucas Duarte, AWS](https://www.youtube.com/watch?v=7yhBBzVmPks)
  - The opening OnCall skit was very realistic... though getting a phone alert after 1
    minute of pod pending seems exaggerated...
  - After the skit, they covered the main content: encoding logs with embed models and
    storing in OpenSearch for RAG, giving the ChatBot k8s readonly permissions (banned
    secrets access), then using Deepseek/Claude for Q&A to solve problems
  - Code: <https://github.com/aws-samples/sample-eks-troubleshooting-rag-chatbot>
- [Portrait Service: AI-Driven PB-Scale Data Mining for Cost Optimization and Stability Enhancement - Yuji Liu & Zhiheng Sun, Kuaishou](https://kccncchn2025.sched.com/event/1x5jD/portrait-service-ai-driven-pb-scale-data-mining-for-cost-optimization-and-stability-enhancement-yuji-liu-zhiheng-sun-kuaishou?iframe=no)
  - Discussed how Kuaishou manages stability and performance optimization in their
    ultra-large-scale cluster of 200,000 machines
  - Covered relatively basic content - mainly collecting vast amounts of cluster
    information, processing through a big data system, then training dedicated models,
    with each service potentially having its own resource optimization model
  - This approach might be too heavy - worth learning from but not very useful in my
    current work scenario (scale too small)

### Service Mesh

- [Revolutionizing Sidecarless Service Mesh With eBPF - Zhonghu Xu & Muyang Tian, Huawei](https://kccncchn2025.sched.com/event/1x5iI/revolutionizing-sidecarless-service-mesh-with-ebpf-zhonghu-xu-muyang-tian-huawei)
  - Mainly covered Huawei's Kmesh, with detailed explanation of the underlying
    implementation architecture (actually very similar to what I heard at last year's
    KubeCon)
  - Simply put, Ambient Mode intercepts traffic to user-space ztunnel for L4 traffic
    processing through istio-cni (underlying iptables), while Kmesh implements these L4
    functions at the kernel level using eBPF. Also briefly introduced Cilium Service Mesh,
    a Per-Node Proxy, with main drawbacks being the requirement for Cilium network plugin
    and its primitive, complex CRDs
  - Kmesh also attempted to implement HTTP protocol parsing with eBPF, but this requires
    kernel patching, which is costly
- [KubeCon EU 2025 - Choosing a Service Mesh - Alex McMenemy & Dimple Thoomkuzhy, Compare the Market](https://www.youtube.com/watch?v=hegNjjatNTU)
  - While most of what I've encountered uses Istio, it's always good to see how others
    make their choices
- [KubeCon EU 2025 - Navigating the Maze of Multi-Cluster Istio: Lessons Learned at Scale - Pamela Hernandez, BlackRock](https://www.youtube.com/watch?v=WpEkfVGWmd8)
  - Multi-cluster Istio is used in quite a few large companies - I was asked about it in
    interviews, worth trying out
- [KubeCon EU 2025 - A Service Mesh Benchmark You Can Trust - Denis Jannot, solo.io](https://www.youtube.com/watch?v=oi4TpxuIYXk)
  - Creating a good benchmark comparison takes a lot of time and effort - it's most
    convenient to just look at the results others provide (:

### Ingress-Nginx

[The Next Steps for Ingress-NGINX and the Ingate Project - Jintao Zhang, Kong Inc.](https://kccncchn2025.sched.com/event/1x5hW/the-next-steps-for-ingress-nginx-and-the-ingate-project-jintao-zhang-kong-inc?iframe=no)

Ingress-NGINX is finally being retired, with its successor being InGate, though InGate is
currently almost empty (:

{{<figure src="/images/kubecon-china-2025/status-of-ingress-nginx.jpg" width="80%">}}

### Security

[Keynote: Who Owns Your Pod? Observing and Blocking Unwanted Behavior at eBay With eBPF](https://kccncchn2025.sched.com/event/1x5jM/keynote-who-owns-your-pod-observing-and-blocking-unwanted-behavior-at-ebay-with-ebpf-jianlin-lv-ebay-liyi-huang-isovalent-at-cisco?iframe=no&w=100%&sidebar=yes&bg=no)

Mainly introduced cilium's tetragon, an eBPF-based K8S security tool, somewhat similar to
apparmor but capable of more fine-grained permission management.

A friend argued that such tools aren't very necessary - we should use GitOps processes and
move security checks to the CICD pipeline.

### Cloud Cost Analysis and Optimization

[KubeCon EU 2025 - Autonomous Al Agents for Cloud Cost Analysis - Ilya Lyamkin, Spotify](https://www.youtube.com/watch?v=sTbJ1-x3_yc&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=345)

Implementation of a Multi-Agent system that automatically creates plans, writes SQL and
Python for cloud cost analysis - very valuable reference.

### WASM Related

[Keynote: An Optimized Linux Stack for GenAI Workloads - Michael Yuan, WasmEdge](https://kccncchn2025.sched.com/event/1x5jJ/keynote-an-optimized-linux-stack-for-genai-workloads-michael-yuan-wasmedge?iframe=no&w=100%&sidebar=yes&bg=no)

Discussed using WasmEdge + LlamaEdge to run small LLM models on edge devices - quite
interesting.

### How to Build an AI Workflow

[KubeCon EU 2025 - Tutorial: Build, Operate, and Use a Multi-Tenant AI Cluster Based Entirely on Open Source](https://www.youtube.com/watch?v=Ab7mRoJYsMo&list=PLj6h78yzYM2MP0QhYFK8HOb8UqgbIkLMc&index=365)

An hour-plus tutorial by IBM. Installed many components including Kueue, Kubeflow,
PyTorch, Ray, vLLM, and Autopilot

## Non-Tech

Attending KubeCon isn't just about listening to technical changes and progress from the
past year - it's also an important opportunity to socialize with developers from various
fields, kind of like a large-scale online friend meetup (:

This year, I got [@scruelt], [@ox-warrior], and other friends to come to KubeCon, and at
the venue, I met up with [@cookie], [@rizumu], [@ayakaneko], and [@dotnetfx35] for casual
chats. I received Kubernetes and Go cookies printed with 3D printers from [@rizumu] and
[@ayakaneko], and incidentally spread the word about NixOS (:

{{<figure src="/images/kubecon-china-2025/photo_friends.jpg" title="Meetup successful! Also spread the word about NixOS" width="80%">}}
{{<figure src="/images/kubecon-china-2025/istio-book-and-badge.jpg" title="K8s/Go cookies and Istio fridge magnets received" width="80%">}}

On Day 2 morning, I found there weren't many talks I wanted to attend, so I noticed there
was a Peer Group Meeting to join, though it required signing up first. I went with
[@scruelt] to sign up, and we were a bit worried that signing up just 20 minutes before
might be too late, but when we got to the meeting room, we found only 3 mentors present,
so we just chatted casually with them. The three mentors were [Nate Waddington] (Head of
Mentorship & Documentation, Canada), [Kohei Ota] (CNCF Ambassador, Japan), and [Amit
DSouza] (co-founder of Odyssey Cloud, Australia). A Cisco engineer also joined in halfway
through.

It was mostly casual conversation. [@scruelt]'s English is better than mine, and since he
just resigned, he had many questions to ask - he initiated most of the topics. As for me,
since everything has been going smoothly lately, I didn't have many questions to ask.

{{<figure src="/images/kubecon-china-2025/peer_group_meeting.jpg" title="Entered the Peer Group Meeting to find only Mentors hhh" width="80%">}}

Let's end with some photos.

{{<figure src="/images/kubecon-china-2025/kubecon-china-welcome.jpg" title="Welcome to KubeCon China 2025" width="80%">}}
{{<figure src="/images/kubecon-china-2025/kubecon-t-shirts.jpg" title="Got a T-shirt first hehe" width="80%">}}
{{<figure src="/images/kubecon-china-2025/kubecon-china-coffee-break.jpg" title="Coffee break time" width="80%">}}
{{<figure src="/images/kubecon-china-2025/suse-mascot-plush-doll-2.jpg" title="Want that SUSE plush toy!" width="80%">}}
{{<figure src="/images/kubecon-china-2025/suse-mascot-plush-doll.jpg" title="A small SUSE on a big SUSE" width="80%">}}

{{<figure src="/images/kubecon-china-2025/talk-tetragon-observibility.jpg" title="Using tetragon to restrict file access" width="80%">}}
{{<figure src="/images/kubecon-china-2025/llm-disaggregated-serving.jpg" title="LWS Talk, discussing PD separation" width="80%">}}

{{<figure src="/images/kubecon-china-2025/nitendo-switch-store-miku.jpg" title="Switch store promoting Miku Boxing" width="80%">}}
{{<figure src="/images/kubecon-china-2025/nitendo-switch-store.jpg" title="Three friends bought Switch 2 here during KubeCon, they made a killing" width="80%">}}

{{<figure src="/images/kubecon-china-2025/kubecon-china-2025-gifts.jpg" title="All my 'loot' hhh" width="80%">}}

{{<figure src="/images/kubecon-china-2025/airplane-boarding.jpg" title="Boarding, goodbye Shenzhen" width="80%">}}
{{<figure src="/images/kubecon-china-2025/airplane-1.jpg" title="How many times have I flown now?" width="80%">}}

Had a great time, see you next year!

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
