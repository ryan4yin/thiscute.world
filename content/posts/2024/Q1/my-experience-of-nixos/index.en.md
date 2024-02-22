---
title: "OS as Code - My Experience of NixOS"
subtitle: ""
description: ""
date: 2024-02-21T16:26:21+08:00
lastmod: 2024-02-21T16:26:21+08:00
draft: false

resources:
  - name: "featured-image"
    src: "nixos-and-flakes-book-202402.webp"

tags: ["NixOS", "Nix", "Flakes", "Linux", "DevOps"]
categories: ["tech"]
series: ["NixOS & Nix Flakes"]
series_weight: 3
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


It's February 2024, exactly 10 months since I started using NixOS. The beginner notes I wrote initially have received a lot of positive feedback and some sponsorships, becoming one of the most popular entry-level tutorials in the entire community. Since I created a dedicated GitHub repository and a separate documentation site for it in June 2023, it has garnered 1189 stars, and besides me, 37 other readers have submitted PRs:

- [NixOS & Flakes - An Unofficial Beginner's Guide](https://nixos-and-flakes.thiscute.world/zh/)

{{<figure src="./nixos-and-flakes-book-202402.webp" title="NixOS & Flakes Book" width="80%">}}

From the perspective of a seasoned user who has been deeply using NixOS as a primary desktop system for nearly 10 months, I'd like to share my insights from a different angle here.

Note that this article is not a NixOS beginner's tutorial; if you're looking for one, please follow the link provided above.

## Nixpkgs Has Too Few Packages?

Firstly, let's clarify that NixOS has a vast number of packages. In terms of size, Nixpkgs is on par with Arch AUR. [Repository statistics](https://link.zhihu.com/?target=https%3A//repology.org/repositories/statistics/total) show that:

![Repository statistics](./repository-statistics.webp)

Although the total number of packages in Nixpkgs may include some "fake" packages due to the inclusion of npm packages and others, even excluding these, the number of packages should be roughly similar to that of AUR.

Moreover, because Nixpkgs is the official package repository and uses a Monorepo and PR Review system, the overall package quality is undoubtedly better than that of AUR. As you can see from the screenshot, Nixpkgs packages are generally more up-to-date and have fewer vulnerabilities than AUR packages.

This is also where NixOS differs from Arch: Arch's official package repository has strict inclusion criteria, while its AUR ecosystem is quite vibrant. Anyone can upload content to AUR, although there is a voting mechanism that serves as a certain level of review, the criteria are quite loose.

NixOS, on the other hand, is quite different. Its official package repository, Nixpkgs, is quite open to new packages, and it's relatively easier to add a package or feature to Nixpkgs compared to other distributions. This is one of the direct reasons why Nixpkgs' size is close to AUR (GitHub shows that Nixpkgs has over 5000 historical contributors, which is quite astonishing). NixOS actually also has a NUR (Nix User Repository) similar to AUR, but because of Nixpkgs' lax attitude, NUR doesn't have much content.

For example, you can directly download and use QQ from the Nixpkgs official package repository, while on Arch, you would need to use AUR or archlinux-cn.

This can be seen as having its own advantages. NixOS is criticized for having too few packages mainly because it does not follow the FHS standard, which means that most Linux programs downloaded online cannot run directly on NixOS. Of course, there are solutions to this. I suggest first checking if there is already a package for the desired software in Nixpkgs, and if so, use it directly. If not, try some community solutions or package it yourself.

Packaging programs is inevitable when using NixOS, as even though Nixpkgs already has a vast number of packages, it's impossible for it to match all your needs 100% of the time. There will always be packages you want to use but can't find in Nixpkgs or NUR, and on NixOS, you often have to write a packaging script for your packages to run normally on the system.

OK, enough chatter. Let's move on to the main topic.

Firstly, NixOS is much more complex than traditional distributions and has a lot of historical issues.

For example, the official documentation is so bad that it forced me, a beginner at NixOS, to write my own beginner's notes while I was learning. After translating my notes into poor English and posting them on reddit ([NixOS & Nix Flakes - A Guide for Beginners](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/)), they received a lot of positive feedback from foreigners (after so much continuous iteration, it has now become one of the most popular beginner tutorials in the community), which also shows how bad the official documentation is.

## Is NixOS Worth Learning?

**Is NixOS worth learning, or is the return on investment high enough? In my view, it all comes down to scale.**

**Here, "scale" refers to three aspects:**

1. **The scale of your custom content for the Linux system:** The more customization you do, the harder it is to migrate to a new version.
2. **The frequency of system updates:** The more frequently you update your system, the higher the risk of encountering issues.
3. **The number of your Linux machines:** The more machines you have, the more you benefit from a system that can easily replicate the same environment.

Let me share my experience with traditional distributions like Arch and Ubuntu, and why I chose NixOS, and the changes it brought me, from a personal perspective.

For example, when I used Deepin Ubuntu in the past, I didn't customize the system much for fear of causing problems and not being able to fix them easily. Moreover, any customizations I made were black boxes and not migratable. A month later, I would have forgotten everything, and the system would have become increasingly chaotic and opaque over time.

If you're using a rolling release distribution like Arch, the issues you encounter are generally minor. But with Ubuntu or Deepin, it's rare for in-place upgrades to go smoothly, which means I had to re-customize everything on the new Ubuntu version. Worse yet, I might have forgotten what I did in the past, meaning I had to spend more time researching my system environment and how everything was installed and configured. This repetitive labor is very painful.

Clearly, the more complex and customized the system, the harder it is to migrate to a new version.

This is why rolling release distributions like Arch, Gentoo, and Fedora are so popular among Linux enthusiasts. Linux users who like to customize their systems mostly use these types of distributions.

Can Arch or Fedora solve the problem completely? Obviously not.

Firstly, they have a higher update frequency, which means you're more likely to break something on your system. Of course, this is a small problem, as most Linux users now use btrfs or zfs file system snapshots for rollback in case of issues.

Their fundamental problem, however, is:

1. Your Arch system environment, file system snapshots, or virtual machine snapshots are still black boxes. They will become increasingly chaotic with continuous use and do not include the "knowledge" of how to build this environment from scratch, making them **unexplainable.**
   - In my work, I've seen some "ancestral virtual machine snapshots" or "ancestral cloud server snapshots" where no one knows how the environment was set up, and each new person who takes over can only continue to pile on buffs, then pass the time bomb to the next person. This is like the game where people take turns adding water to a cup, and whoever adds water when it overflows is out of luck.
1. Arch essentially requires you to follow its updates continuously, which means you must continuously maintain it.
   - If you let a machine run stable for a year and a half and then decide to update it, the risk of problems is quite high. If you then decide to set up a new Arch machine and restore the old environment, you're back to the same problem—you have to figure out how to restore your customization process from the old environment, which is also not a pleasant task.
1. Snapshots are strongly associated with the current hardware environment and are easily affected by various strange issues when used directly on different hardware machines, making them **unmovable.**
1. Snapshots are large binary files, making them expensive to back up and share.

Docker can solve some of these problems.

Firstly, Docker container images can be fully described by Dockerfiles, meaning they are **explainable**, and the same environment can be replicated in different environments. This indicates that they are **movable.**

For server environments, running all applications in containers, with the host machine only responsible for running containers, greatly reduces the cost of system maintenance by only requiring you to maintain the most basic system environment and some Dockerfiles and yaml files and is thus the preferred choice for DevOps.

However, Docker container technology is designed for providing a consistent runtime environment for applications and is not suitable for virtual machine and desktop environments (of course, you can use it in these scenarios if you wish, but it would be quite complicated).
Additionally, Dockerfiles still rely on various scripts and commands you write to build the image, which you need to maintain, and the reproducibility of the results depends on your own skills.

If you choose a minimalist strategy—customizing as little as possible on any desktop system or virtual machine environment and using default settings wherever possible—this was me before switching to NixOS.

To reduce the difficulty of system maintenance, I barely made any significant changes to the systems I used, such as Deepin, Manjaro, EndeavourOS, etc. As an SRE/DevOps, I had already encountered enough environmental problem pitfalls in my work and was tired of writing various installation scripts and Ansible configurations, so I had no desire to deal with these issues in my spare time.

However, if you are a geek who likes to customize and delve into the details of the system, as you make more and more customizations and the system becomes more complex, or if you have more and more Linux machines in your Homelab and cloud environment, you will definitely start to write various deployment flow documents, deployment scripts, or use some automation tools to help yourself complete some tedious work at some point.

Documentation aside, it's obvious that writing automation scripts or choosing automation tools will lead to increasingly complex configurations, and system updates often break some of these functions, requiring you to fix them manually. Moreover, they are highly dependent on your current system environment, so when you confidently use them to deploy environments on new machines, you are very likely to encounter various inconsistent environment-related errors that need to be resolved manually. Another point is that the scripts you write are likely not to have carefully considered abstraction, modularization, error handling, and other aspects, which will also make it increasingly painful to maintain them as the scale expands.

Then you discover NixOS, and you realize that its declarative configuration essentially wraps a pile of bash scripts and provides users with a set of clean and simple APIs. The actual work it does is exactly the same as the pile of scripts I've been writing for years.

You try it out and find that the system customization scripts in NixOS are all stored in a repository called Nixpkgs, maintained by thousands of people, with decades of accumulation, and with a very rich and relatively stable declarative abstraction, module system, type system, a large-scale CI system called Hydra specifically developed for this huge software package repository and NixOS system configuration, and a community operation mode that has formed to facilitate collaboration and updating this complex configuration for thousands of people.

You immediately start learning Nix and begin to rewrite the scripts you've maintained for N years into NixOS configurations.

The more you write, the more satisfied you become, as the reduced configuration is much easier to maintain.

A large part of the functionality previously achieved with various scripts and tools is now encapsulated in Nixpkgs, and you can enable it and pass a few key parameters to run it painlessly. The scripts in Nixpkgs have dedicated maintainers who update and fix any issues found by users, and any updates that haven't undergone CI and multiple stages of testing and validation, such as staging and unstable, won't enter the stable channel.

The you I mentioned earlier is none other than myself.

Now, when I think back to the days when I struggled with systemd to run a simple little tool, I can't help but shed tears... If only I had known about NixOS earlier...

## The Declarative Configuration of NixOS - OS as Code

People with some programming experience should know the importance of abstraction and modularization, as the complexity of a scenario increases, the benefits of abstraction and modularization also increase. The popularity of Terraform/Kubernetes, and even Spring Boot, reflects this. NixOS's declarative configuration is also like this, as it encapsulates the underlying implementation details and has a community responsible for updating and maintaining these lower-level encapsulations. This greatly reduces my cognitive load and frees up my productivity. Its reproducibility also alleviates my concerns about breaking the system.

On the other hand, NixOS's declarative configuration is also a kind of knowledge that describes how to build an OS from scratch, or a kind of source code that can build your NixOS system environment.

As long as this source code doesn't get lost, modifying it, reviewing it, sharing it with others, or borrowing some features you want from others' source code is very easy.

NixOS's configuration declares the complete state of the entire system, and you can easily copy the configuration of other NixOS users to get an identical environment. In contrast, copying the configurations of users of traditional distributions like Arch or Ubuntu is much more complicated, considering various version differences and environment differences, leading to a high level of uncertainty.

## The Learning Curve of NixOS

The entry barrier of NixOS is relatively high and is not suitable for beginners who have never touched Linux and programming. This is because its design philosophy is quite different from traditional Linux distributions. However, this is also its advantage, as once you cross that threshold, you will find a whole new world.

For example, **reading the source code of Nixpkgs and submitting PRs to add features or packages to fix bugs is a basic skill for NixOS users**, and **NixOS users who do this are quite common**.

This is both a deterrent that scares away new users and a ladder for Linux users who have chosen NixOS.

Imagine that most Arch users (like me in the past) might have used Arch for several years but didn't understand the underlying implementation details of Arch, nor did they package their own software. But with NixOS, diving into the source code becomes a norm, which also shows that understanding its implementation details is not difficult.

I will illustrate this point from two aspects.

First, Nix is a relatively simple language with very few syntax rules, **far simpler than general-purpose languages like Java or Python**. Therefore, engineers with some programming experience can master its syntax in just a few hours. With a bit more time, reading common Nix code shouldn't be too difficult.

Second, **NixOS's good declarative abstraction and modularization system divide the OS into many layers**, allowing users to focus only on the current layer of abstraction while still having the option to dive deeper into the next layer to more freely implement the desired functions (The right to choose, in fact, also gives users the opportunity to understand NixOS progressively.). For example, new users can normally use NixOS just by understanding the top-level abstraction. When you want to implement some customizations, digging one level deeper into the abstraction (such as customizing some operations directly through systemd's declarative parameters) is usually enough. If you are already a seasoned NixOS user and want to be more geeky, you can continue to delve deeper.

In summary, understanding the source code in Nixpkgs or using Nix to package a few programs is not difficult, and each NixOS user with some experience can also be a NixOS packager.

## What Sets NixOS Apart?

We've heard a lot about NixOS's strengths, and I've mentioned many of them above.

People outside the circle might mainly hear about its lack of dependency conflicts, the ability to roll back at any time, and its powerful reproducibility.

If you have actually used NixOS, you should also know about its other advantages:

1. System updates have similar atomic properties to database transactions, which means your system updates either succeed or fail (usually without intermediate states).

2. NixOS's declarative configuration actually implements OS as Code, making these configurations very easy to share. You can simply copy the code for the desired functionality from other NixOS users into your system configuration, and you'll get an identical environment. Beginner users can also easily learn a lot from others' configurations.

3. The declarative configuration provides users with highly convenient system customization capabilities, allowing them to quickly switch various components of the system by changing a few lines of configuration.

4. And so on.

These are all selling points of NixOS, some of which can now also be achieved by traditional distributions with innovations like Fedora Silverblue.

However, the system that can solve all these problems right now is only NixOS (and the more niche Guix, which also relies on the Nix package manager).

## Conclusion

From deciding to try NixOS to now, just 10 months later, the gains I've made on Linux far exceed the previous three years. I've tried a lot of new technologies and tools on my PC, and my Homelab has become much richer (I now have more than ten NixOS hosts). My understanding of the Linux system structure has also deepened. Just these few points are worth the price of admission.

In summary, NixOS is very special and powerful.

On the other hand, it also has a considerable amount of historical debt. For example, the documentation is a mess, not user-friendly, the Flakes feature has been in an experimental state since 2019, and Nix's simplicity leads to a large number of Bash scripts in Nixpkgs, and the implementation defects of the module system result in very vague error messages, and so on.

However, the community is developing rapidly, and the community is actively solving technical debts like documentation and Flakes. Moreover, the popularity of NixOS is also increasing (my beginner tutorial has also contributed to this), so I am quite optimistic about its future.

From deciding to dive into NixOS to now, in just 10 months, the harvest I have gained on Linux far exceeds that of the past three years. I have tried a lot of new technologies and tools on my PC, and my Homelab has become much richer (I now have more than ten NixOS hosts). My understanding of the Linux system structure has also deepened. Just these few points are enough to justify my choice.

In summary, NixOS is very special and powerful. On the other hand, it also has a considerable amount of historical debt. For example, the documentation is a mess, not user-friendly, the Flakes feature has been in an experimental state since 2019, and Nix's simplicity leads to a large number of Bash scripts in Nixpkgs, and the implementation defects of the module system result in very vague error messages, and so on.

However, the community is developing rapidly, and the community is actively solving technical debts like documentation and Flakes. Moreover, the popularity of NixOS is also increasing (my beginner tutorial has also contributed to this), so I am quite optimistic about its future.
