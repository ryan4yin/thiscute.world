---
title: "2021 年年终总结"
date: 2022-12-23T10:12:45+08:00
lastmod: 2022-12-23T10:12:45+08:00
draft: true

resources:
- name: "featured-image"
  src: "featured-image.webp"

tags: []
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

## 闲言碎语


是的又过去一年，又到了一年一度的传统节目——年终总结时间。

今年也发生了很多比较大的事件，不论是技术圈还是生活圈：

- 生活上，经历了三年新冠疫情防控后，中国终于转变了政策选择共存。这个转变是如此的迅速，以至于我脑子都有点转不过弯，有一两次进了地铁口还下意识想扫码。
  - 转共存策略后，北京火葬场开始满负荷运转，说明新冠对老人小孩而言还是很危险的，就看谁中彩票...
- 技术上今年最出圈的应该就属于 AI 绘画跟 ChatGPT 了，尤其是 ChatGPT，他给我的感觉是：强人工智能已经不远了。也有技术大佬感慨，这个时刻竟然来临得如此之快，惊喜之余也有点猝不及防。
  - 我的观点是：ChatGPT **完善后**应该能够显著提升各类专业人员的工作效率，会引发新一轮的 AI 创业潮，也很可能会导致行业内许多低端岗位被裁撤。但是目前它的投毒行为（捏造事实）比较严重，不堪大用。

## 生活

- 1 月
  - 购入 Synthesizer V + 青溯 AI 声库，简单调了几首歌试试，效果非常棒。然后就一直放了一年没碰它...还试用了免费的 ACE 虚拟歌姬，合成效果确实很强，跟收费的 Synthesizer V 有的一拼。
  - 在家过春节，给家里二楼装了空调、加湿器跟地垫。但是没买地暖垫，导致开了空调后地上的垫子冰凉。后面补买了地暖垫但是已经要上班了没体验上。
- 2 月跟 3 月
  - 想学下区块链技术，结果发现课程一开始就讲加密哈希函数的基本性质，就决定先搞一波密码学，结果就是输出了一个《写给开发人员的实用密码学》系列文章，内容大部分是翻译的，少部分是我自己补充。
  - 工作上，跟推荐系统大佬一起将服务从 HTTP 切换到 gRPC，效果立竿见影，服务流量下降 50% ~ 60%，延迟下降 30% ~ 50%
- 4 月份
  - 职级晋升通过，从初级 SRE 升到了中级 SRE
  - 使用 [aws/karpenter](https://github.com/aws/karpenter) 实现离线计算集群的弹性扩缩容
  - 读完了 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)，对以太坊有了基本的了解
  - 读了《Go 程序设计语言（英文版）》
- 5 月份
  - 主要是学完了《深入浅出 Kubernetes》这个极客时间专栏
  - 通过《分布式协议与算法实战》等相关资料简单了解了下分布式共识算法的原理，记录了些笔记，8 月份的时候把笔记整理输出为了一篇博客 [分布式系统的一致性问题与共识算法](https://thiscute.world/posts/consistency-and-consensus-algorithm/) 
  - 还读了许多社区的区块链相关资料，包括但不限于 [Web 3.0：穿越十年的讨论 - 知乎](https://www.zhihu.com/special/1452635344142909440)、[《Web3 DApp 最佳编程实践指南》](https://guoyu.mirror.xyz/RD-xkpoxasAU7x5MIJmiCX4gll3Cs0pAd5iM258S1Ek)、[dcbuild3r/blockchain-development-guide](https://github.com/dcbuild3r/blockchain-development-guide)
  - 因为 AI 发展迅猛，来了三分钟兴趣学了一点 [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh)，但是不了了之了。
  - 工作上是研究跨云应用部署方案与跨云 kubernetes 网络方案，如 karmada/kubevela/istio，以及 L4/L7 层的开源/商业网关方案
- 6 月份
  - 读完了《在生命的尽头拥抱你-临终关怀医生手记》
  - 读了一点买的新书：《语言学的邀请》跟《Intimate Relationship》
- 7 月份
  - 工作上主要还是在研究网关优化、Nginx 配置调优。基本确定云上网关及 Kubernetes 集群的网络架构优化的初步方案并开始实施，使用 Go 语言写了一个 Nginx Gateway 控制器
- 8 月
  - 读完了《在峡江的转弯处 - 陈行甲人生笔记》
  - 延续上个月对 Linux 系统的兴趣，快速过了一遍 The ANSI C Programming Language 以熟悉 C 的语法，之后开始阅读 [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)
    - 写了一个小项目 [video2ascii-c](https://github.com/ryan4yin/video2ascii-c) 练手 C 语言。
  - 工作
    - 因为最终还是决定用 APISIX/Nginx，看了一点极客时间《OpenResty 从入门到实战》但是因为兴趣并不强烈，又不了了之了。
    - 另外承接了一个 Data 的数据上报网关的需求，需要在网关层支持一些稍微复杂点的功能确保升级流程的稳定性。跟 APISIX 官方沟通后得到了比较好的解决方案 [custom plugin - set an upstream as a http fallback server](https://github.com/apache/apisix/discussions/7773)
- 9 月
  - 偶然发现手机桌面上有一个安装了好久但是一直没用过的 APP 英语流利说，顺手用它测了下自己的英文水平。然后就对英语感兴趣了，制定了英语学习计划并发布对应的博文 [Learn English Again](https://thiscute.world/posts/learn-english-again/)
- 10 月
- 11 月
- 12 月

## 读书

- 年初辞职后游山玩水，心思稍微安定了些，看了大半本《走出荒野》。
- 6 月份社区组织打新冠疫苗时，在等候室看了本《青春驿站——深圳打工妹写真》，讲述八九十年代打工妹的生活。很真实，感情很细腻。
- 年末二爷爷去世，参加完葬礼后，心态有些变化，看完了大一时买下的《月宫 Moon Palace》，讲述主角的悲剧人生。
- 其余大部分业余时间，无聊，又不想学点东西，也不想运动，于是看了非常多的网络小说打发时间。

## 音乐

年初辞职后，练了一段时间的竹笛跟蓝调口琴，但后来找到工作后就基本沉寂了。

总的来说还是原地踏步吧。

{{< figure src="/images/2021-summary/midi-keyboard-flute-harmonica.webp" >}}

## 工作 - 我在大宇无限的这一年

3 月份刚进大宇的我充满好奇，但也小心谨慎，甚至有点不敢相信自己能进到一家这么棒的公司，感觉自己运气爆棚。
毕竟大宇无论是同事水平还是工作氛围，亦或是用户体量，相比我上家公司都是质的差别。

![](/images/2021-summary/workstation-1.webp "我在大宇的第一个工位")

之后慢慢熟悉工作的内容与方法，leader 尽力把最匹配我兴趣的工作安排给我，帮我排疑解难，同时又给我极大的自主性，真的是棒极了。

然而自主性高带来的也是更高的工作难度，遇到困难时也曾手忙脚乱、迷茫、甚至自我怀疑，很担心是不是隔天就得跑路了...
但好在我终究还是能调节好心态，负起责任，一步步把工作完成。
中间有几次工作有延误时，leader 还陪我加班，事情干完后又带我去吃大餐犒劳自己，真的超级感谢他的帮助与支持。

![](/images/2021-summary/workstation-2.webp "换座位后的新工位，落地窗风景很棒")

这样经历了几个项目的洗礼后，现在我终于能说自己是脚踏实地了，心态从「明天是不是得提桶跑路」转变成了「哇还有这个可以搞，那个 ROI 也很高，有好多有趣的事可以做啊」，我终于能说自己真正融入了大宇无限这家公司，成为了它的一员。

回看下了 2020 年的总结与展望，今年实际的进步，跟去年期望的差别很大。最初的目标大概只实现了 10%，但是接触到了许多意料之外的东西，总体还是满意的：

- 熟悉了新公司的文化与工作方式，这感觉是个很大的收获，我的工作方式有了很大的改善
- 接触并且熟悉了新公司的 AWS 线上环境
  - 负责维护线上 Kubernetes 管理平台，第一次接触到的线上集群峰值 QPS 就有好几万。从一开始的小心翼翼，到现在也转变成了老手，这算是意义重大吧
  - 使用 python 写了几个 Kubernetes 管理平台的服务，这也是我第一次写线上服务，很有些成就感
  - 下半年在 AWS 成本的分析与管控上花了很多精力，也有了一些不错的成果，受益匪浅
  - 学会了 Nginx 的简单使用，刚好够用于维护公司先有的 Nginx 代理配置
- 主导完成了「新建 K8s 集群，将服务迁移到新集群」。虽然并不是一件很难的事，但这应该算是我 2021 年最大的成就了。
  - 升级过程中也是遇到了各种问题，第一次升级迁移时我准备了好久，慌的不行，结果升级时部分服务还是出了问题，当时脑子真的是个懵的，跟 leader 搞到半夜 1 点多后还是没解决，回退到了旧集群，升级失败。之后通过各种测试分析，确认到是某个服务扩缩容震荡导致可用率无法恢复，尝试通过 HPA 的 behavior 来控制扩缩容速率，又意外触发了 K8s HPA 的 bug 把集群控制面搞崩了... 再之后把问题都确认了，第二次尝试升级，又是有个别服务可用率抖动，调试了好几天。那几天神经一直紧绷，每天早上都是被服务可用率的告警吵醒的。跨年的那天晚上业务量上涨，我就在观察服务可用率的过程中跨年了。这样才终于完成了 K8s 集群的升级，期间各位同事也有参与帮忙分析排查各种问题，非常感谢他们，还有努力的我自己。
- 随便写了几个 go 的 demo，基本没啥进步
- 学了一个星期的 rust 语言，快速看完了 the book，用 rust 重写了个 video2chars
- 学习了 Linux 容器的底层原理：cgroups/namespace 技术，并且用 go/rust 实现了个 demo
- 学习了 Linux 的各种网络接口、Iptables
- 熟悉了 PromQL/Grafana，现在也能拷贝些 PromQL 查各种数据了

如果要给自己打分的话，那就是「良好」吧。因为并没有很强的进取心，所以出来的结果也并不能称之为「优秀」。

顺便公司的新办公区真的超赞，详情见我的 twitter：

<blockquote class="twitter-tweet"><p lang="zh" dir="ltr">新办公区真好呐～<br><br>值此良辰美景，好想整个榻榻米坐垫，坐在角落的落地窗边工作🤣<br>那种使用公共设施工（mo）作（yu）的乐趣，以及平常工位见不到的景色交相辉映，是不太好表述的奇妙体验 <a href="https://t.co/FASffzw8N3">pic.twitter.com/FASffzw8N3</a></p>&mdash; ryan4yin | 於清樂 (@ryan4yin) <a href="https://twitter.com/ryan4yin/status/1482891448731070466?ref_src=twsrc%5Etfw">January 17, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 


## 技术方面的感受

- Istio 服务网格：体会到了它有点重，而且它的发展跟我们的需求不一定匹配
  - Sidecar 模式的成本比较高，在未调优的情况下，它会给服务带来 1/3 到 1/4 的成本提升，以及延迟上升
  - 比如切量权重固定为 100（新版本将会放宽限制），不支持 pod 的 warm up（社区已经有 PR，持续观望吧）
  - 而它重点发展的虚拟机支持我们却完全不需要
  - 一直在思考是持续往 Istio 投入，还是换其他的方案
- 服务网格仍然在快速发展，未来的趋势应该是 eBPF + Envoy + WASM
  - Cilium 推出的基于 eBPF 的 Service Mesh 是一个新趋势（它使用高级特性时会退化成 Per Node Proxy 模式），成本、延迟方面都有望吊打 Sidecar 模式的其他服务网格，是今年服务网格领域的大新闻。
  - 我们曾尝试使用中心化网关来替代 Sidecar 以降低成本。但是跨区流量成本、HTTP/gRPC 多协议共存，这些都是挑战。而且这也并不是社区的最佳实践，现在我觉得维持 Sidecar 其实反而能提升资源利用率，我们的集群资源利用率目前很低。如果能把控好，这部分成本或许是可以接受的。
- K8s 集群的日志方面，我们目前是使用自研的基于 gelf 协议的系统，但是问题挺多的
  - 从提升系统的可维护性、易用性等角度来说，loki 是值得探索下的
- K8s 集群管理方面，觉得集群的升级迭代，可以做得更自动化、更可靠。明年可以在多集群管理这个方向上多探索下。
- [Pod 服务质量](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/)：对非核心服务，可以适当调低 requests 的资源量，而不是完全预留(`Guaranteed`)，以提升资源利用率。
- 官方的 HPA 能力是不够用的，业务侧可能会需要基于 QPS/Queue 或者业务侧的其他参数来进行扩缩容
  - 推广基于 [KEDA](https://github.com/kedacore/keda) 的扩缩容能力
  - 关注 [Container resource metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#container-resource-metrics) 的进展
- 成本控制方面，体会到了 ~~ARM 架构~~以及 Spot 竞价实例的好处
  - 2022-02-17 更新：数据库等中间件可以切换到 ARM。EKS 服务目前都是 Spot 实例，它的 ARM 化 ROI 并不高。
- 跨区流量成本有很大的潜在优化空间
  - 跨区流量成本是进出该可用区都会收费，而且不仅涉及 Kubernetes 集群内服务间的调用，还会涉及对 RDS/ES/ElastiCache/EC2 等其他资源的调用。
- 今年各云厂商故障频发，没有**跨 region 的服务迁移**就会很难受，需要持续关注下 [karmada](https://github.com/karmada-io/karmada) 这类多集群管理方案。
  - Google 账号系统宕机
  - Fastly CDN 故障
  - Facebook 故障
  - AWS 更是各种可用区故障，12/7 的故障导致 AWS 大部分服务都崩了。因此我们 SRE 今年经常是救各种大火小火...
- Rust/Go/WASM 蓬勃发展，未来可期。
- AI 落地到各个领域，影响到了我们日常使用的语音导航、歌声合成、语音合成等多个领域，当然也包括与 SRE 工作相关的场景：AIOps

## 2022 年的展望

### 技术侧

今年的展望写得更聚焦一些，争取能实现 50%，就是很大的突破了。

重点仍然是网络技术与 Kubernetes 技术，Redis/Search/Database 等技术还得靠后排，或许明年吧哈哈。

1. 熟练掌握 Go 语言，并分别用于至少两个项目中
   1. 打铁还需自身硬，编码能力是基础中的基础
2. Kubernetes 相关
   1. 以 kubebuilder 为代表的 k8s 开发、拓展技术
   1. 阅读 k8s 及相关生态的源码，了解其实现逻辑
3. 网络技术
   1. 服务网格 Istio
   2. 代理工具 Envoy/APISIX
   3. 网络插件 Cilium + eBPF
4. AWS K8s 成本与服务稳定性优化
   1. 通过拓扑感知的请求转发，节约跨可用区/跨域的流量成本
     1. K8s 新特性：[Topology Aware Hints](https://kubernetes.io/docs/concepts/services-networking/topology-aware-hints/)
     2. Istio: [Locality Load Balancing](https://istio.io/latest/docs/tasks/traffic-management/locality-load-balancing/)
   2. 推广 gRPC 协议
   3. 通过亲和性与反亲和性 + [descheduler](https://github.com/kubernetes-sigs/descheduler)，实现合理调度 Pods 减少跨域流量、也提升服务容灾能力
5. 提升本地开发效率：
   1. [nocalhost](https://github.com/nocalhost/nocalhost)
6. 多集群的应用部署、容灾
      1. karmada
7. 探索新技术与可能性（优先级低）
   1. 基于 Kubernetes 的服务平台，未来的发展方向
      1. kubevela
      2. buildpack
      3. 是否应该推进 gitops
      4. openkruise
   2. Serverless 平台的进展
      1. Knative
      2. OpenFunction
   3. 机器学习、深度学习技术：想尝试下将 AI 应用在音乐、语音、SRE 等我感兴趣的领域，即使是调包也行啊，总之想出点成果...


可以预料到明年 SRE 团队有超多的机会，这其中我具体能负责哪些部分，又能做出怎样的成果，真的相当期待~

### 生活侧

- 运动：
  - 把轮滑练好，学会点花样吧，每个月至少两次。
  - 进行三次以上的次短途旅行，东西冲穿越可以再来一次。
- 音乐：
  - 再一次学习乐理...
  - midi 键盘买了一直吃灰，多多练习吧
  - 买了个 Synthesizer V  Stduio Pro + 「青溯 AI」，新的一年想学下调教，翻唱些自己喜欢的歌。
- 阅读：清单如下，一个月至少读完其中一本。
  - 文学类：
    - [x] 《人间失格》：久仰大名的一本书，曾经有同学力荐，但是一直没看。
    - [ ]《生命最后的读书会》：或许曾经看过，但是一点印象都没了
    - [ ]《百年孤独》：高中的时候读过一遍，但是都忘差不多了
    - [ ]《霍乱时期的爱情》
    - [ ]《苏菲的世界》：据说是哲学启蒙读物，曾经看过，但是对内容完全没印象了。
    - [ ]《你一生的故事》：我也曾是个科幻迷
    - [ ]《沈从文的后半生》
    - [ ]《我与地坛》
    - [ ]《将饮茶》
    - [ ]《吾国与吾民 - 林语堂》
    - [ ]《房思琪的初恋乐园》
  - 人文社科
    - [x]《在生命的尽头拥抱你-临终关怀医生手记》：今年想更多地了解下「死亡」
    - [ ]《怎样征服美丽少女》：哈哈
    - [ ]《爱的艺术》
    - [ ]《社会心理学》
    - [ ]《被讨厌的勇气》
    - [ ]《人体简史》
    - [ ]《科学革命的结构》
    - [ ]《邓小平时代》
    - [ ]《论中国》
    - [ ]《刘擎西方现代思想讲义》
    - [ ]《时间的秩序》
    - [ ]《极简宇宙史》
    - [ ]《圆圈正义-作为自由前提的信念》
    - [ ]《人生脚本》
  - 技术类
    - [ ]《复杂》
    - [ ]《SRE - Google 运维解密》
    - [ ]《凤凰项目：一个 IT 运维的传奇故事》
    - [ ]《人月神话》
    - [ ]《绩效使能：超越 OKR》
    - [ ]《奈飞文化手册》
    - [ ]《幕后产品-打造突破式思维》
    - [ ]《深入 Linux 内核架构》
    - [ ]《Linux/UNIX 系统编程手册》
    - [ ]《重构 - 改善既有代码的设计》
    - [ ]《网络是怎样连接的》：曾经学习过《计算机网络：自顶向下方法》，不过只学到网络层。就从这本书开始重新学习吧。


## 结语

2021 年初朋友与我给自己的期许是「拆破玉笼飞彩凤，顿开金锁走蛟龙」，感觉确实应验了。

今年我希望不论是在生活上还是在工作上，都能「更上一层楼」~


>更多有趣的、有深度的 2021 年度总结：<https://github.com/saveweb/review-2021>

