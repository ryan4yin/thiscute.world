---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

> 在这个信息爆炸的时代，更需要能够放慢脚步，沉下心，系统性的学习。

> 虽然这一页列了这么多东西，但我实际学习还是从心，当前对啥感兴趣就学啥。我也会尝试找到感兴
> 趣的应用场景，做点小玩意或者写点学习感悟，毕竟学而不用，那一是兴趣难以持续，二是纸上谈兵
> 学不到真本事。

<!-- >过去的我：[学习轨迹记录](/history/thisyear) -->

![](/images/now/book-shelf-2.webp)

## 一、我正在研究这些

> 按优先级排序

- 运动
  - 完成每天 500 卡路里的消耗量，目标是减肥+提升体力
  - 方式：玩陆地冲浪板、跑步、登山
- 驾照考试 - 科目一刷题
- Linux 学习
  - 参与 Nixpkgs 的 PR review, 熟悉社区的 PR 流程，改进一些我用到的 NixOS Module.
  - 《深入理解 Linux 进程与内存》

## 二、我今年还想搞搞这些

- 拿到驾照
- 体重降到 55kg
- Linux 学习
  - 积极参与 NixOS 上游贡献
  - 完成基础知识学习
    - 《深入理解 Linux 进程与内存》
    - 《深入理解 Linux 网络》
    - 《BPF Performance Tools（英文版）》 - 35/740
- 云原生
  - 研究 Istio 的底层实现
- RISC-V 与操作系统
- 阅读
  - 《Educated - A Memoir（中文名：你当像鸟飞往你的山）》
  - 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
- 旅游与户外运动

  - 去日本、韩国跟新加坡玩

- 操作系统

  - 课
    程：[操作系统：设计与实现 - 南大 jyy 老师的课程](https://www.bilibili.com/video/BV1Xx4y1V7JZ/)
  - 资料：
    - [操作系统：设计与实现 (2024 春季学期)](https://jyywiki.cn/OS/2024/)
    - [南京大学 计算机科学与技术系 计算机系统基础 课程实验 (PA)](https://nju-projectn.github.io/ics-pa-gitbook/)
  - 书 [Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)

- 部署学习各类数据中间件：
  - Milvus 向量数据库
  - ClickHouse - 存日志之类的时序数据貌似都挺合适，原生分布式、高性能
  - TimescaleDB - 也是 PG 的插件，Scale 能力有限，但是好处是开发人员上手没难度。

## 三、今年的阅读进展

> 电子版都可以在 z-library 上很方便地下载到，实体书的话可以在多抓鱼等二手书平台碰碰运气。

已读：

- 《Go 高级编程》
- [Linux/Unix 系统编程手册（下册）](https://man7.org/tlpi/)

正在读：

- 《深入理解 Linux 网络》
- 《深入理解 Linux 进程与内存》
- 《BPF Performance Tools（英文版）》 - 35/740
- 《Educated - A Memoir（中文名：你当像鸟飞往你的山）》
- The Great Gatsby - 10/41
- 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》

想读，但是没啥计划（大致按感兴趣程度排序）：

- 第一梯队

  - 《界限：通往个人自由的实践指南》
  - 《置身事内：中国政府与经济发展》
  - [Linux Device Driver Development - Second Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition):
    Linux 驱动编程入门，2022 年出的新书，基于 Linux 5.10，amazon 上评价不错，目前只有英文
    版，写的很好，对新手很友好。
  - 《复杂 - 梅拉尼 米歇尔》
  - Psychology and Life, 20th edition, by Richard J. Gerrig

- 第二梯队
  - Mountaineering: The Freedom of the Hills（登山圣经）
  - 《分心也有好人生》
  - 《刘擎西方现代思想讲义》
  - 《五四运动史：现代中国的知识革命》
  - 《八次危机：中国的真实经验》
  - 《我们今天怎样做父亲》：梁启超的教育观
  - 《中国国家治理的制度逻辑》
  - 《江村经济》
  - 《党员、党权与党争：1924 - 1949 年中国国民党的组织形态》
  - 《我的前半生——爱新觉罗·溥仪》
  - 《为什么学生不喜欢上学》

## 四、备选学习路线

### 1. 高优先级

#### 操作系统

理解 Linux 操作系统也是我继续精进技术必不可少的技能。

- 核心课程：课程 [6.S081](https://pdos.csail.mit.edu/6.828/2020/schedule.html) + 书
  [Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
  - 课程相关资源
    - [0xFFFF - MIT6.S081 Operating System Engineering (Fall 2020)](https://0xffff.one/d/1085-mit6-s081-operating-system)
    - [操作系统：设计与实现 - 南大 jyy 老师的课程](https://www.bilibili.com/video/BV1Xx4y1V7JZ/)
  - OSTEP 学习指
    南：<https://github.com/ryan4yin/computer-science/tree/master/coursepages/ostep>
- 学到 xv6 时可结合这份资料啃源
  码：[xv6-annotated](https://github.com/palladian1/xv6-annotated)
- [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html):
  进阶读物，搞系统性能优化的
- 《BPF Performance Tools（英文版）》：进阶读物，Linux 内核技术，主要用于搞 Linux 网络数据
  包处理、性能分析、系统监控的。
- Linux 系统
  - Linux 经典书目(按阅读顺序排列)
    - TLPI - 正在读
    - APUE(Advanced Programming in the UNIX Environment)
    - UNP(Unix Network Programming)
    - Understanding the Linux Kernel, 3rd Edition
  - 极客时间 《Linux 内核技术实战课》
  - [flash-linux0.11-talk](https://github.com/sunym1993/flash-linux0.11-talk)
  - 极客时间《容器实战高手课》
  - 极客时间《eBPF 核心技术与实战》
- C 语言 / Rust 语言

  - 极客时间《深入 C 语言和程序运行原理》
  - 极客时间《Rust 编程第一课》

- Linux 性能调优与 Linux 网络技术
  - [ ] 《深入理解 Linux 网络 - 张彦飞》 - 14/320
  - [ ] 《深入理解 Linux 进程与内存 - 张彦飞》
  - [ ] 极客时间《网络排查案例课》
  - [ ] 极客时间 《Linux 性能优化实战》

#### 计算机网络

计算机网络可算是我的老本行了，用来吃饭的家伙事，技艺不能落下。

- 计算机网络
  - TCP/IP Illustrated, Volume 1, 2nd Edition - 进度 31/920
- 课程
  [CS 144: Introduction to Computer Networking](https://www.youtube.com/watch?v=1CP6aF09OjI&list=PLEAYkSg4uSQ2dr0XO_Nwa5OcdEcaaELSG&index=1&t=14s)
  - 以前学过一次《Computer Networking - A Top-Down Approach, 7e》，这次算是重学吧。
  - 课程主要使用 C++，我或许可以考虑用 rust/go 实现下协议栈？
- TCP/IP 协议栈的实现：可以参考 [google/gvisor](https://github.com/google/gvisor)

### 2. 以后可能会感兴趣的

#### AI infra 方向

这是一个相当新的方向，因为近两年 AI 开始落地而兴起，它既要求熟悉 K8s/Istio 等传统 infra 组
件，又要求对 AI 训练推理相关的技术有足够了解，例如：

- Operator: training-operator
- 调度：volcano
- 框架：Kubeflow, RayTrain, Argo Workflows
- 性能优化：Triton/BentoML/vLLM/PyTorch/CUDA

感觉是一个转型的方向，业余可以看看。

相关资料：

- https://github.com/stas00/ml-engineering/

#### 心理学与认知神经科学

学习路线：

- 入门：
  - 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
  - Psychology and Life, 20th edition, by Richard J. Gerrig, 2012
  - Educational Psychology, 14th Global Edition (Anita Woolfolk, 2021)
  - Development Across the Life Span, 10th edition (Robert S. Feldman, 2023)
- 进阶到认知神经科学
  - Neuroscience: Exploring the Brain, 4th edition (2015)
  - Cognitive Neuroscience: The Biology of the Mind, 5th edition (2019)
- 其他方向
  - 《Intimate Relationships》 - 进度 14/449
  - 《Social Psychology, 14e, David Myers》

#### 嵌入式/物联网

嵌入式跟 IoT 是我 2022 年底开的新坑，目前兴趣强烈。

之前制定的 FPGA 学习路线：

- 从数字电路到 FPGA 再到 RISC-V
  - 当前目标：用 FPGA 实现些小功能
  - 先学点数字电路基础知识
    - 书籍：Practical Electronics for Inventors, Fourth Edition
    - 为了快速上手，直接跳过模拟电路部分，看第 12 到第 13 章
  - 再学点 FPGA 基础知识
    - 书籍：Practical Electronics for Inventors, Fourth Edition
    - 开发板：矽速荔枝糖系列，主要用 verilog 语言开发
    - 阅读第 14 章，简单入门 FPGA
    - verilog 语言，直接用这个站点就够了，是非常好的教程 + 练习场：
      - <https://hdlbits.01xz.net/wiki/Main_Page>
    - 更有趣的练习题： https://www.fpga4fun.com/
    - 从 LED 点灯到 RISCV CPU（循序渐进）:
      https://github.com/BrunoLevy/learn-fpga/blob/master/FemtoRV/TUTORIALS/FROM_BLINKER_TO_RISCV/README.md
  - 进阶：学习 RISCV 与处理器微架构
    - 书籍：Digital Design and Computer Architecture RISC-V Edition
    - 此书从第六章开始讲 RISCV 微架构。

我目前收集的相关内容（仅是一个资料合集，内容有重复的）：

- 嵌入式 Linux 系列
  - [Linux Device Driver Development - Second Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition):
    Linux 驱动编程入门，2022 年出的新书，基于 Linux 5.10，amazon 上评价不错，目前只有英文
    版，写的很好，对新手很友好。
  - [Linux Driver Development for Embedded Processors 2nd Edition](https://github.com/ALIBERA/linux_book_2nd_edition):
    这本是 2018 年出的，写得没上面那本好、内容也没那么新，但是看评价也不错，特点是有许多的
    Lab 可做。
  - [Linux Kernel Programming: A comprehensive guide to kernel internals](https://book.douban.com/subject/35415097/):
    Linux 内核编程领域的新书，适合入门 Linux 内核，amazon 上评价挺好，先收藏一个
  - [Understanding the Linux Kernel, 3rd Edition](https://book.douban.com/subject/1776614/)：Linux
    内核技术进阶。
  - [linux-insides](https://0xax.gitbooks.io/linux-insides/content/index.html): 从
    bootloader 开始讲解了 Linux 内核的许多重要的功能模块，看 stars 很高所以也在这里列一
    下。
- 电路原理
  - Practical Electronics for Inventors, Fourth Edition
- 芯片
  - ARM64: STM32 ESP32 RK3588s
  - RISCV: milkv mars/duo, licheepi4a
  - FPGA / 电路设计:
    [FPGA 玩耍之旅](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/fpga)
- 目前的学习目标
  - DIY 无人机编队飞行！要达成这个目标需要学习的东西有点多，慢慢努力吧~

#### 其他杂项

- Go 语言进阶

  - 《Go 学习笔记（第六版下卷）》
    - 基于 go 1.10，详细分析 go 的实现机制：内存分配、垃圾回收、并发调度等等
  - [ ] [Go语言动手写Web框架](https://geektutu.com/post/gee.html) - 进度 20%
  - [ ] [Go 语言高性能编程](https://github.com/geektutu/high-performance-go)

- 英语
  - 找外教练口语
  - 再多背点单词，现在我技术英文能无障碍阅读，但是生活英语方面词汇量相当低。
  - [ ] 《英语语法新思维——初级教程》
  - [ ] 《English Grammar In Use》语法书
  - [ ] 《Key words for fluency》口语表达

生活：

- 娱乐+运动：
  - 轮滑：倒滑后压步
  - 游泳：学会蛙泳并且提升速度
  - 徒步：夏、冬两季各完成一次麦理浩径全程

#### 其他资料

> 这个列表中的内容没啥优先级，反正先列着，什么时候有兴趣可以玩玩。

> 附一份屌炸天的 CS 自学指南：https://github.com/pkuflyingpig/cs-self-learning/

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
  - [ ] [balancer](https://github.com/zehuamama/balancer): 源码阅读，如何使用 go 实现常见
        balancer 算法

- 容器与 Kubernetes（其实好像也没啥兴趣）

  - [Hacking Kubernetes: Threat-Driven Analysis and Defense](https://hacking-kubernetes.info/):
    Kubernetes 安全，威胁模型以及如何防护。
  - [Container Security: Fundamental Technology Concepts that Protect Containerized Applications](https://containersecurity.tech/):
    容器安全，这书在亚马逊上评价很好。

分布式数据库：

- 学习路线
  1. 极客时间《分布式协议与算法实战》 - 学习进度 50%
  2. 分布式系统：课程 [MIT 6.824](https://pdos.csail.mit.edu/6.824/schedule.html) + 书
     [Designing Data-Intensive Applications](https://dataintensive.net/)
  3. 数据库系统：课程
     [CMU 15-445](https://15445.courses.cs.cmu.edu/fall2019/schedule.html)
  4. 参加 tidb 的 [talent-plan](https://tidb.net/talent-plan)，完成 tinykv 项目
- 其他参考书籍
  - 《Distributed Systems, 3rd Edition, 2017》
  - 《Distributed Algorithms, 2nd Edition, 2018》
  - [SQL 进阶教程](https://book.douban.com/subject/27194738/)

## 五、备选书单

> [我的豆瓣](https://www.douban.com/people/kirito_c/)

如下是我目前想读的书单，如果决定读，就把对应的书移到「计划读」中。

- 家庭教育（教育也要讲究科学，凭直觉做事往往会错得很离谱）
  - 《教育与美好生活》：大名鼎鼎的思想家罗素的教育观。
  - 《孩子：挑战（Children - The Challenge）》：美国人写的书，如何在尊重孩子、给孩子平等自
    由的同时，让孩子尊重规则、承担责任、赢得合作。阿德勒心理学。
  - 《P.E.T.父母效能训练 - 让亲子沟通如此高效而简单》
  - 《高压年代：如何帮助孩子在大学渡过难关、顺利成人（The Stressed Years of Their
    Lives）》：作者之一的儿子杰森在上大学的第一年出现了严重的心理问题：无法返校继续学业，
    情绪濒于崩溃，甚至产生自杀冲动。本书总结了如何去发现并解决青少年的心理问题，帮助他们完
    成从家庭到大学、从青春期到真正成年的顺利过渡。
  - 《享受孩子成长 - 留美教育博士十八年教育手记》：这书主要是个流水账，既包含作者主观的教
    育理念、也援引了许多教育、心理学等领域的重要科学发现。正在读，目前评个 7 分吧。
  - 《游戏力（Playful Parenting）》：游戏力的游戏，特指亲子间的互动。它是思考方式，是互动
    方式，也是大人与孩子在一起轻松开心的状态。本书的重点是解决孩子常见的行为问题，激发孩子
    内在的自信力，重建父母与孩子间亲密沟通的桥梁。
  - 《真希望我父母读过这本书》
  - 《为什么学生不喜欢上学?（Why Don't Students Like School?）》：用认知心理学的原理，详细
    分析了学生学习的过程和教师在课堂教学中必须注意的一些问题。
  - 《学习的本质》：法国人安德烈·焦尔当的书
- 经济 / 管理 / 社会
  - 《Principles Of Economics, 9e, N. Gregory Mankiw》
  - 《圆圈正义-作为自由前提的信念》
  - 《投资中最简单的事》
  - 《债务危机 - 我的应对原则》
  - 《分析与思考 - 黄奇帆的复旦经济课》：这本书会需要一定的经济学基础知识，打算在入门经济
    学后再看
  - Animal Farm - 一本政治讽刺小书
  - 《手把手教你读财报》
  - 《原则 - 应对变化中的世界秩序》
  - 《探路之役 - 1978-1922 年的中国经济改革》
  - 《筚路维艰 - 中国社会主义路径的五次选择》
  - 《邓小平时代》
  - 《论中国》
  - 《中国国家治理的制度逻辑》
  - 《江村经济》
  - 《八次危机：中国的真实经验》
  - 《中国经济：适应与增长》
  - 《中国为什么有前途：对外经济关系的战略潜能》
  - 《置身事内：中国政府与经济发展》
  - 《党员、党权与党争：1924 - 1949 年中国国民党的组织形态》
- 人物传记或者与名人相关的书籍（从历史上的成功者，以及历史中学习）
  - 《史蒂夫·乔布斯传》
  - 《埃隆·马斯克传》
  - 《维特根斯坦传》
  - 《李光耀观天下》
  - 《沈从文的后半生》：这本书更偏研究性质，有点难读
  - 《陆征祥评传》：从中国外交家陆征祥的史料出发考察清末、北洋到国民政府时期，近代中国与世
    界的互动历程。
  - 《第一圈》：不是自传，胜似自传。诺奖得主索尔仁尼琴以自己的亲身经历为原型，再现了斯大林
    时期的独裁制度对人性的摧残和破坏。
  - 《别闹了，费曼先生：科学顽童的故事》
  - 《我的前半生——爱新觉罗·溥仪》：看完电影《末代皇帝》后，对清朝历史产生了兴趣，打算看
    看。
- 历史与纪实作品
  - 《万历十五年》
  - 《跨越边界的社区（修订版）》：持续至今的真实“北漂”史。转型中的中国城市、流动人口、经济
    与社会。北京“浙江村”与“浙江村人”三十年生活记录研究。
  - 《天朝的崩溃：鸦片战争再研究（修订版）》
  - 《甲午战争前后之晚清战局》
  - 《晚期帝制中国的科举文化史》
  - 《剑桥中国晚清史》：1400 页的一本大部头
  - 《五四运动史：现代中国的知识革命》
  - 《中西文化回眸》：这几本中西文化对比的书，主要是想用于学习以及对比中西文化的差异。
  - 《对岸的诱惑：中西文化交流记》
  - 《中西文化的精神分野》
  - 《血殇：埃博拉的过去、现在和未来》
  - 《向您告知，明天我们一家就要被杀：卢旺达大屠杀纪事》
  - 《东京贫困女子》
- 其他人文社科
  - 《跨学科：人文学科的诞生、危机与未来》
  - 《枪炮、病菌与钢铁》
  - 《西线无战事》
  - 《人类群星闪耀时》
  - 《人体简史》
  - 《时间的秩序》
  - 《极简宇宙史》
  - 《人生脚本》
  - 《语言学的邀请》- 进度 68/288
    - 对语言学有点兴趣，同时听说这本书对表达（沟通、写作）也大有帮助~
  - 《步天歌研究》
- 公益慈善 / NGO
  - 《如何改变世界 - 社会企业家与新思想的威力》：据评社会企业的概念即源自此书
  - 《离开微软 改变世界》
  - 《穷人的银行家》：穷人知道该怎么摆脱贫困，只要你给予平等的借贷的权力。相信并支持每个独
    立人自己的选择。
  - 《撬动公益 - 慈善和社会投资新前沿导论》
  - 《表达的力量 - 当中国公益组织遇上媒体》
  - 《财富的责任与资本主义演变 - 美国百年公益发展的启示》
  - 《为公益而共和 - 阿拉善SEE生态协会治理之路》
  - 《公益創業 - 青年創業與中年專業的新選擇》
  - 《蓝毛衣》：如何成为一个社会企业家，有作者的亲身经历，走过的失败教训与成功经验
- 虚构类
  - Majo no Tabitabi（魔女之旅）Vol.1
  - Tasogare-iro no Uta Tsukai（黄昏色的咏使）Vol.1
  - Moon Palace, by Pual Auster - 读过中文版，但是看英文版词汇量也不高，可以一读
- 文学类：
  - 《百年孤独》：高中的时候读过一遍，但是都忘差不多了
  - 《霍乱时期的爱情》
  - 《苏菲的世界（Sophie's World）》：据说是哲学启蒙读物，曾经看过，但是对内容完全没印象
    了。
  - 《你一生的故事》：我也曾是个科幻迷
  - 《房思琪的初恋乐园》
  - 《月光落在左手上》
  - 《了不起的盖茨比》
  - 《The Windup Girl》：高中时读过中文版，刷新我三观，现在想再读一遍英文原版。
- 技术类
  - 《人月神话》
  - 《绩效使能：超越 OKR》
  - 《奈飞文化手册》
  - 《幕后产品-打造突破式思维》
  - 《重构 - 改善既有代码的设计》
  - 《云原生服务网格 Istio：原理、实践、架构与源码解析》
  - 《凤凰项目：一个 IT 运维的传奇故事》
  - 《一人企业：一个人也能赚钱的商业新模式》
- 英语语法
  - 《English Grammar In Use》
  - 《英语语法新思维——初级教程》 - 8/366
- 神秘学（没准啥时候我就想写点小说...）
  - 《性命圭旨》

## 探索互联网上的高质量内容

> 主要参考自 https://www.owenyoung.com/sources/

> 互联网信息泛滥，我从各种信息来源中挑选了一部分我感兴趣的、受推荐次数较多的信息源列在了这
> 里。也要注意的是，天天看最新的新闻与热点，对个人并没有什么好处。在有兴趣或者无聊的时候翻
> 一翻，了解一下世界的变化就好了。

中国与国际上的政史内容：

- [爱思想网](https://www.aisixiang.com/): 国内的一个学术分享站点，国内许多学者在上面针砭时
  弊。
- [中国 1850 - 1950 年间的各种报纸](https://archive.org/details/eastasia-periodicals)

时事新闻（全英文）：

> 有人精选了一些信息源，并制作了一份中文摘要索引: https://www.buzzing.cc/

- [纽约客](https://www.newyorker.com/): 纽约客是一份美国的文学、艺术和时事杂志，以其对政
  治、文化和时事的评论而闻名。
- [大西洋](https://www.theatlantic.com/): 大西洋是一份美国社论杂志，的特色文章涉及政治、外
  交，商业与经济，文化与艺术，科技和科学等领域。
- [英国卫报](https://www.theguardian.com/uk): 英国卫报是英国的一家全国性报纸。
- [日本读卖新闻](https://www.yomiuri.co.jp/): 日本读卖新闻是日本的一家全国性报纸。
- [半岛电视台](https://www.aljazeera.com/): 卡塔尔的国际媒体，由卡塔尔王室拥有。其特点是中
  东阿拉伯世界的视角。
- 一些新兴媒体
  - [新政治家](https://www.newstatesman.com/): 英国的一份进步政治与文化杂志。
  - [Rest of the world](https://restofworld.org/): 科技报道
  - [NOEMA](https://www.noemamag.com/): 「探索席卷我们世界的变革」，发表有关哲学、治理、地
    缘政治、经济、技术和文化交叉领域的文章。
  - [Semafor](https://www.semafor.com/): 将无可争议的事实与记者对这些事实的分析分开，提供
    不同的和更全面的观点，并分享其他媒体对该主题的有力报道。

---

{{< particles_effect_up  >}}
