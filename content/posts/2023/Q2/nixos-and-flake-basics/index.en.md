---
title: "NixOS & Nix Flakes - A Guide for Beginners"
date: 2023-05-10T21:23:28+08:00
lastmod: 2023-05-10T21:23:28+08:00
draft: false

resources:
- name: "featured-image"
  src: "screenshot_2023-05-07-21-21.webp"

tags: ["NixOS", "Nix", "Flakes", "Linux", "DevOps"]
categories: ["tech"]

lightgallery: true

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

>As of 2023-05-10, I have only used the NixOS for about 20 days, so there will inevitably be some mistakes and omissions in this article, please read it carefully. 
I will continue to try my best to repair and improve the content in the future, hope you like it, also eager to get any feedback~

> The target NixOS version of this article is 22.11, and the Nix version is 2.15.0. In this environment, Nix Flakes is still an experimental feature.

>You need to have some Linux experience and programming experience to play with NixOS & Nix Flakes, so I don't recommend NixOS for any Linux beginners.

## 0. Why Nix

I heard about the Nix package manager several years ago. It uses [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) to manage system dependencies, and the Linux distribution build on top of it can roll back to any historical state at any time. Although it sounds impressive, it requires learning a new language and writing code to install packages, I thought it was too troublesome and didn't study it at the time.

But recently I encountered two troublesome things when migrating the system, which made me decide to try Nix.

The fist problem was installing EndeavourOS (a derivative distribution of Arch Linux) on a newly assembled PC. Because My old PC also uses EndeavourOS, I directly `rsync` the old PC's Home directory to the new PC to save time after installation.
However, this synchronization caused a problem. All functions worked normally, but video playback always stuck. Firefox, Chrome, and MPV would all get stuck. I searched various resources online but could not solve the problem until I realized it might be caused by the Home directory synchronization. After clearing the Home directory, the problem was solved immediately... Later, I spent a long time recovering things from the old PC one by one.

The second problem is that I recently wanted to try Wayland, so I changed the desktop from i3wm to sway. 
However, because there was little difference between the two and many inconveniences (hidpi, Sway configuration tuning, etc.), I decided to switch back to i3wm. 
After switching back, GUI programs such as Firefox and Thunar would always get stuck for about a minute after the system started...

I was too tired to deal with the second problem, after thinking about it carefully, I realized that the root cause was that the system did not have any version control and rollback mechanism, which caused the system to be unable to be restored when problems occurred. 
And another problem, when installing a new system, I had to manually export the package list from the old machine and then install them on the new machine.
So I decided to switch to NixOS, and spent half a month studying Nix and Flakes before finally switching from EndeavourOS to NixOS on my PC.


The first step I took was to create a NixOS virtual machine in my Homelab, and debug step by step in this virtual machine to migrate my old PC's EndeavourOS i3 configuration to NixOS + Flakes and restore the entire desktop environment.

Once I had it working on the virtual machine, the rest was easy. I simply backed up my Home directory and software list from my work computer, reinstalled the system as NixOS, git cloned my debugged NixOS configuration, made some adjustments to the disk mounting parameters and added some extra NixOS configurations for my Nvidia graphics card. Finally, with just a few commands, I deployed the configuration and was able to restore the entire i3 desktop environment and my commonly used software on my fresh NixOS system. It was a truly satisfying moment!

The rollback capability of NixOS gave me a lot of confidence - I no longer fear breaking the system. So a few days ago, I further migrated to the hyprland desktop, which is indeed much better than i3, and I love its animation effects! (On EndeavourOS before, I wouldn't have dared to make such a switch for the reasons mentioned earlier - it would have been a big hassle if something went wrong with the system.)

>Note: some friends on V2EX gave feedback that `btrfs`'s snapshot feature can also provide similar rollback capabilities, and it is much simpler. After some research, I found that to be true. `btrfs` can even be configured to boot from a snapshot using GRUB(just like the NixOS does). So if you only want the system rollback capability, then btrfs based snapshot tools(e.g. [btrbk](https://github.com/digint/btrbk)) is also a good choice. Or if you're still interested in Nix, It is definitely worth learning, as Nix's capabilities are far beyond just system snapshots.

{{< figure src="./screenshot_2023-05-07-21-21.webp" caption="My NixOS Desktop" >}}

Now that the background information is out of the way, it's time to dive into the world of Nix!

## I. Introduction to Nix

Nix package manager is a declarative configuration management tool similar to plulumi/terraform/kubernetes that are currently popular in the DevOps field. Users need to declare the expected system state using [DSL](https://en.wikipedia.org/wiki/Domain-specific_language), and Nix is responsible for achieving that goal. The difference is that Nix manages software packages, while plulumi/terraform manages cloud resources.

>To put it simply, "declarative configuration" means that users only need to declare the results they want. For example, you declares that you want to replace the i3 window manager with sway, then Nix will help you achieve the goal. You don't need to worry about the underlying details (such as which packages sway needs to install, which i3-related packages need to be uninstalled, which system configurations or environment variables need to be adjusted for sway, what adjustments need to be made to the Sway parameters if an Nvidia graphics card is used, etc.), Nix will automatically handle these details for the user(prerequisite: if the sway's nix packages are designed properly...).

The Linux distribution built on top of the Nix package manager, NixOS, can be simply described as "OS as Code", which describes the entire operating system's state using declarative Nix configuration files.

NixOS's configuration only manages the system-level state, the user's HOME directory is not under its control. Another important community project, [home-manager](https://github.com/nix-community/home-manager), filled this gap, home-manager designed to managing user-level's packages & HOME directories. **By combining home-manager with NixOS and Git, a fully reproducible and rollbackable system environment can be obtained**.

Due to Nix's declarative and reproducible features, Nix is not only used to manage desktop environments but also widely used to manage development and compilation environments, cloud virtual machines, and container image construction. [NixOps](https://github.com/NixOS/nixops) from the Nix official and [deploy-rs](https://github.com/serokell/deploy-rs)  from the community are both operations tools based on Nix.

>Since there are numerous files in the home directory with varying behaviors, it is impossible to version control all of them due to the high cost. Generally, only some important configuration files are managed using home-manager, and other files that need to be backed up can be backed up and synchronized using rsync/synthing, or use tools like [btrbk](https://github.com/digint/btrbk) to take snapshots of the home directory.

### Advantages of Nix

- **Declarative configuration, Environment as Code**, can be managed with Git. As long as the configuration files are not lost, the system can be restored to any historical state at any time(ideally).
  - Nix lock dependent library versions through a lock file named `flake.lock`, to ensure that the system is reproducible, this idea actually borrows from some package managers such as npm, cargo, etc.
  - Compared with Docker, Nix provides a much stronger guarantee for the reproducibility of build results, because Dockerfile is actually an imperative configuration and there is no such thing as `flake.nix` in Docker, Docker's reproducibility relys on share the build result(which is MUCH MORE LARGAR than Dockerfile itself) through image regitry(e.g. DockerHub).
- **Highly convenient system customization capability**
  - By changing a few lines of configuration, various components of the NixOS system can be easily customized. This is because Nix encapsulates all the underlying complex operations in nix packages and only exports concise and necessary declarative parameters.
  - Moreover, this modification is very safe. An example is that one NixOS user on the V2EX forum have stated that "[**on NixOS, switching between different desktop environments is very simple and clean, and it is very safe. I often switch between gnome/kde/sway.**](https://www.v2ex.com/t/938569#r_13053251)"
- **Rollback**: The system can be rolled back to any historical environment at any time, and NixOS even adds all old versions to the boot options by default to ensure that the system can be rolled back at any time even though it crashes. Therefore, NixOS is also considered one of the most stable Linux Systems.
- **No dependency conflicts**: Because each software package in Nix has a unique hash, its installation path also includes this hash value, so multiple versions can coexist.
- **The community is very active, and there are quite a few third-party projects**. The official package repository, nixpkgs, has many contributors, and many people share their Nix configurations on Github/Gitlab. After browsing through it, the entire ecosystem gives me a sense of excitement in discovering a new continent.

{{< figure src="./nixos-bootloader.avif" caption="All historical versions are listed in the boot options of NixOS. Image from [NixOS Discourse - 10074](https://discourse.nixos.org/t/how-to-make-uefis-grub2-menu-the-same-as-bioss-one/10074)" >}}

### Disadvantages of Nix

- **Relatively high learning curve:**: If you want the system to be completely reproducible and avoid pitfalls caused by improper use, you need to learn about the entire design of Nix and manage the system in a declarative manner. You cannot blindly use `nix-env -i` (which is similar to `apt-get install`).
- **Chaotic documentation**: Firstly, Nix Flakes is still an experimental feature, and there are currently relatively few documents introducing it. Secondly, most of the Nix community's documentation only introduces the old `nix-env`/`nix-channel`. If you want to start learning Nix directly from Nix Flakes, you need to refer to a large number of old documents and extract what you need from them. In addition, some of Nix's current core functions are not well-documented (such as `imports` and Nixpkgs Module System), so it is best to look at the source code to understand them.
- ~~Relatively few packages~~: Retract this one. The official claim is that nixpkgs has [80000+](https://search.nixos.org/packages) packages, and indeed, most packages can be found in nixpkgs.
- **Relatively high disk space usage**: To ensure that the system can be rolled back at any time, Nix preserves all historical environments by default, which can take up a lot of disk space. Although you can manually clean up old historical environments periodically with `nix-collect-garbage`, it is still recommended to buy a larger hard drive.

### Summary

Generally speaking, I think NixOS is suitable for developers who have a certain amount of Linux usage experience and programming experience and want to have more control over their systems. 

Another info, there is also some competition between Nix and the relatively popular [Dev Containers](https://containers.dev/) in the construction of development environment, and the specific differences between them have yet to be explored by me~


## II. Installation

Nix can be installed in multiple ways and supports being installed on MacOS/Linux/WSL as a package manager. Nix also provides NixOS, a Linux distribution that uses Nix to manage the entire system environment.

I chose to directly install NixOS system using its ISO image, to manage the entire system environment through Nix as much as possible.

The installation process is simple, and I won't go into details here.

some reference materials that maybe useful:

1. [Official installation method of Nix](https://nixos.org/download.html): written in bash script, `nix-command` & `flakes` are still experimental features as of 2023-04-23, and need to be manually enabled.
   1. You need to refer to the instructions in [Enable flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) to enable `nix-command` & `flakes`.
   2. The official installer does not provide any uninstallation method. To uninstall Nix on Linux/MacOS, you need to manually delete all related files, users, and groups.
2. [The Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer): a third-party installer written in Rust, which enables `nix-command` & `flakes` by default and provides an uninstallation command.

## III. Nix Flakes and the old Nix

In 2020, Nix introduced two new features, `nix-command` and `flakes`, which provide new command-line tools, standard Nix package structure definitions, and `flake.lock` version lock files similar to cargo/npm. These two features greatly enhance the capabilities of Nix. Although they are still experimental features as of 2023-05-05, they have been widely used by the Nix community and are strongly recommended.

Currently, most of the Nix community's documentation still only covers traditional Nix and does not include Nix Flakes-related content. However, from the perspective of reproducibility and ease of management and maintenance, the old Nix package structure and command-line tools are no longer recommended for use. Therefore, this document will not introduce the usage of the old Nix package structure and command-line tools, and it is recommended that beginners ignore these old contents and just start with `nix-command` & `flakes`.

Here are the old Nix command-line tools and related concepts that are no longer needed in `nix-command` and `flakes`. When searching for information, you can safely ignore them:

1. `nix-channel`: `nix-channel` is similar to other package management tools such as apt/yum/pacman, managing software package versions through stable/unstable/test channels. 
   1. In Nix Flakes, the functionality of `nix-channel` is completely replaced by `inputs` in `flake.nix` to declare dependency sources and `flake.lock` to lock dependency versions.
2. `nix-env`: `nix-env` is a core command-line tool for traditional Nix used to manage software packages in the user environment. It installs software packages from the data sources defined by `nix-channel`, so the installed package versions are influenced by the channel. Packages installed with `nix-env` are not automatically recorded in Nix's declarative configuration and are entirely outside of its control, making them difficult to reproduce on other machines. Therefore, it is not recommended to use this tool.
   1. The corresponding command in Nix Flakes is `nix profile`.
3. `nix-shell`: `nix-shell` is used to create a temporary shell environment.
   1. In Nix Flakes, it is replaced by `nix develop` and `nix shell`.
4. `nix-build`: `nix-build` is used to build Nix packages, and it places the build results in the `/nix/store` path, but it does not record them in Nix's declarative configuration.
   1. The corresponding command in Nix Flakes is `nix build`.
5. ...

>maybe `nix-env -qa` is still useful some times, which returns all packages installed in the System.

## IV. NixOS Flakes Package Repositories

Similar to Arch Linux, Nix also has official and community software package repositories:

1. [nixpkgs](https://github.com/NixOS/nixpkgs) is a Git repository containing all Nix packages and NixOS modules/configurations. Its master branch contains the latest Nix packages and NixOS modules/configurations.
2. [NUR](https://github.com/nix-community/NUR) is similar to Arch Linux's AUR. NUR is a third-party Nix package repository and serves as a supplement to nixpkgs.
3. Nix Flakes can also install software packages directly from Git repositories, which can be used to install Flakes packages provided by anyone.


## V. Nix language basics

The Nix language is used to declare packages and configurations to be built by Nix, if you want to play NixOS and Nix Flakes and enjoy the many benefits they bring, you must learn the basics of this language first.

Nix is a relatively simple functional language, if you already have some programming experiences, it should take less than 2 hours to go through these grammars.

Please read [**Nix language basics - nix.dev**](https://nix.dev/tutorials/first-steps/nix-language) to get a basic understanding of Nix language now, it's a very good tutorial.


## VI. Managing the system declaratively

> https://nixos.wiki/wiki/Overview_of_the_NixOS_Linux_distribution

After learning the basics of the Nix language, we can start using it to configure the NixOS system. The system configuration file for NixOS is located at `/etc/nixos/configuration.nix`, which contains all the declarative configurations for the system, such as time zone, language, keyboard layout, network, users, file system, boot options, etc.

If we want to modify the system state in a reproducible way (which is also the most recommended way), we need to manually edit the `/etc/nixos/configuration.nix` file, and then execute `sudo nixos-rebuild switch` to apply the configuration. This command generates a new system environment based on the configuration file, sets the new environment as the default one, and also preserves & added the previous environment into the grub boot options. This ensures we can always roll back to the old environment(even if the new environment fails to start).

On the other hand, `/etc/nixos/configuration.nix` is the traditional Nix configuration method, which relies on data sources configured by `nix-channel` and has no version locking mechanism, making it difficult to ensure the reproducibility of the system. **A better approach is to use Nix Flakes**, which can ensure the reproducibility of the system and make it easy to manage the configuration.

Now first, let's learn how to manage the system using the default configuration method of NixOS through `/etc/nixos/configuration.nix`, and then transition to the more advanced Nix Flakes.

### 1. Configuring the system using `/etc/nixos/configuration.nix`

As mentioned earlier, this is the traditional Nix configuration method and also the default configuration method currently used by NixOS. It relies on data sources configured by `nix-channel` and has no version locking mechanism, making it difficult to ensure the reproducibility of the system.

For example, to enable ssh and add a user "ryan," simply add the following configuration to `/etc/nixos/configuration.nix`:

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

in the configuration above, we enabled the openssh service, added an ssh public key for the user ryan, and disabled password login.

Now, running `sudo nixos-rebuild switch` deploys the modified configuration, and then we can login to the system using ssh with ssh keys.

This is the default declarative system configuration in NixOS, where any reproducible changes to the system can be made by modifying the `/etc/nixos/configuration.nix` file and deploying the changes by running `sudo nixos-rebuild switch`.

All configuration options in `/etc/nixos/configuration.nix` can be found in the following places:

- By searching on Google, such as `Chrome NixOS`, which will provide NixOS informations related to Chrome. Generally, the NixOS Wiki and the nixpkgs repository source code will be among the top results.
- By searching for keywords in [NixOS Options Search](https://search.nixos.org/options).
- For system-level configurations, relevant documentation can be found in [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration).
- By searching for keywords directly in the [nixpkgs](https://github.com/NixOS/nixpkgs) repository and reading relevant source code.


### 2. Enabling NixOS Flakes Support

Compared to the default configuration approach of NixOS, Nix Flakes provide better reproducibility and a clearer package structure that is easier to maintain. Therefore, it is recommended to use Nix Flakes to manage system configurations.

However, Nix Flakes is currently an experimental feature and is not yet enabled by default. We need to enable it manually by modifying the `/etc/nixos/configuration.nix`, example:

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

  # omit the previous configuration.......

  # enable Nix Flakes and the new nix-command command line tool
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  environment.systemPackages = with pkgs; [
    # Nix Flakes uses the git command to pull dependencies from data sources, so git must be installed first
    git
    vim
    wget
  ];

  # omit the rest of the configuration.......
}
```

Now run `sudo nixos-rebuild switch` to apply the changes, and then you can use Nix Flakes to manage the system configuration.


### 3. Switching System Configuration to `flake.nix`

After enabling the Nix Flakes feature, the `sudo nixos-rebuild switch` command will prioritize reading the `/etc/nixos/flake.nix` file. If not found, it will fallback to `/etc/nixos/configuration.nix`.

Now let's use the official flake templates provided by Nix to learn how to write flakes, check which templates are available using the following command:

```bash
nix flake show templates
```

One of the templates, `templates#full`, shows all possible uses., take a look at its contents:

```bash
nix flake init -t templates#full
cat flake.nix
```


Now create a file `/etc/nixos/flake.nix` and write the configuration content according to the template above.
All system modifications will be taken over by Nix Flakes from now on. An example configuration is shown below:

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
      # to avoid problems caused by different versions of nixpkgs dependencies.
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  # `outputs` are all the build result of the flake. 
  # A flake can have many use cases and different types of outputs.
  # parameters in `outputs` are defined in `inputs` and can be referenced by their names. 
  # However, `self` is an exception, This special parameter points to the `outputs` itself (self-reference)
  # The `@` syntax here is used to alias the attribute set of the inputs's parameter, making it convenient to use inside the function.
  outputs = { self, nixpkgs, ... }@inputs: {
    # Outputs named `nixosConfigurations` is used by execute `nixos-rebuild switch --flake /path/to/flakes/directory` on NixOS System.
    nixosConfigurations = {
      # By default, NixOS will try to refer the nixosConfiguration with its hostname.
      # so the system named `nixos-test` will use this configuration.
      # However, the configuration name can also be specified using `nixos-rebuild switch --flake /path/to/flakes/directory#<name>`.
      # The `nixpkgs.lib.nixosSystem` function is used to build this configuration, the following attribute set is its parameter.
      # Run `nixos-rebuild switch --flake .#nixos-test` in the flake's directory to deploy this configuration on any NixOS system
      "nixos-test" = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # The Nix module system can modularize configurations, improving the maintainability of configurations.
        #
        # Each parameter in the `modules` is a Nix Module, and there is a partial introduction to it in the nixpkgs manual:
        #    <https://nixos.org/manual/nixpkgs/unstable/#module-system-introduction>
        # It is said to be partial because the documentation is not complete, only some simple introductions
        #    (such is the current state of Nix documentation...)
        # A Nix Module can be an attribute set, or a function that returns an attribute set.
        # If a Module is a function, according to the Nix Wiki description, this function can have up to four parameters:
        # 
        #   config: The configuration of the entire system
        #   options: All option declarations refined with all definition and declaration references.
        #   pkgs: The attribute set extracted from the Nix package collection and enhanced with the nixpkgs.config option.
        #   modulesPath: The location of the module directory of Nix.
        #
        # Only these four parameters can be passed by default.
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

Here we define a NixOS system called `nixos-test`, whose configuration file is `./organization.nix`, which is our previous configuration file, so we can still use the old configuration.

Now execute the `sudo nixos-rebuild switch` command to apply the configuration, and there should be no change to the system, because we just switch to Nix Flakes, and the actual configuration content is the same as before.


### 4. Add Custom Cache Mirror

In order to speed up package building, Nix provides <https://cache.nixos.org> to cache build results to avoid build every packages locally.

In the old NixOS configuration, other cache sources can be added through `nix-channel` command, but Nix Flakes avoids using any system-level configuration and environment variables as far as possible to ensure that its build results are not affected by the environment(environment independent). 
Therefore, in order to customize the cache image source, we must add the related configuration in `flake.nix` by using the parameter `nixConfig`. The example is as follows:

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

After the modification, execute `sudo nixos-rebuild switch` to apply the configuration. 

### 5. install home-manager

We mentioned earlier that NixOS can only manage system-level configurations, and user-level configurations need to be managed using home-manager.

According to the official document [Home Manager Manual](https://nix-community.github.io/home-manager/index.htm), in order to install home-manager as an module of NixOS, we need to create `/etc/nixos/home.nix` first, an example content shown below:

```nix
{ config, pkgs, ... }:

{
  # please change the username & home direcotry to your own
  home.username = "ryan";
  home.homeDirectory = "/home/ryan";

  # link the configuration file in current directory to the specified location in Home directory
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
    pkgs.htop
    pkgs.btop
  ];

  # enable starship, a beautiful shell prompt
  programs.starship = {
    enable = true;
    settings = {
      add_newline = false;
      aws.disabled = true;
      gcloud.disabled = true;
      line_break.disabled = true;
    };
  };

  # alacritty terminal emulator
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


After adding `/etc/nixos/home.nix`, you need to import this new configuration file in `/etc/nixos/flake.nix` to make it effective, use the following command to generate an example `/etc/nixos/flake.nix` in the current folder for reference:

```shell
nix flake new -t github:nix-community/home-manager#nixos
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
      # please change the hostname to your own
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

            # replace ryan with your own username
            home-manager.users.ryan = import ./home.nix;

            # Optionally, use home-manager.extraSpecialArgs to pass
            # arguments to home.nix
          }
        ];
      };
    };
  };
}
```


Then execute `sudo nixos-rebuild switch` to apply the configuration, and home-manager will be installed automatically.

After the installation is complete, all user-level programs and configurations can be managed through `/etc/nixos/home.nix`, and when executing `sudo nixos-rebuild switch`, the configuration of home-manager will be applied automatically.

To find the options of home-manager used in `home.nix`, use the following methods:

- [Home Manager - Appendix A. Configuration Options](https://nix-community.github.io/home-manager/options.html): A list of all options, it is recommended to search for keywords in it.
- [home-manager](https://github.com/nix-community/home-manager): Some options are not listed in the official documentation, or the documentation is not clear enough, you can directly search and read the corresponding source code in this home-manager repo.

### 6. Modular NixOS configuration

At this point, the skeleton of the entire system is basically configured. The current system configuration structure in `/etc/nixos` should be as follows:

```
$ tree
.
├── flake.lock
├── flake.nix
├── home.nix
└── configuration.nix
```

The functions of these four files are explained below:

- `flake.lock`: An automatically generated version lock file, which records all input data sources, hash values, and version numbers of the entire flake to ensure that the system is reproducible.
- `flake.nix`: The entry file, which will be recognized and deployed when executing `sudo nixos-rebuild switch`.
  - See [Flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes) for all options of flake.nix.
- `configuration.nix`: Imported as a Nix module in flake.nix, all system-level configurations are currently written in this file.
  - See [Configuration - NixOS Manual](https://nixos.org/manual/nixos/unstable/index.html#ch-configuration) for all options of configuration.nix.
- `home.nix`: Imported by home-manager as the configuration of the user `ryan` in flake.nix, that is, it contains all the Home Manager configurations of `ryan`, and is responsible for managing `ryan`'s Home folder.
  - See [Appendix A. Configuration Options - Home Manager](https://nix-community.github.io/home-manager/options.html) for all options of home.nix.


By modifying the above configuration files, you can change the status of the system and the Home directory declaratively.

As the configuration increases, it is difficult to maintain the configuration files by relying solely on `configuration.nix` and `home.nix`. Therefore, a better solution is to use the module mechanism of Nix to split the configuration files into multiple modules and write them in a classified manner.

`imports` parameter can accept a list of `.nix` files, and merge all the configurations in the list into the current attribute set. Note that the word used here is "**merge**", which means that `imports` will NOT simply overwrite the duplicate configuration items, but handle them more reasonably. For example, if I define `program.packages = [...]` in multiple modules, then `imports` will merge all `program.packages` in all modules into one list. Not only lists can be merged correctly, but attribute sets can also be merged correctly. The specific behavior can be explored by yourself.

>I only found a description of `imports` in [nixpkgs-unstable official manual - evalModules parameters](https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules-parameters): `A list of modules. These are merged together to form the final configuration.`, you can try to understand it... 

With the help of the `imports` parameter, we can split `home.nix` and `configuration.nix` into multiple `.nix` files.

For example, the structure of my previous i3wm system configuration [ryan4yin/nix-config/v0.0.2](https://github.com/ryan4yin/nix-config/tree/v0.0.2) is as follows:

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

For the details of the structure and content, please go to the github repository [ryan4yin/nix-config/v0.0.2](https://github.com/ryan4yin/nix-config/tree/v0.0.2).

### 7. Update the system

After using Nix Flakes, it is also very simple to update the system. First update the flake.lock file, and then deploy it. Execute the following command in the configuration folder:

```shell
# update flake.lock
nix flake update
# deploy the updates
sudo nixos-rebuild switch
```

Sometimes when installing new packages, you may encounter an error of sha256 mismatch when running `nixos-rebuild switch`. You can also try to solve it by updating `flake.lock` through `nix flake update`.

### 8. Rollback the version of some packages

After using Nix Flakes, most people are currently using the `nixos-unstable` branch of nixpkgs. Sometimes you will encounter some bugs, such as the [chrome/vscode crash problem](https://github.com/swaywm/sway/issues/7562)

To resolve this problem, we need to rollback the version of some packages. In Nix Flakes, all package versions and hash values are one-to-one corresponding to the git commit of their input data source. Therefore, to rollback a package to a historical version, we need to lock the git commit of its input data source.

So to rollback the version of some packages, first modify `/etc/nixos/flake.nix`, the example content is as follows (mainly using the `specialArgs` parameter):

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
      nixos-test = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";

        # The core parameter, which passes the non-default nixpkgs data source to other modules
        specialArgs = {
          inherit nixpkgs-stable;
          inherit nixpkgs-fd40cef8d;
        };
        modules = [
          ./hosts/nixos-test

          # omit other configurations...
        ];
      };
    };
  };
}
```

And then refer the packages from `nix-stable` or `nixpkgs-fd40cef8d` in your corresponding sub module, a home manager's sub module as an example:

```nix
{
  pkgs,
  config,
  # nix will search and jnject this parameter from specialArgs in flake.nix
  nixpkgs-stable,
  # nixpkgs-fd40cef8d,
  ...
}:

let
  # To use packages from nixpkgs-stable, we need to configure some parameters for it first
  pkgs-stable = import nixpkgs-stable {
    # The Global parameters will be automatically configured to the default pkgs, so we can directly refer to them from pkgs
    system = pkgs.system;
    # To use chrome, we need to allow the installation of non-free software
    config.allowUnfree = true;
  };
in {
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

After adjusted the configuration, deploy it with `sudo nixos-rebuild switch`, then your firefox/chrome/vscode will revert to the version corresponding to `nix-stable` or `nixpkgs-fd40cef8d`. 

### 9. Manage NixOS configuration with Git

NixOS's configuration file is plain text, so it can be managed with Git just like ordinary dotfiles.

On the other hand, `flake.nix` do not required to be placed in the `/etc/nixos` directory, they can be placed in any directory, as long as the correct path is specified during deployment.

For example, my usage is to place the Nix Flakes configuration in the `~/nixos-config` directory, and then create a soft link in the `/etc/nixos` directory:

```shell
sudo mv /etc/nixos /etc/nixos.bak  # backup the original configuration
sudo ln -s ~/nixos-config/ /etc/nixos

# deploy the flake.nix located at the default location(/etc/nixos)
sudo nixos-rebuild switch
```

And then you can use Git to manage the configuration in the `~/nixos-config` directory. The configuration can be used with ordinary user-level permissions, and it is not required to be owned by root.

Another method is to delete `/etc/nixos` directly, and specify the configuration file path each time you deploy:

```shell
sudo mv /etc/nixos /etc/nixos.bak
cd ~/nixos-config

# deploy the flake.nix located in the current directory
sudo nixos-rebuild switch --flake .
```

Choose whichever you like.


## VII. Usage of Nix Flakes


Up to now, we have written a lot of Nix Flakes configurations to manage the NixOS system. Here is a brief introduction to the more detailed content of Nix Flakes, as well as commonly used nix flake commands.

### 1. Flake outputs

the `outputs` in `flake.nix` are what a flake produces as part of its build. Each flake can have many different outputs simultaneously, including but not limited to:

- Nix packages: named `apps.<system>.<name>`, `packages.<system>.<name>`, or `legacyPackages.<system>.<name>`
- Nix Helper Functions: named `lib`., which means a library for other flakes.
- Nix development environments: named `devShell`
- NixOS configurations: named `nixosConfiguration`
- Nix templates: named `templates`
  - templates can be used by command `nix flake init --template <reference>`
- Other user defined outputs

### 2. Flake Command Line Usage

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

[Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems] is a brand new guide to get started with Nix & Flake, recommended to read for beginners.

## VIII. Nixpkgs's Advanced Usage

`callPackage`, `Overriding`, and `Overlays` are the techniques occasionally used when using Nix to customize the build method of Nix packages.

We know that many programs have a large number of build parameters that need to be configured, and different users may want to use different build parameters. This is where `Overriding` and `Overlays` come in handy. Let me give you a few examples I have encountered:

1. [`fcitx5-rime.nix`](https://github.com/NixOS/nixpkgs/blob/e4246ae1e7f78b7087dce9c9da10d28d3725025f/pkgs/tools/inputmethods/fcitx5/fcitx5-rime.nix): By default, `rimeDataPkgs` for `fcitx5-rime` uses the `rime-data` package, but this parameter can be customized using `override` to load custom rime configurations (such as loading the Xiaohe keyboard input method configuration).
2. [`vscode/with-extensions.nix`](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/editors/vscode/with-extensions.nix): This package for VS Code can also be customized by overriding the value of the `vscodeExtensions` parameter to install custom plugins.
    - [`nix-vscode-extensions`](https://github.com/nix-community/nix-vscode-extensions): This is a vscode plugin manager implemented using this parameter.
3. [`firefox/common.nix`](https://github.com/NixOS/nixpkgs/blob/416ffcd08f1f16211130cd9571f74322e98ecef6/pkgs/applications/networking/browsers/firefox/common.nix): Firefox also has many customizable parameters.
4. ...

In short, in order to customize the build parameters of Nix packages of this type, we need to use `Overriding` or `Overlays`.

### Overriding

>[Chapter 4. Overriding - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overrides)

Simply put, all Nix packages in nixpkgs can be customized with `<pkg>.override {}` to define some build parameters, which returns a new Derivation that uses custom parameters. For example:

```nix
pkgs.fcitx5-rime.override {rimeDataPkgs = [
    ./rime-data-flypy
  ];}
```

The result of executing the above Nix expression is a new Derivation, where the `rimeDataPkgs` parameter is overridden as `[./rime-data-flypy]`, while other parameters retain their original values.

In addition to overriding parameters, you can also override the attributes of a Derivation(condiftion: it's built using `stdenv.mkDerivation`) by using `overrideAttrs`. For example:

```nix
helloWithDebug = pkgs.hello.overrideAttrs (finalAttrs: previousAttrs: {
  separateDebugInfo = true;
});
```

In this example, `helloWithDebug` is a new Derivation, where the `separateDebugInfo` parameter is overridden as `true`, while other parameters retain their original values.

### Overlays

>refer [Chapter 3. Overlays - nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/#chap-overlays)

TODO I haven't fully understood this part yet

## IX. Nix Packaging

>refer: [NixOS Series 3: Software Packaging 101 - Lan Tian @ Blog](https://lantian.pub/en/article/modify-computer/nixos-packaging.lantian/)

TODO I haven't fully understood this part yet.

## Advanced Usage

After becoming familiar with the Nix toolchain, you can further explore Nix's three manuals to discover more ways to use it:

- [Nix Reference Manual](https://nixos.org/manual/nix/stable/package-management/profiles.html): A guide to the Nix package manager, which mainly covers the design of the package manager and instructions for using it from the command line.
- [nixpkgs Manual](https://nixos.org/manual/nixpkgs/unstable/): A manual that introduces parameters of Nixpkgs, how to use, modify, and package Nix packages.
- [NixOS Manual](https://nixos.org/manual/nixos/unstable/): A user manual for the NixOS system, mainly including configuration instructions for system-level components such as Wayland/X11 and GPU.
- [nix-pills](https://nixos.org/guides/nix-pills): Nix Pills provides an in-depth explanation of how to use Nix to build software packages. It is written in a clear and understandable way and is worth reading, as it is also sufficiently in-depth.

After becoming familiar with Nix Flakes, you can try some advanced techniques. Here are some popular community projects to try:

- [flake-parts](https://github.com/hercules-ci/flake-parts): Simplify the writing and maintenance of configuration through the Module module system.
- [flake-utils-plus](https://github.com/gytis-ivaskevicius/flake-utils-plus): A third-party package for simplifying Flake configuration, which is apparently more powerful.
- [devshell](https://github.com/numtide/devshell): As the name suggests.
- [digga][digga]: A large and comprehensive Flake template that combines the functionality of various useful Nix toolkits, but has a complex structure and requires some experience to navigate.
- etc.

## References

Here are some useful resources that I have referred to:

- [Zero to Nix - Determinate Systems][Zero to Nix - Determinate Systems]: A beginner-friendly Nix Flakes tutorial that is worth reading.
- [NixOS series](https://lantian.pub/en/article/modify-website/nixos-why.lantian/): LanTian's NixOS series, which are very clear and easy to understand, a must-read for beginners.
- [Nix Flakes Series](https://www.tweag.io/blog/2020-05-25-flakes/): An official Nix Flakes tutorial series, which provides a relatively detailed introduction and is suitable for beginners.
- [Nix Flakes - Wiki](https://nixos.wiki/wiki/Flakes): The official Nix Flakes wiki, which provides a relatively rough introduction.
- [ryan4yin/nix-config](https://github.com/ryan4yin/nix-config): My NixOS configuration repository, which also lists other configuration repositories that I have referred to in the README.


[digga]: https://github.com/divnix/digga
[New Nix Commands]: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix.html
[Zero to Nix - Determinate Systems]: https://github.com/DeterminateSystems/zero-to-nix
