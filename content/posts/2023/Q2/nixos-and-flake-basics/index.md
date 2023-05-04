---
title: "NixOS 与 Nix Flake 入门"
date: 2023-05-04T15:19:28+08:00
lastmod: 2023-05-04T15:19:28+08:00
draft: true

resources:
- name: "featured-image"
  src: "zero-to-nix.png"

tags: []
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

## 零、为什么选择 Nix

好几年前就听说过 Nix，用 DSL 来管理系统依赖，还能随时回滚到任一历史状态。
虽然听着很牛，但是不仅要多学一门语言，装个包还得改写代码装，当时觉得太麻烦就没考虑去学。
但是最近搞系统迁移遇到两件麻烦事，使我决定尝试下 Nix.

第一件事是在新组装的 PC 主机上安装 EndeavourOS（Arch Linux 的一个衍生发行版），因为旧系统也是 EndeavourOS 系统，安装完为了省事，我就直接把旧电脑的 Home 目录 rsync 同步到了新 PC 上。
这一同步就出了问题，所有功能都工作正常，但是视频播放老是卡住，firefox/chrome/mpv 都会卡住，网上找各种资料都没解决，还是我灵光一闪想到是不是 Home 目录同步的锅，清空了 Home 目录，问题立马就解决了...后面又花好长时间从旧电脑一点点恢复 Home 目录下的东西。

第二件事是，想尝鲜 wayland，把桌面从 i3wm 换成了 sway，但是因为用起来区别不明显，再加上诸多不便（hidpi、sway 配置调优要花时间精力，另外我用的是 sway 官方不支持的 nvidia 显卡），就还是回退到了 i3wm。结果回退后，每次系统刚启动时，有一段时间 firefox/thunar 等 GUI 程序会一直卡着。

发生第二件事时我就懒得折腾了，想到归根结底还是系统没有版本控制跟回滚机制，导致系统出了问题不能还原，装新系统时各种软件包也全靠自己手工从旧机器导出软件包清单，再在新机器安装恢复。就打算干脆换成 NixOS 试试。


## 一、Nix 简介

Nix 包管理器，跟 DevOps 领域当前流行的 plulumi/terraform 很类似，都是声明式的配置管理工具，用户需要用 DSL 语言声明好期望的系统状态，而 nix 负责达成目标。区别在于 Nix 的管理目标是软件包，而 plulumi/terraform 的管理目标是云上资源。

基于 nix 构建的 Linux 发行版 NixOS，可以简单用 OS as Code 来形容，它通过声明式的 Nix 配置文件来描述整个系统的状态。

NixOS 的配置只负责管理系统状态，用户目录不受它管辖。有另一个重要的社区项目 home-manager 专门用于管理用户目录，将 home-manager 与 NixOS、Git 结合使用，就可以得到一个完全可复现、可回滚的系统环境。

因为 nix 声明式、可复现的特性，nix 不仅可用于管理桌面电脑的环境，也有很多人用它管理开发编译环境、云上虚拟机、容器镜像构建，并且 Nix 官方也推出了基于 Nix 的运维工具 NixOps。

>Home 目录下文件众多，行为也不一，因此不可能对其中的所有文件进行版本控制，代价太高。一般仅使用 home-manager 管理一些重要的配置文件，而其他需要备份的文件可以用 rsync 定期备份到其他地方。或者用 synthing 实时同步到其他主机。

总结下 nix 的优点：

- 声明式配置，environment as code
  - nix flake 通过函数式语言的方式描述了软件包的依赖关系，并通过 flake.lock （借鉴了 cargo/npm）记录了所有依赖项的数据源与 hash 值，这使得 nix 可以在不同机器上生成完全一致的环境。
  - 这与 docker/vargrant 有点类似，不过 docker/vargrant 的目标环境都是隔离的容器或虚拟机，nix 比它们更通用，可以用于管理任何物理机、虚拟机、容器的环境。
- 可回滚：可以随时回滚到任一历史环境，NixOS 甚至默认将所有旧版本都加入到了启动项，确保系统滚挂了也能随时回滚。所以也被认为是最稳定的包管理方式。
- 没有依赖冲突问题：因为 nix 中每个软件包都拥有唯一的 hash，其安装路径中也会包含这个 hash 值，因此可以多版本共存。任何其他依赖了某个特定包的 nix 包，都会在其配置文件中声明依赖的包的 hash，这样它只能看到这个 hash 对应的包，就不存在冲突。

nix 的缺点：

- 学习成本高：如果你希望系统完全可复现，并且避免各种不当使用导致的坑，那就需要学习了解 nix 的整个设计。而其他发行版可以直接 `apt install`，因此想要用好 nix，学习成本还是比较高的。
- 文档混乱：入门文档与进阶使用之间缺乏比较好的填充，学习曲线比较陡峭。另一方面 nix flake 不仅文档比较缺乏，还与旧的 nix-env/nix-channel 相关的文档混在一起，增加了学习与辨别的难度。
- 包数量比较少：官方宣称 nixpkgs 是有 [80000+](https://search.nixos.org/packages) 个软件包，但是实际体验下来跟 arch linux 的差距还比较大，毕竟 AUR 生态是真的丰富。
  - 官方包不一定能满足需求，因此为了使系统可复现，逐渐熟悉 nix 后肯定需要学习如何自己打包。
- 比较吃硬盘空间：为了保证系统可以随时回退，nix 默认总是保留所有历史环境，这非常吃硬盘空间。虽然可以定期使用 `nix-collect-garbage` 来手动清理旧的历史环境，也还是建议配置个更大的硬盘...


## 二、安装

Nix 有多种安装方式，支持以包管理器的形式安装到 MacOS/Linux/WSL 三种系统上，Nix 还额外提供了 NixOS ——一个使用 Nix 管理整个系统环境的 Linux 发行版。

我选择了直接使用 NixOS 的 ISO 镜像安装 NixOS 系统，从而最大程度上通过 Nix 管理整个系统的环境。

安装很简单，这里不多介绍，参见相关资料：

- 国内镜像源说明：https://mirrors.bfsu.edu.cn/help/nix/
1. [Nix 的官方安装方式](https://nixos.org/download.html): 使用 bash 脚本编写, 目前（2023-04-23）为止 `nix-command` & `flake` 仍然是实验性特性，需要手动开启。
   1. 你需要参照 [Enable flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) 的说明启用 `nix-command` & `flake`
   2. 官方不提供任何卸载手段，你需要手动删除安装的所有资源 & users & group(`nixbld`).
2. [The Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer): 使用 Rust 编写, 默认启用 `nix-command` & `flake`，并且提供了官方的卸载命令。


## 三、Nix Flake 与旧的 Nix

Nix 长期依赖一直没有标准的包结构定义，直到 2020 年才推出了 `nix-command` & `flake`，它们虽然至今仍然是实验性特性，但是已经得到广泛使用，是强烈推荐使用的功能。

因为 nix-command 与 flake 还未 stable，旧的 Nix 包结构与相关命令行工具仍然是大量 Nix Wiki/教程中的主要内容，从可复现、易于管理维护的角度讲，旧的 Nix 包结构与命令行工具已经不推荐使用了，因此本文档也不会介绍旧的 Nix 包结构与命令行工具的使用方法，也建议新手直接忽略掉这些旧的内容，从 nix flake 学起。

这里列举下在 nix flake 中已经不需要用到的旧的 Nix 命令行工具与相关概念，在查找资料时，如果看到它们直接忽略掉就行：

1. `nix-channel`: nix-channel 与其他包管理工具类似，通过 stable/unstable/test 等 channel 来管理软件包的版本。
   1. nix flake 在 flake.nix 中通过 inputs 声明依赖包的数据源，通过 flake.lock 锁定依赖版本，完全取代掉了 nix-channel 的功能。
2. `nix-env`: 用于管理用户环境的软件包，是传统 Nix 的核心命令行工具。它从 nix-channel 定义的数据源中安装软件包，所以安装的软件包版本受 channel 影响。通过 `nix-env` 安装的包不会被自动记录到 nix 的声明式配置中，是完全脱离掌控的，无法在其他主机上复现，因此不推荐使用。
   1. 在 nix flake 中对应的命令为 `nix profile`
3. `nix-shell`: nix-shell 用于创建一个临时的 shell 环境
   1. 在 nix flake 中它被 `nix develop` 与 `nix shell` 取代了。
4. ...



## 五、NixOS 的包仓库

跟 Arch Linux 类似，Nix 也有官方与社区的软件包仓库：

1. [nixpkgs](https://github.com/NixOS/nixpkgs) 是一个包含了所有 nix 包与 nixos 模块/配置的 Git 仓库，其 master 分支包含最新的 nix 包与 nixos 模块/配置。
2. [NUR](https://github.com/nix-community/NUR): 类似 Arch Linux 的 AUR，NUR 是 Nix 的一个第三方的 nix 包仓库，它包含了一些 nix 包，但是它们并不包含在 nixpkgs 仓库中，因此需要单独安装。
3. Nix Flake 也可直接从 Git 仓库中安装软件包，这种方式可以用于安装一些不在 nixpkgs 仓库中的软件包，或者安装 nixpkgs 仓库中的开发分支的软件包。


## 六、Nix 语言基础

>https://nix.dev/tutorials/nix-language

Nix 语言是一门比较简单的语言，在已有一定编程基础的情况下，过一遍这些语法用时应该在 2 个小时以内。

主要包含如下内容：

1. 数据类型
2. 函数的声明与调用语法
3. 内置函数与库函数
4. inputs 的不纯性
5. 用于描述 build task 的 derivation

### 1. 基础数据类型一览

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

以及一些基础操作符，普通的算术运算、布尔运算就跳过了：

```nix
# List concatenation
[ 1 2 3 ] ++ [ 4 5 6 ] # [ 1 2 3 4 5 6 ]

# Update attribute set attrset1 with names and values from attrset2.
{ a = 1; b = 2; } // { b = 3; c = 4; } # { a = 1; b = 3; c = 4; }

# 逻辑隐含，等同于 !b1 || b2.
bool -> bool
```

### 2. attribute set 说明

花括号 `{}` 用于创建 attribute set，也就是 key-value 对的集合，类似于 JSON 中的对象。

attribute set 默认不支持递归引用，如下内容会报错：

```nix
{
  a = 1;
  b = a + 1; # error: undefined variable 'a'
}
```

不过 nix 提供了 `rec` 关键字（recursive attribute set），可用于创建递归引用的 attribute set：

```nix
rec {
  a = 1;
  b = a + 1; # ok
}
```

在递归引用的情况下，nix 会按照声明的顺序进行求值，所以如果 `a` 在 `b` 之后声明，那么 `b` 会报错。

可以使用 `.` 操作符来访问 attribute set 的成员：

```nix
let
  a = {
    b = {
      c = 1;
    };
  };
in
a.b.c # result is 1
```

`.` 操作符也可直接用于赋值：

```nix
{ a.b.c = 1; }
```

### 3. let ... in ...

nix 的 `let ... in ...` 语法被称作「let 表达式」或者「let 绑定」，它用于创建临时使用的局部变量：

```nix
let
  a = 1;
in
a + a  # result is 2
```

let 表达式中的变量只能在 `in` 之后的表达式中使用，理解成临时变量就行。

### 4. with 语句


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
with a; [ x y z ]  # result is [ 1 2 3 ], equavlent to [ a.x a.y a.z ]
```

### 5. 继承 inherit ...

`inherit` 语句用于从 attribute set 中继承成员，同样是一个简化代码的语法糖，比如：

```nix
let
  x = 1;
  y = 2;
in
{
  inherit x y;
}  # result is { x = 1; y = 2; }
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
}  # result is { x = 1; y = 2; }
```

### 6. ${ ... } 字符串插值

`${ ... }` 用于字符串插值，懂点编程的应该都很容易理解这个，比如：

```nix
let
  a = 1;
in
"the value of a is ${a}"  # result is "the value of a is 1"
```

### 7. 文件系统路径

Nix 中不带引号的字符串会被解析为文件系统路径，路径的语法与 Unix 系统相同。

### 8. 搜索路径

>请不要使用这个功能，搜索路径不是 pure 的，会导致不可预期的行为。

Nix 会在看到 `<nixpkgs>` 这类三角括号语法时，会在 `NIX_PATH` 环境变量中指定的路径中搜索该路径。

因为环境变量 `NIX_PATH` 是可变更的值，所以这个功能是不纯的，会导致不可预期的行为。

### 9. 多行字符串

多行字符串的语法为 `''`，比如：

```nix
''
  this is a
  multi-line
  string
''
```

### 10. 函数

函数的声明语法为：

```nix
<arg1>:
  <body>;
```

举几个常见的例子：

```nix
# function with one argument
a: a + a

# 嵌套函数
a: b: a + b

# function with two arguments
{ a, b }: a + b

# function with two arguments and default values
{ a ? 1, b ? 2 }: a + b

# 带有命名 attribute set 作为参数的函数，并且使用 ... 收集其他可选参数
# 命名 args 与 ... 可选参数通常被一起作为函数的参数定义使用
args@{ a, b, ... }: a + b + args.c
# 如下内容等价于上面的内容
{ a, b, ... }@args: a + b + args.c

# 但是要注意命名参数仅绑定了输入的 attribute set，默认参数不在其中，举例
let 
  f = { a ? 1, b ? 2, ... }@args: args  # this will cause an error
in
  f {}  # result is {}

# 函数的调用方式就是把参数放在后面，比如下面的 2 就是前面这个函数的参数
a: a + a 2  # result is 4

# 还可以给函数命名，不过必须使用 let 表达式
let
  f = a: a + a;
in
f 2  # result is 4
```

#### 内置函数

Nix 内置了一些函数，可通过 `builtins.<function-name>` 来调用，比如：

```nix
builtins.add 1 2  # result is 3
```

详细的内置函数列表参见 [Built-in Functions - Nix Reference Mannual](https://nixos.org/manual/nix/stable/language/builtins.html)

#### import 表达式

`import` 表达式以其他 nix 文件的路径作为参数，返回该 nix 文件的执行结果。

`import` 的参数如果为文件夹路径，那么会返回该文件夹下的 `default.nix` 文件的执行结果。

举个例子，首先创建一个 `file.nix` 文件：

```shell
$ echo "x: x + 1" > file.nix
```

然后使用 import 执行它：

```nix
import ./file.nix 1  # result is 2
```

#### pkgs.lib 函数包

除了 builtins 之外，Nix 的 nixpkgs 仓库还提供了一个名为 `lib` 的 attribute set，它包含了一些常用的函数，它通常被以如下的形式被使用：

```nix
let
  pkgs = import <nixpkgs> {};
in
pkgs.lib.strings.toUpper "search paths considered harmful"  # result is "SEARCH PATHS CONSIDERED HARMFUL"
```


可以通过 [Nixpkgs Library Functions - Nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#sec-functions-library) 查看 lib 函数包的详细内容。

### 11. 不纯

Nix 语言本身是纯函数式的，是纯的，也就是说它就跟数学中的函数一样，同样的输入永远得到同样的输出。

**Nix 唯一的不纯之处在这里：从文件系统路径或者其他输入源中读取文件作为构建任务的输入**。

nix 的构建输入只有两种，一种是从文件系统路径等输入源中读取文件，另一种是将其他函数作为输入。

>nix 中的搜索路径与 `builtins.currentSystem` 也是不纯的，但是这两个功能都不建议使用，所以这里略过了。

### 12. Fetchers

构建输入除了直接来自文件系统路径之外，还可以通过 Fetchers 来获取，Fetcher 是一种特殊的函数，它的输入是一个 attribute set，输出是 nix store 中的一个系统路径。

Nix 提供了四个内置的 Fetcher，分别是：

- `builtins.fetchurl`：从 url 中下载文件
- `builtins.fetchTarball`：从 url 中下载 tarball 文件
- `builtins.fetchGit`：从 git 仓库中下载文件
- `builtins.fetchClosure`：从 Nix store 中获取 derivation


举例：

```nix
builtins.fetchurl "https://github.com/NixOS/nix/archive/7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"
# result example => "/nix/store/7dhgs330clj36384akg86140fqkgh8zf-7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"

builtins.fetchTarball "https://github.com/NixOS/nix/archive/7c3ab5751568a0bc63430b33a5169c5e4784a0ff.tar.gz"
# result example(auto unzip the tarball) => "/nix/store/d59llm96vgis5fy231x6m7nrijs0ww36-source"
```


### 13. Derivations

一个构建动作的 nix 语言描述被称做一个 Derivation，它描述了如何构建一个软件包，它的执行结果是一个 store object

在 Nix 语言的最底层，一个构建任务就是使用 builtins 中的不纯函数 `derivation` 创建的，我们实际使用的 `stdenv.mkDerivation` 就是它的一个 wrapper，屏蔽了底层的细节，简化了用法。

### 14. stdenv.mkDerivation

stdenv，顾名思义即标准构建环境，它是一个 attribute set，提供了构建 Unix 程序所需的标准环境，比如 gcc、glibc、binutils 等等。
它可以完全取代我们在其他操作系统上常用的构建工具链，比如 `./configure`; `make`; `make install` 等等。

即使 stdenv 提供的环境不能满足你的要求，你也可以通过 `stdenv.mkDerivation` 来创建一个自定义的构建环境。

举个例子：

```nix
{ lib, stdenv }:

stdenv.mkDerivation rec {
  pname = "libfoo";
  version = "1.2.3";
  # 源码
  src = fetchurl {
    url = "http://example.org/libfoo-source-${version}.tar.bz2";
    sha256 = "0x2g1jqygyr5wiwg4ma1nd7w4ydpy82z9gkcv8vh2v8dn3y58v5m";
  };

  # 构建依赖
  buildInputs = [libbar perl ncurses];

  # Nix 默认将构建拆分为一系列 phases，这里仅用到其中两个
  # https://nixos.org/manual/nixpkgs/stable/#ssec-controlling-phases
  buildPhase = ''
    gcc foo.c -o foo
  '';
  installPhase = ''
    mkdir -p $out/bin
    cp foo $out/bin
  '';
}
```


### 15. Override 与 Overlays

TODO


## 七、以声明式的方式管理系统

>https://nixos.wiki/wiki/Overview_of_the_NixOS_Linux_distribution

了解了 Nix 语言的基本用法之后，我们就可以开始使用 Nix 语言来配置 NixOS 系统了。NixOS 的系统配置路径为 `/etc/nixos/configuration.nix`，它包含系统的所有声明式配置，如时区、语言、键盘布局、网络、用户、文件系统、启动项等。

如果想要以可复现的方式修改系统的状态（这也是最推荐的方式），就需要手工修改 `/etc/nixos/configuration.nix` 文件，然后执行 `sudo nixos-rebuild switch` 命令来应用配置，此命令会根据配置文件生成一个新的系统环境，并将新的环境设为默认环境。
同时上一个系统环境会被保留，而且会被加入到 grub 的启动项中，这确保了即使新的环境不能启动，也能随时回退到旧环境。

另一方面，`/etc/nixos/configuration.nix` 是传统的 Nix 配置方式，它依赖 nix-channel 配置的数据源，也没有任何版本锁定机制，实际无法确保系统的可复现性。
更推荐使用的是 Nix Flake，它可以确保系统的可复现性，同时也可以很方便地管理系统的配置。

我们下面会分别介绍这两种配置方式。

### 1. 使用 `/etc/nixos/configuration.nix` 配置系统

前面提过了这是传统的 Nix 配置方式，也是当前 NixOS 默认使用的配置方式，它依赖 nix-channel 配置的数据源，也没有任何版本锁定机制，实际无法确保系统的可复现性。

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

这里我启用了 openssh 服务，并为 ryan 用户添加了 ssh 公钥，并禁用了密码登录。

然后运行 `sudo nixos-rebuild switch` 后，就可以通过 ssh 登录到我的系统了，密码登录会直接报错。

这就是 NixOS 最基础的声明式系统配置，要对系统做任何可复现的变更，都只需要修改 `/etc/nixos/configuration.nix` 文件，然后运行 `sudo nixos-rebuild switch` 即可。

### 2. 启用 NixOS 的 Flake 支持

与 NixOS 默认的配置方式相比，Flake 提供了更好的可复现性，同时它定义的包结构也更加清晰，更容易维护，因此更建议使用 Flake 来管理系统配置。

但是目前 flake 作为一个实验性的功能，仍未被默认启用。所以我们需要手动启用它，修改 `/etc/nixos/configuration.nix` 文件，在函数块中启用 flakes 与 nix-command 功能：

```nix
{ config, pkgs, ... }:

{
  nix.settings.experimental-features = [ "nix-command" "flakes" ];
}
```

然后运行 `sudo nixos-rebuild switch` 应用修改后，即可使用 flake 来管理系统配置。


### 3. 将系统配置修改为 flake.nix

在启用了 Nix Flake 特性后，`sudo nixos-rebuild switch` 命令会优先读取 `/etc/nixos/flake.nix` 文件，如果找不到再尝试使用 `/etc/nixos/configuration.nix`。

可以首先使用官方提供的模板来学习 flake 的编写，先查下有哪些模板：

```bash
nix flake show templates
```

其中有个 `templates#full` 模板展示了所有可能的用法，可以看看它的内容：

```bash
nix flake init -t templates#full
cat flake.nix
```

简单浏览后，我们创建文件 `/etc/nixos/flake.nix`，后续系统的所有修改都将全部由 nix flake 接管，参照前面的模板，编写如下内容：

```nix
{
  description = "Ryan's NixOS Flake";

  # 这是 flake.nix 的标准格式，inputs 是 flake 的依赖，outputs 是 flake 的输出
  # inputs 中的每一项依赖都会在被拉取、构建后，作为参数传递给 outputs 函数 
  inputs = {
    # flake inputs 有很多种引用方式，应用最广泛的是 github 的引用方式

    # NixOS 官方软件源，这里使用 nixos-unstable 分支
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # home-manager，用于管理用户配置
    home-manager = {
      url = "github:nix-community/home-manager/release-22.11";
      # follows 是 inputs 中的继承语法
      # 这里使 home-manager 的 nixpkgs 这个 inputs 与当前 flake 的 inputs.nixpkgs 
      # 保持一致，避免依赖的 nixpkgs 版本不一致导致问题
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
    # 名为 nixosConfigurations 的 outputs 会在执行 `nixos-rebuild switch --flake .` 时被使用
    # 默认情况下会使用与主机 hostname 同名的 nixosConfigurations，但是也可以通过 `--flake .#<name>` 来指定
    nixosConfigurations = {
      # hostname 为 nixos-test 的主机会使用这个配置
      # 这里使用了 nixpkgs.lib.nixosSystem 函数来构建配置，后面的 attributes set 是它的参数
      # 在 nixos 系统上使用如下命令即可部署此配置：`nixos-rebuild switch --flake .#nixos-test`
      "nixos-test" = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # modules 中每个参数，都是一个 NixOS Module <https://nixos.org/manual/nixos/stable/index.html#sec-modularity>
        # NixOS Module 可以是一个 attribute set，也可以是一个返回 attribute set 的函数
        # 如果是函数，那么它的参数就是当前的 NixOS Module 的参数.
        # 根据 Nix Wiki 对 NixOS modules 的描述，NixOS modules 函数的参数可以有这四个（详见本仓库中的 modules 文件）：
        # 
        #  config: The configuration of the entire system
        #  options: All option declarations refined with all definition and declaration references.
        #  pkgs: The attribute set extracted from the Nix package collection and enhanced with the nixpkgs.config option.
        #  modulesPath: The location of the module directory of NixOS.
        #
        # 默认只能传上面这四个参数，如果需要传其他参数，必须使用 specialArgs
        # nix flake 的 modules 系统可将配置模块化，提升配置的可维护性
        modules = [
          # 导入之前我们使用的 configuration.nix，这样旧的配置文件仍然能生效
          # 注：configuration.nix 本身也是一个 NixOS Module，因此可以直接在这里导入
          ./configuration.nix
        ];
      };
    };
  };
}
```

这里我们定义了一个名为 nixos 的系统，它的配置文件为 `./configuration.nix`，这个文件就是我们之前的配置文件，这样我们仍然可以沿用旧的配置。

现在执行 `nixos-rebuild switch` 应用配置。

### 4. 为 Flake 添加国内 cache 源

NixOS 为了加快包构建速度，提供了 <https://cache.nixos.org> 提前缓存构建结果提供给用户，但是在国内这个地址非常地慢，如果没有全局代理的话，基本上是无法使用的。

在旧的 NixOS 配置方式中，可以通过 `nix-channel` 来添加国内的 cache 源，但是在 flake 中，这个方式已经不再适用了。

Flake 为了提升可复现性，会尽可能地避免使用任何系统级别的配置、环境变量等，我们必须在 flake.nix 中添加 cache 的国内镜像地址，这就是 `nixConfig` 参数，示例如下：

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # 为了确保够纯，Flake 不依赖系统自身的 /etc/nix/nix.conf，而是在 flake.nix 中通过 nixConfig 设置
  # 但是为了确保安全性，flake 默认仅允许直接设置少数 nixConfig 参数，其他参数都需要在执行 nix 命令时指定 `--accept-flake-config`，否则会被忽略
  # <https://nixos.org/manual/nix/stable/command-ref/conf-file.html>
  # 注意：即使添加了国内 cache 镜像，如果有些包国内镜像下载不到，它仍然会走国外，这时候就得靠旁路由来解决了。
  # 临时修改系统默认网关为旁路由 ip:  sudo ip route add default via 192.168.5.201
  #                    还原修改:   sudo ip route del default via 192.168.5.201
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

改完后部署即可生效。

### 5. 安装 home-manager

前面简单提过，NixOS 自身的配置文件只能管理系统级别的配置，而用户级别的配置则需要使用 home-manager 来管理。
根据官方文档 [Home Manager Manual](https://nix-community.github.io/home-manager/index.htm)，安装流程如下：

我希望将 home manager 作为 NixOS 模块安装，首先需要创建 `/etc/nixos/home.nix`，示例如下：

```nix
{ config, pkgs, ... }:

{
  # 注意修改这里的用户名与用户目录
  home.username = "ryan";
  home.homeDirectory = "/home/ryan";

  # git 相关配置
  programs.git = {
    enable = true;
    userName = "Ryan Yin";
    userEmail = "xiaoyin_c@qq.com";
  };

  # Packages that should be installed to the user profile.
  home.packages = [ 
    pkgs.htop
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

  # alacritty 终端配置，貌似还需要配置 X11 环境，否则无法启动
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

然后再使用如下命令创建 `/etc/nixos/flake.nix`：

```shell
nix flake new /etc/nixos -t github:nix-community/home-manager#nixos
```

通过模板生成好 `/etc/nixos/flake.nix` 配置后不是万事大吉，还得手动改下相关参数：

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
            # 这里的 import 指令在前面 Nix 语法中介绍过了，不再赘述
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

你可以在 [Home Manager - Appendix A. Configuration Options](https://nix-community.github.io/home-manager/options.html) 中找到 Home Manager 支持的所有配置项，它涵盖了几乎所有常用的程序，建议通过关键字搜索自己需要的配置项。


### 6. Nix Flake's Command Line

after enabled `nix-command` & `flake`, you can use `nix help` to get all the info of [New Nix Commands][New Nix Commands], the main commands include:

- `nix build` - build a derivation or fetch a store path, generate a result symlink in the current directory
- `nix develop` - run a bash shell that provides the build environment of a derivation
- `nix flake` - provides subcommands for creating, modifying and querying Nix flakes.
  - `nix flake archive` - copy a flake and all its inputs to a store 
  - `nix flake check` - check whether the flake evaluates and run its tests 
  - `nix flake clone` - clone flake repository 
  - `nix flake info` - show flake metadata 
  - `nix flake init` - create a flake in the current directory from a template 
  - `nix flake lock` - create missing lock file entries 
  - `nix flake metadata` - show flake metadata 
  - `nix flake new` - create a flake in the specified directory from a template 
  - `nix flake prefetch` - download the source tree denoted by a flake reference into the Nix store 
  - `nix flake show` - show the outputs provided by a flake 
  - `nix flake update` - update flake lock file 
- `nix profile` - manage Nix profiles. nix profile allows you to create and manage Nix profiles. A Nix profile is a set of packages that can be installed and upgraded independently from each other. Nix profiles are versioned, allowing them to be rolled back easily. its a replacement of `nix-env`.
    - `nix profile diff-closures` - show the closure difference between each version of a profile 
    - `nix profile history` - show all versions of a profile 
    - `nix profile install` - install a package into a profile 
    - `nix profile list` - list installed packages 
    - `nix profile remove` - remove packages from a profile 
    - `nix profile rollback` - roll back to the previous version or a specified version of a profile 
    - `nix profile upgrade` - upgrade packages using their most recent flake 
    - `nix profile wipe-history` - delete non-current versions of a profile 
- `nix repl` - start an interactive environment for evaluating Nix expressions
- `nix run` - run a Nix application. (use `nix run --help` for detail explanation)
- `nix search` - search for packages, maybe your woulde prefer the website <https://search.nixos.org> instead of this command.
- `nix shell` - run a shell in which the specified packages are available

[Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems] is a brand new guide to get started with Nix & Flake, recommended to read for beginners.

### 7. Flake 的 outputs

Flake outputs are what a flake produces as part of its build. Each flake can have many different outputs simultaneously, including but not limited to:

- Nix packages: named `apps.<system>.<name>`, `packages.<system>.<name>`, or `legacyPackages.<system>.<name>`
- Nix Helper Functions: named `lib`, which means a library for other flakes.
- Nix development environments: named `devShell`
- NixOS configurations: has many different outputs
- Nix templates: named `templates`
  - templates can be used by command `nix flake init --template <reference>`
- 其他用户自定义的 outputs

### Flake 命令行的使用

```bash
# `nixpkgs#ponysay` means `ponysay` from `nixpkgs` flake.
# [nixpkgs](https://github.com/NixOS/nixpkgs) contains `flake.nix` file, so it's a flake.
# `nixpkgs` is a falkeregistry id for `github:NixOS/nixpkgs/nixos-unstable`.
# you can find all the falkeregistry ids at <https://github.com/NixOS/flake-registry/blob/master/flake-registry.json>
# so this command means install and run package `ponysay` in `nixpkgs` flake.
echo "Hello Nix" | nix run "nixpkgs#ponysay"

# this command is the same as above, but use a full flake URI instead of falkeregistry id.
echo "Hello Nix" | nix run "github:NixOS/nixpkgs/nixos-unstable#ponysay"

# instead of treat flake package as an application, 
# this command use the example package in zero-to-nix flake to setup the development environment,
# and then open a bash shell in that environment.
nix develop "github:DeterminateSystems/zero-to-nix#example"

# instead of using a remote flake, you can open a bash shell using the flake located in the current directory.
mkdir my-flake && cd my-flake
## init a flake with template
nix flake init --template "github:DeterminateSystems/zero-to-nix#javascript-dev"
# open a bash shell using the flake in current directory
nix develop
# or if your flake has multiple devShell outputs, you can specify which one to use.
nix develop .#example

# build package `bat` from flake `nixpkgs`, and put a symlink `result` in the current directory.
mkdir build-nix-package && cd build-nix-package
nix build "nixpkgs#bat"
# build a local flake is the same as nix develop, skip it
```


## 八、使用 Nix Flake 打包应用

有时候我们需要使用的应用，nixpkgs 不一定有，社区也找不到，那就只能自己动手打包了。

TODO

## 进阶玩法

在对 Nix Flake 熟悉到一定程度后，你可以尝试一些进阶玩法，如下是一些比较流行的社区项目，可以试用：

- [flake-parts](https://github.com/hercules-ci/flake-parts): Simplify Nix Flakes with the module system, useful to hold multiple system configurations in a single flake.
- [flake-utils-plus](https://github.com/gytis-ivaskevicius/flake-utils-plus): an more powerful utils for flake development.
- [digga][digga]: a powerful nix flake template to hold multiple host's configurations in a single flake.
- [devshell](https://github.com/numtide/devshell)
- etc.


## 参考

- [NixOS 系列（一）：我为什么心动了](https://lantian.pub/article/modify-website/nixos-why.lantian/): 这是 LanTian 大佬的 NixOS 系列文章，写得非常清晰明了，新手必读。
- [Nix Flakes Series](https://www.tweag.io/blog/2020-05-25-flakes/): 官方的 Nix Flake 系列文章，介绍得比较详细，作为新手入门比较 OK
- [Nix Flakes - Wiki](https://nixos.wiki/wiki/Flakes): Nix Flakes 的官方 Wiki，此文介绍得比较粗略。
- 一些参考 nix 配置
  - [xddxdd/nixos-config](https://github.com/xddxdd/nixos-config)
  - [bobbbay/dotfiles](https://github.com/bobbbay/dotfiles)
  - [gytis-ivaskevicius/nixfiles](https://github.com/gytis-ivaskevicius/nixfiles)
  - [fufexan/dotfiles](https://github.com/fufexan/dotfiles): 好漂亮，教练我想学这个
  - [davidak/nixos-config](https://codeberg.org/davidak/nixos-config)
  - [davidtwco/veritas](https://github.com/davidtwco/veritas)
- [NixOS 手册](https://nixos.org/manual/nixos/stable/index.html): 要想把 NixOS 玩透，这是必读的。前面的文章读来会发现很多陌生的概念，需要靠这个补全。
  - 不过也不是说要把所有内容都补一遍，先看个大概，后面有需要再按图索骥即可。



[digga]: https://github.com/divnix/digga
[New Nix Commands]: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix.html
[Zero to Nix - Determinate Systems]: https://github.com/DeterminateSystems/zero-to-nix
