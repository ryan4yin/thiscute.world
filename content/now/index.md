---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---


>过去的我：[学习轨迹记录](/history)

## 一、我正在研究这些

- 阅读《Go 程序设计语言（英文版）》
- 研究清楚 NAT 网关：
  - NAT 的原理、结构 - 50%
  - Kubernetes/Docker 网络所使用的 NAT
  - AWS NAT 网关
  - P2P 内网穿透: zerotier/tailscales
  - Kubernetes 跨 NAT 组网、将开发机器接入 Kubernetes 网络：适合用于本地/云上 K8s 调试
- 学习使用 Envoy 以及 [Istio EnvoyFilter](https://istio.io/latest/docs/reference/config/networking/envoy-filter/)
  - 分析 Envoy Sidecar 的动态配置、流量代理、监控指标等实现细节
  - 重点关注：负载均衡策略、prometheus 指标插件、slow_start 模式、gzip 压缩、gRPC 支持、Zone Aware Load Balancing、基于 iptables/tproxy 的 outbound 流量代理
  - [学习与测试各种负载均衡策略](https://github.com/ryan4yin/knowledge/blob/master/network/proxy%26server/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E7%AE%97%E6%B3%95.md)
- 研究 K8s 集群的节点伸缩优化、服务稳定性优化
  - [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler)
- 研究 K8s 集群的 Pod 拓扑优化
  - TopologySpreadConstraint
  - [descheduler](https://github.com/kubernetes-sigs/descheduler)
- go web 编程: 完成 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go) 这个项目
- 学习使用 
- 《在生命的尽头拥抱你-临终关怀医生手记》


## 二、我最近还想搞搞这些

今年的技术侧学习计划：

1. 把 Go 的几本书都看了，同时做几个项目练练手，学学 Kubernetes 底层
   1. 一个小 Web 项目 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go)
   2. 看看 Kubernetes Programming
   3. 学习极客时间的 Kuberntes 与容器的课程
2. 杂项
   1. 安全相关 [Security Training for Engineers - PagerDuty](https://sudo.pagerduty.com/for_engineers/): 花几个小时，快速学习开发人员需要了解的安全知识
3. 学习 K&R C 以及 rust 语言，同样也写写代码练练手
4. 学习计算机网络，看书、学习 CS144 课程、手动实现 TCP/IP 协议栈
   1. 如果用 rust 的话，可以参考 [google/gvisor](https://github.com/google/gvisor)
5. 学习操作系统
   1. 先学 CSAPP，同时跟课程
   2. 再学 OSTEP，同时跟课程
6. 机器学习
  - [machine-learning - coursera](https://www.coursera.org/learn/machine-learning): 吴恩达教授的网红机器学习课程，火爆多年了，内容对小白很友好。
  - [deep-learning - coursera](https://www.coursera.org/specializations/deep-learning): 仍然是吴恩达教授出品，圣经级别的机器学习课程，火爆多年了，内容对小白很友好。
  - [Machine Learning for Beginners - MicroSoft](https://github.com/microsoft/ML-For-Beginners): ML 入门课程，做得比较有趣。
  - [100-Days-Of-ML-Code](https://github.com/Avik-Jain/100-Days-Of-ML-Code): ML 入门资料

## 三、今年的阅读进展

>电子版都可以在 z-library 上很方便地下载到，实体书的话可以在多抓鱼等二手书平台碰碰运气。

已读：

- [x] 《人间失格》
- [x] 《月宫》
- [x] 《[Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)》
- [x] 《[Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)》

正在读：

- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 61%
- 《Go 程序设计语言（英文版）》 - 进度 53%
- 《复杂 - 梅拉尼 米歇尔》

计划读：

- 补充 C 语言
  - 《The ANSI C Programming Language》：上大学时看过中文版。为了学操作系统，有必要再看一遍，这次就读原著英文版吧。
  - 《Expert C Programming: Deep C Secrets》：我有个群就仿照了这书的名称
  - 补充学习 gdb ld objdump objcopy
- Kubernete、云原生、Go 语言
  - Go 语言学习笔记 - 雨痕：下卷是源码剖析，基于 Go 1.6, 打算在看完《Go 程序设计语言》后看看这本
  - [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/): Kubernetes 进阶
  - [Hacking Kubernetes: Threat-Driven Analysis and Defense](https://hacking-kubernetes.info/): Kubernetes 安全，威胁模型以及如何防护。
  - [Container Security: Fundamental Technology Concepts that Protect Containerized Applications](https://containersecurity.tech/): 容器安全，这书在亚马逊上评价很好。
- 操作系统（大概是以 OSTEP 为核心，学习时缺啥补啥吧）：
  - 核心课程：[Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/): 建议结合 [6.S081](https://pdos.csail.mit.edu/6.828/2020/schedule.html) 课程一起学习
  - OSTEP 学习指南：https://github.com/ryan4yin/computer-science/blob/master/coursepages/coresystems/ostep/OSTEP.md
  - 学到 xv6 时可结合这份资料啃源码：[xv6-annotated](https://github.com/palladian1/xv6-annotated)
  - Advanced Programming in the UNIX Environment, 3rd Edition: 同样是 Linux/Unix 系统的神书。学 OSTEP 遇到瓶颈时或可阅读。
  - [The Linux Programming Interface](https://man7.org/tlpi/): 学习 Linux 的顶级书藉，比 APUE 可能会更亲民一些，可结合阅读。
  - [flash-linux0.11-talk](https://github.com/sunym1993/flash-linux0.11-talk)
  - [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html): 进阶读物，搞系统性能优化的
- 计算机网络
  - 《Computer Networking - A Top-Down Approach, 7e》：这本书我以前学过一次，但是主要只学了应用层到传输层的内容。
    - 可以结合 [CS 144: Introduction to Computer Networking](https://www.youtube.com/watch?v=1CP6aF09OjI&list=PLEAYkSg4uSQ2dr0XO_Nwa5OcdEcaaELSG&index=1&t=14s) 课程一起学习，不过我 C++ 全忘了，或许可以考虑用 rust/go 实现下协议栈？
- 《Social Psychology, 13e, David Myers》
- 《Principles Of Economics, 9e, N. Gregory Mankiw》
- 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
- 《在峡江的转弯处 - 陈行甲人生笔记》
- 《原则 - 应对变化中的世界秩序》
- 《手把手教你读财报》
- 《探路之役 - 1978-1922 年的中国经济改革》
- 《筚路维艰 - 中国社会主义路径的五次选择》
- 《凤凰项目：一个 IT 运维的传奇故事》
- 《生命最后的读书会》
- 《月光落在左手上》

## 四、我的知识清单

### 1. 高优先级

- kubebuilder: 使用 kubebuilder 完成一个实用 operator.
- Cilium 网络插件
- Linux eBPF: 目前相当火热的技术

- 写几个小项目（使用 rust/go）
  - 实现一个文本编辑器
    - https://viewsourcecode.org/snaptoken/kilo/
  - 实现一个简单的 Linux 容器
    - https://blog.lizzie.io/linux-containers-in-500-loc.html
  - 网络代理（不到 2000 行的 TUN 库）
    - https://github.com/songgao/water
  - 实现简单的键值数据库：
    - https://github.com/tidb-incubator/tinykv
  - 实现简单的关系数据库：
    - https://github.com/tidb-incubator/tinysql
  - 学习搜索引擎技术：
    - [这就是搜索引擎](https://book.douban.com/subject/7006719/)
    - https://github.com/huichen/wukong

生活：
- 娱乐+运动：
  - 轮滑：倒滑后压步
- 音乐：Synthesizer V, 练习键盘

### 2. 中优先级

>附一份屌炸天的 CS 自学指南：https://github.com/pkuflyingpig/cs-self-learning/

- 学习英语，目标是能流利地读写交流。
  - 主要是可以扩宽工作的选择面，外企很多职位会要求英文读写流利。

- 容器底层原理
  - 容器镜像的文件系统：overlayfs
  - 镜像的结构分析
  - 镜像的构建流程

- Openresty 技术栈：（暂时感觉兴趣不大）
  - 阅读《Lua 程序设计》
  - 阅读 APISIX 源码 + Openresty
  - 深入学习 Nginx 及 epoll

- [进阶]数据库、数据结构与算法（同样暂时感觉兴趣不大）
  - redis 底层
  - mysql/postgresql 底层

## 五、我的备选书单

如下是我目前想读的书单，如果决定读，就把对应的书移到「计划读」中。

- 文学类：
  - 《百年孤独》：高中的时候读过一遍，但是都忘差不多了
  - 《霍乱时期的爱情》
  - 《苏菲的世界》：据说是哲学启蒙读物，曾经看过，但是对内容完全没印象了。
  - 《你一生的故事》：我也曾是个科幻迷
  - 《沈从文的后半生》
  - 《我与地坛》
  - 《将饮茶》
  - 《吾国与吾民 - 林语堂》
  - 《房思琪的初恋乐园》
  - 《可是我偏偏不喜欢》
- 人文社科
  - 《爱的艺术》
  - 《亲密关系》
  - 《怎样征服美丽少女》：哈哈，之前在豆瓣还是哪看到的，听说很有用。
  - 《被讨厌的勇气》
  - 《邓小平时代》
  - 《论中国》
  - 《人体简史》
  - 《科学革命的结构》
  - 《时间的秩序》
  - 《极简宇宙史》
  - 《刘擎西方现代思想讲义》
  - 《圆圈正义-作为自由前提的信念》
  - 《人生脚本》
  - 《投资中最简单的事》
  - 《债务危机 - 我的应对原则》
- 技术类
  - 《人月神话》
  - 《绩效使能：超越 OKR》
  - 《奈飞文化手册》
  - 《幕后产品-打造突破式思维》
  - 《分析与思考 - 黄奇帆的复旦经济课》：这本书会需要一定的经济学基础知识，打算在入门经济学后再看
  - 《重构 - 改善既有代码的设计》]
  - [The Rust Programming Language](https://doc.rust-lang.org/book/): 2021 年 8 月读过，2022 可以再搞一搞，主要用来写写网络、操作系统。
  - [SQL进阶教程](https://book.douban.com/subject/27194738/)
  - 分布式系统：[Designing Data-Intensive Applications](https://dataintensive.net/) - 可结合 [MIT 6.824](https://pdos.csail.mit.edu/6.824/schedule.html) 课程视频学习
  - 数据库系统：建议直接学习课程 [CMU 15-445](https://15445.courses.cs.cmu.edu/fall2019/schedule.html)
  - 编程语言理论（如何设计一个编程语言）
    - [Crafting Interpreters](http://craftinginterpreters.com)》：亚马逊销量第一的编译器设计书籍，好评如潮。
      - 之前挑战《编程语言实现模式》，很遗憾失败了，这次我决定拿此书再战。
    - [Essentials of Programming Languages, 3rd Edition](https://book.douban.com/subject/3136252/)
    - [The Little Schemer - 4th Edition ](https://book.douban.com/subject/1632977/)

---
