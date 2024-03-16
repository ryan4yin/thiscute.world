---
title: "源码分析系列 - Clash 代理工具"
date: 2022-03-30T00:11:21+08:00
draft: true

resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["网络代理", "源码分析", "网络隧道", "Clash"]
categories: ["tech"]
---

Clash 是一个非常流行的网络隧道工具，常用于科学#上网，它支持非常多的协议，而且支持规则路
由、通过 TUN 直接在第三层转发数据。

本文的主要目的是分析其源码，学习它的实现方式。

- tun 实现
- trojan/vmess/ss 等协议的实现
- rule-based 路由的实现
- 本地 http/socks5 代理的实现

## 参考
