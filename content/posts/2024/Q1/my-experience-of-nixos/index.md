---

title: "OS as Code - 我的 NixOS 使用体会"
subtitle: ""
description: ""
date: 2024-02-21T16:26:21+08:00
lastmod: 2024-02-21T16:26:21+08:00
draft: false

resources:
  - name: "featured-image"
    src: "nixos-and-flakes-book-202402.webp"

tags: ["NixOS", "Nix", "Flakes", "Linux", "DevOps"]
categories: ["tech"]
series: ["NixOS 与 Nix Flakes"]
series_weight: 3
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

toc:
  enable: true
math:
  enable: false
license: ""

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---


> 本文最初发表于 [如何评价NixOS? - 知乎]，觉得比较有价值所以再搬运到我的博客。

我 23 年 4 月开始用 NixOS 之前看过（[如何评价NixOS? - 知乎]） 这个问答，几个高赞回答都从不同方面给出了很有意义的评价，也是吸引我入坑的原因之一。

现在是 2024 年 2 月，距离我入坑 NixOS 刚好 10 个月，我当初写的新手笔记已经获得了大量好评与不少的赞助，并成为了整个社区最受欢迎的入门教程之一。自 2023 年 6 月我为它专门创建一个 GitHub 仓库与单独的文档站点以来，它已经获得了 1189 个 stars，除我之外还有 37 位读者给它提了 PR：

- [NixOS 与 Flakes - 一份非官方的新手指南](https://nixos-and-flakes.thiscute.world/zh/)

{{<figure src="./nixos-and-flakes-book-202402.webp" title="NixOS & Flakes Book" width="80%">}}

那么作为一名已经深度使用 NixOS 作为主力桌面系统接近 10 个月的熟手，我在这里也从另一个角度来分享下我的入坑体会。

注意，这篇文章不是 NixOS 入门教程，想看教程请移步上面给的链接。

## Nixpkgs 中的包太少？ {#is-nixpkgs-lacking-packages}

先澄清下一点，NixOS 的包非常的多，Nixpkgs 中的包在体量上跟 Arch AUR 是一个级别的。[Repository statistics](https://link.zhihu.com/?target=https%3A//repology.org/repositories/statistics/total) 的包仓库统计数据如下：

![Repository statistics](./repository-statistics.webp)

虽然 Nixpkgs 因为还打了许多 npm 之类的包，包的总数有水分，但即使排除掉这部分包，它跟 AUR 的包数量应该也是差不多的。

而且因为 Nixpkgs 是官方包仓库，使用了 Monorepo 与 PR Review 机制，整体的包质量肯定是比 AUR 要好的。上面截图也能看到 Nixpkgs 的包整体上比 AUR 更新、漏洞更少。

包仓库这里也是 NixOS 跟 Arch 不太同的地方，Arch 的官方包仓库收录很严格，相对的 AUR 生态相当繁荣。但任何人都能往 AUR 上传内容，虽然有一个投票机制起到一定审核作用，但这个限制太松散了。

而 NixOS 就很不一样了，它的官方包仓库 Nixpkgs 很乐于接受新包，想为 Nixpkgs 提个 PR 加包或功能相对其他发行版而言要简单许多，这是导致 Nixpkgs 的体量接近 AUR 的直接原因（GitHub 显示 Nixpkgs 有 5000+ 历史贡献者，这很夸张了）。NixOS 其实也有个与 AUR(Arch User Repository) 类似的 NUR（Nix User Repository），但因为 Nixpkgs 的宽松，NUR 反而没啥内容。

举例来说，QQ 能直接从 Nixpkgs 官方包仓库下载使用，而在 Arch 上你得用 AUR 或者 archlinux-cn.

这算是各有优势吧。NixOS 被人喷包少，主要是因为它不遵循 FHS 标准，导致大部分网上下载的 Linux 程序都不能直接在 NixOS 上运行。这当然有解决方案，我建议是首先看看 Nixpkgs 中是否已经有这个包了，有的话直接用就行。如果没有，再尝试一些社区的解决方案，或者自己给打个包。

用 NixOS 的话自己打包程序是不可避免的，因为即使 Nixpkgs 中已经有了这么多包，但它仍然不可能永远 100% 匹配你的需求，总有你想用但 Nixpkgs 跟 NUR 里边都没有的包，在 NixOS 上你常常必须要给你的包写个打包脚本，才能使它在 NixOS 上正常运行。

另外即使有些程序本身确实能在 NixOS 上无痛运行，但为了做到可复现，NixOS 用户通常也会选择自己手动给它打个包。

OK，闲话说完，下面进入正题。

首先，NixOS 比传统发行版复杂很多，也存在非常多的历史遗留问题。

举例来说，它的官方文档烂到逼得我一个刚学 NixOS 的新手自己边学边写入门文档。在我用自己的渣渣英语把笔记翻译了一遍发到 reddit （[NixOS & Nix Flakes - A Guide for Beginners](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/)）后，居然还获得了许多老外的大量好评（经过这么长时间的持续迭代，现在甚至已经变成了社区最受欢迎的新手教程之一），这侧面也说明官方文档到底有多烂。


## NixOS 值不值得学？ {#is-nixos-worth-learning}

**NixOS 值不值得学或者说投入产出比是否够高？在我看来，这归根结底是个规模问题**。

**这里的规模，一是指你对 Linux 系统所做的自定义内容的规模，二是指你系统更新的频繁程度，三是指你 Linux 机器的数量**。

下面我从个人经历的角度来讲下我以前用 Arch Ubuntu 等传统发行版的体验，以及我为什么选择了 NixOS，NixOS 又为我带来了什么样的改变。

举个例子，以前我用 Deepin Ubuntu 时我基本没对系统做过什么深入定制，一是担心把系统弄出问题修复起来头疼，二是如果不额外写一份文档或脚本记录下步骤的话，我做的所有定制都是黑盒且不可迁移的，一个月后我就全忘了，只能战战兢兢地持续维护这个随着我的使用而越来越黑盒、状态越来越混沌的系统。

如果用的是 Arch 这种滚动发行版还好，系统一点点增量更新，遇到的一般都是小问题。而对 Ubuntu Deepin 这种，原地升级只出小问题是很少见的，这基本就意味着我必须在某个时间点，在新版本的 Ubuntu 上把我以前做过的定制再全部重做一遍，更关键的是，我非常有可能已经忘了我以前做了什么，这就意味着我得花更多的时间去研究我的系统环境里到底都有些啥东西，是怎么安装配置的，这种重复劳动非常痛苦。

总之很显然的一点是，我对系统做的定制越多越复杂，迁移到新版本的难度就越大。

我想也正是因为这一点，Arch Gentoo Fedora 这种滚动发行版才在 Linux 爱好者圈子中如此受欢迎，喜欢定制自己系统的 Linux 用户也大都使用这类滚动发行版。

那么 Arch Fedora 就能彻底解决问题了么？显然并不是。
首先它们的更新频率比较高，这代表着你会更容易把你的系统搞出点毛病来。当然这其实是个小问题，现在 Linux 社区谁还没整上个 btrfs / zfs 文件系统快照啊，出问题回滚快照就行。
它们最根本的问题是：

1. 你的 Arch 系统环境、文件系统快照、或者虚拟机快照，它们仍然是个黑盒，仍然会随着你的持续使用而越来越混沌，也并不包含如何从零构建这个环境的「知识」，是**不可解释**的。
   - 我在工作中就见到过一些「**祖传虚拟机快照**」或「**祖传云服务器快照**」，没人知道这个环境是怎么搭建的，每一任接手的人都只能继续往上叠 Buff，然后再把这个定时炸弹传给下一任。这就像那个轮流往一个水杯里加水的游戏，最后在谁加水的时候溢出来了，那就算他倒霉。
1. Arch 实质要求你持续跟着它的更新走，这意味着你必须要持续更新维护它。
    - 如果你把机器放了一年半载跑得很稳定，然后你想要更新一下，那出问题的风险会相当高。如果你因此而决定弄台最新版本的 Arch 机器再把旧环境还原出来，那就又回到了之前的问题——你得想办法从旧环境中还原出你的定制流程，这也不是个好差事。
1. 快照与当前硬件环境强相关，直接在不同硬件的机器上使用很容易遇到各种奇怪的问题，也就是说这东西**不可迁移**。
1. 快照是一堆庞大的二进制文件，它的体积非常大，这使得备份与分享它的成本高昂。

Docker 能解决上述问题中的一部分。
首先它的容器镜像可由 Dockerfile 完全描述，也就是说它是**可解释**的，此外容器镜像能在不同环境中复现出完全一致的环境，这表明它是**可迁移**的。
对于服务器环境，将应用程序全都跑在容器中，宿主机只负责跑容器，这种架构使得你只需要维护最基础的系统环境，以及一些 Dockerfile 跟 yaml 文件，这极大地降低了系统的维护成本，从而成为了 DevOps 的首选。

但 Docker 容器技术是专为应用程序提供一致的运行环境而设计的，在虚拟机、桌面环境等场景下它并不适用（当然你非要这么弄也不是不行，很麻烦就是了）。
此外 Dockerfile 仍旧依赖你所编写的各种脚本、命令来构建镜像，这些脚本、命令都需要你自己维护，其运行结果的可复现能力也完全看你自己的水平。

如果你因为这些维护难题而选择极简策略——尽可能少地定制任何桌面系统与虚拟机环境，能用默认的就用默认——这就是换到 NixOS 之前的我。
为了降低系统维护难度，我以前使用 Deepin Manjaro EndeavourOS 的过程中，基本没对系统配置做任何大变动。
作为一名 SRE/DevOps，我在工作中就已经踩了够多的环境问题的坑，写腻写烦各种安装脚本、Ansible 配置了，业余完全不想搞这些幺蛾子。

但如果你是个喜欢定制与深入研究系统细节的极客，随着你对系统所做的定制越来越多，越来越复杂，或者你 Homelab 与云上的 Linux 机器越来越多，你一定会在某个时间点开始编写各种部署流程的文档、部署脚本或使用一些自动化工具帮自己完成一些繁琐的工作。

文档就不用说了，这个显然很容易过时，没啥大用。
如果你选择自己写自动化脚本或选用自动化工具，它的配置会越来越复杂，而且系统更新经常会破坏掉其中一些功能，需要你手动修复。
此外它还高度依赖你当前的系统环境，当你某天装了台新机器然后信心满满地用它部署环境时，大概率会遇到各种环境不一致导致的错误需要手动解决。还有一点是，你写的脚本大概率并没有仔细考量抽象、模块化、错误处理等内容，这也会导致随着规模的扩大，维护它变得越来越痛苦。

然后你发现了 NixOS，它有什么声明式的配置，你仔细看了下它的实现，哦这声明式的配置，不就是把一堆 bash 脚本封装了下，对用户只提供了一套简洁干净的 api 么，它实际干的活不跟我自己这几年写的一堆脚本一模一样？好像没啥新鲜的。

嗯接着你试用了一下，发现  NixOS  的这套系统定制脚本都存在一个叫 Nixpkgs   的仓库中，有数千人在持续维护它，几十年积累下来已经拥有了一套非常丰富、也比较稳定的声明式抽象、模块系统、类型系统、专为这套超大型的软件包仓库与 NixOS 系统配置而开发的大规模 CI 系统 Hydra、以及逐渐形成的能满足数千人协作更新这套复杂配置的社区运营模式。

你立马学习 nix 语言，然后动手把这套维护了 N 年的脚本改写成 NixOS 配置。

越写就对它越满意，改造后的配置缩水了相当多，维护难度直线下降。

很大部分以前自己用各种脚本跟工具实现的功能，都被  Nixpkgs 封装好了，只需要 enable 一下再传几个关键参数，就能无痛运行。nixpkgs 中的脚本都有专门的 maintainer  维护更新，任何发现了问题的用户也可以提个 PR 修下问题，在没经过 CI 与 staging unstable  等好几个阶段的广泛验证前，更新也不会进入 stable.

上面所说的你，嗯就是我自己。

现在回想下我当初就为了用 systemd 跑个简单的小工具而跟 systemd 疯狂搏斗的场景，泪目... 要是我当初就懂 NixOS...

## NixOS 的声明式配置 - OS as Code {#nixos-declarative-configuration}

有过一定编程经验的人都应该知道抽象与模块化的重要性，复杂程度越高的场景，抽象与模块化带来的收益就越高。Terraform/Kubernetes 甚至 Spring Boot 的流行都体现了这一点。NixOS 的声明式配置也是如此，它将底层的实现细节都封装起来了，并且这些底层封装大都有社区负责更新维护，还有 PR Review、CI 与多阶段的测试验证确保其可靠性，这极大地降低了我的心智负担，从而解放了我的生产力。它的可复现能力则免除了我的后顾之忧，让我不再担心搞坏系统。

NixOS 构建在 Nix 函数式包管理器这上，它的设计理念来自 Eelco Dolstra 的论文 [The Purely Functional Software Deployment Model]（纯函数式软件部署模型），纯函数式是指它没有副作用，就类似数学函数 $y = f(x)$，同样的 NixOS 配置文件（即输入参数 $x$ ）总是能得到同样的 NixOS 系统环境（即输出 $y$）。

这也就是说 **NixOS 的配置声明了整个系统完整的状态，OS as Code**！

只要这个你 NixOS 系统的这份源代码没丢，对它进行修改、审查，将源代码分享给别人，或者从别人的源代码中借鉴一些自己想要的功能，都是非常容易的。
你简单的抄点其他 NixOS 用户的系统配置就能很确定自己将得到同样的环境。相比之下，你抄其他 Arch/Ubuntu 等传统发行版用户的配置就要麻烦的多，要考虑各种版本区别、环境区别，不确定性很高。

## NixOS 的学习成本 {#nixos-learning-curve}

NixOS 的入门门槛相对较高，也不适合从来没接触过 Linux 与编程的小白，这是因为它的设计理念与传统 Linux 发行版有很大不同。
但这也是它的优势所在，跨过那道门槛，你会发现一片新天地。

举例来说，**NixOS 用户翻 Nixpkgs 中的实现源码实际是每个用户的基本技能，给 Nixpkgs 提 PR 加功能、加包或者修 Bug 的 NixOS 用户也相当常见**。
**这既是使新用户望而却步的拦路之虎，同时也是给选择了 NixOS 的 Linux 用户提供的进阶之梯**。

想象下大部分 Arch 用户（比如以前的我）可能用了好几年 Arch，但根本不了解 Arch 底层的实现细节，没打过自己的包。而 NixOS 能让翻源码成为常态，实际也说明理解它的实现细节并不难。我从两个方面来说明这一点。

第一，Nix 是一门相当简单的语言，语法规则相当少，**比 Java Python 这种通用语言简单了太多**。因此有一定编程经验的工程师能花两三个小时就完整过一遍它的语法。再多花一点时间，读些常见 Nix 代码就没啥难度了。

第二，**NixOS 良好的声明式抽象与模块化系统，将 OS 分成了许多层来实现，使用户在使用过程中，既可以只关注当前这一层抽象接口，也可以选择再深入到下一层抽象来更自由地实现自己想要的功能**（**这种选择的权利，实际也给了用户机会去渐进式地理解 NixOS 本身**）。举例来说，新手用户只要懂最上层的抽象就正常使用 NixOS。当你有了一点使用经验，想实现些自定义需求，挖下深挖一层抽象（比如说直接通过 systemd 的声明式参数自定义一些操作）通常就足够了。如果你已经是个 NixOS 熟手，想更极客一点，就可以再继续往下挖。

总之因为上面这两点，理解 Nixpkgs 中的源码或者使用 Nix 语言自己打几个包并不难，可以说每个有一定经验的 NixOS 用户同时也会是 NixOS 打包人。

## NixOS 的卖点？ {#nixos-advantages}

我们看了许多人提到 NixOS 的优点，上面我也提到了不少。
圈外人听得比较多的可能主要是它不存在依赖冲突，能随时回滚，强大的可复现能力。
如果你有实际使用过 NixOS，那你也应该知道 NixOS 的这些优势：

1. 系统更新具有类似数据库事务的原子化特性，这意味着你的系统更新要么成功要么失败，（一般）不会出现中间状态。
2. NixOS 的声明式配置实际实现了 OS as Code，这使得这些配置非常便于分享。直接在 GitHub 上从其他 NixOS 用户那里 Copy 需要的代码到你的系统配置中，你就能得到一个一模一样的功能。新手用户也能很容易地从别人的配置中学到很多东西。
3. 声明式配置为用户提供了高度便捷的系统自定义能力，通过改几行配置，就可以快速更换系统的各种组件。
4. 等等

这些都是 NixOS 的卖点，其中一些特性现在在传统发行版上也能实现，Fedora Silverblue 等新兴的不可变发行版也在这些方面有些不错的创新。
但能解决所有这些问题的系统，目前只有 NixOS（以及更小众的 Guix——它同样基于 Nix 包管理器）。

## NixOS 的缺点与历史债务 {#nixos-disadvantages}

自 NixOS 项目创建至今二十多年来，Nix 包管理器与 NixOS 操作系统一直是非常小众的技术，
尤其是在国内，知道它们存在的人都是少数 Linux 极客，更别说使用它们了。

NixOS 很特殊，很强大，但另一方面**它也有着相当多的历史债务**，比如说：

1. 文档混乱不说人话
1. Flakes 特性使 NixOS 真正满足了它一直宣称的可复现能力，但从 2019 年搞到现在 2024 年，它仍旧处在实验状态。
1. Nix 的 CLI 处在换代期，新版本的 CLI 优雅很多，但其实现目前与 Flakes 特性强绑定，导致两项功能都难以 stable，甚至还阻碍了许多其他特性的开发工作。
1. 模块系统的缺陷与 Nix 错误处理方面的不足，导致长期以来它的报错信息相当隐晦，令人抓狂
1. Nix 语言太过简单导致 Nixpkgs 中大量使用 Bash 脚本
1. NixOS 的大量实现细节隐藏在 Nixpkgs 源码中，比如说软件包的分类。长期一直使用文件夹来对软件包进行分类，没有任何查看源码之外的手段来分类查询其中的软件包，体验很差。
1. <https://nixos.wiki> 站点维护者跑路，官方又长期未提供替代品，导致 NixOS 的文档在本来就很烂的基础上又雪上加霜。
1. NixOS 近来快速增长的用户群体，使得它的社区运营模式也面临着挑战
1. ...

这一堆历史债是 NixOS 一直没能得到更广泛使用的主要原因。
但这些问题也是 NixOS 未来的机会，社区目前正在积极解决这些问题，我很期待看到这些问题被解决后， NixOS 将会有怎样的发展。

## NixOS 的未来 {#nixos-future}

谁也不会对一项没前途的技术感兴趣，那么 NixOS 的未来如何呢？我是否看好它？
这里我尝试使用一些数据来说明我对 NixOS 的未来的看法。

首先看 Nixpkgs 项目，它存储了 NixOS 所有的软件包及 NixOS 自身的实现代码：

[![](./nixpkgs-contributors.webp)](https://github.com/NixOS/nixpkgs/graphs/contributors)

上图能看到从 2021 年开始 Nixpkgs 项目的活跃度开始持续上升，
Top 6 贡献者中有 3 位都是 2021 年之后开始大量提交代码，你点进 GitHub 看，能看到 Top 10 贡献者中有 5 位都是 2021 年之后加入社区的（新增的 @NickCao 与 @figdoda 都是 NixOS 中文社区资深用户）。

再看看 Nix 包管理器的提交记录，它是 NixOS 的底层技术：

[![](./nix-contributors.webp)](https://github.com/NixOS/nixpkgs/graphs/contributors)

上图显示 Nix 项目的活跃度在 2020 年明显上升，Top 6 贡献者中也有 6 位都是在 2020 年之后才开始大量贡献代码的。

再看看 Google Trends 中 NixOS 这个关键词的搜索热度：

[![](./nixos-google-trends.webp)](https://trends.google.com/trends/explore?cat=5&date=2014-01-23%202024-02-23&q=NixOS)

这个图显示 NixOS 的搜索热度有几个明显的上升时间点：

1. 2021 年 12 年
   - 这大概率是因为在 2021 年 11 月 [Nix 2.4](https://nixos.org/manual/nix/unstable/release-notes/rl-2.4) 发布了，它带来了实验性的 Flakes 特性与新版 CLI，
Flakes 使得 NixOS 的可复现能力得到了极大的提升，新 CLI 也更符合用户直觉。
1. 2023 年 6 月
   - 最重要的原因应该是，Youtube 上 Linux 相关的热门频道在这个时间点推出了好几个关于 NixOS 的视频，截至 2024-02-23，Youtube 上播放量最高的三个 NixOS 相关视频都是在 2023-06 ~ 2023-07 这个时间段推出的，它们的播放量之和超过了 130 万。
   ![](./nixos-youtube-videos.webp)
   - China 的兴趣指数在近期最高，这可能是因为国内的用户群一直很少，然后我在 6 月份发布了 [NixOS 与 Flakes - 一份非官方的新手指南](https://nixos-and-flakes.thiscute.world/zh/)，并且在 [科技爱好者周刊](https://github.com/ruanyf/weekly/issues/3315) 等渠道做了些推广，导致 NixOS 的相对指数出现明显上升。
1. 2024 年 1 月
   - 这个我目前不太确定原因。

再看看 Nix/NixOS 社区从 2022 年启用的年度用户调查。

1. [2022 Nix Survey Results](https://discourse.nixos.org/t/2022-nix-survey-results/18983)，根据其中数据计算可得出：
   - 74.5% 的用户是在三年内开始使用 Nix/NixOS 的。
   - 关于如何拓展 Nixpkgs 的调查中，36.7% 的用户使用 Flakes 特性拓展 Nixpkgs，仅次于传统的 overlays.
2. [Nix Community Survey 2023 Results](https://discourse.nixos.org/t/nix-community-survey-2023-results/33124)，简单计算可得出，
   - 54.1% 的用户是在三年内开始使用 Nix/NixOS 的。
   - 关于如何拓展 Nixpkgs 的调查中，使用 Flakes 特性的用户占比为 49.2%，超过了传统的 Overlays.
   - 关于实验特性的调查中，使用 Flakes 特性的用户占比已经达到了 59.1%.

另外 GitHub 的 [Octoverse 2023](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/) 也难得地提了一嘴 Nixpkgs:

> Developers see benefits to combining packages and containerization. As we noted earlier, 4.3 million repositories used Docker in 2023.<br/>
> **On the other side of the coin, Linux distribution NixOS/nixpkgs has been on the top list of open source projects by contributor for the last two years**.

这些数据与我们前面提到的 Nixpkgs 与 Nix 项目的活跃度相符，都显示 Nix/NixOS 社区在 2021 年之后开始迅速增长壮大。

结合上面这些数据看，我对 NixOS 的未来持很乐观的态度。

## 总结 {#conclusion}

从决定入坑 NixOS 到现在，短短 10 个月，我在 Linux 上取得的收获远超过去三年。我已经在 PC 上尝试了非常多的新技术新工具，我的 Homelab 内容也丰富了非常多（我目前已经有了十多台 NixOS 主机），我对 Linux 系统结构的了解也越来越深刻。

光是这几点收获，就完全值回票价了，欢迎入坑 NixOS~


[如何评价NixOS? - 知乎]: https://www.zhihu.com/question/56543855/answer/3403111768
[The Purely Functional Software Deployment Model]: https://edolstra.github.io/pubs/phd-thesis.pdf
