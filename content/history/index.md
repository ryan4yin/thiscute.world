---
title: "曾经的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

记录下我的学习轨迹。

### 2022-05-05

- 学习极客时间专栏《深入浅出 Kubernetes》 - 20%
  - Kubernetes 与其他败北的编排工具比，最大的优势在于它的设计思想：
    - 从更宏观的角度，以统一的方式来定义任务之间的各种关系（最底层是 Pod 与 PV，之上是各种控制器、亲和反亲和、拓扑扩散、自定义控制器，网络侧有 service，底层网络插件等等），并为将来支持更多种类的关系留有余地（开放、强大的自定义能力催生出了丰富的生态）
    - 基于状态的声明式配置，由控制器负责自动达成期望的状态

### 2022-05-02

- 学习[Go语言动手写Web框架](https://geektutu.com/post/gee.html) - 进度 20%


### 2022-05-01

- 研究 FinOps 与 kubecost，完成一篇 Kubernetes 成本分析的文章 - 50%

### 2022-04-26 - 2022-04-28

- 学习极客时间专栏《深入浅出 Kubernetes》，复习容器技术（Namespace/Cgroups/rootfs）
- 2022-04-28 调薪结果出来了，突然觉得身心都有点累了，有点惆怅。总之还是继续努力吧，技术才是我的核心竞争力，少管他什么妖风邪雨。

### 2022-04-25

- 完成了 19 年创建的 go 项目：https://github.com/ryan4yin/video2ascii
- 失眠，半夜随便翻了翻，把《Go 程序设计语言（英文版）》走马观花过了一遍
- 阅读 [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/) - 进度 7%
  - 主要是通过案例讲解 CRD Operator Controller 等 Kubernetes 编程技术

### 2022-04-24

- 阅读《Go 程序设计语言（英文版）》 - 进度 90%
  - 目前还剩两章未读：反射 reflection 与底层编程 unsafe/uintptr

### 2022-04-22 - 2022-04-23

- 阅读《Go 程序设计语言（英文版）》 - 进度 72%
    - 主要完成了 goroutines/channels 以及「并发与变量共享 sync」两个章节


### 2022-04-21

- 多抓鱼买的一批新书到手了，大致读了下几本书的前几页。
  - 目前比较感兴趣的有：《复杂》、《陈行甲人生笔记》、《原则 - 应对变化中的世界秩序》、《这才是心理学》
  - 打算首先读《复杂》
- 使用 [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler) 实现集群弹性扩缩容
  - 发现社区的这个工具（简称 CA），确实没 aws 出品的 karpenter 好用。
  - CA 自身的实现很简单，主要是依靠 AWS ASG 实现扩缩容。
  - 而 EKS 的 NodeGroup 说实话做得太垃圾了，底层 ASG 的很多功能它都不支持，一旦创建很多参数（VPC 参数、实例类型、等等）就无法通过 EKS NodeGroup 变更了。如果越过 EKS NodeGroup 直接修改底层的 ASG 配置，它还会提示「Degraded」说配置不一致，真的是无力吐槽。

### 2022-04-20

- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 73%
- 使用 [aws/karpenter](https://github.com/aws/karpenter) 实现集群弹性扩缩容
  - 已上线 prod 环境，目前给 EMR on EKS 集群专用。
- 更新 /now 页面以及 knowledge 的内容

### 2022-04-18

- 研究使用 [aws/karpenter](https://github.com/aws/karpenter) 实现集群弹性扩缩容
- 阅读《Go 程序设计语言（英文版）》 - 进度 53%
  - 第 7 章「接口」读了一半，大概 22 pages，预计明天能完成
- [ ] 《[Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)》
  - 读到 Introduction 一章，行文真的很有趣，看 projects 也有深度，决定了要把这本书看完，把习题做好。
  - OSTEP 后面的部分会涉及 vx6 源码，这要求比较深的 C 语言知识以及 x86 汇编知识，不过这些可以在学到的时候，再做补充。
  - 在需要用到的时候，学习 CSAPP 的 x86 汇编部分会是一个比较好的补充。

### 2022-04-17

- 阅读《Go 程序设计语言（英文版）》 - 进度 7/13
- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 61%
- 重新整理书单，放到 /now 页面中
- 学习 NAT 原理知识

### 2022-04-15 ~ 2022-04-16 

- 阅读《Go 程序设计语言（英文版）》 - 进度 5/13

### 2022-04-14

- 阅读《Go 程序设计语言（英文版）》 - 进度 4/13

### 2022-04-13

- 阅读《Go 程序设计语言（英文版）》 - 进度 3/13

### 2022-04-10

- 学习 3D 引擎的使用，简单试用了 unity3d 与 unreal engine 5.
  - 确定学习方向：先学学 UE5 蓝图入个门，然后试试把 MMD 模型导入到 UE5 做做动画，中间也会简单接触下 Blender.
  - 感受：UE5 挺不错的，尤其是它还提供 VR 编辑模式，手上的 Quest 2 又能派上用场了
  - 输出文档：[3D 图形相关](https://github.com/ryan4yin/knowledge/tree/master/graphics)
- 阅读《Go 程序设计语言（英文版）》 - 进度 2/13
  - 第一章「导览」大概过了下 Go 的关键特性：完善的工具链，丰富的标准库，goroutine, channel
  - 第二章主要讲程序结构，包含变量、类型声明、指针、结构体、作用域、包与文件结构等等

### 2021-04-08 - 2021-04-09

- 学习区块链技术 Web3.0
  - [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook) - 以太坊入门
    - 进度：100%
    - 跳过了智能合约代码相关的内容，因为代码比较老了，新版本的 solidity 有了许多新变化。
  - [Youtube - Solidity, Blockchain, and Smart Contract Course – Beginner to Expert Python Tutorial](https://www.youtube.com/watch?v=M576WGiDBdQ)
    - 这个视频及相关的 Github 仓库，包含一些区块链可视化以及相关的介绍，更适合学习完理论后，实战合约编写
  - [区块链技术指南](https://github.com/yeasy/blockchain_guide): 《Docker - 从入门到实践》作者的新书，内容同样简洁易懂，侧重介绍原理及知识面，非常棒。

### 2021-03-26 - 2021-04-01

- 学习区块链技术 Web3.0
  - [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook) - 以太坊入门
    - 进度：7/14
    - 这书适合用于学习理论，solidity 开发相关的内容可以跳过，即 7/8 两章
  - [Youtube - Solidity, Blockchain, and Smart Contract Course – Beginner to Expert Python Tutorial](https://www.youtube.com/watch?v=M576WGiDBdQ)
    - 这个视频及相关的 Github 仓库，包含一些区块链可视化以及相关的介绍，更适合学习完理论后，实战合约编写


### 2021-03-23 - 2021-3-25

- 阅读《在生命的尽头拥抱你-临终关怀医生手记》
- 在 Manager 的帮助下申请职级晋升（初级 => 中级 SRE）
  - 再一次认识到我自己写的文字有多么随意... Manager 帮我提炼补充后，文字变得言简意赅，精确客观，瞬间高大上档次了。

### 2021-03-22

- 注册[模之屋](https://www.aplaybox.com)，简单学了下 MMD 跟 [Blender](https://www.blender.org/)

### 2021-03-15 - 2021-03-19

- 学习 Envoy，完成 [Envoy 笔记](https://github.com/ryan4yin/knowledge/tree/master/network/proxy%26server/envoy)


### 2021-03-11 - 2021-03-14

- 《写给开发人员的实用密码学》
  - 完成第七篇「非对称加密算法」的 ECC 部分，并为 RSA 部分补充了部分 Python 代码
  - 将去年写的文章《TLS 协议、TLS 证书、TLS 证书的配置方法、TLS 加密的破解手段》改写并补充内容，改名为《写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议》
  - 为第五篇「密钥交换」补充了 DHKE/ECDH 的代码示例，另外还补充了 DHE/ECDHE 一节
  - 此系列文章的其他小修改与润色
- 业务大佬在 gRPC 的基础上再添加了 gzip 压缩，TX 流量再次下降 80%+
  - 侧面说明以前业务侧对 HTTP 的用法是多么豪放 emmmm
  - 周末上 gzip 压缩功能，业务大佬太肝了啊...

### 2022-03-09

- 发布《写给开发人员的实用密码学》系列第七篇：非对称加密算法，但是暂时只完成了 RSA 部分

### 2022-03-07 - 2022-03-08

- 跟推荐系统大佬一起将服务从 HTTP 切换到 gRPC，效果立竿见影，服务流量下降 50% ~ 60%，延迟下降 30% ~ 50%
  - 提升了服务性能，降低了 AWS 跨区流量成本

### 2022-03-05 - 2022-03-06

- 发布《写给开发人员的实用密码学》系列的第六篇：对称加密算法

### 2022-03-01

- 深圳疫情形式严峻，开始居家办公
- 整理润色后，发布《写给开发人员的实用密码学》前五篇的内容

### 2022-02-19 - 2022-02-25

- 阅读 [Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)，同时完成我的密码学笔记
  - 起因是想学下区块链技术，结果发现课程一开始就讲加密哈希函数的基本性质，就决定先搞一波密码学。
- 完成了《写给开发人员的实用密码学》前五篇的草稿。
- [研究 istio 的 gRPC 支持与监控指标](https://github.com/ryan4yin/knowledge/blob/master/kubernetes/service_mesh/istio/Istio%20%E7%9B%91%E6%8E%A7%E6%8C%87%E6%A0%87.md)

### 2022-02-17

- 发现我们的 EKS 集群主使用的是 AWS Spot 实例，这类实例的 c6i/c6g 性能与价格差距并不高，做 ARM 化的 ROI 貌似并不高
- 发现对 aws 的 RDS/EC2-Volume/Redis 等资源进行全面评估，删掉闲置资源、缩小实例/集群规格，可以轻易节省大量成本（说明以前申请资源时风格比较豪放 2333）
- 继续迭代个人博客

### 2022-02-07 - 2022-02-16

- 迭代我的独立博客 <https://thiscute.world>
  - 添加「阅读排行」页，定期从 Google Analytics 同步数据
  - 从博客园迁移部分有价值的文章到独立博客


### 2022-01-08 - 2022-01-16

- 购入 Synthesizer V + 青溯 AI 声库，简单调了几首歌试试，效果非常棒。
- 也调研了下[歌声合成领域目前的进展](https://github.com/ryan4yin/knowledge/tree/master/music/vocal%20synthesizer)，试用了免费的移动端软件 [ACE 虚拟歌姬](https://www.taptap.com/app/189147?hreflang=zh_CN)，渲染效果真的媲美 CNY 999 的 SynthV AI 套装，不得不感叹 AI 的效果真的强啊。

### 2022-01-01

- 了解 APISIX/Nginx/Envoy 中的各种负载均衡算法，及其适用场景、局限性。

### 2021-12-12

- 练习二个半小时轮滑，学会了压步转弯技术
- 无聊，但是又啥都不想干，耽于网络小说...
- 感觉有点现充了，感觉需要找个更明确的、能给人动力的目标
  - 做个三年的职业规划以及生活规划？

### 2021-11-21

- 轮滑：复习前双鱼、前剪、前蛇，尝试侧压步、倒滑

### 2021-11-08 - 2021-11-12

- 将上次 EKS 升级过程中，有问题的服务迁移到 1.21 的 EKS 集群，直接切线上流量测试。
  - 复现了问题，通过 JFR + pods 数量监控，确认到是服务链路上的个别服务频繁扩缩容导致的，这些服务比较重，对扩缩容比较敏感。
  - 测试在 HPA 中添加 behavior 降低缩容速率，同时添加上 PodDisruptionBudget 以避免节点回收导致大量 Pod 被回收，经测试问题基本解决。
- 遭遇 AWS EKS 托管的控制平面故障，controller-manager 挂了一整天。现象非常奇怪，又是第一次遇到，导致长时间未排查到问题。
  - 确认问题来自 HPA behavior 的 Bug
    1. 储存于 etcd 中的 object 仅会有一个版本，透过 apiserver 读取时会转换成请求的 autoscaling API 版本。
    2. autoscaling/v2beta2 scaleUp 及 scaleDown 对象不能为 null，并在[其 Kubernetse 代码](https://github.com/kubernetes/kubernetes/blob/6ac2d8edc8606ab387924b8b865b4a69630080e0/pkg/apis/autoscaling/v2/defaults.go#L104)可以查看到相应的检查机制。
    3. 当使用 autoscaling/v1 时，v2beta2 版本中的相关对象字段将作为 annotation 保留，apiserver 不会检查 ScaleUp/ScaleDown 的 annotation是否为 non-null，而导致 kube-controller-manager panic 问题。
    4. 我们可以使用 v1 或 v2beta2 创建一个 HPA 对象，然后使用 v1 或 v2beta2 读取、更新或删除该对象。 etcd 中存储的对象只有一个版本，每当您使用 v1 或 v2beta2 获取 HPA 对象时，apiserver 从 etcd 读取它，然后将其转换为您请求的版本。
    5. 在使用 kubectl 时，客户端将默认使用 v1(`kubectl get hpa`)，因此我们必须明确请求 v2beta2 才能使用这些功能(`kubectl get hpa.v2beta2.autoscaling`)
    6. 如果在更新 v1 版本的 HPA 时（kubectl 默认用 v1），手动修改了 v2beta2 功能相关的 annotation 将 scaleUp/scaleDown 设为 null，会导致 controller-manager 挂掉.


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
