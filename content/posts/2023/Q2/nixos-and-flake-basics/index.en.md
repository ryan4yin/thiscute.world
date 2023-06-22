---
title: "NixOS & Nix Flakes - A Guide for Beginners"
date: 2023-05-10T21:23:28+08:00
lastmod: 2023-06-22T02:50:00+08:00
draft: false

resources:
  - name: "featured-image"
    src: "screenshot_2023-05-07-21-21.webp"

tags: ["NixOS", "Nix", "Flakes", "Linux", "DevOps", "Tutorial"]
categories: ["tech"]
series: ["NixOS & Nix Flakes"]
series_weight: 1

lightgallery: true

comment:
  utterances:
    enable: false
  waline:
    enable: false
  disqus:
    enable: true

code:
  # whether to show the copy button of the code block
  copy: true
  # the maximum number of lines of displayed code by default
  maxShownLines: 300
---

> The target NixOS version of this post is 22.11, and the Nix version is 2.13.3. In this environment, Flakes is still an experimental feature.

## Changelog

- 2022/6/22
  - Polish the language of the post.
- 2023/6/21
  - Add some details about the usage of `callPackage`, `override` and `overlays` in section `VIII. Advanced Usage of Nixpkgs`.
  - Add some command line tools I used frequently in section VI-6.
  - Add a new section [When will flakes stablized?]
- 2023/6/6
  - Add examples of flake's inputs & outputs into section `VII. Usage of Nix Flakes`
- 2023/6/4
  - Replace `nix-env --list-generations` by `nix profile history`
  - Replace `nix-collect-garbage` by `nix store gc`
- 2023/6/1
  - Update VI-9 according to [1000 instances of nixpkgs](https://discourse.nixos.org/t/1000-instances-of-nixpkgs/17347), create all nixpkgs instances globally in `flake.nix` to avoid this problem.
- 2023/5/21
  - Complete the section "Overlays".
  - Remove the section "IX. Nix Packaging", which may be moved to a separate post in the future.
  - Add an example of installing programs via flakes at section VI-4.

## 0. Why Nix

I heard about the Nix package manager several years ago. It uses the Nix language to describe system configuration, and the Linux distribution built on top of it can roll back to any historical state at any time. Although it sounds impressive, it requires learning a new language and writing code to install packages, I thought it was too troublesome and didn't study it at the time.

But recently I encountered two troublesome things when migrating the system, which made me decide to try Nix.

The first problem was installing EndeavourOS (a derivative distribution of Arch Linux) on a newly assembled PC. Because My old PC also uses EndeavourOS, to save time, I directly `rsync` the old PC's home directory to the new PC.
However, this synchronization caused problems -- All functions works normally, but video playback always stuck, firefox, chrome, and mpv would all get stuck. I searched various resources online but could not solve the problem until I realized it might be caused by the home directory synchronization. After clearing the home directory, the problem was solved immediately… Later, I spent a long time recovering things from the old PC one by one.

The second problem is that I recently wanted to give wayland a try, so I changed the compositor from i3 to sway.
However, because there was little difference between the two and many inconveniences (hidpi, Sway configuration tuning, etc.), I decided to switch back to i3. After switching back, GUI programs such as firefox and thunar would all get stuck for about one minute after the system started…

I was too tired to deal with the second problem, after thinking about it carefully, I realized that the root cause was that the system did not have any version control and rollback mechanism, which caused the system to be unable to be restored when problems occurred. And another problem, when installing a new system, I had to manually export the package list from the old machine and then install them on the new machine.

So I decided to switch to NixOS.

The first step I took was to create a NixOS virtual machine in my Homelab, and debug step by step in this virtual machine to migrate my old PC's EndeavourOS i3 configuration to NixOS + Flakes and restore the entire desktop environment.

Once I had it working on the virtual machine, the rest was easy. I simply backed up my home directory from my work computer, reinstalled the system as NixOS, `rysnc` the NixOS configuration from the virtual machine, made some adjustments to the disk mounting parameters, and added some extra configuration for my Nvidia graphics card. Finally, with just a few commands, I deployed the configuration and was able to restore the entire i3 environment and my commonly used software on my fresh NixOS system.
It was a truly satisfying moment!

The rollback capability of NixOS gave me a lot of confidence - I no longer fear breaking the system. So a few days ago, I further migrated to the hyprland compositor, which is indeed much better than i3, and I love its animation effects! (On EndeavourOS before, I wouldn't have dared to make such a switch for the reasons mentioned earlier - it would have been a big hassle if something went wrong with the system.)

> Note: some friends on V2EX gave feedback that `btrfs`'s snapshot feature can also provide similar rollback capabilities, and it is much simpler. After some research, I found that to be true. `btrfs` can even be configured to boot from a snapshot using GRUB(just like the NixOS does). So if you only want the system rollback capability, then btrfs based snapshot tools(e.g. [btrbk](https://github.com/digint/btrbk)) are also a good choice. Or if you're still interested in Nix, It is definitely worth learning, as Nix's capabilities are far beyond just system snapshots.

{{< figure src="./screenshot_2023-05-07-21-21.webp" caption="My NixOS Desktop" >}}

So after studying NixOS and Flakes for about half a month, I finally completed my system switch, and this post is born out of the notes I wrote during this period time, hope you like it~

Now that the background information is out of the way, it's time to dive into the world of Nix!

## I. Introduction to Nix

Nix package manager is a declarative configuration management tool similar to pulumi/terraform/kubernetes which are currently popular in the DevOps field. Users need to declare the expected system state in some configuration, and Nix is responsible for achieving that goal. The difference is that Nix manages software packages, while pulumi/terraform manages cloud resources.

> To put it simply, "declarative configuration" means that users only need to declare the results they want. For example, you declare that you want to replace the i3 window manager with sway, then Nix will help you achieve the goal. You don't need to worry about the underlying details (such as which packages sway needs to install, which i3-related packages need to be uninstalled, which system configuration or environment variables need to be adjusted for sway, what adjustments need to be made to the Sway parameters if an Nvidia graphics card is used, etc.), Nix will automatically handle these details for the user(prerequisite: if the sway's nix packages are designed properly...).

NixOS, the Linux distribution built on top of the Nix package manager, can be simply described as "OS as Code", which describes the entire operating system's state using declarative Nix configuration files.

the configuration of NixOS manages only the system-level state, user's HOME directory is not under its control. Another important community project, [home-manager](https://github.com/nix-community/home-manager), filled this gap, home-manager is designed to manage user-level packages & HOME directories. **By combining home-manager with NixOS and Git, a fully reproducible and rollbackable system environment can be obtained**(ideally).

Due to Nix's features such as declarative and reproducible, Nix is not only used to manage desktop environments but also widely used to manage development environments, compilation environments, cloud virtual machines, container image construction, etc. [NixOps](https://github.com/NixOS/nixops) from the Nix official and [deploy-rs](https://github.com/serokell/deploy-rs) from the community are both operations tools based on Nix.

> Since there are numerous files in the home directory with varying behaviors, it is impossible to version control all of them due to the high cost. Generally, only some important configuration files are managed using home-manager, and other files that need to be backed up can be backed up and synchronized using rsync/synthing, or use tools like [btrbk](https://github.com/digint/btrbk) to take snapshots of the home directory.

### Advantages of Nix

- **Declarative configuration, Environment as Code, can be managed with Git**
  - As long as the configuration files are not lost, the system can be restored to any historical state at any time(ideally).
  - Nix lock dependences's version through a lock file named `flake.lock`, to ensure that the system is reproducible, this idea actually borrows from some package managers such as npm, cargo, etc.
  - Compared with Docker, Nix provides a much stronger guarantee for the reproducibility of build results, because Dockerfile is actually an imperative configuration and there is no such thing as `flake.lock` in Docker, Docker's reproducibility relies on sharing the build result(which is MUCH MORE LARGER than Dockerfile itself) through image registry(e.g. DockerHub).
- **Highly convenient system customization capability**
  - By changing a few lines of configuration, various components of NixOS can be easily customized. This is because Nix encapsulates all the underlying complex operations in nix packages and only exports concise and necessary declarative parameters.
  - Moreover, this modification is very safe. An example is that one NixOS user on the V2EX forum stated that "[**on NixOS, switching between different desktop environments is very simple and clean, and it is very safe. I often switch between gnome/kde/sway.**](https://www.v2ex.com/t/938569#r_13053251)"
- **Rollback**: The system can be rolled back to any historical environment at any time, and NixOS even adds all old versions to the boot options by default to ensure that the system can be rolled back at any time even though it crashes. Therefore, NixOS is also considered one of the most stable Linux Systems.
- **No dependency conflicts**: Because each software package in Nix has a unique hash, its installation path also includes this hash value, so multiple versions can coexist.
- **The community is very active, and there are quite a few third-party projects**. The official package repository, nixpkgs, has many contributors, and many people share their Nix configuration on Github/Gitlab. After browsing through it, the entire ecosystem gives me a sense of excitement in discovering a new continent.

{{< figure src="./nixos-bootloader.avif" caption="All historical versions are listed in the boot options of NixOS. Image from [NixOS Discourse - 10074](https://discourse.nixos.org/t/how-to-make-uefis-grub2-menu-the-same-as-bioss-one/10074)" >}}

### Disadvantages of Nix

- **Relatively high learning curve:**: If you want the system to be completely reproducible and avoid pitfalls caused by improper use, you need to learn about the entire design of Nix and manage the system in a declarative manner. You cannot blindly use `nix-env -i` (which is similar to `apt-get install`).
- **Chaotic documentation**: Flakes is still an experimental feature, and there are currently few documents introducing it, Most of the Nix community's documentation only introduces the old cli such as `nix-env`/`nix-channel`. If you want to start learning Nix directly from Flakes, you need to refer to a large number of old documents and extract what you need from them. In addition, some of Nix's current core functions are not well-documented (such as `imports` and Nix Module System), to figure out what it does, it is best to look at the source code...
- ~~Relatively few packages~~: Retract this one. The official claim is that nixpkgs has [80000+](https://search.nixos.org/packages) packages, and indeed, most packages can be found in nixpkgs.
- **Relatively high disk space usage**: To ensure that the system can be rolled back at any time, Nix preserves all historical environments by default, which can take up a lot of disk space. Although you can manually clean up old historical environments periodically with `nix-collect-garbage`, it is still recommended to buy a larger hard drive.

### Summary

Generally speaking, I think NixOS is suitable for developers who have some experience in using Linux and programming and want to have more control over their systems.

I don't recommend you getting started with NixOS if you are new to Linux, it can be a very painful journey.

## II. Installation

Nix can be installed in multiple ways and supports being installed on macOS/Linux/WSL as a package manager. Nix also provides NixOS, a Linux distribution that uses Nix to manage the entire system environment.

I chose to directly install NixOS system using its ISO image, to manage the entire system through Nix as much as possible.

The installation process is simple, and I won't go into details here.

some materials that may be useful:

1. [Official installation method of Nix](https://nixos.org/download.html): written in bash script, `nix-command` & `flakes` are still experimental features as of 2023-04-23, and need to be manually enabled.
   1. You need to refer to the instructions in [Enable flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) to enable `nix-command` & `flakes`.
   2. The official installer does not provide any uninstallation method. To uninstall Nix on Linux/macOS, you need to manually delete all related files, users, and groups.
2. [The Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer): a third-party installer written in Rust, which enables `nix-command` & `flakes` by default and provides an uninstallation command.

## III. Nix Flakes and the classic Nix

As `nix-command` & `flakes` are still experimental features, the official documentation does not cover them in detail, and the community's documentation about them is also very scattered.
However, from the perspective of reproducibility and ease of management and maintenance, the classic Nix package structure and cli are no longer recommended for use.
So I will not introduce the usage of the classic Nix. It's recommended that beginners just start with `nix-command` & `flakes` and ignore all thecontents about the classic Nix.

Here are the classic Nix commands and related concepts that are no longer needed after you enabling `nix-command` and `flakes`, when searching for information, you can safely ignore them:

1. `nix-channel`: `nix-channel` is similar to other package management tools such as apt/yum/pacman, managing software package versions through stable/unstable/test channels.
   1. In Flakes, the functionality of `nix-channel` is completely replaced by `inputs` in `flake.nix` to declare dependency sources and `flake.lock` to lock dependency versions.
2. `nix-env`: `nix-env` is a core command-line tool for traditional Nix used to manage software packages in the user environment. It installs software packages from the data sources defined by `nix-channel`, so the installed package versions are influenced by the channel. Packages installed with `nix-env` are not automatically recorded in Nix's declarative configuration and are entirely outside of its control, making them difficult to reproduce on other machines. Therefore, it is not recommended to use this tool.
   1. The corresponding command in Flakes is `nix profile`.
3. `nix-shell`: `nix-shell` is used to create a temporary shell environment.
   1. In Flakes, it is replaced by `nix develop` and `nix shell`.
4. `nix-build`: `nix-build` is used to build Nix packages, and it places the build results in `/nix/store`, but it does not record them in Nix's declarative configuration.
   1. The corresponding command in Flakes is `nix build`.
5. ...

> maybe `nix-env -qa` is still useful some times, which returns all packages installed in the System.

## IV. Package Repositories of Nix

Similar to Arch Linux, Nix also has official and community software package repositories:

1. [nixpkgs](https://github.com/NixOS/nixpkgs) is a Git repository containing all Nix packages and NixOS modules.
   1. Its `master` branch contains the latest Nix packages and modules.
   2. The `nixos-unstable` branch contains the latest tested modules, but some bugs may still exist.
   3. And the `nixos-XX.YY` branch(the stable branch) contains the latest stable Nix packages and modules.
2. [NUR](https://github.com/nix-community/NUR) is similar to Arch Linux's AUR.
   1. NUR is a third-party Nix package repository and serves as a supplement to nixpkgs, use it at your own risk.
3. Flakes can also install software packages directly from Git repositories, which can be used to install Flakes provided by anyone, we will talk about this later.

## V. Basics of The Nix language

The Nix language is used to declare the configuration to be built by Nix, if you want to play with NixOS and Flakes and enjoy the benefits they bring, you must learn the basics of this language first.

The Nix language is a simple functional language, if you already have some experience in programming, it should take less than 2 hours to go through Nix lanuage's basics.

Please read [**Nix language basics - nix.dev**](https://nix.dev/tutorials/first-steps/nix-language) and [Chapter 4. The Basics of the Language - Nix Pills](https://nixos.org/guides/nix-pills/basics-of-language.html) to get a basic understanding of Nix language now, they are all good introductory materials.

## VI. Managing the system declaratively

> https://nixos.wiki/wiki/Overview_of_the_NixOS_Linux_distribution

After learning the basics of the Nix language, we can start using it to configure our NixOS. The default configuration for NixOS is located at `/etc/nixos/configuration.nix`, which contains all the declarative configuration for the system, such as time zone, language, keyboard layout, network, users, file system, boot options, etc.

If we want to modify the system state in a reproducible way (**which is also the most recommended way**), we need to manually edit `/etc/nixos/configuration.nix`, and then execute `sudo nixos-rebuild switch` to apply the modified configuration, it will generate a new system environment based on the configuration file we modified, sets the new environment as the default one, and also preserves & added the previous environment into the boot options of grub/sytemd-boot. This ensures we can always roll back to the old environment(even if the new environment fails to start).

`/etc/nixos/configuration.nix` is the classic method to configure NixOS, which relies on data sources configured by `nix-channel` and has no version-locking mechanism, making it difficult to ensure the reproducibility of the system. **A better approach is to use Flakes**, which can ensure the reproducibility of the system and make it easy to manage the configuration.

Now first, let's learn how to manage NixOS through the classic method, `/etc/nixos/configuration.nix`, and then migrate to the more advanced Flakes.

### 1. Configuring the system using `/etc/nixos/configuration.nix`

As I mentioned earlier, this is the classic method to configured NixOS, and also the default method currently used by NixOS. It relies on data sources configured by `nix-channel` and has no version-locking mechanism, making it difficult to ensure the reproducibility of the system.

For example, to enable ssh and add a user "ryan", simply add the following content into `/etc/nixos/configuration.nix`:

```nix
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running 'nixos-help').
{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # Omit the previous configuration.......

  # add user ryan
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

  # enable openssh-server
  services.openssh = {
    enable = true;
    permitRootLogin = "no";         # disable root login
    passwordAuthentication = false; # disable password login
    openFirewall = true;
    forwardX11 = true;              # enable X11 forwarding
  };

  # omit the rest of the configuration.......
}
```

In this configuration, we declared that we want to enable the openssh service, add an ssh public key for the user ryan, and disable password login.

Now, let's run `sudo nixos-rebuild switch` to deploy the modified configuration, and then we can login to the system using ssh with the ssh keys we configured.

Any reproducible changes to the system can be made by modifying `/etc/nixos/configuration.nix` and deploying the changes by running `sudo nixos-rebuild switch`.

All configuration options in `/etc/nixos/configuration.nix` can be found in the following places:

- By searching on Google, such as `Chrome NixOS`, which will provide NixOS informations related to Chrome. Generally, the NixOS Wiki and the source code of Nixpkgs will be among the top results.
- By searching for keywords in [NixOS Options Search](https://search.nixos.org/options).
- For system-level configuration, relevant documentation can be found in [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration).
- By searching for keywords directly in the source code of [nixpkgs](https://github.com/NixOS/nixpkgs) on GitHub.

### 2. Enabling NixOS Flakes Support

Compared to the default configuration approach of NixOS, Flakes provide better reproducibility and a clearer package structure that is easier to maintain. Therefore, it is recommended to manage NixOS with Flakes.

However, as Flakes is still an experimental feature currently, it's not enabled by default yet, we need to enable it manually by modifying `/etc/nixos/configuration.nix`, example as follows:

```nix
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running 'nixos-help').
{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # omit the previous configuration.......

  # enable Flakes and the new command line tool
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  environment.systemPackages = with pkgs; [
    # Flakes uses git to pull dependencies from data sources, so git must be installed first
    git
    vim
    wget
    curl

  ];

  # omit the rest of the configuration.......
}
```

Now run `sudo nixos-rebuild switch` to apply the changes, and then you can write the configuration for NixOS with Flakes.

### 3. Switching System Configuration to `flake.nix`

After enabling `flakes`, `sudo nixos-rebuild switch` will try to read`/etc/nixos/flake.nix` first every time you run it, if not found, it will fallback to `/etc/nixos/configuration.nix`.

Now to learn how to write a flake, let's take a look at the official flake templates provided by Nix. First, check which templates are available:

```bash
nix flake show templates
```

The templates `templates#full` contains all possible usecases, let's take a look at it:

```bash
nix flake init -t templates#full
cat flake.nix
```

After reading this example, let's create a file `/etc/nixos/flake.nix` and copy the content of the example into it.
With `/etc/nixos/flake.nix`, all system modifications will be taken over by Flakes from now on.

The template we copied can not jsut be used directly, we need to modify it to make it work, an example of `/etc/nixos/flake.nix` is as follows:

```nix
{
  description = "Ryan's NixOS Flake";

  # This is the standard format for flake.nix. `inputs` are the dependencies of the flake,
  # and `outputs` function will return all the build results of the flake.
  # Each item in `inputs` will be passed as a parameter to the `outputs` function after being pulled and built.
  inputs = {
    # There are many ways to reference flake inputs. The most widely used is github:owner/name/reference,
    # which represents the GitHub repository URL + branch/commit-id/tag.

    # Official NixOS package source, using nixos-unstable branch here
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # home-manager, used for managing user configuration
    home-manager = {
      url = "github:nix-community/home-manager/release-22.11";
      # The `follows` keyword in inputs is used for inheritance.
      # Here, `inputs.nixpkgs` of home-manager is kept consistent with the `inputs.nixpkgs` of the current flake,
      # to avoid problems caused by different versions of nixpkgs.
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  # `outputs` are all the build result of the flake.
  # A flake can have many use cases and different types of outputs.
  # parameters in `outputs` are defined in `inputs` and can be referenced by their names.
  # However, `self` is an exception, This special parameter points to the `outputs` itself (self-reference)
  # The `@` syntax here is used to alias the attribute set of the inputs's parameter, making it convenient to use inside the function.
  outputs = { self, nixpkgs, ... }@inputs: {
    nixosConfigurations = {
      # By default, NixOS will try to refer the nixosConfiguration with its hostname.
      # so the system named `nixos-test` will use this configuration.
      # However, the configuration name can also be specified using `sudo nixos-rebuild switch --flake /path/to/flakes/directory#<name>`.
      # The `nixpkgs.lib.nixosSystem` function is used to build this configuration, the following attribute set is its parameter.
      # Run `sudo nixos-rebuild switch --flake .#nixos-test` in the flake's directory to deploy this configuration on any NixOS system
      "nixos-test" = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # The Nix module system can modularize configuration, improving the maintainability of configuration.
        #
        # Each parameter in the `modules` is a Nix Module, and there is a partial introduction to it in the nixpkgs manual:
        #    <https://nixos.org/manual/nixpkgs/unstable/#module-system-introduction>
        # It is said to be partial because the documentation is not complete, only some simple introductions
        #    (such is the current state of Nix documentation...)
        # A Nix Module can be an attribute set, or a function that returns an attribute set.
        # If a Module is a function, according to the Nix Wiki description, this function can have up to four parameters:
        #
        #  lib:     the nixpkgs function library, which provides many useful functions for operating Nix expressions
        #            https://nixos.org/manual/nixpkgs/stable/#id-1.4
        #  config:  all config options of the current flake
        #  options: all options defined in all NixOS Modules in the current flake
        #  pkgs:   a collection of all packages defined in nixpkgs.
        #           you can assume its default value is `nixpkgs.legacyPackages."${system}"` for now.
        #           can be customed by `nixpkgs.pkgs` option
        #  modulesPath: the default path of nixpkgs's builtin modules folder,
        #               used to import some extra modules from nixpkgs.
        #               this parameter is rarely used, you can ignore it for now.
        # Only these parameters can be passed by default.
        # If you need to pass other parameters, you must use `specialArgs` by uncomment the following line
        # specialArgs = {...}  # pass custom arguments into sub module.
        modules = [
          # Import the configuration.nix we used before, so that the old configuration file can still take effect.
          # Note: /etc/nixos/configuration.nix itself is also a Nix Module, so you can import it directly here
          ./configuration.nix
        ];
      };
    };
  };
}
```

Here we defined a NixOS system called `nixos-test`, whose configuration file is `./configuration.nix`, which is the classic configuration we modified before, so we can still make use of it.

Now run `sudo nixos-rebuild switch` to apply the configuration, and no changes will be made to the system, because we imported the old configuration file in `/etc/nixos/flake.nix`, so the actual state we declared remains unchanged.

### 4. Manage system software through Flakes

After the switch, we can now manage the system through Flakes. The most common requirement for managing a system is to install softwares. We have seen how to install packages through `environment.systemPackages` before, and these packages are all from the official nixpkgs repository.

Now let's learn how to install packages from other sources through Flakes. This is much more flexible than installing from nixpkgs directly. The most obvious benefit is that you can easily set the version of the software.

Use [helix](https://github.com/helix-editor/helix) editor as an example, first we need to add the helix as an input into `flake.nix`:

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # ......

  inputs = {
    # ......

    # helix editor, use the tag 23.05
    helix.url = "github:helix-editor/helix/23.05"
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    nixosConfigurations = {
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # set all inputs parameters as specialArgs of all sub module
        # so that we can use `helix` input in sub modules
        specialArgs = inputs;
        modules = [
          ./configuration.nix
        ];
      };
    };
  };
}
```

Then udpate `configuration.nix` to install `helix` from the input `helix`:

```nix
# Nix will automatically inject `helix` from specialArgs
# into the third parameter of this function through name matching
{ config, pkgs, helix, ... }:

{
  # omit other configuration......

  environment.systemPackages = with pkgs; [
    git
    vim
    wget
    curl

    # install helix from the input `helix`
    helix."${pkgs.system}".packages.helix
  ];

  # omit other configuration......
}
```

Now deploy the changes by `sudo nixos-rebuild switch`, and then we can start the helix editor by `helix` command.

### 5. Add Custom Cache Mirror

To speed up package building, Nix provides <https://cache.nixos.org> to cache build results to avoid build every packages locally.

With the NixOS's classic configuration method, other cache sources can be added by using `nix-channel`, but Flakes avoids using any system-level configuration and environment variables to ensure that its build results are not affected by the environment(so the build results are reproducible).

Therefore, to customize the cache source, we must add the related configuration in `flake.nix` by using the parameter `nixConfig`. An example is as follows:

```nix
{
  description = "NixOS configuration of Ryan Yin";

  # 1. To ensure purity, Flakes does not rely on the system's `/etc/nix/nix.conf`, so we have to set related configuration here.
  # 2. To ensure security, flake allows only a few nixConfig parameters to be set directly by default.
  #    you need to add `--accept-flake-config` when executing the nix command,
  #    otherwise all other parameters will be ignored, and an warning will printed by nix.
  nixConfig = {
    experimental-features = [ "nix-command" "flakes" ];
    substituters = [
      # replace official cache with a mirror located in China
      "https://mirrors.bfsu.edu.cn/nix-channels/store"
      "https://cache.nixos.org/"
    ];

    extra-substituters = [
      # nix community's cache server
      "https://nix-community.cachix.org"
    ];
    extra-trusted-public-keys = [
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
    ];
  };

  inputs = {
    # omit some configuration...
  };

  outputs = {
    # omit some configuration...
  };
}

```

After the modification, run `sudo nixos-rebuild switch` to apply the updates.

### 6. Install home-manager

As I mentioned earlier, NixOS can only manage system-level configuration, to manage the Home directory(user-level configuration), we need to install home-manager.

According to the official document [Home Manager Manual](https://nix-community.github.io/home-manager/index.htm), in order to install home-manager as a module of NixOS, we need to create `/etc/nixos/home.nix` first, an example content shown below:

```nix
{ config, pkgs, ... }:

{
  # please change the username & home direcotry to your own
  home.username = "ryan";
  home.homeDirectory = "/home/ryan";

  # link the configuration file in current directory to the specified location in home directory
  # home.file.".config/i3/wallpaper.jpg".source = ./wallpaper.jpg;

  # link all files in `./scripts` to `~/.config/i3/scripts`
  # home.file.".config/i3/scripts" = {
  #   source = ./scripts;
  #   recursive = true;   # link recursively
  #   executable = true;  # make all files executable
  # };

  # encode the file content in nix configuration file directly
  # home.file.".xxx".text = ''
  #     xxx
  # '';

  # set cursor size and dpi for 4k monitor
  xresources.properties = {
    "Xcursor.size" = 16;
    "Xft.dpi" = 172;
  };

  # basic configuration of git, please change to your own
  programs.git = {
    enable = true;
    userName = "Ryan Yin";
    userEmail = "xiaoyin_c@qq.com";
  };

  # Packages that should be installed to the user profile.
  home.packages = [
    # here is some command line tools I use frequently
    # feel free to add your own or remove some of them

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

  # alacritty - a cross-platform, GPU-accelerated terminal emulator
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

  # This value determines the home Manager release that your
  # configuration is compatible with. This helps avoid breakage
  # when a new home Manager release introduces backwards
  # incompatible changes.
  #
  # You can update home Manager without changing this value. See
  # the home Manager release notes for a list of state version
  # changes in each release.
  home.stateVersion = "22.11";

  # Let home Manager install and manage itself.
  programs.home-manager.enable = true;
}
```

After adding `/etc/nixos/home.nix`, you need to import this new configuration file in `/etc/nixos/flake.nix` to make use of it, use the following command to generate an example in the current folder for reference:

```shell
nix flake new example -t github:nix-community/home-manager#nixos
```

After adjusting the parameters, the content of `/etc/nixos/flake.nix` is as follows:

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
      # TODO please change the hostname to your own
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./configuration.nix

          # make home-manager as a module of nixos
          # so that home-manager configuration will be deployed automatically when executing `nixos-rebuild switch`
          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;

            # TODO replace ryan with your own username
            home-manager.users.ryan = import ./home.nix;

            # Optionally, use home-manager.extraSpecialArgs to pass arguments to home.nix
          }
        ];
      };
    };
  };
}
```

Then run `sudo nixos-rebuild switch` to apply the configuration, and home-manager will be installed automatically.

After the installation is complete, all user-level packages and configuration can be managed through `/etc/nixos/home.nix`. When running `sudo nixos-rebuild switch`, the configuration of home-manager will be applied automatically. (**It's not necessary to run `home-manager switch` manually**!)

To find the options we can use in `home.nix`, referring to the following documents:

- [Home Manager - Appendix A. Configuration Options](https://nix-community.github.io/home-manager/options.html): A list of all options, it is recommended to search for keywords in it.
- [home-manager](https://github.com/nix-community/home-manager): Some options are not listed in the official documentation, or the documentation is not clear enough, you can directly search and read the corresponding source code in this home-manager repo.

### 7. Modular NixOS configuration

At this point, the skeleton of the entire system is basically configured. The current configuration structure in `/etc/nixos` should be as follows:

```
$ tree
.
├── flake.lock
├── flake.nix
├── home.nix
└── configuration.nix
```

The functions of these four files are explained below:

- `flake.lock`: An automatically generated version-lock file, which records all input sources, hash values, and version numbers of the entire flake to ensure that the system is reproducible.
- `flake.nix`: The entry file, which will be recognized and deployed when executing `sudo nixos-rebuild switch`.
  - See [Flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) for all options of flake.nix.
- `configuration.nix`: Imported as a nix module in flake.nix, all system-level configuration are currently written here.
  - See [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration) for all options of configuration.nix.
- `home.nix`: Imported by home-manager as the configuration of the user `ryan` in flake.nix, that is, it contains all the configuration of `ryan`, and is responsible for managing `ryan`'s home folder.
  - See [Appendix A. Configuration Options - home Manager](https://nix-community.github.io/home-manager/options.html) for all options of home.nix.

By modifying these files, you can change the status of the system and the home directory declaratively.

As the configuration increases, it will be difficult to maintain the configuration by relying solely on `configuration.nix` and `home.nix`. Therefore, a better solution is to use the nix module system to split the configuration into multiple modules and write them in a classified manner.

nix module system provide a paramter, `imports`,which accept a list of `.nix` files, and merge all the configuration defined in these files into the current nix module. Note that the word used here is "**merge**", which means that `imports` will **NOT** simply overwrite the duplicate configuration, but handle them more reasonably. For example, if I define `program.packages = [...]` in multiple modules, then `imports` will merge all `program.packages` defined in all nix modules into one list. Not only lists can be merged correctly, but attribute sets can also be merged correctly. The specific behavior can be explored by yourself.

> I only found a description of `imports` in [nixpkgs-unstable official manual - evalModules parameters](https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules-parameters): `A list of modules. These are merged together to form the final configuration.`, it's a bit ambiguous...

With the help of `imports`, we can split `home.nix` and `configuration.nix` into multiple nix modules defined in diffrent `.nix` files.

Use [ryan4yin/nix-config/v0.0.2](https://github.com/ryan4yin/nix-config/tree/v0.0.2) as an example, which is the configuration of my previous NixOS system with i3 window manager. The structure of it is as follows:

```shell
├── flake.lock
├── flake.nix
├── home
│   ├── default.nix         # here we import all submodules by imports = [...]
│   ├── fcitx5              # fcitx5 input method's configuration
│   │   ├── default.nix
│   │   └── rime-data-flypy
│   ├── i3                  # i3 window manager's configuration
│   │   ├── config
│   │   ├── default.nix
│   │   ├── i3blocks.conf
│   │   ├── keybindings
│   │   └── scripts
│   ├── programs
│   │   ├── browsers.nix
│   │   ├── common.nix
│   │   ├── default.nix   # here we import all modules in programs folder by imports = [...]
│   │   ├── git.nix
│   │   ├── media.nix
│   │   ├── vscode.nix
│   │   └── xdg.nix
│   ├── rofi              #  rofi launcher's configuration
│   │   ├── configs
│   │   │   ├── arc_dark_colors.rasi
│   │   │   ├── arc_dark_transparent_colors.rasi
│   │   │   ├── power-profiles.rasi
│   │   │   ├── powermenu.rasi
│   │   │   ├── rofidmenu.rasi
│   │   │   └── rofikeyhint.rasi
│   │   └── default.nix
│   └── shell             # shell/terminal related configuration
│       ├── common.nix
│       ├── default.nix
│       ├── nushell
│       │   ├── config.nu
│       │   ├── default.nix
│       │   └── env.nu
│       ├── starship.nix
│       └── terminals.nix
├── hosts
│   ├── msi-rtx4090      # My main machine's configuration
│   │   ├── default.nix  # This is the old configuration.nix, but most of the content has been split out to modules.
│   │   └── hardware-configuration.nix  # hardware & disk related configuration, autogenerated by nixos
│   └── nixos-test       # my test machine's configuration
│       ├── default.nix
│       └── hardware-configuration.nix
├── modules          # some common NixOS modules that can be reused
│   ├── i3.nix
│   └── system.nix
└── wallpaper.jpg    # wallpaper
```

For more details, see [ryan4yin/nix-config/v0.0.2](https://github.com/ryan4yin/nix-config/tree/v0.0.2).

### 8. Update the system

With Flakes, it is also very simple to update the system. Just run the following commands in `/etc/nixos`:

```shell
# update flake.lock
nix flake update
# apply the updates
sudo nixos-rebuild switch
```

Sometimes you may encounter some error of sha256 mismatch when running `nixos-rebuild switch`, which may be solved by updating `flake.lock` through `nix flake update`.

### 9. Downgrade or upgrade some packages

After using Flakes, most people are currently using the `nixos-unstable` branch of nixpkgs. Sometimes you will encounter some bugs, such as the [chrome/vscode crash problem](https://github.com/swaywm/sway/issues/7562)

To resolve problems, we may need to downgrade or upgrade some packages. In Flakes, all package versions and hash values are one-to-one corresponding to the git commit of their flake input.
Therefore, to downgrade or upgrade a package, we need to lock the git commit of its flake input.

For exmaple, let's add multiple nixpkgs, each using a different git commit or branch:

```nix
{
  description = "NixOS configuration of Ryan Yin"

  inputs = {
    # default to nixos-unstable branch
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    # the latest stable branch of nixpkgs, used to rollback the version of some packages
    # the current latest version is 22.11
    nixpkgs-stable.url = "github:nixos/nixpkgs/nixos-22.11";

    # we can also use git commit hash to lock the version
    nixpkgs-fd40cef8d.url = "github:nixos/nixpkgs/fd40cef8d797670e203a27a91e4b8e6decf0b90c";
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

        # The core parameter, which passes the non-default nixpkgs instances to other nix modules
        specialArgs = {
          # To use packages from nixpkgs-stable, we need to configure some parameters for it first
          pkgs-stable = import nixpkgs-stable {
            system = system;  # refer the `system` parameter form outer scope recursively
            # To use chrome, we need to allow the installation of non-free software
            config.allowUnfree = true;
          };
          pkgs-fd40cef8d = import nixpkgs-fd40cef8d {
            system = system;
            config.allowUnfree = true;
          };
        };
        modules = [
          ./hosts/nixos-test

          # omit other configuration...
        ];
      };
    };
  };
}
```

And then refer the packages from `pkgs-stable` or `pkgs-fd40cef8d` in your sub module, a home manager's sub module as an example:

```nix
{
  pkgs,
  config,
  # nix will search and jnject this parameter from specialArgs in flake.nix
  pkgs-stable,
  # pkgs-fd40cef8d,
  ...
}:

{
  # refer packages from pkgs-stable instead of pkgs
  home.packages = with pkgs-stable; [
    firefox-wayland

    # chrome wayland support was broken on nixos-unstable branch, so fallback to stable branch for now
    # https://github.com/swaywm/sway/issues/7562
    google-chrome
  ];

  programs.vscode = {
    enable = true;
    package = pkgs-stable.vscode;  # refer vscode from pkgs-stable instead of pkgs
  };
}
```

After adjusted the configuration, deploy it with `sudo nixos-rebuild switch`, then your firefox/chrome/vscode will be downgraded to the version corresponding to `nixpkgs-stable` or `nixpkgs-fd40cef8d`.

> according to [1000 instances of nixpkgs](https://discourse.nixos.org/t/1000-instances-of-nixpkgs/17347), it's not a good practice to use `import` in sub modules to customize `nixpkgs`, because each `import` will create a new instance of nixpkgs, which will increase the build time and memory usage as the configuration grows. So here we create all nixpkgs instances in `flake.nix` to avoid this problem.

### 10. Manage the configuration with Git

NixOS configuration is just a set of text files, it is very suitable to be managed with Git, and thus we can easily rollback to a previous version when we encounter some problems.

However, NixOS places the configuration in `/etc/nixos` by default, which requires root permissions to modify, which is not convenient for daily use.
Luckily, Flakes can solve this problem, you can place your flake anywhere you like.

For example, my usage is to place my flake in `~/nixos-config`, and then create a soft link in `/etc/nixos`:

```shell
sudo mv /etc/nixos /etc/nixos.bak  # backup the original configuration
sudo ln -s ~/nixos-config/ /etc/nixos

# deploy the flake.nix located at the default location(/etc/nixos)
sudo nixos-rebuild switch
```

And then you can use Git to manage the configuration in `~/nixos-config`. The configuration can be used with ordinary user-level permissions, and it is not required to be owned by root.

Another method is jsut to delete `/etc/nixos` directly, and specify the configuration file path each time you deploy it:

```shell
sudo mv /etc/nixos /etc/nixos.bak
cd ~/nixos-config

# `--flake .#nixos-test` means deploy the flake.nix located in the current directory, and the nixosConfiguration's name is `nixos-test`
sudo nixos-rebuild switch --flake .#nixos-test
```

Choose whichever you like. After that, system rollback will become very simple, just switch to the previous commit and then deploy it:

```shell
cd ~/nixos-config
# switch to the previous commit
git checkout HEAD^1
# deploy the flake.nix located in the current directory, and the nixosConfiguration's name is `nixos-test`
sudo nixos-rebuild switch --flake .#nixos-test
```

More operations on Git are not described here. Generally speaking, rollback can be done directly through Git. Only when the system crashes completely, you will need to restart into bootloader and boot the system from the previous historical version.

### 11. View and delete history data {#view-and-delete-history}

As we mentioned before, each deployment of NixOS will generate a new version, and all versions will be added to the system boot options. In addition to restarting the computer, we can also query all available historical versions through the following command:

```shell
nix profile history --profile /nix/var/nix/profiles/system
```

The command to clean up historical versions to release storage space:

```shell
# delete all historical versions older than 7 days
sudo nix profile wipe-history --profile /nix/var/nix/profiles/system  --older-than 7d

# we need to collect garbages after wipe-history
sudo nix store gc --debug
```

Another command returns all packages installed in the system:

```shell
nix-env -qa
```

## VII. Usage of Nix Flakes

Up to now, we have written a lot of configuration with Flakes to manage NixOS. Here is a brief introduction to the more detailed content of the Flakes, as well as the new command lines commonly used with flakes.

### 1. Flake inputs {#flake-inputs}

The `inputs` in `flake.nix` is a attribute set, used to specify the dependencies of the current flake, there are many types of `inputs`, for example:

```nix
{
  inputs = {
    # use master branch of the GitHub repository as input, this is the most common input format
    nixpkgs.url = "github:Mic92/nixpkgs/master";
    # Git URL, can be used for any Git repository based on https/ssh protocol
    git-example.url = "git+https://git.somehost.tld/user/path?ref=branch&rev=fdc8ef970de2b4634e1b3dca296e1ed918459a9e";
    # The above example will also copy .git, use this for (shallow) local Git repos
    git-directory-example.url = "git+file:/path/to/repo?shallow=1";
    # Local directories (for absolute paths you can omit 'path:')
    directory-example.url = "path:/path/to/repo";

    bar = {
      url = "github:foo/bar/branch";
      # if the input is not a flake, you need to set flake=false
      flake = false;
    };

    sops-nix = {
      url = "github:Mic92/sops-nix";
      # The `follows` keyword in inputs is used for inheritance.
      # Here, `inputs.nixpkgs` of sops-nix is kept consistent with the `inputs.nixpkgs` in
      # the current flake, to avoid problems caused by different versions of nixpkgs.
      inputs.nixpkgs.follows = "nixpkgs";
    };

    # Pin flakes to a specific revision
    nix-doom-emacs = {
      url = "github:vlaci/nix-doom-emacs?rev=238b18d7b2c8239f676358634bfb32693d3706f3";
      flake = false;
    };

    # To use a subdirectory of a repo, pass `dir=xxx`
    nixpkgs.url = "github:foo/bar?dir=shu";
  }
}
```

### 2. Flake outputs

the `outputs` in `flake.nix` are what a flake produces as part of its build. Each flake can have many different outputs simultaneously, including but not limited to:

- Nix packages: named `apps.<system>.<name>`, `packages.<system>.<name>`, or `legacyPackages.<system>.<name>`
  - we can build a package by command `nix build .#<name>`
- Nix Helper Functions: named `lib`., which means a library for other flakes.
- Nix development environments: named `devShells`
  - `devShells` can be used by command `nix develop`, will be introduced later.
- NixOS configuration: named `nixosConfiguration`
  - `nixosConfiguration` will be used by command `nixos-rebuild switch --flake .#<name>`
- Nix templates: named `templates`
  - templates can be used by command `nix flake init --template <reference>`
- Other user defined outputs, may be parsed by other nix-related tools.

An example copy from NixOS Wiki:

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

### 3. Flake Command Line Usage

after enabled `nix-command` & `flake`, you can use `nix help` to get all the info of [New Nix Commands][New Nix Commands], some useful examples are listed below:

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
# this command use `devShells.example` in flake `zero-to-nix`'s outputs, to setup the development environment,
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

[Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems] is a brand new guide to get started with Nix & Flake, recommended to read for beginners.

## VIII. Nixpkgs's Advanced Usage

`callPackage`, `Overriding`, and `Overlays` are the techniques occasionally used when using Nix to customize the build method of Nix packages.

We know that many programs have a large number of build parameters that need to be configured, and different users may want to use different build parameters. This is where `Overriding` and `Overlays` come in handy. Let me give you a few examples I have encountered:

1. [`fcitx5-rime.nix`](https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix): By default, `fcitx5-rime` use `rime-data` as the value of `rimeDataPkgs`, but this parameter can be customized by `override`.
2. [`vscode/with-extensions.nix`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vscode/with-extensions.nix): This package for VS Code can also be customized by overriding the value of `vscodeExtensions`, thus we can install some custom plugins into VS Code.
   - [`nix-vscode-extensions`](https://github.com/nix-community/nix-vscode-extensions): This is a vscode plugin manager implemented by overriding `vscodeExtensions`.
3. [`firefox/common.nix`](https://github.com/NixOS/nixpkgs/blob/416ffcd08f1f16211130cd9571f74322e98ecef6/pkgs/applications/networking/browsers/firefox/common.nix): Firefox has many customizable parameters too.
4. ...

In short, `Overriding` or `Overlays` can be used to customize the build parameters of Nix packages.

### 1. pkgs.callPackage {#callpackage}

> [Chapter 13. Callpackage Design Pattern - Nix Pills](https://nixos.org/guides/nix-pills/callpackage-design-pattern.html)

In the previous content, We have used `import xxx.nix` to import Nix files many times, this syntax simply returns the execution result of the file, without any further processing of the it.

`pkgs.callPackage` is also used to import Nix files, its syntax is `pkgs.callPackage xxx.nix { ... }`, but unlike `import`, the Nix file imported by it must be a Derivation or a function that returns a Derivation. Its result is a Derivation(a software package) too.

So what does the Nix file that can be used as a parameter of `pkgs.callPackge` look like? You can take a look at the `hello.nix` `fcitx5-rime.nix` `vscode/with-extensions.nix` `firefox/common.nix` we mentioned earlier, they can all be imported by `pkgs.callPackage`.

When the `xxx.nix` used in `pkgs.callPackge xxx.nix {...}` is a function (most Nix packages are like this), the execution flow is as follows:

1. `pkgs.callPackge xxx.nix {...}` will first `import xxx.nix` to get the function defined in it. The parameters of this function usually have `lib`, `stdenv`, `fetchurl` and other parameters, as well as some custom parameters, which usually have default values.
2. Then `pkgs.callPackge` will first look up the value matching the name from the current environment as the parameter to be passed to the function. parameters like `lib` `stdenv` `fetchurl` are defined in nixpkgs, and they will be found in this step.
3. Then `pkgs.callPackge` will merge its second parameter `{...}` with the attribute set obtained in the previous step, and then pass it to the function imported from `xxx.nix` and execute it.
4. Finally we get a Derivation as the result of the function execution.

So the common usage of `pkgs.callPackage` is to import custom Nix packages and used it in Nix Module.
For example, we wrote a `hello.nix` ourselves, and then we can use `pkgs.callPackage ./hello.nix {}` in any Nix Module to import and use it.

### 2. Overriding {#overriding}

> [Chapter 4. Overriding - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overrides)

Simply put, all Nix packages in nixpkgs can be customized with `<pkg>.override {}` to define some build parameters, which returns a new Derivation that uses custom parameters. For example:

```nix
pkgs.fcitx5-rime.override {rimeDataPkgs = [
    ./rime-data-flypy
];}
```

The result of this Nix expression is a new Derivation, where `rimeDataPkgs` is overridden as `[./rime-data-flypy]`, while other parameters remain their original values.

How to know which parameters of `fcitx5-rime` can be overridden? There are several ways:

1. Try to find the source code of the package in the nixpkgs repository on GitHub, such as [fcitx5-rime.nix](https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix)
   1. Note: Be sure to select the correct branch, for example, if you are using the nixos-unstable branch, you need to find it in the nixos-unstable branch.
2. Check by using `nix repl '<nixpkgs>'`, then enter `:e pkgs.fcitx5-rime`, which will open the source code of this package through the default editor, and then you can see all the parameters of this package.

Through these two methods, you can see that the `fcitx5-rime` package has the following input parameters, which can all be modified by `override`:

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

Instead of override the function's parameters, we can also override the attributes of the Derivation created by `stdenv.mkDerivation`.

Take `pkgs.hello` as an example, first check the source code of this package through the method we mentioned earlier:

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

The attributes showed above, such as `pname` `version` `src` `doCheck`, can all be overridden by `overrideAttrs`, for example:

```nix
helloWithDebug = pkgs.hello.overrideAttrs (finalAttrs: previousAttrs: {
  doCheck = false;
});
```

Here we use `overrideAttrs` to override `doCheck`, while other attributes remain their original values.

Some default attributes defined in `stdenv.mkDerivation` can also be overridden by `overrideAttrs`, for example:

```nix
helloWithDebug = pkgs.hello.overrideAttrs (finalAttrs: previousAttrs: {
  separateDebugInfo = true;
});
```

The attribute we override here, `separateDebugInfo`, is defined in `stdenv.mkDerivation`, not in the source code of `hello`.
We can check the source code of `stdenv.mkDerivation` to see all the attributes defined in it by using `nix repl '<nixpkgs>'` and then enter `:e stdenv.mkDerivation`.

### 3. Overlays

> [Chapter 3. Overlays - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overlays)

The `override` we introduced previously will generate a new Derivation, which does not affect the original Derivation in `pkgs`, and is only suitable for use as a local parameter,
if you need to override a Derivation that is also depended on by other Nix packages, then other Nix packages will still use the original Derivation.

To solve this problem, Nix provides the ability to use `overlays`. Simply put, `overlays` can globally modify the Derivation in `pkgs`.

In the classic Nix environment, Nix automatically applies all `overlays` configuration under the paths `~/.config/nixpkgs/overlays.nix` `~/.config/nixpkgs/overlays/*.nix`,
but in Flakes, in order to ensure the reproducibility of the system, it cannot depend on any configuration outside the Git repository, so this classic method cannot be used now.

When using Flakes to write configuration for NixOS, home Manager and NixOS both provide the `nixpkgs.overlays` option to define `overlays`, related documentation:

- [home-manager docs - `nixpkgs.overlays`](https://nix-community.github.io/home-manager/options.html#opt-nixpkgs.overlays)
- [nixpkgs source code - `nixpkgs.overlays`](https://github.com/NixOS/nixpkgs/blob/30d7dd7e7f2cba9c105a6906ae2c9ed419e02f17/nixos/modules/misc/nixpkgs.nix#L169)

For example, the following content is a Module that loads Overlays, which can be used as either a home Manager Module or a NixOS Module, because the two definitions are exactly the same:

> home Manager is an external component after all, and most people use the unstable branch of home Manager & nixpkgs, which sometimes causes problems with home Manager Module, so it is recommended to import `overlays` in a NixOS Module.

```nix
{ config, pkgs, lib, ... }:

{
  nixpkgs.overlays = [
    # overlayer1 - use self and super to express the inheritance relationship
    (self: super: {
     google-chrome = super.google-chrome.override {
       commandLineArgs =
         "--proxy-server='https=127.0.0.1:3128;http=127.0.0.1:3128'";
     };
    })

    # overlayer2 - you can also use `extend` to inherit other overlays
    # use `final` and `prev` to express the relationship between the new and the old
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

    # overlay3 - define overlays in other files
    # here the content of overlay3.nix is the same as above:
    #   `final: prev: { xxx = prev.xxx.override { ... }; }`
    (import ./overlays/overlay3.nix)
  ];
}
```

refer to this example to write your own overlays, import the configuration as a NixOS Module or a home Manager Module, and then deploy it to see the effect.

#### Modular overlays

The previous example shows how to write overlays, but all overlays are written in a single nix file, which is a bit difficult to maintain.

To resolve this problem,here is a best practice of how to manage overlays in a modular way.

First, create an `overlays` folder in the Git repository to store all overlays configuration, and then create `overlays/default.nix`, whose content is as follows:

```nix
args:
  # import all nix files in the current folder, and execute them with args as parameters
  # The return value is a list of all execution results, which is the list of overlays
  builtins.map
  (f: (import (./. + "/${f}") args))  # the first parameter of map, a function that import and execute a nix file
  (builtins.filter          # the second parameter of map, a list of all nix files in the current folder except default.nix
    (f: f != "default.nix")
    (builtins.attrNames (builtins.readDir ./.)))
```

Then you can write all overlays configuration in the `overlays` folder, an example configuration `overlays/fcitx5/default.nix` is as follows:

```nix
# to add my custom input method, I override the default rime-data here
# refer to https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix
{pkgs, config, lib, ...}:

(self: super: {
  # my custom input method's rime-data, downloaded from https://flypy.com
  rime-data = ./rime-data-flypy;
  fcitx5-rime = super.fcitx5-rime.override { rimeDataPkgs = [ ./rime-data-flypy ]; };
})
```

I custom the `rime-data` package through the overlay shown above.

At last, you need to load all overlays returned by `overlays/default.nix` through the `nixpkgs.overlays` option, add the following parameter to any NixOS Module to achieve this:

```nix
{ config, pkgs, lib, ... } @ args:

{
  # ......

  # add this parameter
  nixpkgs.overlays = import /path/to/overlays/dir;

  # ......
}
```

For example, you can just add it directly in `flake.nix`:

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

          # add the following inline module definition
          #   here, all parameters of modules are passed to overlays
          (args: { nixpkgs.overlays = import ./overlays args; })

          # ......
        ];
      };
    };
  };
}
```

By using this modular approach, it is very convenient to modularize all your overlays. Taking my configuration as an example, the structure of the `overlays` folder is roughly as follows:

```nix
.
├── flake.lock
├── flake.nix
├── home
├── hosts
├── modules
├── ......
├── overlays
│   ├── default.nix         # it returns a list of all overlays.
│   └── fcitx5              # fcitx5 overlay
│       ├── default.nix
│       ├── README.md
│       └── rime-data-flypy  # my custom rime-data
│           └── share
│               └── rime-data
│                   ├── ......  # rime-data files
└── README.md
```

## Advanced Usage

After becoming familiar with the Nix toolchain, you can further explore Nix's three manuals to discover more ways to use it:

- [Nix Reference Manual](https://nixos.org/manual/nix/stable/package-management/profiles.html): A guide to the Nix package manager, which mainly covers the design of the package manager and instructions for using it from the command line.
- [nixpkgs Manual](https://nixos.org/manual/nixpkgs/unstable/): A manual that introduces parameters of Nixpkgs, how to use, modify, and package Nix packages.
- [NixOS Manual](https://nixos.org/manual/nixos/unstable/): A user manual for NixOS, mainly including configuration instructions for system-level components such as Wayland/X11 and GPU.
- [nix-pills](https://nixos.org/guides/nix-pills): Nix Pills provides an in-depth explanation of how to use Nix to build software packages. It is written in a clear and understandable way and is worth reading, as it is also sufficiently in-depth.

After becoming familiar with Flakes, you may want to try some advanced techniques. Here are some popular community projects to try:

- [flake-parts](https://github.com/hercules-ci/flake-parts): Simplify the writing and maintenance of configuration through the Module module system.
- [flake-utils-plus](https://github.com/gytis-ivaskevicius/flake-utils-plus): A third-party package for simplifying Flake configuration, which is apparently more powerful.
- [digga][digga]: A large and comprehensive Flake template that combines the functionality of various useful Nix toolkits, but has a complex structure and requires some experience to navigate.
- etc.

And many other useful community projects to explore, here are some of them:

- [dev-templates](https://github.com/the-nix-way/dev-templates): Dev environments for numerous languages based on Nix flakes.
- [devenv](https://github.com/cachix/devenv): development environment management
- [agenix](https://github.com/ryantm/agenix): secrets management
- [colmena](https://github.com/zhaofengli/colmena): NixOS deployment tools
- [nixos-generator](https://github.com/nix-community/nixos-generators): generate iso/qcow2/... from nixos configuration
- [lanzaboote](https://github.com/nix-community/lanzaboote): enable secure boot for NixOS
- [impermanence](https://github.com/nix-community/impermanence): used to make NixOS stateless, to imporve the reproduciability of NixOS system.

## When will flakes stablized {#when-will-flakes-stablized}

Throughout so much content of this post, I've introduced in detail how to start using Flakes to configure NixOS, but at the beginning of this post we mentioned that **Flakes is still an experimental feature, which is worrying**. If Flakes is greatly changed or even removed, we may need to spend a lot of time to migrate the configuration.

In fact this is also one of the most concerned issues in the entire NixOS community, **when will Flakes become a stable feature**?

I dived into some details about flakes:

- https://github.com/NixOS/rfcs/pull/136: A plan to stabilize Flakes and the new CLI incrementally, still WIP.
- https://discourse.nixos.org/t/why-are-flakes-still-experimental/29317: A post, Why are flakes still experimental?
- https://grahamc.com/blog/flakes-are-an-obviously-good-thing/: Flakes are such an obviously good thing... but the design and development process should be better.
- https://nixos-foundation.notion.site/1-year-roadmap-0dc5c2ec265a477ea65c549cd5e568a9： A roadmap of nixos fundation, which includes plan about the stabilization of flakes.

After reading all of these, I feel like that flakes will eventually be stabilized in one or two years, with some important breaking changes.

The benefits of Flakes are obvious, and the entire NixOS community likes it very much. Currently, more than half of the users are using Flakes (especially new users in the NixOS community), so we can be sure that Flakes will never be deprecated.

But currently Flakes still has many problems, and it is likely to introduce some breaking changes in the process of stablizing it, and it's currently uncertain how greatly the breaking changes will be.

So overall, I still recommend everyone to use Flakes, but be prepared for the problems that may be caused by the upcomming breaking changes.

## References

The feedback and discussion of this post is mainly on [this Reddit post](https://www.reddit.com/r/NixOS/comments/13dxw9d/nixos_nix_flakes_a_guide_for_beginners/), you can also comment directly at the bottom of this page.

Here are some useful resources that I referred to:

- [Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems]: A beginner-friendly Nix Flakes tutorial that is worth reading.
- [NixOS series](https://lantian.pub/en/article/modify-website/nixos-why.lantian/): LanTian's NixOS series, which are very clear and easy to understand.
- [Nix Flakes Series](https://www.tweag.io/blog/2020-05-25-flakes/): An official Nix Flakes tutorial series, which provides a relatively detailed introduction and is suitable for beginners.
- [Flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes): The official Nix Flakes wiki, which provides a relatively rough introduction.
- [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config): My Flake for NixOS & macOS.

[digga]: https://github.com/divnix/digga
[New Nix Commands]: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix.html
[Zero to Nix - Determinate Systems]: https://github.com/DeterminateSystems/zero-to-nix
