---
title: "2021 年年终总结"
date: 2020-12-12T23:45:00+08:00
draft: true
resources:
- name: "featured-image"
  src: "featured-image.png"

tags: ["总结"]
categories: ["随笔", "技术"]
---


## 闲言碎语

一晃一年又是过去了，大局上，今年我较好地实现了年初对自己的期许：「**拆破玉笼飞彩凤，顿开金锁走蛟龙。**」

从 W 公司离职后，我非常幸运地进了现在的公司，在融入新公司的过程中也是五味杂陈。
不过总体结果我自己还是挺满意的，目前工作已经步入正轨，也在新公司发现了非常多的机会。

## 生活

- 加入了我司的冲浪小分队，第一次冲浪、海边烧烤
- 定期团建，跟 SRE 小伙伴公款吃喝，今年下馆子次数估计是我去年的七八倍。
- 又买了双轮滑鞋，学会了倒滑、压步转向，复习了大学时学过的若干基础技巧。

## 技术

- 熟悉了新公司的文化与工作方式，这感觉是个很大的收获，我的工作方法有了很大的改善
- 接触并且熟悉了新公司的 AWS 线上环境，负责基于 K8s 的服务管理平台的开发及运维
  - 迭代这个服务管理平台时，用 Python 写了几个服务
- 参与 AWS 成本的分析与管控，有了一些不错的成果
- 学会了使用 Nginx，业余学习了下 Linux 网络接口、Iptables、容器网络
- 简单入门了 Go 以及 Rust，但是没怎么用上，又忘差不多了...


## 今年在技术方面的感受

- Istio 服务网格：体会到了它有点重，而且它的发展跟我们的需求不一定匹配
  - Sidecar 模式的成本太高了，在未调优的情况下，它会给服务带来 1/3 到 1/4 的成本提升，以及延迟上升
  - 比如切量权重固定为 100，不支持 pod 的 warm up，而它重点发展的虚拟机支持我们却完全不需要
  - 一直在思考是持续往 Istio 投入，还是换其他的方案
- 直接使用中心化网关替代 Istio Service Mesh 的方法不可取，会带来大量的跨区流量成本
  - 这其实是在模仿 Per-Node Proxy 的 Service Mesh 模式，但是目前几乎没有采用这个模式的 Service Mesh.
- 感觉 Cilium 推出的基于 eBPF 的 Service Mesh 才是未来的趋势（使用高级特性时会退化成 Per Node Proxy 模式），成本、延迟方面都吊打 Sidecar 模式的其他服务网格.
- K8s 集群管理这方面，发现了 K8s 集群升级的诸多不便
- WASM 与 Rust 蓬勃发展，未来可期
- 成本控制方面，体会到了 ARM 架构以及 Spot 竞价实例的好处
- 跨区流量成本有很大的潜在优化空间
  1. K8s 新特性：[Topology Aware Hints](https://kubernetes.io/docs/concepts/services-networking/topology-aware-hints/)
  2. Istio: [Locality Load Balancing](https://istio.io/latest/docs/tasks/traffic-management/locality-load-balancing/)

## 明年的展望

我看了下 2020 年总结中写的「展望」，大概只实现了 20% 不到。
今年感觉应该写得更聚焦一些，争取能实现 80%.

1. 熟练掌握 Go/Rust 语言，并用于至少一个项目中
2. 深入学习如下技术
   1. Kubernetes 源码
3. 网络技术
   1. 服务网格 Istio
   2. 代理工具 Envoy/APISIX
   3. 网络插件 Cilium + eBPF
4. AWS K8s 成本与服务稳定性优化
   4. Topology Aware Load-Balancing - 节约跨可用区/跨域的流量成本
   5. 实例类型优化：使用更合适的实例类型、CPU 架构（ARM/adm64）
   6. 推广 GRPC 协议
5. 打通本地开发环境与云上的运行环境：
   1. [nocalhost](https://github.com/nocalhost/nocalhost)
   2. [che](https://github.com/eclipse/che)
6. 探索新技术与可能性（优先级低）
   1. 基于 Kubernetes 的服务平台，未来的发展方向
      1. kubevela
      2. buildpack
      3. 是否应该推进 gitops
      4. openkruise
   2. Serverless 平台的进展
      1. Knative
      2. OpenFunction


