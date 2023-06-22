---
title: "NixOS 与 Nix Flakes 打包与开发"
date: 2023-06-22T03:10:28+08:00
lastmod: 2023-06-22T03:10:00+08:00
draft: true

resources:
  - name: "featured-image"
    src: "ryan4yin-nix-config.webp"

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

这篇文章主要介绍 NixOS 与 Flakes 的一些实用技巧，以及一些常用的工具。

## other useful tools

- https://github.com/nixpak/nixpak
- https://github.com/maralorn/nix-output-monitor

## NixOS generator

TODO

## 通过 dev-templates 创建开发环境

[numtide/devshell](https://github.com/numtide/devshell) seems to be a personal project, and not documented well.

[cachix/devenv](https://github.com/cachix/devenv) has rich documentation, and the project is very active, so I decided to give it a try.

[dev-templates](https://github.com/the-nix-way/dev-templates) a collection of Nix templates for development environments, may be more intuitive than cachix/devenv for experienced Nix users.

看了一圈三个项目，感觉 dev-templates 最符合我的需求，另外两个项目感觉不到啥优势。

分析下 lib.mkShell 的实现，首先 `nix repl -f '<nixpkgs>'` 然后输入 `:e pkgs.mkShell`:

TODO

## 打包自己的软件

### 1. stdenv 构建介绍

> https://github.com/NixOS/nixpkgs/tree/nixos-unstable/doc/stdenv

TODO

### 2. many language specific frameworks

> https://github.com/NixOS/nixpkgs/tree/nixos-unstable/doc/languages-frameworks

TODO

## 分布式构建

分布式构建可以通过多台机器来分担本地的编译压力，加快构建速度。
常用于 RISC-V 或 ARM64 架构的构建，因为本来 cache.nixos.org 中对 ARM64 的缓存就很少，而 RISC-V 更是几乎没有任何官方缓存，导致需要大量本地编译。
另外嵌入式场景下往往对底层内核、驱动等有定制需求，这也会导致经常需要在本地执行大量编译动作。

- https://github.com/NixOS/nix/blob/713836112/tests/nixos/remote-builds.nix#L46
- https://sgt.hootr.club/molten-matter/nix-distributed-builds/

多机远程构建是以 Derivation 为单位的，在构建的 packages 较多时可以轻松将所有主机的 CPU 都用上，非常爽。

其他发行版也可以用 distcc/ccache 来构建，不过我没试过，不清楚体验如何。

TODO
