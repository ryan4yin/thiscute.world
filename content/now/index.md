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
- 研究使用 [aws/karpenter](https://github.com/aws/karpenter) 或 [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler) 实现集群弹性扩缩容 - 进度 20%
- 研究清楚 NAT 网关：
  - NAT 的原理、结构
  - Kubernetes/Docker 网络所使用的 NAT
  - AWS NAT 网关
  - P2P 内网穿透: zerotier/tailscales
  - Kubernetes 跨 NAT 组网、将开发机器接入 Kubernetes 网络：适合用于本地/云上 K8s 调试
- 学习使用 [Istio EnvoyFilter](https://istio.io/latest/docs/reference/config/networking/envoy-filter/)，分析 Envoy Sidecar 的动态配置、流量代理、监控指标等实现细节。
  - 重点关注：负载均衡策略、prometheus 指标插件、slow_start 模式、gzip 压缩、gRPC 支持、Zone Aware Load Balancing、基于 iptables/tproxy 的 outbound 流量代理
- 《在生命的尽头拥抱你-临终关怀医生手记》


## 二、我最近还想搞搞这些

- 机器学习
  - [Machine Learning for Beginners - MicroSoft](https://github.com/microsoft/ML-For-Beginners): ML 入门
  - [100-Days-Of-ML-Code](https://github.com/Avik-Jain/100-Days-Of-ML-Code): ML 入门
- go web 编程: 完成 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go) 这个项目


## 三、今年的阅读进展

>电子版都可以在 z-library 上很方便地下载到，实体书的话可以在多抓鱼等二手书平台碰碰运气。

已读：

- [x] 《人间失格》
- [x] 《月宫》
- [x] 《[Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)》
- [x] 《[Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)》

正在读：

- [ ] 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 61%
- [ ] 《Go 程序设计语言（英文版）》 - 进度 7/13

计划读：

- [ ] 《Social Psychology, 13e, David Myers》
- [ ] 《Principles Of Economics, 9e, N. Gregory Mankiw》
- [ ] 《Computer Networking - A Top-Down Approach, 7e》
  - 这本书我以前学过一次，但是主要只学了应用层到传输层的内容。这次重点关注传输层、网络层。
- [ ] 《生命最后的读书会》
- [ ] 《月光落在左手上》
- [ ] 《分析与思考 - 黄奇帆的复旦经济课》
- [ ] 《在峡江的转弯处 - 陈行甲人生笔记》
- [ ] 《刘擎西方现代思想讲义》
- [ ] 《复杂 - 梅拉尼 米歇尔》
- [ ] 《Go 语言学习笔记 - 雨痕》
  - 下卷是源码剖析，基于 Go 1.6, 打算在看完《Go 程序设计语言》后看看这本

## 四、我的备选书单

如下是我目前想读的书单，如果决定读，就把对应的书移到「计划读」中。

- 文学类：
  - [ ] 《百年孤独》：高中的时候读过一遍，但是都忘差不多了
  - [ ] 《霍乱时期的爱情》
  - [ ] 《苏菲的世界》：据说是哲学启蒙读物，曾经看过，但是对内容完全没印象了。
  - [ ] 《你一生的故事》：我也曾是个科幻迷
  - [ ] 《沈从文的后半生》
  - [ ] 《我与地坛》
  - [ ] 《将饮茶》
  - [ ] 《吾国与吾民 - 林语堂》
  - [ ] 《房思琪的初恋乐园》
  - [ ] 《可是我偏偏不喜欢》
- 人文社科
  - [ ] 《爱的艺术》
  - [ ] 《亲密关系》
  - [ ] 《怎样征服美丽少女》：哈哈，之前在豆瓣还是哪看到的，听说很有用。
  - [ ] 《被讨厌的勇气》
  - [ ] 《人体简史》
  - [ ] 《科学革命的结构》
  - [ ] 《邓小平时代》
  - [ ] 《论中国》
  - [ ] 《时间的秩序》
  - [ ] 《极简宇宙史》
  - [ ] 《圆圈正义-作为自由前提的信念》
  - [ ] 《人生脚本》
- 技术类
  - [ ] 《SRE - Google 运维解密》
  - [ ] 《凤凰项目：一个 IT 运维的传奇故事》
  - [ ] 《人月神话》
  - [ ] 《绩效使能：超越 OKR》
  - [ ] 《奈飞文化手册》
  - [ ] 《幕后产品-打造突破式思维》
  - [ ] 《深入 Linux 内核架构》
  - [ ] 《Linux/UNIX 系统编程手册》
  - [ ] 《重构 - 改善既有代码的设计》
  - [ ] 《网络是怎样连接的》：曾经学习过《计算机网络：自顶向下方法》，不过只学到网络层。就从这本书开始重新学习吧。
- 经济学
  - [ ] 《手把手教你读财报》
  - [ ] 《投资中最简单的事》
  - [ ] 《Principles for Dealing with the Changing World Order》


## 五、我的知识清单

### 1. 最高优先级

技术：
- 学习使用 Istio EnvoyFilter
- go web 编程: 完成 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go) 这个项目

生活：
- 娱乐+运动：
  - 轮滑：倒滑后压步

### 2. 高优先级

- 研究 K8s 集群的节点伸缩优化、服务稳定性优化
  - [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler)
  - [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler)
  - [aws/karpenter](https://github.com/aws/karpenter)

- kubebuilder: 使用 kubebuilder 完成一个实用 operator.
- 服务网格
  - Cilium Service Mesh - 使用 eBPF + per-node proxy 实现 的服务网格，很有前景。
  - Zone Aware Load Balancing - 减少跨区流量
  - 如何调优数据面，降低 CPU 使用率及延迟
  - [学习与测试各种负载均衡策略](https://github.com/ryan4yin/knowledge/blob/master/network/proxy%26server/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E7%AE%97%E6%B3%95.md): 需要持续更新这份文档 - 50%

- 日志方案调研：grafana loki
- 配置管理：研究如何使用 vault 实现跨集群的动态配置支持，如何落地此项能力

生活：
- 音乐：Synthesizer V, 练习键盘

- k8s 网络插件 - Cilium
- Kubernetes：阅读源码，熟悉底层细节
- 计算机网络：
  - Computer Networking: A Top-Down Approach, 7th Edition
  - BGP 路由协议
  - vxlan
- 数据库: [SQL进阶教程](https://book.douban.com/subject/27194738/)

### 3. 中优先级

- 研究 K8s 集群的 Pod 拓扑优化
  - Pod/Node 亲和性与反亲和性
  - [descheduler](https://github.com/kubernetes-sigs/descheduler)

- rust 语言

- 容器底层原理
  - 容器镜像的文件系统：overlayfs
  - 镜像的结构分析
  - 镜像的构建流程

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


- 操作系统：
  - [The Linux Programming Interface](https://www.man7.org/tlpi/index.html)
  - [Computer Systems: A Programmer's Perspective, 3/E (CS:APP3e)](http://www.csapp.cs.cmu.edu/)
  - [flash-linux0.11-talk](https://github.com/sunym1993/flash-linux0.11-talk)

- 编译原理
  - [自制编译器](https://book.douban.com/subject/26806041/)
  - [Programming Language Pragmatics, Fourth Edition](https://book.douban.com/subject/26424018/)
  - [Crafting Interpreters](http://craftinginterpreters.com/contents.html)

- 学习英语，目标是能流利地读写交流。
  - 主要是可以扩宽工作的选择面，外企很多职位会要求英文读写流利。

### 4. 低优先级

- 操作系统：
  - [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html)

- 编译原理（如何实现一个编程语言）
  - [编译器设计（第2版）](https://book.douban.com/subject/20436488/)
  - [编程语言实现模式](https://book.douban.com/subject/10482195/)

- Openresty 技术栈：（暂时感觉兴趣不大）
  - 阅读《Lua 程序设计》
  - 阅读 APISIX 源码 + Openresty
  - 深入学习 Nginx 及 epoll

- [进阶]数据库、数据结构与算法
  - MIT 6.824：[Designing Data-Intensive Applications](https://dataintensive.net/)
  - redis 底层
  - mysql/postgresql 底层
  - [Readings in Database Systems](https://book.douban.com/subject/2256069/)


### 5. 其他暂时排不上号的兴趣点


- 值得了解的数据库
  - OLAP
    - ClickHouse
    - Snowflake
    - Druid
    - ElasticSearch
  - HTAP
    - TiDB
    - PostgreSQL
  - 键值数据库
    - Redis
    - Etcd
    - 底层数据库：boltdb/rocksdb/leveldb
  - 文档数据库
    - MongoDB
  - 时序数据库
    - VictoriaMetrics
    - Prometheus
  - 特征向量搜索 / 相似度搜索 / 视频搜索 / 语义搜索
  - 图数据库
    - https://github.com/dgraph-io/dgraph

- 机器学习、深度学习

- 大数据技术
  - ETL
  - Spark
  - 数据湖

- 编程语言
  - Elixir
  - Kotlin

- 编程语言理论（如何设计一个编程语言）
  - [Essentials of Programming Languages, 3rd Edition](https://book.douban.com/subject/3136252/)
  - [The Little Schemer - 4th Edition ](https://book.douban.com/subject/1632977/)

- 微积分、线代、概率论、数学物理方法

- 信号与系统、数字信号处理、音视频处理
- 《声学基础》、《理论声学》、《空间声学》：虽然大学学的一塌糊涂，现在居然又有些兴趣想学来玩玩，写些声学仿真工具试试。
  - 语音合成、歌声合成
  - 声学模拟：[揉搓声模拟](http://www.cs.columbia.edu/cg/crumpling/)


---
