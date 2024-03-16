---
title: "曾经的我 - 2021"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false

# 此页禁用评论系统
comment:
  utterances:
    enable: false
  waline:
    enable: false
---

![](/images/now/book-shelf-1.webp)

> 记录下我的学习轨迹。（结果写着写着有点像是技术笔记跟日记的混合了 hhhh）

全部历史记录：[/history](/history/)

### 2021-12-12

- 练习二个半小时轮滑，学会了压步转弯技术
- 无聊，但是又啥都不想干，耽于网络小说...
- 感觉有点现充了，感觉需要找个更明确的、能给人动力的目标
  - 做个三年的职业规划以及生活规划？

### 2021-11-21

- 轮滑：复习前双鱼、前剪、前蛇，尝试侧压步、倒滑

### 2021-11-08 - 2021-11-12

- 将上次 EKS 升级过程中，有问题的服务迁移到 1.21 的 EKS 集群，直接切线上流量测试。
  - 复现了问题，通过 JFR + pods 数量监控，确认到是服务链路上的个别服务频繁扩缩容导致的，这
    些服务比较重，对扩缩容比较敏感。
  - 测试在 HPA 中添加 behavior 降低缩容速率，同时添加上 PodDisruptionBudget 以避免节点回收
    导致大量 Pod 被回收，经测试问题基本解决。
- 遭遇 AWS EKS 托管的控制平面故障，controller-manager 挂了一整天。现象非常奇怪，又是第一次
  遇到，导致长时间未排查到问题。
  - 确认问
    题[来自 HPA behavior 的 Bug](https://github.com/kubernetes/kubernetes/issues/107038)
    1. 储存于 etcd 中的 object 仅会有一个版本，透过 apiserver 读取时会转换成请求的
       autoscaling API 版本。
    2. autoscaling/v2beta2 scaleUp 及 scaleDown 对象不能为 null，并
       在[其 Kubernetse 代码](https://github.com/kubernetes/kubernetes/blob/6ac2d8edc8606ab387924b8b865b4a69630080e0/pkg/apis/autoscaling/v2/defaults.go#L104)可
       以查看到相应的检查机制。
    3. 当使用 autoscaling/v1 时，v2beta2 版本中的相关对象字段将作为 annotation 保
       留，apiserver 不会检查 ScaleUp/ScaleDown 的 annotation 是否为 non-null，而导致
       kube-controller-manager panic 问题。
    4. 我们可以使用 v1 或 v2beta2 创建一个 HPA 对象，然后使用 v1 或 v2beta2 读取、更新或删
       除该对象。 etcd 中存储的对象只有一个版本，每当您使用 v1 或 v2beta2 获取 HPA 对象
       时，apiserver 从 etcd 读取它，然后将其转换为您请求的版本。
    5. 在使用 kubectl 时，客户端将默认使用 v1(`kubectl get hpa`)，因此我们必须明确请求
       v2beta2 才能使用这些功能(`kubectl get hpa.v2beta2.autoscaling`)
    6. 如果在更新 v1 版本的 HPA 时（kubectl 默认用 v1），手动修改了 v2beta2 功能相关的
       annotation 将 scaleUp/scaleDown 设为 null，会导致 controller-manager 挂掉.

### 2021-10-23

- 跟公司冲浪小分队，第一次玩冲浪，最佳成绩是在板上站了大概 6s...

### 2021-10/11 - 2021-10-19

- 将 EKS 集群从 1.17 升级到 1.21（新建集群切量的方式），但是遇到部分服务迁移后可用率抖动。
  - 未定位到原因，升级失败，回滚了流量。

### 2021-09-13 - 2021-09-17

- 学习极客时间《10X 程序员工作法》
  - 以终推始
  - 识别关键问题
  - ownership

### 2021-09-02 - 2021-09-11

- EKS 集群升级
  - 了解 EKS 集群的原地升级的细节
  - 输出 EKS 集群原地升级的测试方案，以及生产环境的 EKS 集群升级方案
- 学习使用 kubeadm+containerd 部署 k8s 测试集群
  - 涉及到的组件：Kubernetes 控制面、网络插件 Cilium、kube-proxy、coredns、containerd

### 2021-08-31 - 2021-09-01

- 思考我在工作中遇到的一些非技术问题，寻找解法
  - 效率：如何在没人 push 的情况下（没有外部压力），维持住高效率的工作状态（早早干完活下班
    它不香么？）。
    - 建立有效的「自检」与「纠错」机制
      - 自检：
        - 列出目前已知的「异常」和「健康」两类工作状态，每日做一个对比。
        - 每日都列一下详细的工作计划，精确到小时（预留 1 小时 buffer 应对临时需求）。
  - 沟通：遇到问题（各种意义上的问题）时，及时沟通清楚再继续推进，是一件 ROI 非常高的事。
    否则几乎肯定会在后面的某个节点，被这个问题坑一把。
  - 目前的关键目标是啥？存在哪些关键问题（实现关键目标最大的阻碍）？我最近做的主要工作，是
    不是在为关键目标服务？
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

- 入职大宇无限
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

{{< particles_effect_up  >}}
