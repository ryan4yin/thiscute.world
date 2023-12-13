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
      ![](/images/now/nvme-critial-medium-error.webp "2022-11-02 翻车记录，系统无法启动")
      ![](/images/now/nvme-device-not-ready.webp "2023-02-03 翻车记录，系统能启动但是文件损坏")
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
  - 在业余爱好上投入的精力越来越多，工作上相对的越来越懈怠，感觉碰到了瓶颈，但搞不明白该怎么突破。
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
    {{<figure src="i3_2023-07-29_1.webp" width="100%">}}
  - 在新主机上成功复现出我的 NixOS 环境后，紧接着发布了我的系统配置 [ryan4yin/nix-config/v0.0.2)](https://github.com/ryan4yin/nix-config/releases/tag/v0.0.2) 以及这大半个月的学习笔记 [NixOS 与 Nix Flakes 新手入门](https://thiscute.world/posts/nixos-and-flake-basics/)，然后事情就变得越来越有趣起来了！随着读者的反馈以及我对它的不断迭代，这份学习笔记逐渐膨胀成一篇一万多字的博文，并且有了中英双语，然后又转变成一本开源书藉 [nixos-and-flakes-book](https://nixos-and-flakes.thiscute.world/)，在 NixOS 国际社区获得了大量好评！截止 2023-12-13 本书的 GitHub 仓库已经有了 848 stars，是我目前 stars 最多的仓库，它给我带来了巨大的成就感以及社区参与感。我在社区发布的相关帖子：
    - [[2023-05-11] NixOS & Nix Flakes - A Guide for Beginners - Reddit](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/)
    - [[2023-06-22] Updates: NixOS & Nix Flakes - A Guide for Beginners - Reddit](https://www.reddit.com/r/NixOS/comments/14fvz1q/updates_nixos_nix_flakes_a_guide_for_beginners/)
    - [[2023-06-24] An unofficial NixOS & Flakes book for beginners - Discourse](https://discourse.nixos.org/t/an-unofficial-nixos-flakes-book-for-beginners/29561)
    - [[2023-07-06] This isn't an issue but it has to be said: - Discussions](https://github.com/ryan4yin/nixos-and-flakes-book/discussions/43)
    - [[2023-05-09] NixOS 与 Nix Flakes 新手入门 - v2ex 社区](https://www.v2ex.com/t/938569#reply45)
    - [[2023-06-24] NixOS 与 Flakes | 一份非官方的新手指南 - v2ex 社区](https://www.v2ex.com/t/951190#reply9)
    - [[2023-06-24] NixOS 与 Flakes | 一份非官方的新手指南 - 0xffff 社区](https://0xffff.one/d/1547-nixos-yu-flakes-yi-fen-fei-guan)
  - 在 NixOS 上尝试了 i3 与 Hyprland 两个窗口管理器，并且使用 agenix 管理了系统中的敏感信息，比如密码、私钥、wireguard 配置等。
- 6 月
  - 立了个 flag - 把 NixOS 移稙到我手上的两块开发版上跑起来，一块 ARM64 架构的 Orange Pi 5，以及另一块 RISC-V 架构的 LicheePi 4A.
    - 花了好几天时间研究，在俄罗斯网友的耐心帮助下，终于在 6/4 晚上在 Orange Pi 5 上把 NixOS 跑起来了，还挺有成就感的（虽然现在也不知道拿这板子用来干啥...）
    - 之后断断续续折腾了一个月的 NixOS on LicheePi 4A，试了很多方案，还请教了 [HougeLangley](https://github.com/HougeLangley)、[@nickcao](https://github.com/NickCao)、[@chainsx](https://github.com/chainsx) 等大佬，学会了很多 Linux 相关的东西，费尽千辛万苦终于成功把 rootfs 编译出来了，但死活引导不成功。感觉是 uboot-spl 跟 boot 分区这两个地方的内容有问题，但不知道怎么解决，累觉不爱。
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
      {{<figure src="/images/now/2023-08-05-sending-me-$50-for-fun.webp" width="70%">}}
  - 排查问题的方法：首先刷好一个可在 LicheePi 4A 上正常启动的 Fedora 系统，然后用我编译出的 NixOS 的 rootfs 与 initrd 等文件，替换掉 Fedora 的 rootfs 以及 boot 分区中对应的文件，结果发现就能正常启动了！进一步排查确认到，我 6 月份生成的 NixOS rootfs 无法启动的原因是：
    - 我使用了 opensbi 的主线代码编译出的 opensbi，而 LicheePi 4A 的 TH1520 核心需要使用它 fork 的分支
    - 此外我生成的 img 镜像，分区也存在问题，root 分区的大小不对劲。
  - 有读者在 NixOS Discourse 上询问我是否会考虑在 Patreon 上创建一个赞助页面，再加上之前已经有老外赞助了我 $50 刀，我于是在 GitHub 个人页面以及项目中都新增了 Patreon、buymeacoffee、爱发电与 Ethereum Address 等赞助链接。
    - 截止 2023 年底，Patreon 共收到赞助 $10 刀，buymeacoffee 收到赞助 $35 刀，爱发点收到赞助 ￥25 元，以及加密货币收到赞助 $50 刀。
      {{<figure src="/images/now/nixos-patreon_the-first-member.jpg" title="Patreon Messages" width="80%">}}
      {{<figure src="buymeacoffe_earning-2023-12-13.webp" title="Buy Me a Coffee - Earning" width="80%">}}
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
  - 有挺长一阵没怎么碰电脑了，最近发现我的 NixOS 总是启动没多久网络就会卡死，为了解决问题，我重装了 NixOS 系统，顺便给系统添加了 LUKS 全盘加密 + Secure Boot + impermanence.
    - 重装好系统后网络问题就消失了，猜测是 home 目录有什么 X Server 相关的配置文件有毛病导致的。
- 12 月
  - 沉寂一个多月的对业余项目的兴趣又逐渐回来了，但也对我当前的工作状态产生了一些负面影响，希望能将它控制在一定范围内，可别再像以前那样严重影响工作了。

