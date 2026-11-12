---
title: "聊聊开放权重 LLM 模型与 AI 推理软硬件"
subtitle: ""
description: ""
date: 2026-11-11T23:02:31+08:00
lastmod: 2026-11-11T23:02:31+08:00
draft: true

authors: ["ryan4yin"]
featuredImage: "featured-image.webp"
resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Qwen", "Strata", "NPU", "GPU", "DDR6", "HBM"]
categories: ["tech"]
series: []
hiddenFromHomePage: false
hiddenFromSearch: false
license: ""

lightgallery: false

# 否开启表格排序
table:
  sort: false

toc:
  enable: true
math:
  enable: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

2026 年接近尾声，博客也长草挺久了，决定出来水一篇我对当前本地 AI 推理的一些观察与趋势展望。

## 本地 LLM 推理

### 开放权重 LLM 模型

- Qwen - 王者

### 推理软件选择

- Strata - 今年的黑马
- Llama.cpp - 最成熟、支持的模型广泛
- vllm - 比较企业级，如果你显存够大，可以考虑

### Nvidia, AMD, Intel

- Nvidia - 最佳选择，当然也是最贵的选择
- AMD - 性价比之选
- Intel - Arc Pro B70 现在在国内价格也炒上去了，性能还不到 AMD
  R9700 的一半，而且优化也还有待提升，，不是个好选择。

## NPU？

NPU 也分好几条路线：

数据中心路线：

- 华为昇腾 - 功能对标 GPU，甚至在尝试抢训练市场

低功耗 LLM 大模型推理路线：

- AMD Strix Halo / Nvidia DGX Spark
- 爱芯元智 AX8860 - 战未来？性能够高，但刚出的芯片，软件栈还得继续观察。
- 后摩智能 漫界 M50 - 战未来？也差不多才出没多久的芯片，软件栈还得观察。

低功耗小模型推理路线：

- Intel NPU - openvino 软件栈，跟 GPU 统一的
- AMD XDNA NPU - 完全独立的 RyzenAI-SW 软件栈，跟 ROCm 完全隔离的

低算力低功耗的 NPU 用途：

- OCR
- 图像识别、物体识别
- 语音识别 ASR、语音输出 TTS

## 未来的 CPU 会是啥架构？

- CPU 管通用计算
- iGPU/dGPU 管图形渲染，以及重一点的模型推理
- NPU 低功耗的小模型推理

一个小点的 Whisper 模型跑起来都要 2-4
GB 的内存，所以可以预见到，未来个人电脑的内存需求也会出现显著增长。

在 AI 时代之前，现在已经做到了 16G 普及，那么在边缘 AI 推理时代来临后，等内存价格降回正常区间，32G 有望成为主流配置，48G/64G 也有望普及，而 128G/256G 的边缘 AI 推理设备，现在就已经雨后春笋般的冒出来了。
