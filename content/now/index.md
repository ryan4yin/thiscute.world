---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

>在这个信息爆炸的时代，更需要能够放慢脚步，沉下心，系统性的学习。

>过去的我：[学习轨迹记录](/history)

## 一、我正在研究这些

>按优先级排序

- 研究多云与多 Kubernetes 集群的网络架构、应用管理方案
  - 当前方向：Istio 多集群服务网格 + Karmada 多集群应用部署 + cluster-api 多集群创建与更新
  - 也考虑是否统一使用开源的 k8s 网络插件，如 cilium
- 学习[Go语言动手写Web框架](https://geektutu.com/post/gee.html) - 进度 20%
- 阅读 [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/)- 进度 7%
- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 88%
- [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh) - 14.3%
- 极客时间《分布式协议与算法实战》 - 40%

## 二、我今年还想搞搞这些

今年业余时间的技术侧学习计划（不要求按顺序，几个主题可以交替学习）：

1. （2 month）把 Go 的几本书都看了，同时做几个项目练练手，学学 Kubernetes 底层（预计用时 6w）   
   1. 《Go 学习笔记（第六版下卷）》：基于 go 1.10，详细分析 go 的实现机制：内存分配、垃圾回收、并发调度等等
   2. [7天用Go从零实现分布式缓存GeeCache](https://geektutu.com/post/geecache.html)
   2. [7天用Go从零实现ORM框架GeeORM](https://geektutu.com/post/geeorm.html)
   2. [7天用Go从零实现RPC框架GeeRPC](https://geektutu.com/post/geerpc.html)
   2. [Go 语言高性能编程](https://github.com/geektutu/high-performance-go)
   3. [balancer](https://github.com/zehuamama/balancer): 源码阅读，如何使用 go 实现常见 balancer 算法
2. （1 month）分布式协议与区块链
   1. 《区块链核心算法解析》
   2. 《Design Data-Intensive Applications》
   3. 《Blockchain in Action》
   4. 《Distributed Systems, 3rd Edition, 2017》
   5. 《Distributed Algorithms, 2nd Edition, 2018》
3. （1 month）学习 C 语言，同样也写写代码练练手
   1. The ANSI C Programming Language
   2. 极客时间《深入 C 语言和程序运行原理》
   3. 《Expert C Programming: Deep C Secrets》：我有个群就仿照了这书的名称
   4. 补充学习 gdb ld objdump objcopy
4. （预计用时 3 month）学习 Linux
  - 极客时间 《Linux 内核技术实战课》
  - 极客时间 《Linux 性能优化实战》
  - [The Linux Programming Interface](https://man7.org/tlpi/): 学习 Linux 的顶级书藉，据说内容组织比 APUE 对新手更友好些。
  - [flash-linux0.11-talk](https://github.com/sunym1993/flash-linux0.11-talk)
  - 极客时间《容器实战高手课》
  - 极客时间《eBPF 核心技术与实战》
5. （预计用时 2 month）学习计算机网络，看书、学习 CS144 课程、手动实现 TCP/IP 协议栈
  - 《Computer Networking - A Top-Down Approach, 7e》：这本书我以前学过一次，但是主要只学了应用层到传输层的内容。
    - 可以结合 [CS 144: Introduction to Computer Networking](https://www.youtube.com/watch?v=1CP6aF09OjI&list=PLEAYkSg4uSQ2dr0XO_Nwa5OcdEcaaELSG&index=1&t=14s) 课程一起学习，不过我 C++ 全忘了，或许可以考虑用 rust/go 实现下协议栈？
  - 极客时间《网络排查案例课》

学习路径：实践类课程（比如极客时间专栏课）与系统化学习（CMU/MIT 公开课+教材）并重，可以同时或者交替进行。也并没有很严格的学习顺序要求，看兴趣吧。

不过有一点是确定的，就是希望今年一年至少能系统化地学习如下几个方面的知识：

- Kubernetes 原理、kubernetes apiserver/operator 编程
- Go 语言 Web 编程
- 分布式与 Etcd
- 只要求入门，写点简单的小玩具
  - 机器学习与深度学习
  - 区块链与智能合约编程
- 计算机网络：主要是熟悉 L3 网络层与 L4 传输层，结合 K8s 网络进行学习
- Linux：学完 TLPR，能独立进行 Linux 性能调优与性能问题排查

## 三、今年的阅读进展

>电子版都可以在 z-library 上很方便地下载到，实体书的话可以在多抓鱼等二手书平台碰碰运气。

已读：

- [x] 《人间失格》
- [x] 《月宫》
- [x] 《[Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)》
- [x] 《[Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)》
- [x] 《Go 程序设计语言（英文版）》
- [x] 《深入浅出 Kubernetes - 张磊》

正在读：

- 《在生命的尽头拥抱你-临终关怀医生手记》
- 《复杂 - 梅拉尼 米歇尔》
- [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/): Kubernetes 进阶

计划读：

- Kubernete、云原生、Go 语言
  - 《Go 学习笔记（第六版下卷）》：基于 go 1.10，详细分析 go 的实现机制：内存分配、垃圾回收、并发调度等等
- 补充 C 语言
  - 《The ANSI C Programming Language》：上大学时看过中文版。为了学操作系统，有必要再看一遍，这次就读原著英文版吧。
  - 《Expert C Programming: Deep C Secrets》：我有个群就仿照了这书的名称
  - 补充学习 gdb ld objdump objcopy
- Rust 语言
  -  极客时间《Rust 编程第一课》
- 《Social Psychology, 13e, David Myers》
- 《Principles Of Economics, 9e, N. Gregory Mankiw》
- 《在峡江的转弯处 - 陈行甲人生笔记》
- 《手把手教你读财报》
- 《原则 - 应对变化中的世界秩序》
- 《生命最后的读书会》
- 《凤凰项目：一个 IT 运维的传奇故事》


## 四、我的知识清单

### 1. 高优先级

- [Security Training for Engineers - PagerDuty](https://sudo.pagerduty.com/for_engineers/): 花几个小时，快速学习开发人员需要了解的安全知识

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

### 2. 中优先级

>附一份屌炸天的 CS 自学指南：https://github.com/pkuflyingpig/cs-self-learning/

- 学习英语，目标是能流利地读写交流。
  - 主要是可以扩宽工作的选择面，外企很多职位会要求英文读写流利。

- 容器底层原理
  - 容器镜像的文件系统：overlayfs
  - 镜像的构建流程：研究 buildkit/buildah 的实现

- Openresty 技术栈：（暂时感觉兴趣不大）
  - 阅读《Lua 程序设计》
  - 阅读 APISIX 源码 + Openresty
  - 深入学习 Nginx 及 epoll

- [进阶]操作系统（大概是以 OSTEP 为核心，学习时缺啥补啥吧）：
  - 核心课程：[Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/): 建议结合 [6.S081](https://pdos.csail.mit.edu/6.828/2020/schedule.html) 课程一起学习
  - OSTEP 学习指南：https://github.com/ryan4yin/computer-science/blob/master/coursepages/coresystems/ostep/OSTEP.md
  - 学到 xv6 时可结合这份资料啃源码：[xv6-annotated](https://github.com/palladian1/xv6-annotated)
  - Advanced Programming in the UNIX Environment, 3rd Edition: 同样是 Linux/Unix 系统的神书。学 OSTEP 遇到瓶颈时或可阅读。
  - [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html): 进阶读物，搞系统性能优化的
  - Linux eBPF: 目前相当火热的技术，极客时间买了《eBPF 核心技术与实战》，很期待。

- 计算机网络
  - 如果用 rust 的话，可以参考 [google/gvisor](https://github.com/google/gvisor)


- [进阶]数据库、数据结构与算法（暂时感觉兴趣不大）
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
  - 《月光落在左手上》
- 人文社科
  - 《爱的艺术》
  - 《亲密关系》
  - 《怎样征服美丽少女》：哈哈，之前在豆瓣还是哪看到的，听说很有用。
  - 《被讨厌的勇气》
  - 《邓小平时代》
  - 《论中国》
  - 《探路之役 - 1978-1922 年的中国经济改革》
  - 《筚路维艰 - 中国社会主义路径的五次选择》
  - 《人体简史》
  - 《科学革命的结构》
  - 《时间的秩序》
  - 《极简宇宙史》
  - 《刘擎西方现代思想讲义》
  - 《圆圈正义-作为自由前提的信念》
  - 《人生脚本》
  - 《投资中最简单的事》
  - 《债务危机 - 我的应对原则》
  - 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
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
    - 《[Crafting Interpreters](http://craftinginterpreters.com)》：亚马逊销量第一的编译器设计书籍，好评如潮。
      - 之前挑战《编程语言实现模式》，很遗憾失败了，这次我决定拿此书再战。
    - [Essentials of Programming Languages, 3rd Edition](https://book.douban.com/subject/3136252/)
    - [The Little Schemer - 4th Edition ](https://book.douban.com/subject/1632977/)
  - Kubernetes 与容器
    - [Hacking Kubernetes: Threat-Driven Analysis and Defense](https://hacking-kubernetes.info/): Kubernetes 安全，威胁模型以及如何防护。
    - [Container Security: Fundamental Technology Concepts that Protect Containerized Applications](https://containersecurity.tech/): 容器安全，这书在亚马逊上评价很好。

---

## 其他 ideas

- 我看到 github 上 [gopala-kr/10-weeks](https://github.com/gopala-kr/10-weeks) 这个项目，作者进行了一项挑战——每周学习一个新技术栈，目标是在一周内理解该技术栈各项热词的含义并列出大纲，使用该技术构建一个简单的程序，并写一篇博客。我觉得我也可以试试，不过可以把难度降低一些——**利用业余时间，每两个月学习一门新技术，并达成与 gopala-kr 类似的目标**。
- 其他感兴趣的
  - 前端：Preact+Css
  - 3D 建模与渲染：Blender、Unreal Engine 5、C++、taichi
  - 音乐：乐理、Synthesizer V、Reaper、midi 键盘
  - 其他：利用深度学习进行歌声合成、图片分辨率修复（超分辨率）、以及其他好玩的玩法


