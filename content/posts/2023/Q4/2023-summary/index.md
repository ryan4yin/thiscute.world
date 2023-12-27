---
title: "2023 年年终总结"
date: 2023-12-10T18:00:45+08:00
lastmod: 2023-12-10T18:00:45+08:00

draft: true
resources:
- name: "featured-image"
  src: "github-profile-2023-ryan4yin.webp"

tags: ["总结"]
categories: ["life", "tech"]
series: ["年终总结"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

## 闲言碎语

啊呀，又到了一年一度的传统节目——年终总结时间。

## 2023 年流水账

还是跟去年一样，先简单过一下我 2023 年的流水账：

- 1 月
  - 再一次完成了公司 K8s 集群一年一度的升级，虽然仍然有比较大的压力，但这次的过程相当顺利。
  - 然后就是朋友约饭，玩耍，回家过春节。
- 2 月
  - 延续去年底开始对嵌入式硬件的兴趣，继续折腾 stm32 / orange pi 5 / esp32 等嵌入式硬件。
    - 用 STM32 点亮了 TFT 液晶屏，以及搞定了使用 printf 打印日志到串口 - [ryan4yin/learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)
    - 研究在 orangepi5(rk3558s) 上用 npu 跑 AI 任务，写了点笔记 [demos_rk3588](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/rk3588)
  - 折腾 Proxmox VE 集群
    - 主力节点 UM560 固态翻车了，是才用了三个月的 Asgard 512G SSD，颗粒是长江存储的。走京东售后了。（上次翻车是 2022-11-02 炸了根光威弈 Pro 1T，这也没隔多久啊...）
      {{<figure src="/images/now/nvme-critial-medium-error.webp" title="2022-11-02 翻车记录 - 系统无法启动" width="100%">}}
      {{<figure src="/images/now/nvme-device-not-ready.webp" title="2023-02-03 翻车记录 - 系统能启动但是文件损坏" width="100%">}}
    - 研究 Homelab 备份与数据同步方案，写了点笔记 [数据备份与同步策略](https://github.com/ryan4yin/knowledge/blob/master/homelab/%E6%95%B0%E6%8D%AE%E5%A4%87%E4%BB%BD%E4%B8%8E%E5%90%8C%E6%AD%A5.md)
    - 发布文章 [EE 入门（二） - 使用 ESP32 + SPI 显示屏绘图、显示图片、跑贪吃蛇](https://thiscute.world/posts/ee-basics-2-esp32-display/)
      {{<figure src="/images/ee-basics-2-esp32-display/tft_esp32_show_image-2.webp" width="100%">}}
  - 简单玩了玩 Stable-Diffusion-WebUI 跟 sd-webui-controlnet，抄了些网上的提示词，效果确实很惊艳。不过玩了一波就没啥兴趣了，不太想花很多精力去折腾它。
- 3 月
  - 生活上
    - 读完了「The Moon and Sixpence」
    - 跟朋友到游泳馆游泳，算是开年以来最剧烈的一次运动...
    - 跟同事们约着一起穿越了东西冲海岸线，这是我第三次走这条线，风景仍旧很美，当然也走得挺累...
    - 买了块冲浪训练平衡板，练习了一段时间，挺有意思。
  - 业余技术上
    - 仍旧是折腾各种嵌入式设备，新入手了 Sipeed MAIX-III AXera-Pi AX620A（爱芯派）+ Maix M0s MCU, 野火鲁班猫 0，荔枝糖 Nano 9K、M1s Dock、Longan Nano 等一堆大小开发板，折腾各种 Linux 编译、嵌入式开发的内容。
    - 被 Copilot X 小小震撼了下，花了 100 美刀买了个 1 年的订阅，价格不贵，希望能切实帮我提升写代码的效率。
    - 发了篇新博客：[Linux 上的 WireGuard 网络分析（一）](https://thiscute.world/posts/wireguard-on-linux/)
    - 读了一点 [Linux Device Drivers Development 2nd Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition)
- 4 月
  - 在业余爱好上投入的精力越来越多，工作上相对的越来越懈怠，感觉碰到了瓶颈，但搞不明白该怎么解决。
  - 听了 [wd 佬](https://github.com/wdvxdr1123)的建议整了个达尔优 A87Pro 天空轴 v3，一番体验这个天空轴 v3 手感确实贼爽、声音也小，感觉可能有点类似静电容了（虽然我没用过静电容 emmm）。
    - 我毕业以来就 19 年跟 20 年分别买过两把 IKBC 的茶轴跟红轴，茶轴放家里了，红轴一直放在公司用。当时国产轴感觉还不太出名，但是现在我聊键盘的朋友都看不上 cherry 轴了，网上搜了下 cheery 轴也有各种品控下降、轴心不稳、杂音大的诟病。
    - 结合朋友推荐，另外看到 v2ex 上聊键盘的朋友也有说天空轴 v3 好用的，还在知乎上也看到有人说这个轴不错，于是就按捺不住心思下单了。到手确实很惊艳，甚至让我再一次喜欢上了打字的感觉！打了几篇小鹤练习群的赛文享受这种飘逸的感觉。
  - 搞了个 chatglm-6b int4 量化版，本地用我的拯救者笔记本（16G RAM + RTX3070 8G）玩了下，响应速度感觉可以，确实有一定的上下文联想能力，简单的问题也能解答，但是有点不聪明的样子，内容投毒比较严重。
  - 玩 AI 联想到淘垃圾显卡，看嗨了就直接整了套新主机新显示器（我的第一台 PC 主机，以前只买过笔记本电脑），玻璃侧透机箱，RTX 4090，双水冷，组装了大半夜，后面又折腾了好几天，机箱直接当手办展示柜了，效果相当惊艳！缺点一是套下来貌似花了两万多...
    {{<figure src="/images/now/endeavour-rtx4090.webp" title="主机配置" width="80%">}}
    {{<figure src="/images/now/rtx4090-pc-1.webp" title="机箱展示" width="80%">}}
    {{<figure src="/images/now/rtx4090-pc-2.webp" title="机箱展示" width="80%">}}
  - 去听了个 Live House，乐队叫迎春归，青岛的乐队，不过前面许多歌我都觉得一般般，主唱唱功也差了点，全靠架子鼓贝斯烘托。不过末尾几首歌还挺好听的。
  - 天依手办到货，很飒～
    {{<figure src="/images/now/tianyi-vsinger.webp" title="洛天依 秘境花庭 常服手办" width="80%">}}
  - 新主机装了个 Endeavour OS 遇到些奇怪的问题，一怒之下决定换 OS，刚好朋友提到了 NixOS，听说过这玩意儿能做到「可复现」，直接就在 Homelab 里开了个 NixOS 虚拟机开始折腾，由此开始了我的 NixOS 之旅。
  - 用新主机试玩了米忽悠的新游戏「星穹铁道」，还是熟悉的画风跟 UI，制作质量也很高，回合式对战的玩法我本以为会枯燥，不过也还 OK。最重要是 4090 画质够高，游戏的动画跟剧情也都很在线，总体评价很 OK。
  - 用新主机连 Quest 2 打 VR 游戏，发现做过参数优化后，RTX4090 跑 beta saber，Quest 2 的画质参数全调到最高， 5K 120 帧无压力，相当流畅。
  - 用 RTX4090 玩 Cyperpunk 2077，顶配光追画质（叫啥 onedrive）贼棒，真的非常还原真实环境，在 GeForece Experience 上调了个啥优化参数后，4K 差不多能稳定在 100 帧，看半天风景。
- 5 月
  - 月初，在虚拟机里折腾了大半个月 NixOS 后，成功地用几条简单的命令，在我的新主机上复现了整个 NixOS 环境，那一刻真的超级开心，半个月的努力终于得到了回报！
    {{<figure src="/images/2023-summary/i3_2023-07-29_1.webp" width="100%">}}
  - 在新主机上成功复现出我的 NixOS 环境后，紧接着发布了我的系统配置 [ryan4yin/nix-config/v0.0.2)](https://github.com/ryan4yin/nix-config/releases/tag/v0.0.2) 以及这大半个月的学习笔记 [NixOS 与 Nix Flakes 新手入门](https://thiscute.world/posts/nixos-and-flake-basics/)，然后事情就变得越来越有趣起来了！随着读者的反馈以及我对它的不断迭代，这份学习笔记逐渐膨胀成一篇一万多字的博文，并且有了中英双语，然后又转变成一本开源书藉 [nixos-and-flakes-book](https://nixos-and-flakes.thiscute.world/)，在 NixOS 国际社区获得了大量好评！它给我带来了巨大的成就感以及社区参与感。
    {{<figure src="/images/2023-summary/nixos-and-flakes-book-comments_reddit.webp" title="NixOS & Flakes Book 的部分评论 - Reddit" width="100%">}}
    {{<figure src="/images/2023-summary/nixos-and-flakes-book-comments_discourse-github.webp" title="NixOS & Flakes Book 的部分评论 - Discourse 与 GitHub" width="100%">}}
    {{<figure src="/images/2023-summary/nixos-and-flakes-book-comments_discord.webp" title="NixOS & Flakes Book 的部分评论 - Discord" width="100%">}}
  - 在 NixOS 上尝试了 i3 与 Hyprland 两个窗口管理器，并且使用 agenix 管理了系统中的敏感信息，比如密码、私钥、wireguard 配置等。
    - agenix 确实 OK，但它纯 bash 脚本实现的核心功能，体验太差了，错误信息一团糟，解决错误全靠自己摸索。
- 6 月
  - 立了个 flag - 把 NixOS 移稙到我手上的两块开发版上跑起来，一块 ARM64 架构的 Orange Pi 5，以及另一块 RISC-V 架构的 LicheePi 4A.
    - 花了好几天时间研究，在俄罗斯网友的耐心帮助下，终于在 6/4 晚上在 Orange Pi 5 上把 NixOS 跑起来了，还挺有成就感的（虽然现在也不知道拿这板子用来干啥...）
    - 之后断断续续折腾了一个月的 NixOS on LicheePi 4A，试了很多方案，还请教了 [HougeLangley](https://github.com/HougeLangley)、[@nickcao](https://github.com/NickCao)、[@chainsx](https://github.com/chainsx) 等大佬，学会了很多 Linux 相关的东西，费尽千辛万苦终于成功把 rootfs 编译出来了，但死活引导不成功。感觉是 uboot-spl 跟 boot 分区这两个地方的内容有问题，但不知道怎么解决，累觉不爱。
  - 收到一封来自 2018 年的我在 futureme.org 发送的邮件，回想起来，当时我是真迷茫哪。
    {{<figure src="/images/2023-summary/futureme-from-2018-to-2023.webp" title="2018 年写给 5 年后的我的邮件" width="80%">}}
  - 受读者评论启发，将之前的 NixOS 笔记做成了一个单独的文档站点 + GitHub 仓库，[nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book)，也对其内容做了大量更新，用 ChatGPT 3.5 全面优化了英文内容，阅读体验大大提升（英文苦手默默路过...）
    {{<figure src="/images/now/2023-08-13-nixos-and-flakes-book.webp" title="NixOS & Flakes Book" width="100%">}}
- 7 月
  - NixOS 系统配置 [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config) 迭代：
    - 把办公电脑 Macbook Pro 2020 重裝了一遍系統，新系统環境完全通過 nix-darwin 安裝管理，就連大部分的 macOS 系統配置也用声明管理了。至此，我的常用电脑环境全部都使用同一份 nix 配置管理起来了，感覺非常香！
      - Linux 与 macOS 都使用了同一份小鹤音形的 rime 配置，现在输入法的跨平台体验也完全一致了，非常棒！
      - nixpkgs 对 macOS 的支持有限，因此常用的 GUI 程序都通过 nix-darwin 调用 homebrew 进行安装管理。
    - 所有命令行工具的主题，全部统一为了 [catppuccin-mocha](https://github.com/catppuccin/catppuccin).
    - 壁纸文件太大了，将它们拆分到单独的仓库中，方便管理。同时还添加了随机切换壁纸的功能。
    - 添加了三台在 Proxmox VE 上运行的 NixOS 虚拟机，并且尝试用它们组建 NixOS 的分布式构建集群，挺有意思。
    - 发现之前用的 alacritty 功能有限，于是将主力终端换成了 kitty，wezterm 作为备用选择，而 alacritty 就基本不使用了。
    - 主力编辑器从 VsCode 换成了 AstroNvim， 一个 Neovim 发行版，使用非常顺手，启动速度以及使用流畅度都比 VSCode 快很多，缺点就是花了挺长的时间完善我的 Neovim 配置（时间销金窟哪）。
      {{<figure src="/images/now/2023-07-29_astronvim.webp" title="AstroNvim(Neovim)" width="100%">}}
  - 基于在 macOS 上折腾 nix-darwin 的经验，制作了一个 [ryan4yin/nix-darwin-kickstarter](https://github.com/ryan4yin/nix-darwin-kickstarter) 模板仓库，并且在 [Twitter](https://twitter.com/ryan4yin/status/1681639068957028352) 等社区分享了一波，获得一波好评。
  - 从 4 月份折腾 NixOS 到现在，GitHub 上开了五六个 Nix 项目，获得了接近 400 stars，也认识了许多朋友、收到了许多好评，在这个圈子里是有点混开了的 feel.
    - 甚至发现有俄罗斯的老铁在将我的 NixOS 小书翻译成俄语！[fl42v/nixos-and-flakes-book-ru](https://github.com/fl42v/nixos-and-flakes-book-ru)，成就感又涨了一点。
- 8 月
  - 时隔一个多月，在 LicheePi 的 Telegram 群组被老外 ping NixOS 移植进展。又来了点动力再次接续之前 6 月份的移植工作，一番尝试后成功在 Lichee Pi 4A 上把 NixOS 跑起来了！离开始移植已经过去了两个月，迟来的成功，泪目！ping 我的老外也在第二天用我提供的镜像成功把 NixOS 跑起来了！他甚至表示要给我打 $50 美元以表感谢，因为这太有意思了！
    - [ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a)
      {{<figure src="/images/2023-summary/nixos-riscv-cluster.webp" title="NixOS on LicheePi4A" width="100%">}}
  - 排查问题的方法：首先刷好一个可在 LicheePi 4A 上正常启动的 Fedora 系统，然后用我编译出的 NixOS 的 rootfs 与 initrd 等文件，替换掉 Fedora 的 rootfs 以及 boot 分区中对应的文件，结果发现就能正常启动了！进一步排查确认到，我 6 月份生成的 NixOS rootfs 无法启动的原因是：
    - 我使用了 opensbi 的主线代码编译出的 opensbi，而 LicheePi 4A 的 TH1520 核心需要使用它 fork 的分支
    - 此外我生成的 img 镜像，分区也存在问题，root 分区的大小不对劲。
  - 有读者在 NixOS Discourse 上询问我是否会考虑在 Patreon 上创建一个赞助页面，再加上之前已经有老外赞助了我 $50 刀，我于是在 GitHub 个人页面以及项目中都新增了 Patreon、buymeacoffee、爱发电与 Ethereum Address 等赞助链接。
    - 截止 2023 年底，Patreon 共收到赞助 $10 刀，buymeacoffee 收到赞助 $35 刀，爱发点收到赞助 ￥25 元，以及加密货币收到赞助 $50 刀。
      {{<figure src="/images/now/nixos-patreon_the-first-member.jpg" title="Patreon Messages" width="80%">}}
      {{<figure src="/images/2023-summary/buymeacoffe_earning-2023-12-13.webp" title="Buy Me a Coffee - Earning" width="80%">}}
  - 写下新文章 [人生已过四分之一](https://thiscute.world/posts/a-quarter-of-the-way-through-life/)，回顾我到目前为止的人生，以及对未来的展望，挺多感想。
  - 在 [@Manjusaka_Lee](https://twitter.com/Manjusaka_Lee) 的熏陶下，我也整了一个新的邮箱地址 ryan4yin@linux.com。先给 Linux Foundation 捐 \$99，然后再付 \$150 就能得到这个终身邮箱地址。
    - 一是用了这么久 Linux 也该捐点钱，二是感觉这个邮箱很酷！
  - 因为一些心态上的变化，开始参加一些公益活动，比如说加入了「恒晖公益月捐」活动，每月捐 300 块。
  - 在 chainsx 的帮助下，成功在 rock 5a 跟 orange pi 5 plus 两块板子上把 NixOS 跑了起来。
- 9 月
  - 临时起意看了个午夜场的《奥本海默》，IMAX 巨幕。给个 4 星没问题吧，演挺好的，原来美共曾经有这么多美国高级知识分子，这是我以前不了解的。
  - 前几天跟妹妹聊时，她引用了我看的小说里的一句话，然后我看「仿生狮子」兄的荐书时发现，这一句就是《山月记》的摘抄，药哥说他也看过这书，挺好。当时就下单了，今天书到了，决定读一读。
    - 读了第一个短篇，最知名的《山月记》，更类似一个寓言故事，最有韵味的就是那一句「**深怕自己并非明珠而不敢刻苦琢磨，又自信有几分才华，不甘与瓦砾为伍。日渐避世离俗，心中自卑怯懦之自尊终在愤懑与羞怒中愈发张狂。世人皆为驯兽师，猛兽即个人性情**。」
      {{<figure src="/images/now/2023-09-02_midi-keyboard.webp" title="MIDI 键盘、山月记、以及凌乱的桌台..." width="100%">}}
  - 跟朋友聊到陈行甲老师，他给我分享了深慈联《2023 年第二期慈善大讲堂》（报道见 [“坚守初心，笃行致远”，深慈联举办2023年第二期慈善大讲堂](https://new.qq.com/rain/a/20230821A06QDX00)）的视频，看上去分享者与与会者年龄段主要在 40+ 到 50+，他们看待问题的角度跟我们年轻人完全不同，陈行甲老师以及肖兴萍老师的演讲都干货满满，很有收获。
  - 请半天假去看了中国国际光博会，看到了挺多新鲜的东西，像啥气动开关啊、光波导眼镜啊、高能量密度的锌空电池充电包啊、中科院光电所的两台小光刻机啊、长春光机所的空间站小机械臂啊、以及压电陶瓷驱动技术的各种应用，长了见识。
  - 看了些 NixCon 2023 的视频，挺有意思。而且发现所有视频都有一只招财猫在讲台上哈哈。
  - 最感兴趣的内容是这个 - [NixCon2023 Bootstrapping Nix and Linux from TinyCC](https://www.youtube.com/watch?v=Gm8yrvbgY-Y)
  - 看了记录片 [史蒂夫·乔布斯 Steve Jobs](https://movie.douban.com/subject/25850443/)，Jobs 简直是最差的丈夫、父亲跟同事，但他确实是最牛逼的设计天才（或许这两句都应该再加一个「之一」）。
  - 听了天依的新曲[《歌行四方 - 天依游学记》](https://www.bilibili.com/video/BV1Yp4y1j7jX/)，曲跟词都非常棒！完美融合了二次元跟三次元的各种传统音乐，天依的人物建模、服装设计跟渲染质量也提升了一个档次。 很多年前第一次听天依，感觉声音怪怪的，后来出了全息现场会，效果其实也挺差的，然后一步步地建模质量越来越好，人物越来越生动活泼，声音越来越自然，现在又走进了三次元，与传统音乐大师一起合奏。听下来真的很感动，有一种老父亲甚感欣慰的 feel.
  - 看了记录片 [史蒂夫·乔布斯 Steve Jobs](https://movie.douban.com/subject/25850443/)，Jobs 简直是最差的丈夫、父亲跟同事，但他确实是最牛逼的设计天才（或许这两句都应该再加一个「之一」）。
  - 听了天依的新曲[《歌行四方 - 天依游学记》](https://www.bilibili.com/video/BV1Yp4y1j7jX/)，曲跟词都非常棒！完美融合了二次元跟三次元的各种传统音乐，天依的人物建模、服装设计跟渲染质量也提升了一个档次。 很多年前第一次听天依，感觉声音怪怪的，后来出了全息现场会，效果其实也挺差的，然后一步步地建模质量越来越好，人物越来越生动活泼，声音越来越自然，现在又走进了三次元，与传统音乐大师一起合奏。听下来真的很感动，有一种老父亲甚感欣慰的 feel.
  - 了解了下 [世界法治指数](https://worldjusticeproject.org/rule-of-law-index/country/2022/China) 与 [中国各省份司法文明指数](https://www.cnfin.com/hg-lb/detail/20230425/3851364_1.html)
    - 湖南省貌似一直在倒数前二徘徊...很尴尬。
  - 今天看到推上有 MTF 说自己双相情感障碍（躁郁症），突然就想百度一下，进一步找到了注意力缺失障碍（ADHD）这个病，联想到我自己好像有这个问题。
      - 大学时曾经怀疑自己有这个注意力缺失症，还买了本《分心不是我的错》，但书买了一直没看（我整个大学期间都不太看得下书），但没去医院看过。
  - 中秋国庆连休
    - 看完了《被讨厌的勇气》，觉得它虽然缺乏科学依据，但这套理论得确实很好，给我很大启发。
    - 看了一点《这才是心理学》
    - 带我妹使用 ESP32 练习 C 语言，兴趣导向。玩了用 5x5 的 WS2812 彩灯模块写跑马灯、红绿灯之类的小程序，她还非要用 SSD1306 小屏幕显示个「原神启动」，搞得挺开心 emmm
  - 突然对 FPGA 燃起了兴趣，在 HDLBits 上刷了许多 Verilog 入门题。
- 10 月
  - 读完了《叫魂：1768 年中国妖术大恐慌》
  - 看了记录片《溥仪：末代皇帝》跟电影《末代皇帝》，两个片子的内容有些出入，不过这边的史料显然可信度更高，都好评。
  - 我的开源小书 NixOS & Flakes Book 上了 Hacker News 热门，很开心：[NixOS and Flakes Book: An unofficial book for beginners (free)](https://news.ycombinator.com/item?id=37818570)
  - 之前跟朋友聊过我可能有注意里缺失障碍（ADHD），朋友提到可以去看看医生。国庆后经 [@咩咩](bleatingsheep.org/) 再次提醒，约了深圳康宁医院（深圳市精神卫生中心）的特需门诊，然后确诊，开始服药治疗...
    - 跟 0xffff 群友辩论 ADHD 病症相关问题，讨论的内容逐渐发散 - [从 ADHD 注意力缺失症聊开去](https://0xffff.one/d/1643-cong-adhd-zhu-yi-li-que-shi-zheng) 
  - 遵医嘱，搜了些正念冥想的资料，看了点 [正念减压疗法创始人-乔.卡巴金 教正念冥想大师课（中英字幕）](https://www.bilibili.com/video/BV19y4y1V7RU)，尝试了下还有点意思。
  - 跟我妹沟通后感觉她也比较有可能有 ADHD，提前安排她来深圳看心理医生。我妹确诊了抑郁症 + ADHD，医生给开了安非他酮，先吃半个月看看效果再复诊，同时也建议多带我妹出去运动散心。
    - 我妹确诊抑郁症这一点真的让我很意外，让我意识到我一直有些忽视她的心理健康问题。
  - 我确诊 ADHD 并开始用药之后心态有很大的变化，我妹确诊抑郁症又给了我很大的触动。我完全放下了所有技术上的业余爱好，工作上专心工作，业余时间更多地花在了关心家人、运动、学习心理学等事情上。
- 11 月
  - 持续服药治疗以及复诊，确诊后这段时间是我印象中工作效率最高的一段时间，治疗挺有成效。
  - 给我妹买往返火车票、学校请假、预约医生、带她在深圳到处玩。
  - 有挺长一阵没怎么碰电脑了，最近发现我的 NixOS 总是启动没多久网络就会卡死，为了解决问题，我重装了 NixOS 系统，顺便给系统添加了 LUKS 全盘加密 + Secure Boot + impermanence，根卷换成了 tmpfs，因此任何未显式声明持久化的数据，每次重启系统都会被清空。优雅，太优雅了！
    - 重装好系统后网络问题就消失了，猜测是 home 目录有什么 X Server 相关的配置文件有毛病导致的。
- 12 月
  - 沉寂一个多月的对业余项目的兴趣回来了一点，对 NixOS 相关的几个项目做了一番更新。
  - 工作电脑用满三年换新了，新电脑是 Macbook Pro M2，终于用上了 M 系列的 CPU，体验显然比之前的 Intel 版本好很多，不发热了风扇也不响了，续航知道很牛但没啥机会测试。
  - 淘汰下的旧工作电脑给装了个 NixOS，体验还不错，有些小问题但勉强能忍受。
    - 主要问题：Touchbar 跑着跑着会失灵，Touch ID 无法使用，盖上盖子会直接关机，触摸板比较容易误触。其他的体验都挺不错的，第一次在笔记本上用 NixOS，还挺新奇的。
  - 学习 Guile Scheme 以及 nushell，打算后面大量使用这俩语言整些活，Python 脚本有点写腻歪了。
  - 年底确实也缺乏些动力，更多的时间花在了娱乐上。

## 2023 年 Highlights

### 1. 业余技术

技术方面我今年的进展还是挺大的，但跟去年写的展望几乎没啥关联，人生总是充满了意外哈哈...

今年的主要技术成就基本完全集中在 NixOS 这一块，如下几个新项目都或者了很多好评（统计数据截止 2023/12/26）：
- [ryan4yin/nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book): 这本开源小书的仓库于 2023/6/23 创建，目前获得了 23 位贡献者，908 个 stars，以及 4 位国外读者的共计 $70 零花钱赞助，成为了我目前 stars 数最高的项目。它的文档站目前稳定在每天 150 UV.
- [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config): 这份 NixOS 系统配置仓库于 2023/4/23 创建，目前获得了 290 个 stars.
- [ryan4yin/nix-darwin-kickstarter](https://github.com/ryan4yin/nix-darwin-kickstarter): 我于 2023/7/19 创建的一个 Nix-Darwin 模板仓库，目前 129 stars.
- [ryan4yin/nixos-rk3588](https://github.com/ryan4yin/nixos-rk3588): 这是我在 2023/6/4 创建的一个 NixOS 移植项目，目前支持了三块 RK3588 开发板，获得了 46 stars.

- [ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a): 同样是一个 NixOS 移植项目，但目标是基于 RISC-V 指令集的 LicheePi 4A 开发板，断断续续花了两个月才搞定移植工作（用时远超预料...不过成功后获得的成就感也是巨大的）。目前获得了 3 位贡献者与 23 stars，其中一位贡献者还赞助了 $50 给我。

对比下从 2023 年 1 月 1 日到现在，我的 GitHub Metrics 统计数据：

{{<figure src="/images/2023-summary/2023-01-01-github-metrics.svg" attr="2023/01/01 GitHub 统计数据" attrlink="https://github.com/ryan4yin/ryan4yin/blob/f58f1769a72289b44e5313eaed3bbfc21febebda/metrics.classic.svg">}}

TODO: update images & links
{{<figure src="/images/2023-summary/2023-12-31-github-metrics.svg" attr="2023/12/31 GitHub 统计数据" attrlink="https://github.com/ryan4yin/ryan4yin/blob/master/metrics.classic.svg">}}

几个关键指标的变化：

- Stars: 12 => 2044, 涨幅 555%.
- Followers: 152 => 468, 涨幅 208%.
- Forkers: 97 => 201, 涨幅 107%.
- Watchers: 39 => 102, 涨幅 161%.

在折腾 NixOS 的过程中我做的开源项目、入门指南获得了国内外社区的大量好评，认识了好几位国内外的 NixOS 资深用户与嵌入式开发者，还收到了一些外国读者的打赏，[nixos-and-flakes-book](https://nixos-and-flakes.thiscute.world/)，在 NixOS 国际社区获得了大量好评，给我带来了巨大的成就感以及社区参与感！这完全契合了我年初给自己的期许——「**认识更多有趣的人，见识下更宽广的世界**」。

今年不仅给 AstroNvim, ESP-IDF 等知名项目贡献了少许代码，甚至还创造了这么多个受欢迎的新项目，且收到了几十个 PR。之前定的给一些开源项目贡献代码的目标，完全是超额完成了。

总的来说，业余技术今年搞到这个程度，相比去年，能称得上是「优秀」、「超出预期」。

### 2. 工作


工作上只能说马马虎虎，上半年业余在 NixOS 上做的成果得到了非常多的认可，相当有成就感，花了大量的精力在 NixOS 上，也创建了许多相关项目。但另一方面，精力就这么多，我也一直做不到平衡好工作与生活/业余爱好，其结果就是那段时间没啥心思在工作上，把工作搞得一团糟。
当时觉得自己进入了一个瓶颈期，在工作上找不到什么成就感，业余爱好做出了不错的成绩，但又不能靠这个吃饭。

在折腾业余爱好期间，一种找不到方向的焦虑感也一直萦绕着我，有跟一些朋友、同事沟通过这个问题，但大道理谁都懂，真要做起来又是另一回事了。
因为业余搞了些嵌入式硬件感觉有意思，也有隐约考虑过转行搞硬件，但只是些粗浅的想法。
到 8 月份的时候，因为做了一些 NixOS 项目收到几笔赞助，让我可能有点异想天开？了解了些「如何通过开源项目养活自己」类似的信息，8 月中下旬的时候在苏洋的折腾群里提到这个想法，被洋哥泼了冷水 emmm 冷静下来后回想，洋哥说的挺在理的，靠开源用爱发电真能养活自己的凤毛麟角，如果专门往商业项目的方向做，又没了那份折腾的快乐了。

8 月底的时候，苏洋的折腾群里发起一场自我介绍活动，读了许多群友的自我介绍，把我自己在群里发的自我介绍扩写了下，就成了这篇文章 [人生已过四分之一](https://thiscute.world/posts/a-quarter-of-the-way-through-life/)。

当时觉得自己想明白不少，也跟领导同事做了些沟通，工作上状态有所好转，但还是没能完全回到正轨，当时觉得人生可能就是这样永远在这样未知的道路上的挣扎着前进了，也有痛苦，也有快乐。

转折点是国庆后，咩咩催促我去看心理医生，确诊了 ADHD 并开始服药后，我的工作效率才有了质的提升，这也是我今年最大的收获之一。

总体上，我今年的工作做得比去年差，尤其是上半年，我给自己的评价是「及格」。

### 3. 生活

#### 1. 确诊 ADHD 以及治疗

8 月份通过 [我的四分之一人生](https://thiscute.world/posts/a-quarter-of-the-way-through-life/) 做了一个人生回顾后，虽然感觉自己想明白不少，但实际工作上还是很难集中注意力，分心的情况仍然相当严重。
也尝试了通过番茄钟之类的方式来提高工作效率，但效果不佳。

直到国庆后[@咩咩](bleatingsheep.org/)催促我去看心理医生，确诊了 ADHD 并开始服药后，我的工作效率才有了质的提升。
于是我搞明白了，原来我一直以来的注意力问题，并不是什么品格或者意志力问题，而是一种可以治疗的病症。

考虑到 ADHD 的遗传特性，跟妹妹、父母一番沟通后，带我妹来深圳看医生，确诊了 ADHD 以及抑郁症。
说真的，我一直知道我妹妹情绪比较敏感，但从没想过是因为抑郁症。

这之后，除了工作外，我大部分的精力都花在了关心家人、运动、学习心理学等事情上，技术上的东西放下有一阵子了。

#### 2. 参与公益活动

因缘际会跟 [@Manjusaka_Lee](https://twitter.com/Manjusaka_Lee) 聊到了公益，当时在工作上缺乏动力，想在其他的事情上找找感觉，公益本身也是一件很有意义的事情，那段时间学习了解了许多公益资料，参加了一些公益会展与捐款活动，还一度考虑做志愿者。

#### 3. 阅读与写作

首先是我 2023 年的读书记录：

- 2023-03-09 - The Moon and Sixpence
  - 你是要地上的六便士，还是要天上的月亮？
- 2023-08-31 - [How to Do Great Work - Paul Graham](http://www.paulgraham.com/greatwork.html)
  - 黑客与画家一篇两万多字的长文，也算是一本小书了吧，干货满满。
- 2023-09-29 - 《被讨厌的勇气》
  - 一本通过对话的形式讲述阿勒德心理学的书，这门心理学与现代科学心理学不同，它更偏向哲学。
- 2023-10-08 - 《叫魂：1768 年中国妖术大恐慌》
  - 从 1768 年的叫魂案出发，分析了乾隆时期的中国社会的许多方面。比如因各种原因导致人口过度增长、人均资源减少、社会矛盾激化导致的普遍恐慌，以及官僚君主制的运作机制、存在的问题。此书以史为鉴，能帮助我们理解现代中国政治与中国社会的一些基本问题。
- 2023-10-17 - 《分心不是我的错》
  - 介绍 ADHD 的一本书，列举了很多 ADHD 案例，也给出了诊疗建议，对我相当有用！

以及一些未读完的书：

- 《这才是心理学 - 看穿伪科学的批判性思维 第 11 版》
- Psychology and Life, 20th edition, by Richard J. Gerrig
- The Great Gatsby - 10/41
- 《复杂 - 梅拉尼 米歇尔》
- [Linux Device Driver Development - Second Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition): Linux 驱动编程入门，2022 年出的新书，基于 Linux 5.10，amazon 上评价不错，目前只有英文版，写的很好，对新手很友好。

2023 年我读的书籍数量不多，没达成每月读一本书的目标。
而写作方面，算上这篇总结，今年我一共写了 9 篇博文，也没达成每月写一篇的目标。

但鉴于我今年写了一本挺受欢迎的小书 [NixOS & Flakes Book](https://github.com/ryan4yin/nixos-and-flakes-book)，它得到了 NixOS 社区诸多好评，上了 Hacker News 热榜，甚至被官方文档列入推荐阅读，我姑且将今年「阅读与写作」这一项的评分定为「超出期待」！

#### 3. 其他

1. 运动方面乏善可陈，穿越了一次东西冲海岸线，游了几次泳，12 月初晨跑了一周但因为是空腹跑，胃炎给跑犯了，就没再跑了。体重全年都在 60kg 波动，没啥变化。
1. 给我老爸全款买了我们全家的第一辆小轿车（自己没买，一是天天坐地铁用不到，二是我对车也缺乏兴趣）。
2. 计划开始给父母约年度体检，待实施。

#### 4. 总结

生活上今年达成了这么多有意义的成就（确诊 ADHD、将更多精力花在关心家人上、参与公益活动、给家里买车等等），我给自己的评价当然是「优秀」。

### 4. 各种统计数据

首先是我的博客站点 <https://thiscute.world/> 的统计数据：


TODO: update images & links

{{<figure src="/images/2023-summary/thiscute.world-2023-google-analytics.webp" title="thiscute.world - 2023 年 Google Analytics 统计数据" width="100%">}}

{{<figure src="/images/2023-summary/thiscute.world-2023-google-search.webp" title="thiscute.world - 2023 年 Google Search 统计数据" width="100%">}}

另外是今年我新建的 NixOS 笔记站点 <https://nixos-and-flakes.thiscute.world> 的统计数据：

{{<figure src="/images/2023-summary/nixos-and-flakes-book-2023-google-analytics.webp" title="NixOS & Flakes Book - 2023 年 Google Analytics 统计数据" width="100%">}}

{{<figure src="/images/2023-summary/nixos-and-flakes-book-2023-google-search.webp" title="NixOS & Flakes Book - 2023 年 Google Search 统计数据" width="100%">}}

以及两个站点全年在 Vercel 上的流量统计：

{{<figure src="/images/2023-summary/vercel-2023-traffic.webp" title="Vercel - 2023 年流量统计" width="100%">}}

最后是文章阅读量 Top 10：

{{<figure src="/images/2023-summary/2023-top-10-posts.webp" title="2023 年文章阅读量 Top 10" width="100%">}}


## 2023 年展望

其实现在对明年反而没啥特别的期望，现在的状态就挺好的（这大概就是「现充」吧 emmm）。
但总不能因为这个就摆烂，还是要给自己定一些目标，能否达成就看缘分了。

### 1. 技术侧

首先是前几年就定的一些目标，但一直没实现的：

- 云原生
  - 2021 年定的阅读 k8s 及相关生态的源码，两年了没任何进度，2024 年继续…
- Linux 与网络
  - 2022 年看了一半《Linux/Unix 系统编程手册 - 上册》，2023 全年没动这本书，2024 年总该看完了吧...
  - MIT6.S081 Operating System Engineering (Fall 2020) 之前定了个目标学一遍但完全没开始，2024 年继续...
  - 学习学习时下超流行的 eBPF 技术
- 编程语言
  - 2023 年 Go/C 两项语言也算是写了一点吧，2024 年期望提升些代码量，熟能生巧。
  - 2024 年对 Scheme/Nushell/Rust 都比较感兴趣，其中 Scheme/Nushell 都是挺简单的语言，希望能在新的一年里用它们整些活。Rust 偏复杂，有应用机会的话也搞一搞。

然后是今年新增的一些目标：

- 2023 年既然意外地点亮了 NixOS 这项技能点，希望 2024 年能继续深入学习 NixOS 与 Nix 生态，争取为 NixOS 社区做更多的贡献（也可以搞一搞 Guix）。
- 2024 年在 EE 与嵌入式方面，也希望能更深入些，设计一点自己的板子玩玩，做点有意思的东西，比如无人机啊、智能机械臂啊啥的。

### 2. 生活侧

生活上，2024 年希望能：

- 首先仍然是每年固定的目标：每月读一本书、写一篇博客。
- 旅游：带家人至少出省旅游三次。
- 运动：还是想尝试下晨跑，但不要空腹跑，胃炎犯了很难受。
- 音乐：今年买了个 Quest 3 VR 头显，它有个 AR 弹琴的游戏挺不错，希望 2023 年能借此学会些简单的钢琴曲。

## 结语

2022 年的年终总结文末，我给自己 2023 年的期许是「**认识更多有趣的人，见识下更宽广的世界**」，感觉确实应验了。

那么在 2024 年，我希望自己能够「**工作与业余爱好上稳中求进，生活上锻炼好身体、多关心家人**」~


