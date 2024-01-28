---
title: "数据安全不完全指南"
subtitle: ""
description: ""
date: 2024-01-28T00:27:30+08:00
lastmod: 2024-01-28T00:27:30+08:00
draft: true

resources:
- name: "featured-image"
  src: "datasecurity.webp"

tags: ["安全", "密码学", "Linux", "SSH", "PGP", "密码管理", "LUKS", "全盘加密", "零信任", "rclone"]
categories: ["tech"]
series: []
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

toc:
  enable: true
math:
  enable: false
license: ""

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

> 我从 2023-05 开始产生了对强化个人数据安全的兴趣，从那时起到 2024-01-27 为止，我对个人的数据安全做了许多的工作，目前算是达到了一个比较不错的状态。
这里记录下我做的工作，以及我对数据安全的一些思考。

完全介绍说明如何正确地配置：

1. LUKS - Linux 全盘加密
   1. 启动时必须输入解密密码，否则无法启动
2. SSH 密钥 + passphrase + ssh-agent + 2FA
   2. passphrase 的实现原理，是否真正安全？是否存在被暴力破解的可能？应该设置为多长、多复杂比较合适？
3. GPG 密钥 + passphrase + gpg-agent + 2FA
   1. 这是个啥玩意儿？

之前持续更新的 <https://0xffff.one/d/1528/13>

