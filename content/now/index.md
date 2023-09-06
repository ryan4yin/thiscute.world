---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

> 在这个信息爆炸的时代，更需要能够放慢脚步，沉下心，系统性的学习。

> 虽然这一页列了这么多东西，但我实际学习还是从心，当前对啥感兴趣就学啥。我也会尝试找到感兴趣的应用场景，做点小玩意，毕竟学而不用，那兴趣就难以持续。

<!-- >过去的我：[学习轨迹记录](/history) -->

![](/images/now/book-shelf-2.webp)


## 一、我正在研究这些

>按优先级排序

- 从数字电路到 FPGA 再到 RISC-V
  - 当前目标：用 FPGA 实现些小功能
  - 先学点数字电路基础知识
    - 书籍：Practical Electronics for Inventors, Fourth Edition
    - 为了快速上手，直接跳过模拟电路部分，看第 12 到第 13 章
  - 再学点 FPGA 基础知识
    - 书籍：Practical Electronics for Inventors, Fourth Edition
    - 开发板：矽速荔枝糖系列，主要用 verilog 语言开发
    - 阅读第 14 章，再网上找点其他 verilog 资料对照学习下
    - verilog 练习题：https://hdlbits.01xz.net/wiki/Main_Page
  - 进阶：学习 RISCV 与处理器微架构
    - 书籍：Digital Design and Computer Architecture RISC-V Edition
    - 此书从第六章开始讲 RISCV 微架构。
- 学习研究 NixOS 与 ARM64 / RISCV64 开发板
- 学习与理解公益，参与公益活动
  - 目前想了解的：英国的社会企业与医疗体系，中国的扶贫攻坚
- 《Educated - A Memoir（中文名：你当像鸟飞往你的山）》
- 《一个天文学家的夜空漫游指南》
- 练习 Midi 键盘

## 二、我今年还想搞搞这些

今年的学习进展：

- 操作系统
  - 课程 [MIT 6.S081: Operating System Engineering](https://csdiy.wiki/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/MIT6.S081/)
  - 书 [Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
  - 书 [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 296/572
  - 代码 [xv6-annotated](https://github.com/palladian1/xv6-annotated)
- 从零开始造 OS
  - [南京大学 计算机科学与技术系 计算机系统基础 课程实验 (PA)](https://nju-projectn.github.io/ics-pa-gitbook/)
  - [rust-raspberrypi-OS-tutorials](https://github.com/rust-embedded/rust-raspberrypi-OS-tutorials): rust 版
  - [rpi4-osdev](https://github.com/isometimes/rpi4-osdev): c 语言版

## 三、今年的阅读进展

>电子版都可以在 z-library 上很方便地下载到，实体书的话可以在多抓鱼等二手书平台碰碰运气。

已读：
- 2023-03-09 - The Moon and Sixpence
  - 你是要地上的六便士，还是要天上的月亮？
- 2023-06-23 - [NixOS & Flakes Book](https://github.com/ryan4yin/nixos-and-flakes-book)
  - 这不是我今年读的书，而是我自己写的一本中英双语的开源小书，算是今年到目前为止的巅峰成就了。
- 2023-08-31 - [How to Do Great Work - Paul Graham](http://www.paulgraham.com/greatwork.html)
  - 黑客与画家一篇两万多字的长文，也算是一本小书了吧，干货满满。

正在读：
- 《Educated - A Memoir（中文名：你当像鸟飞往你的山）》
- 《一个天文学家的夜空漫游指南》
- The Great Gatsby - 10/41
- [Linux Device Driver Development - Second Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition): Linux 驱动编程入门，2022 年出的新书，基于 Linux 5.10，amazon 上评价不错，目前只有英文版，写的很好，对新手很友好。
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)


想读，但是没啥计划（大致按感兴趣程度排序）：

- 第一梯队
  - 《Educated - A Memoir（中文名：你当像鸟飞往你的山）》
  - 《一个天文学家的夜空漫游指南》
  - 《刘擎西方现代思想讲义》
  - 《界限：通往个人自由的实践指南》
  - 《复杂 - 梅拉尼 米歇尔》
- 第二梯队
  - 《科学革命的结构》
  - 《江城》
  - 《山月记》
  - 《生命最后的读书会》
  - 《被讨厌的勇气》
  - 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
  - 《步天歌研究》
  - 《性命圭旨》

## 四、备选学习路线

### 1. 高优先级

#### 操作系统

理解 Linux 操作系统也是我继续精进技术必不可少的技能。

- 核心课程：课程 [6.S081](https://pdos.csail.mit.edu/6.828/2020/schedule.html) + 书 [Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
  - 课程相关资源：[0xFFFF - MIT6.S081 Operating System Engineering (Fall 2020)](https://0xffff.one/d/1085-mit6-s081-operating-system)
  - OSTEP 学习指南：<https://github.com/ryan4yin/computer-science/tree/master/coursepages/ostep>
- 学到 xv6 时可结合这份资料啃源码：[xv6-annotated](https://github.com/palladian1/xv6-annotated)
- [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html): 进阶读物，搞系统性能优化的
- 《BPF Performance Tools（英文版）》：进阶读物，Linux 内核技术，主要用于搞 Linux 网络数据包处理、性能分析、系统监控的。
- Linux 系统
  - 极客时间 《Linux 内核技术实战课》
  - [flash-linux0.11-talk](https://github.com/sunym1993/flash-linux0.11-talk)
  - 极客时间《容器实战高手课》
  - 极客时间《eBPF 核心技术与实战》
- C 语言 / Rust 语言
  - 极客时间《深入 C 语言和程序运行原理》
  - 极客时间《Rust 编程第一课》

- Linux 性能调优与 Linux 网络技术
  - [ ] 《深入理解 Linux 网络 - 张彦飞》 - 14/320
  - [ ] 极客时间《网络排查案例课》
  - [ ] 极客时间 《Linux 性能优化实战》


#### 嵌入式/物联网

嵌入式跟 IoT 是我 2022 年底开的新坑，目前兴趣强烈。

我目前收集的相关内容（仅是一个资料合集，内容有重复的）：

- 嵌入式 Linux 系列
  - [Linux Device Driver Development - Second Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition): Linux 驱动编程入门，2022 年出的新书，基于 Linux 5.10，amazon 上评价不错，目前只有英文版，写的很好，对新手很友好。
  - [Linux Driver Development for Embedded Processors 2nd Edition](https://github.com/ALIBERA/linux_book_2nd_edition): 这本是 2018 年出的，写得没上面那本好、内容也没那么新，但是看评价也不错，特点是有许多的 Lab 可做。
  - [Linux Kernel Programming: A comprehensive guide to kernel internals](https://book.douban.com/subject/35415097/): Linux 内核编程领域的新书，适合入门 Linux 内核，amazon 上评价挺好，先收藏一个
  - [Understanding the Linux Kernel, 3rd Edition](https://book.douban.com/subject/1776614/)：Linux 内核技术进阶。
  - [linux-insides](https://0xax.gitbooks.io/linux-insides/content/index.html): 从 bootloader 开始讲解了 Linux 内核的许多重要的功能模块，看 stars 很高所以也在这里列一下。 
- 电路原理
  - Practical Electronics for Inventors, Fourth Edition
- 芯片
  - ARM64: STM32 ESP32 RK3588s
  - RISCV: milkv mars/duo, licheepi4a
  - FPGA / 电路设计: [FPGA 玩耍之旅](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/fpga)
- 目前的学习目标
  - DIY 无人机编队飞行！要达成这个目标需要学习的东西有点多，慢慢努力吧~

### 2. 以后可能会感兴趣的

#### 计算机网络

计算机网络可算是我的老本行了，用来吃饭的家伙事，技艺不能落下。

- 计算机网络
  - TCP/IP Illustrated, Volume 1, 2nd Edition  - 进度 31/920
- 课程 [CS 144: Introduction to Computer Networking](https://www.youtube.com/watch?v=1CP6aF09OjI&list=PLEAYkSg4uSQ2dr0XO_Nwa5OcdEcaaELSG&index=1&t=14s)
  - 以前学过一次《Computer Networking - A Top-Down Approach, 7e》，这次算是重学吧。
  - 课程主要使用 C++，我或许可以考虑用 rust/go 实现下协议栈？
- TCP/IP 协议栈的实现：可以参考 [google/gvisor](https://github.com/google/gvisor)


#### 机器学习与深度学习

2022 到 2023 这两年，AI 技术又陆续出现明显突破，ChatGPT 与 Stable Diffusion 都令人印象深刻。
我与大多数普通人一样，对 AI 技术本身兴趣不大，更感兴趣的是 AI 能带给世界哪些改变。
所以我的目标仅仅是入个门，能在自己感兴趣的领域应用上 AI 的研究成果。

- [ ] [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh) - 14.3%


#### 其他杂项

- Go 语言进阶
  - 《Go 学习笔记（第六版下卷）》
    - 基于 go 1.10，详细分析 go 的实现机制：内存分配、垃圾回收、并发调度等等
  - [ ] [Go语言动手写Web框架](https://geektutu.com/post/gee.html) - 进度 20%
  - [ ] [Go 语言高性能编程](https://github.com/geektutu/high-performance-go)

- Kubernetes 原理、Kubernetes APIServer/Operator 编程
  - [ ] [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/)

- 英语
  - [ ] [American Pronunciation Workshop](https://www.bilibili.com/video/BV1Ts411m7EU/) 美语发音教程
  - [ ] [Master Spoken English Feeling Phonics](https://www.bilibili.com/video/BV1k4411Q7iw/) 进阶发音教程
  - [ ] 《英语语法新思维——初级教程》
  - [ ] 《English Grammer In Use》语法书
  - [ ] 《Key words for fluency》口语表达

生活：
- 娱乐+运动：
  - 轮滑：倒滑后压步
  - 游泳：学会蛙泳并且提升速度

#### 其他资料

>这个列表中的内容没啥优先级，反正先列着，什么时候有兴趣可以玩玩。

>附一份屌炸天的 CS 自学指南：https://github.com/pkuflyingpig/cs-self-learning/


- 写几个小项目（使用 rust/go）
  - 实现一个文本编辑器
    - https://viewsourcecode.org/snaptoken/kilo/
  - 实现一个简单的 Linux 容器
    - https://blog.lizzie.io/linux-containers-in-500-loc.html
  - 网络代理（不到 2000 行的 TUN 库）
    - https://github.com/songgao/water

- Go 语言 Web 编程
  - [ ] [7天用Go从零实现分布式缓存GeeCache](https://geektutu.com/post/geecache.html)
  - [ ] [7天用Go从零实现ORM框架GeeORM](https://geektutu.com/post/geeorm.html)
  - [ ] [7天用Go从零实现RPC框架GeeRPC](https://geektutu.com/post/geerpc.html)
  - [ ] [balancer](https://github.com/zehuamama/balancer): 源码阅读，如何使用 go 实现常见 balancer 算法

- [Security Training for Engineers - PagerDuty](https://sudo.pagerduty.com/for_engineers/): 花几个小时，快速学习开发人员需要了解的安全知识

- Openresty 技术栈：（暂时感觉兴趣不大）
  - 阅读《自己动手实现 Lua》
  - 深入学习 Nginx 及 epoll

- 容器与 Kubernetes
  - [Hacking Kubernetes: Threat-Driven Analysis and Defense](https://hacking-kubernetes.info/): Kubernetes 安全，威胁模型以及如何防护。
  - [Container Security: Fundamental Technology Concepts that Protect Containerized Applications](https://containersecurity.tech/): 容器安全，这书在亚马逊上评价很好。

- 检索技术
  - [这就是搜索引擎](https://book.douban.com/subject/7006719/)
  - 极客时间《检索技术 25 讲》


分布式数据库：

- 学习路线
  1. 极客时间《分布式协议与算法实战》 - 学习进度 50%
  2. 分布式系统：课程 [MIT 6.824](https://pdos.csail.mit.edu/6.824/schedule.html) + 书 [Designing Data-Intensive Applications](https://dataintensive.net/)
  3. 数据库系统：课程 [CMU 15-445](https://15445.courses.cs.cmu.edu/fall2019/schedule.html)
  4. 参加 tidb 的 [talent-plan](https://tidb.net/talent-plan)，完成 tinykv 项目
- 其他参考书籍
  - 《Distributed Systems, 3rd Edition, 2017》
  - 《Distributed Algorithms, 2nd Edition, 2018》
  - [SQL进阶教程](https://book.douban.com/subject/27194738/)


编程语言理论：

- 《[Crafting Interpreters](http://craftinginterpreters.com)》：亚马逊销量第一的编译器设计书籍，好评如潮。
  - 之前挑战《编程语言实现模式》，很遗憾失败了，这次我决定拿此书再战。
- [Essentials of Programming Languages, 3rd Edition](https://book.douban.com/subject/3136252/)
- [The Little Schemer - 4th Edition ](https://book.douban.com/subject/1632977/)
- 《WebAssembly 核心原理》
- 用 Go 语言讲编程语言理论
  - 《自己动手实现 Lua》
  - 《自己动手实现 Java 虚拟机》


## 五、备选书单

如下是我目前想读的书单，如果决定读，就把对应的书移到「计划读」中。

- 文学类：
  - 《百年孤独》：高中的时候读过一遍，但是都忘差不多了
  - 《霍乱时期的爱情》
  - 《苏菲的世界（Sophie's World）》：据说是哲学启蒙读物，曾经看过，但是对内容完全没印象了。
  - 《你一生的故事》：我也曾是个科幻迷
  - 《沈从文的后半生》：这本书更偏研究性质，有点难读
  - 《房思琪的初恋乐园》
  - 《月光落在左手上》
  - 《了不起的盖茨比》
  - 《The Windup Girl》：高中时读过中文版，刷新我三观，现在想再读一遍英文原版。
- 人文社科
  - 《Social Psychology, 13e, David Myers》
  - 《Intimate Relationships》 - 进度 14/449
  - 《Principles Of Economics, 9e, N. Gregory Mankiw》
  - Majo no Tabitabi（魔女之旅）Vol.1
  - Tasogare-iro no Uta Tsukai（黄昏色的咏使）Vol.1
  - Moon Palace, by Pual Auster - 读过中文版，但是看英文版词汇量也不高，可以一读
  - Animal Farm - 一本政治讽刺小书
  - 《手把手教你读财报》
  - 《原则 - 应对变化中的世界秩序》
  - 《探路之役 - 1978-1922 年的中国经济改革》
  - 《筚路维艰 - 中国社会主义路径的五次选择》
  - 《圆圈正义-作为自由前提的信念》
  - 《人体简史》
  - 《邓小平时代》
  - 《论中国》
  - 《时间的秩序》
  - 《极简宇宙史》
  - 《人生脚本》
  - 《投资中最简单的事》
  - 《债务危机 - 我的应对原则》
  - 《分析与思考 - 黄奇帆的复旦经济课》：这本书会需要一定的经济学基础知识，打算在入门经济学后再看
  - 《语言学的邀请》- 进度 68/288
    - 对语言学有点兴趣，同时听说这本书对表达（沟通、写作）也大有帮助~
- 技术类
  - 《人月神话》
  - 《绩效使能：超越 OKR》
  - 《奈飞文化手册》
  - 《幕后产品-打造突破式思维》
  - 《重构 - 改善既有代码的设计》
  - 《云原生服务网格 Istio：原理、实践、架构与源码解析》
    - 比较老的书了，不过用来学下 Istio 的底层架构跟源码，感觉还是有价值的。
  - 《凤凰项目：一个 IT 运维的传奇故事》
- 英语语法
  - 《English Grammer In Use》
  - 《英语语法新思维——初级教程》     - 8/366

---

## 其他 ideas

- 我看到 github 上 [gopala-kr/10-weeks](https://github.com/gopala-kr/10-weeks) 这个项目，作者进行了一项挑战——每周学习一个新技术栈，目标是在一周内理解该技术栈各项热词的含义并列出大纲，使用该技术构建一个简单的程序，并写一篇博客。我觉得我也可以试试，不过可以把难度降低一些——**利用业余时间，每两个月学习一门新技术，并达成与 gopala-kr 类似的目标**。
- 其他感兴趣的
  - 3D 建模与渲染：Blender、Unreal Engine 5、C++、taichi
  - 音乐：乐理、Synthesizer V、Reaper、midi 键盘


{{< particles_effect_up  >}}
