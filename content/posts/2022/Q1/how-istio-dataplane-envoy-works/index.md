---
title: "Istio 数据面 Envoy 是如何工作的"
date: 2022-03-30T00:11:21+08:00
draft: true
resources:
  - name: "featured-image"
    src: ".png"

tags: ["Istio", "Envoy", "Service Mesh", " 服务网格", "网络代理", "Kubernetes"]
categories: ["tech"]
series: ["云原生相关"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

本文着重分析，在数据面 Envoy 上，Istio 是如何实现上层抽象 VirtualService DestinationRule Gateway 等功能的：

- 作为一个反向代理，Envoy 如何处理监听、请求转发、HTTP/gRPC 负载均衡、限流限并发
- 作为一个正向代理，Envoy 如何处理 Pod 发送出去的数据

## 参考
