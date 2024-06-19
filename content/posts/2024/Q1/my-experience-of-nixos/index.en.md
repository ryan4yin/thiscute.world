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
  enable: true
license: ""

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

It's February 2024, exactly 10 months since I started using NixOS. The beginner notes I
wrote initially have received a lot of positive feedback and some sponsorships, becoming
one of the most popular entry-level tutorials in the entire community. Since I created a
dedicated GitHub repository and a separate documentation site for it in June 2023, it has
garnered 1189 stars, and besides me, 37 other readers have submitted PRs:

- [NixOS & Flakes - An Unofficial Beginner's Guide](https://nixos-and-flakes.thiscute.world/zh/)

{{<figure src="./nixos-and-flakes-book-202402.webp" title="NixOS & Flakes Book" width="80%">}}

From the perspective of a seasoned user who has been deeply using NixOS as a primary
desktop system for nearly 10 months, I'd like to share my insights from a different angle
here.

Note that this article is not a NixOS beginner's tutorial; if you're looking for one,
please follow the link provided above.

## Nixpkgs Has Too Few Packages?

Some people(in China) say that NixOS has too few packages, and this is one of the reasons
they don't use it. Is this true?

To clarify, NixOS boasts a substantial number of packages. The
[Repository statistics](https://link.zhihu.com/?target=https%3A//repology.org/repositories/statistics/total)
illustrate this as follows:

![Repository statistics](./repository-statistics.webp)

The count of packages in Nixpkgs is indeed inflated by the inclusion of many programming
language libraries — it seems that quite a few Haskell developers use Nix as their
language package manager. For instance, there are
[Haskell Packages(18000+)](https://search.nixos.org/packages?channel=unstable&query=haskell),
[R Packages(27000+)](https://search.nixos.org/packages?channel=unstable&query=rpackages),
and
[Emacs Packages(6000+)](https://search.nixos.org/packages?channel=unstable&query=emacspackages).
However, even after subtracting these, Nixpkgs still has over 40000 packages, which,
although less than AUR, is hardly a number that corresponds to the description of "too few
packages."

The package repository is also a point of differentiation between NixOS and Arch. Arch's
official repository has stringent inclusion criteria, while the AUR ecosystem is quite
vibrant. The AUR allows anyone to upload content, and although a voting mechanism serves
as a form of review, it feels rather lenient.

NixOS takes a different approach. Its official package repository, Nixpkgs, is very
receptive to new packages. Submitting a Pull Request to add a package or feature to
Nixpkgs is significantly simpler compared to other distributions, which is a key reason
for the large number of packages in Nixpkgs (GitHub shows that Nixpkgs has over 5000
contributors, an impressive figure).

The update process for the Nixpkgs repository is also more rigorous than that of AUR. PRs
generally need to pass a series of GitHub Actions, Maintainer's Review, and
[Ofborg](https://github.com/NixOS/ofborg) check and automatic build tests before being
merged. Nixpkgs encourages maintainers to add tests for their packages (the `doCheck` flag
is set to `true` by default), all of which contribute to the overall quality of the
packages.

NixOS also has a counterpart to AUR, the NUR (Nix User Repository), but due to the
permissive nature of Nixpkgs, NUR is not as populated.

For example, you can directly download and use QQ(an IM App popular in China) from the
Nixpkgs official package repository, while on Arch, you would need to use AUR or
archlinux-cn.

This can be seen as having its own advantages. NixOS is criticized for having too few
packages mainly because it does not follow the FHS standard, which means that most Linux
programs downloaded online cannot run directly on NixOS. Of course, there are solutions to
this. I suggest first checking if there is already a package for the desired software in
Nixpkgs, and if so, use it directly. If not, try some community solutions or package it
yourself.

Packaging programs is inevitable when using NixOS, as even though Nixpkgs already has a
vast number of packages, it's impossible for it to match all your needs 100% of the time.
There will always be packages you want to use but can't find in Nixpkgs or NUR, and on
NixOS, you often have to write a packaging script for your packages to run normally on the
system.

OK, enough chatter. Let's move on to the main topic.

Firstly, NixOS is much more complex than traditional distributions and has a lot of
historical issues.

For example, the official documentation is so bad that it forced me, a beginner at NixOS,
to write my own beginner's notes while I was learning. After translating my notes into
poor English and posting them on reddit
([NixOS & Nix Flakes - A Guide for Beginners](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/)),
they received a lot of positive feedback from foreigners (after so much continuous
iteration, it has now become one of the most popular beginner tutorials in the community),
which also shows how bad the official documentation is.

## Is NixOS Worth Learning?

**Is NixOS worth learning, or is the return on investment high enough? In my view, it all
comes down to scale.**

**Here, "scale" refers to three aspects:**

1. **The scale of your custom content for the Linux system:** The more customization you
   do, the harder it is to migrate to a new version.
2. **The frequency of system updates:** The more frequently you update your system, the
   higher the risk of encountering issues.
3. **The number of your Linux machines:** The more machines you have, the more you benefit
   from a system that can easily replicate the same environment.

Let me share my experience with traditional distributions like Arch and Ubuntu, and why I
chose NixOS, and the changes it brought me, from a personal perspective.

For example, when I used Deepin, Ubuntu and other traditional distros in the past, I
didn't customize the system much for fear of causing problems and not being able to fix
them easily. Moreover, any customizations I made were black boxes and not migratable. A
month later, I would have forgotten everything, and the system would have become
increasingly chaotic and opaque over time.

If you're using a rolling release distribution like Arch, the issues you encounter are
generally minor. But with Ubuntu or Deepin, it's rare for in-place upgrades to go
smoothly, which means I had to re-customize everything on the new Ubuntu version. Worse
yet, I might have forgotten what I did in the past, meaning I had to spend more time
researching my system environment and how everything was installed and configured. This
repetitive labor is very painful.

Clearly, the more complex and customized the system, the harder it is to migrate to a new
version.

I think this is why rolling release distributions like Arch, Gentoo, and Fedora are so
popular among Linux enthusiasts. Linux users who like to customize their systems mostly
use these types of distributions.

So can Arch or Fedora solve the problems completely? Obviously not.

Firstly, they have a higher update frequency, which means you're more likely to break
something on your system. Of course, this is a small problem, as most Linux users now use
btrfs or zfs file system snapshots for rollback in case of issues.

Their fundamental problems, however, is:

1. Your Arch system environment, file system snapshots, or virtual machine snapshots are
   still black boxes. They will become increasingly chaotic with continuous use and do not
   include the "knowledge" of how to build this environment from scratch, making them
   **unexplainable.**
   - In my work, I've seen some "**ancestral virtual machine snapshots**" or "**ancestral
     cloud server snapshots**" where no one knows how the environment was set up, and each
     new person who takes over can only continue to pile on buffs, then pass the time bomb
     to the next person. This is like the game where people take turns adding water to a
     cup, and whoever adds water when it overflows is out of luck.
1. Arch essentially requires you to follow its updates continuously, which means you must
   continuously maintain it.
   - If you let a machine run stable for a year and then decide to update it, the risk of
     problems is quite high. If you then decide to set up a new Arch machine and restore
     the old environment, you're back to the same problem — you have to figure out how to
     restore your customization process from the old environment, which is also not a
     pleasant task.
1. Snapshots are strongly associated with the current hardware environment and are easily
   affected by various strange issues when used directly on different hardware machines,
   making them **unmovable.**
1. Snapshots are large binary files, making them expensive to back up and share.

Docker can solve some of these problems. Firstly, Docker container images can be fully
described by Dockerfiles, meaning they are **explainable**, and the same environment can
be replicated in different environments. This indicates that they are **movable.**

For server environments, running all applications in containers, with the host machine
only responsible for running containers, greatly reduces the cost of system maintenance by
only requiring you to maintain the most basic system environment and some Dockerfiles and
yaml files and is thus the preferred choice for DevOps.

However, Docker container technology is designed for providing a consistent runtime
environment for applications and is not suitable for virtual machine and desktop
environments (of course, you can use it in these scenarios if you wish, but it would be
quite complicated). Additionally, Dockerfiles still rely on various scripts and commands
you write to build the image, which you need to maintain, and the reproducibility of the
results depends on your own skills.

If you choose a minimalist strategy - customizing as little as possible on any desktop
system or virtual machine environment and using default settings wherever possible, this
was me before switching to NixOS.

To reduce the difficulty of system maintenance, I barely made any significant changes to
the systems I used, such as Deepin, Manjaro, EndeavourOS, etc. As an SRE/DevOps, I had
already encountered enough environmental problem pitfalls in my work and was tired of
writing various installation scripts and Ansible configurations, so I had no desire to
deal with these issues in my spare time.

However, if you are a geek who likes to customize and delve into the details of the
system, as you make more and more customizations and the system becomes more complex, or
if you have more and more Linux machines in your Homelab and cloud environment, you will
definitely start to write various deployment flow documents, deployment scripts, or use
some automation tools to help yourself complete some tedious work at some point.

Documentation aside, it's obvious that writing automation scripts or choosing automation
tools will lead to increasingly complex configurations, and system updates often break
some of these functions, requiring you to fix them manually. Moreover, they are highly
dependent on your current system environment, so when you confidently use them to deploy
environments on new machines, you are very likely to encounter various inconsistent
environment-related errors that need to be resolved manually. Another point is that the
scripts you write are likely not to have carefully considered abstraction, modularization,
error handling, and other aspects, which will also make it increasingly painful to
maintain them as the scale expands.

Then you discover NixOS, and you realize that its declarative configuration essentially
wraps a pile of bash scripts and provides users with a set of clean and simple APIs. The
actual work it does is exactly the same as the pile of scripts you've been writing for
years.

You try it out and find that the system customization scripts in NixOS are all stored in a
repository called Nixpkgs, maintained by thousands of people, with decades of
accumulation, and with a very rich and relatively stable declarative abstraction, module
system, type system, a large-scale CI system called Hydra specifically developed for this
huge software package repository and NixOS system configuration, and a community operation
mode that has formed to facilitate collaboration and updating this complex configuration
for thousands of people.

You immediately start learning Nix and begin to rewrite the scripts you've maintained for
N years into NixOS configurations.

The more you write, the more satisfied you become, as the reduced configuration is much
easier to maintain.

A large part of the functionality previously achieved with various scripts and tools is
now encapsulated in Nixpkgs, and you can enable it and pass a few key parameters to run it
painlessly. The scripts in Nixpkgs have dedicated maintainers who update and fix any
issues found by users, and any updates that haven't undergone CI and multiple stages of
testing and validation, such as staging and unstable, won't enter the stable channel.

The "you" I mentioned earlier is none other than myself.

Now, when I think back to the days when I struggled with systemd to run a simple little
tool, I can't help but shed tears... If only I had known about NixOS earlier...

## The Declarative Configuration of NixOS - OS as Code

People with some programming experience should know the importance of abstraction and
modularization, as the complexity of a scenario increases, the benefits of abstraction and
modularization also increase. The popularity of Terraform, Kubernetes, and even Spring
Boot, reflects this. NixOS's declarative configuration is also like this, as it
encapsulates the underlying implementation details and has a community responsible for
updating and maintaining these lower-level encapsulations. This greatly reduces my
cognitive load and frees up my productivity. Its reproducibility also alleviates my
concerns about breaking the system.

NixOS is built on top of Nix, a functional package manager, drawing its design philosophy
from Eelco Dolstra's paper [The Purely Functional Software Deployment Model]. "Purely
functional" means it has no side effects, much like a mathematical function $y = f(x)$,
where the same NixOS configuration file (input parameter $x$) always yields the same NixOS
system environment (output $y$).

This means that **NixOS's configuration declares the entire system's state, OS as Code**!

As long as you have the source code of your NixOS system and it hasn't been lost,
modifying it, reviewing it, sharing the source code with others, or borrowing features
from someone else's source code is quite straightforward.

You can easily copy other NixOS users' system configurations to ensure you'll get the same
environment. In contrast, copying configurations from users of traditional distributions
like Arch or Ubuntu is much more cumbersome, considering the various version differences
and environmental peculiarities, leading to a high level of uncertainty.

## The Learning Curve of NixOS

The entry barrier of NixOS is relatively high and is not suitable for beginners who have
never touched Linux and programming. This is because its design philosophy is quite
different from traditional Linux distributions. However, this is also its advantage, as
once you cross that threshold, you will find a whole new world.

For example, **reading the source code of Nixpkgs and submitting PRs to add features， add
packages or fix bugs is a basic skill for NixOS users**, and **NixOS users who do this are
quite common**. **This is both a deterrent that scares away new users and a ladder for
Linux users who have chosen NixOS**.

Imagine that most Arch users (like me in the past) might have used Arch for several years
but didn't understand the underlying implementation details of Arch, nor did they package
their own software. But with NixOS, diving into the source code becomes a norm, which also
shows that understanding its implementation details is not difficult.

I will illustrate this point from two aspects.

First, Nix is a relatively simple language with very few syntax rules, **far simpler than
general-purpose languages like Java or Python**. Therefore, engineers with some
programming experience can master its syntax in just a few hours. With a bit more time,
reading common Nix code shouldn't be too difficult.

Second, **NixOS's good declarative abstraction and modularization system divide the OS
into many layers**, allowing users to focus only on the current layer of abstraction while
still having the option to dive deeper into the next layer to more freely implement the
desired functions (The right to choose, in fact, also gives users the opportunity to
understand NixOS progressively.). For example, new users can normally use NixOS just by
understanding the top-level abstraction. When you want to implement some customizations,
digging one level deeper into the abstraction (such as customizing some operations
directly through systemd's declarative parameters) is usually enough. If you are already a
seasoned NixOS user and want to be more geeky, you can continue to delve deeper.

In summary, understanding the source code in Nixpkgs or using Nix to package a few
programs is not difficult, and each NixOS user with some experience can also be a NixOS
packager.

## What Sets NixOS Apart?

We've heard a lot about NixOS's strengths, and I've mentioned many of them above.

People outside the Nix community might mainly hear about its dependency-conflicts-free,
the ability to roll back at any time, and its powerful reproducibility.

If you have actually used NixOS, you should also know about its other advantages:

1. NixOS's flakes feature allows you to lock the system to a specific state, and you can
   update it when you want to, even if it spans a year or two. NixOS does not force you to
   update your system frequently, you can choose to do this or not at all. Because the
   state of the system can be completely inferred from your NixOS configuration, it's much
   easier to upgrade from a old version to the latest one.

   1. It's always good to have a choice, I don't like being forced, and neither do
      sysadmins or DevOps in companies.

1. System updates have similar atomic properties to database transactions, which means
   your system updates either succeed or fail (usually without intermediate states).

1. NixOS's declarative configuration actually implements OS as Code, making these
   configurations very easy to share. You can simply copy the code for the desired
   functionality from other NixOS users into your system configuration, and you'll get an
   identical environment. Beginner users can also easily learn a lot from others'
   configurations.
   1. This is also why more and more users are using NixOS for Linux desktop ricing on
      GitHub and reddit r/unixporn in recent years.
1. The declarative configuration provides users with highly convenient system
   customization capabilities, allowing them to quickly switch various components of the
   system by changing a few lines of configuration.

1. And so on.

These are all selling points of NixOS, some of which can now also be achieved by
traditional distributions with innovations like Fedora Silverblue.

However, the system that can solve all these problems right now is only NixOS (and the
more niche Guix. According to
[Guix's README](https://git.savannah.gnu.org/cgit/guix.git/tree/README#n69), it's also
based on the Nix package manager).

## NixOS's Disadvantages and Historical Debts {#nixos-disadvantages}

For over two decades since the creation of the NixOS project, Nix package manager and the
NixOS operating system have been very niche technologies, especially in China, where only
a few Linux enthusiasts are aware of their existence, let alone using them.

NixOS is very special and powerful, but on the other hand, it has a considerable amount of
historical debt, such as:

1. Poorly organized and impenetrable documentation
2. The Flakes feature, which truly enables NixOS to meet its claimed reproducibility, is
   still in an experimental state from its official release in 2021(Nix 2.4) to 2024 now..
3. The Nix CLI is in a transition period, and the new version is much more elegant, but
   its implementation is strongly bound to the Flakes feature, making both difficult to
   stabilize and even hindering the development of many other features.
4. Defects in the module system and insufficient error handling in Nix have led to
   long-term cryptic error messages, driving users crazy.
5. The Nix language's simplicity has resulted in a large number of Bash scripts being used
   in Nixpkgs, and most of Nix's features are implemented in C++, making it a black box
   from the perspective of Nix.
6. Many implementation details of NixOS are hidden in the Nixpkgs source code, such as the
   classification of software packages and what attributes can be overridden in
   derivations.
   - Nixpkgs has long used folders to classify software packages, and there is no way to
     query the software packages by category except through the source code.
   - All derivation-related information in Nixpkgs can currently only be obtained by
     looking at the source code.
7. The maintainer of the <https://nixos.wiki> site has left, and the official has long
   failed to provide an alternative, making NixOS's documentation even worse than it
   already was.
8. The recent rapid growth of Nix/NixOS's user base has posed challenges to its community
   operation model.
9. ...

These historical debts are the main reasons why NixOS has not been more widely used. But
these issues are also opportunities for NixOS's future, as the community is actively
working to solve them. I am looking forward to seeing how NixOS will develop once these
issues are resolved.

## The Future of NixOS

No one is interested in a technology that has no future, so what about the future of
NixOS? Am I optimistic about it? Here, I try to illustrate my views on the future of NixOS
using some data.

First, let's look at the Nixpkgs project, which stores all the software packages for NixOS
and the implementation code for NixOS itself:

[![](./nixpkgs-contributors.webp)](https://github.com/NixOS/nixpkgs/graphs/contributors)

The graph shows that the activity of the Nixpkgs project has been continuously increasing
since 2021. Among the Top 6 contributors, three began contributing code in large
quantities after 2021. If you look at GitHub, you'll see that five out of the Top 10
contributors joined the community after 2021, including seasoned NixOS-CN members @NickCao
and @figsoda.

Now let's look at the commit history of the Nix package manager, which is the underlying
technology of NixOS:

[![](./nix-contributors.webp)](https://github.com/NixOS/nixpkgs/graphs/contributors)

The graph shows a significant increase in activity in the Nix project in 2020, five of the
top 6 contributors beginning to contribute code in large quantities after 2020.

Next, let's look at the Google Trends for the keyword "NixOS":

[![](./nixos-google-trends.webp)](https://trends.google.com/trends/explore?cat=5&date=2014-01-23%202024-02-23&q=NixOS)

This graph shows several obvious upticks in the search trending for NixOS:

1. In December 2021
   - This is likely due to the release of Nix 2.4 in November 2021, which brought
     experimental Flakes features and a new CLI. Flakes greatly improves the
     reproducibility of NixOS,and the new CLI is more in line with user intuition.
1. In June 2023
   - The most important reason should be that several popular Linux-related channels on
     YouTube launched several videos about NixOS around this time. As of 2024-02-23, the
     three NixOS-related videos with the highest views on YouTube were all released
     between June and July 2023, with a total view count exceeding 1.3 million.
     ![](./nixos-youtube-videos.webp)
   - Interest in China peaked recently, which may be because the user base in China has
     always been small. Then in June, I released
     [NixOS and Flakes - An Unofficial Beginner's Guide](https://nixos-and-flakes.thiscute.world/zh/),
     and I did some promotion through channels like
     [Technology Lover's Weekly](https://github.com/ruanyf/weekly/issues/3315), leading to
     a significant increase in the relative index of NixOS.
1. In January 2024
   - I'm not sure of the reason for this yet.

Now let's look at the annual user survey started by the Nix/NixOS community in 2022.

1. [2022 Nix Survey Results](https://discourse.nixos.org/t/2022-nix-survey-results/18983),
   based on the data:
   - 74.5% of users began using Nix/NixOS within the last three years.
   - In the survey about extending Nixpkgs, 36.7% of users use Flakes to extend Nixpkgs,
     second only to traditional overlays.
2. [Nix Community Survey 2023 Results](https://discourse.nixos.org/t/nix-community-survey-2023-results/33124),
   a simple calculation reveals:
   - 54.1% of users began using Nix/NixOS within the last three years.
   - In the survey about extending Nixpkgs, the percentage of users using Flakes reached
     49.2%, surpassing traditional Overlays.
   - In the survey about experimental features, the percentage of users using Flakes
     reached 59.1%.

Additionally, GitHub's
[Octoverse 2023](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/) report
also mentioned Nixpkgs:

> Developers see benefits to combining packages and containerization. As we noted earlier,
> 4.3 million repositories used Docker in 2023. **On the other side of the coin, Linux
> distribution NixOS/nixpkgs has been on the top list of open source projects by
> contributor for the last two years**.

These data points align with the increased activity in the Nixpkgs and Nix projects and
show that the Nix/NixOS community began growing rapidly after 2021.

Considering all these data points, I am very optimistic about the future of NixOS.

## Conclusion

From deciding to dive into NixOS to now, just 10 months later, the gains I've made on
Linux far exceed those of the past three years. I have tried a lot of new technologies and
tools on my PC, and my Homelab has become much richer (I now have more than ten NixOS
hosts). My understanding of the Linux system structure has also deepened.

These few points alone are enough to justify the choice, welcome to the world of NixOS!

[The Purely Functional Software Deployment Model]:
  https://edolstra.github.io/pubs/phd-thesis.pdf
