---
title: "Kubernetes 网络是如何工作的"
date: 2022-05-06T11:56:00+08:00
draft: true

resources:
- name: "featured-image"
  src: "kubernetes-networking.webp"

tags: ["Kubernetes", "Linux", "NAT", "网络", "内网穿透", "网络隧道", "Overlay 网络", "Underlay 网络", "wireguard"]
categories: ["tech"]
series: ["云原生相关"]
---


本文包含如下几个部分：

第二部分：

以 Calico 为例介绍 Kubernetes 网络如何工作（Overlay）：

- CNI 网络接口
- Iptables
- BGP 网络
- vxlan/ipip/geneve 等 overlay 网络

第三部分：

介绍 AWS EKS 与 VPC 整合的 Kubernetes 网络如何工作（Underlay）

第四部分：

- 多云 overlay 网络：[kilo](https://github.com/squat/kilo)
- 穿透进 Kubernetes 内网：将本地开发机器接入 Kubernetes 网络，用于开发调试

第五部分：

Network Policy


## 参考

关于 Kubernetes 网络：

- [数据包在 Kubernetes 中的一生（2）](https://blog.fleeto.us/post/life-of-a-packet-in-k8s-2/)
- [数据包在 Kubernetes 中的一生（3）](https://blog.fleeto.us/post/life-of-a-packet-in-k8s-3/)
- [kube-proxy IPVS 模式的工作原理 - 米开朗基扬](https://www.cnblogs.com/ryanyangcs/p/14888443.html)
