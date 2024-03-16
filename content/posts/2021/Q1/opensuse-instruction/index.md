---
title: "openSUSE 使用指南"
date: 2021-01-04T08:42:21+08:00
draft: false

resources:
  - name: "featured-image"
    src: "linux-opensuse.webp"

tags: ["openSUSE", "Linux"]
categories: ["tech"]
---

openSUSE 是一个基于 RPM 的发行版，这和 RHEL/CentOS 一致。
但是它的官方包管理器是专有的 zypper，挺好用的，软件也很新。

我最近从 [Manjaro](/posts/manjaro-instruction/) 切换到了 openSUSE，发现 KDE 桌面确实比 Manjaro 更丝滑，而且社区源 OBS 体验下来比 AUR 更舒服。

<!--more-->

尤其是容器/Kubernetes 方面，源里面的东西比 AUR 更丰富，而且是官方维护的。
本文算是对迁移流程做的一个总结。

> 本文以 openSUSE Tumbleweed 为基础编写，这是一个和 Manjaro/Arch 一样的滚动发行版，软件源都很新。
> openSUSE 社区的大部分用户都是使用的 Tumbleweed.
> 它的硬件兼容性也要比 openSUSE Leap（稳定版）好——实测小米游戏本安装 Leap，休眠后 Touchpad 会失灵。

## 一、zypper 的基础命令

zypper 的源在国内比较慢，但实际上下载的时候，zypper 会智能选择最快的镜像源下载软件包，比如国内的清华源等。

但是我发现官方的源索引更新太慢，甚至经常失败。因此没办法，还是得手动设置镜像源：

```shell
# 禁用原有的官方软件源
sudo zypper mr --disable repo-oss repo-non-oss repo-update repo-update-non-oss repo-debug
# 添加北外镜像源
sudo zypper ar -fcg https://mirrors.bfsu.edu.cn/opensuse/tumbleweed/repo/oss/ bfsu-oss
sudo zypper ar -fcg https://mirrors.bfsu.edu.cn/opensuse/tumbleweed/repo/non-oss/ bfsu-non-oss
```

然后就是 zypper 的常用命令：

```shell
sudo zypper refresh  # refresh all repos
sudo zypper update   # update all software

sudo zypper search --installed-only  <package-name>  # 查找本地安装的程序
sudo zypper search <package-name>  # 查找本地和软件源中的程序

sudo zypper install <package-name>  # 安装程序
sudo zypper remove --clean-deps <package-name>  # 卸载程序，注意添加 --clean-deps 或者 -u，否则不会卸载依赖项！

sudo zypper clean  # 清理本地的包缓存
```

## Install Software

> 这里需要用到 [OBS(Open Build Service, 类似 arch 的 AUR，但是是预编译的包)](https://mirrors.openSUSE.org/list/bs.html)，因为 OBS 东西太多了，因此不存在完整的国内镜像，平均速度大概 300kb/s。
> 建议有条件可以在路由器上加智能代理提速。

安装需要用到的各类软件:

```shell
# 启用 Packman 仓库，使用阿里云镜像源
sudo zypper ar "http://mirrors.aliyun.com/packman/suse/openSUSE_Tumbleweed/" Packman

# install video player and web browser
sudo zypper install mpv ffmpeg-4 chromium firefox

# install screenshot and other utils
# 安装好后可以配个截图快捷键 alt+a => `flameshot gui`
sudo zypper install flameshot peek nomacs

# install git clang/make/cmake
sudo zypper install git gcc clang make cmake

# install wireshark
sudo zypper install wireshark
sudo gpasswd --add $USER wireshark  #  将你添加到 wireshark 用户组中
```

### IDE + 编程语言

```shell
# install vscode: https://en.openSUSE.org/Visual_Studio_Code
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo zypper addrepo https://packages.microsoft.com/yumrepos/vscode vscode
sudo zypper refresh
sudo zypper install code

# 安装 dotnet 5: https://docs.microsoft.com/en-us/dotnet/core/install/linux-openSUSE#openSUSE-15-
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo zypper addrepo https://packages.microsoft.com/openSUSE/15/prod/ microsoft-prod
sudo zypper refresh
sudo zypper install dotnet-sdk-5.0

# 安装新版本的 go（源中的版本比较低，更建议从 go 官网下载安装）
sudo zypper install go
```

通过 tarball/script 安装：

```shell
# rustup，rust 环境管理器
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# jetbrains toolbox app，用于安装和管理 pycharm/idea/goland/android studio 等 IDE
# 参见：https://www.jetbrains.com/toolbox-app/

# 不使用系统 python，改用 miniconda 装 python3.8
# 参考：https://github.com/ContinuumIO/docker-images/blob/master/miniconda3/debian/Dockerfile
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
sudo /bin/bash /tmp/miniconda.sh -b -p /opt/conda
rm /tmp/miniconda.sh
sudo /opt/conda/bin/conda clean -tipsy
sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
echo "conda activate base" >> ~/.bashrc
# miniconda 的 entrypoint 默认安装在如下目录，添加到 PATH 中
echo "export PATH=\$PATH:\$HOME/.local/bin" >> ~/.bashrc
```

接下来安装 VSCode 插件，下列是我的插件列表：

1. 语言：
   1. python/go/c#/julia/flutter
   2. c/c++ extension pack
   3. rust-analyzer
   4. shellchecker
   5. redhat xml & yaml
   6. even-better-toml
   7. edit-csv
   8. vscode-proto3
2. ansible/terraform
3. markdown all in one + Markdown Preview Enhanced
4. 美化：
   1. community material theme
   2. vscode icons
   3. glasslt-vsc
5. docker/kubernetes
6. IntelliJ IDEA Keybindings
7. gitlens
8. prettier
9. utils
   1. comment translate
   2. path intellisense
   3. svg
   4. visual studio intellicode
10. remote ssh + remote containers
11. rest client
12. vscode databases

### 容器 + Kubernetes

```shell
# 时髦的新容器套装: https://documentation.suse.com/sles/15-SP2/html/SLES-all/cha-podman-overview.html
sudo zypper in podman kompose skopeo buildah katacontainers
# 安装 kubernetes 相关工具，tumbleweed 官方仓库的包都非常新！很舒服
sudo zypper in helm k9s kubernetes-client

# 本地测试目前还是 docker-compose 最方便，docker 仍有必要安装
sudo zypper in docker
sudo gpasswd --add $USER docker
sudo systemctl enable docker
sudo systemctl start docker

# 简单起见，直接用 pip 安装 docker-compose 和 podman-compose
sudo pip install docker-compose podman-compose
```

### 办公、音乐、聊天

```shell
# 添加 openSUSE_zh 源：https://build.opensuse.org/project/show/home:opensuse_zh
sudo zypper addrepo 'https://download.opensuse.org/repositories/home:/opensuse_zh/openSUSE_Tumbleweed' openSUSE_zh
sudo zypper refresh
sudo zypper install wps-office netease-cloud-music

# linux qq: https://im.qq.com/linuxqq/download.html
# 虽然简陋但也够用，发送文件比 KDE Connect 要方便一些。
sudo rpm -ivh linux_qq.rpm
```

### 安装输入法

我用的输入法是小鹤音形，首先安装 fcitx-rime:

```shell
# 添加 m17n obs 源：https://build.openSUSE.org/repositories/M17N
sudo zypper addrepo 'https://download.opensuse.org/repositories/M17N/openSUSE_Tumbleweed' m17n
sudo zypper refresh
sudo zypper install fcitx5 fcitx5-configtool fcitx5-qt5 fcitx5-rime
```

然后，从 http://flypy.ys168.com/ 下载最新的鼠须管（MacOS）配置文件，将解压得到的 rime 文件夹拷贝到 ~/.local/share/fcitx5/ 下：

```shell
mv rime ~/.local/share/fcitx5/
```

现在重启系统，在 fcitx5 配置里面添加 rime「中州韵」，就可以正常使用小鹤音形了。

### QEMU/KVM

不得不说，openSUSE 安装 KVM 真的超方便，纯 GUI 操作：

```shell
# see: https://doc.openSUSE.org/documentation/leap/virtualization/html/book-virt/cha-vt-installation.html
sudo yast2 virtualization
# enter to terminal ui, select kvm + kvm tools, and then install it.
```

KVM 的详细文档参见 [KVM/README.md](../../virtual%20machine/KVM/README.md)

### VPN 连接与防火墙

防火墙默认会禁用 pptp 等 vpn 协议的端口，需要手动打开.

允许使用 PPTP 协议：

```shell
# 允许 gre 数据包流入网络
sudo firewall-cmd --permanent --zone=public --direct --add-rule ipv4 filter INPUT 0 -p gre -j ACCEPT
sudo firewall-cmd --permanent --zone=public --direct --add-rule ipv6 filter INPUT 0 -p gre -j ACCEPT

# masquerade: 自动使用 interface 地址伪装所有流量（将主机当作路由器使用，vpn 是虚拟网络，需要这个功能）
sudo firewall-cmd --permanent --zone=public --add-masquerade
# pptp 客户端使用固定端口 1723/tcp 通信
firewall-cmd --add-port=1723/tcp --permanent

sudo firewall-cmd --reload
```

允许使用 wireguard 协议，此协议只使用 tcp 协议，而且可以端口号可以自定义。不过 wireguard 自身的配置文件 `/etc/wireguard/xxx.conf` 就能配置 iptables 参数放行相关端口，这里就不赘述了。

## 触摸板手势

参考 [libinput-gestures](https://github.com/bulletmark/libinput-gestures)

## 安装 Nvidia 闭源驱动

> 完全参考官方文档 <https://en.opensuse.org/SDB:NVIDIA_drivers>

```shell
# 添加 Nvidia 官方镜像源
zypper addrepo --refresh https://download.nvidia.com/opensuse/tumbleweed NVIDIA

# 搜索驱动以及对应的版本号
# 在如下 Nvidia 官方站点根据提示检索出合适的最新驱动，然后使用其版本号在如下 zypper 命令输出中找到对应的驱动名称
# https://www.nvidia.com/Download/index.aspx
# 比如我的显卡是 RTX3070，通过版本号能找到其对应的驱动为  x11-video-nvidiaG06
zypper se -s x11-video-nvidiaG0*

# 安装驱动
zypper in  x11-video-nvidiaG06 x11-video-nvidiaG06
```

如果你还需要安装 CUDA 来本地炼丹，CUDA 的安装有两种方法：

- 直接将 CUDA 安装在本机，可参考 [NVIDIA CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)
- 使用 Docker 容器炼丹，可参考 [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

## 设置代理工具

为了加速网络或者访问一些国内不存在的网站，网络代理是必不可少的工具。

我习惯使用 clash，极简安装方法如下：

1. 首先 `sudo zypper in clash` 安装好 clash
2. clash 环境配置（记不清是否得手动配置这个了...）
   1. 下载好 [Country.mmdb](https://github.com/Dreamacro/maxmind-geoip/releases) 放到 `~/.config/clash` 中
   2. 好像还需要下载下 clash-dashboard 到 `~/.config/clash/ui`
3. 找到你自己的 clash 配置订阅地址（各种机场都会提供的），写个小脚本内容为 `curl "<订阅地址>" > ~/.config/clash/config.yaml`
   1. 如果这个文件夹还没有就先创建一下
   2. 如果代理是自己搭建的，那就自己写这个配置咯
4. 把脚本放在 PATH 中的某个目录中，方便随时调用更新
5. 使用 tmux 后台启动 clash，代理就设置完成了
   1. 浏览器可以通过 swichomega 来设置细致的代理规则
   2. 命令行可以直接使用 `export HTTP_PROXY=http://127.0.0.1; export HTTPS_PROXY=http://127.0.0.1` 来使用代理，大部分命令行程序都会使用这两个环境变量的配置。
6. 一般机场给的 clash 配置都会直接开启 clash Web 配置页，可以通过 <http://localhost:9090/ui/#/proxies> 直接访问

## 设置 zypper 使用 proxy 下载更新

zypper 默认不会读取 `HTTP_PROXY` 跟 `HTTPS_PROXY` 等环境变量，对于一些无国内镜像的源而言，可以通过如下方式配置走代理提升下载速度（这需要你已经有本地代理才行，比如说 clash）：

- 进入 YaST GUI
- 在搜索框直接搜索 `proxy` 即可找到对应的配置项
- 配置好 http 以及 https 协议的代理地址，如果是本地的 clash，可以直接填 `http://127.0.0.1:7890`
- 在「No Proxy Domains」中添加国内镜像源地址，使它们不要走代理
  - 如果是跟我的教程走的，应该需要将这个值改成 `localhost,127.0.0.1,mirrors.bfsu.edu.cn,mirrors.aliyun.com`

### KDE Connect

KDE Connect 是一个 PC 手机协同工具，可以在电脑和手机之间共享剪切版、远程输入、发送文件、共享文件夹、通知同步等等。
总而言之非常好用，只要手机和 PC 处于同一个局域网就行，不需要什么数据线。

如果安装系统时选择了打开防火墙，KDE Connect 是连不上的，需要手动开放端口号：

```shell
# see: https://userbase.kde.org/KDEConnect#firewalld
# 还可以使用 --add-source=xx.xx.xx.xx/xx 设置 ip 白名单
sudo firewall-cmd --zone=public --permanent --add-port=1714-1764/tcp
sudo firewall-cmd --zone=public --permanent --add-port=1714-1764/udp

sudo firewall-cmd --reload

# 确认下已经开放这些端口
sudo firewall-cmd --list-all
```

然后手机（Android）安装好 KDE Connect，就能开始享受了。

目前存在的 Bug:

- [ ] Android 10 禁止了后台应用读取剪切版，这导致 KDE Connect 只能从 PC 同步到手机，而无法反向同步。
  - 如果你有 ROOT 权限，可以参考 [Fix clipboard permission on Android 10](https://szclsya.me/posts/android/fix-clipboard-android-10/) 的方法，安装 ClipboardWhitelist 来打开权限。
  - 否则，貌似就只能使用手机端的「远程输入」模块来手动传输文本了。

### VPN 连接与其他防火墙相关配置

防火墙默认会禁用所有对外端口，需要手动打开。

允许使用 PPTP 协议：

```shell
# 允许 gre 数据包流入网络
sudo firewall-cmd --permanent --zone=public --direct --add-rule ipv4 filter INPUT 0 -p gre -j ACCEPT
sudo firewall-cmd --permanent --zone=public --direct --add-rule ipv6 filter INPUT 0 -p gre -j ACCEPT

# masquerade: 自动使用 interface 地址伪装所有流量（将主机当作路由器使用，vpn 是虚拟网络，需要这个功能）
sudo firewall-cmd --permanent --zone=public --add-masquerade
# pptp 客户端使用固定端口 1723/tcp 通信
firewall-cmd --add-port=1723/tcp --permanent

sudo firewall-cmd --reload

# 确认下已经开放这些端口
sudo firewall-cmd --list-all
```

允许使用 wireguard 协议：

此协议只使用 tcp 协议，而且可以端口号可以自定义。不过 wireguard 自身的配置文件 `/etc/wireguard/xxx.conf` 就能配置 iptables 参数放行相关端口，这里就不赘述了。

### OpenSSH 服务

为了局域网数据传输方便，以及远程使用 PC，我一般都会给自己的 Linux 机器打开 OpenSSH 服务。

在 OpenSUSE 上启用 OpenSSH 服务的流程：

```shell
sudo systemctl enable sshd
sudo systemctl start sshd
sudo systemctl status sshd
```

#### 2. 设置使用密钥登录

显然密钥登录才足够安全，这里介绍下我如何设置密钥登录。

先生成密钥对（如果你常用 github，本地应该已经有密钥对了，可以考虑直接使用同一个密钥对，这样就能跳过这一步）：

```shell
# 或者直接命令行指定密钥算法类型(-t)、名称与路径(-f)、注释(-C)、密钥的保护密码(-P)。
## 当密钥较多时，注释可用于区分密钥的用途。
## 算法推荐使用 ed25519/ecdsa，默认的 rsa 算法目前已不推荐使用（需要很长的密钥和签名才能保证安全）。
ssh-keygen -t ed25519 -f id_rsa_for_xxx -C "ssh key for xxx" -P ''
```

接下来需要把公钥追加到主机的 `$HOME/.ssh/authorized_keys` 文件的末尾（`$HOME` 是 user 的家目录，不是 root 的家目录，请看清楚了）：

```shell
# 方法一，手动将公钥添加到 ~/.ssh/authorized_keys 中
# 然后手动将  ~/.ssh/authorized_keys 的权限设为 600
chmod 600 ~/.ssh/authorized_keys

# 方法二：如果你的密钥对在其他主机上，可以直接在该主机上执行如下命令将公钥添加到 openSUSE 机器上，会有提示输入密码
#   -i 设定公钥位置，默认使用 ~/.ssh/id_rsa.pub
ssh-copy-id  -i path/to/key_name.pub user@host
```

现在就完事了，可以使用密钥钥登录试试：

```shell
#   -i 设定私钥位置，默认使用 ~/.ssh/id_rsa
ssh <username>@<server-ip> -i <rsa_private_key>

# 举例
ssh ubuntu@111.222.333.444 -i ~/.ssh/id_rsa_for_server
```

#### 2. 调整安全设置

openSUSE 的 OpenSSH 服务默认是允许密码登录的，虽然也有登录速率限制，还是会有点危险。

既然我们前面已经设置好了密钥登录，现在就可以把密码登录功能完全禁用掉，提升安全性。

请取消注释并修改 `/usr/etc/ssh/sshd_config` 中如下参数的值：

> 注意 OpenSSH 的主配置文件是 `/usr/etc/ssh/sshd_config`，而不是大部分 Linux 发行版使用的 `/etc/ssh/sshd_config`。

```conf
# 安全相关配置
LoginGraceTime 2m
StrictModes yes
MaxAuthTries 6
MaxSessions 10

# 禁止使用 root 用户登录
PermitRootLogin no

# 允许使用公钥认证
PubkeyAuthentication yes

# 禁用明文密码登录
PasswordAuthentication no
# 禁用掉基于 password 的交互式认证
KbdInteractiveAuthentication no
# 禁用 PAM 模块
UsePAM no
```

改完后再重启下 sshd 服务并用 ssh 命令登录测试确认功能已生效：

```shell
# 尝试在使用「公钥验证」之外的其他方法登录
# 如果 sshd 服务的设置正确，这行命令应该登录失败并报错「Permission Denied(publickey)」
ssh -o PubkeyAuthentication=no user@host
```

### firewall 防火墙介绍

firewall 是 SUSE/RedHat 等 RPM 发行版使用的防火墙程序，它底层使用的是 iptables/nftables，常用命令如下：

```bash
systemctl enable firewalld   # 启用 firewalld 服务，即打开「开机自启」功能
systemctl disable firewalld  # 关闭 firewalld 服务，即关闭「开机自启」功能

systemctl status firewalld   # 查看 firewalld 的状态
systemctl start  firewalld   # 启动
systemctl stop firewalld     # 停止

# 打开 SSH 端口
sudo firewall-cmd --zone=public --add-port=22/tcp --permanent

# 关闭 SSH 端口
firewall-cmd --zone=public --remove-port=22/tcp --permanent

# 修改防火墙规则后需要重载配置
sudo firewall-cmd --reload

# 查看 firewall 的状态
sudo firewall-cmd --list-all
```

## 其他设置

从 Windows 带过来的习惯是单击选中文件，双击才打开，这个可以在「系统设置」-「工作空间行为」-「常规行为」-「点击行为」中修改。
