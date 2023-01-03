---
title: "2022 年年终总结"
date: 2023-01-02T18:00:45+08:00
lastmod: 2023-01-02T18:00:45+08:00

draft: false
resources:
- name: "featured-image"
  src: "github-profile-2022-ryan4yin.webp"

tags: ["总结"]
categories: ["life", "tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

## 闲言碎语


是的又过去一年，又到了一年一度的传统节目——年终总结时间。


## 2022 年流水账

先简单过一下我 2022 年的流水账（有记录一个 `/history`，回顾起来就是方便）：

- 1 月
  - 购入 Synthesizer V + 青溯 AI 声库，简单调了几首歌试试，效果非常棒。然后就一直放了一年没碰它...还试用了免费的 ACE 虚拟歌姬，合成效果确实很强，跟收费的 Synthesizer V 有的一拼。
  - 在家过春节，给家里二楼装了空调、加湿器跟地垫。但是没买地暖垫，导致开了空调后地上的垫子冰凉。后面补买了地暖垫但是已经要上班了没体验上。
- 2 月跟 3 月
  - 想学下区块链技术，结果发现课程一开始就讲加密哈希函数的基本性质，就决定先搞一波密码学，结果就是输出了一个[《写给开发人员的实用密码学》系列文章](https://thiscute.world/posts/practical-cryptography-basics-1/)，内容大部分是翻译的，少部分是我自己补充。
  - 主要工作：跟推荐系统大佬一起将服务从 HTTP 切换到 gRPC，效果立竿见影，服务流量下降 50% ~ 60%，延迟下降 30% ~ 50%。
- 4 月份
  - 读完了 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)，对以太坊有了基本的了解。
  - 读了《Go 程序设计语言（英文版）》
    - ![](/images/now/the-go-programming-language.webp "Go 程序设计语言（英文版） 2022-08-19 补图")
  - 很高兴通过了职级晋升，不再是 SRE 萌新了。
  - 主要工作：使用 [aws/karpenter](https://github.com/aws/karpenter) 实现离线计算集群的弹性扩缩容，省了一波成本。
- 5 月份
  - 主要是学完了《深入浅出 Kubernetes》这个极客时间专栏
  - 通过《分布式协议与算法实战》等相关资料简单了解了下分布式共识算法的原理，记录了些笔记，8 月份的时候把笔记整理输出为了一篇博客 [分布式系统的一致性问题与共识算法](https://thiscute.world/posts/consistency-and-consensus-algorithm/) 
  - 还读了许多社区的区块链相关资料，包括但不限于 [Web 3.0：穿越十年的讨论 - 知乎](https://www.zhihu.com/special/1452635344142909440)、[《Web3 DApp 最佳编程实践指南》](https://guoyu.mirror.xyz/RD-xkpoxasAU7x5MIJmiCX4gll3Cs0pAd5iM258S1Ek)、[dcbuild3r/blockchain-development-guide](https://github.com/dcbuild3r/blockchain-development-guide)
  - 因为 AI 发展迅猛，来了三分钟兴趣学了一点 [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh)，但是进度条走了不到 15% 就不了了之了。
  - 主要工作：研究跨云应用部署方案与跨云 kubernetes 网络方案，如 karmada/kubevela/istio，以及 L4/L7 层的开源/商业网关方案
- 6 月份
  - 读完了《在生命的尽头拥抱你-临终关怀医生手记》
  - 读了一点买的新书：《语言学的邀请》跟《Intimate Relationship》
- 7 月份
  - 主要工作：确定并实施网关架构优化的初步方案，使用 Go 语言写了一个 Nginx Gateway 控制器，迁移流量到新容器化网关省了一波成本。
- 8 月
  - 读完了《在峡江的转弯处 - 陈行甲人生笔记》
    - ![](/images/now/life-notes-of-chenxingjia.webp "陈行甲人生笔记")
  - 延续上个月对 Linux 系统的兴趣，快速过了一遍 The ANSI C Programming Language 以熟悉 C 的语法，之后开始阅读 [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)
    - 写了一个小项目 [video2ascii-c](https://github.com/ryan4yin/video2ascii-c) 练手 C 语言。
    - ![](/images/now/the-asni-c-programming-language.webp "The ANSI C Programming Language")
  - 因为今年搞网关 APISIX/Nginx 接触比较多，看了一点极客时间《OpenResty 从入门到实战》但是因为兴趣并不强烈，又不了了之了。
  - 主要工作：
    - 搞网关优化省了一波成本，但是期间也搞出一个严重故障...
    - 承接了一个数据上报网关的需求，需要在网关层支持一些稍微复杂点的功能确保升级流程的稳定性。跟 APISIX 官方沟通后得到了比较好的解决方案 [custom plugin - set an upstream as a http fallback server](https://github.com/apache/apisix/discussions/7773)
- 9 月
  - 偶然发现手机桌面上有一个安装了好久但是一直没用过的 APP 英语流利说，顺手用它测了下自己的英文水平。然后就对英语感兴趣了，制定了英语学习计划并发布对应的博文 [Learn English Again](https://thiscute.world/posts/learn-english-again/)，然后就开始坚持学英语，感觉整个过程都很顺利。
  - 主要工作：
    - 仍然是搞网关优化省成本，因为各种原因，再次输出一篇 Post Mortem
    - 搞数据上报网关的需求
- 10 月
  - 找了很多英语学习资料，通过每日的坚持学习，渐渐找到了自己的英语学习节奏，完善了学习规划。
  - 《Linux/Unix 系统编程手册（上册）》阅读进度过半，但是业余时间就这么点，同时用来学习 Linux 跟英语实在有点吃力，这本书的阅读就慢慢放下了。
    - ![](/images/now/the-linux-programming-interface.webp "Linux/Unix 系统编程手册（上册）")
  - 通过友链漫游，发现了 [0xFFFF 社区](https://0xffff.one)，内容质量很高，也在社区的 QQ 群里跟群友们聊了些有意思有价值的内容。
  - 打游戏学英语
      ![](/images/learn-english-again/genshin-impact-noelle.webp "超飒的重剑女仆 Noelle")
      ![](/images/learn-english-again/demo2-talk-1.webp "DEEMO 2 中丰富的对话内容")
  - 因为许多原因，中概股大跌，公司架构大调整，走了很多大佬，包括去年带我冲浪的算法部门前辈。
  - 主要工作
    - 搞数据上报网关的需求，一路踩坑，总算把数万 QPS 的流量全部迁移到新网关上了。
- 11 月
  - 重新对搞 Homelab 产生了兴趣，买了三台 MINI 主机组了一个 Homelab，时隔一年多又开始折腾 Proxmox VE，做各种规划。
  - 迭代了很多次后的个人 Homelab 文档：[ryan4yin/knowledge/homelab](https://github.com/ryan4yin/knowledge/tree/master/homelab)
    - ![](/images/now/dashy-homepage.webp "我的 Homelab 导航页 2022-11-12")
  - 因为业余时间沉迷搞 Homelab，英语打卡就变得断断续续了...但是词汇量测试的效果出乎意料，进步速度喜人，阅读能力也能感觉到有明显提升。
  - 月底搬家换了个新租房，床是挂天花板上的，房间就宽敞了很多，而且拉了独立的电信宽带，网速杠杠的。
  - 主要工作：继续推进线上网关优化项目，以及调研 K8s / Istio 的新版本变化，为集群升级做预备工作。
- 12 月
  - 从 Homelab 折腾到 HomeAssistant/ESPHome，然后就折腾 ESP32/ESP8266，结果很意外地就买了一堆硬件，入手了电烙铁热风枪万用表等各种仪器，ESP/51/STM32 都玩了个遍...
    - 输出内容有两个代码仓库：[learn-8051-asm](https://github.com/ryan4yin/learn-8051-asm) 与 [learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)，以及一份 EE 笔记：[Electrical Engineering.md](https://github.com/ryan4yin/knowledge/blob/master/electrical-engineering/Electrical%20Engineering.md)
      {{<figure src="/images/now/experience-of-electrical-engineering.webp" title="我的电子电路初体验" width="60%">}}
      {{<figure src="/images/now/zy-kt-104-front.webp" title="焊好的可调稳压电源 - 正面" width="60%">}}
  - ChatGPT 横空出世，引发全网热潮。有技术大佬感慨，这个时刻竟然来临得如此之快，惊喜之余也有点猝不及防。我也把玩了一波，也用它帮助我学了许多硬件相关的东西，很有帮助。
    - 个人猜测未来 ChatGPT 成熟后大概率能极大提升技术人员的工作效率，很可能间接影响到许多人的工作。
  - 年底还入手了一台 3D 打印机 ELEGOO Neptune 3 Pro...
  - 全国逐渐放开疫情管控，我得了新冠，然后康复...
  - 这个月折腾硬件，英语漏打卡更严重了，但是词汇量仍然在稳步增长，阅读起来也是越来越顺畅。
  - 主要工作：
    - 线上网关优化项目基本落地，取得了预期收益，但是没达到之前设的激进目标。（旧网关仍留存极少部分流量，还需要时间去统一网关架构）
    - 做 K8s 集群升级准备，然后月底公司大面积新冠，拖慢了这项工作的进度，即使后调了升级时间，仍然感觉有点虚...
- 最后是连续三年蝉联我年度歌手的天依同学，截图放这里纪念一下：
  {{<figure src="/images/now/netease-cloud-music-2022-singer-of-ryan4yin.webp" title="我的网易云年度歌手" width="50%">}}


## 2022 年 Highlight

### 1. 英语

英语也是我今年比较惊喜的一个部分，很长一段时间内，我都觉得英语的优先级并不高，一直没有把它的学习排上日程，水平也一直没啥显著提升。

但是从今年 9 月份开始到现在这四个月的英语学习中，我的进步相当明显，从去年大概  4700 词，到现在测试结果为 6583 词，涨了近 2000 词，月均接近 500 词（按这个速度，2023 年 10000 词的目标好像没啥难度了）。

词汇量测试结果按时间排序如下，使用的测试工具是 [Test Your Vocabulary](https://preply.com/en/learn/english/test-your-vocab) ：

{{<figure src="/images/now/2023-01-02-test-your-vocabulary-result.webp" title="2023-01-02 词汇量测试结果：6583 词" width="70%">}}
{{<figure src="/images/now/2022-12-19-test-your-vocabulary-result.webp" title="2022-12-19 词汇量测试结果：6300 词" width="40%">}}
{{<figure src="/images/learn-english-again/2022-11-17-test-your-vocabulary-result.webp" title="2022-11-17 词汇量测试结果：5600 词" width="65%">}}
{{<figure src="/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp" title="2022-10-18 词汇量测试结果：5100 词" width="40%">}}


另外因为主要是靠读书来学英语，今年的英文阅读能力也有明显提升，跟 9 月份刚开始读的时候比，阅读体验要流畅多了。
一些英文原版书阅读成就：

{{<figure src="/images/now/mintreading-first-100days-achivement.webp" title="在薄荷阅读上读完的第一本英语原版书" width="35%">}}

而口语、写作这些今年基本没练习，原地踏步。

### 2. 业余技术

今年业余搞的技术，感觉这些都是我比较满意的：

- Web3: 今年上半年花了不少时间去了解 Web3，但是仍然没敢说自己已经懂了它。水比较深，浅尝辄止。
- 电子电路（硬件）：点亮这个技能完全是个意外...但也挺惊喜的，毕竟我大学学的建筑声学，以前都没接触过硬件。
- Go 语言：去年底定的目标是将 Go 语言应用在至少两个项目上，实际上只用在了一个项目上，完成度 50% 吧。
- Linux: Linux 今年主要是复习了一遍 C 语言，然后看了半本《Linux/Unix 系统编程手册（上册）》，之后因为学英语就给放下了。
  - 毕竟英语的成果很不错，这个结果我觉得也是预期内的。
- 博客：今年博客经营得尚可，数了下有 18 篇技术干货，四篇非技术文章。最主要是三月份翻译密码学的文章冲了一波内容量。虽然 12 月份又鸽掉了...总体还是满意的。

### 3. 工作

SRE 组今年工作的主旋律其实就是省钱，我今年的工作上有更多的挑战，不过因为得心应手很多，反倒没什么想特别着墨描述的了。

### 4. 阅读

2022 年一共读完了这些书：

- [x] 《人间失格》
- [x] 《月宫》
- [x] 《[Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)》
- [x] 《[Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)》
- [x] 《Go 程序设计语言（英文版）》
- [x] 《深入浅出 Kubernetes - 张磊》
- [x] 《在生命的尽头拥抱你-临终关怀医生手记》
- [x] 《在峡江的转弯处 - 陈行甲人生笔记》
- [x] 《The ANSI C Programming Language》
- [x] The Time Machine
- [x] Learn Robotics With Raspberry Pi
  - 学习使用树莓派控制智能小车，结合本书与网上资料，我制作了一台使用 Xbox One 手柄遥控的四驱小车，相当有意思~
- [x] Learn Robotics Programming, 2nd Edition
  - 跟前面那本一样是讲树莓派小车的，不过这本书更深入，代码含量高很多。
  - 快速翻了一遍，跳过了其中大部分代码，因为书中的小车不太符合我的需求。
- [x] The Unlikely Pilgrimage of Harold Fry
- [x] 51 单片机自学笔记

看起来，去年定的一个月至少读一本书的目标，还是达成了滴~

## 2023 年的展望


### 技术侧

2022 年的结果跟年初的展望区别仍然是挺大的，但是我个人挺满意。

这里再记一下 2023 年技术上的展望，看看今年能实现多少，又会点出多少意料之外的技能吧哈哈：

- 云原生
  - 去年定的阅读 k8s 及相关生态的源码没任何进度，2023 年继续...
- Linux
  - 2023 年把《Linux/Unix 系统编程手册》这套书看完，并且借着对硬件的兴趣学一学 Linux 驱动开发。
  - 学习学习时下超流行的 eBPF 技术
- 3D 打印
  - 2022 年底买了台打印机，那不必须得打印点自己设计的东西？
  - FreeCAD 学！Blender 可能跟 3D 打印没啥关系但是也要学！
- 编程语言
  - 今年 Go/C 两个语言的技能点感觉是点出来了，2023 年需要巩固下，用它们完成些更复杂的任务。
  - 另外借着搞硬件的兴趣，把 Rust/C++ 两门语言也玩一玩
    - C++ 主要是用来玩 ESP32/ESP8266，rust 那可是时下最潮的系统级语言，2022 年虽然用 rust 写了点 demo 但离熟练还差很远。
- 其他
  - 2022 年我给开源社区提交的代码贡献几乎没有，希望 2023 年能至少给三个开源项目提交一些代码贡献，这也是检验自己的代码水平。


### 生活侧

2022 年初我写的生活上的展望，貌似只有「阅读」这一项达标了...
不过今年也仍旧记录下 2023 年的展望：

- 2022 年因为疫情以及自己懒，参与的户外活动相当少，2023 年希望能更多的做些户外运动，身体还是很重要的啊。
- 把轮滑水平练上去一点，轮滑鞋在 2022 年吃灰了几乎一整年...
- 音乐上，口琴、竹笛、midi 键盘、Synthesizer V / ACE Studio / Reaper，总要把其中一个练一练吧...（什么？学吉他？？不敢开新坑了，旧坑都还没填完呢...）
- 阅读：仍然跟去年保持一样的节奏就好，目标是一个月至少阅读一本书。
- 英语：英语的规划在 [Learn English Again](https://thiscute.world/posts/learn-english-again/) 中已经做得比较详尽了，这里仅摘抄下目标。
  - 2023 年达到 CEFR 的 C1 等级，报考并取得 BEC 高级证书
  - 2023 年底词汇量超过 10000

## 结语

2021 年的年终总结文末，我给自己 2022 年的期许是「更上一层楼」，感觉确实应验了。

那么 2023 年，我希望自己能够「认识更多有趣的人，见识下更宽广的世界」~

>更多有趣的的 2022 年度总结：<https://github.com/saveweb/review-2022>
