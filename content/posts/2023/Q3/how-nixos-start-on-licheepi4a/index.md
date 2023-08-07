---
title: "NixOS 在 Lichee Pi 4A 上是如何启动的"
subtitle: ""
description: ""
date: 2023-08-07T18:40:57+08:00
lastmod: 2023-08-07T18:40:57+08:00
draft: true

resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: [Linux", "NixOS", "LicheePi4A", "Embedded", "U-Boot", "RISC-V"]
categories: ["tech"]
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

## 前言

我从今年 5 月份初收到了内测板的 Lichee Pi 4A，这是当下性能最高的 RISC-V 开发板之一，不过当时没怎么折腾。

6 月初的时候我开始尝试在 Orange Pi 5 上运行 NixOS，在 [NixOS on ARM 的 Matrix 群组](https://matrix.to/#/#nixos-on-arm:nixos.org) 中得到了 @K900 的帮助，没费多大劲就成功了，一共就折腾了三天。

于是我接着尝试在 Lichee Pi 4A 上运行 NixOS，因为已经拥有了 Orange Pi 5 上的折腾经验，我以为这次会很顺利。
但是实际难度远远超出了我的预期，我从 6 月 13 号开始断断续续折腾到 7 月 3 号，接触了大量的新东西，包括 U-Boot、OpenSBI、SPL Flash、RISCV Boot Flows 等等，
还参考了 @chainsx 的 Fedora for Lichee Pi 4A 方案，请教了 @NickCao 许多 NixOS 相关的问题，@revy 帮我修了好几个 revyos/thead-kernel 在标准工具链上编译的 bug，期间也请教过 @HougeLangley 他折腾 Lichee Pi 4A 的经验。
我在付出了这么多的努力后，才最终成功编译出了 NixOS 的系统镜像（包含 boot 跟 rootfs 两个分区）。

但是！现在要说「但是」了。

镜像是有了，系统却无法启动...找了各种资料也没解决，也没好意思麻烦各位大佬，搞得有点心灰意冷，就先把这部分工作放下了。

接着就隔了一个多月没碰 Lichee Pi 4A，直到 8 月 5 号，外国友人 @JayDeLux 在 [Mainline Linux for RISC-V](https://t.me/linux4rv) TG 群组中 ping 了下我，我才决定再次尝试一下。

在之前工作的基础上一番骚操作后，我在 8 月 6 号晚上终于成功启动了 NixOS，这次意外的顺利，后续也成功通过一份 Nix Flake 配置编译出了可用的 NixOS 镜像。

最终成果：<https://github.com/ryan4yin/nixos-licheepi4a>

这个折腾过程挺曲折，虽然最终达成了目标，但是期间遭受了不少折磨 emmm
不过也是一次有趣的经历，学到了许多新技术知识、认识了些有趣的外国友人（@JayDeLux 甚至还给我打了 $50 美刀表示感谢），也跟 @HougeLangley 、@chainsx 、@Rabenda(revy) 等各位大佬混了个脸熟。

这篇文章就是记录下我在这个折腾过程中学到的所有知识，以飨读者，同时也梳理一下自己的收获。

本文的写作思路是自顶向下的，先从 NixOS 镜像的 boot 分区配置、启动脚本开始分析，过渡到实际的启动日志，这样先对整个启动过程有个大概的了解，接着再详细分析其中各个陌生概念的含义、各组件的作用。

## Lichee Pi 4A 介绍

LicheePi 4A 是当前市面上性能最高的 RISC-V Linux 开发板之一，它以 TH1520 为主控核心（4xC910@1.85G， RV64GCV，4TOPS@int8 NPU， 50GFLOP GPU），板载最大 16GB 64bit LPDDR4X，128GB eMMC，支持 HDMI+MIPI 双4K 显示输出，支持 4K 摄像头接入，双千兆网口（其中一个支持POE供电）和 4 个 USB3.0 接口，多种音频输入输出（由专用 C906 核心处理）。

以上来自 Lichee Pi 4A 官方文档 [Lichee Pi 4A - Sipeed Wiki](https://wiki.sipeed.com/hardware/zh/lichee/th1520/lpi4a/1_intro.html).

总之它是我手上性能最高的 RISC-V 开发板。

LicheePi 4A 官方主要支持 [RevyOS](https://github.com/revyos/revyos/)—— 一款针对 T-Head 芯片生态的 Debian 优化定制发行版。
根据猴哥（@HougeLangley）文章介绍，它也是目前唯一且确实能够启用 Lichee Pi 4A 板载 GPU 的发行版，

RevyOS 的内核、u-boot 和 opensbi 代码仓库：

- https://github.com/revyos/thead-kernel.git
- https://github.com/revyos/thead-u-boot.git
- https://github.com/revyos/thead-opensbi.git

## NixOS 介绍

这个感觉就不用多说了啊，我在这几个月已经给 NixOS 写了非常多的文字了，感兴趣请直接移步 [ryan4yin/nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book).

在 4 月份接触了 NixOS 后，我成了 NixOS 铁粉。
作为一名铁粉，我当然想把我手上的所有性能好点的板子都装上 NixOS，Lichee Pi 4A 自然也不例外。

我目前主要完成了两块板子的 NixOS 移植工作，一块是 Orange Pi 5，另一块就是 Lichee Pi 4A。
Orange Pi 5 是 ARM64 架构的，刚好也遇到了拥有该板子的 NixOS 用户 @K900，在他的帮助下我很顺利地就完成了移植工作。

而 Lichee Pi 4A 就比较曲折，也比较有话题性。所以才有了这篇文章。

## 移植思路

LicheePi 4A use RevyOS officially. The basic idea of this repo is to use revyos's kernel, u-boot and opensbi, with a NixOS rootfs, to get NixOS running on LicheePi 4A.


## NixOS 启动流程分析

rootfs 已经成功构建完成，内容如下：

```bash
╭───┬───────────────────────┬──────┬──────────┬──────────────╮
│ # │         name          │ type │   size   │   modified   │
├───┼───────────────────────┼──────┼──────────┼──────────────┤
│ 0 │ boot                  │ dir  │   4.1 KB │ 53 years ago │
│ 1 │ lost+found            │ dir  │  16.4 KB │ 53 years ago │
│ 2 │ nix                   │ dir  │   4.1 KB │ 53 years ago │
│ 3 │ nix-path-registration │ file │ 242.7 KB │ 53 years ago │
╰───┴───────────────────────┴──────┴──────────┴──────────────╯
```

可以看到 NixOS 整个根目录下一共就两个文件夹 `/boot` 跟 `/nix/store`，这与传统的 Linux 发行版大相径庭。
传统的 Linux 发行版遵循 UNIX 系统的 [FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) 标准，根目录下会有很多文件夹，比如 `/bin`、`/etc`、`/home`、`/lib`、`/opt`、`/root`、`/sbin`、`/srv`、`/tmp`、`/usr`、`/var` 等等。

仔细看下 `/boot` 的内容：

```bash
› tree
.
├── extlinux
│   └── extlinux.conf
└── nixos
    ├── rzc42b6qjxy10wb1wkfmrxjcxsw52015-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-dtbs
    │   ├── sifive
    │   │   └── hifive-unleashed-a00.dtb
    │   └── thead
    │       ├── fire-emu-crash.dtb
    │       ├── fire-emu.dtb
    │       ├── fire-emu-gpu-dpu-dsi0.dtb
    │       ├── fire-emu-soc-base.dtb
    │       ├── fire-emu-soc-c910x4.dtb
    │       ├── fire-emu-vi-dsp-vo.dtb
    │       ├── fire-emu-vi-vp-vo.dtb
    │       ├── ......
    │       ├── light-fm-emu-dsi0-hdmi.dtb
    │       ├── light-fm-emu-dsp.dtb
    │       ├── light-fm-emu.dtb
    │       ├── light-fm-emu-gpu.dtb
    │       ├── light-fm-emu-hdmi.dtb
    │       ├── light-fm-emu-npu-fce.dtb
    │       ├── light-lpi4a-ddr2G.dtb
    │       ├── light-lpi4a.dtb
    │       └── light_mpw.dtb
    ├── rzc42b6qjxy10wb1wkfmrxjcxsw52015-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-Image
    └── vh8624bjxdpxh7ds3nqvqbx992yx63hp-initrd-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-initrd

5 directories, 61 files
```

可以看到它使用 extlinux 作为 bootloader，再看下 extlinux 的配置内容：


```bash
› cat extlinux.conf
# Generated file, all changes will be lost on nixos-rebuild!

# Change this to e.g. nixos-42 to temporarily boot to an older configuration.
DEFAULT nixos-default

MENU TITLE ------------------------------------------------------------
TIMEOUT 50

LABEL nixos-default
  MENU LABEL NixOS - Default
  LINUX ../nixos/rzc42b6qjxy10wb1wkfmrxjcxsw52015-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-Image
  INITRD ../nixos/vh8624bjxdpxh7ds3nqvqbx992yx63hp-initrd-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-initrd
  APPEND init=/nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37/init console=ttyS0,115200 root=/dev/mmcblk0p3 rootfstype=ext4 rootwait rw earlycon clk_ignore_unused eth=$ethaddr rootrwoptions=rw,noatime rootrwreset=yes loglevel=4
  FDT ../nixos/rzc42b6qjxy10wb1wkfmrxjcxsw52015-linux-riscv64-unknown-linux-gnu-5.10.113-thead-1520-dtbs/thead/light-lpi4a.dtb
```

可以看到它使用了 `/nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37/init` 作为 init 程序，系统的 rootfs 分区为 `/dev/mmcblk0p3`，使用的文件系统为 ext4，等等。


再看下 init 脚本，会发现 `/etc` `/etc/nixos` `/tmp` `/run` `/proc` `/dev` `/sys` 等文件夹都是在这一步被自动创建的，而且其中许多东西都是直接 symlink 到 `/nix/store` 中的文件：

```bash
› cat /nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37/init
#! /nix/store/ny69lqq5dgw5xz6h5ply8cwzifcvplxx-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash

systemConfig=/nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37

export HOME=/root PATH="/nix/store/4l7v9y3r2mp2sdhjxjl35yvjsxmrdl4h-coreutils-riscv64-unknown-linux-gnu-9.1/bin:/nix/store/c1xb4z38bvl29vbvc2la2957gv9sdy61-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin"


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Process the kernel command line.
    for o in $(</proc/cmdline); do
        case $o in
            boot.debugtrace)
                # Show each command.
                set -x
                ;;
        esac
    done


    # Print a greeting.
    echo
    echo -e "\e[1;32m<<< NixOS Stage 2 >>>\e[0m"
    echo


    # Normally, stage 1 mounts the root filesystem read/writable.
    # However, in some environments, stage 2 is executed directly, and the
    # root is read-only.  So make it writable here.
    if [ -z "$container" ]; then
        mount -n -o remount,rw none /
    fi
fi


# Likewise, stage 1 mounts /proc, /dev and /sys, so if we don't have a
# stage 1, we need to do that here.
if [ ! -e /proc/1 ]; then
    specialMount() {
        local device="$1"
        local mountPoint="$2"
        local options="$3"
        local fsType="$4"

        # We must not overwrite this mount because it's bind-mounted
        # from stage 1's /run
        if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" = true ] && [ "${mountPoint}" = /run ]; then
            return
        fi

        install -m 0755 -d "$mountPoint"
        mount -n -t "$fsType" -o "$options" "$device" "$mountPoint"
    }
    source /nix/store/z1b5brgask2dvsq2gjkk8vc9rv5r2c0y-mounts.sh
fi


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" = true ]; then
    echo "booting system configuration ${systemConfig}"
else
    echo "booting system configuration $systemConfig" > /dev/kmsg
fi


# Make /nix/store a read-only bind mount to enforce immutability of
# the Nix store.  Note that we can't use "chown root:nixbld" here
# because users/groups might not exist yet.
# Silence chown/chmod to fail gracefully on a readonly filesystem
# like squashfs.
chown -f 0:30000 /nix/store
chmod -f 1775 /nix/store
if [ -n "1" ]; then
    if ! [[ "$(findmnt --noheadings --output OPTIONS /nix/store)" =~ ro(,|$) ]]; then
        if [ -z "$container" ]; then
            mount --bind /nix/store /nix/store
        else
            mount --rbind /nix/store /nix/store
        fi
        mount -o remount,ro,bind /nix/store
    fi
fi


if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Use /etc/resolv.conf supplied by systemd-nspawn, if applicable.
    if [ -n "" ] && [ -e /etc/resolv.conf ]; then
        resolvconf -m 1000 -a host </etc/resolv.conf
    fi


    # Log the script output to /dev/kmsg or /run/log/stage-2-init.log.
    # Only at this point are all the necessary prerequisites ready for these commands.
    exec {logOutFd}>&1 {logErrFd}>&2
    if test -w /dev/kmsg; then
        exec > >(tee -i /proc/self/fd/"$logOutFd" | while read -r line; do
            if test -n "$line"; then
                echo "<7>stage-2-init: $line" > /dev/kmsg
            fi
        done) 2>&1
        exec > >(tee -i /run/log/stage-2-init.log) 2>&1
    fi
fi


# Required by the activation script
install -m 0755 -d /etc /etc/nixos
install -m 01777 -d /tmp


# Run the script that performs all configuration activation that does
# not have to be done at boot time.
echo "running activation script..."
$systemConfig/activate


# Record the boot configuration.
ln -sfn "$systemConfig" /run/booted-system


# Run any user-specified commands.
/nix/store/ny69lqq5dgw5xz6h5ply8cwzifcvplxx-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash /nix/store/b63lb8ssxjzdwdvrn39k73vavlk8kinj-local-cmds


# Ensure systemd doesn't try to populate /etc, by forcing its first-boot
# heuristic off. It doesn't matter what's in /etc/machine-id for this purpose,
# and systemd will immediately fill in the file when it starts, so just
# creating it is enough. This `: >>` pattern avoids forking and avoids changing
# the mtime if the file already exists.
: >> /etc/machine-id


# No need to restore the stdout/stderr streams we never redirected and
# especially no need to start systemd
if [ "${IN_NIXOS_SYSTEMD_STAGE1:-}" != true ]; then
    # Reset the logging file descriptors.
    exec 1>&$logOutFd 2>&$logErrFd
    exec {logOutFd}>&- {logErrFd}>&-


    # Start systemd in a clean environment.
    echo "starting systemd..."
    exec /run/current-system/systemd/lib/systemd/systemd "$@"
fi



# 再看看其中的 $systemConfig/activate 都干了些啥
# 能看到它就是继续生成与链接各种 Linux 运行必备的 FHS 文件树，以及各种必备的文件
# 比如 /bin/sh /home /root /etc /var 等等
› cat /nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37/activate
#!/nix/store/ny69lqq5dgw5xz6h5ply8cwzifcvplxx-bash-5.2-p15-riscv64-unknown-linux-gnu/bin/bash

systemConfig='/nix/store/a5gnycsy3cq4ix2k8624649zj8xqzkxc-nixos-system-nixos-23.05.20230624.3ef8b37'

export PATH=/empty
for i in /nix/store/4l7v9y3r2mp2sdhjxjl35yvjsxmrdl4h-coreutils-riscv64-unknown-linux-gnu-9.1 /nix/store/00k2kgxrxx8nrs9sqrajl43aabg58655-gnugrep-riscv64-unknown-linux-gnu-3.7 /nix/store/pjsjh36lkn6jqina5l30609d8ldyqw7g-findutils-riscv64-unknown-linux-gnu-4.9.0 /nix/store/n0wk98079d81zaa37ll4nnkh0gnnjp45-getent-glibc-riscv64-unknown-linux-gnu-2.37-8 /nix/store/j3vh88d4kkpgnjdpxhqibpjqa4x59pzy-glibc-riscv64-unknown-linux-gnu-2.37-8-bin /nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13 /nix/store/csi20f6aksz8fdcjb7sz9a860vjd4v9g-net-tools-riscv64-unknown-linux-gnu-2.10 /nix/store/c1xb4z38bvl29vbvc2la2957gv9sdy61-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin; do
    PATH=$PATH:$i/bin:$i/sbin
done

_status=0
trap "_status=1 _localstatus=\$?" ERR

# Ensure a consistent umask.
umask 0022

#### Activation script snippet specialfs:
_localstatus=0
specialMount() {
  local device="$1"
  local mountPoint="$2"
  local options="$3"
  local fsType="$4"

  if mountpoint -q "$mountPoint"; then
    local options="remount,$options"
  else
    mkdir -m 0755 -p "$mountPoint"
  fi
  mount -t "$fsType" -o "$options" "$device" "$mountPoint"
}
source /nix/store/z1b5brgask2dvsq2gjkk8vc9rv5r2c0y-mounts.sh


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "specialfs" "$_localstatus"
fi

#### Activation script snippet binfmt:
_localstatus=0
mkdir -p -m 0755 /run/binfmt



if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "binfmt" "$_localstatus"
fi

#### Activation script snippet stdio:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "stdio" "$_localstatus"
fi

#### Activation script snippet binsh:
_localstatus=0
# Create the required /bin/sh symlink; otherwise lots of things
# (notably the system() function) won't work.
mkdir -m 0755 -p /bin
ln -sfn "/nix/store/qs8dvkg2719slcc6rvv89whphg697cwm-bash-interactive-5.2-p15-riscv64-unknown-linux-gnu/bin/sh" /bin/.sh.tmp
mv /bin/.sh.tmp /bin/sh # atomically replace /bin/sh


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "binsh" "$_localstatus"
fi

#### Activation script snippet check-manual-docbook:
_localstatus=0
if [[ $(cat /nix/store/v3hlwi9fqqhgwsggd5p478rgmsqxfph5-options-used-docbook) = 1 ]]; then
  echo -e "\e[31;1mwarning\e[0m: This configuration contains option documentation in docbook." \
          "Support for docbook is deprecated and will be removed after NixOS 23.05." \
          "See nix-store --read-log /nix/store/0z3bpdvagjpmpl7m2i4ajzjyg6cipc8a-options.json.drv"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "check-manual-docbook" "$_localstatus"
fi

#### Activation script snippet domain:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "domain" "$_localstatus"
fi

#### Activation script snippet users:
_localstatus=0
install -m 0700 -d /root
install -m 0755 -d /home

/nix/store/r5wdgk9pwj7bvff208vsd9a821b9dw0c-perl-riscv64-unknown-linux-gnu-5.36.0-env/bin/perl \
-w /nix/store/jb6kmxd6ixbcb8s338ah2pdz26n0bbz4-update-users-groups.pl /nix/store/yjjxriwk6s7k14hrkd4mkmixmj1vskv5-users-groups.json


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "users" "$_localstatus"
fi

#### Activation script snippet groups:
_localstatus=0


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "groups" "$_localstatus"
fi

#### Activation script snippet etc:
_localstatus=0
# Set up the statically computed bits of /etc.
echo "setting up /etc..."
/nix/store/h1hh2x1zj7h7ih36jy6482x01976cyhd-perl-riscv64-unknown-linux-gnu-5.36.0-env/bin/perl /nix/store/rg5rf512szdxmnj9qal3wfdnpfsx38qi-setup-etc.pl /nix/store/b154qqwp6pybryjrdn9yfcvckipn5ybj-etc/etc


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "etc" "$_localstatus"
fi

#### Activation script snippet hashes:
_localstatus=0
users=()
while IFS=: read -r user hash tail; do
  if [[ "$hash" = "$"* && ! "$hash" =~ ^\$(y|gy|7|2b|2y|2a|6)\$ ]]; then
    users+=("$user")
  fi
done </etc/shadow

if (( "${#users[@]}" )); then
  echo "
WARNING: The following user accounts rely on password hashing algorithms
that have been removed. They need to be renewed as soon as possible, as
they do prevent their users from logging in."
  printf ' - %s\n' "${users[@]}"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "hashes" "$_localstatus"
fi

#### Activation script snippet hostname:
_localstatus=0
hostname "nixos"


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "hostname" "$_localstatus"
fi

#### Activation script snippet modprobe:
_localstatus=0
# Allow the kernel to find our wrapped modprobe (which searches
# in the right location in the Nix store for kernel modules).
# We need this when the kernel (or some module) auto-loads a
# module.
echo /nix/store/zafa80062xl2sybshivrz81qa38nas5y-kmod-riscv64-unknown-linux-gnu-30/bin/modprobe > /proc/sys/kernel/modprobe


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "modprobe" "$_localstatus"
fi

#### Activation script snippet nix:
_localstatus=0
install -m 0755 -d /nix/var/nix/{gcroots,profiles}/per-user

# Subscribe the root user to the NixOS channel by default.
if [ ! -e "/root/.nix-channels" ]; then
    echo "https://nixos.org/channels/nixos-23.05 nixos" > "/root/.nix-channels"
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "nix" "$_localstatus"
fi

#### Activation script snippet systemd-timesyncd-init-clock:
_localstatus=0
if ! [ -f /var/lib/systemd/timesync/clock ]; then
  test -d /var/lib/systemd/timesync || mkdir -p /var/lib/systemd/timesync
  touch /var/lib/systemd/timesync/clock
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "systemd-timesyncd-init-clock" "$_localstatus"
fi

#### Activation script snippet udevd:
_localstatus=0
# The deprecated hotplug uevent helper is not used anymore
if [ -e /proc/sys/kernel/hotplug ]; then
  echo "" > /proc/sys/kernel/hotplug
fi

# Allow the kernel to find our firmware.
if [ -e /sys/module/firmware_class/parameters/path ]; then
  echo -n "/nix/store/h4hgs3gig9l1x1d15v3cnlq11hg4p1r0-firmware/lib/firmware" > /sys/module/firmware_class/parameters/path
fi


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "udevd" "$_localstatus"
fi

#### Activation script snippet usrbinenv:
_localstatus=0
mkdir -m 0755 -p /usr/bin
ln -sfn /nix/store/4l7v9y3r2mp2sdhjxjl35yvjsxmrdl4h-coreutils-riscv64-unknown-linux-gnu-9.1/bin/env /usr/bin/.env.tmp
mv /usr/bin/.env.tmp /usr/bin/env # atomically replace /usr/bin/env


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "usrbinenv" "$_localstatus"
fi

#### Activation script snippet var:
_localstatus=0
# Various log/runtime directories.

mkdir -m 1777 -p /var/tmp

# Empty, immutable home directory of many system accounts.
mkdir -p /var/empty
# Make sure it's really empty
/nix/store/2fw7rr6yaaspkwwix771lcdwj02a3qxx-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/chattr -f -i /var/empty || true
find /var/empty -mindepth 1 -delete
chmod 0555 /var/empty
chown root:root /var/empty
/nix/store/2fw7rr6yaaspkwwix771lcdwj02a3qxx-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/chattr -f +i /var/empty || true


if (( _localstatus > 0 )); then
  printf "Activation script snippet '%s' failed (%s)\n" "var" "$_localstatus"
fi

#### Activation script snippet wrappers:
_localstatus=0
chmod 755 "/run/wrappers"

# We want to place the tmpdirs for the wrappers to the parent dir.
wrapperDir=$(mktemp --directory --tmpdir="/run/wrappers" wrappers.XXXXXXXXXX)
chmod a+rx "$wrapperDir"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/chsh"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/chsh" > "$wrapperDir/chsh.real"

# Prevent races
chmod 0000 "$wrapperDir/chsh"
chown root:root "$wrapperDir/chsh"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/chsh"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/dbus-daemon-launch-helper"
echo -n "/nix/store/3x1cpq5axfwygjssjg42clfvi085xjgp-dbus-riscv64-unknown-linux-gnu-1.14.6/libexec/dbus-daemon-launch-helper" > "$wrapperDir/dbus-daemon-launch-helper.real"

# Prevent races
chmod 0000 "$wrapperDir/dbus-daemon-launch-helper"
chown root:messagebus "$wrapperDir/dbus-daemon-launch-helper"

chmod "u+s,g-s,u+rx,g+rx,o-rx" "$wrapperDir/dbus-daemon-launch-helper"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/fusermount"
echo -n "/nix/store/770sky5x7dbcmzc2xahvws7pw250bj2s-fuse-riscv64-unknown-linux-gnu-2.9.9/bin/fusermount" > "$wrapperDir/fusermount.real"

# Prevent races
chmod 0000 "$wrapperDir/fusermount"
chown root:root "$wrapperDir/fusermount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/fusermount"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/fusermount3"
echo -n "/nix/store/gkxzqirzcf548w4421jlwhn1imp4979d-fuse-riscv64-unknown-linux-gnu-3.11.0/bin/fusermount3" > "$wrapperDir/fusermount3.real"

# Prevent races
chmod 0000 "$wrapperDir/fusermount3"
chown root:root "$wrapperDir/fusermount3"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/fusermount3"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/mount"
echo -n "/nix/store/c1xb4z38bvl29vbvc2la2957gv9sdy61-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/mount" > "$wrapperDir/mount.real"

# Prevent races
chmod 0000 "$wrapperDir/mount"
chown root:root "$wrapperDir/mount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/mount"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newgidmap"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/newgidmap" > "$wrapperDir/newgidmap.real"

# Prevent races
chmod 0000 "$wrapperDir/newgidmap"
chown root:root "$wrapperDir/newgidmap"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newgidmap"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newgrp"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/newgrp" > "$wrapperDir/newgrp.real"

# Prevent races
chmod 0000 "$wrapperDir/newgrp"
chown root:root "$wrapperDir/newgrp"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newgrp"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/newuidmap"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/newuidmap" > "$wrapperDir/newuidmap.real"

# Prevent races
chmod 0000 "$wrapperDir/newuidmap"
chown root:root "$wrapperDir/newuidmap"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/newuidmap"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/passwd"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/passwd" > "$wrapperDir/passwd.real"

# Prevent races
chmod 0000 "$wrapperDir/passwd"
chown root:root "$wrapperDir/passwd"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/passwd"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/ping"
echo -n "/nix/store/vwzakxlkma6lg0yd5ilx0cbj69whpm38-iputils-riscv64-unknown-linux-gnu-20221126/bin/ping" > "$wrapperDir/ping.real"

# Prevent races
chmod 0000 "$wrapperDir/ping"
chown root:root "$wrapperDir/ping"

# Set desired capabilities on the file plus cap_setpcap so
# the wrapper program can elevate the capabilities set on
# its file into the Ambient set.
/nix/store/cpnqm7m872fsqky7bjbqwy8llbbf33l9-libcap-riscv64-unknown-linux-gnu-2.68/bin/setcap "cap_setpcap,cap_net_raw+p" "$wrapperDir/ping"

# Set the executable bit
chmod u+rx,g+x,o+x "$wrapperDir/ping"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sg"
echo -n "/nix/store/wj90d7n8xfk163vwyg74fvnxh88fsp6h-shadow-riscv64-unknown-linux-gnu-4.13/bin/sg" > "$wrapperDir/sg.real"

# Prevent races
chmod 0000 "$wrapperDir/sg"
chown root:root "$wrapperDir/sg"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sg"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/su"
echo -n "/nix/store/jy1c86m85801g025pd6gs9ljhj301bsi-shadow-riscv64-unknown-linux-gnu-4.13-su/bin/su" > "$wrapperDir/su.real"

# Prevent races
chmod 0000 "$wrapperDir/su"
chown root:root "$wrapperDir/su"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/su"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sudo"
echo -n "/nix/store/54s80ssm7q2y1aqaavnrkvw7b4hkdm1g-sudo-riscv64-unknown-linux-gnu-1.9.13p3/bin/sudo" > "$wrapperDir/sudo.real"

# Prevent races
chmod 0000 "$wrapperDir/sudo"
chown root:root "$wrapperDir/sudo"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sudo"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/sudoedit"
echo -n "/nix/store/54s80ssm7q2y1aqaavnrkvw7b4hkdm1g-sudo-riscv64-unknown-linux-gnu-1.9.13p3/bin/sudoedit" > "$wrapperDir/sudoedit.real"

# Prevent races
chmod 0000 "$wrapperDir/sudoedit"
chown root:root "$wrapperDir/sudoedit"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/sudoedit"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/umount"
echo -n "/nix/store/c1xb4z38bvl29vbvc2la2957gv9sdy61-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/umount" > "$wrapperDir/umount.real"

# Prevent races
chmod 0000 "$wrapperDir/umount"
chown root:root "$wrapperDir/umount"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/umount"

cp /nix/store/ms8338dmzf45grswqknyghvzfszv6cby-security-wrapper-riscv64-unknown-linux-gnu/bin/security-wrapper "$wrapperDir/unix_chkpwd"
echo -n "/nix/store/cffy2kkpwgams7b94ixrslvf9nny88pv-linux-pam-riscv64-unknown-linux-gnu-1.5.2/bin/unix_chkpwd" > "$wrapperDir/unix_chkpwd.real"

# Prevent races
chmod 0000 "$wrapperDir/unix_chkpwd"
chown root:root "$wrapperDir/unix_chkpwd"

chmod "u+s,g-s,u+rx,g+x,o+x" "$wrapperDir/unix_chkpwd"


if [ -L /run/wrappers/bin ]; then
  # Atomically replace the symlink
  # See https://axialcorps.com/2013/07/03/atomically-replacing-files-and-directories/
  old=$(readlink -f /run/wrappers/bin)
  if [ -e "/run/wrappers/bin-tmp" ]; then
    rm --force --recursive "/run/wrappers/bin-tmp"
  fi
  ln --symbolic --force --no-dereference "$wrapperDir" "/run/wrappers/bin-tmp"
  mv --no-target-directory "/run/wrappers/bin-tmp" "/run/wrappers/bin"
  rm --force --recursive "$old"


# Make this configuration the current configuration.
# The readlink is there to ensure that when $systemConfig = /system
# (which is a symlink to the store), /run/current-system is still
# used as a garbage collection root.
ln -sfn "$(readlink -f "$systemConfig")" /run/current-system

# Prevent the current configuration from being garbage-collected.
mkdir -p /nix/var/nix/gcroots
ln -sfn /run/current-system /nix/var/nix/gcroots/current-system

exit $_status
```


## 实际启动日志

使用 USB 转串口工具，连接到开发板的 UART0 串口，就能看到开发板的启动日志。
一个正常的启动流程日志如下所示：

```
Welcome to minicom 2.8
brom_ver 8
[APP][E] protocol_connect failed, exit.
OpenSBI v0.9
   ____                    _____ ____ _____
  / __ \                  / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|____/_____|
        | |
        |_|

Platform Name             : T-HEAD Light Lichee Pi 4A configuration for 8GB DDR board
Platform Features         : mfdeleg
Platform HART Count       : 4
Platform IPI Device       : clint
Platform Timer Device     : clint
Platform Console Device   : uart8250
Platform HSM Device       : ---
Platform SysReset Device  : thead_reset
Firmware Base             : 0x0
Firmware Size             : 132 KB
Runtime SBI Version       : 0.3

Domain0 Name              : root
Domain0 Boot HART         : 0
Domain0 HARTs             : 0*,1*,2*,3*
Domain0 Region00          : 0x000000ffdc000000-0x000000ffdc00ffff (I)
Domain0 Region01          : 0x0000000000000000-0x000000000003ffff ()
Domain0 Region02          : 0x0000000000000000-0xffffffffffffffff (R,W,X)
Domain0 Next Address      : 0x0000000000200000
Domain0 Next Arg1         : 0x0000000001f00000
Domain0 Next Mode         : S-mode
Domain0 SysReset          : yes

Boot HART ID              : 0
Boot HART Domain          : root
Boot HART ISA             : rv64imafdcvsux
Boot HART Features        : scounteren,mcounteren,time
Boot HART PMP Count       : 0
Boot HART PMP Granularity : 0
Boot HART PMP Address Bits: 0
Boot HART MHPM Count      : 16
Boot HART MHPM Count      : 16
Boot HART MIDELEG         : 0x0000000000000222
Boot HART MEDELEG         : 0x000000000000b109
[    0.000000] Linux version 5.10.113 (nixbld@localhost) (riscv64-unknown-linux-gnu-gcc (GCC) 13.1.0, GN0
[    0.000000] OF: fdt: Ignoring memory range 0x0 - 0x200000
[    0.000000] earlycon: uart0 at MMIO32 0x000000ffe7014000 (options '115200n8')
[    0.000000] printk: bootconsole [uart0] enabled
[    2.292495] (NULL device *): failed to find vdmabuf_reserved_memory node
[    2.453953] spi-nor spi0.0: unrecognized JEDEC id bytes: ff ff ff ff ff ff
[    2.460971] dw_spi_mmio ffe700c000.spi: cs1 >= max 1
[    2.466001] spi_master spi0: spi_device register error /soc/spi@ffe700c000/spidev@1
[    2.497453] sdhci-dwcmshc ffe70a0000.sd: can't request region for resource [mem 0xffef014064-0xffef01]
[    2.509014] misc vhost-vdmabuf: failed to find vdmabuf_reserved_memory node
[    3.386036] debugfs: File 'SDOUT' in directory 'dapm' already present!
[    3.392692] debugfs: File 'Playback' in directory 'dapm' already present!
[    3.399524] debugfs: File 'Capture' in directory 'dapm' already present!
[    3.406262] debugfs: File 'Playback' in directory 'dapm' already present!
[    3.413067] debugfs: File 'Capture' in directory 'dapm' already present!
[    3.425466] aw87519_pa 5-0058: aw87519_parse_dt: no reset gpio provided failed
[    3.432752] aw87519_pa 5-0058: aw87519_i2c_probe: failed to parse device tree node

<<< NixOS Stage 1 >>>

running udev...
Starting systemd-udevd version 253.6
kbd_mode: KDSKBMODE: Inappropriate ioctl for device
Gstarting device mapper and LVM...
checking /dev/disk/by-label/NIXOS_SD...
fsck (busybox 1.36.1)
[fsck.ext4 (1) -- /mnt-root/] fsck.ext4 -a /dev/disk/by-label/NIXOS_SD
NIXOS_SD: recovering journal
NIXOS_SD: clean, 148061/248000 files, 818082/984159 blocks
mounting /dev/disk/by-label/NIXOS_SD on /...

<<< NixOS Stage 2 >>>

running activation script...
setting up /etc...
++ /nix/store/2w8nachmhqvbjswrrsdia5cx1afxxx60-util-linux-riscv64-unknown-linux-gnu-2.38.1-bin/bin/findm/
+ rootPart=/dev/disk/by-label/NIXOS_SD
++ lsblk -npo PKNAME /dev/disk/by-label/NIXOS_SD
+ bootDevice=/dev/mmcblk1
++ lsblk -npo MAJ:MIN /dev/disk/by-label/NIXOS_SD
++ /nix/store/zag1z2yvsh2ccpsbgsda7xhv4sfha7mj-gawk-riscv64-unknown-linux-gnu-5.2.1/bin/awk -F: '{print '
+ partNum='26 '
+ echo ,+,
+ sfdisk -N26 --no-reread /dev/mmcblk1
GPT PMBR size mismatch (8332023 != 122894335) will be corrected by write.
The backup GPT table is not on the end of the device. This problem will be corrected by write.
warning: /dev/mmcblk1: partition 26 is not defined yet
Disk /dev/mmcblk1: 58.6 GiB, 62921900032 bytes, 122894336 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 58B10C85-BB4D-F94A-9194-82020FC9DC23

Old situation:

Device          Start     End Sectors  Size Type
/dev/mmcblk1p1  16384  425983  409600  200M Microsoft basic data
/dev/mmcblk1p2 425984 8331990 7906007  3.8G Linux filesystem

/dev/mmcblk1p26: Created a new partition 3 of type 'Linux filesystem' and of size 54.6 GiB.

New situation:
Disklabel type: gpt
Disk identifier: 58B10C85-BB4D-F94A-9194-82020FC9DC23

Device           Start       End   Sectors  Size Type
/dev/mmcblk1p1   16384    425983    409600  200M Microsoft basic data
/dev/mmcblk1p2  425984   8331990   7906007  3.8G Linux filesystem
/dev/mmcblk1p3 8333312 122892287 114558976 54.6G Linux filesystem

The partition table has been altered.
Calling ioctl() to re-read partition table.
Re-reading the partition table failed.: Device or resource busy
The kernel still uses the old table. The new table will be used at the next reboot or after you run part.
Syncing disks.
+ /nix/store/wm9ynqbkqi7gagggb4y6f4l454kkga32-parted-riscv64-unknown-linux-gnu-3.6/bin/partprobe
+ /nix/store/yln7ma9dldr3f2dva4l0iq275s4brxml-e2fsprogs-riscv64-unknown-linux-gnu-1.46.6-bin/bin/resize2D
resize2fs 1.46.6 (1-Feb-2023)
Filesystem at /dev/disk/by-label/NIXOS_SD is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/disk/by-label/NIXOS_SD is now 988250 (4k) blocks long.

+ /nix/store/f5w7dd1f195bxkashhr5x0a788nxrxvc-nix-riscv64-unknown-linux-gnu-2.13.3/bin/nix-store --load-b
+ touch /etc/NIXOS
+ /nix/store/f5w7dd1f195bxkashhr5x0a788nxrxvc-nix-riscv64-unknown-linux-gnu-2.13.3/bin/nix-env -p /nix/vm
+ rm -f /nix-path-registration
starting systemd...

Welcome to NixOS 23.05 (Stoat)!

[  OK  ] Created slice Slice /system/getty.
[  OK  ] Created slice Slice /system/modprobe.
[  OK  ] Created slice Slice /system/serial-getty.......
......
```




## RISC-V / ARM64 开发板的启动流程

{{<figure src="./current-riscv-boot-flow.webp" title="RISCV 开发版当前的引导流程" width="60%">}}

{{<figure src="./current-arm64-boot-flow.webp" title="ARM64 开发版当前的引导流程" width="60%">}}

### u-boot，u-boot-spl，u-boot-tpl 的关系

对于一般嵌入式而言只需要一个 u-boot 作为 bootloader 即可，但是在小内存，或者有 atf 的情况下还可以有 spl，tpl:

- spl：Secondary Program Loader，二级加载器
- tpl：Tertiary Program Loader，三级加载器

出现 spl 和 tpl 的原因最开始是因为系统 sram 太小，rom 无法在 ddr 未初始化的情况下一次性把所有代码从 flash，emmc，usb 等搬运到 sram 中执行，也或者是 flash 太小，无法完整放下整个 u-boot 来进行片上执行。所以 u-boot 又定义了 spl 和 tpl，spl 和 tpl 走 u-boot 完全相同的 boot 流程，不过在 spl 和 tpl 中大多数驱动和功能被去除了，根据需要只保留一部分 spl 和 tpl 需要的功能，通过 CONFIG_SPL_BUILD 和 CONFIG_TPL_BUILD 控制；一般只用 spl 就足够了，spl 完成 ddr 初始化，并完成一些外设驱动初始化，比如 usb，emmc，以此从其他外围设备加载 u-boot，但是如果对于小系统 spl 还是太大了，则可以继续加入 tpl，tpl 只做 ddr 等的特定初始化保证代码体积极小，以此再次从指定位置加载 spl，spl 再去加载 u-boot。

从目前来看，spl 可以取代上图中 bl2 的位置，或者 bl1，根据具体厂商实现来决定，有一些芯片厂商会将 spl 固化在 rom 中，使其具有从 emmc，usb 等设备加载 u-boot 或者其他固件的能力。

### OpenSBI

OpenSBI 是 System call type interface layer between Firmware runtime, M-Mode
to Operating system, S-Mode.

```mermaid
flowchart LR
    U["U-Boot SPL(M-Mode)"] --> O["OpenSBI(M-Mode)"] --> O2["U-Boot Proper(S-Mode)"]
    O2--> L["Linux Kernel(S-Mode)"] --> USER["User Space(U-Mode)"]
```

#### FW_DYNAMIC

- Pack the firmware with runtime accessible to the next level boot stage, fw_dynamic.bin
- Can be packable in U-Boot SPL, Coreboot

首先编译出 `fw_dynamib.bin`：

```bash
CROSS_COMPILE=riscv64-buildroot-linux-gnu- make PLATFORM=sifive/fu540
```

然后基于该文件构建 u-boot-spl.bin:

```bash
CROSS_COMPILE=riscv64-buildroot-linux-gnu- make sfive_fu540_spl_defconfig

export OPENSBI=</path/to/fw_dynamic.bin>
CROSS_COMPILE=riscv64-buildroot-linux-gnu- make
```

### vmlinux vmlinuz Image zImage 等都有何关系

> https://www.baeldung.com/linux/kernel-images

按生成顺序依次介绍如下：

- vmlinux：Linux 内核编译出来的原始的内核文件，elf 格式，未做压缩处理。
  - 该映像可用于定位内核问题，但不能直接引导 Linux 系统启动。
- Image：Linux 内核编译时，使用 objcopy 处理 vmlinux 后生成的二进制内核映像。
  - 该映像未压缩，可直接引导 Linux 系统启动。
- zImage：一种 Linux 内核映像，专为 X86 架构的系统设计，它使用 LZ77 压缩算法。
- bzImage: 一种可启动的二进制压缩内核映像
  - `bz` 是 big zipped 的缩写。通常使用 gzip 压缩算法，但是也可以用别的算法。
  - 包含 boot loader header + gzip 压缩后的 vmlinux 映像
- vmlinuz: 它跟 bzImage 一样都是指压缩后的内核映像，两个名称基本可以互换。

### initrd 与 initramfs

> https://www.zhihu.com/question/22045825

#### initrd

在早期的 linux 系统中，一般只有硬盘或者软盘被用来作为 linux 根文件系统的存储设备，因此也就很容易把这些设备的驱动程序集成到内核中。但是现在的嵌入式系统中可能将根文件系统保存到各种存储设备上，包括 scsi、sata，u-disk 等等。因此把这些设备的驱动代码全部编译到内核中显然就不是很方便。

为了解决这一矛盾，于是出现了 initrd，它的英文含义是 boot loader iniTIalized RAM disk，就是由 boot loader 初始化的内存盘。在 linux 内核启动前， boot loader 会将存储介质中的 initrd 文件加载到内存，内核启动时会在访问真正的文件系统前先访问该内存中的 initrd 文件系统。
在 boot loader 配置了 initrd 在这情况下，内核启动被分成了两个阶段，第一阶段内核会解压缩 initrd 文件，将解压后的 initrd 挂载为根目录；第二阶段才执行根目录中的 `/init` 脚本（cpio 格式的 initr 为 `/init`, 而 image 格式的 initrd<也称老式块设备的 initrd 或传统的文件镜像格式的 initrd>为 `/initrc`）。

`/init` 通常是一个 bash 脚本，我们可以通过它加载 realfs（真实文件系统）的驱动程序，并挂载好 /dev /proc /sys 等文件夹，接着就可以 mount 并 chroot 到真正的根目录，完成整个 rootfs 的加载。

#### initramfs

在 linux2.5 中出现了 initramfs，它的作用和 initrd 类似，只是和内核编译成一个文件(该 initramfs 是经过 gzip 压缩后的 cpio 格式的数据文件)，该 cpio 格式的文件被链接进了内核中特殊的数据段.init.ramfs 上，其中全局变量**initramfs_start 和**initramfs_end 分别指向这个数据段的起始地址和结束地址。内核启动时会对.init.ramfs 段中的数据进行解压，然后使用它作为临时的根文件系统。

### 设备树

TODO

### Linux 的不同引导方式

1. extlinux
2. u-boot

TODO



## 参考

- [LicheePi 4A —— 这个小板有点意思（第一部分） - HougeLangley](https://litterhougelangley.club/blog/2023/05/27/licheepi-4a-%e8%bf%99%e4%b8%aa%e5%b0%8f%e6%9d%bf%e6%9c%89%e7%82%b9%e6%84%8f%e6%80%9d%ef%bc%88%e7%ac%ac%e4%b8%80%e9%83%a8%e5%88%86%ef%bc%89/)
- [An Introduction to RISC-V Boot flow: Overview, Blob vs Blobfree standards](https://crvf2019.github.io/pdf/43.pdf)
- [ARMv8 架构 u-boot 启动流程详细分析(一)](https://bbs.huaweicloud.com/blogs/363735)
- [聊聊 SOC 启动（五） uboot 启动流程一](https://zhuanlan.zhihu.com/p/520060653)
- [基于 qemu-riscv 从 0 开始构建嵌入式 linux 系统 ch5-1. 什么是多级 BootLoader 与 opensbi(上)¶](https://quard-star-tutorial.readthedocs.io/zh_CN/latest/ch5-1.html)
- [Linux系统构成简单介绍 - 野火 嵌入式Linux镜像构建与部署](https://doc.embedfire.com/linux/rk356x/build_and_deploy/zh/latest/building_image/image_composition/image_composition.html)

