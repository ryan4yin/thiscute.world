---
title: "Kubernetes 网络是如何工作的 - 以 Calico 为例"
date: 2022-03-30T00:11:21+08:00
draft: true

resources:
- name: "featured-image"
  src: "featured-image.jpg"

tags: ["Kubernetes", "Linux", "容器", "网络", ""]
categories: ["技术"]
---

以 Calico 为例介绍 Kubernetes 网络如何工作：

- CNI 网络接口
- Iptables
- BGP 网络
- vxlan/ipip/geneve 等 overlay 网络



## 参考

- [数据包在 Kubernetes 中的一生（2）](https://blog.fleeto.us/post/life-of-a-packet-in-k8s-2/)
- [数据包在 Kubernetes 中的一生（3）](https://blog.fleeto.us/post/life-of-a-packet-in-k8s-3/)
