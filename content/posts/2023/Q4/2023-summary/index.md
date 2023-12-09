---
title: "2023 年年终总结"
date: 2023-12-30T18:00:45+08:00
lastmod: 2023-12-30T18:00:45+08:00

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
  - 延续去年底开始对 Homelab 与嵌入式硬件的兴趣，继续折腾 Proxmox VE 集群，以及 stm32 / orange pi / esp32 等嵌入式硬件，成果大概有这些：
  - 简单玩了玩 Stable-Diffusion-WebUI 跟 sd-webui-controlnet，抄了些网上的提示词，效果确实很惊艳。不过玩了一波就没啥兴趣了，不太想花很多精力去折腾它。
- 3 月
  - 仍旧是折腾各种嵌入式设备，新入手了 Sipeed MAIX-III AXera-Pi AX620A（爱芯派）+ Maix M0s MCU, 野火鲁班猫 0，荔枝糖 Nano 9K、M1s Dock、Longan Nano 等一堆大小开发板，折腾各种 OS 编译、嵌入式开发的内容。
  - 读完了「The Moon and Sixpence」
  - 跟朋友到游泳馆游泳，算是开年以来最剧烈的一次运动...
  - 跟同事们约着一起穿越了东西冲海岸线，这是我第三次走这条线，风景仍旧很美，当然也走得挺累...
  - 买了块冲浪训练平衡板，练习了一段时间，挺有意思。
  - 读了一点 [Linux Device Drivers Development 2nd Edition](https://github.com/PacktPublishing/Linux-Device-Driver-Development-Second-Edition)
- 4 月
  - 在业余爱好上投入的精力越来越多，工作上相对的越来越懈怠，感觉碰到了瓶颈，但搞不明白该怎么突破。
  - 听了 [wd 佬](https://github.com/wdvxdr1123)的建议整了个达尔优 A87Pro 天空轴 v3，一番体验这个天空轴 v3 手感确实贼爽、声音也小，开始将它作为主力键盘。
  - 搞了个 chatglm-6b int4 量化版，本地用我的拯救者笔记本（16G RAM + RTX3070 8G）玩了下，响应速度感觉可以，确实有一定的上下文联想能力，简单的问题也能解答，但是有点不聪明的样子，内容投毒比较严重。
  - 玩 AI 联想到涛显卡，看嗨了就直接整了套新主机新显示器（我的第一台 PC 主机，以前只买过笔记本电脑），玻璃侧透机箱，RTX 4090，双水冷，组装了大半夜，后面又折腾了好几天，机箱直接当手办展示柜了，效果相当惊艳！缺点一是套下来貌似花了两万多...
    {{<figure src="/images/now/endeavour-rtx4090.webp" title="主机配置" width="60%">}}
    {{<figure src="/images/now/rtx4090-pc-1.webp" title="机箱展示" width="60%">}}
    {{<figure src="/images/now/rtx4090-pc-2.webp" title="机箱展示" width="60%">}}
  - 去听了个 Live House，乐队叫迎春归，青岛的乐队，不过前面许多歌我都觉得一般般，主唱唱功也差了点，全靠架子鼓贝斯烘托。不过末尾几首歌还挺好听的。
  - 天依手办到货，很飒～
    {{<figure src="/images/now/tianyi-vsinger.webp" title="洛天依 秘境花庭 常服手办" width="60%">}}
  - 新主机装了个 Endeavour OS 遇到些奇怪的问题，一怒之下决定换 OS，刚好朋友提到了 NixOS，听说过这玩意儿能做到「可复现」，直接就在 Homelab 里开了个 NixOS 虚拟机开始折腾，由此开始了我的 NixOS 之旅。
  - 用新主机试玩了米忽悠的新游戏「星穹铁道」，还是熟悉的画风跟 UI，制作质量也很高，回合式对战的玩法我本以为会枯燥，不过也还 OK。最重要是 4090 画质够高，游戏的动画跟剧情也都很在线，总体评价很 OK。
  - 用新主机连 Quest 2 打 VR 游戏，发现做过参数优化后，RTX4090 跑 beta saber，Quest 2 的画质参数全调到最高， 5K 120 帧无压力，相当流畅。
  - 用 RTX4090 玩 Cyperpunk 2077，顶配光追画质（叫啥 onedrive）贼棒，真的非常还原真实环境，在 GeForece Experience 上调了个啥优化参数后，4K 差不多能稳定在 100 帧，看半天风景。
- 5 月
  - 月初，在虚拟机里折腾了大半个月 NixOS 后，成功地用几条简单的命令，在我的新主机上复现了整个 NixOS 环境，那一刻真的超级开心，半个月的努力终于得到了回报！
  - 在新主机上成功复现出我的 NixOS 环境后，紧接着发布了我的系统配置 [ryan4yin/nix-config/v0.0.2)](https://github.com/ryan4yin/nix-config/releases/tag/v0.0.2) 以及这大半个月的学习笔记 [NixOS 与 Nix Flakes 新手入门](https://thiscute.world/posts/nixos-and-flake-basics/)，然后事情就变得越来越有趣起来了！
