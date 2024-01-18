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

> Twitter 上 @Manjusaka_Lee 等大佬喜欢写周报，不过我不太喜欢周报的形式。因为周报的标题本身没啥意义，而要看其中的内容却得一个个点进去看，这对我自己回顾过往的学习、工作、生活，体验非常不方便。
> 我比较喜欢类似「一镜到底」的阅读体验，所以我采用这种单页的方式来记录我的日常。（基于同样的理由，我将博客单页展示的文章数量上限调整成了 `1000`）

全部历史记录：[/history](/history/)


### 2024-01-18

- 学习了 Emacs Magit 拓展的用法，确实挺香的。

{{<figure src="/images/now-2024/2023-01-18_nixos-book-1k-stars.webp" title="NixOS 小书满 1k stars 了！" width="80%">}}

### 2024-01-17

- 注销印象笔记账号，使用 evernote-backup 跟 evernote2md 两个工具将笔记迁移到了一个私有 Git 仓库，用 GitJournal 在手机上查看编辑笔记。
- 考虑到笔记跟其他各种数据的安全性，买了一堆 U 盘，用于重要数据的双备份，打算全部 LUKS 加密存储，LUKS 解密密钥交叉保存在不同的 U 盘上。
  - 简单的说就是，一定要两个不同的 U 盘都在手上才能解密其中的数据。
  - 以前对安全的考虑不多，曾经把各种重要账号的 backup_code 直接保存在百度云盘或 onedrive 上，一些密码经过简单的转换后直接写在印象笔记中。隐患挺大。这次加密备份方案上线过程中，也打算同步更新一次所有的 backup codes 以及主要账号的密码。

{{<figure src="/images/now-2024/2023-01-17_evernote-china-delete-account.webp" title="注销了从大一用到现在的 evernote 印象笔记，数据都迁移到了 GitJournal" width="70%">}}
{{<figure src="/images/now-2024/2023-01-17_buy-usb-keys-for-security.webp" title="买了一堆 U 盘，用于 GPG 密钥等数据的双备份，LUKS 加密存储" width="70%">}}

### 2023-01-16

- 偶尔想起，在 NixOS TG 群里提到我电脑重启经常报 /dev/xxx is not a LUKS devices，NickCao 立马问我是不是有多个磁盘，问题马上就定位到了，万能的 NickCao!

### 2024-01-15

- 读了一遍 Vim 的官方文档 <https://vimhelp.org/>，深入学习了 Vim 本身的使用。
- 又过了一遍 Helix 的 `:tutor`，Helix 确实精简非常多，键位设计上 `motion` 前置用着确实更舒服一点，值得一用。

### 2024-01-14

- 对 2023 年的年终总结做了些更新，加了些图片，补充了对 2024 年工作上的展望，技术上的期望也做了些调整，更明确、精简了。
- 以 2024 年的新状态与目标为参照，更新了 /now 页面
- 参加 Emacs 深圳线下聚会，作为一个玩 Emacs 不到一个月的新手，去听听大佬们的分享，学习一下，也感受下极客圈的氛围哈哈。
    - 印象深刻的有一个用 Framework 模块化笔记本的大佬，坐我旁边，还有一个日常用 Streamdeck 的佬（也用 Nix，日常写 Elixir）
    - 三个人分享，他们命令行操作全都贼六，基本不用鼠标。
    - 因为发现大家都对 Nix 比较感兴趣，甚至有不少朋友曾经试用过但被劝退了。我也借此机会分享了下 NixOS/nix-darwin 的使用，优缺点。以及为什么我现在在尝试 Guix（我就是因为折腾 Guix，安装文档装了个 Emacs 不会用，这才入了 Emacs 的坑）。

### 2024-01-10 - 2024-01-13

- 完成了将密码管理全部迁移到 password-store 的工作，现在 NixOS/macOS 跟 Android 上都可以使用了，非常香！
- 继续微调 emacs 配置，之前加了 lsp-bridge 后语法高亮各种毛病，它的配置还是太复杂了，我换回了 lsp-mode. doom-emacs 下 lsp-mode 完全是开箱即用的，慢一点但配置起来不费脑子！
- 熟悉 orgmode 语法，用起来还是挺多不习惯，尤其是它的转义问题，我研究了一整天，现在还是有几个「[未解之迷](https://github.com/ryan4yin/guix-config/blob/079bd61/ORGMODE.org)」...
- 发现 NixOS 内置了 Guix 支持 [nixos/guix: init](https://github.com/NixOS/nixpkgs/pull/264331)，装上玩了一波。
- 跟领导聊完了年终绩效，以及明年的工作展望。看起来我明年需要深入搞一搞 AIGC 的规模化，有机会深入搞下新鲜火热的 AI 技术，还挺期待的。
  - RTX 4090 虽然吃灰大半年，但现在国内已经禁售了... 或许今年还能发挥一下它的作用

### 2024-01-09

- [pass : 密码管理本不复杂](https://nyk.ma/posts/password-store/): 前两天学 Emacs 看到了这篇文章，给我带来了对密码管理的新思路！
- 然后今天研究一天的 password-store 跟 gpg 的使用，把所有原本保存在 Firefox 中的密码全部迁移到了 password-store + GnuPG 加密，并 push 到 GitHub 的一个私有仓库上。太香了！

### 2024-01-01 - 2024-01-07

- 继续尝鲜 DoomEmacs，对其配置做了大量的迭代。
  - 折腾好多天了，目前遇到的问题都解决得差不多了，很漂亮用着也挺舒服。现在最头疼的问题还剩：
    - Emacs 的代码格式化跟 Neovim 不一致，两边会把代码格式化来格式化去... 导致我无法在同一项目上混用两个编辑器
- 学会了使用 parinfer 这个插件写 lisp/scheme，确实非常爽，它会根据缩进情况全自动地添加或删除括号，使用户完全不用关心括号的问题。难怪被人说这个插件使写 lisp 就跟写 python 一样了 emmm
- 把 Makefile 换成了 Justfile，简单清爽了不少，还结合 nushell 脚本做了些代码重构
- 学习整理了下编辑器的基础知识：Vim 键位速查表、现代化编辑器的LSP/TreeSitter 介绍与对比、Formatter/Linter 等工具的区别等等。
  - <https://github.com/ryan4yin/nix-config/tree/main/home/base/desktop/editors>
- 周六到逛了半天公园，可能是天气好、然后山里空气、风景也不错，再听着歌，简直开心到起飞！
- 周日早上挂了医院的过敏反应科，想做个过敏源筛查，做了皮试跟血检，三天后才能出结果。

### 2024-01-01

- 发布了 [2023 年年终总结](/posts/2023-summary/)

