---
title: "NixOS 与 Nix Flakes 新手入门"
date: 2023-05-04T15:19:28+08:00
lastmod: 2023-06-04T14:25:15+08:00
draft: false

resources:
  - name: "featured-image"
    src: "screenshot_2023-05-07-21-21.webp"

tags: ["NixOS", "Nix", "Flakes", "Linux", "DevOps"]
categories: ["tech"]
series: ["NixOS 与 Nix Flakes"]
series_weight: 1

lightgallery: true

comment:
  utterances:
    enable: true
  waline:
    enable: false

code:
  # whether to show the copy button of the code block
  copy: true
  # the maximum number of lines of displayed code by default
  maxShownLines: 300
---

> 本文的目标 NixOS 版本为 22.11，Nix 版本为 2.13.3，在此环境下 Nix Flakes 仍然为实验性功能。

## 更新日志 {#updates}

- 2023/6/21
  - 在 `八、Nixpkgs 的高级用法` 补充 callPackage、override 与 overlays 的使用细节。
  - 在 `六-6` 补充了一些我常用的命令行工具配置。
  - 添加 `五-14` 一节，介绍 if...then...else... 语句。
  - 在文末添加新的一节「Flakes 何时会成为稳定特性？」
- 2023/6/6
  - 在 `七、Nix Flakes 的使用` 一节中添加 flake 的 inputs 与 outpus 使用案例。
- 2023/6/4
  - 使用 `nix profile history` 替换掉旧指令 `nix-env --list-generations`
  - 使用 `nix store gc` 替换掉旧指令 `nix-collect-garbage`
- 2023/6/1
  - 更新「六-9」一节，为了避免 [1000 instances of nixpkgs](https://discourse.nixos.org/t/1000-instances-of-nixpkgs/17347) 描述的 nixpkgs 实例泛滥问题，改为仅在全局创建 nixpkgs 实例。
- 2023/5/21
  - 补充 overlays 一节的内容。
  - 移除「九、使用 Nix Flakes 打包应用」，这部分可能会放在后续文章中介绍。
  - 「六-4」一节补充了一个通过 flakes 数据源安装程序的例子。

## 零、为什么选择 Nix {#why-nix}

好几年前就听说过 Nix 包管理器，它用 Nix 语言编写配置来管理系统依赖，此外基于 Nix 包管理器设计的 Linux 发行版 NixOS，还能随时回滚到任一历史状态。
虽然听着很牛，但是不仅要多学一门语言，装个包还得写代码，当时觉得太麻烦就没研究。
但是最近搞系统迁移遇到两件麻烦事，使我决定尝试下 Nix.

第一件事是在新组装的 PC 主机上安装 EndeavourOS（Arch Linux 的一个衍生发行版），因为旧系统也是 EndeavourOS 系统，安装完为了省事，我就直接把旧电脑的 Home 目录 rsync 同步到了新 PC 上。
这一同步就出了问题，所有功能都工作正常，但是视频播放老是卡住，firefox/chrome/mpv 都会卡住，网上找各种资料都没解决，还是我灵光一闪想到是不是 Home 目录同步的锅，清空了 Home 目录，问题立马就解决了...后面又花好长时间从旧电脑一点点恢复 Home 目录下的东西。

第二件事是，我最近想尝鲜 wayland，把桌面从 i3wm 换成了 sway，但是因为用起来区别不明显，再加上诸多不便（hidpi、sway 配置调优都要花时间精力），嫌麻烦就还是回退到了 i3wm。结果回退后，每次系统刚启动时，有一段时间 firefox/thunar 等 GUI 程序会一直卡着，要大概 1 分钟后才能正常启动...

发生第二件事时我就懒得折腾了，想到归根结底还是系统没有版本控制跟回滚机制，导致出了问题不能还原，装新系统时各种软件包也全靠自己手工从旧机器导出软件包清单，再在新机器安装恢复。就打算干脆换成 NixOS.

我折腾的第一步是在我 Homelab 上开了台 NixOS 虚拟机，在这台虚拟机里一步步调试，把我物理机的 EndeavourOS i3 配置迁移到 NixOS + Flakes，还原出了整个桌面环境。
在虚拟机里搞定后问题就不大了，直接备份好我办公电脑的 Home 目录、软件清单，然后将系统重装为 NixOS，再 git clone 我调试好的 NixOS 配置，改一改硬盘挂载相关的参数，额外补充下 Nvidia 显卡相关的 NixOS 配置，最后一行命令部署配置。几行命令就在我全新的 NixOS 系统上还原出了整个 i3 桌面环境跟我的常用软件，那一刻真的很有成就感！

NixOS 的回滚能力给了我非常大的底气——再也不怕把系统搞挂了，于是我前几天我又进一步迁移到了 hyprland 桌面，确实比 i3 香多了，它的动画效果我吹爆！（在以前 EndeavourOS 上我肯定是不太敢做这样的切换的，原因前面已经解释过了——万一把系统搞出问题，会非常麻烦。）

> 补充：v2ex 上有 v 友反馈 btrfs 文件系统的快照功能，也能提供类似的回滚能力，而且简单很多。我研究了下发现确实如此，btrfs 甚至也可以像 NixOS 一样配置 grub 从快照启动。所以如果你只是想要系统回滚能力，那么基于 btrfs 快照功能的 [btrbk](https://github.com/digint/btrbk) 也是一个不错的选择。当然如果你仍然对 Nix 感兴趣，那学一学也绝对不亏，毕竟 Nix 的能力远不止于此，系统快照只是它能力的一部分而已～

{{< figure src="./screenshot_2023-05-07-21-21.webp" caption="我当前的 NixOS 桌面" >}}

在学了大半个月的 NixOS 与 Nix Flakes 后，我终于将我的 PC 从 EndeavouOS 系统切换到了 NixOS，这篇文章就脱胎于我这段时间的折腾笔记，希望能对你有所帮助～

前因后果交代完毕，那么下面开始正文！

## 一、Nix 简介 {#nix-intro}

Nix 包管理器，跟 DevOps 领域当前流行的 pulumi/terraform/kubernetes 类似，都是声明式配置管理工具，用户需要在某些配置文件中声明好期望的系统状态，而 Nix 负责达成目标。区别在于 Nix 的管理目标是软件包，而 pulumi/terraform 的管理目标是云上资源。

> 简单解释下什么是「声明式配置」，它是指用户只需要声明好自己想要的结果——比如说希望将 i3 桌面替换成 sway 桌面，Nix 就会帮用户达成这个目标。用户不需要关心底层细节（比如说 sway 需要安装哪些软件包，哪些 i3 相关的软件包需要卸载掉，哪些系统配置或环境变量需要针对 sway 做调整、如果使用了 Nvidia 显卡 Sway 参数要做什么调整才能正常运行等等），Nix 会自动帮用户处理这些细节。

基于 Nix 构建的 Linux 发行版 NixOS，可以简单用 OS as Code 来形容，它通过声明式的 Nix 配置文件来描述整个操作系统的状态。

NixOS 的配置只负责管理系统层面的状态，用户目录不受它管辖。有另一个重要的社区项目 home-manager 专门用于管理用户目录，将 home-manager 与 NixOS、Git 结合使用，就可以得到一个完全可复现、可回滚的系统环境。

因为 Nix 声明式、可复现的特性，Nix 不仅可用于管理桌面电脑的环境，也有很多人用它管理开发编译环境、云上虚拟机、容器镜像构建，Nix 官方的 [NixOps](https://github.com/NixOS/nixops) 与社区的 [deploy-rs](https://github.com/serokell/deploy-rs) 都是基于 Nix 实现的运维工具。

> Home 目录下文件众多，行为也不一，因此不可能对其中的所有文件进行版本控制，代价太高。一般仅使用 home-manager 管理一些重要的配置文件，而其他需要备份的文件可以用 rsync/synthing 等手段做备份同步，或者用 [btrbk](https://github.com/digint/btrbk) 之类的工具对 home 目录做快照。

### Nix 的优点 {#nix-advantages}

- 声明式配置，Environment as Code，可以直接用 Git 管理配置，只要配置文件不丢，系统就可以随时还原到任一历史状态（理想情况下）。
  - 这跟一些编程语言中 cargo.lock/go.mod 等文件锁定依赖库版本以确保构建结果可复现的思路是一致的。
  - 与 Docker 相比，Dockerfile 实际是命令式的配置，而且也不存在版本锁这样的东西，所以 Docker 的可复现能力远不如 Nix.
- 高度便捷的系统自定义能力
  - 通过改几行配置，就可以简单地更换系统的各种组件。这是因为 Nix 将底层的复杂操作全部封装在了 nix package 包中，只给用户提供了简洁且必要的声明式参数。
  - 而且这种修改非常安全，例证之一是有 v 友表示「[nixos 切换不同桌面非常简单干净，而且很安全，我就经常 gnome/kde/sway 来回换着用。](https://www.v2ex.com/t/938569#r_13053251)」
- 可回滚：可以随时回滚到任一历史环境，NixOS 甚至默认将所有旧版本都加入到了启动项，确保系统滚挂了也能随时回退。所以 Nix 也被认为是最稳定的包管理方式。
- 没有依赖冲突问题：因为 Nix 中每个软件包都拥有唯一的 hash，其安装路径中也会包含这个 hash 值，因此可以多版本共存。
- 社区很活跃，第三方项目也挺丰富，官方包仓库 nixpkgs 贡献者众多，也有很多人分享自己的 Nix 配置，一遍浏览下来，整个生态给我一种发现新大陆的兴奋感。

{{< figure src="./nixos-bootloader.avif" caption="NixOS 启动项中列出了所有历史版本，图来自 [NixOS Discourse - 10074](https://discourse.nixos.org/t/how-to-make-uefis-grub2-menu-the-same-as-bioss-one/10074)" >}}

### Nix 的缺点 {#nix-disadvantages}

- 学习成本高：如果你希望系统完全可复现，并且避免各种不当使用导致的坑，那就需要学习了解 Nix 的整个设计，并以声明式的方式管理系统，不能无脑 `nix-env -i`（这类似 `apt-get install`）。
- 文档混乱：首先 Nix Flakes 目前仍然是实验性特性，介绍它本身的文档目前比较匮乏。 其次 Nix 社区绝大多数文档都只介绍了旧的 `nix-env`/`nix-channel`，想直接从 Nix Flakes 开始学习的话，需要参考大量旧文档，从中提取出自己需要的内容。另外一些 Nix 当前的核心功能，官方文档都语焉不详（比如 `imports` 跟 Nixpkgs Module System），想搞明白基本只能看源码了...
- ~~包数量比较少~~：撤回下这一条，官方宣称 nixpkgs 是有 [80000+](https://search.nixos.org/packages) 个软件包，使用下来确实绝大部分包都能在 nixpkgs 里找到，体验还是不错滴。
- 比较吃硬盘空间：为了保证系统可以随时回退，nix 默认总是保留所有历史环境，这非常吃硬盘空间。虽然可以定期使用 `nix-collect-garbage` 来手动清理旧的历史环境，也还是建议配置个更大的硬盘...
- 报错信息比较隐晦：一般的报错提示还是比较清楚的，但是遇到好几次依赖版本有问题或者传参错误提示不出原因，`--show-trace` 直接输出一堆的内部堆栈，都花了很长时间才定位到，通过升级依赖版本或者修正参数后问题解决。
  - 猜测导致这个问题的原因有两个，一是 Nix 是动态语言，各种参数都是运行时才确定类型。二是我用到的 flake 包的错误处理逻辑写得不太好，错误提示不清晰，一些隐晦的错误甚至通过错误堆栈也定位不到原因。

### 简单总结下 {#nix-simple-summary}

总的来说，我觉得 NixOS 适合那些有一定 Linux 使用经验与编程经验，并且希望对自己的系统拥有更强掌控力的开发者。

另外一条信息：在开发环境搭建方面 Nix 与相对流行的 [Dev Containers](https://containers.dev/) 也有些竞争关系，它们的具体区别还有待我发掘~

## 二、安装 {#install-nix}

Nix 有多种安装方式，支持以包管理器的形式安装到 MacOS/Linux/WSL 三种系统上，Nix 还额外提供了 NixOS ——一个使用 Nix 管理整个系统环境的 Linux 发行版。

我选择了直接使用 NixOS 的 ISO 镜像安装 NixOS 系统，从而最大程度上通过 Nix 管理整个系统的环境。

安装很简单，这里不多介绍，仅列一下我觉得比较有用的参考资料：

- 国内镜像源说明：<https://mirrors.bfsu.edu.cn/help/nix/>

1. [Nix 的官方安装方式](https://nixos.org/download.html): 使用 bash 脚本编写, 目前（2023-04-23）为止 `nix-command` & `flakes` 仍然是实验性特性，需要手动开启。
   1. 你需要参照 [Enable flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) 的说明启用 `nix-command` & `flakes`
   2. 官方不提供任何卸载手段，要在 Linux/MacOS 上卸载 Nix，你需要手动删除所有相关的文件、用户以及用户组
2. [The Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer): 第三方使用 Rust 编写的 installer, 默认启用 `nix-command` & `flakes`，并且提供了卸载命令。

## 三、Nix Flakes 与旧的 Nix {#nix-flakes-and-old-nix}

Nix 于 2020 年推出了 `nix-command` & `flakes` 两个新特性，它们提供了全新的命令行工具、标准的 Nix 包结构定义、类似 cargo/npm 的 `flake.lock` 版本锁文件等等。这两个特性极大地增强了 Nix 的能力，因此虽然至今（2023/5/5）它们仍然是实验性特性，但是已经被 Nix 社区广泛使用，是强烈推荐使用的功能。

目前 Nix 社区的绝大多数文档仍然只介绍了传统 Nix，不包含 Nix Flakes 相关的内容，但是从可复现、易于管理维护的角度讲，旧的 Nix 包结构与命令行工具已经不推荐使用了，因此本文档也不会介绍旧的 Nix 包结构与命令行工具的使用方法，也建议新手直接忽略掉这些旧的内容，从 `nix-command` & `flakes` 学起。

这里列举下在 `nix-command` & `flakes` 中已经不需要用到的旧的 Nix 命令行工具与相关概念，在查找资料时，如果看到它们直接忽略掉就行：

1. `nix-channel`: nix-channel 与 apt/yum/pacman 等其他 Linux 发行版的包管理工具类似，通过 stable/unstable/test 等 channel 来管理软件包的版本。
   1. Nix Flakes 在 flake.nix 中通过 inputs 声明依赖包的数据源，通过 flake.lock 锁定依赖版本，完全取代掉了 nix-channel 的功能。
2. `nix-env`: 用于管理用户环境的软件包，是传统 Nix 的核心命令行工具。它从 nix-channel 定义的数据源中安装软件包，所以安装的软件包版本受 channel 影响。通过 `nix-env` 安装的包不会被自动记录到 Nix 的声明式配置中，是完全脱离掌控的，无法在其他主机上复现，因此不推荐使用。
   1. 在 Nix Flakes 中对应的命令为 `nix profile`
3. `nix-shell`: nix-shell 用于创建一个临时的 shell 环境
   1. 在 Nix Flakes 中它被 `nix develop` 与 `nix shell` 取代了。
4. `nix-build`: 用于构建 Nix 包，它会将构建结果放到 `/nix/store` 路径下，但是不会记录到 Nix 的声明式配置中。
   1. 在 Nix Flakes 中对应的命令为 `nix build`
5. ...

## 四、NixOS 的 Flakes 包仓库 {#nixos-flakes-repo}

跟 Arch Linux 类似，Nix 也有官方与社区的软件包仓库：

1. [nixpkgs](https://github.com/NixOS/nixpkgs) 是一个包含了所有 Nix 包与 NixOS 模块/配置的 Git 仓库，其 master 分支包含最新的 Nix 包与 NixOS 模块/配置。
1. 比如 [qq](https://github.com/NixOS/nixpkgs/tree/master/pkgs/applications/networking/instant-messengers/qq) 就直接包含在 nixpkgs 中了
1. [NUR](https://github.com/nix-community/NUR): 类似 Arch Linux 的 AUR，NUR 是 Nix 的一个第三方的 Nix 包仓库，算是 nixpkgs 的一个增补包仓库。
1. 这些常用国产软件，都可以通过 NUR 安装：
1. [qqmusic](https://github.com/nix-community/nur-combined/blob/master/repos/xddxdd/pkgs/uncategorized/qqmusic/default.nix)
1. [wechat-uos](https://github.com/nix-community/nur-combined/blob/master/repos/xddxdd/pkgs/uncategorized/wechat-uos/default.nix)
1. [dingtalk](https://github.com/nix-community/nur-combined/blob/master/repos/xddxdd/pkgs/uncategorized/dingtalk/default.nix)
1. 更多程序，可以在这里搜索：[Nix User Repositories](https://nur.nix-community.org/)
1. Nix Flakes 也可直接从 Git 仓库中安装软件包，这种方式可以用于安装任何人提供的 Flakes 包

此外一些没有 Nix 支持或者支持不佳的软件，也可以考虑通过 Flatpak 或者 AppImage 的方式安装使用，这两个都是在所有 Linux 发行版上可用的软件打包与安装手段，详情请自行搜索，这里就不介绍细节了。

## 五、Nix 语言基础 {#nix-language}

> https://nix.dev/tutorials/first-steps/nix-language

Nix 语言是 Nix 的基础，要想玩得转 NixOS 与 Nix Flakes，享受到它们带来的诸多好处，就必须学会这门语言。

Nix 是一门比较简单的函数式语言，在已有一定编程基础的情况下，过一遍这些语法用时应该在 2 个小时以内，本文假设你具有一定编程基础（也就是说写得不会很细）。

这一节主要包含如下内容：

1. 数据类型
2. let...in... with inherit 等特殊语法
3. 函数的声明与调用语法
4. 内置函数与库函数
5. inputs 的不纯性（Impurities）
6. 用于描述 Build Task 的 Derivation
7. Overriding 与 Overlays
8. ...

先把语法过一遍，有个大概的印象就行，后面需要用到时再根据右侧目录回来复习。

### 1. 基础数据类型一览 {#basic-data-types}

下面通过一个 attribute set （这类似 json 或者其他语言中的 map/dict）来简要说明所有基础数据类型：

```nix
{
  string = "hello";
  integer = 1;
  float = 3.141;
  bool = true;
  null = null;
  list = [ 1 "two" false ];
  attribute-set = {
    a = "hello";
    b = 2;
    c = 2.718;
    d = false;
  }; # comments are supported
}
```

以及一些基础操作符（普通的算术运算、布尔运算就跳过不介绍了）：

```nix
# 列表拼接
[ 1 2 3 ] ++ [ 4 5 6 ] # [ 1 2 3 4 5 6 ]

# 将 // 后面的 attribut set 中的内容，全部更新到 // 前面的 attribute set 中
{ a = 1; b = 2; } // { b = 3; c = 4; } # 结果为 { a = 1; b = 3; c = 4; }

# 逻辑隐含，等同于 !b1 || b2.
bool -> bool
```

### 2. let ... in ... {#let-in}

Nix 的 `let ... in ...` 语法被称作「let 表达式」或者「let 绑定」，它用于创建临时使用的局部变量：

```nix
let
  a = 1;
in
a + a  # 结果是 2
```

let 表达式中的变量只能在 `in` 之后的表达式中使用，理解成临时变量就行。

### 3. attribute set 说明 {#attribute-set}

花括号 `{}` 用于创建 attribute set，也就是 key-value 对的集合，类似于 JSON 中的对象。

attribute set 默认不支持递归引用，如下内容会报错：

```nix
{
  a = 1;
  b = a + 1; # error: undefined variable 'a'
}
```

不过 Nix 提供了 `rec` 关键字（recursive attribute set），可用于创建递归引用的 attribute set：

```nix
rec {
  a = 1;
  b = a + 1; # ok
}
```

在递归引用的情况下，Nix 会按照声明的顺序进行求值，所以如果 `a` 在 `b` 之后声明，那么 `b` 会报错。

可以使用 `.` 操作符来访问 attribute set 的成员：

```nix
let
  a = {
    b = {
      c = 1;
    };
  };
in
a.b.c # 结果是 1
```

`.` 操作符也可直接用于赋值：

```nix
{ a.b.c = 1; }
```

此外 attribute set 还支持一个 has attribute 操作符，它可用于检测 attribute set 中是否包含某个属性，返回 bool 值：

```nix
let
  a = {
    b = {
      c = 1;
    };
  };
in
a?b  # 结果是 true，因为 a.b 这个属性确实存在
```

has attribute 操作符在 nixpkgs 库中常被用于检测处理 `args?system` 等参数，以 `(args?system)` 或 `(! args?system)` 的形式作为函数参数使用（叹号表示对 bool 值取反，是常见 bool 值运算符）。

### 4. with 语句 {#with-statement}

with 语句的语法如下：

```nix
with <attribute-set> ; <expression>
```

`with` 语句会将 `<attribute-set>` 中的所有成员添加到当前作用域中，这样在 `<expression>` 中就可以直接使用 `<attribute-set>` 中的成员了，简化 attribute set 的访问语法，比如：

```nix
let
  a = {
    x = 1;
    y = 2;
    z = 3;
  };
in
with a; [ x y z ]  # 结果是 [ 1 2 3 ], 等价于 [ a.x a.y a.z ]
```

### 5. 继承 inherit ... {#inherit}

`inherit` 语句用于从 attribute set 中继承成员，同样是一个简化代码的语法糖，比如：

```nix
let
  x = 1;
  y = 2;
in
{
  inherit x y;
}  # 结果是 { x = 1; y = 2; }
```

inherit 还能直接从某个 attribute set 中继承成员，语法为 `inherit (<attribute-set>) <member-name>;`，比如：

```nix
let
  a = {
    x = 1;
    y = 2;
    z = 3;
  };
in
{
  inherit (a) x y;
}  # 结果是 { x = 1; y = 2; }
```

### 6. ${ ... } 字符串插值 {#string-interpolation}

`${ ... }` 用于字符串插值，懂点编程的应该都很容易理解这个，比如：

```nix
let
  a = 1;
in
"the value of a is ${a}"  # 结果是 "the value of a is 1"
```

### 7. 文件系统路径 {#file-system-path}

Nix 中不带引号的字符串会被解析为文件系统路径，路径的语法与 Unix 系统相同。

### 8. 搜索路径 {#search-path}

> 请不要使用这个功能，它会导致不可预期的行为。

Nix 会在看到 `<nixpkgs>` 这类三角括号语法时，会在 `NIX_PATH` 环境变量中指定的路径中搜索该路径。

因为环境变量 `NIX_PATH` 是可变更的值，所以这个功能是不纯的，会导致不可预期的行为。

在这里做个介绍，只是为了让你在看到别人使用类似的语法时不至于抓瞎。

### 9. 多行字符串 {#multi-line-string}

多行字符串的语法为 `''`，比如：

```nix
''
  this is a
  multi-line
  string
''
```

### 10. 函数 {#nix-function}

函数的声明语法为：

```nix
<arg1>:
  <body>
```

举几个常见的例子：

```nix
# 单参数函数
a: a + a

# 嵌套函数
a: b: a + b

# 双参数函数
{ a, b }: a + b

# 双参数函数，带默认值。问号后面的是参数的默认值
{ a ? 1, b ? 2 }: a + b

# 带有命名 attribute set 作为参数的函数，并且使用 ... 收集其他可选参数
# 命名 args 与 ... 可选参数通常被一起作为函数的参数定义使用
args@{ a, b, ... }: a + b + args.c
# 如下内容等价于上面的内容,
{ a, b, ... }@args: a + b + args.c

# 但是要注意命名参数仅绑定了输入的 attribute set，默认参数不在其中，举例
let
  f = { a ? 1, b ? 2, ... }@args: args
in
  f {}  # 结果是 {}，也就说明了 args 中包含默认值

# 函数的调用方式就是把参数放在后面，比如下面的 2 就是前面这个函数的参数
a: a + a 2  # 结果是 4

# 还可以给函数命名，不过必须使用 let 表达式
let
  f = a: a + a;
in
  f 2  # 结果是 4
```

#### 内置函数 {#built-in-function}

Nix 内置了一些函数，可通过 `builtins.<function-name>` 来调用，比如：

```nix
builtins.add 1 2  # 结果是 3
```

详细的内置函数列表参见 [Built-in Functions - Nix Reference Mannual](https://nixos.org/manual/nix/stable/language/builtins.html)

#### import 表达式 {#import-expression}

`import` 表达式以其他 Nix 文件的路径作为参数，返回该 Nix 文件的执行结果。

`import` 的参数如果为文件夹路径，那么会返回该文件夹下的 `default.nix` 文件的执行结果。

举个例子，首先创建一个 `file.nix` 文件：

```shell
$ echo "x: x + 1" > file.nix
```

然后使用 import 执行它：

```nix
import ./file.nix 1  # 结果是 2
```

#### pkgs.lib 函数包 {#pkgs-lib}

除了 builtins 之外，Nix 的 nixpkgs 仓库还提供了一个名为 `lib` 的 attribute set，它包含了一些常用的函数，它通常被以如下的形式被使用：

```nix
let
  pkgs = import <nixpkgs> {};
in
pkgs.lib.strings.toUpper "search paths considered harmful"  # 结果是 "SEARCH PATHS CONSIDERED HARMFUL"
```

可以通过 [Nixpkgs Library Functions - Nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#sec-functions-library) 查看 lib 函数包的详细内容。

### 11. 不纯（Impurities） {#impurities}

Nix 语言本身是纯函数式的，是纯的，「纯」是指它就跟数学中的函数一样，同样的输入永远得到同样的输出。

Nix 有两种构建输入，一种是从文件系统路径等输入源中读取文件，另一种是将其他函数作为输入。

**Nix 唯一的不纯之处在这里：从文件系统路径或者其他输入源中读取文件作为构建任务的输入**，这些输入源参数可能没变化，但是文件内容或数据源的返回内容可能会变化，这就会导致输入相同，Nix 函数的输出却可能不同——函数变得不纯了。

> Nix 中的搜索路径与 `builtins.currentSystem` 也是不纯的，但是这两个功能都不建议使用，所以这里略过了。

### 12. Fetchers {#fetchers}

构建输入除了直接来自文件系统路径之外，还可以通过 Fetchers 来获取，Fetcher 是一种特殊的函数，它的输入是一个 attribute set，输出是 Nix Store 中的一个系统路径。

Nix 提供了四个内置的 Fetcher，分别是：

- `builtins.fetchurl`：从 url 中下载文件
- `builtins.fetchTarball`：从 url 中下载 tarball 文件
- `builtins.fetchGit`：从 git 仓库中下载文件
- `builtins.fetchClosure`：从 Nix Store 中获取 Derivation

举例：

```nix
builtins.fetchurl "https://github.com/NixOS/nix/archive/7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"
# result example => "/nix/store/7dhgs330clj36384akg86140fqkgh8zf-7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"

builtins.fetchTarball "https://github.com/NixOS/nix/archive/7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"
# result example(auto unzip the tarball) => "/nix/store/d59llm96vgis5fy231x6m7nrijs0ww36-source"
```

### 13. Derivations {#derivations}

一个构建动作的 Nix 语言描述被称做一个 Derivation，它描述了如何构建一个软件包，它的构建结果是一个 Store Object.

Store Object 的存放路径格式为 `/nix/store/<hash>-<name>`，其中 `<hash>` 是构建结果的 hash 值，`<name>` 是它的名字。路径 hash 值确保了每个构建结果都是唯一的，因此可以多版本共存，而且不会出现依赖冲突的问题。

`/nix/store` 被称为 Store，存放所有的 Store Objects，这个路径被设置为只读，只有 Nix 本身才能修改这个路径下的内容，以保证系统的可复现性。

在 Nix 语言的最底层，一个构建任务就是使用 builtins 中的不纯函数 `derivation` 创建的，我们实际使用的 `stdenv.mkDerivation` 就是它的一个 wrapper，屏蔽了底层的细节，简化了用法。

### 14. if...then...else... {#if-then-else}

if...then...else... 用于条件判断，它是一个有返回值的表达式，语法如下：

```nix
if 3 > 4 then "yes" else "no" # 结果为 "no"
```

也可以与 let...in... 一起使用：

```nix
let
  x = 3;
in
  if x > 4 then "yes" else "no" # 结果为 "no"
```

## 六、以声明式的方式管理系统 {#declarative-system-management}

> https://nixos.wiki/wiki/Overview_of_the_NixOS_Linux_distribution

了解了 Nix 语言的基本用法之后，我们就可以开始使用 Nix 语言来配置 NixOS 系统了。NixOS 的系统配置路径为 `/etc/nixos/configuration.nix`，它包含系统的所有声明式配置，如时区、语言、键盘布局、网络、用户、文件系统、启动项等。

如果想要以可复现的方式修改系统的状态（这也是最推荐的方式），就需要手工修改 `/etc/nixos/configuration.nix` 文件，然后执行 `sudo nixos-rebuild switch` 命令来应用配置，此命令会根据配置文件生成一个新的系统环境，并将新的环境设为默认环境。
同时上一个系统环境会被保留，而且会被加入到 grub 的启动项中，这确保了即使新的环境不能启动，也能随时回退到旧环境。

另一方面，`/etc/nixos/configuration.nix` 是传统的 Nix 配置方式，它依赖 `nix-channel` 配置的数据源，也没有任何版本锁定机制，实际无法确保系统的可复现性。
**更推荐使用的是 Nix Flakes**，它可以确保系统的可复现性，同时也可以很方便地管理系统的配置。

我们下面首先介绍下通过 NixOS 默认的配置方式来管理系统，然后再过渡到更先进的 Nix Flakes.

### 1. 使用 `/etc/nixos/configuration.nix` 配置系统 {#configuration-nix}

前面提过了这是传统的 Nix 配置方式，也是当前 NixOS 默认使用的配置方式，它依赖 `nix-channel` 配置的数据源，也没有任何版本锁定机制，实际无法确保系统的可复现性。

简单起见我们先使用这种方式来配置系统，后面会介绍 Flake 的使用。

比如要启用 ssh 并添加一个用户 ryan，只需要在 `/etc/nixos/configuration.nix` 中添加如下配置：

```nix
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).
{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # 省略掉前面的配置......

  # 新增用户 ryan
  users.users.ryan = {
    isNormalUser = true;
    description = "ryan";
    extraGroups = [ "networkmanager" "wheel" ];
    openssh.authorizedKeys.keys = [
        # replace with your own public key
        "ssh-ed25519 <some-public-key> ryan@ryan-pc"
    ];
    packages = with pkgs; [
      firefox
    #  thunderbird
    ];
  };

  # 启用 OpenSSH 后台服务
  services.openssh = {
    enable = true;
    permitRootLogin = "no";         # disable root login
    passwordAuthentication = false; # disable password login
    openFirewall = true;
    forwardX11 = true;              # enable X11 forwarding
  };

  # 省略其他配置......
}
```

这里我启用了 openssh 服务，为 ryan 用户添加了 ssh 公钥，并禁用了密码登录。

现在运行 `sudo nixos-rebuild switch` 部署修改后的配置，之后就可以通过 ssh 密钥远程登录到我的这台主机了。

这就是 NixOS 默认的声明式系统配置，要对系统做任何可复现的变更，都只需要修改 `/etc/nixos/configuration.nix` 文件，然后运行 `sudo nixos-rebuild switch` 部署变更即可。

`/etc/nixos/configuration.nix` 的所有配置项，可以在这几个地方查到：

- 直接 Google，比如 `Chrome NixOS` 就能找到 Chrome 相关的配置项，一般 NixOS Wiki 或 nixpkgs 仓库源码的排名会比较靠前。
- 在 [NixOS Options Search](https://search.nixos.org/options) 中搜索关键字
- 系统级别的配置，可以考虑在 [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration) 找找相关文档
- 直接在 [nixpkgs](https://github.com/NixOS/nixpkgs) 仓库中搜索关键字，读相关的源码。

### 2. 启用 NixOS 的 Flakes 支持 {#enable-nix-flakes}

与 NixOS 默认的配置方式相比，Nix Flakes 提供了更好的可复现性，同时它清晰的包结构定义原生支持了以其他 Git 仓库为依赖，便于代码分享，因此更建议使用 Nix Flakes 来管理系统配置。

但是目前 Nix Flakes 作为一个实验性的功能，仍未被默认启用。所以我们需要手动启用它，修改 `/etc/nixos/configuration.nix` 文件，在函数块中启用 flakes 与 nix-command 功能：

```nix
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).
{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # 省略掉前面的配置......

  # 启用 Nix Flakes 功能，以及配套的新 nix-command 命令行工具
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  environment.systemPackages = with pkgs; [
    git  # Nix Flakes 通过 git 命令从数据源拉取依赖，所以必须先安装好 git
    vim
    wget
    curl
  ];

  # 省略其他配置......
}
```

然后运行 `sudo nixos-rebuild switch` 应用修改后，即可使用 Nix Flakes 来管理系统配置。

额外还有个好处就是，现在你可以通过 `nix repl` 打开一个 nix 交互式环境，有兴趣的话，可以使用它复习测试一遍前面学过的所有 Nix 语法。

### 3. 将系统配置切换到 flake.nix {#switch-to-flake-nix}

在启用了 Nix Flakes 特性后，`sudo nixos-rebuild switch` 命令会优先读取 `/etc/nixos/flake.nix` 文件，如果找不到再尝试使用 `/etc/nixos/configuration.nix`。

可以首先使用官方提供的模板来学习 flake 的编写，先查下有哪些模板：

```bash
nix flake show templates
```

其中有个 `templates#full` 模板展示了所有可能的用法，可以看看它的内容：

```bash
nix flake init -t templates#full
cat flake.nix
```

我们参照该模板创建文件 `/etc/nixos/flake.nix` 并编写好配置内容，后续系统的所有修改都将全部由 Nix Flakes 接管，示例内容如下：

```nix
{
  description = "Ryan's NixOS Flake";

  # 这是 flake.nix 的标准格式，inputs 是 flake 的依赖，outputs 是 flake 的输出
  # inputs 中的每一项依赖都会在被拉取、构建后，作为参数传递给 outputs 函数
  inputs = {
    # flake inputs 有很多种引用方式，应用最广泛的是 github:owner/name/reference，即 github 仓库地址 + branch/commit-id/tag

    # NixOS 官方软件源，这里使用 nixos-unstable 分支
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # home-manager，用于管理用户配置
    home-manager = {
      url = "github:nix-community/home-manager/release-22.11";
      # `follows` 是 inputs 中的继承语法
      # 这里使 sops-nix 的 `inputs.nixpkgs` 与当前 flake 的 `inputs.nixpkgs` 保持一致，
      # 避免依赖的 nixpkgs 版本不一致导致问题
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  # outputs 即 flake 的所有输出，其中的 nixosConfigurations 即 NixOS 系统配置
  # 一个 flake 可以有很多用途，也可以有很多种不同的输出，nixosConfigurations 只是其中一种
  #
  # outputs 的参数都是 inputs 中定义的依赖项，可以通过它们的名称来引用。
  # 不过 self 是个例外，这个特殊参数指向 outputs 自身（自引用），以及 flake 根目录
  # 这里的 @ 语法将函数的参数 attribute set 取了个别名，方便在内部使用
  outputs = { self, nixpkgs, ... }@inputs: {
    # 名为 nixosConfigurations 的 outputs 会在执行 `sudo nixos-rebuild switch` 时被使用
    # 默认情况下上述命令会使用与主机 hostname 同名的 nixosConfigurations
    # 但是也可以通过 `--flake /path/to/flake/direcotry#nixos-test` 来指定
    # 在 flakes 配置文件夹中执行 `sudo nixos-rebuild switch --flake .#nixos-test` 即可部署此配置
    #   其中 `.` 表示使用当前文件夹的 Flakes 配置，`#` 后面的内容则是 nixosConfigurations 的名称
    nixosConfigurations = {
      # hostname 为 nixos-test 的主机会使用这个配置
      # 这里使用了 nixpkgs.lib.nixosSystem 函数来构建配置，后面的 attributes set 是它的参数
      # 在 nixos 系统上使用如下命令即可部署此配置：`nixos-rebuild switch --flake .#nixos-test`
      "nixos-test" = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # Nix 模块系统可将配置模块化，提升配置的可维护性
        #
        # modules 中每个参数，都是一个 Nix Module，nixpkgs manual 中有半份介绍它的文档：
        #    <https://nixos.org/manual/nixpkgs/unstable/#module-system-introduction>
        # 说半份是因为它的文档不全，只有一些简单的介绍（Nix 文档现状...）
        # Nix Module 可以是一个 attribute set，也可以是一个返回 attribute set 的函数
        # 如果是函数，那么它的参数就是当前的 NixOS Module 的参数.
        # 根据 Nix Wiki 对 Nix modules 的描述，Nix modules 函数的参数可以有这几个：
        #
        #  lib:     nixpkgs 自带的函数库，提供了许多操作 Nix 表达式的实用函数
        #           详见 https://nixos.org/manual/nixpkgs/stable/#id-1.4
        #  config:  当前 flake 的所有 config 参数的集何
        #  options: 当前 flake 中所有 NixOS Modules 中定义的所有参数的集合
        #  pkgs:    一个包含所有 nixpkgs 包的集合
        #           入门阶段可以认为它的默认值为 `nixpkgs.legacyPackages."${system}"`
        #           可通过 `nixpkgs.pkgs` 这个 option 来自定义 pkgs 的值
        #  modulesPath: 默认 nixpkgs 的内置 Modules 文件夹路径，常用于从 nixpkgs 中导入一些额外的模块
        #               这个参数通常都用不到，我只在制作 iso 镜像时用到过
        #
        # 默认只能传上面这几个参数，如果需要传其他参数，必须使用 specialArgs，你可以取消注释如下这行来启用该参数
        # specialArgs = inputs  # 将 inputs 中的参数传入所有子模块
        modules = [
          # 导入之前我们使用的 configuration.nix，这样旧的配置文件仍然能生效
          # 注: /etc/nixos/configuration.nix 本身也是一个 Nix Module，因此可以直接在这里导入
          ./configuration.nix
        ];
      };
    };
  };
}
```

这里我们定义了一个名为 `nixos-test` 的系统，它的配置文件为 `./configuration.nix`，这个文件就是我们之前的配置文件，这样我们仍然可以沿用旧的配置。

现在执行 `sudo nixos-rebuild switch` 应用配置，系统应该没有任何变化，因为我们仅仅是切换到了 Nix Flakes，配置内容与之前还是一致的。

### 4. 通过 Flakes 来管理系统软件 {#manage-system-software-with-flakes}

切换完毕后，我们就可以通过 Flakes 来管理系统了。管系统最常见的需求就是装软件，我们在前面已经见识过如何通过 `environment.systemPackages` 来安装 `pkgs` 中的包，这些包都来自官方的 nixpkgs 仓库。

现在我们学习下如何通过 Flakes 安装其他来源的软件包，这比直接安装 nixpkgs 要灵活很多，最显而易见的好处是你可以很方便地设定软件的版本。
以 [helix](https://github.com/helix-editor/helix) 编辑器为例，我们首先需要在 `flake.nix` 中添加 helix 这个 inputs 数据源：

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # ......

  inputs = {
    # ......

    # helix editor, use tag 23.05
    helix.url = "github:helix-editor/helix/23.05"
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    nixosConfigurations = {
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # 将所有 inputs 参数设为所有子模块的特殊参数，这样就能在子模块中使用 helix 这个 inputs 了
        specialArgs = inputs;
        modules = [
          ./configuration.nix
        ];
      };
    };
  };
}
```

接下来在 `configuration.nix` 中就能引用这个 flake input 数据源了：

```nix
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).
# Nix 会通过名称匹配，自动将 specialArgs 中的 helix 注入到此函数的第三个参数
{ config, pkgs, helix, ... }:

{
  # 省略掉前面的配置......

  environment.systemPackages = with pkgs; [
    git  # Nix Flakes 通过 git 命令从数据源拉取依赖，所以必须先安装好 git
    vim
    wget
    curl

    # 这里从 helix 这个 inputs 数据源安装了 helix 程序
    helix."${pkgs.system}".packages.helix
  ];

  # 省略其他配置......
}
```

改好后再 `sudo nixos-rebuild switch` 部署，就能安装好 helix 程序了，可直接在终端使用 `helix` 命令测试验证。

### 5. 为 Flake 添加国内 cache 源 {#add-cache-source-for-flake}

Nix 为了加快包构建速度，提供了 <https://cache.nixos.org> 提前缓存构建结果提供给用户，但是在国内访问这个 cache 地址非常地慢，如果没有全局代理的话，基本上是无法使用的。
另外 Flakes 的数据源基本都是某个 Github 仓库，在国内从 Github 下载 Flakes 数据源也同样非常非常慢。

在旧的 NixOS 配置方式中，可以通过 `nix-channel` 命令添加国内的 cache 镜像源以提升下载速度，但是 Nix Flakes 会尽可能地避免使用任何系统级别的配置跟环境变量，以确保其构建结果不受环境的影响，因此在使用了 Flakes 后 `nix-channel` 命令就失效了。

为了自定义 cache 镜像源，我们必须在 `flake.nix` 中添加相关配置，这就是 `nixConfig` 参数，示例如下：

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # 为了确保够纯，Flake 不依赖系统自身的 /etc/nix/nix.conf，而是在 flake.nix 中通过 nixConfig 设置
  # 但是为了确保安全性，flake 默认仅允许直接设置少数 nixConfig 参数，其他参数都需要在执行 nix 命令时指定 `--accept-flake-config`，否则会被忽略
  #     <https://nixos.org/manual/nix/stable/command-ref/conf-file.html>
  # 注意：即使添加了国内 cache 镜像，如果有些包国内镜像下载不到，它仍然会走国外。
  # 我的解法是使用 openwrt 旁路由 + openclash 加速下载。
  # 临时修改系统默认网关为我的旁路由 IP:
  #    sudo ip route add default via 192.168.5.201
  # 还原路由规则:
  #    sudo ip route del default via 192.168.5.201
  nixConfig = {
    experimental-features = [ "nix-command" "flakes" ];
    substituters = [
      # replace official cache with a mirror located in China
      "https://mirrors.bfsu.edu.cn/nix-channels/store"
      "https://cache.nixos.org/"
    ];

    # nix community's cache server
    extra-substituters = [
      "https://nix-community.cachix.org"
    ];
    extra-trusted-public-keys = [
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
    ];
  };

  inputs = {
    # 省略若干配置...
  };

  outputs = {
    # 省略若干配置...
  };
}

```

改完后使用 `sudo nixos-rebuild switch` 应用配置即可生效，后续所有的包都会优先从国内镜像源查找缓存。

> 注：上述手段只能加速部分包的下载，许多 inputs 数据源仍然会从 Github 拉取，另外如果找不到缓存，会执行本地构建，这通常仍然需要从国外下载源码与构建依赖，因此仍然会很慢。为了完全解决速度问题，仍然建议使用旁路由等局域网全局代理方案。

### 6. 安装 home-manager {#install-home-manager}

前面简单提过，NixOS 自身的配置文件只能管理系统级别的配置，而用户级别的配置则需要使用 home-manager 来管理。

根据官方文档 [Home Manager Manual](https://nix-community.github.io/home-manager/index.htm)，要将 home manager 作为 NixOS 模块安装，首先需要创建 `/etc/nixos/home.nix`，配置方法如下：

```nix
{ config, pkgs, ... }:

{
  # 注意修改这里的用户名与用户目录
  home.username = "ryan";
  home.homeDirectory = "/home/ryan";

  # 直接将当前文件夹的配置文件，链接到 Home 目录下的指定位置
  # home.file.".config/i3/wallpaper.jpg".source = ./wallpaper.jpg;

  # 递归将某个文件夹中的文件，链接到 Home 目录下的指定位置
  # home.file.".config/i3/scripts" = {
  #   source = ./scripts;
  #   recursive = true;   # 递归整个文件夹
  #   executable = true;  # 将其中所有文件添加「执行」权限
  # };

  # 直接以 text 的方式，在 nix 配置文件中硬编码文件内容
  # home.file.".xxx".text = ''
  #     xxx
  # '';

  # 设置鼠标指针大小以及字体 DPI（适用于 4K 显示器）
  xresources.properties = {
    "Xcursor.size" = 16;
    "Xft.dpi" = 172;
  };

  # git 相关配置
  programs.git = {
    enable = true;
    userName = "Ryan Yin";
    userEmail = "xiaoyin_c@qq.com";
  };

  # 通过 home.packages 安装一些常用的软件
  # 这些软件将仅在当前用户下可用，不会影响系统级别的配置
  # 建议将所有 GUI 软件，以及与 OS 关系不大的 CLI 软件，都通过 home.packages 安装
  home.packages = with pkgs;[
    # 如下是我常用的一些命令行工具，你可以根据自己的需要进行增删
    neofetch
    nnn # terminal file manager

    # archives
    zip
    xz
    unzip
    p7zip

    # utils
    ripgrep # recursively searches directories for a regex pattern
    jq # A lightweight and flexible command-line JSON processor
    yq-go # yaml processer https://github.com/mikefarah/yq
    exa # A modern replacement for ‘ls’
    fzf # A command-line fuzzy finder

    # networking tools
    mtr # A network diagnostic tool
    iperf3
    dnsutils  # `dig` + `nslookup`
    ldns # replacement of `dig`, it provide the command `drill`
    aria2 # A lightweight multi-protocol & multi-source command-line download utility
    socat # replacement of openbsd-netcat
    nmap # A utility for network discovery and security auditing
    ipcalc  # it is a calculator for the IPv4/v6 addresses

    # misc
    cowsay
    file
    which
    tree
    gnused
    gnutar
    gawk
    zstd
    gnupg

    # nix related
    # 
    # it provides the command `nom` works just like `nix
    # with more details log output
    nix-output-monitor

    # productivity
    hugo # static site generator
    glow # markdown previewer in terminal

    btop  # replacement of htop/nmon
    iotop # io monitoring
    iftop # network monitoring

    # system call monitoring
    strace # system call monitoring
    ltrace # library call monitoring
    lsof # list open files

    # system tools
    sysstat
    lm_sensors # for `sensors` command
    ethtool
    pciutils # lspci
    usbutils # lsusb
  ];

  # 启用 starship，这是一个漂亮的 shell 提示符
  programs.starship = {
    enable = true;
    settings = {
      add_newline = false;
      aws.disabled = true;
      gcloud.disabled = true;
      line_break.disabled = true;
    };
  };

  # alacritty 终端配置
  programs.alacritty = {
    enable = true;
      env.TERM = "xterm-256color";
      font = {
        size = 12;
        draw_bold_text_with_bright_colors = true;
      };
      scrolling.multiplier = 5;
      selection.save_to_clipboard = true;
  };

  programs.bash = {
    enable = true;
    enableCompletion = true;
    bashrcExtra = ''
      export PATH="$PATH:$HOME/bin:$HOME/.local/bin:$HOME/go/bin"
    '';

    # set some aliases, feel free to add more or remove some
    shellAliases = {
      urldecode = "python3 -c 'import sys, urllib.parse as ul; print(ul.unquote_plus(sys.stdin.read()))'";
      urlencode = "python3 -c 'import sys, urllib.parse as ul; print(ul.quote_plus(sys.stdin.read()))'";
      httpproxy = "export https_proxy=http://127.0.0.1:7890; export http_proxy=http://127.0.0.1:7890;";
    };
  };

  # This value determines the Home Manager release that your
  # configuration is compatible with. This helps avoid breakage
  # when a new Home Manager release introduces backwards
  # incompatible changes.
  #
  # You can update Home Manager without changing this value. See
  # the Home Manager release notes for a list of state version
  # changes in each release.
  home.stateVersion = "22.11";

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
```

添加好 `/etc/nixos/home.nix` 后，还需要在 `/etc/nixos/flake.nix` 中导入该配置，它才能生效，可以使用如下命令，在当前文件夹中生成一个示例配置以供参考：

```shell
nix flake new example -t github:nix-community/home-manager#nixos
```

调整好参数后的 `/etc/nixos/flake.nix` 内容示例如下：

```nix
{
  description = "NixOS configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager.url = "github:nix-community/home-manager";
    home-manager.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ nixpkgs, home-manager, ... }: {
    nixosConfigurations = {
      # 这里的 nixos-test 替换成你的主机名称
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./configuration.nix

          # 将 home-manager 配置为 nixos 的一个 module
          # 这样在 nixos-rebuild switch 时，home-manager 配置也会被自动部署
          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;

            # 这里的 ryan 也得替换成你的用户名
            # 这里的 import 函数在前面 Nix 语法中介绍过了，不再赘述
            home-manager.users.ryan = import ./home.nix;

            # 使用 home-manager.extraSpecialArgs 自定义传递给 ./home.nix 的参数
            # 取消注释下面这一行，就可以在 home.nix 中使用 flake 的所有 inputs 参数了
            # home-manager.extraSpecialArgs = inputs;
          }
        ];
      };
    };
  };
}
```

然后执行 `sudo nixos-rebuild switch` 应用配置，即可完成 home-manager 的安装。

安装完成后，所有用户级别的程序、配置，都可以通过 `/etc/nixos/home.nix` 管理，并且执行 `sudo nixos-rebuild switch` 时也会自动应用 home-manager 的配置。

`home.nix` 中 Home Manager 的配置项有这几种查找方式：

- [Home Manager - Appendix A. Configuration Options](https://nix-community.github.io/home-manager/options.html): 一份包含了所有配置项的列表，建议在其中关键字搜索。
- [home-manager](https://github.com/nix-community/home-manager): 有些配置项在官方文档中没有列出，或者文档描述不够清晰，可以直接在这份 home-manager 的源码中搜索阅读对应的源码。

### 7. 模块化 NixOS 配置 {#modularize-nixos-configuration}

到这里整个系统的骨架基本就配置完成了，当前我们 `/etc/nixos` 中的系统配置结构应该如下：

```
$ tree
.
├── flake.lock
├── flake.nix
├── home.nix
└── configuration.nix
```

下面分别说明下这四个文件的功能：

- `flake.lock`: 自动生成的版本锁文件，它记录了整个 flake 所有输入的数据源、hash 值、版本号，确保系统可复现。
- `flake.nix`: 入口文件，执行 `sudo nixos-rebuild switch` 时会识别并部署它。
- `configuration.nix`: 在 flake.nix 中被作为系统模块导入，目前所有系统级别的配置都写在此文件中。
  - 此配置文件中的所有配置项，参见官方文档 [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration)
- `home.nix`: 在 flake.nix 中被 home-manager 作为 ryan 用户的配置导入，也就是说它包含了 ryan 这个用户的所有 Home Manager 配置，负责管理其 Home 文件夹。
  - 此配置文件的所有配置项，参见 [Appendix A. Configuration Options - Home Manager](https://nix-community.github.io/home-manager/options.html)

通过修改上面几个配置文件就可以实现对系统与 Home 目录状态的修改。
但是随着配置的增多，单纯依靠 `configuration.nix` 跟 `home.nix` 会导致配置文件臃肿，难以维护，因此更好的解决方案是通过 Nix 的模块机制，将配置文件拆分成多个模块，分门别类地编写维护。

在前面的 Nix 语法一节有介绍过：「`import` 的参数如果为文件夹路径，那么会返回该文件夹下的 `default.nix` 文件的执行结果」，实际 Nix 还提供了一个 `imports` 参数，它可以接受一个 `.nix` 文件列表，并将该列表中的所有配置**合并**（Merge）到当前的 attribute set 中。注意这里的用词是「合并」，它表明 `imports` 如果遇到重复的配置项，不会简单地按执行顺序互相覆盖，而是更合理地处理。比如说我在多个 modules 中都定义了 `program.packages = [...]`，那么 `imports` 会将所有 modules 中的 `program.packages` 这个 list 合并。不仅 list 能被正确合并，attribute set 也能被正确合并，具体行为各位看官可以自行探索。

> 我只在 [nixpkgs-unstable 官方手册 - evalModules parameters](https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules-parameters) 中找到一句关于 `imports` 的描述：`A list of modules. These are merged together to form the final configuration.`，可以意会一下...（Nix 的文档真的一言难尽...这么核心的参数文档就这么一句...）

我们可以借助 `imports` 参数，将 `home.nix` 与 `configuration.nix` 拆分成多个 `.nix` 文件。

比如我之前的 i3wm 系统配置 [ryan4yin/nix-config/v0.0.2](https://github.com/ryan4yin/nix-config/tree/v0.0.2)，结构如下：

```shell
├── flake.lock
├── flake.nix
├── home
│   ├── default.nix         # 在这里通过 imports = [...] 导入所有子模块
│   ├── fcitx5              # fcitx5 中文输入法设置，我使用了自定义的小鹤音形输入法
│   │   ├── default.nix
│   │   └── rime-data-flypy
│   ├── i3                  # i3wm 桌面配置
│   │   ├── config
│   │   ├── default.nix
│   │   ├── i3blocks.conf
│   │   ├── keybindings
│   │   └── scripts
│   ├── programs
│   │   ├── browsers.nix
│   │   ├── common.nix
│   │   ├── default.nix   # 在这里通过 imports = [...] 导入 programs 目录下的所有 nix 文件
│   │   ├── git.nix
│   │   ├── media.nix
│   │   ├── vscode.nix
│   │   └── xdg.nix
│   ├── rofi              #  rofi 应用启动器配置，通过 i3wm 中配置的快捷键触发
│   │   ├── configs
│   │   │   ├── arc_dark_colors.rasi
│   │   │   ├── arc_dark_transparent_colors.rasi
│   │   │   ├── power-profiles.rasi
│   │   │   ├── powermenu.rasi
│   │   │   ├── rofidmenu.rasi
│   │   │   └── rofikeyhint.rasi
│   │   └── default.nix
│   └── shell             # shell 终端相关配置
│       ├── common.nix
│       ├── default.nix
│       ├── nushell
│       │   ├── config.nu
│       │   ├── default.nix
│       │   └── env.nu
│       ├── starship.nix
│       └── terminals.nix
├── hosts
│   ├── msi-rtx4090      # PC 主机的配置
│   │   ├── default.nix                 # 这就是之前的 configuration.nix，不过大部分内容都拆出到 modules 了
│   │   └── hardware-configuration.nix  # 与系统硬件相关的配置，安装 nixos 时自动生成的
│   └── nixos-test       # 测试用的虚拟机配置
│       ├── default.nix
│       └── hardware-configuration.nix
├── modules          # 从 configuration.nix 中拆分出的一些通用配置
│   ├── i3.nix
│   └── system.nix
└── wallpaper.jpg    # 桌面壁纸，在 i3wm 配置中被引用
```

详细结构与内容，请移步前面提供的 github 仓库链接，这里就不多介绍了。

### 8. 更新系统 {#update-nixos-system}

在使用了 Nix Flakes 后，要更新系统也很简单，先更新 flake.lock 文件，然后部署即可。在配置文件夹中执行如下命令：

```shell
# 更新 flake.lock
nix flake update
# 部署系统
sudo nixos-rebuild switch
```

另外有时候安装新的包，跑 `sudo nixos-rebuild switch` 时可能会遇到 sha256 不匹配的报错，也可以尝试通过 `nix flake update` 更新 flake.lock 来解决（原理暂时不太清楚）。

### 9. 回退个别软件包的版本 {#rollback-package-version}

在使用 Nix Flakes 后，目前大家用得比较多的都是 `nixos-unstable` 分支的 nixpkgs，有时候就会遇到一些 bug，比如我最近（2023/5/6）就遇到了 [chrome/vscode 闪退的问题](https://github.com/swaywm/sway/issues/7562)。

这时候就需要退回到之前的版本，在 Nix Flakes 中，所有的包版本与 hash 值与其 input 数据源的 git commit 是一一对应的关系，因此回退某个包的到历史版本，就需要锁定其 input 数据源的 git commit.

为了实现上述需求，首先修改 `/etc/nixos/flake.nix`，示例内容如下（主要是利用 `specialArgs` 参数）：

```nix
{
  description = "NixOS configuration of Ryan Yin"

  inputs = {
    # 默认使用 nixos-unstable 分支
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    # 最新 stable 分支的 nixpkgs，用于回退个别软件包的版本，当前最新版本为 22.11
    nixpkgs-stable.url = "github:nixos/nixpkgs/nixos-22.11";

    # 另外也可以使用 git commit hash 来锁定版本，这是最彻底的锁定方式
    nixpkgs-fd40cef8d.url = "github:nixos/nixpkgs/fd40cef8d797670e203a27a91e4b8e6decf0b90c";
  };

  outputs = inputs@{
    self,
    nixpkgs,
    nixpkgs-stable,
    nixpkgs-fd40cef8d,
    ...
  }: {
    nixosConfigurations = {
      nixos-test = nixpkgs.lib.nixosSystem rec {
        system = "x86_64-linux";

        # 核心参数是这个，将非默认的 nixpkgs 数据源传到其他 modules 中
        specialArgs = {
          # 注意每次 import 都会生成一个新的 nixpkgs 实例
          # 这里我们直接在 flake.nix 中创建实例， 再传递到其他子 modules 中使用
          # 这样能有效重用 nixpkgs 实例，避免 nixpkgs 实例泛滥。
          pkgs-stable = import nixpkgs-stable {
            system = system;  # 这里递归引用了外部的 system 属性
            # 为了拉取 chrome 等软件包，需要允许安装非自由软件
            config.allowUnfree = true;
          };

          pkgs-fd40cef8d = import nixpkgs-fd40cef8d {
            system = system;
            config.allowUnfree = true;
          };
        };
        modules = [
          ./hosts/nixos-test

          # 省略其他模块配置...
        ];
      };
    };
  };
}
```

然后在你对应的 module 中使用该数据源中的包，一个 Home Manager 的子模块示例：

```nix
{
  pkgs,
  config,
  # nix 会从 flake.nix 的 specialArgs 查找并注入此参数
  pkgs-stable,
  # pkgs-fd40cef8d,  # 也可以使用固定 hash 的 nixpkgs 数据源
  ...
}:

{
  # 这里从 pkg-stable 中引用包
  home.packages = with pkgs-stable; [
    firefox-wayland

    # chrome wayland support was broken on nixos-unstable branch, so fallback to stable branch for now
    # https://github.com/swaywm/sway/issues/7562
    google-chrome
  ];

  programs.vscode = {
    enable = true;
    package = pkgs-stable.vscode;  # 这里也一样，从 pkgs-stable 中引用包
  };
}
```

配置完成后，通过 `sudo nixos-rebuild switch` 部署即可将 firefox/chrome/vscode 三个软件包回退到 stable 分支的版本。

> 根据 @fbewivpjsbsby 补充的文章 [1000 instances of nixpkgs](https://discourse.nixos.org/t/1000-instances-of-nixpkgs/17347)，在子模块中用 `import` 来定制 `nixpkgs` 不是一个好的习惯，因为每次 `import` 都会重新求值并产生一个新的 nixpkgs 实例，在配置越来越多时会导致构建时间变长、内存占用变大。所以这里改为了在 `flake.nix` 中创建所有 nixpkgs 实例。

### 10. 使用 Git 管理 NixOS 配置 {#git-manage-nixos-config}

NixOS 的配置文件是纯文本，因此跟普通的 dotfiles 一样可以使用 Git 管理。

此外 Nix Flakes 配置也不一定需要放在 `/etc/nixos` 目录下，可以放在任意目录下，只要在部署时指定正确的路径即可。

> 我们在前面第 3 小节的代码注释中有说明过，可以通过 `sudo nixos-rebuild switch --flake .#xxx` 的 `--flake` 参数指定 Flakes 配置的文件夹路径，并通过 `#` 后面的值来指定使用的 outputs 名称。

比如我的使用方式是将 Nix Flakes 配置放在 `~/nixos-config` 目录下，然后在 `/etc/nixos` 目录下创建一个软链接：

```shell
sudo mv /etc/nixos /etc/nixos.bak  # 备份原来的配置
sudo ln -s ~/nixos-config/ /etc/nixos
```

然后就可以在 `~/nixos-config` 目录下使用 Git 管理配置了，配置使用普通的用户级别权限即可，不要求 owner 为 root.

另一种方法是直接删除掉 `/etc/nixos`，并在每次部署时指定配置文件路径：

```shell
sudo mv /etc/nixos /etc/nixos.bak  # 备份原来的配置
cd ~/nixos-config

# 通过 --flake .#nixos-test 参数，指定使用当前文件夹的 flake.nix，使用的 nixosConfiguraitons 名称为 nixos-test
sudo nixos-rebuild switch --flake .#nixos-test
```

两种方式都可以，看个人喜好。搞定之后，系统的回滚也变得非常简单，只需要切换到上一个 commit 即可：

```shell
cd ~/nixos-config
# 回滚到上一个 commit
git checkout HEAD^1
# 部署
sudo nixos-rebuild switch --flake .#nixos-test
```

Git 的更多操作这里就不介绍了，总之一般情况下的回滚都能直接通过 Git 完成，只在系统完全崩溃的情况下，才需要通过重启进入 grub，从上一个历史版本启动系统。

### 11. 查看与清理历史数据 {#view-and-delete-history}

如前所述，NixOS 的每次部署都会生成一个新的版本，所有版本都会被添加到系统启动项中，除了重启电脑外，我们也可以通过如下命令查询当前可用的所有历史版本：

```shell
nix profile history --profile /nix/var/nix/profiles/system
```

以及清理历史版本释放存储空间的命令：

```shell
# 清理 7 天之前的所有历史版本
sudo nix profile wipe-history --profile /nix/var/nix/profiles/system  --older-than 7d
# 清理历史版本并不会删除数据，还需要手动 gc 下
sudo nix store gc --debug
```

以及查看系统层面安装的所有软件包（这个貌似只能用 `nix-env`）：

```shell
nix-env -qa
```

## 七、Nix Flakes 的使用 {#nix-flakes-usage}

到这里我们已经写了不少 Nix Flakes 配置来管理 NixOS 系统了，这里再简单介绍下 Nix Flakes 更细节的内容，以及常用的 nix flake 命令。

### 1. Flake 的 inputs {#flake-inputs}

`flake.nix` 中的 `inputs` 是一个 attribute set，用来指定当前 Flake 的依赖，inputs 有很多种类型，举例如下：

```nix
{
  inputs = {
    # 以 GitHub 仓库为数据源，指定使用 master 分支，这是最常见的 input 格式
    nixpkgs.url = "github:Mic92/nixpkgs/master";
    # Git URL，可用于任何基于 https/ssh 协议的 Git 仓库
    git-example.url = "git+https://git.somehost.tld/user/path?ref=branch&rev=fdc8ef970de2b4634e1b3dca296e1ed918459a9e";
    # 上面的例子会复制 .git 到本地, 如果数据量较大，建议使用 shallow=1 参数避免复制 .git
    git-directory-example.url = "git+file:/path/to/repo?shallow=1";
    # 本地文件夹 (如果使用绝对路径，可省略掉前缀 'path:')
    directory-example.url = "path:/path/to/repo";
    # 如果数据源不是一个 flake，则需要设置 flake=false
    bar = {
      url = "github:foo/bar/branch";
      flake = false;
    };

    sops-nix = {
      url = "github:Mic92/sops-nix";
      # `follows` 是 inputs 中的继承语法
      # 这里使 sops-nix 的 `inputs.nixpkgs` 与当前 flake 的 inputs.nixpkgs 保持一致，
      # 避免依赖的 nixpkgs 版本不一致导致问题
      inputs.nixpkgs.follows = "nixpkgs";
    };

    # 将 flake 锁定在某个 commit 上
    nix-doom-emacs = {
      url = "github:vlaci/nix-doom-emacs?rev=238b18d7b2c8239f676358634bfb32693d3706f3";
      flake = false;
    };

    # 使用 `dir` 参数指定某个子目录
    nixpkgs.url = "github:foo/bar?dir=shu";
  }
}
```

### 2. Flake 的 outputs {#flake-outputs}

`flake.nix` 中的 `outputs` 是一个 attribute set，是整个 Flake 的构建结果，每个 Flake 都可以有许多不同的 outputs。

一些特定名称的 outputs 有特殊用途，会被某些 Nix 命令识别处理，比如：

- Nix packages: 名称为 `apps.<system>.<name>`, `packages.<system>.<name>` 或 `legacyPackages.<system>.<name>` 的 outputs，都是 Nix 包，通常都是一个个应用程序。
  - 可以通过 `nix build .#name` 来构建某个 nix 包
- Nix Helper Functions: 名称为 `lib` 的 outputs 是 Flake 函数库，可以被其他 Flake 作为 inputs 导入使用。
- Nix development environments: 名称为 `devShells` 的 outputs 是 Nix 开发环境
  - 可以通过 `nix develop` 命令来使用该 Output 创建开发环境
- NixOS configurations: 名称为 `nixosConfigurations.<hostname>` 的 outputs，是 NixOS 的系统配置。
  - `nixos-rebuild switch .#<hostname>` 可以使用该 Output 来部署 NixOS 系统
- Nix templates: 名称为 `templates` 的 outputs 是 flake 模板
  - 可以通过执行命令 `nix flake init --template <reference>` 使用模板初始化一个 Flake 包
- 其他用户自定义的 outputs，可能被其他 Nix 相关的工具使用

NixOS Wiki 中给出的使用案例：

```nix
{ self, ... }@inputs:
{
  # Executed by `nix flake check`
  checks."<system>"."<name>" = derivation;
  # Executed by `nix build .#<name>`
  packages."<system>"."<name>" = derivation;
  # Executed by `nix build .`
  packages."<system>".default = derivation;
  # Executed by `nix run .#<name>`
  apps."<system>"."<name>" = {
    type = "app";
    program = "<store-path>";
  };
  # Executed by `nix run . -- <args?>`
  apps."<system>".default = { type = "app"; program = "..."; };

  # Formatter (alejandra, nixfmt or nixpkgs-fmt)
  formatter."<system>" = derivation;
  # Used for nixpkgs packages, also accessible via `nix build .#<name>`
  legacyPackages."<system>"."<name>" = derivation;
  # Overlay, consumed by other flakes
  overlays."<name>" = final: prev: { };
  # Default overlay
  overlays.default = {};
  # Nixos module, consumed by other flakes
  nixosModules."<name>" = { config }: { options = {}; config = {}; };
  # Default module
  nixosModules.default = {};
  # Used with `nixos-rebuild --flake .#<hostname>`
  # nixosConfigurations."<hostname>".config.system.build.toplevel must be a derivation
  nixosConfigurations."<hostname>" = {};
  # Used by `nix develop .#<name>`
  devShells."<system>"."<name>" = derivation;
  # Used by `nix develop`
  devShells."<system>".default = derivation;
  # Hydra build jobs
  hydraJobs."<attr>"."<system>" = derivation;
  # Used by `nix flake init -t <flake>#<name>`
  templates."<name>" = {
    path = "<store-path>";
    description = "template description goes here?";
  };
  # Used by `nix flake init -t <flake>`
  templates.default = { path = "<store-path>"; description = ""; };
}
```

### 3. Flake 命令行的使用 {#flake-commands-usage}

在启用了 `nix-command` & `flakes` 功能后，我们就可以使用 Nix 提供的新一代 Nix 命令行工具 [New Nix Commands][New Nix Commands] 了，下面列举下其中常用命令的用法：

```bash
# 解释下这条指令涉及的参数：
#   `nixpkgs#ponysay` 意思是 `nixpkgs` 这个 flake 中的 `ponysay` 包。
#   `nixpkgs` 是一个 flakeregistry ida,
#    nix 会从 <https://github.com/NixOS/flake-registry/blob/master/flake-registry.json> 中
#    找到这个 id 对应的 github 仓库地址
# 所以这个命令的意思是创建一个新环境，安装并运行 `nixpkgs` 这个 flake 提供的 `ponysay` 包。
#   注：前面已经介绍过了，nix 包 是 flake outputs 中的一种。
echo "Hello Nix" | nix run "nixpkgs#ponysay"

# 这条命令和上面的命令作用是一样的，只是使用了完整的 flake URI，而不是 flakeregistry id。
echo "Hello Nix" | nix run "github:NixOS/nixpkgs/nixos-unstable#ponysay"

# 这条命令的作用是使用 zero-to-nix 这个 flake 中名 `devShells.example` 的 outptus 来创建一个开发环境，
# 然后在这个环境中打开一个 bash shell。
nix develop "github:DeterminateSystems/zero-to-nix#example"

# 除了使用远程 flake uri 之外，你也可以使用当前目录下的 flake 来创建一个开发环境。
mkdir my-flake && cd my-flake
## 通过模板初始化一个 flake
nix flake init --template "github:DeterminateSystems/zero-to-nix#javascript-dev"
## 使用当前目录下的 flake 创建一个开发环境，并打开一个 bash shell
nix develop
# 或者如果你的 flake 有多个 devShell 输出，你可以指定使用名为 example 的那个
nix develop .#example

# 构建 `nixpkgs` flake 中的 `bat` 这个包
# 并在当前目录下创建一个名为 `result` 的符号链接，链接到该构建结果文件夹。
mkdir build-nix-package && cd build-nix-package
nix build "nixpkgs#bat"
# 构建一个本地 flake 和 nix develop 是一样的，不再赘述
```

此外 [Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems] 是一份全新的 Nix & Flake 新手入门文档，写得比较浅显易懂，适合新手用来入门。
## 八、Nixpkgs 的高级用法 {#nixpkgs-advanced-usage}

callPackage、Overriding 与 Overlays 是在使用 Nix 时偶尔会用到的技术，它们都是用来自定义 Nix 包的构建方法的。

我们知道许多程序都有大量构建参数需要配置，不同的用户会希望使用不同的构建参数，这时候就需要 Overriding 与 Overlays 来实现。我举几个我遇到过的例子：

1. [fcitx5-rime.nix](https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix): fcitx5-rime 的 `rimeDataPkgs` 默认使用 `rime-data` 包，但是也可以通过 override 来自定义该参数的值，以加载自定义的 rime 配置（比如加载小鹤音形输入法配置）。
2. [vscode/with-extensions.nix](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vscode/with-extensions.nix): vscode 的这个包也可以通过 override 来自定义 `vscodeExtensions` 参数的值来安装自定义插件。
   1. [nix-vscode-extensions](https://github.com/nix-community/nix-vscode-extensions): 就是利用该参数实现的 vscode 插件管理
3. [firefox/common.nix](https://github.com/NixOS/nixpkgs/blob/416ffcd08f1f16211130cd9571f74322e98ecef6/pkgs/applications/networking/browsers/firefox/common.nix): firefox 同样有许多可自定义的参数
4. 等等

总之如果需要自定义上述这类 Nix 包的构建参数，或者实施某些比较底层的修改，我们就得用到 Overriding 跟 Overlays。

### 1. pkgs.callPackage {#callpackage}

> [Chapter 13. Callpackage Design Pattern - Nix Pills](https://nixos.org/guides/nix-pills/callpackage-design-pattern.html)

前面我们介绍并大量使用了 `import xxx.nix` 来导入 Nix 文件，这种语法只是单纯地返回该文件的执行结果，不会对该结果进行进一步处理。
比如说 `xxx.nix` 的内容是形如 `{...}: {...}`，那么 `import xxx.nix` 的结果就是该文件中定义的这个函数。

`pkgs.callPackage` 也是用来导入 Nix 文件的，它的语法是 `pkgs.callPackage xxx.nix { ... }`. 但跟 `import` 不同的是，它导入的 nix 文件内容必须是一个 Derivation 或者返回 Derivation 的函数，它的执行结果一定是一个 Derivation，也就是一个软件包。

那可以作为 `pkgs.callPackge` 参数的 nix 文件具体长啥样呢，可以去看看我们前面举例过的 `hello.nix` `fcitx5-rime.nix` `vscode/with-extensions.nix` `firefox/common.nix`，它们都可以被 `pkgs.callPackage` 导入。

当 `pkgs.callPackge xxx.nix {...}` 中的 `xxx.nix`，其内容为一个函数时（绝大多数 nix 包都是如此），执行流程如下：

1. `pkgs.callPackge xxx.nix {...}` 会先 `import xxx.nix`，得到其中定义的函数，该函数的参数通常会有 `lib`, `stdenv`, `fetchurl` 等参数，以及一些自定义参数，自定义参数通常都有默认值。
2. 接着 `pkgs.callPackge` 会首先从当前环境中查找名称匹配的值，作为将要传递给前述函数的参数。像 `lib` `stdenv` `fetchurl` 这些都是 nixpkgs 中的函数，在这一步就会查找到它们。
3. 接着 `pkgs.callPackge` 会将其第二个参数 `{...}` 与前一步得到的参数集（attribute set）进行合并，得到一个新的参数列表，然后将其传递给该函数并执行。
4. 函数执行结果是一个 Derivation，也就是一个软件包。

这个函数比较常见的用途是用来导入一些自定义的 Nix 包，比如说我们自己写了一个 `hello.nix`，然后就可以在任意 Nix Module 中使用 `pkgs.callPackage ./hello.nix {}` 来导入并使用它。

### 2. Overriding {#overriding}

> [Chapter 4. Overriding - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overrides)

简单的说，所有 nixpkgs 中的 Nix 包都可以通过 `<pkg>.override {}` 来自定义某些构建参数，它返回一个使用了自定义参数的新 Derivation. 举个例子：

```nix
pkgs.fcitx5-rime.override {rimeDataPkgs = [
    ./rime-data-flypy
];}
```

上面这个 Nix 表达式的执行结果就是一个新的 Derivation，它的 `rimeDataPkgs` 参数被覆盖为 `[./rime-data-flypy]`，而其他参数则沿用原来的值。

如何知道 `fcitx5-rime` 这个包有哪些参数可以覆写呢？有几种方法：

1. 直接在 GitHub 的 nixpkgs 源码中找：[fcitx5-rime.nix](https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix)
   1. 注意要选择正确的分支，加入你用的是 nixos-unstable 分支，那就要在 nixos-unstable 分支中找。
2. 通过 `nix repl` 交互式查看：`nix repl '<nixpkgs>'`，然后输入 `:e pkgs.fcitx5-rime`，会通过编辑器打开这个包的源码，然后就可以看到这个包的所有参数了。

通过上述两种方法，都可以看到 `fcitx5-rime` 这个包拥有如下输入参数，它们都是可以通过 `override` 修改的：

```nix
{ lib, stdenv
, fetchFromGitHub
, pkg-config
, cmake
, extra-cmake-modules
, gettext
, fcitx5
, librime
, rime-data
, symlinkJoin
, rimeDataPkgs ? [ rime-data ]
}:

stdenv.mkDerivation rec {
  ...
}
```

除了覆写参数，还可以通过 `overrideAttrs` 来覆写使用 `stdenv.mkDerivation` 构建的 Derivation 的属性。
以 `pkgs.hello` 为例，首先通过前述方法查看这个包的源码：

```nix
# https://github.com/NixOS/nixpkgs/blob/nixos-unstable/pkgs/applications/misc/hello/default.nix
{ callPackage
, lib
, stdenv
, fetchurl
, nixos
, testers
, hello
}:

stdenv.mkDerivation (finalAttrs: {
  pname = "hello";
  version = "2.12.1";

  src = fetchurl {
    url = "mirror://gnu/hello/hello-${finalAttrs.version}.tar.gz";
    sha256 = "sha256-jZkUKv2SV28wsM18tCqNxoCZmLxdYH2Idh9RLibH2yA=";
  };

  doCheck = true;

  # ......
})
```

其中 `pname` `version` `src` `doCheck` 等属性都是可以通过 `overrideAttrs` 来覆写的，比如：

```nix
helloWithDebug = pkgs.hello.overrideAttrs (finalAttrs: previousAttrs: {
  doCheck = false;
});
```

上面这个例子中，`doCheck` 就是一个新的 Derivation，它的 `doCheck` 参数被改写为 `false`，而其他参数则沿用原来的值。

除了包源码中自定义的参数值外，我们也可以通过 `overrideAttrs` 直接改写 `stdenv.mkDerivation` 内部的默认参数，比如：

```nix
helloWithDebug = pkgs.hello.overrideAttrs (finalAttrs: previousAttrs: {
  separateDebugInfo = true;
});
```

具体的内部参数可以通过 `nix repl '<nixpkgs>'` 然后输入 `:e stdenv.mkDerivation` 来查看其源码。

### 3. Overlays {#overlays}

> [Chapter 3. Overlays - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overlays)

前面介绍的 override 函数都会生成新的 Derivation，不影响 pkgs 中原有的 Derivation，只适合作为局部参数使用。
但如果你需要覆写的 Derivation 还被其他 Nix 包所依赖，那其他 Nix 包使用的仍然会是原有的 Derivation.

为了解决这个问题，Nix 提供了 overlays 能力。简单的说，Overlays 可以全局修改 pkgs 中的 Derivation。

在旧的 Nix 环境中，Nix 默认会自动应用 `~/.config/nixpkgs/overlays.nix` `~/.config/nixpkgs/overlays/*.nix` 这类路径下的所有 overlays 配置。

但是在 Flakes 中，为了确保系统的可复现性，它不能依赖任何 Git 仓库之外的配置，所以这种旧的方法就不能用了。

在使用 Nix Flakes 编写 NixOS 配置时，Home Manager 与 NixOS 都提供了 `nixpkgs.overlays` 这个 option 来引入 overlays, 相关文档：

- [home-manager docs - `nixpkgs.overlays`](https://nix-community.github.io/home-manager/options.html#opt-nixpkgs.overlays)
- [nixpkgs source code - `nixpkgs.overlays`](https://github.com/NixOS/nixpkgs/blob/30d7dd7e7f2cba9c105a6906ae2c9ed419e02f17/nixos/modules/misc/nixpkgs.nix#L169)

举个例子，如下内容就是一个加载 Overlays 的 Module，它既可以用做 Home Manager Module，也可以用做 NixOS Module，因为这俩定义完全是一致的：

> 不过我使用发现，Home Manager 毕竟是个外部组件，而且现在全都用的 unstable 分支，这导致 Home Manager Module 有时候会有点小毛病，因此更建议以 NixOS Module 的形式引入 overlays

```nix
{ config, pkgs, lib, ... }:

{
  nixpkgs.overlays = [
    # overlayer1 - 参数名用 self 与 super，表达继承关系
    (self: super: {
     google-chrome = super.google-chrome.override {
       commandLineArgs =
         "--proxy-server='https=127.0.0.1:3128;http=127.0.0.1:3128'";
     };
    })

    # overlayer2 - 还可以使用 extend 来继承其他 overlay
    # 这里改用 final 与 prev，表达新旧关系
    (final: prev: {
      steam = prev.steam.override {
        extraPkgs = pkgs:
          with pkgs; [
            keyutils
            libkrb5
            libpng
            libpulseaudio
            libvorbis
            stdenv.cc.cc.lib
            xorg.libXcursor
            xorg.libXi
            xorg.libXinerama
            xorg.libXScrnSaver
          ];
        extraProfile = "export GDK_SCALE=2";
      };
    })

    # overlay3 - 也可以将 overlay 定义在其他文件中
    # 这里 overlay3.nix 中的内容格式与上面的一致，都是 `final: prev: { xxx = prev.xxx.override { ... }; }`
    (import ./overlays/overlay3.nix)
  ];
}
```

这里只是个示例配置，参照此格式编写你自己的 overlays 配置，将该配置作为 NixOS Module 或者 Home Manager Module 引入，然后部署就可以看到效果了。

#### 模块化 overlays 配置

上面的例子说明了如何编写 overlays，但是所有 overlays 都一股脑儿写在一起，就有点难以维护了，写得多了自然就希望模块化管理这些 overlays.

这里介绍下我找到的一个 overlays 模块化管理的最佳实践。

首先在 Git 仓库中创建 `overlays` 文件夹用于存放所有 overlays 配置，然后创建 `overlays/default.nix`，其内容如下：

```nix
args:
  # import 当前文件夹下所有的 nix 文件，并以 args 为参数执行它们
  # 返回值是一个所有执行结果的列表，也就是 overlays 的列表
  builtins.map
  (f: (import (./. + "/${f}") args))  # map 的第一个参数，是一个 import 并执行 nix 文件的函数
  (builtins.filter          # map 的第二个参数，它返回一个当前文件夹下除 default.nix 外所有 nix 文件的列表
    (f: f != "default.nix")
    (builtins.attrNames (builtins.readDir ./.)))
```

后续所有 overlays 配置都添加到 `overlays` 文件夹中，一个示例配置 `overlays/fcitx5/default.nix` 内容如下：

```nix
# 为了不使用默认的 rime-data，改用我自定义的小鹤音形数据，这里需要 override
# 参考 https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix
{pkgs, config, lib, ...}:

(self: super: {
  # 小鹤音形配置，配置来自 flypy.com 官方网盘的鼠须管配置压缩包「小鹤音形“鼠须管”for macOS.zip」
  rime-data = ./rime-data-flypy;
  fcitx5-rime = super.fcitx5-rime.override { rimeDataPkgs = [ ./rime-data-flypy ]; };
})
```

我通过上面这个 overlays 修改了 fcitx5-rime 输入法的默认数据，加载了我自定义的小鹤音形输入法。

最后，还需要通过 `nixpkgs.overlays` 这个 option 加载 `overlays/default.nix` 返回的所有 overlays 配置，在任一 NixOS Module 中添加如下参数即可：

```nix
{ config, pkgs, lib, ... } @ args:

{
  # ......

  # 添加此参数
  nixpkgs.overlays = import /path/to/overlays/dir;

  # ......
}
```

比如说直接写 `flake.nix` 里：

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # ......

  inputs = {
    # ......
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    nixosConfigurations = {
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        specialArgs = inputs;
        modules = [
          ./hosts/nixos-test

          # 添加如下内嵌 module 定义
          #   这里将 modules 的所有参数 args 都传递到了 overlays 中
          (args: { nixpkgs.overlays = import ./overlays args; })

          # ......
        ];
      };
    };
  };
}
```

按照上述方法进行配置，就可以很方便地模块化管理所有 overlays 配置了，以我的配置为例，overlays 文件夹的结构大致如下：

```nix
.
├── flake.lock
├── flake.nix
├── home
├── hosts
├── modules
├── ......
├── overlays
│   ├── default.nix         # 它返回一个所有 overlays 的列表
│   └── fcitx5              # fcitx5 overlay
│       ├── default.nix
│       ├── README.md
│       └── rime-data-flypy  # 自定义的 rime-data，需要遵循它的文件夹格式
│           └── share
│               └── rime-data
│                   ├── ......  # rime-data 文件
└── README.md
```

你可以在我的配置仓库 [ryan4yin/nix-config/v0.0.4](https://github.com/ryan4yin/nix-config/tree/v0.0.4) 查看更详细的内容，获取些灵感。

## 进阶玩法 {#advanced-topics}

逐渐熟悉 Nix 这一套工具链后，可以进一步读一读 Nix 的三本手册，挖掘更多的玩法：

- [Nix Reference Manual](https://nixos.org/manual/nix/stable/package-management/profiles.html): Nix 包管理器使用手册，主要包含 Nix 包管理器的设计、命令行使用说明。
- [nixpkgs Manual](https://nixos.org/manual/nixpkgs/unstable/): 主要介绍 Nixpkgs 的参数、Nix 包的使用、修改、打包方法。
- [NixOS Manual](https://nixos.org/manual/nixos/unstable/): NixOS 系统使用手册，主要包含 Wayland/X11, GPU 等系统级别的配置说明。
- [nix-pills](https://nixos.org/guides/nix-pills): Nix Pills 对如何使用 Nix 构建软件包进行了深入的阐述，写得比官方文档清晰易懂，而且也足够深入，值得一读。

在对 Nix Flakes 熟悉到一定程度后，你可以尝试一些 Flakes 的进阶玩法，如下是一些比较流行的社区项目，可以试用：

- [flake-parts](https://github.com/hercules-ci/flake-parts): 通过 Module 模块系统简化配置的编写与维护。
- [flake-utils-plus](https://github.com/gytis-ivaskevicius/flake-utils-plus):同样是用于简化 Flake 配置的第三方包，不过貌似更强大些
- [digga][digga]: 一个大而全的 Flake 模板，揉合了各种实用 Nix 工具包的功能，不过结构比较复杂，需要一定经验才能玩得转。
- ......

以及其他许多实用的社区项目可探索，我比较关注的有这几个：

- [dev-templates](https://github.com/the-nix-way/dev-templates): 原汁原味的 devShell 模板，可以用于快速搭建开发环境。
- [devenv](https://github.com/cachix/devenv): 开发环境管理
- [agenix](https://github.com/ryantm/agenix): secrets 管理
- [nixos-generator](https://github.com/nix-community/nixos-generators): 镜像生成工具，从 nixos 配置生成 iso/qcow2 等格式的镜像
- [lanzaboote](https://github.com/nix-community/lanzaboote): 启用 secure boot
- [impermanence](https://github.com/nix-community/impermanence): 用于配置无状态系统。可用它持久化你指定的文件或文件夹，同时再将 /home 目录挂载为 tmpfs 或者每次启动时用工具擦除一遍。这样所有不受 impermanence 管理的数据都将成为临时数据，如果它们导致了任何问题，重启下系统这些数据就全部还原到初始状态了！
- [colmena](https://github.com/zhaofengli/colmena): NixOS 主机部署工具

## 总结 {#summary}

这是本系列文章的第一篇，介绍了使用 Nix Flakes 配置 NixOS 系统的基础知识，跟着这篇文章把系统配置好，就算是入门了。

我会在后续文章中介绍 NixOS & Nix Flakes 的进阶知识：开发环境管理、secrets 管理、软件打包、远程主机管理等等，尽请期待。


## 最后，Flakes 何时会成为稳定特性？ {#when-will-flakes-stablized}

我们通篇文章两万多字，详细介绍了如何开始使用 Flakes 配置 NixOS 系统，但是文章开头就提到了 Flakes 目前还是实验性功能，这不免让人担忧，如果啥时候 Flakes 被大改甚至被移除，那到时可能还需要花费大量的精力去迁移配置。

实际上这也是目前整个 NixOS 社区最关心的问题之一Flakes 何时会成为稳定特性？

我深入了解了下 Flakes 现状与未来计划相关的资料，大概有这些：

- https://github.com/NixOS/rfcs/pull/136: 一份渐进式地将 Flakes 与 new CLI 两个实验性特性推向稳定的 RFC，目前还在讨论中。
- https://discourse.nixos.org/t/why-are-flakes-still-experimental/29317: 最近的一次关于 Flakes 稳定性的讨论，可以看到大家的疑惑，以及社区对 Flakes 的态度。
- https://grahamc.com/blog/flakes-are-an-obviously-good-thing/: NixOS 社区成员的文章，记录了他对 Flakes 的看法，以及对社区当初添加 Flakes 特性时的不当举措的懊悔。
- https://nixos-foundation.notion.site/1-year-roadmap-0dc5c2ec265a477ea65c549cd5e568a9： NixOS Fundation 的一份 Roadmap，其中提到了 Flakes 的计划：`Stabilize flakes and release Nix 3.0. Flakes are widely used (there are more GitHub repos being created with a flake.nix than a default.nix) but they’re still marked as experimental, which is not a good situation. The same applies to the new nix CLI.`

读完上述内容后，我对 Flakes 的未来有了更清晰的认识：**它大概将在未来一两年内成为稳定特性**。

Flakes 带来的好处是显而易见的，整个 NixOS 社区都很喜欢它，目前超过半数的用户已经在大量使用 Flakes（尤其是 NixOS 社区的新用户），因此我们可以确定 Flakes 绝对不会被废弃。
但是 Flakes 目前仍然存在许多问题，将它推向稳定的过程中，很可能会引入一些不兼容的改动，这个改动的大小目前还无法确定。

因此总的来说，我仍然推荐大家使用 Flakes，但是也要做好准备——未来可能需要解决许多不兼容变更带来的问题。

## 参考 {#reference}

如下是我参考过的比较有用的 Nix 相关资料：

- [Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems]: 浅显易懂的 Nix Flakes 新手入门文档，值得一读。
- [NixOS 系列](https://lantian.pub/article/modify-website/nixos-why.lantian/): 这是 LanTian 大佬的 NixOS 系列文章，写得非常清晰明了，新手必读。
- [Nix Flakes Series](https://www.tweag.io/blog/2020-05-25-flakes/): 官方的 Nix Flakes 系列文章，介绍得比较详细，作为新手入门比较 OK
- [Nix Flakes - Wiki](https://nixos.wiki/wiki/Flakes): Nix Flakes 的官方 Wiki，此文介绍得比较粗略。
- [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config): 我的 NixOS 配置仓库，README 中也列出了我参考过的其他配置仓库

[digga]: https://github.com/divnix/digga
[New Nix Commands]: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix.html
[Zero to Nix - Determinate Systems]: https://github.com/DeterminateSystems/zero-to-nix
