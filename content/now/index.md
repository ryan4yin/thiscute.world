---
title: "此时此刻的我"
date: 2021-02-01T14:14:35+08:00
draft: false
---


## 一、我的学习清单

根据个人兴趣，以及工作需求划分优先级。

列清单的目的：
- 指明方向：目前我对哪些知识感兴趣，或者哪些知识对我最有用。把时间花在哪一部分知识上是 ROI 最高的？

### 最高优先级

技术：
- 阅读 Lua 程序设计
- 阅读 APISIX 源码
- 深入学习 Openresty
- 深入学习 Nginx 及 epoll

非技术：
- 学习极客时间《10X程序员工作法》
- 每周单独抽出一部分时间（1h+），思考工作中遇到的一些非技术问题，寻找解法
- 如何把排到手上的事情做好？


### 高优先级

- Kubernetes Operator
- 容器底层原理
  - 容器镜像的文件系统：overlayfs
  - 镜像的结构分析
  - 镜像的构建流程
- k8s 网络插件 - calico/flannel
  - BGP 路由协议
  - vxlan

### 中优先级

- MIT 6.824：《数据密集型应用系统设计》raft
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
- redis 底层
- mysql/postgresql 底层
- 英语词汇量


## 二、我想读的书

- [Computer Systems: A Programmer's Perspective, 3/E (CS:APP3e)](http://www.csapp.cs.cmu.edu/)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [The Linux Programming Interface](https://www.man7.org/tlpi/index.html)
- Computer Networking: A Top-Down Approach, 7th Edition
- [Systems Performance: Enterprise and the Cloud, 2nd Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html)



---

## 三、此时此刻的我

### now

- 阅读 Lua 程序设计
- 阅读 APISIX 源码
- 思考我遇到的一些非技术问题（工作、生活都有吧），寻找解法
  - 工作：
    - 效率：如何在没人 push 的情况下，维持住高效率的工作状态。
    - 沟通：遇到问题（各种意义上的问题）时，及时沟通清楚再继续推进，是一件 ROI 非常高的事。否则几乎肯定会在后面的某个节点，被这个问题坑一把。
    - 目前的关键目标是啥？存在哪些关键问题（实现关键目标最大的阻碍）？我最近做的主要工作，是不是在为关键目标服务？


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
