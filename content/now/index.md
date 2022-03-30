---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

## 我正在研究这些

- 学习使用 [Istio EnvoyFilter](https://istio.io/latest/docs/reference/config/networking/envoy-filter/)，分析 Envoy Sidecar 的动态配置、流量代理、监控指标等实现细节。
  - 重点关注：负载均衡策略、prometheus 指标插件、slow_start 模式、gzip 压缩、gRPC 支持、Zone Aware Load Balancing、基于 iptables/tproxy 的 outbound 流量代理
- 研究使用 [aws/karpenter](https://github.com/aws/karpenter) 实现集群弹性扩缩容 - 进度 20%
- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 54%
- 区块链技术 Web3.0
  - [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook) - 以太坊入门 - 36%
  - [以太坊开发者文档](https://ethereum.org/zh/developers/docs/intro-to-ethereum/) - 以太坊进阶
  - [Youtube - Solidity, Blockchain, and Smart Contract Course – Beginner to Expert Python Tutorial](https://www.youtube.com/watch?v=M576WGiDBdQ)

## 我最近还想搞搞这些


- go web 编程: 完成 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go) 这个项目


## 我的学习清单

技术上，目前的重点仍然是网络技术与 Kubernetes 技术，缓存/搜索/数据库等技术还得靠后排，或许明年吧哈哈。

生活上，就完全看个人兴趣安排了，目前对音乐、轮滑、阅读比较感兴趣。

### 最高优先级

技术：
- 学习使用 Istio EnvoyFilter
- go web 编程: 完成 [xhup-club-api-go](https://github.com/coding-and-typing/xhup-club-api-go) 这个项目

生活：
- 娱乐+运动：
  - 轮滑：倒滑后压步

阅读（一二三月份，就读这两本吧）：

- [x] 《人间失格》
- [x] [Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)
- [ ] 《在生命的尽头拥抱你-临终关怀医生手记》


### 高优先级

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

阅读（四五六月份的书单）：

- [ ] 《生命最后的读书会》
- [ ] 《在峡江的转弯处 - 陈行甲人生笔记》
- [ ] 《分析与思考 - 黄奇帆的复旦经济课》
- [ ] 《经济学原理（第七版）》

生活：
- 音乐：Synthesizer V, 练习键盘

- k8s 网络插件 - Cilium
- Kubernetes：阅读源码，熟悉底层细节
- 计算机网络：
  - Computer Networking: A Top-Down Approach, 7th Edition
  - BGP 路由协议
  - vxlan
- 数据库: [SQL进阶教程](https://book.douban.com/subject/27194738/)

### 中优先级

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

### 低优先级

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


### 其他暂时排不上号的兴趣点


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
