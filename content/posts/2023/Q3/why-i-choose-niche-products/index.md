---
title: "为什么我折腾这些小众技术？"
subtitle: ""
description: ""
date: 2023-08-01T11:40:57+08:00
lastmod: 2023-08-01T11:40:57+08:00
draft: false

resources:
  - name: "featured-image"
    src: "anime-girls-seagulls.webp"

tags: ["Vim", "Neovim", "VSCode", "Editor", "IDE", "Linux", "中文输入法"]
categories: ["tech", "life"]
series: []
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

我折腾过许多的小众技术，而今年新折腾的主要有 NixOS、窗口管理器 i3 / hyprland、以及 Neovim，其中 NixOS 我甚至折腾到了一个新境界——出了一本帮助新手入门的中英双语开源书籍 [nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book)，还搞了好几个 NixOS 相关的开源项目（比如 [nix-darwin-kickstarter](https://github.com/ryan4yin/nix-darwin-kickstarter) 跟 [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config)），都收到了许多好评。

结合我自己折腾这些小众技术的经历，以及我经常被问到的问题（为什么你选择用 [NixOS](nixos.org/) / [Neovim](https://github.com/Neovim/Neovim) / [小鹤音形中文输入法](https://flypy.com/)？它有什么好处？它真的能提升效率吗？等等），我想在这里简单谈谈我对它们的看法。

<!--more-->

## 什么是小众技术？

小众，是相对于大众而言的。小众技术，指在该领域中用户占比较相对较小的技术。

基于这样的定义，我可以列举出我接触过的不同领域的一些小众技术：

| 领域           | 小众技术                                   | 大众技术              |
| -------------- | ------------------------------------------ | --------------------- |
| 编辑器         | Neovim、Emacs                              | VSCode、Pycharm、IDEA |
| 中文输入方案   | 双拼、小鹤音形、五笔、二笔、郑码、灵形速影 | 智能拼音              |
| Linux 操作系统 | NixOS、Gentoo、Arch Linux                  | Ubuntu、Fedora        |
| 窗口管理器     | i3、hyprland                               | KDE、GNOME            |


大多数人在使用这些领域的技术时，都会选择大众技术，因为它们的入门门槛低，使用起来也比较方便。
我曾经也是这大多数人之一，但是我渐渐发现，这些小众技术也有它们的优势，所以我开始尝试使用它们，并逐渐过渡到了它们。


## 这些小众技术有什么特点？

小众技术显然得拥有一些优势，才能吸引到一部分用户，让这些用户选择它们而不是大众技术。

从我个人的使用经验来看，我用过的这些小众技术，具有一些比较明显的共同特征。

首先是它们共同的劣势：**入门门槛更高，入门阶段需要花费更多的时间去学习、熟悉**。

这就过滤掉了大部分用户，只有那些喜欢折腾、喜欢挑战的人才会去尝试这些小众技术。

比如说五笔输入法，它们的入门门槛很高，需要花费大量的时间去记忆它的键位编排、去练习，前期的输入体验会跌到谷底。
要想达到你曾经智能拼音的输入速度，感觉至少得每天练习 1 个小时，持续一个月（这很可能还不够）。

其他形码输入法也是一样，我用的小鹤音形算是一个折衷的选择，它的入门门槛比五笔低一些，学会后也能获得类似五笔的输入体验。

再说说它们共同的优势：

1. **定制程度高**：用户可以根据自己的需求，自由地定制各种功能。
2. **强烈的掌控感、绝佳的使用体验**：高度的自定义，让用户感觉到自己在使用这些技术的过程中，能够完全掌控一切，从而带来绝佳的使用体验。
3. **用户黏性高、社区活跃**：用户在使用这些技术的过程中，会不断地去探索、去学习、去定制，这会让用户对它们产生强烈的归属感。

也因为上面这些原因，用户一旦成功入门某项小众技术（比如说形码输入法、Neovim/Emacs 编辑器），就很难再退回到曾经的大众方案——他们会发现曾经的大众方案用起来，各种不顺手、不爽快。

## 我为什么折腾这些小众技术？

我折腾过许多小众技术，而原因中最大的一部分，应该是好奇心。
但好奇心只能让我去尝试，让我留下来的，是它们优秀的使用体验。

比如说最近折腾的 Neovim 编辑器、Hyprland 窗口管理器，让我留下来继续使用它们的原因，一是 Neovim 跟 Hyprland 配置好了之后，真的很漂亮！而且 Neovim 速度真的超快、太快了！
一些从没深度体验过 Neovim 的 VSCode / IDEA 用户可能会觉得这种快不过如此，但是一旦你真的体验过，就会发现这种快真的很爽，就像流浪地球 2 中图恒宇的感叹一样（550W 太快了！这速度太快了！）

二是实际入门后，发现它们用起来很爽快，基于键盘的交互，能带给我形码输入法的那种掌控感、流畅感（优雅，太优雅了 hhh）。


{{<figure src="./hyprland_2023-07-29_1.webp" title="我的 NixOS + Hyprland 桌面" width="85%">}}
{{<figure src="./hyprland_2023-07-29_2.webp" title="我的 Neovim 编辑器" width="85%">}}

而我折腾并且爱上 NixOS，也是基于类似的原因。
拥有声明式、可复现（一致的运行环境）、OS as Code 等这些特点的 NixOS，对于本运维狗而言，真就是理想中的样子，这让我迫不及待地想要使用它，即使发现了问题也希望能尽快完善它，使它能够适用于更多的场景。

> 前两天在 4chan 上看到某外国网友的这么一段评论（虽然言词有点偏激，但我还真有点认同...）：
> Completely and utterly unacceptable. Imagine having a tool that can't even properly undo an operation and then relying on it to manage an operating system.
> `apt`, `pip`, `pm`, `rpm`, `pacman`, whatever are all a mad fucking joke.

## 小众工具或技术能提升效率吗？

有许多人说，Neovim 编辑器、i3 窗口管理器、形码输入法等这些小众工具或技术，能提升效率，我觉得这是一个误区。
相反，其中许多工具或技术，实际上是一个时间销金窟，你会被自己的兴趣驱使着去不断探索它们的边界、调整它的配置使其更契合自己的需求。
这导致至少前面较长一段上升期，这些投入的时间会比你效率提升所省下的时间多得多。

所以说到底，想用这些技术来提升效率啥的还是不用想了。
它能提升你的效率，但是比较有限，除非你写代码/文档的效率是受限于你的手速 emmm

> 当然也有些特殊场景，比如说有的人需要经常输入些生僻字，这时候智能拼音就比较鸡肋了，五笔等形码输入法就确实能大大提升输入效率。

或者有人会说，完全熟悉后，vim/emacs 能使你更容易进入心流状态？这个也很难说吧。


## 那折腾这些东西，到底有什么好处？

如果从很功利的角度看的话，确实就没啥好处，就跟打游戏一样，单纯在消遣时光而已。

{{<figure src="./useless-work.jpg" width="35%">}}

要说跟做些无聊的事消遣时光有啥区别的话，大概就是还确实能获得点有用的东西。
比如我，遇到 AstroNvim 的 bug ，会提 PR 给上游仓库。发现 NixOS 的文档很糟糕，我直接自己写文档并分享出来。
发现 NixOS 缺少对我手头某块开发板的支持，我会自己尝试移植。
啥时候发现某工具缺少自己想要的功能，我也可能直接自己写一个。

这些折腾过程中获得的经验、创建的开源项目、在上游仓库中留下的 PR 、在社区中收获的感谢，感觉都是有价值的。
它不一定有啥业务价值，但是它好玩啊，还能交到朋友，帮到别人，在开源社区留下自己的痕迹，这不是很有意思么？

Linus 最开始写 Linux，也[只是为了好玩（Just For Fun）](https://book.douban.com/subject/1451172/).


## 结语

你展望人生的时候，不可能把这些点连起来；只有当你回顾人生的时候，才能发现它们之间的联系。所以你必须有信心，相信这些点总会以某种方式，对你的未来产生影响。你必须相信一些事情----你的勇气、命运、人生、缘分等等。这样做从未令我失望，反而决定了我人生中所有与众不同之处。

—— [You’ve got to find what you love, by Steve Jobs, CEO of Apple Computer](https://news.stanford.edu/2005/06/12/youve-got-find-love-jobs-says/)



