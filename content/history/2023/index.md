---
title: "曾经的我 - 2023"
date: 2023-01-01T14:14:35+08:00
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

> Twitter 上 @Manjusaka_Lee 等大佬喜欢写周报，不过我不太喜欢周报的形式。因为周报的标题本身没啥意义，而要看其中的内容却得一个个点进去看，这对我自己回顾过往的学习、工作、生活，体验非常不方便。
> 我比较喜欢类似「一镜到底」的阅读体验，所以我采用这种单页的方式来记录我的日常。（基于同样的理由，我将博客单页展示的文章数量上限调整成了 `1000`）

全部历史记录：[/history](/history/)

### 2023-12-30 - 2023-12-31

- 因为 Guix 推荐使用 Emacs 作为主力编辑器（都是 Lisp 圈子的），加之在 Neovim 上没找到好用的 Guix/Scheme 插件，装了个 doom-emacs 开始了 emacs 折腾之旅。
- 带我妹来深圳复诊，顺便玩。
    - 逛了深圳 AD01 动漫展。第一次逛漫展，体验挺不错的。
    - 到大梅沙看了看大海。小孩比例超高，又比较热，体验差了点。大鹏那边会好玩很多，但太远了。

### 2023-12-28 - 2023-12-29

- 已经完全适应了将 zellij+neovim 用做默认开发环境，体验非常棒！
- 业余继续尝试折腾 Guix 系统，遇到了 Scheme 语言、Guix 配置、构建速度慢等各种问题，都一一解决了，记了些笔记。
    - https://github.com/ryan4yin/guix-config

### 2023-12-27

- 了解了下 Helix 插件系统，试用时发现 Helix 也没内置的终端功能，相关 Issue 讨论中发现挺多用户习惯使用 tmux/zellij 作为日常的终端环境。联想到我最近在使用 kitty/wezterm 时发现它们的搜索/终端历史选择复制等功能上存在的诸多欠缺，而 Neovim 里我目前主要使用的 toggleterm.nvim 插件也日常导致 neovim 卡死，瞬间就对将 zellij 作为日常终端环境产生了兴趣。
    - 一番探究发现 Zellij 很优雅地解决了我在 kitty/wezterm/neovim 遇到的这些问题，而且速度很快，再者它在任何终端模拟器中都能提供一致的体验。以及最重要的是，它使用起来真的很简单，对新手相当友好，键位也很符合直觉！甚至跟 Neovim 一样也支持鼠标操作！
    - 晚上直接把 Neovim/kitty/wezterm 里面相关的配置与插件全部删掉了，并且在 nushell 中设置为自动启动 Zellij，终端环境全面替换成了 Zellij，体验下来非常舒适！（我确实得说，这体验跟 tmux 不是一个级别的，tmux 真的新手劝退，而且性能很差）
- Scheme 的语法跟 Guile 的文档都走马观花看了一遍，再次尝试折腾 Guix 系统。

### 2023-12-26

- 今晚研究了下 Guix Scheme 语言，打算好好学一学，再深入折腾下 Guix 系统。而且 eww 的配置文件也是 Lisp 系语言，Scheme 学了用得上，动力就比较足。

### 2023-12-25

- 晚上不知道有啥可干，跟 NixOS 群友聊了聊 nushell 的优势跟 bash 的垃圾，突然有想法把 NixOS 配置中的所有 shell 脚本全改造成 nushell，试用了 nuenv 来打 Nix 包，一试就搞到凌晨...也是各种踩坑的血泪教训，算是熟悉了下 nushell 以及 Nix 的打包环境。
    - 主要就是各种 Permission Denied 的错误，以前 bash 打包完全没遇到过，试到凌晨才搞明白，貌似 Nix 打包中的 source 文件都是只读的，另外 $out 中的内容也是一旦写入后就无法修改的，至少用 nushell 是这样。我因为尝试直接改 source 文件，或者在 $out 中改文件，就一直 Permission Denied 到哭...

### 2023-12-24

- 周末这两天尝试把 NixOS 在 Macbook Pro 2020 上装起来了，500G 的磁盘分了 300G 给 NixOS. 使用体验还不错，主要大冬天的可以在床上折腾 NixOS 了。
    - 安装过程中遇到的主要问题
        - 因为我几张 TF 卡的读写速度都比手上的 U 盘快，之前折腾开发板也习惯了用 TF 卡加读卡器来装系统，结果 macOS 死活识别不了，最后还是换成我的垃圾 U 盘，才成功识别到...
        - 一开始过于自信，直接尝试在 U 盘的 LiveOS 系统上一次性安装我的整个 NixOS 配置，结果内核编译报错重试好几次，重试好多遍搞了大半夜，最后放弃了... 第二天老老实实整了个 minimal 的 flake 配置，结果搞好几个小时还是编译不过 kernel，各种重启进 Live OS、挂载硬盘、加载 WiFi 驱动、通过难用得要死的 wpa_cli 连接 WiFi，再部署 NixOS 配置，这套流程一晚上不知道走了多少遍，我 WiFi 密码都输麻了...
        - 最后直接换成了 NixOS 的 mainline latest kernel 才一次安装成功，重启进入系统后再部署我完整的 NixOS 配置 + Apple T2 定制 kernel，很顺利就成功了！感动！
        - 所以说系统安装也还是搞个 stage1 stage2 这样两步安装最省心哪，不要老想着一步到位。

### 2023-12-21

- 完成了数据上报网关及对应 EKS 集群的的升级，加了许多新特性，但总体升级还挺顺利的。一个总体接近 500 万连接的网关，折腾起来还是挺有成就感的。
    - 开始做实际的迁移工作与回话之前，想得还不是很清楚，心里是没底的。但实际把前期工作、迁移规划与验证做好后，真正开始迁移工作时，又觉得这没啥难的。
- 继续对新电脑的 Nix 配置做了些调整，更新了下 NixOS 入门小书的部分内容。
- 继续研究在 Macbook Pro 2020 上安装 NixOS.

{{<figure src="/images/now/2023-12-21_nixos-and-flakes-book-888-stars.webp" title="NixOS 入门小书 888 stars 了，截图纪念一下" width="80%">}}


### 2023-12-20

- 继续做数据上报网关的升级迁移工作，今年 roadmap 中的核心工作，算上这个就都搞定了，心里感觉很踏实。
    - 今年工作状态一度挺糟糕，10 月份确诊 ADHD 是个转折点，之后的工作状态就有了非常大的改善，这也是我今年最大的收获之一。
- 新电脑到手了，仍然是换了台库存二手机，Macbook Pro 2022 M2 16G. 但库存机有个好处就是，很快就能换新 emmm 这台电脑用到 2023/8 就又能换台新的了。
    - 尝试在新电脑上部署我的 nix-darwin 配置，遇到些问题，但总体挺顺利的，之前在旧办公电脑（Macbook Pro 2020 I5 16G）上使用的 nix 配置基本没改几行代码，就能直接在这台新 M2 上用
        - 总结下，主要的修改就是把 system 参数从 x86_64-darwin 改成 aarch64-darwin，以及 nixpkgs 中的 gdb 不支持 aarch64-darwin，把它排除掉，然后就没啥问题了。
- 旧的 Intel 版 Macbook 以后就放家里当床上电脑用了，考虑装个 NixOS，晚上看了点在 Macbook Pro 2022 I5 16G 上装 NixOS 的文档：<https://github.com/NixOS/nixos-hardware/tree/master/apple/t2>

### 2023-12-19

- 写年终总结，每天想起来就写一点点，基本写完了，偶尔有些想法再补充点，就等着年末发出来了。
- 最近几天又开始折腾 NixOS，更新了一波 ryanyin/nix-config，深入学习了下 NixOS 的模块系统，并在 NixOS & Flakes Book 中更新了相关的学习笔记。
- 给老妹买了往返车票，元旦期间来深圳玩，顺便去医生那复诊。她提到安非他酮现在副作用还是有点大，吃了犯恶心、心跳快，这次看医生可能得考虑下换药。
- 前段时间比较忙的活干差不多了，而且我吃专注达其实也有点副作用，最近就停了一周多药，立马吃麻麻香...工作状态也还可以，毕竟最近工作也不是很忙。
- 突然想到办公电脑可能快用满三年了，问了下 PeopleOps 说 11/23 就满三年了，于是开心地提了电脑换新的申请。

### 2023-12-11

- 上周尝试了提前一小时到公司旁边的公园晨跑，但没跑几天就胃炎就变严重了。考虑到可能是空腹晨跑导致的问题，停了两天，饮食啥的立马又生龙活虎。所以结论是空腹晨跑真的伤胃。
- 打算后面要么早上吃点早餐再跑，要么就晚上跑步或者打打 VR 吧。

### 2023-11-30 - 2023-12-09

- 开始每天早起一个小时，到离公司不远的公园晨跑，运动完在公司冲个凉再吃早餐，倒是惬意。
- 12/02 - 12/09: 更新我的 nix-config，解决了因使用 nushell 带来的环境变量丢失，从而引发的一系列问题。调整优化 neovim 配置，解决 terminfo 相关问题。
- 12/05 - 12/09: 更新 nixos-and-flakes-book，升级到 NixOS 23.11，并添加了一些新内容。
- 明显感觉到沉寂一个多月的对业余项目的兴趣又回来了，但也对我当前的工作状态产生了一些负面影响，希望能将它控制在一定范围内，不要再想以前那样严重影响工作了。
- 说是要学心理学，其实最近一个多月，工作状态确实非常好，但业余时间是真没学啥东西，心理学也很久没读了。

### 2023-11-25 - 2023-11-28

- NixOS 系统最近总是启动没多久网络就会卡死，重装了 NixOS 系统并添加了 LUKS 全盘加密，问题就消失了，猜测是 home 目录有什么 GUI 相关的配置文件有毛病导致的。
    - 之前的问题：
      - 系统启动没多久网络就会卡死，但除网络之外其他的都正常。
      - 测了 X11 / Wayland 都有一样的问题，但是退出 X11 / Wayland 切换到 TTY 后，网络就恢复正常了。
      - dmesg / journalctl 都没找到啥有用的信息。
    -  新的 NixOS+BTRFS 全盘加密方案文档及配置：<https://github.com/ryan4yin/nix-config/tree/nixos-install>
- 跟朋友聊了 BTRFS 与 LUKS 加密相关的信息，他提到了 Secure Boot + TPM2 + FIDO2 + LUKS + Recover Key 的方案，这应该是目前最安全的方案了，打算有空研究下。
    - NixOS + Secuer Boot 的配置方法：<https://github.com/nix-community/lanzaboote/blob/master/docs/QUICK_START.md>
    - 在 NixOS 上使用 TPM2 自动解锁 LUKS 的配置方法待研究。
- 后面打算逐步把 Homelab 所有物理机都改成全盘加密方案，同时所有数据盘 / 备份盘也都改成 LUKS 加密，全面强化数据安全。

### 2023-11-13 - 2023-11-24

- 工作上效率挺高，上班时间沉迷工作无法自拔...
- 2023-11-18 - 2023-11-19 带我妹到处玩玩，复诊。安非他酮我妹吃着效果


### 2023-11-14

- 最近一周都没干什么，业余打了打重新开服的节奏大师手游、玩了玩 VR、看了点小说。
- 复诊时医生说我用药已经比较稳定了，后续可以直接走简易门诊拿药，不需要专门挂 ADHD 的门诊号了（毕竟也挺难抢）。
- 跟我妹保持沟通，约了下周复诊的门诊，也买好了往返车票。

### 2023-11-06

- 妹妹他们早上到家了，她说心情仍旧不错，让我感觉到只要我能带她多玩玩，谈谈心聊聊天，这个抑郁症不难治。ADHD 方面我也很期待她吃药后的表现。
- 感觉从 10/15 确诊 ADHD 开始，我身边的一切都好起来了，妹妹确诊抑郁症也意味着以往的很多问题都有解决方案了，我也很开心！

### 2023-11-02 - 2023-11-05

- 11/2 晚上到高铁站接妹妹跟爸爸
- 11/3 带我妹看心理医生，顺便在岗厦北等几个地铁大站点玩了玩。我妹确诊了 抑郁症 + ADHD，医生给开了安非他酮，先吃半个月看看效果再复诊，同时也建议多带我妹出去运动散心。
- 11/4 特种兵游玩，上午在一个海边公园玩，下午跟几个在深圳的伯父堂弟到爬凤凰山，晚上也是聚会。
- 11/5 带我妹到壹方城玩了一个上午，看各种书店杂货店里的二次元周边，她说玩得非常开心！一路各种哇喔哇喔（这就是大城市啊）
    - 晚上送妹妹跟老爸坐火车硬卧回家，也约好了医生 11/19 的复诊。

### 2023-10-30

- 复诊，医生给加了安非他酮，跟专注达一起吃了几天，确实效果更好。体验上新加的安非他酮使我心情更愉悦、行动力更强。
- 给我妹预约好了心理医生，买好了她跟我爸从老家到深圳的往返车票。

### 2023-10-28 - 2023-10-29

- 因为我自身确诊了 ADHD，我一方面在研究考虑带我妹来深圳确诊（她的症状也比较明显），另一方面在学习各种 ADHD 跟心理学知识。今天偶然查到 ADHD 在认知神经科学方面的资料，对这门学科产生了兴趣。
- 发现知乎上这方面的资料挺不错，质量很高。从中收集了几本神经科学的入门教科书（英文），也查到了点相关的公开课视频，打算系统地学一学。

### 2023-10-20 - 2023-10-27

- 持续吃专注达，一天一颗。效果挺好，它不能解决所有问题，我仍然会经常想要打开手机的各种 APP 或者各种网页，但能够控制得住自己了。
- 体感上其实不太能确定这种自控力的提升是不是药物的功劳，因为以前我也有过这种类似「大彻大悟」的体验，两者不太好区分。但我确实感觉到最近两周是我工作状态最好的一段时间了。


### 2023-10-19

- 感冒症状，下午请半天假回家休息。
- 遵医嘱，搜了些正念冥想的资料，看了点 [正念减压疗法创始人-乔.卡巴金 教正念冥想大师课（中英字幕）](https://www.bilibili.com/video/BV19y4y1V7RU)，尝试了下还有点意思。

### 2023-10-16 - 2023-10-17

- 嗑药（专注达），效果很好，并且在持续记录自己的治疗状况。
- 10/17 看完了《分心不是我的错》，对我了解自身的 ADHD 病症很有帮助，我给了 5 星。
- 10/17 下班后，跟 0xffff 群友辩论 ADHD 病症相关问题，渐渐地聊到了人生的意义、道之类的东西，很有意思，我写个回复写到晚上快 2 点钟。
    - [从 ADHD 注意力缺失症聊开去](https://0xffff.one/d/1643-cong-adhd-zhu-yi-li-que-shi-zheng) 

### 2023-10-15

- 康宁医院的坪山院区，在辉辉那睡了一晚，第二天一早他开车送我去医院看诊，跟着我在医院呆了一整天，下午又把我送到地铁站。
    - 事实证明预约 VIP 门诊是一个明智的决定，因为普通门诊的病人会更多，不好占用医师太多的时间，而 VIP 门诊费贵十多倍（挂号费 400 + 初诊费 200），就诊病人少（但复诊有时候还是需要等一会儿），院区的各种检测也都完全不用排队。
    - 花了大概 40 分钟跟医生聊我的过往病史，医生说我的症状很典型。
    - 医生给开了各种检测，一共花了我自费 160，医保 800 + 843 + 599 + 50 = 2292。
        - 测验最重要的一部分是各种注意力、认知功能、眼动功能测验，一部分是对其他疾病的排除性检查，另一部分是确认身体各项指标是否正常以确保能安全服用专注达。
    - 最后医生给确诊了 ADHD 注意力缺失障碍，开了 14 片专注达（医保全报销 266 元），一天一到两片，另外建议我两周后复诊。
    - 医生也建议我做一些专注力训练，主要是拼图拼模型，以及正念冥想，还有就是阅读纸质书（强调翻页的这个动作、触感这些信息）。
- 晚上预约了同一个医生两周后（10/30 周一）的复诊，到时候再与医生沟通用药效果与下一步治疗方案。
- 为了尝试一下专注达的效果，晚上先吃了一片，打算从今天开始写 ADHD 治疗日记。

### 2023-10-14

- 打 VR 游戏
- 看了点《分心不是我的错》

### 2023-10-11 - 2023-10-13

- 打新买的 VR 游戏
- 之前跟朋友聊过我可能有注意里缺失障碍（ADHD），朋友提到可以去看看医生。这两天经 [@咩咩](bleatingsheep.org/) 再次提醒，预约了深圳康宁医院（深圳市精神卫生中心）的门诊。
    - 因为约不到「成人多动症专科门诊」，这两天有空就查一下医院的预约页，约到了同一个医生本周日（10/15）的「特需心理门诊（VIP Clinic）」。
    - 业余也看了些资料，越看越觉得我从小到大的各种毛病，都跟其症状很匹配。


### 2023-10-10

- steam 买了六七百块钱的游戏，包括艾尔登法环，然后玩了一晚上。

### 2023-10-09

- 继续读《置身事内》
- NixOS & Flakes Book 上 Hacker News 热门了，很开心：[NixOS and Flakes Book: An unofficial book for beginners (free)](https://news.ycombinator.com/item?id=37818570)
    - 被 HN 的网友吐槽站点的代码块配色跟换行问题很大，花了挺长时间排查修复（发现主要的锅是 vitepress 自身，有点后悔，当初可能选 docusaurus 更好些）。

### 2023-10-08

- v2ex 上总是不缺乏讨论人生意义的日经贴，找到一份古早的帖子，成年的梦想家们：[假如你不缺钱了，你会做件什么样的大事/有什么新的目标？](https://www.v2ex.com/t/345741)
- 上面简单的梦想太过乏味，知乎上的这篇 [如何找到人生目标](https://www.zhihu.com/question/20054842) 更具启发性。
- 读了 0xffff.one 站长的 [疫情后的一些思考](https://zgq.ink/posts/after-covid-19)，挺有感触。尤其是最近参与些慈善活动，又联想到欧美的社会公益做得比中国好了太多，中国的公益慈善体系还很青涩稚嫩。仔细想来，爱、平等、自由，甚至现代科学、社会主义，在这片土地上至今仍是外来文化，社会的发展转变需要时间，转变过程中的文化冲突、观念差异不可避免。
    - 期待整个社会一夜之间焕然一新不现实，而如果因此厌恶逃避甚至反过来嘲讽这一切，对我而言似也缺失了一些应有的担当。还是实事求是、脚踏实地做人做事吧，相信明天会更好。
- 又上班摸鱼看了这篇[当一位清华本硕博放弃“北京中产”，去往非洲 | 二湘空间](https://mp.weixin.qq.com/s/T1SdSwBAdpbvdnPuTxRN6Q)，有些观点我很认同。
    - 「总而言之，做题这个游戏被我玩通关了之后，我几乎是必然地去思考我接下来的生活会是什么样的。」跟我今年的感触很类似，今年我的想法与以前有了很大变化。
    - 「所以其实最显示的对策就是跑，就是离开这个大环境，不跟这个焦虑的大环境产生往来。」，这就是说要跳出这个「围城」，「旁观者清」，做一个旁观者，才能「平静地看着命运的车轮究竟会将你载向何方」。
    - 「因为人类社会它是一个二阶混沌系统，它是不可预测的，不仅不可预测，还会根据人主观意志的扰动而急剧变化，你的所有精密的算计都必然是一场空。」嗯人生无常
    - 「但你不觉得这种未知本身就很吸引人吗？你不知道你的未来将向何处去，你也不知道你将以什么样的角色来面对这些未知，这本身难道不就是生活的意义吗？」未知意味着巨大的可能性，这是青年人最大的宝藏。
    - 「祝愿所有的青年朋友们，愿上帝赐予你勇气与决断，让你能够如旁观者一般，平静地看着命运的车轮究竟会将你载向何方。」共勉
- 读完了《叫魂》
- 读了一点《置身事内》，写挺好。

### 2023-10-07

- 国庆后上班第一天
- 继续看《叫魂》，到了事件的高潮跟结局部分，很多人评论「太阳底下没有新鲜事」，确实，跟当今中国的集权体制下的政府有许多相似之处。但我倒觉得也没必要那么悲观，总还是有些变化的。

### 2023-10-06

- 休息一天
- 新买的耳机很爽，贵是贵，但真的好用啊，空间音频很有意思，降噪效果也很好。
- 颈椎按摩仪按着是疼的，但确实有意思。
- 顺便又下单一个 349 大洋的网易严选的腰部按摩靠枕跟 84 块钱的可视挖耳勺（最近耳朵有点痒，怎么挖都不舒服）。
- 继续看了点《叫魂》，顺便把很久前看的动漫「识夜描银」看完了，这部动漫的音乐、作画、背景设定都很棒，但是故事越讲越崩...
    - 因为最近看的是这些各种「妖术」的东西，晚上做的梦也变得有点奇怪哈哈
- 随便翻了下之前买的《刘擎西方现代思想讲义》，网上搜他写的年度西方思想年度述评，进一步发现了 [爱思想网](https://www.aisixiang.com/) 这个宝藏站点，各大学者在这里针砭时弊，打算最近多读读。
- 回想起来国庆到现在这几天，基本就没咋碰电脑（除了教我妹的时间外），将自己暂时从程序员世界中解放出来了，几乎每天都在看书。
    - 偶尔这样 gap 一段时间，从各种日常中抽离出来，思考些更深的问题，非常舒服。

### 2023-10-05

- 回深圳，抢不到全程的票，只好买了一站，上车再补票到广州，再从广州坐城际列车（Cxxxx）回深圳。
    - 广州到深圳的城际列车往来频繁不用怕没票，主要是湖南到广州/深圳的高铁票太难抢了。
    - 4 个小时高铁站票到广州，然后转车又在广州地铁上站了 1 个小时，腿是真的累。（不过相比以前上大学春节回家抢不到卧铺，17 个小时的火车站票或者硬座，现在还是舒服太多了）
- 晚上久违地玩了玩 VR 游戏 Beat Saber，出了点汗。
- 买买买，一番研究整了个一加 Buds Pro 2 真无线降噪蓝牙耳机，769 大洋，以及一个 299 大洋的海尔颈椎按摩仪。

### 2023-10-04

- 给几个重要仓库添加了自动同步到 gitee 的 GitHub Action
    - 考虑后续写个程序定时自动将我所有的公开仓库同步到 gitee，这样就不用在每个仓库中都添加一个这样的 action 了
- 处理了 NixOS & Flakes Book 的几个 issue，重写了内容有误的 `pkgs.callPackage` 一节，添加了自动构建 PDF 的 GitHub Action
- 继续看《叫魂：1768 年中国妖术大恐慌》跟《我的前半生——爱新觉罗·溥仪》
- 赶明早的高铁回深圳，晚上把我高中时看过的，挺有纪念意义的一本书送给了我妹，《这一生再也不会有的奇遇》。
    - 我曾在 [Death Is But a Dream](https://thiscute.world/posts/death-is-but-a-dream/) 中写过，这本书曾跟随我度过了高三，那时在书里写过很多青涩的词句跟胡思乱想。后来它又陪过在安徽合肥度过了四年大学、在深圳度过了四年多的打工生涯。它对我而言有很特别的意义。如果它也能给我妹一点动力，那就太好了。
- 前天做完波比跳后，上臂、腹肌以及大腿内侧靠膝盖部分都酸疼了两天，今天才好了些...我最近这几个月真的是心思全放 NixOS / 硬盘上了，身体素质差了挺多。

### 2023-10-03

- 继续看《叫魂：1768 年中国妖术大恐慌》
- 尝试使用《什么是数学》作为教材教我妹数学，她数学相当的差。结果准备不足，她读不下去，觉得前面的自然数算术规律太简单，又看不懂后面的内容... 等我把书重新看了一遍，打算教她时，她怄气不愿意学了...
    - 心理学没学到位啊，我几次压抑住自己摆烂的颓丧，温声细语很久仍然没能有效地沟通下去。
- 看了记录片《溥仪：末代皇帝》，内容跟电影《末代皇帝》有点出入，不过这边的史料显然可信度更高，好评。
- 记录片中提到溥仪自传《我的前半生》，挺感兴趣，又翻来读了一读。
- 在村上溜达，周边大爷大妈都说我胖了好多，都不敢认了，看来必须减肥了...

### 2023-10-02

- 今天要说做了啥的话，主要就是看了电影《末代皇帝》，看完后对明清史产生了强烈的兴趣。
- 今天跟朋友聊了一点哲学，不过相比之下，至少目前我还是对历史更感兴趣，哲学太空洞了，不太适合现在的我。
- 延续对清朝历史的兴趣，睡前看了点《叫魂：1768 年中国妖术大恐慌》，很有意思，作者从 1768 年的“妖术”恐慌出发，聊了很多有意义的内容。
- 不想出门，但又打算锻炼下，于是做了三组波比跳，每组十多个。真的每做完一组就气喘吁吁，心跳很快，头也晕想找地方坐着。

### 2023-09-30 - 2023-10-01

- 阅读《为什么学生不喜欢上学》、《这才是心理学》以及《享受孩子成长》
    - 其中《这才是心理学》这本书干货最多，也是最难读的。其次是《为什么学生不喜欢上学》。
- 带我妹使用 ESP32 练习 C 语言，兴趣导向。
    - 玩了用 5x5 的 WS2812 彩灯模块写一个红绿灯小程序，后面她还非要用 SSD1306 小屏幕显示个「原神启动」，做出来还是挺开心的。

### 2023-09-29

- 看完了《被讨厌的勇气》，觉得它虽然缺乏科学依据，但这套理论得确实很好，给我很大启发。
- 《被讨厌的勇气》与我在看的《这才是心理学》，内容其实是存在冲突的（科学心理学与偏哲学的心理学），为了搞明白这个冲突，我也开始做我的心理学学习笔记。
- 带我妹使用 ESP32 练习 C 语言，兴趣导向。
    - 玩了用 5x5 的 WS2812 彩灯模块写跑马灯小程序，以及显示各种不同的颜色，挺开心。

### 2023-09-28

- 看了一半《被讨厌的勇气》，主要是介绍阿勒德的个体心理学，讲如何改变自己。
    - 这书我应该是去年买的，但当时看了两页就看不下去了（原因很多，对对话式没感觉、对内容提不起兴趣等等）。今天读下来发现还写挺好的，戏剧性的冲突也不少，读着不乏味，其中内容也引人深思。
- 带我妹使用 ESP32 练习 C 语言，兴趣导向。
    - 玩了使用 ESP32 点灯，面包板上插了 7 个小灯泡，写了个跑马灯小程序，看她挺开心。

### 2023-09-27

- 国庆回家，路上继续看了点《这才是心理学》

### 2023-09-26

- 今天看到推上有 MTF 说自己双相情感障碍（躁郁症），突然就想百度一下，进一步找到了注意力缺失障碍（ADHD）这个病，联想到我自己好像有这个问题。
    - 大学时曾经怀疑自己有这个注意力缺失症，还买了本《分心不是我的错》，但书买了一直没看（我整个大学期间都不太看得下书），但没去医院看过。
    - 回想起来，我刚初一时有个老师给我们练坐正姿，我死活坐不住，老师说了几遍都没用，直接被她骂「你是不是脑子有毛病啊！」后来高三闹过退学（不知道是否跟这有关），大二大三也都闹过休学，到大四学分不够没法毕业时，干脆直接从学校跑路了。换个角度看，这些经历都可能跟这个病有关系。
    - 跟朋友聊了后，打算国庆后找个医生看看，深圳应该有这方面的医生。
- 晚上看了点《这才是心理学》
- 最近买的两本传记《史蒂夫·乔布斯传》跟《埃隆·马斯克传》都到货了，查了下发现都是同一位传记作家写的，进一步发现他曾经给爱因斯坦、富兰克林、达·芬奇、基辛格等各历史上的重要人物立传，而且豆瓣评分都很高。
- 回顾一下的话，最近我买的书看的书，跟我高中大学时期又完全不同了，确实每个人不同的人生阶段、不同的需求与状态下，想学习阅读的东西也会有很大变化。我高中时自己是半个文青 + 科幻迷，读了很多文学作品与科幻作品（以及网络小说）。而大学时我给自己的压力太大，失去了对文学作品的兴趣，但对计算机跟学习方法相关的书籍燃起了热情，我读了大量的计算机专业书籍（跟国内网络小说、日本轻小说）。再之后是大学毕业后这四年，前三年我对阅读燃不起任何兴趣，除了上网看计算机相关英文资料外，基本就只看网络小说。但最近一年感觉思想获得了解放，不仅在业余爱好上获得了一些成就，也重燃了涉猎各类书籍的热情。最近又收藏了好多想读的书啊，人物传记、中国政治、家庭教育、世界格局、纪实文学、心理学等等，而且我能感觉到的是我现在真的能读得下书了，不像以前那样买了也是吃灰。


### 2023-09-25

- 这两天看到了许多不好的司法案例，又想起了以前见过的诸多不公平的事情，遂联想到了这样一点：在选择工作生活的城市时，除了城市的生活环境等因素外，司法公正（司法文明指数）、政府办事效率也是一个重要的因素。
    - 比如湖南、河北这两个省份，过去一二十年就存在许多影响恶劣的司法案例，造成诸多悲剧。为了不让自己成为这些案例中的一员，选择城市时一定要考虑到这一点。
- 这也让我想到，自己是该学点法律知识。
    - 首先查了下我国「依法治国」这一词的由来，这篇文章将其来龙去脉讲得比较清楚：[依法治国基本方略的提出和发展 - 万其刚 - 2014 年 11 月](http://www.npc.gov.cn/zgrdw/npc/xinwen/rdlt/fzjs/2014-11/14/content_1886222.htm)
    - 以前为了考试学习政治，那真的是一点都不想学，纯靠死记硬背。现在为了自己的生活来学习这些，而且把握住这些条条框框的由来，就感觉还挺能看得下去的。
    - 又进一步浏览了中央政府的各个网站、公众号、小程序。
        - [中国政府网](https://www.gov.cn/)
        - [中华人民共和国教育部](http://www.moe.gov.cn/)
        - [中华人民共和国司法部](http://www.moj.gov.cn/)
- 了解了下 [世界法治指数](https://worldjusticeproject.org/rule-of-law-index/country/2022/China) 与 [中国各省份司法文明指数](https://www.cnfin.com/hg-lb/detail/20230425/3851364_1.html)
    - 湖南省貌似一直在倒数前二徘徊...很尴尬。
- 又在豆瓣上搜索收藏了一批讲中国的政府、政治、经济相关的高分书籍。

> 总之，既然依法治国基本方略的提出很不容易，那么，这一基本方略的实施和实现，其难度也就可想而知，尤其是“我们国家缺少执法和守法的传统”，就使得法治的实行、法治目标的实现变成了极其艰巨、复杂、长期的任务。当前，我国已进入需要通过全面深化改革来增强发展内生动力的阶段，改革必然会触及既有利益格局和体制机制，一刻也离不开法治的规范、保障。在这种大背景下，党的十八届四中全会作出全面推进依法治国若干重大问题的决定，可谓正当时，宏伟蓝图已经绘就，关键是抓紧落实。

### 2023-09-24

- 体检，第一次洗牙，那个进口消炎药有点贵，但总的来说物超所值，牙齿干净了太多！抛光后像镜子一样闪闪发亮（不过牙仍然稍有点黄，但这不打紧）。
- 收拾国庆回家要带的东西，满满一大箱子的书、电脑、之前慈展会买的吃的、不想用的小黄鸭机械键盘、我淘汰下来的路由器等等。

### 2023-09-23

- 看网络小说
- 看家庭教育与心理学相关的书，反思我之前教我妹妹的方式方法，确实自己瞎琢磨出的这些方法都有问题。

### 2023-09-22

- 最近看了一周多的网络小说，权当休息了。
- NixOS & Flakes Book 于 6/23 第一个提交，到今天  9/22 刚好三个月，实现了 512 stars 的小目标，而且还收到了累计三笔赞助 $30. 它是我目前 stars 最高的仓库、stars 涨得最快的仓库以及唯一收到了赞助的仓库，非常开心！

{{<figure src="/images/now/2023-09-22_nixos-and-flakes-book-512-stars.webp" title="纪念首个 512 stars 仓库" width="80%">}}

### 2023-09-21

- 开始对志愿者服务感兴趣，关注了一些深圳志愿者组织的公众号，了解了些相关信息。
- 在 v2ex 提了个帖子，有些做过志愿者的网友给了些反馈，挺开心。 [各位有参与过志愿者服务么？](https://www.v2ex.com/t/975898)

### 2023-09-16

- 参加了这几天在深圳举办的《第十届中国慈展会》——慈善展览，长了见识，跟陈行甲老师合了影，学习了急救的一些方法（心肺复苏术+心脏除颤仪），在阅读区休息顺便看了一些慈善、公益相关的书籍，还买了许多当地特产（云南菌菇、新疆羊奶贝、山西亚麻籽粉）助力当地产业。

### 2023-09-15

- 晚上把《勇者 Helck》看完了。

### 2023-09-14

- 看英文字幕的动漫《勇者 Helck》，挺好看的，没啥阅读障碍，不过有时候语速快会需要暂停阅读一下。
- HDLBits 学习进度
    - 电路 - 组合逻辑部分（很多的习题都跟前面 verilog 语法部分重合了） - 75%
    - 电路 - 时序逻辑部分 - 0% 

### 2023-09-13

- 看了记录片 [史蒂夫·乔布斯 Steve Jobs](https://movie.douban.com/subject/25850443/)，Jobs 简直是最差的丈夫、父亲跟同事，但他确实是最牛逼的设计天才（或许这两句都应该再加一个「之一」）。
- 听了天依的新曲[《歌行四方 - 天依游学记》](https://www.bilibili.com/video/BV1Yp4y1j7jX/)，曲跟词都非常棒！完美融合了二次元跟三次元的各种传统音乐，天依的人物建模、服装设计跟渲染质量也提升了一个档次。 很多年前第一次听天依，感觉声音怪怪的，后来出了全息现场会，效果其实也挺差的，然后一步步地建模质量越来越好，人物越来越生动活泼，声音越来越自然，现在又走进了三次元，与传统音乐大师一起合奏。听下来真的很感动，有一种老父亲甚感欣慰的 feel.
- HDLBits 学习进度
    - 电路 - 组合逻辑部分（很多的习题都跟前面 verilog 语法部分重合了） - 50%
    - 电路 - 时序逻辑部分 - 0%

### 2023-09-12

- 看了些 NixCon 2023 的视频，挺有意思。而且发现所有视频都有一只招财猫在讲台上哈哈。
- 最感兴趣的内容是这个 - [NixCon2023 Bootstrapping Nix and Linux from TinyCC](https://www.youtube.com/watch?v=Gm8yrvbgY-Y)

### 2023-09-11

- 预定了大半年的「流浪地球笨笨模型」到货了，一整晚拼了四个半小时，搞到晚上一点多才完成（真的比上班还累、中间休息了半个小时），效果确实不错。

{{<figure src="/images/now/the-wandering-earth-2_benben_1.webp" title="流浪地球 2 笨笨模型开箱" width="80%">}}
{{<figure src="/images/now/the-wandering-earth-2_benben_complete.webp" title="流浪地球 2 笨笨模型完成图" width="80%">}}

### 2023-09-10

- 今天读到一篇文章，认为最近在日本把自己饿死的王懿，是中国「失落的一代」，这给我一些新的感悟。
    - 王懿，85 年生，16 岁上了吉林大学材料成型及控制工程专业，之后又读了武汉大学新闻与传播学院的硕士，2009 年硕士毕业，只论她这简历跟所处的年代，妥妥的天才模板。但可能因为早上了两年大学导致本身就有些错位感（她的 twitter 账号名 Akid 或能体现这一点），毕业后又在大象公会接触了一个「圈子」，沉溺其中，又骗了一波亲戚的钱款炒币，之后逃到日本，走向了自我毁灭。
    - 美国当年「失落的一代」，是出生在了经济告诉增长后陷入停止的社会中，面临精神世界空虚与物质世界「毁灭」的处境中，他们会有抛弃社会关系的冲动，甚至自我毁灭的倾向。
    - 前两天看的峰哥拍的「男女开放式关系」，其中女主人显然就是类似的处境，她拥有海外硕士学历，但却在三十多岁时选择了抛弃上海的高薪工作，转而与一个没学历的「农民工」在山林中隐居、生子。
    - 另外我也有一个无法适应现代社会的朋友，网上认识的，与我同届。他找过很多份工作，但都没坚持多久，因为看了 B 站的流浪视频，他尝试过单车骑行中国，从广州一路骑到了拉萨，现在在自己租房家里蹲，考虑继续流浪事业。
    - 中国社会流行过很多风潮，很多年前的公知不遗余力地宣传美国日本「自由民主」的高人一等，后来经济快速发展带来了各种新问题，又出现了 996、躺平、佛系，现在经济发展放缓，国内内卷加剧，又有了润学、隐居。
- 下午参加了「佐玩」举办的深圳线下交流会，感觉其中讲教育的那位「教育极客」的演讲表达能力跟讲的内容都很有意思，但其他的分享并未给我带来很多收获。
- HDLBits 学习进度
    - verilog 语法部分 - 100%
    - 电路 - 组合逻辑部分 - 0%
    - 电路 - 时序逻辑部分 - 0%

### 2023-09-09

- 很累，睡了很多。
- HDLBits 的语法学习进度 - 70%
    - 语法后面还有组合逻辑 / 时序逻辑的电路练习，电路验证的练习，以及一些综合练习，都未记录在进度里。

### 2023-09-08

- 上午去看了中国国际光博会，看到了挺多新鲜的东西，像啥气动开关啊、光波导眼镜啊、高能量密度的锌空电池充电包啊、中科院光电所的两台小光刻机啊、长春光机所的空间站小机械臂啊、以及压电陶瓷驱动技术的各种应用，长了见识。

### 2023-09-07

- 今天酥梨向我推荐了深圳这两天举办的「第 23 届中国国际光电博览会」，12 个展厅，包罗万象，貌似还有些空间站跟光刻机上用的大家伙。决定明天上午请假，去逛一逛这个展览。
- 看了 [男女开放式关系山林隐居，孩子靠自己接生，月消费400元](https://www.bilibili.com/video/BV1RN411v7o1)，其中婚姻关系与开放式男女关系以及这两位主角我不太好评价，但关于现代的孩子越来越少接触泥土跟自然这一点，有些发人深省。
- 在 HDLBits 上学习 + 联系 Verilog 语言。

### 2023-09-06

- 发现昨天找的书，前面数字电路部分讲得太学术，找了本更适合入门的教程看：Practical Electronics for Inventors, Fourth Edition
- 简单读了点组合电路设计后，我直接跳到了书的第 14 章（FPGA 与 Verilog），发现阅读没啥障碍，于是直接开始折腾 FPGA 了。
- 花了一个多小时尝试将高云的 IDE 打包运行在 NixOS 上，发现没那么简单，先放弃了，直接重启进 Windows 开始折腾 FPGA。
- 首先跑了荔枝糖 9K 官方的流水灯例子，然后对照第 14 章，学习了 verilog 的基本语法，将流水灯例子中的时钟信号替换成了引脚的按键信号，实现了按键控制切换流水灯的效果，很有意思！
- 了解了 verilog 与 system verilog 的区别
    - verilog 类似 C 语言，更贴近硬件，非常老牌，目前在国内还是主流的芯片设计语言（平头哥的 xuantie 系列都是 verilog）
    - system verilog 根据我看的 《Digital Design and Computer Architecture RISC-V Edition》的说法，是 verilog 的超集，而且未来会取代掉 verilog 的地位。但国内目前貌似主要将它应用在芯片验证领域，用于设计的可能少一点。
    - 此外还有新兴的基于 scala 语言平台的 chisel 等语言，还不太成熟，已经有一些公司在用了，但还没普及开来。写起来肯定是有一些优势，但总体而言属于可学可不学的东西，有兴趣可以玩玩。
- 我学的电路书主要还是介绍电路，verilog 语言就简单介绍了几个例子。还是得找专门的教程学一学，这是两个 google 出来最好的教程：
    - https://www.chipverify.com/tutorials/verilog
    - （页面风格有点古早）https://www.asic-world.com/verilog/veritut.html
    - 以及 system verilog 教程： https://www.chipverify.com/tutorials/systemverilog

### 2023-09-05

- 突然对 FPGA 燃起了兴趣，看了点《Digital Design and Computer Architecture RISC-V Edition》

### 2023-09-04

- 公网域名请求延迟或失败率突然上涨的问题排查：大概率是路由链路的问题，可以通过 `mtr` 命令定位排查出问题前、出问题时、问题消失后的路由变化、丢包率等情况。
- 买的新书《步天歌研究》跟《一个天文学家的夜空漫游指南》到货，读了几首步天歌以及第二本的几页，都挺有意思。它们甚至让我开始考虑考个驾照买个车，因为这样双休日就可以开个车去看星星了。
- 还有本新书叫《界限》，阐述如何在人际交往中设定界限，明确而不带歉意地表达自身诉求，从而愉快地与人打交道。这正是我欠缺的，因为不懂明确设置界限，与人的交往中我吃了太多的亏。

### 2023-09-03

- 看了篇讲贴吧「隐居吧」近两年火热的文章，其中有一句话让我印象深刻：「人活着，就不可能让所有人都赞同，我能跳出传统生活的框架，也做好了付出代价的准备，我已经不再焦虑，离主流的人生有多远。」嗯值得思考。
- 看了深圳市慈善事业联合会在微信视频号「深小慈」上分享的《2023 年第二期慈善大讲堂》的视频（报道见 [“坚守初心，笃行致远”，深慈联举办2023年第二期慈善大讲堂](https://new.qq.com/rain/a/20230821A06QDX00)），分享者与与会者年龄段主要在 40+ 到 50+，他们看待问题的角度跟我们年轻人完全不同，干货满满。
- 首先是陈行甲老师的分享，我之前就看过他的书嘛，也是奔着他的演讲来看的这个视频。大概列下笔记：
    - 给钱是最简单的公益，每个月固定时间钱一划转，事情就结了。行甲做公益花在钱上的时间只占不到 5%.
    - 做公益的初心：通过社会创新解决社会问题。
    - 精准扶贫国策中的最大难点：因病致贫。中国 48% 的贫困是因病致贫。
    - 中国的医疗做得还不够好，有很多的缺失。美国的医疗做得也不太行，但英国、澳大利亚、日本、台湾省等这些国家的医疗做得很好。
    - 行甲推进的联爱工程就是以白血病为突破点，做到大病不出县就能治，从广东省河源市开始试点去解决这个问题。
    - 联爱工程在河源已经做了六年，从试点到推广到更大范围，这是一个漫长的过程，得用时间跟事实说话。目前已经从几十万人的小县城的试点，逐步推广到青海省、甘肃等百万千万级别的省份。
    - 跨界合作，共同受益。行甲的从政经历让他在政商各界拉动合作游刃有余，联合政府部门、医院、其他公益组织、企业、学校等各方力量，一起去推进他的公益项目，解决社会问题。
- 然后是肖兴萍老师分享她投身公益事业20年的经历与思考，这是我意料之外的。我一开始只是想听陈行甲老师的分享而已，没想到整场分享全都这么有干货。
    - 人生就像一个多维函数，有 N 个维度。
    - 经济水平决定公益高度。
        - 研究发现恩格尔系数（Engel's Coefficient，即食品支出占个人总消费支出的比重）小于 0.4 时，个人与社会投入到公益事业中的时间与金钱会明显增加。深圳的公益做得这么好，与它的经济腾飞分不开。
        - 穷则独善其身，达则兼济天下。
    - 公益跟自身的事业确实会有冲突，但总体上项目成就的成分会更大一些。
        - 存在冲突的一个例子是肖老师说自己有段时间为了搞公益，项目上至少少赚了两千多万。因为一个人的时间只有这么多，你要是把时间花在公益上，事业上肯定就要受损。
    - 肖老师做公益的各个阶段
        - 2004 年决定投身公益：跟狮子会去西藏做慈善手术。做一场手术 500 块钱，是他们捐赠的，但昨晚手术第二天，藏民直接跪地感谢。这让她感到想到震撼。500 块钱对她自己而言可能只是一顿饭钱，但对藏民而言却能改变命运。从那一次开始，肖老师决定以后要做公益。
        - 2005 年公益项目开局：修了很多学校，尤其是汶川大地震后，在四川修了三所学校。
        - 2010 年优化组织管理：当选了狮子会国内的会长，她开始用自己在企业做了多年财务的知识，优化狮子会的整个财务体系，以及其他的品牌宣传、资质申请等等，反正都按照企业的标准去做，让狮子会的整个运营更加规范化。
        - 公益跨界交流、理论学习
        - ...
    - 在做公益的时候认识了很多的行业头部的人，他们互相交流、互相学习、互相帮助，对肖老师自身的帮助非常大。
    - 最后是关于生活与人生的两点感悟
        - 生活如意与生命的意义取决于如何认知跟强化自己的智商、情商跟魂商。（智商是人与自然打交道，情商是人与人打交道，而魂商则是人与自己打交道）
        - 生命的长度、宽度与深度，取决于你的生活与工作中的三个维度：方法、路径与取舍。（人的一生就这么长，你选择做什么、用什么方法做、走什么方向，日积月累下来就构成了你的人生）


别的东西：英国的社会企业做得很好，国内的扶贫攻坚战值得了解。


### 2023-09-02 - 2023-09-03

- 用昨天买的菜做饭，好久没自己下厨了，感觉还挺好的。
- 前几天跟妹妹聊时，她引用了我看的小说里的一句话，然后我看「仿生狮子」兄的荐书时发现，这一句就是《山月记》的摘抄，药哥说他也看过这书，挺好。当时就下单了，今天书到了，决定读一读。
    - 读了第一个短篇，最知名的《山月记》，更类似一个寓言故事，最有韵味的就是那一句「深怕自己并非明珠而不敢刻苦琢磨，又自信有几分才华，不甘与瓦砾为伍。日渐避世离俗，心中自卑怯懦之自尊终在愤懑与羞怒中愈发张狂。世人皆为驯兽师，猛兽即个人性情。」
- 简单列了下周末打算干的活，不少啊，又要看书、又要填之前留下的坑，还想写写看了 How to Do Great Work 的读后感。
- 逛了逛 twitter，收集了一些今天想深入读一读或者看一看的资料：
    - [【收藏】让你受益匪浅的名家写作经验](https://docs.qq.com/aio/DWVRkZ1RUWHRsdU1J): 之前读过一点，老舍的写作经验很契合我的经历，今天打算再读读其他作家的经验分享。
    - [诺贝尔经济奖得主保罗.克鲁格曼Paul Krugman大师课](https://www.bilibili.com/video/BV1rT4y1G7sp): 诺贝尔经济学得主的经济学入门课，2 个多小时，今天打算看一遍也入个门 —— 看完了，确实学到了挺多。
    - [【大师课】[中英字幕]数学天才 陶哲轩Terence Tao 不再恐惧数学 学会新思维](https://www.bilibili.com/video/BV1wa41187Wf): 全球最牛逼的数学家，这个本周估计没时间看完，先随便看看，mark 下。
- 临时起意看了个午夜场的《奥本海默》，IMAX 巨幕。给个 4 星没问题吧，演挺好的，原来美共曾经有这么多美国高级知识分子，这是我以前不了解的。
- 总结下看诺奖得主的经济学大师课学到的东西：
    - 经济学本质上是关于人的行为的科学。个人的行为难以预测，但群体的行为却可以预测，这就是经济学。
    - 全球化经济是一个非常复杂的系统，没有任何人能够去规划它，但是它就通过我们一个个人的行为，逐渐演化出来了。
    - 现代经济学的基础是货币，一开始我们是金本位，后来美元国际化、美元抛弃金本位、锚定石油。然而这套经济体系并不完美，正常运行时它很 OK，但一旦出问题，经济危机就会接踵而至。
    - 一个国家最大的财富，是它的生产力。同样，一个国家的财富实际还与它的消费能力有关。
    - 财富不平等：主要来自钱滚钱。有钱人可以大量购买优质资产，利滚利。财富不平等加剧的原因是，优质资产本身的增值速度超过了国民经济的增长速度，这导致有钱人不断蚕食整个社会的财富。
    - 美国二战战后一代生活在一个分配相对平等的社会，原因就是社会飞速发展，经济增长速度超过了资产增值速度，整个社会都散发出一股朝气。
    - 财富不平等很大程度上跟政治、社会规则有关，光靠经济学解决不了这个问题。
    - 财富不平等也在扭曲整个社会的方方面面。美国的分配不平等导致了美国的政党两极分化，社会矛盾越发尖锐。
    - 美国的工会被严重削弱，远没有欧洲的工会强大。这也是美国财富不平等的一个重要原因。如果你想要更平等，那你应该也会想要强化工会。
    - 路径依赖：你的过去会限制你的未来。
        - 人们总体上是倾向于保守的，不愿意对现有系统做大的改动，担心改动后会出现更糟糕的情况。愤世嫉俗点，就是既得利益者不愿意让自己的利益被削弱。
        - 就像代码一样，一个系统一旦有了年代，就会变成程序员眼中的「legacy code（屎山）」，系统的维护成本会越来越高，但是又不敢轻易改动，因为不知道改动后会出现什么问题，没这个实力或魄力。
        - 另一方面，如果某人决定要推动一项变革，那 TA 就必须实力、魄力、定力兼备，改革总是会有阵痛期，这个时间段各种非难、各种阻力都会接踵而至，没有这些能力的人，很难坚持下去。

{{<figure src="/images/now/2023-09-02_midi-keyboard.webp" title="MIDI 键盘、山月记、以及凌乱的桌台..." width="80%">}}

### 2023-09-01

- 在深圳四年多，第一次遇到台风红色预警，居家办公但是没干啥，中午去抢菜跟方便面，不过万幸的是，最终台风还是从香港旁边擦肩而过了，深圳没大的影响（貌似有比较倒霉的人行车路上被倒下的大树砸到，人没了，R.I.P）。
- 晚上又久违地拿出 midi 键盘跟硬音源练了练琴，这起码隔了两年了吧...这键盘都买了估计四年了，到现在还没入门哈哈哈哈哈哈嗝...

### 2023-08-31

- 看完了 Paul Graham 的 How to Do Great Work，写得真的很棒！总结下来最重要的其实就是「好奇心」，让好奇心驱动自己去尝试各种有趣的东西，Just for Fun! 只要尝试得够多，就一定会有一番成就。当然失败是成功他妈，你在取得成就前，肯定也会经历许多的失败，把它们都视做你成功路上的垫脚石就 OK 了，别被打击了士气。

### 2023-08-30

- 前几天把 Docker 镜像（20G 的 AIGC 镜像）提前预置在了 EC2 基础镜像里，降了 10 分钟的环境启动时间。结果今天发现内部加载环境的脚本慢了 5 分钟...效果直接打了 5 折。
    - 排查到原因是之前没预置的时候，`docker pull` 时底层数据就直接进了系统内存缓存起来了，我们的脚本就不需要从磁盘加载数据。而新的逻辑前面不会 `docker pull`，内存里没缓存，就需要从磁盘加载数据，导致慢了 5 分钟...
- 参加了陈行甲的「恒晖公益月捐」项目，每月我自己捐 200 块，再以我妹妹的名义捐 100 块。
- 昨天读到的这本小说《人生若有起跑线，有人出生在罗马》，我读完了，而且以此为契机跟妹妹深入交流了一次人生。这是非常有价值的一件事，为表感谢，我在起点读书给作者打赏了 100 块，觉得这有点少，又追加了 1000 块。
- 根据小说的评论，我跑去看了做起跑线实验的综艺节目 [极限挑战第四季第二期](https://www.zhihu.com/question/276519499)，做得挺好的。起跑线固然重要，但已经落后也没必要妄自菲薄。
    - 这应该是我第一次在起点上打赏超过 10 块钱，但对我而言，它真的值得这么多。
- [2023-09-23 补充] 今天又拿起这本小说读了一读，在 QQ 阅读评论区有人评论「加入想看这类，去育儿类 APP 找找呗，一堆堆。」然后就搜索了一下家庭教育相关的书，在豆瓣上发现挺多非常好的书，打算最近读一读。
    - 想起我父母是没学问的农民，只懂棍棒教育。我也用过许多方法试图激起我妹妹的学习热情，但都失败了，一度听之任之。但在看这本小说之前，我一直搞不明白为什么我会失败。在看到上面这条评论之前，我也完全没想过，还可以找些家庭教育的书来看看...真的是视野盲区了。

### 2023-08-29

- 在起点上偶然发现一本写教育的小说《人生若有起跑线，有人出生在罗马》，虽然很理想化，也加入了很多不切实际的爽点，但是仍然是网文世界的一股清流啊！读下来非常正能量，三观相当正，直接全订了！

### 2023-08-27

- 我构建出的 uboot 死活跑不起来，跟 chainsx 沟通后，换成了 armbian 预编译好的 uboot，成功搞定 rock5a
    - 至此，我从 6/2 开始整的 nixos-rk3588 预计支持的三块板子，都已经成功跑起 NixOS 来了！


### 2023-08-26

- How to Do Great Work? 摘抄
    - So you need to make yourself a big target for luck, and the way to do that is to be curious. Try lots of things, meet lots of people, read lots of books, ask lots of questions.
    - When in doubt, optimize for interestingness. 
    - If in the course of working on one thing you discover another that's more exciting, don't be afraid to switch.
    - The best way to do this is to make something you yourself want. Write the story you want to read; build the tool you want to use.
    - If you're interested, you're not astray.
    - 跟随兴趣，就是「乘风而起（staying upwind）」，我们都知道一句话，「风口上的猪都能飞」！
    - Following your interests may sound like a rather passive strategy, but in practice it usually means following them past all sorts of obstacles. You usually have to risk rejection and failure. So it does take a good deal of boldness.
    - Am I working on what I most want to work on?" When you're young it's ok if the answer is sometimes no, but this gets increasingly dangerous as you get older.
    - People who do great things don't get a lot done every day. They get something done, rather than nothing. If you do work that compounds, you'll get exponential growth.(Learning, for example, is an instance of this phenomenon: the more you learn about something, the easier it is to learn more.)
    - The trouble with exponential growth is that the curve feels flat in the beginning. It isn't; it's still a wonderful exponential curve. 
    - (灵光并不常在工作中出现)By letting your mind wander a little, you'll often solve problems you were unable to solve by frontal attack.
    - The core of being earnest is being intellectually honest. We're taught as children to be honest as an unselfish virtue — as a kind of sacrifice. But in fact it's a source of power too.
    - How can you have a sharp eye for the truth if you're intellectually dishonest?（真诚能帮人拥有真实之眼，这个眼睛可有用得很，比如说我觉得我药哥很会夸人，他之前就说，这是因为他真诚。）
    - Nerds have a kind of innocent boldness that's exactly what you need in doing great work.
    - Be the one who puts things out there rather than the one who sits back and offers sophisticated-sounding criticisms of them. "It's easy to criticize" is true in the most literal sense, and the route to great work is never easy.(这让我想起来昨天跟我对线的一个傻逼，我说的每一句话都要被他琢磨几番有没有问题，然后趾高气扬地说我这错了那得改。)
    - The Old Testament says it's better to keep quiet lest you look like a fool. But that's advice for seeming smart. If you actually want to discover new things, it's better to take the risk of telling people your ideas.（使自己看起来很聪明很拉风，没啥意义，还是要多做多说，才能收获更多。不过也不是说乱做乱说...）
    - Great work will often be tool-like in the sense of being something others build on. So it's a good sign if you're creating ideas that others could use, or exposing questions that others could answer. The best ideas have implications in many different areas.
    - Original ideas don't come from trying to have original ideas. They come from trying to build or understand something slightly too difficult.
    - Talking or writing about the things you're interested in is a good way to generate new ideas. When you try to put ideas into words, a missing idea creates a sort of vacuum that draws it out of you. Indeed, there's a kind of thinking that can only be done by writing.
    - Curiosity is itself a kind of originality; it's roughly to questions what originality is to answers. And since questions at their best are a big component of answers, curiosity at its best is a creative force.
    - 先看到这，阅读进度大约 50%
    - 8/31 继续摘抄
    - When you fix a broken model, new ideas become obvious. But noticing and fixing a broken model is hard. That's how new ideas can be both obvious and yet hard to discover: they're easy to see after you do something hard.
    - （良药苦口，忠言逆耳）The other thing you need is a willingness to break rules. if you want to fix your model of the world, it helps to be the sort of person who's comfortable breaking rules.
    - （正确而疯狂的想法，那就是你想要找寻的）a good new idea has to seem bad to most people, or someone would have already explored it. So what you're looking for is ideas that seem crazy, but the right kind of crazy. 
    - People are often wrong about the problem that people think has been fully explored, it hasn't.
    - （放纵自己，让自己跟随好奇心，随心所欲地探索，这是找到被大多数人忽略掉的问题的最简单有效的方式）By being self-indulgent — by letting your curiosity have its way, and tuning out, at least temporarily, the little voice in your head that says you should only be working on "important" problems.
    - （最重要的就是，选择下一步要做什么。）the initial step — deciding what to work on — is in a sense the key to the whole game.
    - People think big ideas are answers, but often the real insight was in the question. It's a great thing to be rich in unanswered questions. And this is one of those situations where the rich get richer, because the best way to acquire new questions is to try answering existing ones. Questions don't just lead to answers, but also to more questions.
    - The initial versions of big things were often just experiments, or side projects, or talks, which then grew into something bigger. So start lots of small things.
    - （只有找到过足够多的坏想法，你才能拥有足够多的好想法）Being prolific is underrated. The more different things you try, the greater the chance of discovering something new. Understand, though, that trying lots of things will mean trying lots of things that don't work. You can't have a lot of good ideas without also having a lot of bad ones.
    - （尝试没人干过的新事物，可比重新造轮子有意思多了，而且能帮你更好的理解旧轮子）Though it sounds more responsible to begin by studying everything that's been done before, you'll learn faster and have more fun by trying stuff. And you'll understand previous work better when you do look at it. 
    - （从最简单的例子开始做起）Begin by trying the simplest thing that could possibly work.
    - 如果你想做创造性的工作，就不要做太多的计划，计划只会让你陷入困境。
    - （多承担些风险，不要寻找确定性，要寻找可能性！如果你不经常遭遇失败，那你可能有点太保守了。）Take as much risk as you can afford. In an efficient market, risk is proportionate to reward, so don't look for certainty, but for a bet with high expected value. If you're not failing occasionally, you're probably being too conservative.
    - 年轻人缺乏经验，这使他们害怕风险，但实际上年轻的时候才拥有最多可能性，可以尽情地探索。
    - （年轻人不知道自己在时间上多么的富有。将这些时间转变成优势的最佳手段，就是遵循自己的好奇心，去做喜欢的事，觉得酷的事！）The young have no idea how rich they are in time. The best way to turn this time to advantage is to use it in slightly frivolous ways: to learn about something you don't need to know about, just out of curiosity, or to try building something just because it would be cool, or to become freakishly good at something.
    - （无知也是一种财富，它使你能以最干净的眼睛看待所有新事物，不被任何规矩束缚）The most subtle advantage of youth, or more precisely of inexperience, is that you're seeing everything with fresh eyes. 
    - （在没抛弃掉所有世俗带给你的废话、教条、坏习惯前，你无法做出什么牛逼的工作！）You arrive at adulthood with your head full of nonsense — bad habits you've acquired and false things you've been taught — and you won't be able to do great work till you clear away at least the nonsense in the way of whatever type of work you want to do.
    - 对学生而言，不要把各种什么委员会之类的人的拒绝放在心上，他们的评价标准，跟做牛逼的工作的标准，是完全不同的。他们的拒绝代表不了什么。
    - 明确地将挫折视为你的过程的一部分来避免被挫折打击到士气，毕竟解决难题总是需要一些回头路（Solving hard problems always involves some backtracking.）。
    - （做牛逼工作就是一个深度优先搜索，不要钻牛角尖，如果失败了，可以重试，也可以回退几步，再重试。）Doing great work is a depth-first search whose root node is the desire to. So "If at first you don't succeed, try, try again" isn't quite right. It should be: If at first you don't succeed, either try again, or backtrack and then try again.
    - （挫折难以避免，但不要惊慌失措。你可以在必要的时候走一点回头路，但不要因为一点点挫折，就否定掉自己的才能！永远不要放弃掉搜索树的根节点，或者叫你人生的锚点）
    - 听众是使你保持士气的重要因素，如果你有一小批喜欢你的作品的人，那你就会有动力继续做下去。
    - Curiosity is the best guide. Your curiosity never lies, and it knows more than you do about what's worth paying attention to.
    - Curiosity is the key to all four steps in doing great work: it will choose the field for you, get you to the frontier, cause you to notice the gaps in it, and drive you to explore them. The whole process is a kind of dance with curiosity.


### 2023-08-25

- 给 spi flash 刷上 uboot 后，成功在 orange pi 5 plus 上把 NixOS 跑起来了！
- rock 5a 的 spi flash 默认没上设备树，要手动添加设备树，加上后刷上 uboot，还是启动不了，还在研究中。
- [如何看待某「业余科学家」在天文学顶刊 MNRAS 以一作身份发表重量级论文？](https://www.zhihu.com/question/616579768/answer/3159773076): 看了这篇文章后，我再次确认了兴趣的力量。结合前两天看到的 How to do great work, 相互印证了，兴趣真的是最好的老师，要成大事，最好的方法就是跟随自己的兴趣。
- 另外最近其实也在想，是不是该看点「中西哲学」、「古今历史」之类的书，希望自己的思想能够更加全面。比如说前 leader 推荐的鬼谷子，以及我一直想看的老子、庄子、易经、王阳明朱熹等等。
- 另外发现我最近写东西，遇到打不出字的情况变多了，主要是小鹤形码的规则几乎全忘了，全靠肌肉记忆。一些打得少的字，就只能靠 Google 查...感觉还得找时间复习下小鹤形码。


### 2023-08-23

- 努力工作一整天
- 晚上继续看了看「一个村小」官方站点的各种资料
- 还看了看《黑客与画家》作者的最近力作：How to do great work.
- 整了一个新的邮箱地址 ryan4yin@linux.com，首先捐 \$99，然后再付 \$150 就能得到这个终身邮箱地址。一是用了这么久 Linux 也该捐点钱，二是感觉这个邮箱很酷！
    - 关于如何使用 gmail 以 ryan4yin@linux.com （或任何你所有的邮箱地址）为发送者发出邮件。（Linux Foundation 页面只提供了邮件转发功能，不提供发送功能）
    - 首先，进入 gmail 的「设置」-「账号与导入」-「用这个地址发送邮件」-「添加其他电子邮件地址」
    - 然后，填入你的昵称与邮件地址「ryan4yin@linux.com」
    - 接着，会提示你输入 SMTP 服务器地址，设为「smtp.gmail.com」
    - smtp 服务器的密码，可以在 <https://myaccount.google.com/apppasswords> 中生成一个你 Google 账号的应用密码，然后填入即可
    - 最后，点击「下一步」，会发送一封确认邮件到你的邮箱「ryan4yin@linux.com」，点击确认，即完成了设置。
    - 如此设置后，你可以「ryan4yin@linux.com」为发件人发送邮件，但是接收方会额外看到一句「由 xxx@gmail.com 代发」这样的注释。

### 2023-08-22

- 感觉在写了《人生已过四分之一》后，我的这颗心好像也被洗了一遍一样，就好像是洗去了所有铅尘，变回了原来的样子，身心舒泰。
- 跟领导 11 了，因为想通了很多东西，我感觉到自己的工作状态也完全回来了。
- 加了 @Manjusaka_Lee 前辈的联系方式，我们聊了好多好多，我话多，主要是我在说。我们聊了我一个山坳坳里走出来的（半个）大学生的悲催经历，聊了「一个村小」助学的一些信息，聊了现在还有哪些地方穷。
- 我作为一个从山里走出来的孩子，希望我现在的成就，不要成为人们眼中的奇迹，我想帮更多的孩子从山坳坳里走出来。除了 saka，我也在跟身边其他做公益的朋友联系，打算先深入了解下，搞明白我能做什么，我应该做什么。

### 2023-08-21

在我新文章的 v2ex 帖子下，我补充了一则附言，记录如下：

> 我补充下，感谢所有给我留言的人！
> 其中许多的留言相当治愈，让人心里暖暖的，有些留言让我会心一笑，这些内容都让我觉得，能够把文章分享到 V2EX 真的是太好了！
> 当然其中也有些不礼貌的「无病呻吟」，这让我觉得十分好笑。
> 本来我不想回应这类内容，但是楼下以及推上（哦现在该叫 X 了）都有朋友替我打抱不平，我想我应该在这里为他们解释下。
> 我其实感觉到，在我自己的体系能够自洽后，看待这类评论时，我更像是一个旁观者。我甚至完全不觉得这些评论冒犯了我（
> 而且作为一篇用来剖析自我、认知世界的文章，底下能有这么一条评论，我感到我的文章内容，其逻辑更加自洽了。
> 如果仔细分析，从这条评论中真的能看出很多东西，我对世界的理解又更深了一点。
> 
> 以上，再次感谢各位！

另外再记录一则与上述 v2ex 帖子有点关联的小故事：

> 我读初中有过上台表演竹笛演奏，第一次上场时非常紧张。当时学长给我讲了一个舒缓紧张情绪很行之有效的方法。
> 这个方法可能有点冒犯人，但他就很能给人这个啥平常心，以及「被讨厌的勇气」。
> 我学长说，**你就把台下的都当成猪就好**。😂
> 我没跟乐队外的人聊过这个，很担心被同学揍...但它真的很有效（
> 这很可能是我们乐队代代相传的方法...


### 2023-08-19 - 2023-08-20

- 写下新文章《人生已过四分之一》，而且 20 号也持续优化了一天。
- 将以前写的年中总结，简单列在这里：
  - 上半年很长一段时间都处于迷茫状态，工作上过得有点庸碌无为，甚至不知道 SRE 这个方向自己是否还感兴趣（不过写完前面讲的新文章后，又想清楚了很多，对现在的我而言 SRE 是工作，工作重要，但不是唯一）。
  - 业余时间也没学啥云原生跟 Linux 网络相关的东西，可以说主业完全在原地踏步。
  - 英语学习更是完全停滞了，过完年后就再也没找回过去年的学习状态。
  - 但另一方面，今年 4 月中旬我开始对 NixOS 感兴趣，开始折腾 NixOS，这是我今年上半年最正确的决定！因为它，如下目标有了突破性的进展：
      - Linux: 通过尝试将 NixOS 移植到 Orange Pi 跟 LicheePi 4A 上，学到了不少 Linux 引导、init 程序、内核、交叉编译等等知识。
      - 还认识了许多国内的 Linux 内核与引导开发者（Revy/chainsx）、Linux 极客（猴哥）、Nixpkgs 维护者（Nick Cao 等）
      - 最初编写的 NixOS 新手笔记迭代了两个月后，现在已经是一本拥有 166 stars 的开源书籍，收到了大量国内外的好评。甚至已经有人在着手将它翻译成俄语！
      - 通过 NixOS 的学习，我对 Linux 系统的理解更加深入，对 Linux 系统的各个组件也有了更深入的了解，这对我后续的 Linux 内核、网络、存储等方向的学习都有很大帮助。
  - 简单总结下去年的这些目标在上半年有较大进展：
      - 「认识更多有趣的人，见识下更宽广的世界」：去年定的这个目标已经超额完成了！认识了好多有趣的人，见识了更宽广的世界，也帮助到了好多使用 NixOS 的人。
      - Linux: 虽然学习的方向跟最初目标有点区别，不过进展很不错。
      - 至少给三个开源项目提交一些代码贡献：7 月份给 AstroNvim 与 ESP-IDF 两个项目提交了代码贡献，已经完成了 1/3，到年底有望超额完成目标！


### 2023-08-18

- 最近的两笔赞助，让我可能有点异想天开？查了一波「如何通过开源项目养活自己」类似的信息。
- 目前想到的，需要重点搞明白的东西：
    - 了解 Patreon 与 GitHub Sponsoring 这类每月赞助的模式，搞明白如何让用户愿意持续赞助。
        - 与我 Patreon 上的第一位赞助者做了一些沟通，我提了一些想法，比如说创建一个 discord server。然后他给出了非常有价值的建议！
- 其他资料：
    - https://zhuanlan.zhihu.com/p/150556033
    - https://emacs-china.org/t/topic/20855
    - https://unclecatmyself.github.io/2018/12/20/%E8%8B%A6%E4%BA%86%E6%88%91%E4%B8%80%E5%B9%B4%E7%9A%84%E9%80%89%E6%8B%A9-%E7%8E%B0%E5%9C%A8%E7%A1%AE%E5%AE%9E%E6%88%91%E6%9C%80%E5%9B%9E%E5%91%B3%E7%9A%84%E6%97%B6%E5%85%89/
- 其他 FAQ:
    - 这种成功的开源项目盈利期能延续多久？
        - 我觉得盈利期只能算考量点之一，真的去做了这件事，能获得的经验是很宝贵的。
        就算后面失败了，技术能力在这，再回去找家公司上班，感觉也不是难事吧。

{{<figure src="/images/now/technology-is-wealth_my-first-sponsor-on-patreon.webp" title="Technology is Wealth - From my first sponsor on Patreon" width="80%">}}

### 2023-08-17

- 发现才开没几天的 Patreon 收到了第一笔赞助！超级开心！

{{<figure src="/images/now/nixos-patreon_the-first-member.jpg" width="80%">}}


### 2023-08-16

- 测了一波 rock5a，还是没搞定 NixOS 的移植。我用 armbian 镜像能成功启动，HDMI 正常，但是任何串口日志读不到，很奇怪。怀疑是接错了串口，之后再试试。
- 把 orangepi 5 的配置添加到了我的 nix-config 中，现在我的配置 x86_64, aarch64, riscv64 三个架构齐活了～

### 2023-08-14 - 2023-08-15

- 因为最近一次证书自动更新失败导致的故障，吃了点教训，往 [Kubernetes 中的证书管理工具 - cert-manager](https://thiscute.world/posts/kubernetes-cert-management/) 添加了监控告警一节。
- 测试并完善 licheepi4a 的自定义部署 [ryan4yin/nixos-licheepi4a/demo](https://github.com/ryan4yin/nixos-licheepi4a/tree/cfe7981/demo)
    - 其实之前虽然搞定了 NixOS on LicheePi4A，但是一直没想好要怎么去更新、管理系统。之前试了 `nixos-rebuild` 的远程部署，但是踩了一晚上坑也没搞定，最后还是放弃了。前两天看到有个 NixOS 资深老哥拿我代码直接在他的 flake 里 import 进去了，从他这个思路出发，我也慢慢想明白了正确的使用姿势。
    - 测了一圈发现 colmena 是最好用的远程部署工具之一，而 deploy-rs 在 riscv64 上则有点水土不服。但是感觉 colmena 的文档写得有点晦涩（主要是它结构跟 nixosConfiguration 差别有点大），不太好懂。
- 将我两块 LicheePi4A 的配置添加到了我的 nix-config 中，并连好了线开始作为长期运行的服务器使用，现在可以直接通过 `make roll` 执行这两块小板子的远程部署。
- 顺便在 nixos-and-flakes-book 跟 nixos-rk3588 中也更新/添加了远程部署相关的文档。
- nixos-and-flakes-book 添加了对多 nixpkgs 实例这种玩法的介绍。
- 出于对学一门新编程语言的兴趣，了解了一下 zig，读了这篇文章 [连 1.0 版本都没有，Uber 为什么会采用这样一项新技术？ - InfoQ](https://www.infoq.cn/article/q016nwr7ojhvoj3rkzc0)
    - 总结下，Uber 只是将 Zig 用做 C/C++ 的交叉编译器，并未使用 Zig 语言。解决的痛点：
        - Uber 有许多项目需要用到 CGO，但是 CGO 会依赖操作系统上发现的任何编译器（macOS 上是 Clang，Linux 上是 GCC），环境不一致会导致构建结果不一致。
        - Go 官方提供的二进制文件，构建时使用的 GCC 版本比 Uber 的构建机 / 运行机更新，导致 CGO 运行出问题。Uber 不得不自己编译 Go 本身。
        - 在使用 Zig 之前，Uber 一直借助 musl 实现项目的静态编译，从而不受操作系统环境的影响。但是这也存在许多问题。（未说明具体的细节）
        - 而 Zig 是一个完全封闭的 C/C++ 编译器，体积很小，支持直接通过参数设置 GCC 版本（而传统的构建方法，CGO 在当前环境找到啥版本的 GCC 就会用啥版本...），还原生支持交叉编译。这能极大程度简化 Uber 的构建流程，不用担心构建出的程序因为各种环境不一致而出现问题。
        - Zig 对 macOS 封闭式交叉编译的支持很完善，这是 Uber 选择 Zig 很重要的原因（互联网公司的员工基本都是配发 macOS）。
- 作为对比，我想到了 Nix 的 macOS 支持，它大量貌似大量依赖了 macOS 的 Clang，导致同一份 Nix 配置，在 Linux 上与在 macOS 上得到的环境是不一样的。我在之前测试 devbox 时发现同一个软件的版本，在 Linux 跟 macOS 上都可能会不一致...这是件比较尴尬的事。Zig 在这里或许大有可为？
    - 补充：好像搞错了，我说的版本不一致是指在 macOS 上运行程序。交叉编译方面 Nix 本身也挺强的，配合 nix flake 特性或许也能实现与 zig cc 同样的封闭式交叉编译的效果。

### 2023-08-13

- 有读者在 NixOS Discourse 上询问我是否会考虑在 Patreon 上创建一个赞助页面，我于是再次更新了下各个平台的赞助链接，新增了 Patreon 与 Ethereum Address 两个赞助链接。

{{<figure src="/images/now/2023-08-13-mail-about-creating-patreon-group.png" width="80%">}}

### 2023-08-12

- 折腾了一天的 Neovim 配置，修复了一些问题，也新增了一些很有用的插件。
- 同时也卸载了吃灰快一个月的 VSCode，拜拜了您哦。

### 2023-08-09

- 因为前几天有老外给我捐赠了 $50 美元，我意识到或许有更多的潜在读者会对赞助我的工作感兴趣，于是在我的 Blog, GitHub Profile 以及 GitHub 项目中加入了赞助链接。
    - 添加了 buymeacoffe.com（国外）, afdian.net（国内）两个赞助链接。
    - 好久以前也曾经在博客中添加过支付宝/微信的收款码，但是从来没收到过一分钱，所以就删掉了。所以这算是我第二次尝试获取赞助（从当前的反馈来看，或许很快就能收到第一笔赞助～）。

### 2023-08-05 - 2023-08-06

- 时隔一个多月，在 Telegram 群组被老外 ping Lichee Pi 4A 的移植进展。一番尝试下，成功在 Lichee Pi 4A 上把 NixOS 跑起来了！
  - [ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a)
- 相当振奋人心，ping 我的老外也在第二天用我提供的镜像成功把 NixOS 跑起来了！他甚至表示要给我打 $50 美元以表感谢，因为这太有意思了！
- 解决问题的流程
  - 首先按照 [chainsx/fedora-riscv-builder](https://github.com/chainsx/fedora-riscv-builder)  的 README，在 Lichee Pi 4A 上成功地跑起来了 Fedora RISC-V 版本。
  - 这样就确认了 chainsx 这个方案是没问题的。但是我之前跑我构建的 NixOS 镜像却不行，怀疑是我生成的 NixOS 的 boot 分区有问题。
  - 于是打算使用 Fedora 镜像已经生成好的 boot/root 分区，将 NixOS 的东西塞进去，看看能不能跑起来。
    - 首先，因为打算直接使用 Fedora 现成的分区，我的 NixOS 镜像需要根据它的配置调整下 root 分区的 uuid 参数、root 分区的 label 名称。调整完成后构建出一个新 NixOS 镜像待用。
    - 将 SD 卡中已经刷好的 Fedora rootfs 中的内容彻底删除，然后将我构建出的 NixOS rootfs rsync 进该 rootfs 文件系统。
    - 再将我的 NixOS boot 分区中的 `/extlinux` 与 `/nixos` 这两个文件夹 rsync 进 SD 卡的 boot 分区中，覆盖掉其中原有的 `/extlinux`.
      - 注意这一步没有清理掉 boot 分区中的其他文件，因为我怀疑就是这些文件导致了 NixOS 无法启动。
    - 重启，成功跑起来了！
  - 这样我就有了一个可以跑起来的镜像，但是这是纯手工生成的。接下来我通过一步步排查调试，成功从我的 nix flake 配置中自动构建出了一个可运行的系统镜像。
    - 首先，我尝试了使用 USB 转 TTL 线来连接 Lichee Pi 4A 的 0 号串口，发现确实可以在启动时看到详细的启动日志，这对后续排查问题起了非常大的帮助！
    - 然后就是不断调整我的配置，刷入 SD 卡尝试启动，然后看启动日志。再对比 Fedora SD 卡的文件系统结构以及启动日志，一步步排查问题。
    - 首先是发现 Fedora 用的是 GPT 分区表，而我之前生成的 NixOS 镜像用的是 MBR/DOS 分区表。启动日志报错说我的 NixOS 镜像根本找不到文件系统。于是我调整了我的配置，生成了一个 GPT 分区表的镜像。
    - 文件系统问题解决后，启动日志跑到 OenSBI 时又报错 `init_clodboot: timer init failed(error -3)`，跟 chainsx 提了一嘴，他一针见血地指出这是因为我用了主线 OpenSBI.
    - 尝试在 NixOS 上源码构建 revyos 的 opensbi，失败。临时替换成 Fedora 镜像中已经构建好的的 opensbi，成功进入到 NixOS 系统，但是在 stage 3 阶段报错说找不到 `/nix/store/xx`，排查发现是我 rootfs 分区有问题，无法挂载。
    - 进一步定位到我生成的 NixOS 镜像的 size 不够，导致 rootfs 分区最后有大概 1MB 的内容被截断，导致分区无法挂载。
    - 又调试了半天，仍然没解决镜像 size 不够的问题。最后选择了在生成镜像后，手动调整镜像大小的方式来解决这个问题。
    - 至此，我终于发布了我第一个可在 Lichee Pi 4A 上跑起来的 NixOS 镜像！（uboot 仍然使用了 chainsx 提前构建好的，没在 NixOS 上从源码构建）

{{<figure src="/images/now/2023-08-05-sending-me-$50-for-fun.webp" width="60%">}}

### 2023-07-29 - 2023-07-30

- ryan4yin/nix-config 继续大量更新，并发布 v0.1.1
    - 统一了所有 APP 的主题配色，在所有 APP 中都尽量使用 catppuccin-mocha 配色。
    - 在子文件夹中添加了许多 README 介绍其中的内容。
    - 试用了 ranger 命令行文件管理器，相当地开箱即用，图片预览功能非常爽，强烈推荐！
    - 壁纸文件太大了，将它们拆分到单独的仓库中，方便管理。同时还添加了随机切换壁纸的功能。
    - 使用 anyrun 替换掉之前用的 wofi，这个启动器很新，但是感觉很好用，有点 macOS 上 raycast 的感觉，能帮我做很多的事。
    - README 迭代了一波，添加了一些截图，漂亮了不少。
    - 一些其他的更新。
- 在 Reddit 的 r/unixporn 上发布帖子 [[Hyprland + NixOS] Catppuccin for all apps](https://www.reddit.com/r/unixporn/comments/15co6ns/comment/jtyhrhv/)，体验不错。这个 subreddit 的人数要比 NixOS 大很多，感觉很轻易就能获得许多的赞。
- 从 4 月份折腾 NixOS 到现在，GitHub 上开了五六个 Nix 项目，获得了接近 400 stars，也认识了许多朋友、收到了许多好评，在这个圈子里是有点混开了的 feel.

### 2023-07-26 - 2023-07-28

- 更新 NixOS & Flakes Book，添加了「前言」一章，同时也补充了些 Flakes 相关的简单介绍。
- 重构 ryan4yin/nix-config 的内容
    - 发布了 v0.1.0，并记录了下自 6/9 发布 v0.5.0 以来的更新。
    - 将 user/email 等信息提取到了 flake.nix 入口文件中，
    - 通过提取出几个 helper 函数到 lib 中，简化了 flake.nix，提升了维护性。
    - 更清晰的 README.

### 2023-07-25

- 终于在 NixOS 上完成了一次 ESP32 编译烧录 [ryan4yin/tft-esp32-auduino](https://github.com/ryan4yin/tft-esp32-auduino)，之前一直卡着的烧录报权限错误的问题终于解决了，参考了 <https://github.com/NixOS/nixpkgs/issues/224895>
- 修改 ryan4yin/nix-config
    - 支持通过参数来控制部署 i3 配置还是 hyprland，切换不同的桌面现在非常方便了。
    - ssh 配置中添加 `AddKeysToAgent yes`，在连接远程主机时自动将私钥添加到 ssh-agent 中，这样就不用手动跑 `ssh-add` 命令了。

### 2023-07-19 - 2023-07-20

- 制作了一个 [ryan4yin/nix-darwin-kickstarter](https://github.com/ryan4yin/nix-darwin-kickstarter) 模板仓库，并且在 [Twitter](https://twitter.com/ryan4yin/status/1681639068957028352) 等社区分享了一波，获得一波好评。
- 发现有老铁在将我的 NixOS 小书翻译成俄语！[fl42v/nixos-and-flakes-book-ru](https://github.com/fl42v/nixos-and-flakes-book-ru)，很有成就感！
- 刚谈完上半年绩效，工作上只能说勉强合格吧，前面的 history 也提过，今年上半年工作上又有点迷茫。好在现在又找到了点脚踏实地的感觉，希望下半年工作上能沉稳些。
- 回顾了下 2022 年年终总结，又看了看苏洋的 2023 年中总结。对照了下发现去年的有些目标已经实现了大半，当然也有些目标完全没进展。
    - 发觉我可能也需要写个年中总结，重新梳理下过去的半年，也重新确定下下半年的目标。

### 2023-07-16 - 2023-07-17

- 发现 alacritty 还是不太行了，图片显示分辨率太低，另外在 macOS 上也有些小问题。
    - 研究后发现 kitty 可能是更好的选择，切换到 kitty 后体验很好，alacritty 现在沦为备胎。
- 根据评论更新给 esp-idf 提的 PR [fix: create-project & create_component with proper file permission - esp-idf](https://github.com/espressif/esp-idf/pull/11836)
- 修复我 nix-config 配置中的两个 bug:
  - [neovim: smartindent breaks indented comments](https://github.com/ryan4yin/nix-config/issues/4)
    - 顺便给 astronvim 提了个 PR [fix(options): don't set smartindent](https://github.com/AstroNvim/AstroNvim/pull/2136) 修了下这个毛病。
    - 这个问题很烦，之前真是没啥头绪，尝试了修改 tree-sitter.nvim/null-ls.nvim 甚至删掉所有 nix 相关配置，都没用。
    - 然后 7/17 又尝试根据找到的几个可能的参数一个个加上关键问题描述搜索了下，就找到了两个相关 issue，问题瞬间就清晰了。
  - 另一个是上班发现 macOS 上的 wireguard `wg-quick` 命令有毛病，把我网络搞坏了。
    - 问了有 wireguard 经验的同事，他之前就处理过这个问题，很快就帮我确认了问题是 wireguard 停掉后 DNS 解析没更新，导致 DNS 解析挂掉。
    - 解决方案：[wireguard: DNS stop to work after wg-quick down xxx on macOS](https://github.com/ryan4yin/nix-config/issues/5)
- 发现 macOS 上的输入法用着很不顺手，macOS 百度输入法加载了小鹤挂接码后卡得没法用，macOS 官方的又只有双拼。
    - 最后决定用 squirrel 输入法，体验下来是个很棒的想法！
    - 现在我的 Linux 跟 macOS 都使用的同一份小鹤音形 rime 词库，macOS 使用 brew 自动安装 squirrel，Linux 使用 fcitx5-rime，使用体验也完全统一了，感觉非常好！
- 开始看《无职转生》这部动漫，它对应的小说我大概在大三时看过，作者对涩涩的描写有点烦，不过故事真的很棒，当时看完小说就有点怅然若失。
  - 动漫看下来也很棒，感觉还是比较还原原著的。世界观很宏大，有很多不同的景色，人物也很有生命力，主角的成长也很有意思。


### 2023-07-15

- 週六，在家把公司的 Macbook Pro 2020 重裝了一遍系統，新環境完全通過 nix-darwin 安裝，就連大部分的 macOS 系統配置，我也用 nix-darwin 配好了，感覺非常香！
    - GUI APP 主要通過 nix-darwin 的 homebrew 功能安裝。
- 順便把之前一直沒做的 secrets 管理也搞定了，macOS 上的 agenix 比較坑，出了錯也沒打日誌，另外 nix-darwin 的參數跟 NixOS 也有些不一致。爲了解決 agenix 與 nix-darwin 的問題花了大半天的時間。
- 現在感覺我的 nix-config 配置在當前階段很完美地 cover 了我所有的個人配置，包括一些存放在 nix-secrets 私有倉庫中的敏感信息。


### 2023-07-10 - 2023-10-13

- 最近在 NixOS 上搞嵌入式开发，感觉 VSCode 有点力不从心了。它老是想安装自己的环境，但我希望它直接使用我 `nix develop` 在命令行中打开的环境，各种环境毛病。
  - 想了下 neovim 本身就跑在命令行里，可以完美解决这个问题！这是使我尝试切换到 neovim 的主要原因。
- 花一晚上的时间抄了网友的配置，把基础环境配好了，挺漂亮，不过还有许多问题要解决。
  - 比如说 python/yaml/html 等语言只有语法高亮，没有 lsp 语法错误及提示、bufferline 插件没效果，修改过的内容没有高亮提示等。
  - 此外对 neovim 的组合快捷键还不太熟悉，也还从来没在 neovim 这类环境中尝试过调试代码、格式化代码，这都得研究研究。
  - 目前体验很丝滑，响应比 VSCode 快好多，插件生态也非常丰富，非常舒适。感觉把环境调好后，体验会非常好，这玩意儿就跟窗口管理器、NixOS 一样的，不折腾还好，一用上就再也接受不了旧的 IDE 了。
- 最開始考慮到 NixOS 不遵循 FHS，neovim 插件可能會有坑，所以主要是在 GitHub 的各種 nix 配置中查找 neovim 的配置。抄了幾份裸寫的配置後發現太難整了，各種 bug，調得頭疼。
    - 於是開始考慮在 neovim 社區找些現成的配置模板，這中間也[走了些彎路](https://github.com/ryan4yin/nix-config/commit/7cc49c29f1d85f62445eddb49e5d75f6a3865730)
    - 最終發現 AstroNvim 很匹配我需求，但是它默認用 Mason.nvim 裝 lsp 等插件，這些插件在 NixOS 上都用不了，必須改成用 nix 安裝，爲了解決這個問題又折騰了好久。
- 初步配置完成後，發了條 Twitter [最近两天开始从 VSCode 迁移到 Neovim](https://twitter.com/ryan4yin/status/1679176508844445696) 結果意外受歡迎。

{{<figure src="/images/now/2023-07-29_astronvim.webp" title="AstroNvim(Neovim)" width="80%">}}

### 2023-07-08 - 2023-07-09

- 更新了一波 NixOS & Flakes Book 的显示效果，充分利用上 vitepress 的各种功能。
  - 补充了全套站点 favicon，基于 NixOS 官方图标生成的。
  - 补充之前从博客迁移过来时删除掉的几张屏幕截图（好像只有一张）。
  - 为许多代码块的重点代码行添加了高亮，对读者更友好。（vitepress 自带的功能）
  - 基于我常用的桌面壁纸（出自动漫 rolling girls）为小书制作了一个 banner（用 figma 做的），添加在了仓库 README 跟内容的第一页中，很好看。
- 几个月没折腾 MCU 了，尝试了在 NixOS 上使用 ESP-IDF、PlatformIO 进行 MCU 开发。给 ESP-IDF 提了个 PR 修复在 NixOS 上存在的 Bug.
  - ESP-IDF 跟 PlatformIO 的命令行都搞定了，能正常编译烧录。
  - 但是这俩的 VSCode 插件都各种毛病，感觉这类 GUI IDE 还是太偏向初学者了，老喜欢装自己的环境，在 NixOS 这种非 FHS 的机器上就有点水土不服。有点想尝试切换到 neovim.

{{<figure src="/images/now/2023-08-13-nixos-and-flakes-book.webp" title="NixOS & Flakes Book" width="80%">}}

### 2023-07-04

- 新买的 Milk-V Duo 板子到货，晚上久违地拿出了电烙铁把引脚焊上了，然后学习了一波这玩意儿的玩法。
  - 发现它使用 buildroot 生成 rootfs，所以又学习了一波 buildroot 的使用。
  - 这个玩意儿官方 SDK 比较全，打算通过它学习下 RISC-V Linux 相关的知识，尤其是引导部分，然后再继续折腾 LicheePi 4A.

### 2023-06-25 - 2023-07-03

- 持续优化 [nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book) 的内容，主要是英文内容，备受好评的同时也有好几位指出其中存在相当多的语法错误、拼写错误、表达错误...
  - 先后用 copilot chat 与 chatgpt 3.5 优化了一波英文内容，发现 chatgpt 3.5 确实强多了，copilot chat 不适合干这活。
  - 这份文档是我在与读者的沟通中一步步优化的，读者的好评带来的成就感是我更新的最大动力，一些读者的反馈也对它的「进化」产生了很大的帮助。我最初只是想分享一下自己的 NixOS 折腾心得，内容也比较随意，没想到最后却成了一本包含中英双语的开源书籍，国外的阅读量甚至是国内的两倍，而且还得到了许多 stars ，真的完全没预料到，不过很开心。
- LicheePi 4A 的 rootfs 虽然编译出来了，但是死活引导不成功。感觉是 uboot-spl 跟 boot 分区这两个地方的内容有问题，但是 Linux 引导我屁也不懂一个，至今没搞定。
  - 中间尝试了打出镜像用 QEMU 进行测试，但是跑起来打印出 OpenSBI 的日志后就卡住了，CPU 一直有一两个核心跑到 100%，也搞不清楚是咋了。
- 也试着搞了搞 [ryan4yin/nixos-rk3588](https://github.com/ryan4yin/nixos-rk3588) 中的 Rock 5A 以及 OrangePi 5 Plus 支持，没搞定，内核编译不成功...
- 7/1 中午出门吃午饭，大概二十分钟，回来进房间一脚下去全是水，发现家里被淹了。
  - 走进几步发现地上是个排插，吓一跳赶紧把总闸给拉了（万幸水还不深，尤其是几个排插那里地不平，水深都不到 1cm，不然可能直接寄了...）
  - 排查发现是洗衣机水龙头破裂，给关上了，又跟房东沟通，他让我自己把水扫进洗手间，晚上他来给换水龙头。
  - 应该是最近最恐怖的一次经历了，最庆幸的是它是午饭漏的水，就二十分钟回来就发现了，时间比较短水不多，排插也还没漏电...
  - 想起前两天才看过 B 站大猛子说自己之前喝酒误事，水龙头没关，水从 4 楼淹到 1 楼，各种交涉，腻子啥的全整一遍估计得配 10 多万，几年白干...心中只有庆幸。

### 2023-06-23 - 2023-06-24

- 根据前面收到的批评与建议，新建了一个 GitHub 仓库作为用于与社区协作共建此文档：[nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book)，使用 vitepress 搭建了全新的文档站点，同时也更新了所有被指出存在误导的内容。
  - 这此更新花了我一整天的时间，效果非常惊艳，我自己都明显觉得 vitepress 搭建的新文档站索引很齐全很方便，阅读体验比超长的一页博客好太多了。
  - 也再次在 [Reddit](https://www.reddit.com/r/NixOS/comments/14fvz1q/updates_nixos_nix_flakes_a_guide_for_beginners/) [v2ex](https://www.v2ex.com/t/951190#reply9) [0xffff.one](https://0xffff.one/d/1547-nixos-yu-flakes-yi-fen-fei-guan) 等社区以及交流群分享了下，收到了许多 stars.
- 在 LicheePi 4A 群同步了下进展，仍然未能成功编译 rootfs. 意外得到 revy 老师的帮助，在他修了几个内核 bug 后，我成功将 NixOS 的 rootfs 编译了出来！
  - 不过刷到板子上启动不了，看了下发现原来 boot 分区是不能直接用 revyos 的，必须要从 NixOS 生成，解决掉这个问题应该就能启动了。

### 2023-06-21 - 2023-06-22

- 对 [NixOS 与 Flakes 新手入门](https://thiscute.world/posts/nixos-and-flake-basics/) 这篇文章进行了大量更新，并在 [Reddit](https://www.reddit.com/r/NixOS/comments/14fvz1q/updates_nixos_nix_flakes_a_guide_for_beginners/) 上宣传了下。
  - 除了许多好评外，还在 Reddit 与 Discord 上收到一些非常有建设性的批评与建议，简要总结如下：
    - 批评之一是文章太长，阅读困难。与其说它是一篇文章，倒不如说它更像是一本给初学者写的入门书。它不是博客这种简短的读物，而是内容更广泛且更有野心的文档。
    - 批评之二是文章内容包含许多与 NixOS 无关的冗余信息，噪音太多。如果当成博客写这自然无所谓，但是如果想要面对更广泛的 NixOS 用户，那就不合适了。
    - 批评之三是一些内容存在误解，或者说写得比较随意，不够精确，容易误导新人。
  - 忠言逆耳，这些批评虽然让我有一点不舒服，但是都非常有价值。

### 2023-06-17 - 2023-06-18

- 在家整了两天的 [ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a)，试了很多方案，还是没能成功编译出 rootfs...
  - 在 [LicheePi 4A —— 这个小板有点意思（第一部分）](https://litterhougelangley.club/blog/2023/05/27/licheepi-4a-%e8%bf%99%e4%b8%aa%e5%b0%8f%e6%9d%bf%e6%9c%89%e7%82%b9%e6%84%8f%e6%80%9d%ef%bc%88%e7%ac%ac%e4%b8%80%e9%83%a8%e5%88%86%ef%bc%89/) 上留了言，看看大佬是否有时间给我提供些帮助。
  - 编译 NixOS 时发现 RISC-V 架构下基本没有缓存可用，为了解决构建速度问题，意外研究了一波 Nix 的分布式构建，组建了一个 NixOS 分布式构建集群，我得说真的很爽。
  - 还给集群搞了点有意思的「艺名」：[nix-config/hosts/idols](https://github.com/ryan4yin/nix-config/tree/main/hosts/idols)
- 看 [2023 Linux 上海聊天会 - LitterHouge](https://www.bilibili.com/video/BV1FP41117oA/)
  - 一开始只觉得有趣，后面发现我在整的 LP4A 编译，底层用的 revyos，咋视频里有一位昵称就是 revy 呢？然后一查发现都是大佬，revyos 的主要开发者就是视频里这位，膜拜了...
  - [revy](https://github.com/Rabenda) 在各种平台上都用的一个涩涩的头像，结果现实中却是个好胖的大叔，这种反差真的太有意思了 emmmm
  - 另外视频里很健谈的 [xen0n](https://github.com/xen0n) 是 qiniu 的佬，同时也是 Linux loongarch 架构的 reviewer.
    - 但是看他的博客跟视频中的表现，确实给 loongarch 社区做贡献对他的本职工作产生了很大负面影响，而且 2022 年还自付了 5 位数去国际会议上做 loongarch 的宣讲。
      - 从这个方面讲做开源确实是需要付出很多，跟收获的影响力相比，这也并不算微不足道。
      - 尤其是他博客中还提到，给开源贡献意味着在 PR 被合并之前，你会有很大部分精力被消耗在跟 reviewer 的沟通上，你需要注意及时跟进 upstream 更新、及时回复 reviewer 的反馈，长时间去做这种工作，就相当于是在打白工了。本职工作不可避免的会受到影响。
- 看上面 huoge 的视频，通过 B 站推荐意外跳到了 TheCW 的视频里，发现宝藏 UP 主一枚，还加了他的 discord 闲聊群。
  - 上个月水了篇 yabai 的文章，前几天就有网友评论问我是不是 B 站上的 TheCW（因为跟我域名 thiscute.world 有点像），结果今天就发现发现 TheCW 5 月份也出了个介绍 yabai 的视频，确实有那么点缘分在 emmm

### 2023-06-15

- 学习了 Linux 的各种安全技术
  - 主要过了一遍 apparmor/selinux, firejail/bubblewrap, seccomp, 以及 Linux PAM
  - 笔记 [Linux 应用安全](https://github.com/ryan4yin/knowledge/blob/master/linux/Linux%20%E5%BA%94%E7%94%A8%E5%AE%89%E5%85%A8.md)

### 2023-06-13 - 2023-06-14

- 折腾 [ryan4yin/nixos-licheepi4a](https://github.com/ryan4yin/nixos-licheepi4a)，尝试在 LicheePi 4A 上把 NixOS 跑起来。
  - 一开始使用标准工具链 + binfmt 模拟 riscv64 架构进行构建，跑着就睡了，醒来发现在跑了 4h30mins 后构建失败了，卡在 guile 这个包的某个依赖上。
  - 先不论报错，这个构建速度就很不正常，之前用同样的方法构建 aarch64 架构的 NixOS 也只花了 1h25mins
  - 看了下发现 Sipeed 官方的文档是用的交叉编译工具链，所以尝试改成交叉编译，但是改完后 linux-config 遇到了参数报错，还没解决，不知道咋回事。

### 2023-06-10

- 看了点 Linux 内核官方文档，其中对内核开发流程的描述做事的方法论，更多的是与技术无关的，而是一些软技能，比如做事前先与社区沟通、即使发的邮件没人回，也不应该认为没人对你的项目感兴趣而直接放弃，在开发时仍应该持续同步进展、等等诸如此类。文中还举了一些内容很有意义、但是因为未事先沟通或者做对抗式沟通，而在后续付出惨痛代价的项目，其中有些在做了大量修改后才合并到主线，也有些就永远游离在主线之外了。
  - 全文多次提到挫败感、绝望等字词，其实也是在强调如果不按文中所述的方法论去做，很可能会在参与社区的过程中感到挫败，甚至绝望...
- 感觉或许可以定个目标，把 Linux 文档中感兴趣的部分都读一遍。
- 早上起来收到封 FutureMe 的邮件，是 2018 年 6 月的我给 5 年后的我写的。当时我 21 岁，大三，刚闹完一波休学。我爸坐高铁从浙江赶过来，字也签了，跟我说他的任务已经完成了，我想干什么他也阻止不了，让我自生自灭。可最后关头因为一些原因，我还是放弃了...当时真的相当迷茫，不清楚未来会如何。
  - 目前看的话，5 年后我混得好像还行，薪资与工作环境都超出了我当时的预想，甚至有余力在业余随兴趣去做一些有价值的事。
  - 但是现在也有现在的迷茫，近期把大量精力投入到了业余折腾上，对工作越来越提不起兴趣，甚至在考虑要不要辞职休息一段时间。明明工作并不困难，工作压力也不大，但就是提不起兴趣，感觉有点类似以前在学校的状态，有朋友说这是所谓的三年之痒。

### 2023-06-01 - 2023-06-04

- 花了好几天时间研究，在俄罗斯网友的耐心帮助下，终于在 6/4 晚上在 Orange Pi 5 上把 NixOS 跑起来了，还挺有成就感的（虽然现在也不知道拿这板子用来干啥...）
  - 仓库地址 [ryan4yin/nixos-rk3588](https://github.com/ryan4yin/nixos-rk3588)

### 2023-05-31

- 继续研究了一波 OBS，不过没直播，随便录了点东西。
- 研究 OBS 音频卡顿的问题
  - 尝试了重启各种软件（Remmina/OBS）、重启系统，调整录制参数，全都没有用，仍然卡顿。
  - 最终发现把音频录制从 PulseAudio 切换到 ALSA，卡顿问题就解决了。所以能确认是 PulseAudio 的问题。
  - 但是这个 ALSA 驱动貌似只能录制麦克风的声音，无法录制系统输出的声音，所以想要将完整的歌曲输出到 OBS，还存在问题。
  - 为了彻底解决问题，专门研究了一波 NixOS 的几个音频驱动：内核模块 ALSA、新框架 Pipewire，旧的 PulseAudio/JACK，调了一波 NixOS 参数，仅启用 Pipewire，重启后再次用 OBS 自带的 PulseAudio 插件录制，仍然有问题。
  - 最终使用一个社区的 Pipewire 录制插件，完美解决了音频卡顿的问题：[obs-pipewire-audio-capture](https://github.com/dimtpap/obs-pipewire-audio-capture)

### 2023-05-30

- 之前不知道咋的突然对搞直播产生了点兴趣，研究了一波买了个影石 Insta360 Link AI 4K 摄像头，30 号到货，晚上就用它进行了人生第一次直播，有几位朋友前来捧场。
  - 这个云台摄像头确实有点意思，可以自动跟踪人脸，还能手势控制，如果是 Windows 系统，还能安装电脑客户端控制进行俯拍模式。
  - 不过价格也确实感人，618 折后也要 1598。
- 直播的内容，主要是研究如何在 Orange Pi 5 Plus 上把 NixOS 系统跑起来。
- 用 OBS Studio 直播时遇到音频有卡顿的问题，没解决就直接静默了...

### 2023-05-25 - 2023-05-29

- 之前预定的 Rock 5A 到货，另外 Orange Pi 5 Plus 出货也买了一块，以及一块之前 5/8 就到货的 RISC-V 开发版 Licheepi4A，手上多了三块板子，抽时间都刷了个官方系统，随便玩了玩。

### 2023-05-23

- 0xffff 社区想打几个 3D 模型，我又掏出了吃灰几个月的 3D 打印机，发现上次打印时用 PLA 的温度打了 PTEG 材料，把打印头给糊住了。因为打印机摆在地上很难观察到打印头的状况，我调平好几次都有问题，把打印头拆下来才搞明白原因。把打印头加热、用螺丝刀把糊住的 PTEG 材料清理掉，再重新调平好几次，才打出效果不错的 XYZ 测试方块。
  - 尝试用红色 PTEG 打印标准尺寸的 [World's Best CSS Developer" Trophy ](https://www.printables.com/model/163302-worlds-best-css-developer-trophy/files#preview)，等明天看看效果。

### 2023-05-16

- 玩了玩 Github 上流行的 LLM 本地知识库项目 langchain-ChatGLM 跟 5 月份新开源的 DB-GPT
  - langchain-ChatGLM stars 多，但是效果不太行，不太能搜到知识库的内容，而且 ChatGLM-6B 模型的理解能力不太行。
  - DB-GPT 效果还不错，但是它的基础模型 Vicuna-13B 太大了，在 RTX4090 上也动不动就爆显存，问不了复杂的内容。
- 打算后续跟进下 DB-GPT 的进展，同时也学习下 LoRa 微调技术，看看能不能通过把个人知识库训练成 LoRa 来降低对显存的需求，或者完成些别的有趣的任务。

### 2023-05-12

- 昨天没考虑到帖子的流量会下降，目前 upvotes 76，离月榜第一 92 还有点距离，不过现在热度被 Reddit 下调了，估计还需要一段时间才能到达月榜第一的位置。
  - 年榜就不太好说了，或许等上了月榜第一后，能持续获得流量，就有机会杀入年榜前十了。
  - 这个数值也不需要太在意，总之我写了篇好文章，很多人好评感谢，还反馈给我各种修改意见，我已经很开心了～

### 2023-05-11

- [我在 Reddit 上的 NixOS 新手入门帖子](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/) 的反响非常热烈，轻松杀入 NixOS 话题下月榜前三，再过两天拿下月榜 TOP1 感觉没啥悬念，杀入年榜前十感觉问题也不大。
  - 除了一致的好评外，也已经有人开始催更后续内容了...

### 2023-05-10

- 在 NixOS 中文社区某位群友的建议下，将 NixOS 折腾笔记翻译成了英文，并且在 NixOS Froum 跟 Reddit 上都分享了下
  - [Reddit 上才 1 个小时就收到了好几个点赞跟评论](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/)！兴奋得我晚上睡不着，爬起来根据 Reddit 上的反馈，再次爆肝优化文章内容，搞到凌晨 5 点才睡...

### 2023-05-09

- NixOS 的文章整理得差不多了，在 0xffff 社区、NixOS 中文 TG 群、苏洋的折腾群、[V2ex](https://www.v2ex.com/t/938569#reply13) 跟 Twitter 上都分享了下，收获了许多好评反馈，尤其是 NixOS 中文 TG 群的正面反馈，以及 V2ex 上的评论收藏，让我非常开心～
  - 也再次爆肝优化了一波文章内容。

### 2023-05-04 - 2023-05-07

- 研究使用 nix flake 配置 nixos 系统，[nix-config](https://github.com/ryan4yin/nix-config)
  - nixos 确实好用，但是官方文档太烂了，学起来很费劲，从 [nix 笔记提交记录](https://github.com/ryan4yin/knowledge/commits/8b1c5d104da1738d76287c0b50cd36a4caec2512/linux/nix) 上看，从 2022/4/21 折腾到现在已经半个月了，才把系统搞到基本可用的状态。
- 有了 nixos 后，底气足了很多，将桌面环境从 i3wm 切换到 hyprland，确实非常丝滑，hyprland 的动画效果非常棒！
  - 另外目前遇到最大的坑就是 fcitx5 在 wayland 下，无法在 chrome/vscode 下使用的问题，还没解决，这些中文都是通过 alacritty + vim 写的。因为这个原因，都有点想考虑换成 neovim 了...
- 也将 NixOS 折腾笔记整理了下，发了篇新博客文章。不过内容还有点乱，不太拿得出手。

### 2023-04-30 - 2023-05-03

- 研究使用 nix flake 配置 nixos 系统，[nix-config](https://github.com/ryan4yin/nix-config) 发布 v0.0.1

### 2023-04-27

- The Great Gatsby - 10/41

### 2023-04-26

- 工作状态上回来了一点，为了在工作时更专注，避免掉习惯性摸手机、刷 Twitter/V2ex/QQ，重新开始使用 「Forest 专注森林」，它是基于番茄工作法的一款 App，每专注工作一次就可以种一颗树，还有许多树种可选。效果真的不错，确实对我专注编程有帮助。
  - 我上次集中使用还是在 2017 年了，现在登录账号还能看到当时种的大片银杏，有点感慨。
- 游戏
  - 试玩了米忽悠的新游戏「星穹铁道」，还是熟悉的画风跟 UI，制作质量也很高，回合式对战的玩法我本以为会枯燥，不过也还 OK。最重要是动画跟剧情都很在线，总体评价很 OK。
    - 不过我试玩的是安卓版，抗锯齿做得比较拉，打算明天用 RTX4090 玩玩看。
  - 打 VR 游戏，发现昨天调过优化参数后，RTX4090 跑 beta saber，Oculuse Quest 2 的画质参数全调到最高， 5K 120 帧无压力，相当流畅。想着既然这么流畅，又试了试 Air 模式连接，完全感觉不到延迟，画质稍微掉了一点点，不过把 SteamVR 的动态分辨率改成固定的应该能解决。
    - 之前没调 GeForce Experience 参数，效果比这差很多，还有点卡顿，当时就觉得很疑惑，不过后面折腾 Linux 就没怎么玩游戏了...现在才搞明白原来是参数没调优。
  - 总体来说 RTX4090 在调整好显卡参数优化的前提下，不论是 VR 还是 3A 游戏，体验都很丝滑、画质清晰，玩游戏贼爽，确实比我之前的 RTX3070 笔记本好太多了。

### 2023-04-25

- 英语阅读
  - The Great Gatsby - 9/41
  - 最近一个月有点迷茫，状态不对劲，没读啥英语...今天读了两篇 The Greate Gatsby，故事情节都要慢慢回忆...
- 用 RTX4090 玩 Cyperpunk 2077，顶配光追画质（叫啥 onedrive）贼棒，真的非常还原真实环境，在 GeForece Experience 上调了个啥优化参数，帧率得到了很大提升，4K 差不多能稳定在 100 帧，看半天风景。
  - 不过 2077 的碰撞检测还是有点 bug...游戏都出来快三年了还卡 bug...

### 2023-04-24

- Homelab 重新折腾一通后，又打算修复下 Homelab 的 k8s 环境，顺便尝试下 Istio 多集群部署。
  - 折腾一整天，用 kubeadm 部署了个 1.27.0 的 k8s 集群，网络用的 cilium，也搞定了 cert-manager
- 死活搞不定 istio 多集群部署（external-istiod 模式，或者叫 primary-remote 模式）。
- 在新集群上部署了个单集群 istio，尝试了下 [istio with Gateway API](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/#automated-deployment)，感觉还不错。不需要手动部署 istio ingressgateway 了，配置好 Gateway 资源后 istio 会自动部署对应的 deployment 和 service。

### 2023-04-23

- 之前因为做 PVE 虚拟机备份，发现 PVE 的 local 分区默认只有 100G，不够用（当前方案下备份需要临时存储在 local 分区），这次把两台 64G 内存的小主机，local 分区(root 卷)调到了 326G，local-lvm 分区(data 卷)则改为了 633G，目前感觉是个比较好的方案。
- 同时将集群升级到了最新的 Proxmox VE 7.4，想看看能否解决一些遇到的问题。

### 2023-04-21 - 2023-04-22

- 了解了下 nixpkgs，它最大的优势就是：多版本管理，系统可以随时回退到任意一个版本，杜绝系统被搞乱了还原不了的情况。
  - 当然它也有些别的优点：系统可在任何一台机器上还原（可复现）、不存在依赖冲突问题、等等。
- 然后因为尝试在 Endeavour-i3wm 上尝试 sway，发现暂时不咋地，又退回到了 i3wm，然后 firefox 启动就要卡很久，QQ 也莫名奇妙闪退，一怒之下打算换成 NixOS，试试它是不是能帮忙解决这个问题。
- 输出笔记 [knowledge/linux/nix](https://github.com/ryan4yin/knowledge/tree/master/linux/nix) 与配置仓库 [ryan4yin/nix-config（暂时为私有仓库）](https://github.com/ryan4yin/nix-config)

### 2023-04-17

- 又过去一周，真的啥也没干。
- 我的工作状态已经很久不在线了，各种事情能拖就拖，各种拖沓的工作带来的压力使我的业余学习也变得很懈怠。这段时间业余几乎啥也没干，硬件软件都没搞，网络小说倒是看了不少。
- 天依手办到货，很飒～

{{<figure src="/images/now/tianyi-vsinger.webp" title="洛天依 秘境花庭 常服手办" width="60%">}}

### 2023-04-16

- 去听了个 Live House，乐队叫迎春归，青岛的乐队，不过前面许多歌我都觉得一般般，主唱唱功也差了点，全靠架子鼓贝斯烘托。不过末尾几首歌还挺好听的。

### 2023-04-12

- 主机配件全部到货，花了一晚上装机。这是我第一台 PC 主机，之前只拥有过三台笔记本，玻璃橱柜机箱装出来的效果很惊艳，成就感爆棚！
  - 临时装了个鲁大师（娱乐大师）跑了下，排名 99.9604%，也算符合预期，毕竟都选了顶配显卡。

{{<figure src="/images/now/endeavour-rtx4090.webp" title="主机配置" width="60%">}}
{{<figure src="/images/now/rtx4090-pc-1.webp" title="机箱展示" width="60%">}}
{{<figure src="/images/now/rtx4090-pc-2.webp" title="机箱展示" width="60%">}}

### 2023-04-10

- 安装新显示器，调整房间布局，32 寸 4K 显示器就是爽！新房间布局也有点新鲜感。

### 2023-04-09

- 受最近 AI 刺激，又研究了一波显卡，从闲鱼二手 P40 P100 一路看到 V100、4090，看完了 [ML GPU Comparo Spreadsheet of Doom](https://docs.google.com/spreadsheets/d/1Zlv4UFiciSgmJZncCujuXKHwc4BcxbjbSBg71-SdeNk/edit#gid=0) 后就开始看各种装机方案，然后就被海景房主机（侧透玻璃橱窗）迷住了眼，方向开始转变成怎么装机放老婆手办最养眼...
  - 研究了一晚上装机方案，第二天醒来直接全部下单了...
  - CPU/GPU 双 360mm 水冷，B760M+I5-13600KF 板 U 套装，七彩虹 RTX4090 24G 水神，32 寸 4K144Hz 显示器等等，林林总总花了接近 26k，刷新我自己的花钱记录了。
  - 毕竟买的是 4090，那么除了 AI 之外，我当然也很期待它在 VR 与其他 3A 游戏上的表现。

### 2023-04-08

- 搞了个 chatglm-6b int4 量化版，本地用我的拯救者笔记本（16G RAM + RTX3070 8G）玩了下，响应速度感觉可以，确实有一定的上下文联想能力，简单的问题也能解答，但是有点不聪明的样子，内容投毒比较严重。
  - 感觉当个稍微聪明一点的聊天机器人还 OK，但是仅限玩乐，干不了什么实际的工作。如果使用半精度跑估计会好一些，不过手上只有一张 8G 显存的 RTX3070，跑不动。
  - 另外还有个 ChatGLM-130B，根据官方文档描述效果已经接近 GPT-3 了，不过至少也要 4 张 RTX3090 才能跑...贫民只能等 AI 技术继续迭代了。

### 2023-04-07

- 这几天真的啥都没干，光看网络小说去了。
- 工作越来越懈怠，在 v 站上发了篇帖子 [工作快四年了，对工作渐渐失去兴趣](https://www.v2ex.com/t/930343)，倾诉了我兴趣转移、有点想转行的想法。获得了一些 v 友的支持与建议，并且了解到了「职业倦怠」这样一个现象。回想起来大宇也有这样的现象，在工作三年左右，员工辞职的概率会有一个突增。
  - 职业倦怠的定义：你有工作能力，但却丧失了工作动力。
  - [如果工作进入了倦怠期 每天都想辞职 你会选择裸辞 暂停下来休息吗？](https://www.zhihu.com/question/417416656/answer/1943349616)
  - [怎么一步一步走出职业倦怠期？](https://www.zhihu.com/question/465045834/answer/1941141141)
- 我现在的工作可以说是很清闲了，而且现在大环境也不好，因此还是很希望自己能再按部就班地工作一年攒攒钱，同时业余时间系统地学一学嵌入式，然后再考虑转行或者考研。
- 也是是说，还是得把心态摆正啊，不说多么有进取心，至少把本职工作做好吧。
- 听了 [wd 佬](https://github.com/wdvxdr1123)的建议整了个达尔优 A87Pro 天空轴 v3，一番体验这个天空轴 v3 手感确实贼爽、声音也小，感觉可能有点类似静电容了（虽然我没用过静电容 emmm）。
  - 我毕业以来就 19 年跟 20 年分别买过两把 IKBC 的茶轴跟红轴，茶轴放家里了，红轴一直放在公司用。当时国产轴感觉还不太出名，但是现在我聊键盘的朋友都看不上 cherry 轴了，网上搜了下 cheery 轴也有各种品控下降、轴心不稳、杂音大的诟病。
  - 结合朋友推荐，另外看到 v2ex 上聊键盘的朋友也有说天空轴 v3 好用的，还在知乎上也看到有人说这个轴不错，于是就按捺不住心思下单了。到手确实很惊艳，甚至让我再一次喜欢上了打字的感觉！打了几篇小鹤练习群的赛文享受这种飘逸的感觉。

### 2023-03-29

- 买的陆地冲浪板到货了，晚上 11 点半跑到小区外的商业街门口玩到 0 点 40，会一点滑行跟转弯了，不过还不稳当。
<!-- - 跟壁画之家的偶像们一起用网易云「一起听」功能听歌。 -->

### 2023-03-28

- 整理发布了文章 [Linux 上的 WireGuard 网络分析（一）](https://thiscute.world/posts/wireguard-on-linux/)

### 2023-03-27

- 在想什么时候要不考个 EE 的研究生？
  - 一方面是我现在的学历还挺尴尬的，另一方面是我现在对 EE 也比较感兴趣，第三是我现在可以自己供自己读研，不用担心经济问题（前提是不考虑出国，不然我这点工资还真不够...）。
  - 我现在还算有点这样弥补自己学历、追逐梦想的机会，等未来结婚生子就真的没那么容易了，或许真的应该好好考虑这个选项。
  - 但是这个选择也要考虑到现在的考研难度、手上资金情况、未来就业情况，以及自己是不是三分钟兴趣。
  - 总的来说，起码再自学一年硬件，确认了自己的兴趣程度后再考虑这个选项吧。目前得想办法把我对云原生的兴趣再给找回来，现在这状态还挺尴尬的，硬件还没入门，工作也不上心...
  - 反驳：学 EE 可能也没必要考研，现在经济不景气考研的人太多了难度大，另一方面学习终究还是考自己，考个普通普通学校没啥意义，好学校又不是那么容易考的。
- 折腾 WireGuard 协议

### 2023-03-26

- 对用 ESP32 搞一搞 IP-KVM 远程控制产生了点兴趣，研究了一波 USB 协议。
- 发现合宙的 ESP32S3 开发板有个 DVP 摄像头接口，就尝试在上面跑 [esp32-camera](https://github.com/espressif/esp32-camera)，
  - 首先搞了个 demo，根据 [CORE-ESP32-S3 开发板原理图 - LuatOS](https://wiki.luatos.com/chips/esp32s3/hardware.html) 确定引脚
  - 然后就败北了，日志啥的都正常，可 PSRAM 初始化怎么着都失败，找半圈这里说到了 [luatos-esp32s3-camera 拓展板 - 立创开源](https://oshwhub.com/chain01/luatos-esp32s3-camera) 合宙 ESP32S3 的 PSRAM 跟它的摄像头接口是冲突的，需要额外的转接板...
- 今年以来，业余搞硬件搞到有一点失去方向，对工作有点失去兴趣，久违地又感到了些许迷茫。
- 买了个陆地冲浪板，型号是「YATAGA 八咫乌 SFW06 - 双驱 - 32 英寸」，780 大洋，等到货了。
<!-- - 跟壁画之家的偶像们一起用网易云「一起听」功能听歌。 -->

### 2023-03-24

- 继续用平衡训练板联系侧身跟换前后脚，能感觉到比昨天有明显进步，而且因为很有意思，也很有动力坚持下去~
- 英语学习连续第三天

<!-- - 跟壁画之家的偶像们一起用网易云「一起听」功能听歌。 -->

### 2023-03-23

- 被 Copilot X 小小震撼了下，花了 100 美刀买了个 1 年的订阅，价格不贵，希望能切实帮我提升写代码的效率。
- 之前的 ESP32CAM 没玩起来，又新买了块，今天到货试了下，发现同样的配置方法，烧录一切正常了，又换回旧板子，也正常了...看来大概率还是上次跑了 `yay -Syyu` 更新了内核，但是没重启导致的问题。
- 又坚持学习了两天英语~
- 平衡训练板第三天，开始练习侧身跟换前后脚，保持平衡的难度瞬间大了很多，但是也很有意思。
  - 从右脚在后换成左脚在前后，练习时明显感觉到腰部肌肉酸痛。显然是因为我是右撇子，左腿与相关的肌肉缺乏锻炼。

### 2023-03-21

- 冲浪训练用的平衡板到货了，音箱放上音乐玩这个板子很有意思。如果坚持练，感觉今年还可以去冲几波浪，肯定不会像上次那么狼狈了。
- 矽速科技的几块板子也到货了，花时间把手上已有的矽速板子 demo 全跑了一遍。
  - 笔记记录在 [electrical-engineering/sipeed](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/sipeed)
  - 上手现在 5 块矽速的板子了，如果算上还没出货的两块 LicheePi4A 那就是 7 块。最近 Maix II Dock 降价还搞得我手痒难耐，但是其实完全没啥需求去买，光手上现有的板子就够我玩好久了...
- 英语学习又鸽了一周多了...

### 2023-03-19

- 大腿肌肉酸痛，下楼梯是个瘸的。昨晚用筋膜枪按摩了几波，看来没能帮忙缓解乳酸堆积，或者说没筋膜枪就比现在更严重了。
- 买了块陆地冲浪平衡板，在家练练平衡感，今年或许会再去冲个浪~
- 还在 Sipeed 家整了一块入门级 FPGA 开发板——荔枝糖 Nano 9K、一块 M1s Dock、跟一块 RISC-V 的板子 Longan Nano
  - 不过它家都是周一才发货，这让我感觉这是家好公司，但同时又觉得好慢...
- 继续读「[Linux Device Drivers Development 2nd Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition)」

### 2023-03-18

- 跟公司几位小伙伴约了一波深圳东西冲海岸线穿越。
  - 翻了下记录，上次穿越这条海岸线是 2021 年 8 月，时隔一年多了。不过上次只到天文台就沿着大马路下山了，一个是因为我运动得少，太累了，另外也是没发现天文台另一边是海岸栈道。
  - 这次是 3 月份，没 8 月份那么热，喝的水少很多，速度也快了很多，三个半小时走完整条海岸线。
  - 因为是第二次走，那种被美景震撼的感觉要少一点，不过有一点跟上次感觉一样——风景最好的就是上下天文台的那段路。

### 2023-03-12

- 跟朋友去游泳，算是今年最剧烈的一次运动了...
  - 注：预计下周去深圳东西冲穿越海岸线，那将是一项更大的挑战。去年到玩得贼爽（去年是 6 月份去的，很晒、很热、喝了很多水）。
- 继续学 Linux 驱动开发，读了「Linux Driver Development for Embedded Processors 2nd Edition」跟「[Linux Device Drivers Development 2nd Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition)」，发现第二本书更新，而且写得更好。
  - 了解了一个 Hello World 内核模块是怎么编写、编译、加载、卸载的。

### 2023-03-11

- 把我用剩的电话卡、以及玩电子的一些元件打包寄给了我妹玩。
- 野火的 Linux 驱动开发教程看了感觉没啥乐趣，不知道从何下手，于是开始读「Linux Driver Development for Embedded Processors 2nd Edition」
  - 根据书中内容跨平台编译 Raspberry Pi 4 的 Linux 内核失败，换成跟着 [Cross-Compiling the Kernel - Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/computers/linux_kernel.html#cross-compiling-the-kernel) 编译，一次成功，使用 5900HX 全量编译总用时 6 分钟多一点。

### 2023-03-10

- 折腾好久，终于编译成功了鲁班猫的 Linux 固件。
  - 官方建议用 Ubuntu 18.04 作为编译环境，一开始我在 Arch Linux 上用 Ubuntu 容器跑编译，但是因为内核太新了（6.3）导致装各种包都得重新编译，python 相关的东西全是跑单线程编译，慢得吐血。好不容易装完，它又需要 qemu 虚拟化，容器里跑这个貌似有毛病。
  - 还有个问题是，使用百度云下载的离线 SDK 跟着官方文档走，可能是 Github 代码有过 force push，导致 `repo sync -c` 总是会报错，但是不影响编译，只是用不上最新的代码，可以先忽略。
  - 于是改成在 Homelab 上跑 Ubuntu 18.04 虚拟机，8 核 16 线程全给它的情况下，完成一次全量编译也要 25 分钟，速度慢的一些点是一些中间步骤只能用上单核，以及许多下载安装包相关的工作得看网速情况。

### 2023-03-09

- 买的野火鲁班猫 0 无线版到了，这是野火基于 RK3566 的一块开发板
  - 它的设计类似树莓派，但是开放的资料非常全，包含 SoC 原厂的各种文档、SDK 驱动开发包、核心板封装库，还提供许多免费的在线文档，内容包含 Linux 内核编译部署、Linux 驱动开发、嵌入式 QT 开发等等
- 读完了「The Moon and Sixpence」

### 2023-03-08

- 买的 MAIX-III AXera-Pi（爱芯派）跟 Maix Zero M0s 到货，晚上简单玩了玩爱芯派，M0s 看了点资料得用博流智能提供的 SDK，后面再折腾。
  - 可能是送的 32G TF 卡 IO 不行，这块板子的 NPU 感觉性能还可以，但是 CPU 跟 IO 都有点拉，跑个 `pip3 list` 都要卡老半天。
  - 为了快速编译，根据 ax-pipeline 文档配了下本地交叉编译工具链（没用 docker），没啥坑，编译速度也挺快的。

### 2023-03-07

- 最近接触荔枝派相关的东西比较多，就研究了一波 Sipeed 公司的所有产品，做了个笔记 [electrical-engineering/sipeed](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/sipeed)
- 心动了，下单了 599 大洋的 MAIX-III AXera-Pi AX620A（爱芯派） + 21.9 大洋的 Maix M0s MCU.
- 又觉得 MCU 玩了不少时间了，想进阶搞 Linux 驱动开发，爱芯派看上去不太合适，又下单一块 214 大洋的野火鲁班猫 0 无线版。
- 跟妹妹聊了下，她正在学 Python 跟 C 语言，而且对电子也挺感兴趣的，于是整理了一份手上多余的万用表、面包板、杜邦线、传感器、显示屏、MCU、SBC 等材料，打算找时间寄回家给她玩。

### 2023-03-02 - 2023-03-06

- 翻出好久前买的 TFT 显示屏，折腾用 ESP32 驱动它。
- 整理了一波嵌入式相关的[社区论坛、博客公众号等](https://www.zhihu.com/question/352385472/answer/2921790194)，主要是自己玩缺点意思，想找些志同道合的朋友交流~
- 发布文章[EE 入门（二） - 使用 ESP32 + SPI 显示屏绘图、显示图片、跑贪吃蛇](https://thiscute.world/posts/ee-basics-2-esp32-display/)

### 2023-02-28

- 闲鱼 290 大洋买的 One Plus 5 6G+64G 到货了，CPU 是 Snapdragon 835，刷了 Ubuntu Touch 系统简单玩了下，有点意思。

### 2023-02-22 - 2023-02-25

- 搞定了 Stable-Diffusion-WebUI Docker 容器，简单玩了玩效果比较拉。然后抄了些网上的提示词，效果确实很惊艳。还试玩了 sd-webui-controlnet，画出来的人物确实跟 controlnet 参考图非常相似，很强。不过玩了一波又没啥兴趣了，不太想花很多精力去折腾它。话眭如此，下一篇文章确实可以考虑试试用 AI 配图。
- 今年刚开年，各大公司就都开始搞 AI，资本开始入场。AI 绘画的 ControlNet 模型又给这个方向带来全新的变化，可以预见 AI 在未来几年很可能逐渐取代部分中低端工作。
- 今年过去两个月了，这两个月都没怎么学英语...

### 2023-02-21

- 折腾一晚上终于用 STM32 点亮了 TFT 液晶屏，以及搞定了使用 printf 打印日志到串口。
  - [ryan4yin/learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)

### 2023-02-16 - 2023-02-20

- 180 大洋买的 ESP-Drone 到货，玩了一晚上直接机翼折损...而且即使在室内也很不稳定不好操控，感觉是因为飞控算法不行或者芯片性能太弱。
- 学了一波 ESP-IDF 编程，发现封装得比较彻底，只需要调上层接口就行，整了整 WS2812 彩灯控制，代码简单，也很有意思。
- ESP-IDF 的文档虽然也挺多，可学起来没啥方向感。于是又开始跟野火 STM32 HAL 库的教程，学了一波发现 STM32 比 ESP32 要复杂很多，STM32 HAL 更接近底层，学起来有很多地方一知半解，但是感觉学会了进步也会更大。
- 在用 STM32 HAL 整 TFT 显示器，目前还未成功...
- 2/18 在深圳南头古城跟 0xFFFF 线下约了一波茶会，谈天说地随便聊了聊。
- 还整了一波本地跑 Stable-Diffusion-WebUI Docker 容器，遇到点问题，我 RTX 3070 8G 跑到 5G 后内存就不涨了，日志也没任何更新，暂时放弃折腾。

### 2023-02-15

- 看上了 [esp-drone](https://github.com/espressif/esp-drone) 这个项目，为了轻松入门，直接在淘宝上买了一套 esp-drone 的散件打算自己组装，花了 180 大洋（感觉自己折腾的话估计只要 100，不过效果不好说）。
- 翻出了之前买的两块 esp32 开发板，开始学习 vscode + esp-idf 进行 esp32 程序开发，发现它用到的技术确实比较杂（C + CMake + Kconfig + Python），门槛比 STM32 要高，不过对我而言还 OK。
  - 用 ESP32 整了个 WS2812 跑马灯，比较有意思~

### 2023-02-11

- 研究 Homelab 备份与数据同步方案，写了点笔记 [数据备份与同步策略](https://github.com/ryan4yin/knowledge/blob/master/homelab/%E6%95%B0%E6%8D%AE%E5%A4%87%E4%BB%BD%E4%B8%8E%E5%90%8C%E6%AD%A5.md)
- 研究了下 Linux 远程桌面方案：SSH X11 Forwarding 跟 xrdp，意外发现在客户端是 Linux 的情况下，SSH X11 Forwarding 配置与使用居然如此简单而且效果也非常好！只需要改一行 sshd 配置，客户端直接 `ssh -X user@host` 就 ok 了~
- 研究在 orangepi5(rk3558s) 上跑 AI 任务，写了点笔记 [demos_rk3588](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/rk3588)

### 2023-02-10

- 重新研究了下 Proxmox VE，更新了之前写的 Proxmox 使用指南
- 发现 Windows Server 跑的 NAS 数据传输还是不太快，晚上整了一波 Promox VE 的 PCIe 直通想把 USB 控制器直通给 Windows，结果完全失败...
  - 输出半成品笔记 [Proxmox PCI 直通.md](https://github.com/ryan4yin/knowledge/blob/master/homelab/Proxmox%20PCI%20%E7%9B%B4%E9%80%9A.md)

### 2023-02-09

- datacenter 版的 win server 2022 有毛病老是挂掉重启，换了 standard 版重装系统
- 为了用上 windows 的 smb/iscsi 黑科技，我不得不考虑把存了 2T 数据的 btrfs 盘改成 ntfs/refs 文件系统
  - 研究了一波 refs 发现不太行，而且 linux 完全不支持这个系统，有风险，还是决定用 ntfs
  - 首先考虑把 btrfs 磁盘挂载进 wsl2，再用 rsync 同步到 ntfs 盘，结果新装的 wsl2 又有毛病，`wsl --mount` 报错...
  - 第二个方案成功了——两个盘都挂载到 ubuntu 虚拟机用 rsync 拷贝到 ntfs 磁盘。
    - 但是拷贝时发现 linux 的 ntfs 驱动性能不行，将就着用了。
    - 睡前想到另一个方案：直接用开源驱动把 btrfs 挂在 win server 下再对拷，据此查到了 winbtrfs，但是查了下据依云等大佬说，比较灵车，我又不敢用了。
    - 朋友表示 btrfs 用 winbtrfs 挂为只读在 windows 上 copy，可能速度会好很多（喷的就是 ntfs 的 Linux 驱动）。

### 2023-02-08

- 最近买的 Orange Pi 5 到手玩了两天了，确实有点意思。
  - 其核心 RK3558S 还有 NPU，我找了 rockchip 官方 demo [rknpu2](https://github.com/rockchip-linux/rknpu2) 玩了玩，挺有意思的。
  - 瑞芯微官方的 [rknn-toolkit2](https://github.com/rockchip-linux/rknn-toolkit2) 好像得安装在 x64 PC 上，模型得用它进行转换后才能跑在 rk3558s 上面，具体还没研究。玩板子顺便还能玩一玩 AI，挺不错~
- UM560 炸掉的 asgard 固态 2023/2/7 换新到货了，装好机后重新加入 PVE 集群，重建挂掉的 k3s 集群，调整 NAS 架构，又更新相关的笔记，反正一番折腾。
- 确定改用 Windows Server 2022 DataCenter 跑 NAS 系统，因为它的 SMB 协议很多黑科技，速度快。硬盘盒就直接映射到这台 Windows Server 里面。
  - 一个盘给 Windows 当 SMB 硬盘用，用了 ReFS 文件系统
  - 另一个盘绑定到 wsl2 给 docker 容器用，仍然决定用 btrfs 文件系统
- 遇到一个问题是 windows server 2022 因为没嵌套虚拟化，装不了 hyper-v，一番查找发现，将 vm cpu 类型从 kvm64 改为 host 就解决了
- 另一个问题是 wsl2 ubuntu 无法启动，通过 [WSL/issues/5440](https://github.com/microsoft/WSL/issues/5440#issuecomment-778660156) 中提到的方法解决了——创建 `~/.wslconfig`，通过它禁用 wsl 嵌套虚拟化功能。
- 再一个问题就是通过 wsl2 访问 btrfs 等 linux 系的文件系统
  - 根据官方文档 [在 WSL 2 中装载 Linux 磁盘](https://learn.microsoft.com/zh-cn/windows/wsl/wsl2-mount-disk)，通过 `GET-CimInstance -query "SELECT * from Win32_DiskDrive"` 查询磁盘 ID，再通过 `wsl --mount \\.\PHYSICALDRIVE2 --bare` 挂载即可.
  - 注意事项是，必须以 `--bare` 裸磁盘的方式挂载进 wsl2 中，再手动在 wsl2 中通过 `sudo mount /dev/sdb1 xxx` 的方式挂载磁盘，否则会报错。(这个文件系统挂载，重启后大概会消失，还得研究下怎么搞成自动挂载)
- 仍然没找到英语学习的节奏，年后基本没学几天英语。
- 搞硬件的热情又上来了，特别是 RK3558S 这颗 SOC 感觉挺好玩的样子，加了 OrangePi5 的群见了市面（群友们玩得都挺有意思）。

### 2023-02-03

- 折腾 Homelab 时，主力节点 UM560 固态翻车了，是才用了三个月的 Asgard 512G SSD，颗粒是长江存储的。走京东售后了
  - 上次翻车是 2022-11-02 炸了根光威弈 Pro 1T，这也没隔多久啊...

![](/images/now/nvme-critial-medium-error.webp "2022-11-02 翻车记录，系统无法启动，这是显示器输出内容")
![](/images/now/nvme-device-not-ready.webp "2023-02-03 翻车记录，系统能启动但是文件损坏，这是 dmesg 信息")

### 2023-01-30

- 健身 30mins: day 2

### 2023-01-29

- 过年期间放下了所有的学习，测了词汇量也停留在了 6500，今天开始恢复学习
- 更新 Learn English Again 这篇文章，并在 0xffff 社区发贴分享
- 买的健身器材到了，现有设备瑜伽垫、握力器、脚蹬拉力器、弹力健身棒。没计算啥卡路里，简单定下了每天运动 30mins 的小目标，等坚持一个月再看看体重有无改善吧，现在感觉有点虚胖。
- 健身 30mins: day 1
  - 玩了玩几样健身设备，感觉还挺有意思的。练习强度也不大，不累，算是体验阶段。后续再慢慢加量。
- 英语阅读
  - The Moon and Sixpence - 23/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习 - 145/270 (漏打卡 62 天)

### 2023-01-14

- 跟 0xFFFF 社区的朋友们约饭，账单金额也很讨喜：666
- 想清楚了一个问题：其实经历曲折一点，对个人的心态是有帮助的。经历太过一帆风顺了，后期反而很可能遇到瓶颈
  - 我觉得我搞技术的职业生涯发展这么顺利，跟高中、大学期间的这么多曲折经历，关系挺大的
  - 之前也在跟人的一些沟通中提到过一点——「我在学校时负面情绪就已经爆棚了，刚工作时虽然起点贼低，但是相比在学校时心理压力小太多了，反而感觉到获得了解放。工作上的负面情绪对我而言可能就像毛毛雨，而做自己喜欢的事带来的成就感则是我在学校时从未体会过的。这种从业前期的经历使我更在意成就感、同事的认可而非某些负面情绪。」
  - 古人总结过这个叫「塞翁失马，焉知非福」，现代也有很多人叫「吃亏是福」。

### 2023-01-11

- 一晚上没接告警，工作真告一段落了。
- 然后就是失去了继续学习英语、折腾其他东西的东西，感觉真的需要停一下，修养一段时间，恢复下被新冠、咳嗽、以及 K8s 升级这个大任务消耗掉的精气神。

### 2023-01-10

- 又一次完成 K8S 集群升级，虽然还是跟去年一样鸭梨山大，写了好多小脚本做各种升级处理，还加了四五个小时班，搞到 11 点...但总体上比 2021 年那一次顺畅多了，一次完成。没去年那么多加戏——升级回滚好几次，API 可用率还各种抖动。
  - 这次升级这么顺利，我的个人经验是其一，内部平台的多集群支持是其二，今年我做的网关的改造降低了流量迁移难度是其三，最后同事也仍然跟去年一样为我提供了重要帮助。话不多说，感恩各位同事。
  - 再立个 flag，2023 年我要推动公司的 K8s 集群升级流程迭代，告别「依靠个人经验，一路做各种骚操作解决各种意料之外的疑难杂症，最终完成升级」的「石器时代」，实现半自动化。
  - 突然想到，十多万 QPS 的流量迁移，好像有点像是所谓的「给飞行中的飞机换引擎」，瞬间变得高大上了。
- 抗过今晚，明天再收个尾，2022 年的工作就告一段落了。好像心中的一块石头落了地。

### 2023-01-06 - 2023-01-08

- 跟同事交流后对工作与个人的成长有了些新的感悟，结合之前与领导聊过的个人职业发展，感觉人生也是各种 trade-off 啊。
  - 回想我在大宇这两年，第一年的工作其实很不顺利，没找到方向，被 leader 推着往前瞎走，到年底的时候发现，之前做的事因为兼容性问题要全部推翻...感觉随时要提桶跑路。leader 说过几次组里我的适应速度最慢，工作上一直没磨合好。
  - 真的有运气的成分，各种原因年底本来领导属意由另一位同事执行的 EKS 升级工作，因为他有其他事忙不过来，又交给了我（我之前已经做过一次升级，出了问题回退了）。在年底终于硬着头皮把它搞定了，这拯救了我去年年底的绩效。
- 晚上跟朋友聊天吹水时想到一点，「博客评论，本质上也是社交。你给人家评论，人家也会回访，看到好的文章也不介意评论一句。」所以许多生活博客评论数是最多的，这说明博主花了很多精力在维系这个圈子。就我的体验看，适当的博客社交感觉还挺不错的。
- 回顾了一下很久前做过的心里评测记录，有一点比较重要的我一直没改掉：「过度分享」，我好像一直比较喜欢分享自己的种种，但如果过了某个界限，也并不是一件好事。
  - 还是要把握住核心，说话前多动下脑子想下倾听者的感受，少说点废话，也少分享些别人不感兴趣的内容。

### 2023-01-05

- 最近看到两个 ext4 文件系统相关的帖子，知识点刚好能串起来，都跟 ext4 文件系统的 htree 这个 B 树索引有关：
  - [文件系统作为缓存时的路径生成方案 - 0xffff.one 社区](https://0xffff.one/d/1395-wen-jian-xi-tong-zuo-wei-huan-cun)
  - [在有大量长文件名小文件的情况下需要启用 large_dir - @Manjusaka_Lee](https://twitter.com/Manjusaka_Lee/status/1610690497550643206)

### 2023-01-02

- 英语阅读
  - The Moon and Sixpence - 15/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习 - 118/270 (漏打卡 36 天)
- 词汇量测试：新的一年，测了一下词汇量，测了三次选了结果低的一次，词汇量为 **6583**
  {{<figure src="/images/now/2023-01-02-test-your-vocabulary-result.webp" title="2023-01-02 词汇量测试结果：6583 词" width="70%">}}
  {{<figure src="/images/now/2022-12-19-test-your-vocabulary-result.webp" title="2022-12-19 词汇量测试结果：6300 词" width="40%">}}
  {{<figure src="/images/learn-english-again/2022-11-17-test-your-vocabulary-result.webp" title="2022-11-17 词汇量测试结果：5600 词" width="65%">}}
  {{<figure src="/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp" title="2022-10-18 词汇量测试结果：5100 词" width="40%">}}
- 电子电路
  - 3D 打印机折腾了几天，暂时放下了。
  - 电子电路的话，跨年前后这几天学完了《51 单片机自学笔记》的汇编部分，然后直接开始通过野火的视频教程学 STM32，跟着写了一些 C 代码挺有意思的。
  - 输出内容有两个仓库：[learn-8051-asm](https://github.com/ryan4yin/learn-8051-asm) 与 [learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)
    {{<figure src="/images/now/8051-display-2023.webp" title="8051 汇编 - 数码管显示 2023" width="70%">}}
    {{<figure src="/images/now/8051-led-dancing.gif" title="8051 汇编 - LED 编舞..." width="70%">}}
    {{<figure src="/images/now/8051-display-start-seconds.gif" title="8051 汇编 - 数码管动态显示秒数" width="70%">}}
  - 简单看了下 ESP32/ESP8266 开发发现用的是 C++，感觉可能得花一两天时间学下 C++ 的 Class 相关逻辑，不然代码不好懂。
  - 另外也在考虑玩一玩 STM32 Linux 驱动开发以及 Rust 嵌入式开发，这两个大概是新的一年希望点亮的技能了。

哦还有连续三年蝉联我年度歌手的天依同学，截图放这里纪念一下：

{{<figure src="/images/now/netease-cloud-music-2022-singer-of-ryan4yin.webp" title="我的网易云年度歌手" width="50%">}}

