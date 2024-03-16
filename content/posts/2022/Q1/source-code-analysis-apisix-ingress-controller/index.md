---
title: "源码分析系列 - APISIX Ingress Controller"
date: 2022-03-30T00:11:21+08:00
draft: true

resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["网络代理", "网关", "源码分析", "APISIX", "Ingress", "Kubernetes"]
categories: ["tech"]
---

最近发现有牛人写了 kong-ingress-controller 的源码分析文章，我就想模仿下，也写篇 apisix-ingress-controller 的源码分析。

## 参考

- [apisix-ingress-controller](https://github.com/apache/apisix-ingress-controller)
- [Kong ingress controller 源码阅读 - Mayo's Blog](https://shoujo.ink/2021/11/kong-ingress-controller-%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB/)
