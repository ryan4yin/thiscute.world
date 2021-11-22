---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false
---


## 一、我的学习清单

根据个人兴趣，以及工作需求划分优先级。

### 最高优先级

技术：
- rust 语言/go 语言及 web 编程
- Istio: 熟悉 Istio 及 Envoy，了解新版本的功能
- Kubernetes Operator

生活：
- 娱乐+运动：
  - 轮滑：学习侧压步、倒滑后压步

### 高优先级

- k8s 网络插件 - calico/cilium
  - BGP 路由协议
  - vxlan
- Kubernetes：阅读源码，熟悉底层细节

### 中优先级

- Openresty 技术栈：
  - 阅读 Lua 程序设计
  - 阅读 APISIX 源码 + Openresty
  - 深入学习 Nginx 及 epoll

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
  - 实现简单的数据库：tinysql/tinykv  


### 低优先级

- linux 性能测试、优化及相关工具
  - eBPF

- 深入理解计算机网络：数据包的构造、 raw socket，Linux TCP/IP 协议栈

- MIT 6.824：《数据密集型应用系统设计》raft

- redis 底层
- mysql/postgresql 底层

- 算法与数据结构：这个就在学 Linux/Redis/SQL 的过程中穿插着学吧。

- 英语词汇量
- 学习简单的 Parser 原理：《编程语言实现模式》


### 其他比较感兴趣的东西

- 微积分、线代、概率论、数学物理方法
- 信号与系统、数字信号处理、音视频处理
- 机器学习、深度学习
- 《声学基础》、《理论声学》、《空间声学》：虽然大学学的一塌糊涂，现在居然又有些兴趣想学来玩玩，写些声学仿真工具试试。
- 语音合成、歌声合成
- 高难度的研究课题
  - 声学模拟：[揉搓声模拟](http://www.cs.columbia.edu/cg/crumpling/)


## 二、我想读的书

- [Computer Systems: A Programmer's Perspective, 3/E (CS:APP3e)](http://www.csapp.cs.cmu.edu/)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [The Linux Programming Interface](https://www.man7.org/tlpi/index.html)
- Computer Networking: A Top-Down Approach, 7th Edition
- [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html)



---

## 三、此时此刻的我

主要记录下业余时间我都在干些啥。

### now

目前想做的：
- Envoy、Cilium
- 搞一搞 rust 编程，go web 编程

### 2021-11-21

- 轮滑：复习前双鱼、前剪、前蛇，尝试侧压步、倒滑

### 2021-11-08 - 2021-11-12

- 将上次 EKS 升级过程中，有问题的服务迁移到 1.21 的 EKS 集群，直接切线上流量测试。
  - 复现了问题，通过 JFR + pods 数量监控，确认到是服务链路上的个别服务频繁扩缩容导致的，这些服务比较重，对扩缩容比较敏感。
  - 测试在 HPA 中添加 behavior 降低缩容速率，同时添加上 PodDisruptionBudget 以避免节点回收导致大量 Pod 被回收，经测试问题基本解决。
- 遭遇 AWS EKS 托管的控制平面故障，controller-manager 挂了一整天。现象非常奇怪，又是第一次遇到，导致长时间未排查到问题。


### 2021-10-23

- 跟公司冲浪小分队，第一次玩冲浪，最佳成绩是在板上站了大概 6s...

### 2021-10/11 - 2021-10-19

- 将 EKS 集群从 1.17 升级到 1.21（新建集群切量的方式），但是遇到部分服务迁移后可用率抖动。
  - 未定位到原因，升级失败，回滚了流量。

### 2021-09-13 - 2021-09-17

- 学习极客时间《10X程序员工作法》
  - 以终推始
  - 识别关键问题
  - ownership

### 2021-09-02 - 2021-09-11

- EKS 集群升级
  - 了解 EKS 集群的原地升级的细节
  - 输出 EKS 集群原地升级的测试方案，以及生产环境的 EKS 集群升级方案
- 学习使用 kubeadm+containerd 部署 k8s 测试集群
  - 涉及到的组件：Kuberntes 控制面、网络插件 Cilium、kube-proxy、coredns、containerd

---

### 2021-08-31 - 2021-09-01

- 思考我在工作中遇到的一些非技术问题，寻找解法
    - 效率：如何在没人 push 的情况下（没有外部压力），维持住高效率的工作状态（早早干完活下班它不香么？）。
      - 建立有效的「自检」与「纠错」机制
        - 自检：
          - 列出目前已知的「异常」和「健康」两类工作状态，每日做一个对比。
          - 每日都列一下详细的工作计划，精确到小时（预留 1 小时 buffer 应对临时需求）。
    - 沟通：遇到问题（各种意义上的问题）时，及时沟通清楚再继续推进，是一件 ROI 非常高的事。否则几乎肯定会在后面的某个节点，被这个问题坑一把。
    - 目前的关键目标是啥？存在哪些关键问题（实现关键目标最大的阻碍）？我最近做的主要工作，是不是在为关键目标服务？
  - 如何把安排到手上的事情做好？
    - 思考这件事情真正的目标的什么？
      - 比如任务是排查下某服务状态码有无问题，真正的目的应该是想知道服务有没有异常
    - 达成真正的目标，需要做哪些事？
      - 不仅仅状态码需要排查，还有服务负载、内存、延迟的分位值，或许都可以看看。
    - 跟需求方沟通，询问是否真正需要做的，是前面分析得出的事情。

这些问题都是有解法的，关键是思路的转换。

---

### 2021-08-28 => 2021-08-29

- 容器底层原理：
  - linux namespace 与 cgroups
  - linux 虚拟网络接口 macvlan/ipvlan、vlan、vxlan

---

### 2021-08-19 => 2021-08-23

- 阅读 rust 语言的官方文档：the book
- 边读文档边做 rustlings 的小习题
  - 目前完成了除 macros 之外的所有题
  - 遇到的最难的题：conversions/{try_from_into, from_str}
- 使用 rust 重写了一版 video2chars

---

### 2021-08-12 => 2021-08-16

- Linux 的虚拟网络接口
- Linux 的 netfilter 网络处理框架，以及其子项目 iptables/conntrack

---

### 2021-03-11 => 2021-08-09

- 学习 nginx - openresty - apisix
- 工作中，在自己负责的领域，建立起 ownership
- 学习新公司的工作模式：OKR 工作法
- 学习新公司的思维模式（识别关键问题）
  - 如何从公司的角度去思考问题，找到我们目前最应该做的事情
  - 从以下角度去评价一件事情的重要性
    - 这件事情对我们目前的目标有多大帮助？
    - 需要投入多少资源和人力？
    - 在推进过程中，有哪些阶段性成果或者 check point？

---
