---
title: "曾经的我 - 2024"
date: 2024-01-01T14:14:35+08:00
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

> Twitter 上 @Manjusaka_Lee 等大佬喜欢写周报，不过我不太喜欢周报的形式。因为周报的标题本身
> 没啥意义，而要看其中的内容却得一个个点进去看，这对我自己回顾过往的学习、工作、生活，体验
> 非常不方便。我比较喜欢类似「一镜到底」的阅读体验，所以我采用这种单页的方式来记录我的日
> 常。（基于同样的理由，我将博客单页展示的文章数量上限调整成了 `1000`）

全部历史记录：[/history](/history/)

### 2023-03-23 - 2023-03-24

- 尝试在 Orange Pi 5 上运行基于 eBPF 的某代理程序，遇到了许多问题
  - 首先遇到的是，不存在 ksm 内核模块，因为这是一个基于 armbian/rockchip 的定制内核，它默
    认关掉了许多内核模块。需要修改内核参数生成新的 .config 文件，然后重新编译内核。
  - 恰好前两天有人给我的 [nixos-rk3588](https://github.com/ryan4yin/nixos-rk3588) 提 issue
    说他将内核升级到了 6.1，发现在 UEFI 下无法启动。就决定直接在 6.1 的内核上添加一些缺失
    的模块，新内核用着也更爽一点 emmmm 弄了挺久的，最终发现 EDK2 不支持 6.1 内核的 dtbs 设
    备树，通过一些手段可以解决。此外内核模块列表也做了许多调整。
  - 东西都解决后，为了隔离环境，我一开始尝试使用 microvm.nix 来运行此 ebpf 程序，遇到了
    agenix 在 microvm.nix 中出莫名其妙的问题，原因大概率是 bash 脚本太脆弱了，microvm 的环
    境可能有些不同。弄得有点心累，暂时放弃迁移了...
  - 我虚拟机里跑的代理也出了点问题，不过好在有每日自动备份，restore 了一个旧版本，问题解
    决。虚拟机的快照功能真香啊。
- 给 nix-config 加了些新测试，发现并修复了一些之前没发现的 bug，同时也避免未来再出现同类问
  题。
- 最近各种想法很多，nix-config 仓库经常建了很多分支，然后功能还没弄好，又有了新的点子，结
  果就是多分支开发，互相冲突... 目前的解决方法就是，在发觉难以管理的时候，先把一些未完成的
  分支 merge 掉，降低维护成本，后面想推进它们了再提新的 PR 完善这些 WIP 的功能。
  - 这里的问题是，我各种想法不是按一定顺序出现的，经常是在做 A 的过程中遇到了些问题，然后
    想到了一个解决方案 B，B 跟 A 可能并无关联，但我又想尽快验证 B 的可行性（想法不抓住，后
    面可能就再也想不起来了），于是就开了个分支去验证 B. 这样就导致了分支越来越多，互相之间
    冲突的概率就越来越大，越来越难维护。到了某个时间点，我就会一次性把旧的分支全 merge
    掉，降低维护成本...

### 2023-03-19 - 2023-03-21

- 持续迭代使用 NixOS + KubeVirt + FLux2 取代 Proxmox VE 的方案，方案基本调通了，时间主要用
  在了解决这些问题上：
  - K8s 集群中部署的 Controller/Operator 删除非常麻烦，它们会创建各种 CRs 并添加
    finalizer，一旦删除顺序不对就会导致 CR 无法删除，这个问题在 Pulumi 时就遇到过，当时以
    为 Flux2 可能自动能解决这个。但现在看是 K8s 自身的问题，必须通过手动在 Pulumi/Flux2 等
    工具中声明好依赖关系，才能保证删除顺序正确。另外 victoria-metircs 等个别 operator，即
    使删除顺序是正确的，也会因为它设置的许多保护策略导致无法删除，必须手动一个个确认并删除
    （繁琐，但我能理解这么做的目的，确保不丢数据）。
  - KubeVirt 的 Multus-CNI 插件在 k3s 上无法正常工作，各种报错导致 Pod 都无法删除了（删除
    也要调用 CNI 插件，但插件不工作），因为这个问题，以及上面提到的集群数据删除很麻烦的问
    题，我在测试 KubeVirt 的时候借助 Proxmox 的虚拟机快照重置了好多次集群状态。
  - Flux2 的同步速度比较慢，每次改完配置再跑 `flux reconcile` 但是要等好久才能同步完成，这
    也严重拖慢了我的迭代速度。但为了保证集群环境的可复现性，又没有太好的办法。好在配置调好
    后，内容基本不会有大的变动，所以这个问题也不是很大。
  - longhorn 的分布式存储倒是部署上就能用，UI 面板也挺友好，出问题能给出关键信息，好评。
- 为 [nixos-cn.github.io](https://github.com/NixOS-CN/nixos-cn.github.io) 提了几个 PR 补充
  内容，同时对完善该文档产生了兴趣，提了个
  [Issue 18](https://github.com/NixOS-CN/nixos-cn.github.io/issues/18) 寻求项目 Owner 的意
  见。

当前的 Homelab 改造进展：

- All in NixOS，做到 99% 的声明式配置
- 监控系统迁移到 NixOS（Prometheus + Alertmanager + Grafana + Uptime-Kuma） - 100%
- 网络设备迁移到 NixOS（dae 旁路网关 + tailscale 网关） - 100%
- K8s 集群迁移到 NixOS - 100%
- 将 Homelab 监控、Git 仓库、旁路网关都迁移到一块 Orange Pi 5 上，并启用 LUKS 加密 - 100%
- 这是 KubeVirt 改造的前置工作，这三项服务都需要最高的稳定性，也被 kubevirt 依赖，因此需要
  放在 kubevirt 集群之外
- K8s 集群使用 Flux2 进行 GitOps 式自动配置 - 100%
- 两块 RK3588 板子启用 UEFI + NixOS + LUKS - 100%
- 使用 kubevirt 全面替换 Proxmox VE 集群，并启用 LUKS 加密 + Secure Boot - 50%
- 方案已经在 PVE 里的一个 k3s 集群上通过验证，接下来是替换工作。
- 基于 restic 与 rclone 做 Homelab 数据加密备份与版本控制 - 0%
- 监控节点(hostname=ruby)性能给得够高，将其同时用做 homelab 的控制节点，方便我在 macOS 上
  进行 homelab 的管理与更新 - 100%

### 2023-03-18

- 折腾这个[域名被加入到黑名单](https://twitter.com/ryan4yin/status/1769602470282744022)的
  问题，一整天心思一直被它拉住，活都没干好...

### 2024-03-16

- 又对 NixOS & Flakes Book 做了大量更新，主要是各种小问题的修复。
  - NixOS 群友建议使用 pre-commit-hooks 自动调用一些 spellchecker/markdown-formatter 等工
    具，试了下帮我解决了大量的格式问题与拼写错误，非常好用！已经把这个也抄到了我其他项目
    中。
- 拿到了护照跟港澳通行证，要开始摇人一起去香港新加坡玩了～

### 2024-03-14

- 参加 2024 玄铁 RISC-V 生态大会，第一次亲眼见到中国科学院院士做报告，挺开心的。一整天听下
  来，对如下几个报告的印象比较深刻：
  - 倪光南院士对 RISC-V 的开篇介绍，大概芯片工艺与指令集架构的发展历程，并引出了 RISC-V 的
    优势：开源开放、模块化、Chiplink 技术。
  - 包云岗（一生一芯项目以及香山开源 IP 发起者）阐述了 RISC-V 技术变革的定位以及它未来可能
    的几种商业模式。
  - 郭松柳（中科院计算所）介绍了他们在 RISC-V 软件生态上的工作，包括支持 RISC-V 的操作系
    统、周边软件生态支持等等。
- 另外因为也约到了 0xFFFF 的朋友一起去，他又叫上了深大电信协会里对 RISC-V 感兴趣的几位同
  学，在听完报告后，我们也聊了很多关于 RISC-V、X64、ARM、MIPS、LoongArch 等架构的话题，感
  觉很有意思。
  - 我是业余玩家，对指令集的了解不多，底层的指令细节主要是在听他们聊，感觉还是很有意思的，
    也学到了不少东西，对 RISC-V 起了更多的兴趣。
- 会议结束后，我跟朋友又在展厅完了很久 openKylin 展出的 LicheePi 4A 跟 Milk-V Pioneer，测
  了 Chromium 的渲染性能、ffmpeg 的编解码性能之类的，也拍了 64 核的 htop 监控图，超好玩！
- 之后又跟他们去了深圳大学丽湖校区吃了学校的晚饭，学校很漂亮、饭也很便宜很香。完了又在学校
  里逛了得有一个多小时，拍了很多照片，体验了小半天校园生活，梦回大学时代哈哈。
  - 深大真的很有钱，学校里的设施都很好，校园环境也很漂亮，又很大，这次游玩的体验很好。

### 2024-03-11 - 2024-03-13

- 偶然在 NixOS 中文群聊天，guangtao 老师提出可以用 overlays 来解决 darwin 的 broken
  packages 问题，非常好
  用：[Refactor: Remove darwin packages](https://github.com/ryan4yin/nix-config/pull/84/files#diff-3c2d7691414cb91e9476b1dc1302f1375e6daa96259b31789a9308a97f75ef69)
- 继续研究 ArgoCD 跟 Flux2，发现 ArgoCD 的文档很乱，HA 的架构也比较复杂。Flux2 的文档相对
  清晰许多，而且架构简单，使用方便，所以决定在公司的几个项目跟我个人 Homelab 上都使用
  Flux2 来管理 K8s 集群。
- Nix 配置少量重构，添加 Eval Tests 跟 NixOS Tests，并且修了一堆之前重构导致的 Bug，之前因
  为没有测试，有些 bug 现在加了测试才发现。

### 2024-03-09 - 2024-03-10

- 发现我当前的 Nix 配置已经比较复杂了，而且不太能支撑我想要的一些功能，于是决定重构。
  - 首先提了个 issue 记录了下改造目
    标：[(Feature) Refactor the code to make it more maintainable and readable](https://github.com/ryan4yin/nix-config/issues/83)
  - 完成并合并了第一个 PR
    [refactor: flake outputs & hosts](https://github.com/ryan4yin/nix-config/pull/79)，解
    决了当前最大的痛点。
- 几个社区项目都多了挺多 Issue，不过在搞配置重构，没怎么管它们。
- nixos-rk3588 有人提问新版本默认不能交叉编译了，沟通后给加了个 PR
  [feat: add fully cross compilation](https://github.com/ryan4yin/nixos-rk3588/pull/21)

### 2024-03-08

- 更新 NixOS & Flakes Book 的部分内容，许可证从 MIT 替换成了更适合文档的 CC-BY-SA 4.0。
- 搞定了 NixOS RK3588 + UEFI + tmpfs + LUKS，上到了我的两块 Orange Pi 5 / Plus 板子上。
- 之前尝试在 Homelab 上使用 Pulumi，但遇到比较多的问题，放弃了。跟 @Kev @Viz 聊过后，在他
  们的推荐下，转而开始研究 ArgoCD 跟 FLux2 两个 K8s GitOps 工具，打算上线到 Homelab。

### 2024-03-06 - 2024-03-07

- [ryan4yin/nixos-rk3588/pull/19](https://github.com/ryan4yin/nixos-rk3588/pull/19): 搞定
  了 ISO 镜像在 UEFI + NixOS 模式下启动失败的问题，解法是直接生成 Raw Image 而不是 iso 镜
  像。
- [ryan4yin/nix-config/pull/74](https://github.com/ryan4yin/nix-config/pull/74): 尝试在
  RK3588 上添使用 NixOS + LUKS + Secure Boot 启动。
- 报名参加了 3/14 的 2024 玄铁 RISC-V 生态大会，因为是周四工作日，还提前请了假。Pi Day 玩
  玩 RISC-V，感觉很有意思。
  - 呼朋引伴，拉到了 0xffff.one 社区与其他对 RISC-V 感兴趣的朋友一起去。
- 这两天搞 ARM 板子，对继续更新 nixos-rk3588 跟 nixos-licheepi4a 又起了兴趣，打算把它们搞
  得更完善一些，对已有的 Issues 做了些整理，也跟几位 issue owners 做了些沟通。

### 2024-03-01 - 2024-03-05

- 认识了 dae 社区的新朋友，聊 NixOS 跟 CloudNative 等话题，聊得火热。
- 探索 NixOS + K3s + KubeVirt 这套虚拟化方案，遇到一些难点：
  - 虚拟机需要使用 underlay 网络，接入到宿主机的网桥上。但直接桥接好像说会导致无法热迁移，
    这个研究了很多。
  - 为虚拟机分配静态 IP 地址，毕竟 K8s 默认使用动态 IP.
  - 分布式存储方案，因为虚拟机数据是在 PVC 里的，如果不使用分布式存储，那么机器就无法迁移
    到其他节点上了（文档只说了热迁移要求这个，但我感觉非热迁移显然也会有问题吧）。
- 一开始尝试使用 pulumi 来声明式地配置整个 KubeVirt 集群，测试代码
  [ryan4yin/nix-config/pull/71](https://github.com/ryan4yin/nix-config/pull/71/files)，但
  发现用 pulumi 管集群确实不太爽快，尤其是它对依赖关系的处理很不好。destroy 时它先把我
  operator 的 pods 给删掉了，但后面删除 CR 时又得由 operator/controller 完成 finalizer 操
  作，结果就是删除无法成功...
  - 跟 Kev/Viz 两位朋友聊了后，决定换成 flux2/argocd 来以 GitOps 的方式管理整个集群，貌似
    它们有些黑科技能自动识别到这些依赖关系，总之不会出现先删掉我 operator/controller 导致
    CR 无法清理的问题。
- 如果使用 KubeVirt，可 KubeVirt 一是它比较复杂也没那么成熟，肯定没 PVE 那么稳定，二是它需
  要拉取镜像，这最好是过一下我软路由。所以软路由、Git 仓库、Homelab 监控等组件，就得单独部
  署，不能跑在 KubeVirt 里面（我依赖我自己这种架构，出了问题没法修）。
- 所以就决定把软路由(dae)、Git 仓库、Homelab 监控等组件单独部署到一块 ARM 开发板上，但安全
  起见也要设置 LUKS 加密。接着就开始折腾我的 Orange Pi 5 跟 Orange Pi 5 Plus 两块板子。
  - 以前使用的直接 dd 的方式不兼容 LUKS 加密，而且我之前做的镜像也无法在 Orange Pi 5 Plus
    上从 SSD 启动，于是又研究了一晚上的 EDK2-RK3588，想看看用 UEFI 的方式能否解决此问题，
    结果是能进 Grub，但接着 NixOS 怎么启动都是一直报错。

### 2024-02-29

- 朋友聊到 BTC 大涨，看了下币安发现我的加密货币也涨挺多，SOL 更离谱，涨了十多倍。
- 顺便就聊到了什么把加密货币变现的问题，需要借助香港银行账户、护照这两个东西，又考虑到今年
  本来就打算旅游，直接申请了下周一去办护照跟港澳通行证。
- 后面再看看我妹的护照跟港澳通行证要怎么办，需要哪些材料。这样后面她过来就可以一起去香港跟
  国外玩了。

### 2024-02-26 - 2024-02-27

- 早睡早起，晨练。尝试了下早起打光剑，仍旧会导致呕吐...看来早上锻炼前不吃点东西是不行的。
- 发现通过 `ssh -A xxx` 将桌面电脑的 ssh-agent 临时提供给控制节点 ruby 使用，可以免去在服
  务器上保存私钥带来的安全隐患

### 2024-02-24 ~ 2024-02-25

- 看《葬送的芙莉莲》
- 尝试将一台 PVE 节点替换成 LUKS 加密 + BTRFS 文件系统，大败北
  - 首先发现 PVE 的安装程序不支持 LUKS 加密，必须首先安装 Debian，然后再安装 PVE 来实现。
    或者先安装好 PVE，然后再手动加密整个磁盘。
  - 尝试使用 disko 自动分区、LUKS 加密、挂载 BTRFS，用得非常舒服，比手动跑一堆命令要方便太
    多了。
  - 使用 debootstrap 安装 Debian，也遇到一些问题，在花了许多时间后都解决了。
  - 最后安装 PVE 时，发现它对文件系统的分区以及文件系统都有些要求，太脆弱了，遇到各种报
    错，最后放弃了。
- PVE 没搞定，而且也不太喜欢这种不可复现的系统，刚好最近看到说 kubevirt 发布 1.0 了，打算
  直接上 NixOS + K3s + kubevirt 来搞虚拟化。正在研究中。

### 2024-02-21 - 2024-02-23

- 写了
  [OS as Code - 我的 NixOS 使用体会](https://thiscute.world/posts/my-experience-of-nixos/)，
  然后优化这篇文章...

### 2024-02-20

- 工作上梳理了下 Q1 要干的活，目标是啥，有哪些痛点难点，以及在这些痛点难点上有哪些可以做的
  事情，这样得出了一个初步的工作计划，然后开始正式推进 Q1 工作。
- 业余技术上也没写啥东西，同样是做了些梳理与规划，更新了些相关文档。

### 2024-03-18 - 2024-02-19

- 春節正式結束，開始了新的一年的工作，不過還沒咋進入工作狀態。
- 搞了下 Homelab，將之前弄的三臺 NixOS 主機分別擔任監控、應用、路由器三個角色：
  - 使用 NixOS 部署了 Prometheus + Node-Exporters 監控系統，一些好用的 Grafana
    Dashboards，用 caddy 做反向代理。
  - 負責應用的 NixOS 主機上部署了許多應用，如 Homelab, SFTPGO， Uptime-Kuma 等。
- 加了一個 6 節點的 k3s 集羣，並嘗試使用 pulumi 來聲明式 + GitOps 地管理整個集羣配置，但還
  沒搞定。

### 2024-02-16 - 2024-02-17

- 弄了一天的 NixOS Router 跟 dae 配置，完成了这个 PR
  [ryan4yin/nix-config/pull/60](https://github.com/ryan4yin/nix-config/pull/60)，并且删掉
  了之前的 OpenWRT 虚拟机，离 All in NixOS 又近了一步。

### 2024-02-14 - 2024-02-15

- 回深圳，路上没事干，写了一天的 NixOS 文档，完成了这个 PR
  [ryan4yin/nixos-and-flakes-book/pull/86](https://github.com/ryan4yin/nixos-and-flakes-book/pull/86)

### 2024-02-10

- 大年初一，拜年，吃饭。
- 考虑到今年打算国际旅行，研究了下护照、签证、目的地选择等相关事宜。
  - 港澳通行证应该挺好办，找个时间先弄了，出个大陆。
  - 热门目的地（目前这几个都爆火，人太多了，而且贵，感觉 5 月份之前都不太适合？）：香港、
    新加破（免签）、日本、泰国、马来西亚。
  - 日本签证的话，查了下我应该能申请到三年多次旅游签证（年收入超 20 万），价格七八百的样
    子。
  - 非深户在深圳办理出国护照指南
  - 我妹可能只能在湖南省办理护照，这个也得研究下

### 2024-02-07

- 帮我妹弄了个 Copilot，她对弄个人网站感兴趣，又把前年国庆给她弄的 Hugo 站点捡回来搞了下。
- 在 NixOS 中文群水群，跟群友聊了 Nix/NixOS 当前文档上的一些问题：
  - nix.dev 的 sidebar index 很散乱，完全没搞明白自己的定位。尤其是里面 NixOS 这一块塞了一
    堆杂七杂八的东西，搞得又好像个 wiki，根本不适合新手学习。
  - nix.dev 的定位是 Nix 教程，从涵盖入门到深入学习的各种内容。但它现在的结构不太匹配这个
    定位。另一方面这也是说，官方目前根本没有 NixOS 的新手教程。
  - Nixpkgs/NixOS 的文档没有分页，对 SEO 跟阅读都很不友好。
- 另外也聊到了 nix flake lock --update-input 这个命令已经被废弃了，现在推荐用 nix flake
  update xxx 来更新 flake 的依赖。

### 2024-02-05

- [@碎冰冰](https://xuezhao.space/)发消息说搞定了他的博客，我一看第一篇文章就说减掉 45Kg，
  懵了，差点以为单位错了...太猛了，我宣布以后碎冰冰就是我偶像了😍
- 坐高铁顺利到家~ 开始在家摸鱼的生活了。

### 2024-02-03 - 2024-02-04

- 从头开始重新学 [Dive into Deep Learning](https://d2l.ai/)
  - 前面数学基础知识花了挺多时间，然后看神经网络时，还是有很多知识点的 gap，跟我很久以前尝
    试学 AI 的感觉一样。不过以前因为没看到过实际惊艳的效果，缺乏坚持的动力，这次应该能克
    服。
  - 从实操代码开始，英文版跟中文版就出现了比较大的区别，主要是英文版完全改成用 Class 的方
    式来组织代码了，而且 PyTorch 变成了默认框架。所以从线性神经网络这一节开始，以英文版为
    主要学习材料。

### 2024-02-01

- 公司年会，今年的年会公司意料之外的壕气，每人发一台 iPhone 15. 老板还说本来想订 140 台遥
  遥领先，但余承东说他没货，只能换 iPhone 15 了，真壕哪。
  - 然后年会的抽奖奖品也比前两年提升了一个档次，记得前年最高的奖是瓶茅台，还是某位 Owner
    私人捐赠的。今年这种级别的奖品好多件。
  - 再然后就是也少了一些随机选人上台回答问题或者做游戏的尴尬环节，我这种小透明可以更放松地
    享受年会。
- 发的 iPhone 15 当晚拆开自用了，打算跟 Android 换着用，体验下两种不同的硬件跟生态。

### 2024-01-29 - 2024-01-31

- 发了两篇博客
  - [NixOS 在 Lichee Pi 4A 上是如何启动的](https://thiscute.world/posts/how-nixos-start-on-licheepi4a/)
  - [个人数据安全不完全指南](https://thiscute.world/posts/an-incomplete-guide-to-data-security/)
- 对深入学习 NixOS 产生了兴趣，读了些
  [the Nix community RFCs](https://github.com/NixOS/rfcs/)、[Nixpkgs PR](https://github.com/NixOS/nixpkgs/pulls?q=is%3Apr+is%3Aopen+sort%3Acomments-desc)
  等相关资料。
  - [RFC062 - content-addressed-paths](https://github.com/NixOS/rfcs/blob/master/rfcs/0062-content-addressed-paths.md)
    - 受到许多 Nix 用户关注的一个实验特性。它从包的 output 计算其 Output path 与对应的
      Hash 值，固定的 Output 总是输出到固定的地址。
    - 这一是能减少许多重复的构建（许多包可能因其 Input 不同而被重复构建，浪费资源），二是
      可以替代掉旧的基于 public key 的缓存信任模型（拉下来的缓存只要地址跟源码能匹配，那就
      肯定没有被篡改
      过）。[Content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
      是一个在存储领域被广泛用于数据可信校验与数据去重，比如你在 QQ 里上传一份，有时候发现
      它几个 G 的数据一两秒就上传成功了，这实际根本没上传数据，只是对比了下文件 Hash 发现
      QQ 线上已经有这个文件了。
    - 该特性最大的改变是，以前 Nix 是从 Derivation 的 inputs 计算其 output 路径，包定义也
      只锁定了 src 源数据 的 Hash 值。因此在执行构建之前，一个 derivation 的 output 路径就
      已经被确定了。而 CAS 这个特性则必须通过构建结果来计算其 output 路径，因此 output
      path 必须在构建完毕后才能给出。
    - 这其中可能存在的问题是，有些包的构建结果并不是确定性的，比如你构建两次 glibc，可能会
      因为时间或其他随机因素而产生不同的结果。
  - [Nixpkgs Maintainers 说明](https://github.com/NixOS/nixpkgs/blob/master/maintainers/README.md):
    虽然目前我也没维护啥包，但确实有些兴趣参与一下，读了下要求。
  - [ Nix RFC 指导委员会的会议纪要](https://github.com/NixOS/rfc-steering-committee/issues?q=):
    讨论各种社区提出的各种 RFC
  - [RFC146 - 使用类似 tag 的方式对 packages 做分类](https://github.com/NixOS/rfcs/pull/146):
    Nixpkgs 确实一直缺少一个好的分类方式，在基于文件夹的分类方式已经被
    [[RFC 0140] Simple Package Paths](https://github.com/NixOS/rfcs/pull/140) 取代的背景下
    提出这个特性，我觉得是个非常好的想法，希望它尽快落地！
  - [RFC134](https://github.com/NixOS/nix/issues/7868): 跟项目复杂性，可拓展性有关的 PR，
    看着是个很不错的想法，正在落地中。
  - [CLI stabilization effort](https://github.com/NixOS/nix/issues/7701): 我已经跟进这个
    Issue 有一段时间了，目前看年底大家都放假，没啥新进展。
  - [[RFC 0165] Bootspec v2](https://github.com/NixOS/rfcs/pull/165): 强化对嵌入式相关的设
    备树的支持，加强 initrd secrets 的安全性等，挺不错的
  - [[RFC 0166] 官方的 Nix 代码格式化风格](https://github.com/NixOS/rfcs/pull/166): 有一说
    一，Nix 的代码格式化确实很混乱，是个好 RFC，希望尽快落地...
  - [Official NixOS Wiki](https://discourse.nixos.org/t/official-nixos-wiki/38715): 这个是
    前一阵看到的，NixOS 终于又要搞官方 Wiki 了，泪目。
- 查了下 NixOS 的 Google Trending 与 Nixpkgs 的 Contributors 趋势，发现
  - @NickCao @Figsoda @bobby285271 等几位国内的活跃贡献者几乎都是从 2021 年开始参与贡献
    的，Top N 的 @SuperSandro2000 @fabaff 等好几位也是这个时间段。
  - 2021 年 Nix 最大的变化，应该就是
    [Nix 2.4](https://nixos.org/manual/nix/stable/release-notes/rl-2.4) 引入了
    `--experimental-features` 这个 flag，并发布了 Flakes、The New Nix CLI 以及
    content-addressed path 三个实验性特性。Flakes 大大加强了 NixOS 的可复现能力，大概因此
    而吸引了一大批用户的关注。实际上这也是我在 2023 年被 NixOS 圈粉的主要原因。
  - Nixpkgs 的 commits 图也是一个明显的上升趋势，整个项目都是越来越活跃。
  - RFC 流程也运行得越来越好，Flakes 等遗留问题也从 2023 年开始提出了明确的解决思路并已经
    推进了一部分。此外整个 Nix 社区的组织架构也越来越完善，
  - 总体看，我觉得 NixOS 的未来很光明。
- 调整 2024 年的目标，Guix 折腾了一波觉得还是没 NixOS 香，加上目前看 NixOS 社区相当活跃，
  决定重点投入 NixOS 而不是 Guix.
  - 也在考虑是否通过 Rust 语言来学习操作系统。最好是学了 Linux 跟 Rust 立即就能写点有用的
    程序。

### 2024-01-28

- 对 nix-config 做了比较多的改动
  - 尝试了在 Hyprland 下使用 sunshine/rustdesk 当远程桌面，全部失败，wayland 下的远程桌面
    方案稳定性仍旧很差。
  - yabai 在 macOS 14.3 Intel 下无法正常工作，排查到 6.0.7 解决了这个问题，但 Nixpkgs 里仍
    旧只有 6.0.6，所以 override 了一下解决了问题。
  - 将旧的基于 Ubuntu 22.04 的 tailscale-gateway 虚拟机替换成了 NixOS，非常舒适。
  - 尝试使用 NixOS + dae 作为 bypass router 替代掉我当前的 OpenWRT 旁路由，加了点初步的配
    置，但还没开始测试。
  - 将所有 Hosts 的静态 IP、网关配置集中管理，方便以后修改。

### 2024-01-26 - 2024-01-27

- 研究了 OpenSSH 与 GnuPG 的密钥安全性，并据此重新生成了所有个人 SSH 及 PGP 密钥对。它们的
  passphrase 也全部使用了新生成的随机密码，专门编了些小故事来记忆它们（毕竟人类擅长记忆故
  事，但不擅长记忆随机字符）。
- 更新了一遍我所有重要账号的密码，以及 backup codes，全部保存在了我的 password-store 中。
  - 改了近 30 个账号的密码，包括微信、QQ、GitHub、Google、Microsoft、等等。
- 使用新生成的 GPG 新密钥对重新加密整个 pass 密码仓库，清理整个 pass 仓库的所有历史
  commit，确保只有新的密钥对能解密其中数据
- 做了完善的数据备份，所有备份数据全部通过 rclone 加密存储。
  - rclone 的加密配置保存在 secrets 仓库中，而 secrets 的恢复密钥当然不能用 rclone 加密存
    储，否则就死锁了。所以我将 secrets 仓库的恢复密钥使用 age 对称加密后再存储在备份盘中
    （passphrase 与 GPG 一致以避免遗忘）。
  - 其实 secrets 仓库恢复用的 SSH 密钥本身就有 passphrase，但 OpenSSH 自身的加密算法不够
    morden，所以再用 age 加密一层会保险很多（即使使用的是相同的 passphrase）。
- 在去年发的帖子中更新了最新进展：
  [学习并强化个人的数据安全性（持续更新）](https://0xffff.one/d/1528/10)
- 读了一遍 [Wayland 官方文档](https://wayland.freedesktop.org/)，大概了解了 X11 的缺陷，以
  及 Wayland 的改进。大概意思就是去掉中间代理商 X.org Server，让 Compositor 自己直接跟内核
  通信，同时 Application 也直接通过共享内存的方式自己渲染，结果上就是比 X11 好许多的性能，
  以及比 X11 精简非常多的协议实现。Compositor 跟 Application 都获得了更大的自由空间，这也
  激发了社区的创造力。所以在 wlroots 这个工具库之上，出现了许多活跃的现代化的 Compositor
  实现，比如说 Hyprland.
- 调研了下支持 Wayland 的远程桌面方案，在 X11 上是有很多成熟的方案可选的，比如说
  `ssh -X`/RDP，而在 Wayland 上，目前看（2024-01）比较 OK 的方案有（待测试）：
  - [waypipe](https://gitlab.freedesktop.org/mstoeckl/waypipe/): 一个类似 `ssh -X` 的方案
  - 据说 rustdesk 目前对 wayland 的支持比较 OK
  - 也有很多人推荐使用 sunshine + moonlight 这套游戏串流方案。

### 2024-01-22

- 研究了一波所有 rust/go 重写的摩登命令行工具的简单使用及区
  别：eza/bat/sad/duf/dust/gdu/fzf/ripgrep/fd 等等。
- 因为跟朋友聊到 Emacs Magit 插件好用，他向我推荐了类似的 TUI 工具 lazygit 跟 lazydocker，
  确实也都很好用，而且比 Emacs 轻量、对新手更友好。
- 读了点 NixOS 创始人的论
  文：[The Purely Functional Software Deployment Model](https://edolstra.github.io/pubs/phd-thesis.pdf)
- 朋友 @碎冰冰 问了下「你在学一个新的技术或者框架的时候，是怎么做的笔记？我看技术书籍老觉
  得有时候做成了抄书，有时候看二手资料，也觉得有点一叶障目。」
  - 我的回答：
    - 我以前自学了点分布式系统，做了这个笔记：
      https://thiscute.world/posts/consistency-and-consensus-algorithm/
    - 我学这玩意儿的时候看的各种资料，都只讲了作者自己想到的某个方面，没有任何一篇文章能完
      整地解答我的疑惑。
    - 我带着疑问，通过查阅各种资料，把我想知道的东西全部汇总到了一起，结果就是这篇文章。其
      实里面绝大部分数据都是抄的，但我觉得写出来自己还是清晰了不少。
    - 而且我也相信我做了一些别人没做过的事情，因为我自己的这篇文章能解答我学习过程中的疑
      惑，但我看过的其他任何一份资料都做不到这一点。
    - **所以我觉得，内容是不是抄的并不重要。最核心的是，要带着疑问去做笔记，笔记里要有自己
      的思考在**。

### 2024-01-21

- 了解了下 canokey 跟其他硬件密钥方案，以后有兴趣自己搞几个看看。
- 学习了下如何使用 NixOS 当路由器用，目前第一步是用它替换我的 OpenWRT 旁路由。
  - 这个旁路由目前只有一个功能：帮我「流畅上网」，因为 clash 已经跑路了，目前打算换成 dae
    来加流畅上网功能。
- 用了几天 Emacs Magit，确实非常香啊！已经爱不释手了，比记一堆 Git 命令要方便太多了。

### 2024-01-20

- 继续补充更新了一波我的个人加密方案文档，文档目前在我的私密笔记中，打算近期开始实施。
  - 其实也没有那么急，有兴趣的时候就折腾一下，一两个月内搞定就行。

### 2024-01-19

- 重新梳理了下我 2024 年的兴趣与目标，更新了 /now 页面以及 /2023-summary 中的 2024 年展
  望。
  - 技术上的三个核心目标：**搞搞 AIGC、学学操作系统、了解下 Lisp/Emacs 生态圈**
- 补充更新我的个人安全加密方案文档。并且研究了 LUKS2 加密的安全性，发现它的 argon2id KDF
  算法可以手动设定迭代次数，这样可以大幅提升破解难度。这跟我以前学的密码学知识对应上了。
  - 进一步考虑，OpenSSH 私钥的 passphrase、GnuPG 的 passphrase 强度分别有多高？确实还没研
    究过呢。
  - 调研了跨平台的全盘加密方案，最后发现 rclone 自带的加密功能应该是最好使的，而且还能同时
    将数据加密备份到七牛云/青云/阿里云等云服务商提供的免费对象存储空间。看了下其安全性应该
    也足够。
- 因为渐渐意识到 Nix 设计上存在的一些缺陷，正在尝试折腾 Guix 跟 Guile 语言。
  - 目前只能说没有银弹，Guix 也有它自己的缺点...

### 2024-01-18

- 学习了 Emacs Magit 拓展的用法，确实挺香的。
- 买的 U 盘到货了，写了一晚上的个人数据安全方案，梳理了下我所有的隐私数据，初步考虑清楚了
  如何做多备份、如何加密、如何灾难恢复等等。
  - 密码尽量设计得够随机且复杂度高，然后尽量通过复用密码来减少记忆负担，定期回顾密码，或者
    确保日常会经常用到这些密码，避免遗忘。
  - argon2 的迭代次数设置得尽可能高，提升破解难度。
  - 根据数据的重要级别与日常使用频率对数据进行分类，然后分别采用不同的加密方案、分别保存在
    不同的 U 盘上。
  - U 盘需要定期检查（暂定半年或一年一次），防止数据损坏。

{{<figure src="/images/now-2024/2023-01-18_nixos-book-1k-stars.webp" title="NixOS 小书满 1k stars 了！" width="80%">}}

### 2024-01-17

- 注销印象笔记账号，使用 evernote-backup 跟 evernote2md 两个工具将我的私密笔记迁移到了一个
  私有 Git 仓库，用 GitJournal 在手机上查看编辑笔记。
- 考虑到笔记跟其他各种数据的安全性，买了一堆 U 盘，用于重要数据的双备份，打算全部 LUKS 加
  密存储，LUKS 解密密钥交叉保存在不同的 U 盘上。
  - 简单的说就是，一定要两个不同的 U 盘都在手上才能解密其中的数据。
  - 以前对安全的考虑不多，曾经把各种重要账号的 backup_code 直接保存在百度云盘或 onedrive
    上，一些密码经过简单的转换后直接写在印象笔记中。隐患挺大。这次加密备份方案上线过程中，
    也打算同步更新一次所有的 backup codes 以及主要账号的密码。

{{<figure src="/images/now-2024/2023-01-17_evernote-china-delete-account.webp" title="注销了从大一用到现在的 evernote 印象笔记，数据都迁移到了 GitJournal" width="70%">}}
{{<figure src="/images/now-2024/2023-01-17_buy-usb-keys-for-security.webp" title="买了一堆 U 盘，用于 GPG 密钥等数据的双备份，LUKS 加密存储" width="70%">}}

### 2023-01-16

- 偶尔想起，在 NixOS TG 群里提到我电脑重启经常报 /dev/xxx is not a LUKS devices，NickCao
  立马问我是不是有多个磁盘，问题马上就定位到了，万能的 NickCao!

### 2024-01-15

- 读了一遍 Vim 的官方文档 <https://vimhelp.org/>，深入学习了 Vim 本身的使用。
- 又过了一遍 Helix 的 `:tutor`，Helix 确实精简非常多，键位设计上 `motion` 前置用着确实更舒
  服一点，值得一用。

### 2024-01-14

- 对 2023 年的年终总结做了些更新，加了些图片，补充了对 2024 年工作上的展望，技术上的期望也
  做了些调整，更明确、精简了。
- 以 2024 年的新状态与目标为参照，更新了 /now 页面
- 参加 Emacs 深圳线下聚会，作为一个玩 Emacs 不到一个月的新手，去听听大佬们的分享，学习一
  下，也感受下极客圈的氛围哈哈。
  - 印象深刻的有一个用 Framework 模块化笔记本的大佬，坐我旁边，还有一个日常用 Streamdeck
    的佬（也用 Nix，日常写 Elixir）
  - 三个人分享，他们命令行操作全都贼六，基本不用鼠标。
  - 因为发现大家都对 Nix 比较感兴趣，甚至有不少朋友曾经试用过但被劝退了。我也借此机会分享
    了下 NixOS/nix-darwin 的使用，优缺点。以及为什么我现在在尝试 Guix（我就是因为折腾
    Guix，安装文档装了个 Emacs 不会用，这才入了 Emacs 的坑）。

### 2024-01-10 - 2024-01-13

- 完成了将密码管理全部迁移到 password-store 的工作，现在 NixOS/macOS 跟 Android 上都可以使
  用了，非常香！
- 继续微调 emacs 配置，之前加了 lsp-bridge 后语法高亮各种毛病，它的配置还是太复杂了，我换
  回了 lsp-mode. doom-emacs 下 lsp-mode 完全是开箱即用的，慢一点但配置起来不费脑子！
- 熟悉 orgmode 语法，用起来还是挺多不习惯，尤其是它的转义问题，我研究了一整天，现在还是有
  几个「[未解之迷](https://github.com/ryan4yin/guix-config/blob/079bd61/ORGMODE.org)」...
- 发现 NixOS 内置了 Guix 支持
  [nixos/guix: init](https://github.com/NixOS/nixpkgs/pull/264331)，装上玩了一波。
- 跟领导聊完了年终绩效，以及明年的工作展望。看起来我明年需要深入搞一搞 AIGC 的规模化，有机
  会深入搞下新鲜火热的 AI 技术，还挺期待的。
  - RTX 4090 虽然吃灰大半年，但现在国内已经禁售了... 或许今年还能发挥一下它的作用

### 2024-01-09

- [pass : 密码管理本不复杂](https://nyk.ma/posts/password-store/): 前两天学 Emacs 看到了这
  篇文章，给我带来了对密码管理的新思路！
- 然后今天研究一天的 password-store 跟 gpg 的使用，把所有原本保存在 Firefox 中的密码全部迁
  移到了 password-store + GnuPG 加密，并 push 到 GitHub 的一个私有仓库上。太香了！

### 2024-01-01 - 2024-01-07

- 继续尝鲜 DoomEmacs，对其配置做了大量的迭代。
  - 折腾好多天了，目前遇到的问题都解决得差不多了，很漂亮用着也挺舒服。现在最头疼的问题还
    剩：
    - Emacs 的代码格式化跟 Neovim 不一致，两边会把代码格式化来格式化去... 导致我无法在同一
      项目上混用两个编辑器
- 学会了使用 parinfer 这个插件写 lisp/scheme，确实非常爽，它会根据缩进情况全自动地添加或删
  除括号，使用户完全不用关心括号的问题。难怪被人说这个插件使写 lisp 就跟写 python 一样了
  emmm
- 把 Makefile 换成了 Justfile，简单清爽了不少，还结合 nushell 脚本做了些代码重构
- 学习整理了下编辑器的基础知识：Vim 键位速查表、现代化编辑器的LSP/TreeSitter 介绍与对
  比、Formatter/Linter 等工具的区别等等。
  - <https://github.com/ryan4yin/nix-config/tree/main/home/base/desktop/editors>
- 周六到逛了半天公园，可能是天气好、然后山里空气、风景也不错，再听着歌，简直开心到起飞！
- 周日早上挂了医院的过敏反应科，想做个过敏源筛查，做了皮试跟血检，三天后才能出结果。

### 2024-01-01

- 发布了 [2023 年年终总结](/posts/2023-summary/)
