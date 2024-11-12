---
title: "KubeCon China 2024 Adventure"
subtitle: ""
description: ""
date: 2024-08-27T10:10:22+08:00
lastmod: 2024-09-05T15:54:00+08:00
draft: false

featuredImage: "kubecon-china-2024-linus.webp"
authors: ["ryan4yin"]

tags: ["Cloud-Native", "Kubernetes", "MultiCloud", "Service Mesh", "Istio"]
categories: ["tech"]
series: ["Cloud-Native Related"]

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

## Preface

I had known for a while that KubeCon China would be held in Hong Kong this year, and while
I was interested, I initially got deterred by the steep price of KubeCon tickets.

Sometimes you just have to believe in the magic of luck. By a twist of fate, I learned
about KubeCon's 'End User Ticket Program' from my friend @Kev and snagged a ticket for
free. I also invited three friends from the [0xFFFF Community](https://0xffff.one/),
[@Chever-John](https://0xffff.one/u/Chever-John),
[@0xdeadbeef](https://0xffff.one/u/0xdeadbeef), and
[@MingLLuo](https://0xffff.one/u/MingLLuo), to join in. We rented an Airbnb in Hong Kong,
explored quite a few places in the city, and had a fruitful trip.

> I also tried to invite other friends and colleagues, but they couldn't make it for
> various reasons, which was a bit of a bummer.

<!--more-->

## TL;DR

This post is heavy on images and some non-technical content. For friends who are more
interested in the tech side, let me give you a quick summary.

After returning from KubeCon, I also watched some other CNCF conference videos, and these
are the ones that left an impression:

- [Keynote: Cloud Native in its Next Decade - KubeCon Europe 2024](https://www.youtube.com/watch?v=9EARwoRStBY&list=PLj6h78yzYM2N8nw1YcqqKveySH6_0VnI0&index=4):
  Discussed the future of CloudNative, drawing conclusions similar to what was heard live
  at KubeCon China.
- [Another Choice for Istio Multi-Cluster & Multi-Network Deployment Model - KubeCon Europe 2024](https://www.youtube.com/watch?v=2MFwz0WCnuE&list=PLj6h78yzYM2M3MubjXdYRsish04DcKKLT&index=7):
  Addressed the pain points of Istio's multi-cluster solutions and introduced China
  Mobile's solution. I've always wanted to try multi-cluster solutions but hesitated due
  to concerns about manageability. This video provided some inspiration.
- [DRA in KubeVirt: Overcoming Challenges & Implementing Changes - KubeCon Europe 2024](https://www.youtube.com/watch?v=8JBwQ6T-ZKE&list=PLj6h78yzYM2NNl95W4Rtp0e0MX9FCw8RN&index=9):
  DRA is a new API in K8s, and this talk showed how to use it in kubevirt to solve some
  issues. It's evident that K8s has introduced quite a few new things in recent years.

Based on the three-day experience at KubeCon China and the content of the videos above,
here's my take:

1. Almost everyone discussing networking was talking about eBPF, Envoy, and Gateway API.
2. Istio's Ambient Mode attracted many companies that had previously given up on service
   meshes due to sidecar performance issues.
3. Karmada's multi-cluster management solution has been put into practical use by many
   companies and was a frequent topic of discussion.
4. There were also quite a few talks on AI and WASM, but I found them a bit boring as I'm
   not very interested in those areas.
5. Companies like NIO and China Mobile are trying to apply K8s in edge computing scenarios
   (smart cars, communication base stations), which seems a bit distant from ordinary
   internet companies.
6. What will the next decade of cloud native look like?
   - Technologies like Kubernetes and Service Meshes, which emerged over the past decade,
     have now become "**Boring but useful infrastructure**" and will serve as the
     foundation for other cloud native technology trends, widely used but not undergoing
     much change themselves.
   - Technologies such as AI, eBPF, WASM, and Rust will mature over the next decade,
     replacing Kubernetes' current position.

The KubeCon China 2024 conference videos will be added to the following YouTube Playlist
for those interested to watch:

- [KubeCon + CloudNativeCon + Open Source Summit + AI_dev China 2024 - Youtube](https://www.youtube.com/playlist?list=PLj6h78yzYM2NcAGHRxgBHY8x3QTfnZQCv)
  The PPTs related to the videos can be downloaded here:
- [KubeCon China 2024 - Schedule](https://kccncossaidevchn2024.sched.com/)

## Technical Insights

My main focus at the conference was on topics related to Istio and Gateway API. I've been
researching Istio's Ambient Mode recently and wanted to gain a deeper understanding of the
implementation details and trade-offs from the conference.

The three days of talks met my expectations well. Core contributors to Istio/Envoy
Gateway/Ingress Controller shared the latest advancements in these projects, as well as
implementation details and future development directions.

Ambient Mode is in beta and was a focal point for me. Here are some key points I've
gathered:

1. [istio/ztunnel](https://github.com/istio/ztunnel): A userspace L4 proxy that only
   handles L4 traffic.
   - ztunnel establishes connections separately with upstream and downstream, turning a
     single connection into three (A <=> ztunnel <=> ztunnel <=> B), which incurs
     performance overhead.
   - Since all traffic is forwarded through ztunnel, updating it can cause a brief traffic
     interruption. A good solution might be to use a recreate update strategy and roll out
     updates to all nodes in a node group.
   - ztunnel's use of the HBONE protocol enforces mTLS, which cannot be turned off, adding
     performance overhead in scenarios where security is not a concern.
2. [istio/proxy](https://github.com/istio/proxy): An L7 proxy based on Envoy, deployed
   separately as a waypoint in ambient mode to handle L7 traffic.
   - In the waypoint architecture, the proxy and the upstream/downstream Pods are likely
     on different nodes, leading to an additional network hop compared to the sidecar
     model, which may result in performance loss and increased cross-Zone traffic.
   - Both the waypoint and sidecar are envoy, and the goal is to reduce the number of
     envoy containers to decrease resource consumption.

And some other solutions:

- [kmesh](https://github.com/kmesh-net/kmesh): Similar to Ambient Mode in architecture, it
  uses eBPF exclusively for the L4 proxy, offering better performance as eBPF modifies
  network packets directly in the kernel space without establishing separate connections
  with upstream and downstream. Also, eBPF program updates do not interrupt traffic.
- [cilium service mesh](https://cilium.io/use-cases/service-mesh/): Features a per-node
  proxy with L7 envoy proxy running on each node, unlike the waypoint deployed separately
  via deployment. However, it has some issues:
  - The per-node proxy cannot flexibly adjust resource usage, potentially leading to
    resource wastage.
  - All traffic on the same node is processed by the same envoy proxy, unable to achieve
    namespace-level traffic isolation like the waypoint.
  - It is tightly bound to cilium cni and can only be used with cilium cni.
    - It is said to be more complex to use?

Overall, KubeCon was a great opportunity to learn about the latest trends in the industry,
meet developers of projects, and network with other tech professionals. It helped broaden
my technical horizons, maintain my enthusiasm and motivation for technology, and avoid
being insular in my company's business.

## Itinerary

### Accommodation

Since we were staying in Hong Kong for three days, accommodation was a necessary
consideration. My friends, who had experience with travel and lodging, helped us find an
Airbnb not far from the conference venue. The experience was quite pleasant; the room was
clean, tidy, and had a certain charm. Although I found it a bit small, my friends said
this space is the standard for a family of three or four in Hong Kong and was much better
than hotels in the same price range.

### Day 1

Even though we booked our accommodations in advance and did some homework, we hit a snag
on the first day – persistent rain in Shenzhen led to @Chever-John's flight being canceled
outright, and even the replacement flight was delayed. He arrived at the venue on time,
but he had only slept for two hours and didn't get to stay at the hotel he booked in
Shenzhen the night before. On the first day, he seemed pretty out of it during the
sessions. But hey, no worries – ~~at least I got to enjoy the talks to the fullest~.

Back to the main event, after picking up our badges, we kicked off our three-day KubeCon
China adventure.

The technical content has been summarized earlier, so here I'll just share some photos.

{{<figure src="/images/kubecon-china-2024/IMG20240821084905_20240905145523.webp" title="The main hall corridor, not a bad view of the sea" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821143748_20240905145522.webp" title="The corridor leading to various meeting rooms, the hotel service was spot on" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821175102_20240905145522.webp" title="Tea break during lunch, well-fed and watered" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821181445_20240905145522.webp" title="Chilled drinks were also on the house, awesome" width="80%">}}
{{<figure src="/images/kubecon-china-2024/20240821-istio-and-modern-api-gateways-navigating-the-future-of-service-meshes.webp" title="Several bigwigs discussing the future of Istio and Gateway API" width="80%">}}

In the evening, @Mingluo took us on a tour of the Eslite bookstore in Hong Kong. The
bookstore had several floors, but there weren't many books that caught my interest.a

Afterward, we visited a bunch of electronic malls and anime merchandise stores, which was
quite an eye-opener for me.

{{<figure src="/images/kubecon-china-2024/IMG20240821192248_20240905145522.webp" title="The cover of 'The Child I Pushed'" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821192314_20240905145522.webp" title="Another book cover" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821201008_20240905145523.webp" title="Lots of anime piano scores, including 'April is My Lie'" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821201059_20240905145522.webp" title="Not sure where we ended up, anime merchandise everywhere" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202220_20240905145521.webp" title="Light novel bookstore 1" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202237_20240905145521.webp" title="Light novel bookstore 2" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821202314_20240905145521.webp" title="Light novel bookstore 3" width="80%">}}

That's about it for day one – a bit of tech talk, some evening exploration in Hong Kong,
and then back to rest.

### Day 2

{{<figure src="/images/kubecon-china-2024/IMG20240822102713_20240905145521.webp" title="Loads of CNCF stickers, free to take, and I grabbed some for my colleagues too" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240821215634_20240905145521.webp" title="My collection of CNCF stickers" width="80%">}}

The day started with a talk by Huawei, introducing the innovative solution of Kmesh. The
technical details were presented very well. If you want to check out the PPT and video,
head over to
[Revolutionizing Service Mesh with Kernel Native Sidecarless Architecture - Xin Liu, Huawei Technologies Co., Ltd.](https://kccncossaidevchn2024.sched.com/event/1eYYm/revolutionizing-service-mesh-with-kernel-native-sidecarless-architecture-zhi-chang-yi-wu-jie-xin-liu-huawei-technologies-co-ltd)

{{<figure src="/images/kubecon-china-2024/IMG20240822110054_20240905145521.webp" title="Huawei presenting Kmesh" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822111805_20240905145520.webp" title="How Kmesh achieves hot updates without disconnecting using eBPF" width="80%">}}

I also listened to Mr. Jintao Zhang's talk on
[A Decade of Cloud Native Journey: The Evolution of Container Technology and the Kubernetes Ecosystem - Jintao Zhang, Kong Inc.](https://kccncossaidevchn2024.sched.com/event/1eYZg/a-decade-of-cloud-native-journey-the-evolution-of-container-technology-and-the-kubernetes-ecosystem-chang-daepjrekuberneteschang-xu-ni-zha-jintao-zhang-kong-inc)

{{<figure src="/images/kubecon-china-2024/IMG20240822162954_20240905145520.webp" title="Jintao Zhang, a veteran in the industry, has been playing with Docker since early days" width="80%">}}

In the evening, we took a casual walk and explored the city, checking out the night view
by the Hong Kong seaside.

{{<figure src="/images/kubecon-china-2024/IMG20240822213416_20240905145520.webp" title="Hong Kong's night scenery, quite bustling" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822213841_20240905145520.webp" title="Bright lights and bustling crowds" width="80%">}}
{{<figure src="/images/kubecon-china-2024/IMG20240822215218_20240905145520.webp" title="Came across the Commercial Press on the way" width="80%">}}

### Day 3

The highlight of the morning on the third day was the interview with Linus. Getting to see
him in person made my trip complete!

{{<figure src="/images/kubecon-china-2024/IMG20240823093047_20240905145520.webp" title="Linus" width="80%">}}

There weren't many topics that caught my interest on the third day. After Linus's
interview, I just wandered around, took a group photo with a few friends, and then took
the subway home.

{{<figure src="/images/kubecon-china-2024/our-selfie.webp" title="Our group selfie" width="80%">}}
{{<figure src="/images/kubecon-china-2024/our-pc-and-shark.webp" title="Our PC and Shark selfie" width="80%">}}

A friend of mine attended a TiDB talk, and the PPT looked pretty interesting, lol.

{{<figure src="/images/kubecon-china-2024/20240823-tidb-your-next-mysql-is-not-a-mysql.webp" title="TiDB" width="80%">}}

After three days of walking around the project exhibition hall, I scored four canvas bags,
three T-shirts, and a bunch of other small gifts. The food and drinks were more than
enough, no need to mention that. Also, I've read online that the service industry in Hong
Kong has a bad attitude, but this hotel might have been of a higher star rating, and the
experience was quite good.

All in all, the experience was quite enjoyable, and I'd love to come back next year if I
have the chance! Love you, KubeCon China & Hong Kong!
