---
title: "Why do I explore these niche technologies?"
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

I have dabbled with many niche technologies, and this year, the main ones I explored are NixOS, window manager i3/hyprland, and Neovim. NixOS, in particular, took me to a whole new level - I even created an open-source bilingual book [nixos-and-flakes-book](https://github.com/ryan4yin/nixos-and-flakes-book) to help beginners get started. Additionally, I worked on several NixOS-related open-source projects like [nix-darwin-kickstarter](https://github.com/ryan4yin/nix-darwin-kickstarter) and [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config), which all received positive feedback.

Based on my experiences with these niche technologies and the frequent questions I receive (e.g., why did I choose [NixOS](nixos.org/) / [Neovim](https://github.com/Neovim/Neovim) / [Flypy Chinese Input Method](https://flypy.com/)? What are their advantages? Can they really improve productivity?), I would like to briefly share my thoughts on them.

## What are niche technologies?

"Niche" refers to being different from the mainstream. Niche technologies are those with a relatively smaller user base within their respective domains.

According to this definition, I can list some niche technologies I have encountered in different fields:

| Domain         | Niche Technologies                              | Mainstream Technologies |
| -------------- | ----------------------------------------------- | ----------------------- |
| Text Editors   | Neovim, Emacs                                  | VSCode, Pycharm, IDEA   |
| Chinese Input Methods | Double Pinyin, Flypy, Wubi, Erbi, Zhengma, Lingxingsuying | Intelligent Pinyin |
| Linux OS       | NixOS, Gentoo, Arch Linux                      | Ubuntu, Fedora         |
| Window Managers| i3, hyprland                                   | KDE, GNOME             |

Most people tend to choose mainstream technologies in these fields due to their lower learning curve and ease of use. I was once part of the majority, but I gradually discovered the advantages of niche technologies, which led me to try and eventually transition to them.

## What are the characteristics of these niche technologies?

Niche technologies obviously have some advantages to attract a portion of users and make them choose these technologies over mainstream ones.

Based on my personal experience with these niche technologies, they share some notable common characteristics.

Firstly, they have a common downside: **higher learning curve and more time required to get familiar with them during the initial stages**.

This filters out the majority of users, and only those who enjoy tinkering and embracing challenges will be willing to explore these niche technologies.

For instance, with the Wubi input method, the learning curve is steep, requiring a significant amount of time to memorize the key arrangement and practice, leading to a challenging input experience in the early stages. To achieve the typing speed you had with an intelligent Pinyin method, you might need to practice Wubi for at least an hour a day consistently for a month (and perhaps even more).

Other shape-based input methods have similar characteristics. I opted for Flypy as a compromise; it has a lower learning curve compared to Wubi, and after mastering it, I can enjoy a similar input experience to Wubi.

Now, let's discuss their common advantages:

1. **High customizability**: Users can freely customize various functions according to their needs.
2. **Strong sense of control and excellent user experience**: The high level of customization gives users a sense of complete control while using these technologies, resulting in an excellent user experience.
3. **High user retention and active communities**: Users continuously explore, learn, and customize these technologies, creating a strong sense of belonging within the communities.

Due to these reasons, once users successfully familiarize themselves with a niche technology (e.g., shape-based input methods, Neovim/Emacs editors), it becomes challenging for them to revert to the previous mainstream solutions. They will find the previous solutions less convenient and enjoyable.

## Why do I explore these niche technologies?

I have explored various niche technologies, and curiosity is the primary reason. However, what makes me stick with them is their excellent user experience.

For instance, with Neovim editor and Hyprland window manager, once configured, they are aesthetically pleasing! Moreover, Neovim is exceptionally fast, even too fast! This speed may not impress those who haven't experienced VSCode / IDEA before, but once you get used to it, you'll find the speed truly impressive, just like the character Tu Hongyu exclaims in the Three-Body Problem (550W is too fast! This speed is too fast!).

Additionally, after mastering these technologies, I find them enjoyable to use. The keyboard-driven interaction provides a sense of control and smoothness similar to shape-based input methods (elegant, so elegant!).

{{<figure src="./hyprland_2023-07-29_1.webp" title="My NixOS + Hyprland Desktop" width="85%">}}
{{<figure src="./hyprland_2023-07-29_2.webp" title="My Neovim Editor" width="85%">}}

Similarly, my love for NixOS is based on similar reasons. NixOS with its declarative, reproducible (consistent runtime environment), OS as Code features aligns perfectly with what an operations enthusiast like me desires. I couldn't wait to use it and even wanted to improve it promptly to make it suitable for more scenarios.

> A few days ago, I saw a comment from a foreign netizen on 4chan (although the language was a bit extreme, I still somewhat agreed...):
> Completely and utterly unacceptable. Imagine having a tool that can't even properly undo an operation and then relying on it to manage an operating system. `apt`, `pip`, `pm`, `rpm`, `pacman`, whatever are all a mad fucking joke.

## Can niche tools or technologies improve productivity?

Many people claim that niche tools like Neovim editor, i3 window manager, and shape-based input methods can boost productivity, but I believe it is a misconception. In fact, many of these tools or technologies can be time-consuming distractions, driven by one's interests to continuously explore their boundaries and adjust configurations to better suit individual needs. During the initial phase, the time invested in these endeavors often outweighs the saved time from increased productivity.

So, ultimately, trying to use these technologies to significantly boost productivity is not realistic. They can improve your efficiency, but to a limited extent, unless your typing speed is the limiting factor in your productivity, emmm...

> Of course, there are some special scenarios where shape-based input methods like Wubi can indeed significantly improve input efficiency, especially when dealing with rare characters.

Or some may argue that once you become completely proficient, vim/emacs makes it easier to enter a state of flow? That is also difficult to say.

## So, what are the benefits of tinkering with these things?

If we look at it from a purely pragmatic perspective, there may not be many benefits; it's like playing games, just spending leisure time.

{{<figure src="./useless-work.jpg" title="Why do you always delve into these things that are useless for the business? (teasing tone)" width="35%">}}

However, compared to doing something boring for leisure, there are some useful takeaways. For instance, when I encounter a bug in AstroNvim

, I provide a PR to the upstream repository. When I find that NixOS documentation is inadequate, I write my own documentation and share it. If I notice that NixOS lacks support for a specific development board I have, I might try to port it. And if I find that a certain tool lacks a feature I want, I might just write one myself.

The experiences gained, open-source projects created, PRs left in upstream repositories, and the appreciation received in the community all feel valuable. It may not necessarily have business value, but it's fun, and you get to make friends, help others, and leave your mark in the open-source community - isn't that interesting?

Linus, when he first created Linux, did it [just for fun](https://www.goodreads.com/book/show/160171.Just_for_Fun).

