---
title: "Proxmox Virtual Environment 使用指南"
date: 2022-11-27T22:38:03+08:00
lastmod: 2022-11-27T22:38:03+08:00
draft: false

resources:
- name: "featured-image"
  src: "proxmox-logo.webp"

tags: ["虚拟化", "Visualization", "KVM", "QEMU", "libvirt", "Proxmox"]
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

>本文介绍我使用 PVE 的一些心得（不保证正确 emmmm），可能需要一定使用经验才能顺畅阅读。

## 前言

我在去年的文章 [「QEMU/KVM 虚拟化环境的搭建与使用」](https://thiscute.world/posts/QEMU/KVM-usage/) 中介绍了如何使用 QEMU/KVM 作为桌面虚拟化软件，其功能对标开源免费的 [Oracle VM VirtualBox](https://www.virtualbox.org/) 以及收费但是用户众多的 [VMware Workstation Pro](https://www.vmware.com/products/workstation-pro.html).

虽然我们也可以远程使用 QEMU/KVM，但是使用门槛比较高。而且如果要管理多台服务器，各种命令也比较繁琐。
我们显然需要更易用的软件来管理服务器场景下的虚拟化。

而这篇文章介绍的 [Proxmox Virtual Environment](https://pve.proxmox.com/wiki/Main_Page)（后续简称 PVE），就是一个基于 QEMU/KVM 的虚拟机集群管理平台。

PVE 以 Debian + QEMU/KVM + LXC 为基础进行了深度定制，提供了一套比较完善的 Web UI，基本上 95% 的操作都可以直接通过它的 Web UI 完成，但是仍然有些功能只需要使用它的 CLI 完成，或者说需要手动修改一些配置文件。

PVE 完全基于 Linux 世界的各种开源技术，存储技术使用了 LVM（也支持 Ceph/iSCSI/NFS），也支持通过 cloudinit 预配置网络、磁盘扩容、设置 hostname（这其实是 libvirtd 的功能）。
它的文档也比较齐全，而且写得清晰易懂，还包含许多它底层的 QEMU/KVM/CEPH/Cloudinit 等开源技术的内容，对学习 Linux 虚拟化技术也有些帮助。（这里必须喷下 VMware 的文档，真的是写得烂得一批，不知所云）

总的来说，PVE 没有 [vShpere Hypervisor][vShpere Hypervisor] 跟 [Windows Hyper-V][Windows Hyper-V] 那么成熟、完善、稳定，但是基于 QEMU/KVM 且能够免费使用，很适合 Linux/开源/虚拟化 爱好者折腾。

>你可能还听说过 OpenStack，不过这个玩意儿我没接触过，所以这里略过了它。

因为这些原因，我选择了 PVE 作为我的 Homelab 系统。

先贴一张我当前 Homelab 的 PVE 控制台截图，然后就进入正文。

![](/images/proxmox-ve-instruction/ryan-pve-console.webp "我的 PVE 集群")


## 一、安装 PVE 系统

建议直接使用 [ventoy](https://github.com/ventoy/Ventoy) 制作一个 U 盘启动盘，把官网下载的 PVE 拷贝进去即可进行系统安装。
安装过程中需要注意的点有：

- 如果你有多台机器，每台机器需要使用不同的主机名称（hostname），否则后面组建 PVE 集群时会有麻烦。
  - 建议使用机器型号 + 数字编号作为机器的 hostname
- 最好是为每台机器配置静态 IP，避免 IP 变更。

系统安装好后即可按照提示直接访问其 Web UI，会提示 HTTPS 证书无效，忽略即可。另外还会有一个烦人的 PVE 订阅提示，也可直接忽略（7.2 及以上版本，暂时没找到怎么禁用掉这个提示）。

此外对于国内环境，建议按下面这篇文章配置国内镜像源（提升软件安装速度）：

```shell
# 设置 debian 的阿里镜像源
cp /etc/apt/sources.list /etc/apt/sources.list.bak
sed -i "s@\(deb\|security\).debian.org@mirrors.aliyun.com@g" /etc/apt/sources.list

# 设置 pve 国内镜像源
# https://mirrors.bfsu.edu.cn/help/proxmox/
echo 'deb https://mirrors.bfsu.edu.cn/proxmox/debian buster pve-no-subscription' > /etc/apt/sources.list.d/pve-no-subscription.list
```

### 组建 PVE 集群

>如果你仅使用单机 PVE，可忽略这一节内容。

将多台 PVE 节点组成一个集群，可以获得很多新玩法，比如虚拟机在多节点间的热迁移。

这个也还挺简单的，首先随便登入一台机器的 Web Console，点击「Datacenter」=>「Cluster」=>「Create Cluster」即可创建一个 PVE 集群。

接着复制「Join Information」中的内容，在其他每台 PVE 节点的 Web Console 页面中，点击「Datacenter」=>「Cluster」=>「Join Cluster」，然后粘贴前面复制的「Join Information」，再输入前面节点的密码，等待大约一分钟，然后刷新页面，PVE 集群即组建完成。

![](/images/proxmox-ve-instruction/pve-cluster-configuration.webp "PVE 集群配置")


PVE 集群的所有节点是完全平等的，集群组建完成后，登录其中任意一个节点的 Web Console 都可以管理集群中所有节点的资源。

## 二、PVE 控制台的使用

PVE 控制台的使用还挺简单的，多试试基本就会用了。这里不做详细介绍，主要说明下一些要点：

- CPU
  - 对于比较吃性能或者对实时性要求高的虚拟机如 windows/openwrt，可以将其 CPU 类型设置为 `host`
  - 对于虚拟机核数，建议将 `sockets` 设为 1（即 CPU 插槽数，一般物理服务器才会有 2 及以上的 CPU 插槽），cores 设为你想分配给该虚拟机的 CPU 核数
  - 仅针对多物理 CPU 场景（多 `sockets`）才需要启用 NUMA
- 磁盘、网卡
  - 尽量使用 `virtio` 作为 scsi 磁盘、network 网卡的虚拟化控制器，它的性能最高
  - 如果硬盘是 SSD，虚拟机磁盘可以启用 `SSD Emulation`，对于 IO 性能要求高的场景还可以为磁盘勾选 `IO  Thread` 功能
- 其他选项
  - 调整启动项顺序，对于 cloud image 建议只启用 scsi0 这个选项
- 虚拟机模板（Template）与克隆（Clone）
  - 建议首先使用 ubuntu/opensuse cloud image 配置好基础环境（比如安装好 vim/curl/qemu-guest-agent），然后转换为 template，其他所有 Linux 虚拟机都可以直接 clone 一个，改个新名字，再改改 cloudinit 配置跟磁盘大小，就能直接启动使用了。相当方便。
  - 仅 Full Clone 的虚拟机才可以在 PVE 集群节点间随意迁移，因此如果你需要虚拟机迁移功能，请不要使用 Link Clone.
- BIOS 通常都建议使用默认的 SeaBIOS，仅 Windows 等场景才建议换成 OMVF(UEFI)
  - OMVF 的分辨率、Secure Boot 等参数，都可以在启动时按 ESC 进入 UEFI 配置界面来调整。

而 PCIe 直通之类的高级功能，我现在还没玩到，建议自行搜索相关资料...

### 1. 使用 cloudinit 自动配置网卡、SSH密钥、存储空间

>完全参照官方文档 [Cloud-Init_Support - PVE Docs](https://pve.proxmox.com/wiki/Cloud-Init_Support)

>注意：下面的几种镜像都分别有自己的坑点，仅 Ubuntu/OpenSUSE 测试通过，其他发行版的 Cloud 镜像都有各种毛病...

首先下载 Cloud 版本的系统镜像：

1. [Ubuntu Cloud Images (RELEASED)](https://cloud-images.ubuntu.com/releases/): 提供 img 格式的裸镜像（PVE 也支持此格式）
   - 请下载带有 .img 结尾的镜像，其中 `kvm.img` 结尾的镜像会更精简一点，而不带 kvm 的会稍微大一点，但是带了所有常用的内核模块。
2. [OpenSUSE Cloud Images](https://download.opensuse.org/repositories/Cloud:/Images:/)
   - 请下载带有 NoCloud 或者 OpenStack 字样的镜像。
3. 对于其他镜像，可以考虑手动通过 iso 来制作一个 cloudinit 镜像，参考 [openstack - create ubuntu cloud images from iso](https://docs.openstack.org/image-guide/ubuntu-image.html)

>注：[Debian Cloud Images](https://cdimage.debian.org/cdimage/cloud/) 的镜像无法使用，其他 ubuntu/opensuse 的 cloud 镜像也各有问题...在后面的常见问题中有简单描述这些问题。

上述镜像和我们普通虚拟机使用的 ISO 镜像的区别，一是镜像格式不同，二是都自带了 `cloud-init`/`cloud-utils-growpart` 等 cloud 相关软件，三是如果你使用了。

其中 NoCloud 表示支持 cloudinit NoCloud 数据源——即使用 `seed.iso` 提供 user-data/meta-data/network-config 配置，PVE 就是使用的这种模式。
而 Openstack 镜像通常也都支持 NoCloud 模式，所以一般也是可以使用的。

cloud image 基本都没有默认密码，并且禁用了 SSH 密码登录，必须通过 cloud-init 设置私钥方式进行 ssh 登录。

建议在 cloud-init 配置中自行设置账号与私钥，不要使用默认的账号名。
比如测试环境，可以直接设置账号为 root，并设置相应的私钥。

接下来我们需要将得到的 qcow2 镜像导入 PVE，并用它创建一个虚拟机模板。

首先创建虚拟机，并以导入的磁盘为该虚拟机的硬盘

```shell
# 创建新虚拟机
qm create 9000 --name ubuntu-bionic-template --memory 2048 --net0 virtio,bridge=vmbr0

# 将下载好的 img/qcow2 镜像导入为新虚拟机的硬盘
qm importdisk 9000 ubuntu-20.10-server-cloudimg-amd64.img local-lvm

# 通过 scsi 方式，将导入的硬盘挂载到虚拟机上
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0

# qcow2 镜像默认仅 2G 大小，需要手动扩容到 32G，否则虚拟机启动会报错
qm resize 9000 scsi0 32G
```


```shell
# 创建一个 cloud-init 需要使用的 CDROM 盘(sr0)
qm set 9000 --ide2 local-lvm:cloudinit
# 设置系统引导盘
qm set 9000 --boot c --bootdisk scsi0
# 设置 serial0 为显示终端，很多云镜像都需要这个。（？感觉我不需要？）
qm set 9000 --serial0 socket --vga serial0
```

后续配置：
1. 手动设置 cloud-init 参数，**重新生成 cloudinit image**，启动虚拟机，并通过 ssh 登入远程终端
   1. 貌似启动虚拟机时 PVE 会自动重新生成 seed.iso，但是手动生成下肯定更保险...
2. 检查 qemu-guest-agent，如果未自带，一定要手动安装它！
   1. ubuntu 需要通过 `sudo apt install qemu-guest-agent` 手动安装它
3. 安装所需的基础环境，如 docker/docker-compose/vim/git/python3
4. 关闭虚拟机，然后将虚拟机设为模板
5. 接下来就可以从这个模板虚拟机，克隆各类新虚拟机了~

![](/images/proxmox-ve-instruction/pve-cloudinit-configuration.webp "改完配置后一定要点击 Regenerate Image!")

其他 cloudinit 相关文档：

- [配置 Cloud-Init 工具 - 华为云](https://support.huaweicloud.com/usermanual-ims/ims_01_0407.html)
- [canonical/cloud-init - github](https://github.com/canonical/cloud-init)
- [Run Amazon Linux 2 as a virtual machine on premises](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-linux-2-virtual-machine.html)

### 2. 虚拟机硬盘扩容

CentOS/Ubuntu/Debian 提供的 Cloud 镜像，都自带了 `cloud-utils-growpart` 这个组件，可以实现在扩容物理硬盘时，自动调整 Linux 的分区大小。

因此需要扩容虚拟机时，直接通过 UI 面板/命令行扩容虚拟机的硬盘即可， Linux 的分区会被 `cloud-utils-growpart` 自动扩容。

而其他非 Cloud 镜像，则需要在扩容磁盘后再进入虚拟机手动扩容分区跟磁盘，具体命令就不介绍了，请自行查阅相关文档吧。

>因为这个方便的特性，也为了减少虚拟化的开销，Cloud 镜像默认是不使用 LVM 逻辑分区的。
LVM 逻辑分区虽然方便，但是它对物理机的作用更大些。虚拟机因为本身就能动态扩容“物理硬盘”的大小，基本不用不到 LVM。

>还有一点，就是虚拟机通常只需要一个根分区就行，尤其是归 openstack/kubernetes 管的虚拟机。
只有在使用分布式存储之类的场景下，数据需要独立存储，才需要用到额外的分区(`/data` 之类的)。
一般只有物理机，才需要像网上很多文章提的那样，为 `/boot` `/` `/home` 去单独分区。
而且现在大家都用 SSD 了，物理机这样做分区的都少了，比如我个人电脑，就是一个 `/` 分区打天下。。。

## 三、常见问题

### 1. 导入已有的 qcow2 镜像

>必须要命令行操作

先通过 scp 将 qcow2 传输到 PVE 上，然后命令行使用如下命令导入镜像：

```shell
# 命令格式
qm importdisk <vmid> <source> <storage>
# 示例
qm importdisk 201 vm-201-disk-1.qcow2 local-lvm
```

导入完成后，在 WebUI 界面的左侧会看到多了一个「未使用的磁盘 0」，
现在新建一台新虚拟机，然后删除掉默认的磁盘（分离+删除，要两步），然后挂载这个「未使用的磁盘 0」就大功告成了。


### 2. 点击 shutdown 后 PVE 系统卡住

PVE 的 `shutdown` 功能依赖 `qemu-guest-agent`，对于还没有安装 `qemu-guest-agent` 的任何主机，或者已经卡死无响应的虚拟机，千万不要点 `shutdown` 按钮，因为一定会卡住很久，最后失败！

`shutdown` 卡住的解决办法：手动在下方的「Tasks」面板中双击卡住的「Shutdown」操作，然后点击「stop」停止该操作。

该如何关闭这类没有 `qemu-guest-agent` 或者已经卡死无响应的主机？答案是使用 `stop`！

### 3. can’t lock file ‘/var/lock/qemu-server/lock-xxx.conf’ – got timeout

PVE 虚拟机卡在 BIOS 系统引导这一步，无法启动，也无法 `stop`！

解决方法：手动删除掉 lockfile: `/var/lock/qemu-server/lock-xxx.conf`

因为虚拟机还卡在 BIOS 引导这一步，删除掉 lockfile 再关闭虚拟机并不会导致数据丢失。

### 4. PVE 集群有一个节点宕机，如何解除关联？

将多个节点组成一个 PVE Cluster 是很自然的一个选择，它能提供虚拟机热迁移（同 CPU 供应商）、统一管理面板等非常方便的功能。
但是这会带来集群级别的高可用问题。

根据官方文档 [Cluster_Manager - Proxmox](https://pve.proxmox.com/wiki/Cluster_Manager)，如果你需要容忍一定数量的节点宕机，PVE Cluster 至少需要三台主机（这跟 Etcd 一样，大概是 Raft 共识算法的要求），并且所有节点的 PVE 版本要完全一致。

那么如果个别节点出了问题，无法修复，该如何将它踢出集群呢？

如果需要踢出的节点仍然处于可用状态，而且在线节点占比超过 50%，则修改流程如下：

- 首先通过访问节点的 shell 界面，通过命令 `pvecm nodes` 确认集群的所有节点
- 将需要移除的节点彻底关机，并且确保它不会以当前配置再次启动（也就是说关机后需要清空硬盘，避免数据混乱）
- 通过命令 `pvecm delnode xxx` 将问题节点移除集群
- 重置旧节点硬盘，并重新装机，用做其他用途。

如果你的集群只有 2 个节点，或者有超过 3 个节点但是宕机节点数不低于 50%，那出于数据一致性要求 Raft 算法会禁止更新集群数据，上面的流程就走不通了。如果你直接走上面的流程，它会报错 `cluster not ready - no quorum?` 这时需要首先修改配置，使剩下的节点重新达成一致。其实就是修改选主节点时的投票数。

对于 2 个节点但挂掉 1 个的情况，首先执行如下指令允许当前节点自己选主：

```shell
# 设置只需要 1 票就能当前主节点
# 潜在问题是可能有些集群元数据只在损坏节点上有，这么改会导致这些数据丢失，从而造成一些问题。
# 安全起见，建议在修复集群后，再重启一遍节点...
pvecm expected 1
```

现在 quorum 就已经恢复了，可以走前面给出的节点移除流程。

如果节点已经删除，但是 Web GUI 上仍然显示有被删除的节点，可以在集群的所有剩余节点上，手动删除掉 `/etc/pve/nodes/node-name/` 文件夹，即可从集群中彻底删除该节点的数据，注意千万别删错了，不然就尴尬了...

如果 corosync 完全无法启动，上面给出的命令也会修改选主投票参数也会失败，这时可以直接手动修改 `/etc/corosync/corosync.conf` 删除掉有问题的节点对应的配置，调低 expceted 投票数，使 corosync 能正常启动，再执行前述操作。


### 5. cloud image 的坑

#### ubuntu cloud image 的坑

- ubuntu 启动时会报错 `no such device: root`，但是过一会就会正常启动。
  - 这是 ubuntu cloud image 的 bug: https://bugs.launchpad.net/cloud-images/+bug/1726476
- ubuntu 启动后很快就会进入登录界面，但是 root 密码可能还没改好，登录会报密码错误，等待一会再尝试登录就 OK 了
- ubuntu 的默认网卡名称是 ens3，不是 eth0，注意修改 network_config 的网卡名称，否则网络配置不会生效
- 以 kvm 结尾的 Ubuntu Cloud Image 无法识别到 USB 设备，将 USB 端口映射到该虚拟机中没有任何作用。
  - kvm 使用了精简版的 linux 内核，去掉了 USB 等在云上用不到的驱动，建议改用无 kvm 结尾的镜像。

##### 「Ubuntu Cloud Image 无法识别到 USB 设备」的排查记录

现象：

- 在尝试使用 PVE 将 USB 接口直通到 Ubuntu Cloud Image 启动的虚拟机作为 NAS 系统时，发现 `lsblk` 根本无法找到我的 USB 硬盘
- 换成我笔记本接硬盘盒，能够正常识别并挂载硬盘
- 使用 `lsusb` 不会报错，但是也看不到任何内容
- 使用 `lspci` 能找到 USB 对应的 PCI 设备
- 进一步使用 `cat /proc/modules | grep usb` 与 `lsmod | grep usb` 均查不到任何 usb 相关的内核模块
  - 而在我笔记本上 `lsmod | grep usb` 能够输出 `usb_storage` `usb_core` 等多项内核模块。 
- 再用 `modprobe usb` 会提示 `modprobe: FATAL: Module usb not found in directory /lib/modules/5.15.0-1021-kvm`

问题原因很明显了，Ubuntu 根本没有为 cloud image 预置 usb 内核模块，所以才有这个问题...

进一步搜索发现这个帖子：[What's the difference between ubuntu's amd64-disk-kvm.img and the regular amd64.img cloud images?](https://askubuntu.com/questions/1315370/whats-the-difference-between-ubuntus-amd64-disk-kvm-img-and-the-regular-amd64)，解答了我的疑惑。

原因是，我使用了 ubuntu 为 cloud 环境做了精简的 kvm 内核，非常轻量，但是缺少 usb 等常用内核模块。

对于 NAS 外接存储这个场景，我应该使用不以 kvm 结尾的 ubuntu cloud image，换了个基础镜像后问题就解决了~

#### opensuse cloud image 的坑

- opensuse leap 15 只支持 network_config v1，对 v2 的支持有 bug，`gateway4` 不会生效

#### debian cloud image 的坑

debian 的 cloud 镜像根本没法用，建议避免使用它。

- debian 启动时会彻底卡住，或者直接报错 kernel panic
  - 原因是添加了 spice 图形卡，换成 vnc 就正常了
- [Debian Cloud Images](https://cdimage.debian.org/cdimage/cloud/) 中的 nocloud 镜像不会在启动时运行 cloudinit，cloudinit 完全不生效
  - 不知道是啥坑，没解决

### 6. 克隆创建的虚拟机，卡在 `Booting from Hard Disk...` 状态

被用做模板的虚拟机可以正常启动，但是克隆的虚拟机就卡住了。

可能的原因：

1. 磁盘有问题，出这个问题的 cloud image 是 `ubuntu-20.10-server-cloudimg-amd64.img`，我更换成 `ubuntu-20.10-server-cloudimg-amd64-disk-kvm.img` 就没问题了。
   1. 磁盘镜像均下载自 https://cloud-images.ubuntu.com/releases/groovy/release-20201210/
2. BIOS 不匹配：将 BIOS 从 SeaBIOS 切换到 OVMF(UEFI)
   1. 如果仍然无法启动，请进入 OVMF 的 BIOS 界面关闭「Secure Boot」后再重启看看

### 7. 虚拟机启动时 cloudinit 报错 faild to start OpenBSD Secure Shell server 

有如下几种可能：

- **可能性一：虚拟机名称包含非法字符**
  - pve 的 cloudinit 配置会在启动时尝试将虚拟机 hostname 修改为与虚拟机一致，但是又没有对虚拟机名称做合法性校验...
  - 当你使用的虚拟机名称包含了非法字符时就会出这个问题，比如 `ubuntu-22.10-cloudimage-template`，其中的 `.` 就是非法的， `.` 在 DNS 中用于划分不同的域！
  - **解决方法**：克隆个新虚拟机并改用合法名称，再删除旧虚拟机，问题就解决了。
- **可能性二：磁盘空间不足**
  - qcow 镜像转换成的虚拟机磁盘很小，只有 2G，如果不扩容，启动时就会出各种奇怪的问题。
  - **解决方法**：通过 Web UI 扩容磁盘大小，建议至少给 32G。

### 8. 修改 Linux 虚拟机的 Hostname

如前所述，pve 的 cloudinit 配置会在启动时尝试将虚拟机 hostname 修改为与虚拟机一致，这导致手动修改无法生效无效。

解决方法：从旧的虚拟机克隆一个新虚拟机，将新虚拟机名称设为你期望的 hostname，然后删除旧虚拟机，启动新克隆的虚拟机，即完成了 hostname 重命名。


### 9. 虚拟机迁移时报错 `Host key verification failed`

>社区相关帖子：https://forum.proxmox.com/threads/host-key-verification-failed-when-migrate.41666/

这通常是因为节点增删，或者不小心动到了 `~/.ssh/known_hosts` 文件，导致的问题。

可以通过手动在每台节点上执行如下命令解决：

```shell
ssh -o 'HostKeyAlias=<Target node Name>' root@<Target node IP>
```

注意将上述命令中的 `Target node Name>` 改为节点名称，将 `<Target node IP>` 改为节点 IP 地址。

### 10. PVE 的 vm 不支持 vmx/svm 虚拟化指令集

> 参考: https://zhuanlan.zhihu.com/p/354034712

在 Linux 虚拟机中运行如下命令：

```shell
egrep '(vmx|svm)' --color=always /proc/cpuinfo
```

有输出则说明此虚拟机本身也支持 vmx/svm 虚拟化指令集（vmx 是 intel 指令集，svm 是 amd 的指令集）。

如果没有任何输出，说明此虚拟机不支持嵌套虚拟机，无法在其内部运行 Hyper-V 或者 kvm 虚拟化程序。

一般来说 PVE 宿主机默认就会启用嵌套虚拟化功能，可通过如下指令验证：

```shell
# intel 用这个命令，输出 Y 则表示启用了嵌套虚拟化
cat /sys/module/kvm_intel/parameters/nested
# amd 用如下指令，输出 1 则表示启用了嵌套虚拟化
cat /sys/module/kvm_amd/parameters/nested
```

如果输出不是 `Y`/`1`，请自己网上查下如何启用。

上面这么一堆操作能证明，宿主机已经启用了嵌套虚拟化，但是虚拟机内部却没有虚拟化指令集。

**根本原因是使用了默认使用 kvm64 这个 CPU 类型，它是一种虚拟化的 CPU，不支持 vmx/svm 指令集！将虚拟机的 CPU 类型改为 `host`，然后重启虚拟机，问题就解决了**。


## 四、PVE 网络配置

### 1. 桥接多张物理网卡

示例如下，主要就是在 vmbr0 网桥的 `Bridge Ports` 里面：

![](/images/proxmox-ve-instruction/pve-multiple-nic.webp "桥接多张物理网卡")


### 2. 手动添加 USB 物理网卡

>参考官方文档: [SysAdmin - Network Configuration](https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysadmin_network_configuration)

我遇到这个问题的场景是：我的 mini 主机（GTR5）只有两个 2.5G 网卡，不太够用。而家里的路由器剩下的都是千兆网口，路由器也难以拓展网卡。
网上搜了下 2.5G 交换机又发现价格 429 起步，所以决定买两张 USB 2.5GbE 网卡插在这台小主机上作为便宜的网口拓展方案。

现在网卡有了，有两种方式可以让 PVE 识别到这张网卡：

>好像 PVE 偶尔也能自动识别到网卡，就是比较慢...

1. 方法一：直接重启机器，然后就能在 Web UI 的 `Network` 配置中见到这张 USB 网卡了。之后直接把该网卡加入到 vmbr 网桥的 `Bridge Ports` 中并应用配置，就大功告成了。
2. 方法二：不重启机器实现添加 USB 网卡。如果机器不能重启，就可以走这个流程：
   1. 首先，使用 `ip link` 命令打印出当前的所有网络接口
   2. 将 2.5GbE 网卡插到 USB3.0 端口上，Linux 将自动识别到它
   3. 现在再使用 `ip link` 命令查看所有网络接口，找到新增的接口名称（通常在输出内容最末尾）。
      1. 在我的环境中新的 USB 网卡名称为 `enx00e04c680178`
   4. 在配置文件 `/etc/network/interfaces` 的末尾新增一行：`iface enx00e04c680178 inet manual`（注意替换网卡名称）
   5. 现在直接刷新 Web UI 页面， USB 网卡就会出现了。之后直接把该网卡加入到 vmbr 网桥的 `Bridge Ports` 中并应用配置，就大功告成了。

### 3. 配置 WiFi 网卡

如果主机自带了 WiFi 网卡，启动后 Proxmox VE 能识别到该网卡，但是无法通过 Web UI 修改它的任何配置。

那么本着物尽其用的精神，该如何利用上这张 WiFi 网卡呢？

根据 PVE 官方文档 [WLAN - Proxmox VE Docs](https://pve.proxmox.com/wiki/WLAN)，并不建议在 PVE 上使用 WLAN，它存在如下问题：

- WiFi 自身必须是一个 Linux Bridge 设备，无法被桥接到 vmbr0 等网桥上。因为大多数 Access Point 都会直接拒绝掉未授权的源地址发过来的数据包...
- 与有线连接相比，WiFi 的延迟要高得多，而且不太稳定。

如果要配置 WLAN 网卡的话，可以直接参考 Debian 的官方文档进行配置：[How to use a WiFi interface - Debian](https://wiki.debian.org/WiFi/HowToUse)

因此，我觉得将 WiFi 网卡直接 USB 直通给机器内的 OpenWRT 虚拟机来玩，可能是更好的主意。

后续将会更新相关内容...待续

## 拓展 - cloudinit 高级配置

PVE 使用 CDROM 只读盘(`/dev/sr0`)来进行 cloud-init 的配置。
在虚拟机启动后，`/dev/sr0` 将被卸载。

可挂载上该只读盘，查看其中的初始化配置内容：

```shell
$ mkdir cloud-config
$ mount /dev/sr0 cloud-config
mount: /dev/sr0 is write-protected, mounting read-only
$ ls cloud-config
meta-data  network-config  user-data
```

查看其中内容，会发现 `user-data` 有很多参数都被硬编码了，没有通过 PVE Web Console 暴露出来，导致我们无法自定义这些配置。

比如它硬编码了 `manage_etc_hosts: true`，强制每次都使用虚拟机的名称作为 hostname.

如果确认有修改这些配置的需求，完全可以修改掉 PVE 代码里的硬编码参数。
通过全文搜索即可找到硬编码参数的位置，以 `manage_etc_hosts` 为例：

```shell
# 在 /usr/share 中全文搜索 manage_etc_hosts 这个关键字
grep -r manage_etc_hosts /usr/share
```

直接就搜索到了硬编码位置是 `/usr/share/perl5/PVE/QemuServer/Cloudinit.pm`，修改对应的 cloudinit 配置模板，然后重启节点（重启才能重新加载对应的 ruby 程序），即可实现对该硬编码参数的修改。


## 拓展 - 自动化配置与监控告警

自动化配置相关工具：

1. [Telmate/terraform-provider-proxmox](https://github.com/Telmate/terraform-provider-proxmox/): 用户最多，但是只支持管理虚拟机资源
1. [danitso/terraform-provider-proxmox](https://github.com/danitso/terraform-provider-proxmox): stars 少，但是可以管理 PVE 的大部分资源，包括节点、用户、资源池、TLS证书等等
    - 代码更顺眼，但是作者忙，没时间合并 pr，导致 Bug 更多一些，而且很久没更新了...
2. [ryan4yin/pulumi-proxmox](https://github.com/ryan4yin/pulumi-proxmox): 我维护的一个 proxmox 自动配置工具
3. [Python SDK](https://github.com/proxmoxer/proxmoxer)

监控告警：

- [prometheus pve expoter](https://github.com/prometheus-pve/prometheus-pve-exporter): 通过 prometheus+grafana 监控 PVE 集群

## 拓展 - 其他 QEMU/KVM 相关的虚拟化平台

PVE 毕竟是一个商业系统，虽然目前可以免费用，但是以后就不一定了。

如果你担心 PVE 以后会不提供免费使用的功能，或者单纯想折腾折腾的技术，还可以试试下面这些虚拟化平台：

- [webvirtcloud](https://github.com/retspen/webvirtcloud): 其前身是 webvirtmgr，一个完全开源的 QEMU/KVM Web UI，额外提供了用户管理功能。
- [kubevirt](https://github.com/kubevirt/kubevirt): 基于 Kubernetes 进行虚拟化管理
- [rancher/harvester](https://github.com/rancher/harvester): Rancher 开源的基于 Kubernetes 的超融合平台(HCI)
  - 其底层使用 kubevirt 提供虚拟化能力，通过 longhorn 提供分布式存储能力。
  - HCI 超融合 = 计算虚拟化 + 网络虚拟化 + 分布式存储，它和传统的虚拟化软件最大的不同是：分布式存储。
  - 企业级场景下一般至少得 10GbE 网络 + SSD 才能 hold 住 HCI 超融合架构。
  - 超融合对存储的一些要求：
    - 软件定义 – 解除硬件绑定，可通过升级拓展更丰富的功能，自动化能力高
    - 全分布式架构 - 扩展性好，消除单点故障风险
    - 高可靠性 - 智能的故障恢复功能，丰富的数据保护手段
    - 高性能 – 支持多种存储介质，充分挖掘和利用新式硬件的性能
    - 高度融合 – 架构简单并易于管理
  - 超融合架构可以降低私有云的构建与维护难度，让私有云的使用维护和公有云一样简单。
  - 超融合架构下，虚拟机的计算和存储是完全高可用的：计算资源能智能动态更换，存储也是分布式存储，底层计算和存储也可以很简单的扩缩容。

我打算有时间在 PVE 集群里跑个 rancher/harvester 玩玩 emmmm

## 参考

- [KVM 虚拟化环境搭建 - ProxmoxVE](https://zhuanlan.zhihu.com/p/49118355)
- [KVM 虚拟化环境搭建 - WebVirtMgr](https://zhuanlan.zhihu.com/p/49120559)


[vShpere Hypervisor]: https://www.vmware.com/cn/products/vsphere-hypervisor.html
[Windows Hyper-V]: https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview