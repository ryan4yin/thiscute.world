---
title: "曾经的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false

# 此页禁用评论系统
comment:
  utterances:
    enable: false
  waline:
    enable: false
---

![](/images/now/book-shelf-1.webp)

>记录下我的学习轨迹。（结果写着写着有点像是技术笔记跟日记的混合了 hhhh）

>Twitter 上 @manjusaka.eth 等大佬喜欢写周报，不过我不太喜欢周报的形式。因为周报的标题本身没啥意义，而要看其中的内容却得一个个点进去看，这对我自己回顾过往的学习、工作、生活，体验非常不方便。
>我比较喜欢类似「一镜到底」的阅读体验，所以我采用这种单页的方式来记录我的日常。（基于同样的理由，我将博客单页展示的文章数量上限调整成了 `1000`）
>同时如果某一天的日报内容跟前一天并无区别，我会直接省略掉当天的记录。

### 2023-02-21

- 折腾一晚上终于用 STM32 点亮了 TFT 液晶屏，以及搞定了使用 printf 打印日志到串口。
  - [ryan4yin/learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)

### 2023-02-16 - 2023-02-20

- 180 大洋买的 ESP-Drone 到货，玩了一晚上直接机翼折损...而且即使在室内也很不稳定不好操控，感觉是因为飞控算法不行或者芯片性能太弱。
- 学了一波 ESP-IDF 编程，发现封装得比较彻底，只需要调上层接口就行，整了整 WS2812 彩灯控制，代码简单，也很有意思。
- ESP-IDF 的文档虽然也挺多，可学起来没啥方向感。于是又开始跟野火 STM32 HAL 库的教程，学了一波发现 STM32 比 ESP32 要复杂很多，STM32 HAL 更接近底层，学起来有很多地方一知半解，但是感觉学会了进步也会更大。
- 在用 STM32 HAL 整 TFT 显示器，目前还未成功...
- 2/18 在深圳南头古城跟 0xFFFF 线下约了一波茶会，谈天说地随便聊了聊。
- 还整了一波本地跑 Stable-Diffusion-WebUI，结果模型太大了，我 8G 的 RTX 3070 跑不动...打算换个小点的模型跑。

### 2023-02-15

- 看上了 [esp-drone](https://github.com/espressif/esp-drone) 这个项目，为了轻松入门，直接在淘宝上买了一套 esp-drone 的散件打算自己组装，花了 180 大洋（感觉自己折腾的话估计只要 100，不过效果不好说）。
- 翻出了之前买的两块 esp32 开发板，开始学习 vscode + esp-idf 进行 esp32 程序开发，发现它用到的技术确实比较杂（C + CMake + Kconfig + Python），门槛比 STM32 要高，不过对我而言还 OK。
  - 用 ESP32 整了个 WS2812 跑马灯，比较有意思~

### 2023-02-11

- 研究 Homelab 备份与数据同步方案，写了点笔记 [数据备份与同步策略](https://github.com/ryan4yin/knowledge/blob/master/homelab/%E6%95%B0%E6%8D%AE%E5%A4%87%E4%BB%BD%E4%B8%8E%E5%90%8C%E6%AD%A5.md)
- 研究了下 Linux 远程桌面方案：SSH X11 Forwarding 跟 xrdp，意外发现在客户端是 Linux 的情况下，SSH X11 Forwarding 配置与使用居然如此简单而且效果也非常好！只需要改一行 sshd 配置，客户端直接 `ssh -X user@host` 就 ok 了~
- 研究在 orangepi5(rk3558s) 上跑 AI 任务，写了点笔记 [demos_rk3588](https://github.com/ryan4yin/knowledge/tree/master/electrical-engineering/demos_rk3588)

### 2023-02-10

- 重新研究了下 Proxmox VE，更新了之前写的 Proxmox 使用指南
- 发现 Windows Server 跑的 NAS 数据传输还是不太快，晚上整了一波 Promox VE 的 PCIe 直通想把 USB 控制器直通给 Windows，结果完全失败...
  - 输出半成品笔记 [Proxmox PCI 直通.md](https://github.com/ryan4yin/knowledge/blob/master/homelab/Proxmox%20PCI%20%E7%9B%B4%E9%80%9A.md)

### 2023-02-09

- datacenter 版的 win server 2022 有毛病老是挂掉重启，换了 standard 版重装系统
- 为了用上 windows 的 smb/iscsi 黑科技，我不得不考虑把存了 2T 数据的 btrfs 盘改成 ntfs/refs 文件系统
  - 研究了一波 refs 发现不太行，而且 linux 完全不支持这个系统，有风险，还是决定用 ntfs
  - 首先考虑把 btrfs 磁盘挂载进 wsl2，再用 rsync 同步到 ntfs 盘，结果新装的 wsl2 又有毛病，`wsl --mount` 报错...
  - 第二个方案成功了——两个盘都挂载到 ubuntu 虚拟机用 rsync 拷贝到 ntfs 磁盘。
    - 但是拷贝时发现 linux 的 ntfs 驱动性能不行，将就着用了。
    - 睡前想到另一个方案：直接用开源驱动把 btrfs 挂在 win server 下再对拷，据此查到了 winbtrfs，但是查了下据依云等大佬说，比较灵车，我又不敢用了。
    - 朋友表示 btrfs 用 winbtrfs 挂为只读在 windows 上 copy，可能速度会好很多（喷的就是 ntfs 的 Linux 驱动）。

### 2023-02-08

- 最近买的 Orange Pi 5 到手玩了两天了，确实有点意思。
  - 其核心 RK3558S 还有 NPU，我找了 rockchip 官方 demo [rknpu2](https://github.com/rockchip-linux/rknpu2) 玩了玩，挺有意思的。
  - 瑞芯微官方的 [rknn-toolkit2](https://github.com/rockchip-linux/rknn-toolkit2) 好像得安装在 x64 PC 上，模型得用它进行转换后才能跑在 rk3558s 上面，具体还没研究。玩板子顺便还能玩一玩 AI，挺不错~
- UM560 炸掉的 asgard 固态 2023/2/7 换新到货了，装好机后重新加入 PVE 集群，重建挂掉的 k3s 集群，调整 NAS 架构，又更新相关的笔记，反正一番折腾。
- 确定改用 Windows Server 2022 DataCenter 跑 NAS 系统，因为它的 SMB 协议很多黑科技，速度快。硬盘盒就直接映射到这台 Windows Server 里面。
  - 一个盘给 Windows 当 SMB 硬盘用，用了 ReFS 文件系统
  - 另一个盘绑定到 wsl2 给 docker 容器用，仍然决定用 btrfs 文件系统
- 遇到一个问题是 windows server 2022 因为没嵌套虚拟化，装不了 hyper-v，一番查找发现，将 vm cpu 类型从 kvm64 改为 host 就解决了
- 另一个问题是 wsl2 ubuntu 无法启动，通过 [WSL/issues/5440](https://github.com/microsoft/WSL/issues/5440#issuecomment-778660156) 中提到的方法解决了——创建 `~/.wslconfig`，通过它禁用 wsl 嵌套虚拟化功能。
- 再一个问题就是通过 wsl2 访问 btrfs 等 linux 系的文件系统
  - 根据官方文档 [在 WSL 2 中装载 Linux 磁盘](https://learn.microsoft.com/zh-cn/windows/wsl/wsl2-mount-disk)，通过 `GET-CimInstance -query "SELECT * from Win32_DiskDrive"` 查询磁盘 ID，再通过 `wsl --mount \\.\PHYSICALDRIVE2 --bare` 挂载即可.
  - 注意事项是，必须以 `--bare` 裸磁盘的方式挂载进 wsl2 中，再手动在 wsl2 中通过 `sudo mount /dev/sdb1 xxx` 的方式挂载磁盘，否则会报错。(这个文件系统挂载，重启后大概会消失，还得研究下怎么搞成自动挂载)
- 仍然没找到英语学习的节奏，年后基本没学几天英语。
- 搞硬件的热情又上来了，特别是 RK3558S 这颗 SOC 感觉挺好玩的样子，加了 OrangePi5 的群见了市面（群友们玩得都挺有意思）。


### 2023-02-03

- 折腾 Homelab 时，主力节点 UM560 固态翻车了，是才用了三个月的 Asgard 512G SSD，颗粒是长江存储的。走京东售后了
  - 上次翻车是 2022-11-02 炸了根光威弈 Pro 1T，这也没隔多久啊...

![](/images/now/nvme-critial-medium-error.webp "2022-11-02 翻车记录，系统无法启动，这是显示器输出内容")
![](/images/now/nvme-device-not-ready.webp "2023-02-03 翻车记录，系统能启动但是文件损坏，这是 dmesg 信息")


### 2023-01-30

- 健身 30mins: day 2

### 2023-01-29

- 过年期间放下了所有的学习，测了词汇量也停留在了 6500，今天开始恢复学习
- 更新 Learn English Again 这篇文章，并在 0xffff 社区发贴分享
- 买的健身器材到了，现有设备瑜伽垫、握力器、脚蹬拉力器、弹力健身棒。没计算啥卡路里，简单定下了每天运动 30mins 的小目标，等坚持一个月再看看体重有无改善吧，现在感觉有点虚胖。
- 健身 30mins: day 1
  - 玩了玩几样健身设备，感觉还挺有意思的。练习强度也不大，不累，算是体验阶段。后续再慢慢加量。
- 英语阅读
  - The Moon and Sixpence  - 23/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习   - 145/270 (漏打卡 62 天)

### 2023-01-14

- 跟 0xFFFF 社区的朋友们约饭，账单金额也很讨喜：666
- 想清楚了一个问题：其实经历曲折一点，对个人的心态是有帮助的。经历太过一帆风顺了，后期反而很可能遇到瓶颈
  - 我觉得我搞技术的职业生涯发展这么顺利，跟高中、大学期间的这么多曲折经历，关系挺大的
  - 之前也在跟人的一些沟通中提到过一点——「我在学校时负面情绪就已经爆棚了，刚工作时虽然起点贼低，但是相比在学校时心理压力小太多了，反而感觉到获得了解放。工作上的负面情绪对我而言可能就像毛毛雨，而做自己喜欢的事带来的成就感则是我在学校时从未体会过的。这种从业前期的经历使我更在意成就感、同事的认可而非某些负面情绪。」
  - 古人总结过这个叫「塞翁失马，焉知非福」，现代也有很多人叫「吃亏是福」。


### 2023-01-11

- 一晚上没接告警，工作真告一段落了。
- 然后就是失去了继续学习英语、折腾其他东西的东西，感觉真的需要停一下，修养一段时间，恢复下被新冠、咳嗽、以及 K8s 升级这个大任务消耗掉的精气神。


### 2023-01-10

- 又一次完成 K8S 集群升级，虽然还是跟去年一样鸭梨山大，写了好多小脚本做各种升级处理，还加了四五个小时班，搞到 11 点...但总体上比 2021 年那一次顺畅多了，一次完成。没去年那么多加戏——升级回滚好几次，API 可用率还各种抖动。
  - 这次升级这么顺利，我的个人经验是其一，内部平台的多集群支持是其二，今年我做的网关的改造降低了流量迁移难度是其三，最后同事也仍然跟去年一样为我提供了重要帮助。话不多说，感恩各位同事。
  - 再立个 flag，2023 年我要推动公司的 K8s 集群升级流程迭代，告别「依靠个人经验，一路做各种骚操作解决各种意料之外的疑难杂症，最终完成升级」的「石器时代」，实现半自动化。
  - 突然想到，十多万 QPS 的流量迁移，好像有点像是所谓的「给飞行中的飞机换引擎」，瞬间变得高大上了。
- 抗过今晚，明天再收个尾，2022 年的工作就告一段落了。好像心中的一块石头落了地。

### 2023-01-06 - 2023-01-08

- 跟同事交流后对工作与个人的成长有了些新的感悟，结合之前与领导聊过的个人职业发展，感觉人生也是各种 trade-off 啊。
  - 回想我在大宇这两年，第一年的工作其实很不顺利，没找到方向，被 leader 推着往前瞎走，到年底的时候发现，之前做的事因为兼容性问题要全部推翻...感觉随时要提桶跑路。leader 说过几次组里我的适应速度最慢，工作上一直没磨合好。
  - 真的有运气的成分，各种原因年底本来领导属意由另一位同事执行的 EKS 升级工作，因为他有其他事忙不过来，又交给了我（我之前已经做过一次升级，出了问题回退了）。在年底终于硬着头皮把它搞定了，这拯救了我去年年底的绩效。
- 晚上跟朋友聊天吹水时想到一点，「博客评论，本质上也是社交。你给人家评论，人家也会回访，看到好的文章也不介意评论一句。」所以许多生活博客评论数是最多的，这说明博主花了很多精力在维系这个圈子。就我的体验看，适当的博客社交感觉还挺不错的。
- 回顾了一下很久前做过的心里评测记录，有一点比较重要的我一直没改掉：「过度分享」，我好像一直比较喜欢分享自己的种种，但如果过了某个界限，也并不是一件好事。
  - 还是要把握住核心，说话前多动下脑子想下倾听者的感受，少说点废话，也少分享些别人不感兴趣的内容。

### 2023-01-05

- 最近看到两个 ext4 文件系统相关的帖子，知识点刚好能串起来，都跟 ext4 文件系统的 htree 这个 B 树索引有关：
  - [文件系统作为缓存时的路径生成方案 - 0xffff.one 社区](https://0xffff.one/d/1395-wen-jian-xi-tong-zuo-wei-huan-cun)
  - [在有大量长文件名小文件的情况下需要启用 large_dir - @Manjusaka_Lee](https://twitter.com/Manjusaka_Lee/status/1610690497550643206)

### 2023-01-02

- 英语阅读
  - The Moon and Sixpence  - 15/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 118/270 (漏打卡 36 天)
- 词汇量测试：新的一年，测了一下词汇量，测了三次选了结果低的一次，词汇量为 **6583**
    {{<figure src="/images/now/2023-01-02-test-your-vocabulary-result.webp" title="2023-01-02 词汇量测试结果：6583 词" width="70%">}}
    {{<figure src="/images/now/2022-12-19-test-your-vocabulary-result.webp" title="2022-12-19 词汇量测试结果：6300 词" width="40%">}}
    {{<figure src="/images/learn-english-again/2022-11-17-test-your-vocabulary-result.webp" title="2022-11-17 词汇量测试结果：5600 词" width="65%">}}
    {{<figure src="/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp" title="2022-10-18 词汇量测试结果：5100 词" width="40%">}}
- 电子电路
  - 3D 打印机折腾了几天，暂时放下了。
  - 电子电路的话，跨年前后这几天学完了《51 单片机自学笔记》的汇编部分，然后直接开始通过野火的视频教程学 STM32，跟着写了一些 C 代码挺有意思的。
  - 输出内容有两个仓库：[learn-8051-asm](https://github.com/ryan4yin/learn-8051-asm) 与 [learn-stm32f103c8t6](https://github.com/ryan4yin/learn-stm32f103c8t6)
    {{<figure src="/images/now/8051-display-2023.webp" title="8051 汇编 - 数码管显示 2023" width="70%">}}
    {{<figure src="/images/now/8051-led-dancing.gif" title="8051 汇编 - LED 编舞..." width="70%">}}
    {{<figure src="/images/now/8051-display-start-seconds.gif" title="8051 汇编 - 数码管动态显示秒数" width="70%">}}
  - 简单看了下 ESP32/ESP8266 开发发现用的是 C++，感觉可能得花一两天时间学下 C++ 的 Class 相关逻辑，不然代码不好懂。
  - 另外也在考虑玩一玩 STM32 Linux 驱动开发以及 Rust 嵌入式开发，这两个大概是新的一年希望点亮的技能了。

哦还有连续三年蝉联我年度歌手的天依同学，截图放这里纪念一下：

{{<figure src="/images/now/netease-cloud-music-2022-singer-of-ryan4yin.webp" title="我的网易云年度歌手" width="50%">}}


### 2022-12-25

- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 110/270 (漏打卡 29 天)
- 电子电路
  - 在焦急地等待大半天后，晚上 3D 打印机「ELEGOO Neptune 3 Pro」终于到货了，折腾了一波，很好玩（
  - 继续通过我的摇摇棒学习《51 单片机自学笔记》
- 白天退了烧，但是到了晚上又开始低烧了，新冠确实比一般感冒要折磨人一点...

### 2022-12-24

- 英语阅读
  - The Moon and Sixpence  - 8/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 109/270 (漏打卡 28 天)
- 电子电路
  - 又下单一批元器件，另外斥巨资 1499 买了一台 3D 打印机「ELEGOO Neptune 3 Pro」，预计明天到货
  - 因为之前的摇摇棒刚好是用的 STC89S52 单片机，开始通过它学习《51 单片机自学笔记》。
    - 这本书用的是 keli 语法汇编，一番折腾搞定了用 linux platformio 编译上传书中的汇编代码，成果放在了 [learn-8051-asm](https://github.com/ryan4yin/learn-8051-asm)，后续持续更新。
  - 考虑到折腾面包板很容易忘记电路接线，打算画点原理图，一番搜索决定研究下开源跨平台工具 KiCAD

### 2022-12-20

- 英语阅读
  - The Moon and Sixpence  - 6/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 105/270 (漏打卡 25 天)
- 电子电路
  - 找到 [platform-intel_mcs51/issues/47](https://github.com/platformio/platform-intel_mcs51/issues/47) 这个 issue，根据它的描述，解决了上周摇摇棒（使用的 51 单片机）烧录卡住的问题
  - 焊接了一个指尖陀螺套件，这也是我第一次焊接贴片元件，贴得歪歪扭扭的，不过工作正常，效果很惊艳~很好玩 emmmm
- 工作
  - 这两周主要是落地了 Nginx TLS 加密，将 TLS 加密从 AWS NLB 上移到 Nginx + cert-manager，降了一波成本。
  - 另外预计下周执行 EKS 容器集群版本升级，仍打算使用稳妥的「新建集群」方式，开始搭建调试新集群。

### 2022-12-19

- 英语阅读
  - The Moon and Sixpence  - 4/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 104/270 (漏打卡 25 天)
- 词汇量测试：又过去了一个月，本月因为玩上了 Homelab 跟电子电路，漏打了很多卡，但是前面厚积薄发，测出的词汇量相比上个月上涨约 700 词，到了 6300
  {{<figure src="/images/now/2022-12-19-test-your-vocabulary-result.webp" title="2022-12-19 词汇量测试结果：6300 词" width="40%">}}
  {{<figure src="/images/learn-english-again/2022-11-17-test-your-vocabulary-result.webp" title="2022-11-17 词汇量测试结果：5600 词" width="65%">}}
  {{<figure src="/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp" title="2022-10-18 词汇量测试结果：5100 词" width="40%">}}
- 电子电路
  - 花了一晚上焊好了一块可调电压电流稳压电源，最后看说明书，发现必须输入 AC 24V 交流电...买错板子了尴尬，买的时候只注意了 0-30V 可调，没注意输入电源的参数...
  - 不过它的元件很多，还有很多大个头，应该是我目前焊接过的最有意思的板子了~
  - ![](/images/now/zy-kt-104-front.webp "焊好的可调稳压电源 - 正面")
  - ![](/images/now/zy-kt-104-back.webp "焊好的可调稳压电源 - 背面")
- 回顾了下我目前短暂的电子电路入门史，2022/12/1-2022/12/8 开始玩 ESPHome 智能家居，2022/12/11 买了一堆焊接套装、塞车底盘等各种套件，开始正式玩电子电路...到目前满打满算 19 天。

### 2022-12-18

- 英语学习
  - 鸽了...
- 电子电路
  - 焊一个特斯拉线圈套件时，一个功率三极管跟一个功率 MOSFET 管引脚插太深，散热片跟卖家展示图的安装方式不一样了。然后就开始拆焊，但这两个元件都好大一块金属特别难拆，最后三极管成功拆焊，MOSFET 管的引脚被我掰断了...直接导致我一整天都不想焊任何东西了...
- Linux
  - 因为不想焊电路板了，就打算搞一搞闲置许久的笔记本。旧的 OpenSUSE 用了一年多，用出了很多毛病，顺便就打算换个 Linux 发行版。
    - OpenSUSE Twmbleweed 的毛病细数如下：
      - 在 Nvidia 独显模式下无法启动，但是我用 Windows 打游戏时又希望开独显模式...
      - 关机基本上都是关不掉了，得强制关机...
      - KDE 桌面也各种毛病
        - x11 对高分屏的缩放支持很垃圾，各种缩放不一致。换成对缩放支持比较好的 plasma wayland 又各种 bug。
        - 桌面各种外观组件，都给人一种很脆弱的感觉，不论是高仿的 Windows 还是 MacOS，都只是样子货。实际一使用就能感觉到使用流畅度差 Windows/MacOS 太多了（主要是动画差，很生硬）。
  - 试用了一圈，考虑到对国产软件的支持（Arch AUR 仓库）、Nvidia 显卡支持，以及桌面高分屏支持，最终选择了 Endeavour 系统，直接使用 i3wm 窗口管理器，目前体验良好。目前体验总结如下：
    - 可以使用鼠标，也能使用快捷键，可以像 tmux 一样调整多窗口布局，或者全屏，总体挺方便的。我目前是鼠标跟几个好记的快捷键结合使用。
    - 有些组件如关机菜单、dmenu 等页面仍然完全没有缩放，还没搞明白怎么调。不过应该可以调大。
    - 启动跟关闭都很快，OpenSUE 下系统无法关机的问题消失了。
  - 因为听说 sway 对 wayland 的支持比较好，性能更高，对缩放的支持也更好，试安装了 endeavour 社区的 sway 桌面版本，发现 sway 根本无法启动...一番调研发现是 sway 不支持 nvidia 闭源驱动，使用参数强制启动 sway 后系统完全没缩放，鼠标图标都完全不显示，暂时放弃了。打算等明年 sway 的 vulkan api 支持 stable，再来试试。

### 2022-12-16

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 100/100 (补读 15 天)
    - 凌晨一点低烧（腋温 38）睡不着，看完了这本书的最后一段。全书 9W 词不算多，但是 100 天却感觉这么长。读完还是挺感慨的。小说的内容很不错，值 5 颗星。
    - 想起去年 12 月，凌晨在高铁站看完保罗奥斯特的《月宫》，而此时此刻，今年 12 月，我在凌晨发着烧看完了《The Unlikely Pilgrimage of Harold Fry》。再次清晰地理解到，一年又过去了啊
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 101/270 (漏打卡 24 天)
- 电子电路
  - 安装好了淘宝 28 块钱买的四自由度模板机械臂，拿昨天写的遥控小车代码改了改逻辑，使用树莓派实现了蓝牙手柄遥控机械臂。不过机械臂钳子的舵机被我弄坏了，夹不了东西 emmm
  - 焊接好了淘宝 23.5 元买的行走机器人套件，虽然确实能正常前进后退，但是前进/回退的切换间隔有点长，调了半天没搞明白怎么调电位器能缩短它的间隔时间。当然显然我也还没明白它的电路图原理，只是单纯照着 PCB 板标注把元器件焊接上去了而已，隔几天再研究下这个电路图，了解下各个元器件的功能，以及电路如何工作。

{{<figure src="/images/now/mintreading-first-100days-achivement.webp" title="在薄荷阅读上读完的第一本英语原版书" width="35%">}}

### 2022-12-15

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 99/100 (补读 15 天)
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 100/270 (漏打卡 24 天)
    - 学了八分钟，然后就 0 点了...所以没打到卡
- 电子电路
  - 给昨天组装的树莓派四驱小车，用 pygame 写了七十多行代码，接入了 Xbox One 蓝牙手柄控制，实现了童年时的梦想——拥有一台遥控赛车！
    - Xbox One 蓝牙连接部分参考了 [Setting up Xbox Controllers on the Raspberry Pi](https://pimylifeup.com/xbox-controllers-raspberry-pi/)，pygame 代码参考了 [How to use an Xbox Controller with your Robot](https://www.youtube.com/watch?v=F5Bq7HVJkX0)
  - 花了一个多小时，快速翻完了这两本书剩下的内容，补全了硬件领域的一些知识。不过我很清楚自己想要了解什么，所以不太关注书中的代码细节（因为大概率用不上，不如自己写 emmm）。
    - Learn Robotics With Raspberry Pi
    - Learn Robotics Programming, 2nd Edition
  - 在社区空地上发现两个报废的氛围灯，把灯带拆回来，给手办柜做了一个暖色调顶灯~

### 2022-12-14

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 98/100 (补读 15 天)
- 电子电路
  - 组装搭建了一台树莓派四驱小车，用 gpiozero 控制，虽然代码超级简单，但我是第一次玩硬件，感觉好有意思！
    - 元件：树莓派 4B + 面包板 + 面包板电源 + 移动电源 + L9110S 四路直流电机驱动板 + 四驱小车底盘
    - 使用的连接线：母对母/母对公杜邦线 + USB 公对公数据线
    - 这一套去掉移动电源跟树莓派，总成本 40 大洋
    - 准备了一个八颗电池串联的电池盒，但是感觉用一次性电池玩这个太浪费了，所以换成了移动电源。
  - 后面还可以试试接入蓝牙手柄控制、接入摄像头等传感器，感觉可玩性挺高的。

### 2022-12-13

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 97/100 (补读 15 天)
- 电子电路
  - 网上再查了下烙铁头优化方法，跟 0xffff 群友讨论了下，将烙铁头上锡、上松香，然后在湿润的高温海绵上各种摩擦，折腾了好一番后，成功将氧化物去除。
    - 毕竟这个发热芯是一体的，贵，舍不得直接当成耗材（用钢丝球或者砂纸暴力去氧化）...
    - 另外就是发现这么用，还挺费高温海绵的，感觉得多买几块。
    - 同时群友表示铜丝球好用，以及贵的焊材能省不少心，又想下单一波了...
  - 发现烙铁头才到手两天，虽然刀尖的氧化物去掉了，但是上面也开始氧化了。群友表示只要日常使用的刀尖没黑就没毛病。
  - 看了许多「烙铁头（又称焊咀）使用与保养方法」，整理到了我的个人笔记中

### 2022-12-12

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 96/100 (补读 15 天)
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 97/270 (漏打卡 21 天)
- 电子电路
  - 网友改装的 PD 供电 L245 焊笔（兼容 JBC245 烙铁头）到货，焊接了我的第一块电路板（洞洞板），毕竟第一次，卖相显然不咋样...不过能够 work 哈哈
  - 玩着玩着，发现烙铁头变黑了...
    - 原因之一是我测试了几次空烧状态下会不会休眠，这个看起来都正常。
    - 主要原因很可能是我使用高温海绵擦拭烙铁头时没加水，用力擦拭时把烙铁头表面整坏了...
      - 根据网上资料，如果在干燥的高温海绵上清洁烙铁头，会使烙铁头受损而导致不上锡。
    - 给高温海绵加水后，试用了网上一些除氧化层的方法，在海绵上擦拭、上松香、上焊锡，但是都没能把氧化层去掉，它不沾锡。

### 2022-12-11

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 95/100 (补读 15 天)
  - The Moon and Sixpence  - 2/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 96/270 (漏打卡 20 天)
  - 发现背单词确实比英语阅读更难坚持，读故事更容易坚持一点...
  - 另外就是最近沉迷搞电子...
- 电子电路
  - 玩上瘾了，又买了大几百块钱的各种工具、器件
    - 焊接工具套装、各种开发版、电子元件包、七八个各种 ESP 开发版/模块、四驱小车套件 + 机械臂套件
    - 为了练习焊接 + 学一些电子电路基础，在淘宝「电子爱好者之家」上买了许多初中级的焊接套件
    - 各种其他相关工具：耐高温硅胶垫、螺丝磁性收纳垫等等
  - 以及玩电子后发现租房桌子不够用，淘宝补了一张 80cm * 60cm * 75cm 的方桌，专门用做电子工作台
  - 大学学电子工程的前同事（现在在搞 C# 开发）过来玩，感叹仿佛看到了当年自己寝室的景象，也是摆满各种元器件 emmm
  - 烧坏一个 1117 稳压管，搜索相关资料时发现宝藏 UP [工科男孙老师](https://space.bilibili.com/43584648)，从硬件入门到晶体管、dcdc 模块设计、示波器，都有讲。
    - 进一步找到了 [爱上半导体](https://space.bilibili.com/395188578)

![](/images/now/experience-of-electrical-engineering.webp "我的电子电路初体验")


### 2022-12-08

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 92/100 (补读 14 天)
  - The Moon and Sixpence  - 1/36
- ESPHome & Home Assistant
  - 之前买的 DHT11 传感器一直只有温度读数而且还高了室温 10 多摄氏度，湿度读数一直为 0. 网上怎么查都查不到相关资料，今天把它的蓝色塑料壳拆掉，随便擦了擦里面的面板后，瞬间两个读数都有了，而且运行一段时间后，温度也渐渐地接近室温了
    - 看起来就是里面有啥看不见的脏东西，或者就是塑料外壳本身有问题。
    - 拆掉外壳并清理后，又跑了大概 10 分钟等待数值稳定，温度仍然偏高接近 2 摄氏度，不过这在它的误差范围内。湿度比米家传感器的读数低了 9% 左右。
    - 对传感器吹一口气，温度跟湿度也会立马大增，看起来是 work 了，只是精度不够高，而且把壳子一套上温度立马就涨好几度...
  - 用 ESP32-C3 开发版接上了之前买了但一直没用上的 MP-135 气体传感器与 GY-302 数字光强度传感器
    - GY-302 效果挺不错
    - MP-135 一直检测不到它的模拟信号，只有 2 元的数字信号输出正常，用烟一熏或者酒精喷雾来一点，都会立马设为高电平，而且传感器的绿色指示灯也会亮起。

### 2022-12-07

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 91/100 (补读 14 天)
- 全国开始放松管控，出了疫情防控新十条规定，12306 也发公告火车站不再要求查验核酸。
  - 转眼间「精准防控」就在全国铺开了，大家对之后的经济复苏的预期都更乐观了，但是短期对感染新冠的担忧加强了。
  - 我也在京东上买了两个温度计，红外跟口腋温度计各一个...以及打算买点发烧止疼药（貌似都推荐对乙烯基氨酚），网上仍然很难买，打算这周去药店看看。

### 2022-12-06

- 晚上再次研究昨晚遇到的开发版问题
  - 发现只要把显示屏断电，wifi 就能正常连接，一连接显示屏，wifi 连接就会报错 auth expired...
  - 另外只要一连接红外发射器，系统就无法启动，也没有任何日志...把红外显示器拔掉，系统就正常了...
  - 跟 ChatGPT 讨论了下，它虽然没给出具体思路，但是提到的总线、传输频率，让我突然意识到，我的红外发射器跟显示屏的走线，都是直接从 ESP8266 模块下面经过的...可能是这造成了干扰。
  - 改了一下面包板的布局跟走线，就一切正常了，看来信号线如果经过核心模块，很可能使 ESP8266 无法正常工作...

### 2022-12-05

- 研究了一波时下流行的最强对话 AI ChatGPT，确实牛逼。虽然还有很多投毒信息，但是总体来讲已经比 copilot 等过去见过的 AI 强了一个级别，就像是看到了强人工智能的曙光。
- 晚上打算把 ESP8266 这块开发版用树莓派组个系统，但是怎么搞都有问题。
  - 系统启动后无法连接 wifi、接上红外发射模块后就内存泄漏导致系统无法启动等等，坑都被我踩了个遍...
  - 没解决睡觉去了

### 2022-12-02 - 2022-12-04

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 88/100 (漏打卡 10 天，已补读 8 天)
  - 薄荷阅读读满 80 天赠送的实体书到货了，回看下过去近三个月的阅读，收获良多，也感慨坚持之不易。主要我的兴趣点经常变化，近一两个月折腾 Homelab 跟智能家居，漏打了很多天的卡...
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 89/270 (漏打卡 15 天)
- ESPHome
  - 搞定了显示模块、红外空调遥控模块
  - （一直对搞电子电路很感兴趣，但是没想到我是这个时间点，从玩智能家居开始真正进入这个方向）
  - 朋友带了焊台过来帮我把两个传感器引脚焊上了，顺便教他搭了个 hugo 博客部署到了 github pages 上。
  - 玩得兴起又新买了一波传感器、 ESP32/ESP8266 开发版、四驱小车底盘、4 自由度机械臂等等，打算玩玩遥控车+遥控机械手。
  - 还研究了一波电烙铁吸锡器...先记录了下相关信息，后面如果继续发烧下去估计就得买了...
- 哦还有一个值得记录的就是最近 ChatGPT 开放访问，我的微信群、Twitter、关注的公众号相关文章与讨论，这个智能程度，真的有种「未来已来」的感觉了。我当前的饭碗还端稳多久？如何避免被淘汰？或许该重新考虑下这些问题了。

### 2022-12-01

- ESPHome 开发版传感器套装到货，首先把两个开发版都刷上了 ESPHome 固件
  - ESP8266 一次成功
  - ESP32-C3 默认配置编译失败说 Arudino Framework 不支持此开发版，调整 Arudino Framework 及 `platform-espressif32` 的版本到最新版后解决，并将解法补充到了搜到的 issue 上：[ESP32-C3 Arduino Core 2.0.0 - ESPHome](https://github.com/esphome/issues/issues/3031)
- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 85/100 (漏打卡 10 天，已补读 5 天)
  - 一点英语 270 天英语学习                  - 86/270 (漏打卡 14 天)

### 2022-11-30

- 买的米家智能家居设备到货，玩了一晚上的小爱音箱跟摄像头...
- 英语
  - The Unlikely Pilgrimage of Harold Fry - 84/100 (漏打卡 10 天，已补读 5 天)
  - 玩小爱音响跟摄像头，再次把一点英语打卡给鸽掉了...

### 2022-11-29

- 因为装了个 Home Assistant 后一直闲置，一时兴起开始了解如何把它玩起来，结果从 Home Assistant 一路看到小米米家，再看到 ESPHome...
  - 输出相关文档 [homelab/Home Automation.md](https://github.com/ryan4yin/knowledge/blob/master/homelab/Home%20Automation.md)
  - 买了一堆米家相关的智能家居设备（智能音箱、动感灯带、各种传感器等等），以及 ESPHome 相关开发版、传感器、面包板、万用表啥的...打算体验下
- 英语
  - The Unlikely Pilgrimage of Harold Fry - 83/100 (漏打卡 10 天，已补读 5 天)
  - 晚上查智能家居相关资料搞太嗨了，把一点英语打卡给鸽掉了...坚持打卡不断真的好难啊...

### 2022-11-28

- 考虑自己写一些简单的 dashboard 或者简单的工单系统、服务管理平台
  - 了解了一波[低代码开发平台](https://github.com/topics/low-code-framework)
    - 好处：开发简单
    - 缺点：UI 自定义比较困难
  - @zgq 给推荐了一套轻量级、上手简单的解决方案：[Alpine, Tailwind, Deno, SQLite 我的本地服务四件套](https://limboy.me/posts/local-services-tools/)
- 顺便阅读了 limboy 的 [应该成为专才还是通才](https://limboy.me/posts/specialize-or-generalist/)
  - 核心要点是「**要在某个特定领域做到 Top 非常困难，掌握大量不同技能不是解决之道，而应该多考虑如何将技能进行有效组合，技能的有效叠加大有裨益**。」
- 跟网友沟通后确认，Windows 可以将 SMB/WebDAV/ISCSI 协议共享挂载为网络硬盘，并绑定一个盘号！
  - 很久之前我 smb 挂载没成功，就一直以为只能挂载 iscsi 硬盘...
  - 重新梳理了一遍 NAS 相关的知识点，放在了 [homelab/Network Attached Storage](https://github.com/ryan4yin/knowledge/blob/master/homelab/Network%20Attached%20Storage.md) 里面

### 2022-11-27

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 81/100 (漏打卡 10 天，已补读 5 天)
  - The Time Machine  - 30/30
    - 读完了，内容想象力丰富，新奇有趣，也学到很多熟词生义、新词新表达。
  - The Moon and Sixpence  - 0.5/36
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 82/270 (漏打卡 12 天)
  - 一点英语已经漏打卡 12 天，基本都是 2022/11 月漏的。主要原因一是搞 Homelab，二是搬家、跟亲戚朋友聚会...
- 整理发表文章「Proxmox Virtual Environment 使用指南」
- OpenMediaVault 的 ISCSI 插件(tgt) 性能太差，研究了一波使用 Windows Server 2022 搭建 ISCSI + SMB 服务，看看是否能跑满我的 2.5G 带宽。

### 2022-11-25 - 2022-11-26

- 晚上去东莞松山湖跟高中同学聚会，车跑在高速上，旁边是城市远眺的夜景，还在下雨。朦胧中远眺的城市夜景，对久居城市，并且鲜少夜间出行的我而言。这样的景色显得很科幻。
- 然后跟几位同学打麻将打到半夜三点多...
- 第二天一起吃完饭，送读博的同学回工作地点，远远眺望了下他所在的大科学工程「[中国散裂中子源](http://english.ihep.cas.cn/csns/)」，感觉很高大上。

![](/images/now/play-mahjong-with-classmates.webp)
![](/images/now/china-spallation-neutron-source.webp)


### 2022-11-20

- 英语阅读
  - The Time Machine                          - 27/30
- 在朋友的帮助下搬家，最重的书都是朋友帮我搬上楼了，结果我仍然累得不行...相当尴尬...
- 新租房开通了电信 1000M 宽带，家庭网络体验感直线上升。

### 2022-11-18 - 2022-11-19

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 73/100
  - The Time Machine                          - 25/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 74/270
- 11/19 下午找了一圈房子，定了个 2000 一月的（包管理费），离坪洲站 50 米
  - 租房价格明显比去年低了很多，感觉跟今年经济不景气有关，很多人离开了深圳

### 2022-11-17

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 71/100
  - The Time Machine                          - 24/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 72/270
- 跟 RC（NoneBot/CQHTTP 作者）聊了聊，互相加了个小社群。
  - 沟通中梳理了下我今年对「高质量社群」的一些总结：社群的最大好处是能互相提供不一样的角度去看世界，互相提供价值。
  - 我今年算上 RC 的小群，一共加了四个感觉对我比较有帮助的群聊：
    - 年初的时候加了「十年之约 QQ 群」，见识了五花八门的写博客的网友，其中比较触动我的有经历坎坷的 [@叶开](https://qq.md/post/about)，有做 H 站被抓进牢的博友，还有很多搞安全的、写纯生活内容的博友，感觉很有意思。
      - 但是因为感觉更多的是开拓视野，内容对我帮助不大，却很容易让我分心，退过四次群了（每次退完又想加回去 emmm）
    - 第二个是「[苏洋的折腾群](https://soulteary.com/2019/02/01/small-community-description.html)」，苏洋的入群审核很严格，他会评估你跟折腾群互相之间能不能提供价值产出、你是否足够开放真诚，来决定是否接受加群邀请。群里大都是从事技术行业的工作党或者技术爱好者，群聊内容比较偏硬件、运维，比较偏工程，质量很高，对我很有帮助。
    - 第三个是 <https://0xffff.one> 的 QQ 群，最初是因为发现 [0x0001](zgq.ink) 在非常认真的做这个站点，而且社区帖子质量很高，所以加的群。群里应该有许多学生党，而且主题也是刷国外名校的公开课，所以聊得会更偏基础些，比如 6.S081、MIT 6.824、CS-144 等等，质量也很高。
      - 0xffff 社区在深圳也有不定期的线下聚会，上周参加了一次感觉很棒~
    - 第四个就是今天加的 RC 的小群了，主要是围绕 nonebot 生态聚集起来的，同样是各行各业、各个年龄段、各个学历层级都有，氛围也很好~
      - 跟我自己的小群比较类似，我的群最初是围绕小鹤音形输入法建立起来的一个程序员交流群，慢慢地就变成一个输入法圈子的程序员交流群，建立也有 5 年多了，人不多，活跃的人中，大家互相都很熟。聊天内容则是啥都有，代码、输入法、乐器、跑步、考试，反正想聊啥就聊啥咯。
- 使用 [Test Your Vocabulary](https://preply.com/en/learn/english/test-your-vocab) 做了一次词汇量评估，发现相比上个月 10/18 的测试，词汇量上升了大概 500 词。效果显著！
  - 而且明显发现测试中的很多词都是最近一个月刚学的词，其中好几个还忘记含义了（哭）。
  - 之前定的目标词汇量增加速度为：每天约 20 个单词，即一个月新增 600 词。估计是因为这个月搞 Homelab 鸽了好几天，导致词汇量上升速度不达预期。
  - 画外：不得不说，这个测试感觉真的很准。

{{<figure src="/images/learn-english-again/2022-11-17-test-your-vocabulary-result.webp" title="2022-11-17 词汇量测试结果：5600 词" width="65%">}}
{{<figure src="/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp" title="2022-10-18 词汇量测试结果：5100 词" width="40%">}}

### 2022-11-13

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 67/100
  - The Time Machine                          - 22/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 68/270
- 跟 0xFFFF 社区线下约饭，聊了到学英语、业务逻辑、搞 infra、国内国外等等，体验很好~
  - 一起聊的伙伴们各行各业都有，嵌入式 Linux、数仓、研究生

### 2022-11-12

- 搞机
  - 搞了台 OpenWRT 虚拟机作为软路由，使用了恩山论坛很火的省心固件，效果很好
  - 搞了个 OpenMediaVault 虚拟机，配置好了 SMB 文件夹共享、ISCSI 游戏盘、filebrowser 浏览器访问等等，体验很好（但是配置修改很慢，filebrowser 还有 Bug，总感觉有机会自己用 docker-compose 搞一套可能用着更爽些，缺点是要付出比较多的时间成本）。
- GTR5 主机的 1T 固态掉盘了，基本每次开机 20mins 就会掉盘，插上显示器显示内容为 `nvme nvme0: Device not ready; aborting reset, CSTS=0x1`
  - 还好不是主力机，没存重要数据，把虚拟机都迁移到 UM560 后，直接给错误截了个图，京东申请了售后
- 搞机搞到鸽掉了英语

![](/images/now/dashy-homepage.webp "我的 Homelab 导航页 2022-11-12")

### 2022-11-09


- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 63/100
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 64/270
- 也快年底了，趁着做 Review 写 OKR，顺便梳理下我今年的工作，除去参与日常的成本分析与管控、运维工作外，主要有如下这些：
  - 2022Q1（两个月） - 搞 HTTP 迁移到 gRPC 的支持方案，帮助业务方迁移到 gRPC 协议，流量成本与延迟的下降非常明显
  - 2022Q2（两个月） - 改用 AWS karpenter 做 EKS 离线计算集群（EMRonEKS）的扩缩容，使集群快速缩容，降低成本
  - 2022Q3（两个月） - 主要在做网关优化：
    1. 将运行在虚拟机上的 Nginx 网关容器化，迁移到 EKS 中。一是为了实现快速扩缩容，二是缩短 Nginx 到服务的流量链路，节约成本
       - 使用 go 语言写了个 sidecar 处理 nginx 的配置 reload、日志上传到 s3 等工作
    2. 使用 AWS NLB 取代 AWS ALB，结果是 Nginx 的 TCP 连接剧烈增长，导致 nginx reload 的影响很大，做了很多内核 TCP 连接相关的参数调优、以及 Nginx reload 相关的调整
    3. 利用 CloudFront 作为边缘网关，回源到 NLB，实现 DTO 流量的缩减，同时寻求降低时延
       - 此方案会带来 CloudFront 的请求成本剧烈上涨，只有在有请求减免协议的情况下才有省成本的可能
       - 注意仅 GET/HEAD 接口的回源流量才免费，所以此方案不适用于大量使用 POST/PUT 等方法的接口
       - 发现在使用纯 HTTP 回源时，将 CloudFront 用做 API 接口的边缘网关能显著降低时延
  - 2022Q4（三个月）- 仍然是在做网关优化
    1. 验证了在 Nginx 上做 TLS 加密的可行性：使用 cert-manager 申请与管理 TLS 证书，并在 Nginx 上实现 TLS 加密，使用 sidecar 处理证书的轮转
    2. 使用 APISIX 搭建 APP 端数据上报网关，以帮助 Data 团队自建数据分析平台，取代当前的神策。
       - 峰值接近 6W QPS，由于经验不足，APISIX 网关跟 Data 的数据解析器都问题频出，跟 Data 花了很多精力去排查问题、调优参数。投入的时间远超预期...
    3. 继续将流量大的接口迁移到 Q3 做的容器化网关，并添加前置 CloudFront 边缘网关，达成成本节约。期间发生两次失误，损失数千美刀
       - 2022-08-08 Post Mortem 1: 我在迭代 staging 环境配置时未意识到它与 prod 环境共用了同一个 EC2 安全组，导致容器化网关的线上流量归零 2h。因为仅配置了 Nginx 可用率告警，无流量时可用率仍然是 100%，完全未触发告警规则...直到我下班路上才猛然想起这回事，在地铁站里紧急修复...
         - 问题之一是 prod 环境与 staging 环境使用了同一个 EC2 安全组，没有做隔离；问题之二是仅配置了可用率告警，缺失 QPS 剧烈波动的告警
       - 2022-09-16 Post Mortem 2: 迁移旧 Nginx 配置时没仔细审查旧的 Nginx 配置，导致流量改成走 CloudFront 后服务获取到的客户端 IP 实际为 CloudFront IP。但是服务可用率正常，业务侧也未配置相关告警指标，所有人无感知。直到第二天运营发现此问题，并沟通快速修复
         - SRE 侧：问题根源是 SRE 未形成 Nginx 配置的 Check & Review 规范，导致很多事情全凭个人经验与发挥。
           - 表面原因：旧配置使用了 `proxy_set_header X-Forwarded-For $remote_addr;`，而正确的配置应该是 `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
         - 业务侧：问题根源是迁移时只关注了服务可用率，未关注核心业务指标
           - 表面原因：业务服务缺乏客户端 IP 相关指标与监控告警
  - 2022Q5（三个月） - 继续推进网关优化，取得预定的成本收益
    - 识别到 AWS ALB/NLB 的流量成本中是包含 TLS 握手的流量的，而握手时为了最大兼容性，服务端通常需要将证书的整个证书链发送给客户端，造成大量的流量成本
    - 使用单域名证书、ECC 公钥、证书层级短的证书、TLS1.3 session 复用，均可帮助缩减 TLS 握手的流量成本。
    - 测试调研，确认在 Nginx 上做 TLS 加密比使用 AWS NLB 提供的加密具有很大优势，能进一步降低 TLS 握手流量成本，以及 TLS 数据处理费用（NLCU）

### 2022-11-08

- 内存条到货，买了两根内存条，将 GTR5 5900HX 扩容到了 64G 内存，之前装的 32G 内存则换到 UM560 上。
- 加完内存后计算发现，GTR5 512G 的固态硬盘不够用了，于是把笔记本里给 Windows 游戏用的 1T 固态拆出来放在了 GTR5 5900HX 上，600G 的游戏本来想备份到硬盘盒，后来嫌备份太慢直接不备份了...
- 堂弟过来喝酒聊天，又花了时间搞机器，结果又把英语学习给鸽了...明天绝对不鸽！

### 2022-11-07

- 很久以前我编辑 `/histoy` 这个页面就很卡顿，而且 backspace/enter 经常彻底失去作用，今天定位到了这个问题
  - 一开始我以为是 vscode 的问题，试了 [vscode#28737](https://github.com/microsoft/vscode/issues/28737) 中的参数发现没任何作用。
  - 今天想到只有编辑我的博客项目时才卡，进一步地，只有编辑 `/history` 页时才卡，而这个页面有 1200 多行内容，所以猜测是 markdown 插件的性能问题。搜索找到了 [vscode-markdown#969](https://github.com/yzhang-gh/vscode-markdown/issues/969)
  - 根据上述 issue 中的性能问题定位文档，我在 vscode running extension 中开了下性能录制，发现时间全花在 [httpyac](https://github.com/AnWeber/httpyac) 上了，把它 disabled 掉问题就解决了...
- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 62/100
- 发现坚持每天学英语真的是一件相当难的事
  - 之前学到 40 天的时候，我觉得自己已经差不多养成每天学习的习惯了。可国节庆回家那天就忙到把学习给忘了，之后 SRE 小组出去聚餐又给忘了一次，第三次是最近一周迷上搞 Homelab，又漏打了两三天的卡。
  - 现在的总体进度是 62 天，漏打卡 5 天。算上之前在薄荷阅读上打了 7 天卡，一共有 69 天了。
  - 上次测词汇量是 10/18，感觉本月 11/18 可以再测一次，应该又涨了几百。

![](/images/now/vscode-markdown-performance-issue.webp)

### 2022-11-04 - 2022-11-06

- 家庭服务器规划：[ryan4yin/knowledge/homelab](https://github.com/ryan4yin/knowledge/tree/master/homelab)
- HDMI 视频采集卡跟另一台主机均到货，开始搭建家庭服务器环境~
  - MINISFORUM UM560 踩坑记录：
    - 首先遇到的问题是， 主机无法启动，风扇啸叫，视频采集卡无输出。
      - 用电脑试了下确定采集卡无问题，挨个插拔后定位到是内存条的问题，重新插拔后解决。
    - 然后遇到的是，家里没有键盘...打算拿 PC USB 接口模拟键盘输出，发现还挺麻烦。
      - 一番研究确定使用 [debian preseed](https://github.com/philpagel/debian-headless) 模式自动化安装，然后再在 debian 上安装 Proxmox VE 虚拟化系统，曲线救国。
    - 因为我的笔记本是 openSUSE，直接跑 debian-headless 的 Makefile 各种报错，手动用 zypper 安装各项依赖，遇到 genisoimage 报错 `option '-e' is ambiguous;`
      - 换了好几个 OBS 源的 genisoimage 都没解决问题，最后在 stackoverflow 上找到[解决方法](https://stackoverflow.com/questions/31831268/genisoimage-and-uefi) - 写了一个 10 来行的 bash 脚本作为 wrapper，问题解决。
    - 镜像终于打出来了，但是在写入之前我用 qemu 测试，又遇到坑：每次都卡在设置 Root 密码这一步
      - 重新使用 debian 官方提供的 `example-pressed.cfg` 改了一份 `preseed.cfg`，发现就能正常提示我，接下来需要 ssh 进去进行后续设置了。
      - 其中关键修改可能是添加了 `d-i netcfg/wireless_wep string` 这一行，因为 UM560 是带 WIFI 6E 网卡的...
    - 又是一番折腾，还额外安装了 clash 进行安装加速，终于给 UM560 装上了 Debian 并进一步装上了 Proxmox VE
  - Beelink GTR5 AMD Ryzen 9 5900H 踩坑记录：
    - 使用同样的流程安装，每次都卡住...
    - 猜测原因是 GTR5 是双 RJ45 接口，`preseed.cfg` 需要做针对性调整，但是又调了两个小时，还是没解决...
    - 主要问题是主机没有串口，我也没串口连接线，显示器啥都不显示，根本看不到安装卡在了哪...
    - 可能的解决方法：
      - 直指本质：买一个键盘或者借一个键盘...
      - 就要折腾：路由器上能看到 GTR5 的主机 IP 是 `0.0.0.0`，也能看到 MAC 地址，说明 ARP 协议已经通过了，但是卡在了 DHCP 协议这里。或许可以在 DHCP 服务器上做些文章，只要 IP 分配成功了，应该就能直接通过 ssh 协议连接上去试试了。
      - The Hardest Way：再研究下 PXE 网络装机，但是感觉大概率遇到同样的问题...
    - 折腾到第二天早上 7 点多还没解决，最后京东下单了一个键盘...
- Proxmox VE 踩坑记录（一年多没用了，把以前踩过的坑又踩一遍...）
  - 详见官方文档 [Network Configuration -Proxmox VE](https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysadmin_network_configuration)
  - Linux Bridge: 即网络桥接，虚拟机与外部主机共享网络
    - 默认情况下 PVE 会将 IP 地址、网关、掩码都配置在 eno1 物理网卡上
    - 首先先记下 eno1 网卡的参数，并将其 IP 地址、网关、掩码三个参数清空掉
    - 然后新建网桥 vmbr0，将之前记录的 eno1 网卡的 IP 地址、网关、掩码都配置在此网桥上，bridge-port 填 eno1
    - 点击应用配置即完成创建
    - 新手常见问题（仅在 debian 上装 PVE 时才会发生，测试发现直接使用 iso 安装无此问题）：
      - 未清除 eno1 网卡参数，导致创建 vmbr0 时提示无法将 bridge-port 设为 eno1
      - 未清除 eno1 网卡参数，导致用错误的参数创建好 vmbr0 后，由于底层 ARP 协议混乱，整个外部局域网都出现网络时好时坏的情况。
  - 路由模式：其实仍然是创建一个 Linux Bridge，不过我们通过配置可以把它当成二级子路由器用，准确的说这种模式叫「**Proxy-ARP Transparent Router**」
    - 此功能目前无法通过 UI 配置，必须命令行改配置才行。需要在 eno1 网卡上设置 ip_forward 跟 prox_arp 相关参数。
    - 因为路由模式不修改内外网的 IP，这要求在外部网络的路由表中添加子路由器的网段配置。
    - 详见官方文档，此模式的实际玩法待测试，上述均属我的猜测。
  - NAT 网关模式：路由模式仅工作在 L3 网络层，而 NAT 更进一步，使用 Iptables 将 IP 与 L4 的端口一并做了修改。
    - 好处是内部网络就跟外部网络完全隔离了，安全性啥的更高。而且不需要额外修改外部网络的路由规则。
- K3s 问题
  - 在 raspberrypi 上遇到 [Fail running on Raspberry Pi Ubuntu 21.10](https://github.com/k3s-io/k3s/issues/4234#issuecomment-947954002) 这个问题，跑了下 `sudo apt install linux-modules-extra-raspi` 再重启问题就解决了。
  - 新版本 k8s 需要指定 ingressClassName，但是 k3s 默认没有创建 ingressClass : [Create by default traefik ingressClass when creating a cluster](https://github.com/k3s-io/k3s/issues/556
  - 在 1.25 版的 k3s 集群上安装 victoria-metrics-k8s-stack 时，operator 一直报错，排查日志发现是 `policy/v1beta1` 被废弃导致的，顺手提了个 PR [fix: bump victoria-metrics-operator's version to 0.15.*](https://github.com/VictoriaMetrics/helm-charts/pull/401)


### 2022-11-03

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 57/100
  - The Time Machine                          - 21/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 58/270
- 上班：大数据服务遭遇性能瓶颈，发送 kafka 延迟高涨。
  - 因为节点没安装 node-exporter 没法看监控，手动跑了一堆 sysstat 相关的命令分析网络 IO、磁盘 IO，以及一堆其他命令分析 TCP 连接、CPU 利用率等等，都很正常...（再次确认 node-exporter 有多么方便...）
  - 最后通过 **kubectl-flame 画火焰图**，定位到是启用了 gzip 压缩耗时很长。改成不压缩后估算发现 kafka 带宽顶不住全部流量，最后改成 lz4 压缩算法解决，平衡了客户端压缩性能与贷款消耗。
  - 同时也了解到 alibaba 开源的 arthas 也能做同样的工作。
- 折腾硬件
  - 买的 mini 主机 MINISFORUM UM560 到货了，装好固态、内存条后，想到自己没有显示器...装机很麻烦
    - 研究了一下 [Proxmox 网络装机](https://pve.proxmox.com/wiki/Unattended_installation_of_Proxmox)，感觉太麻烦，放弃该方案。
    - 想着利用上手上的平板或者笔记本显示屏，一番研究后在京东下单一根 80 块的 1080p HDMI 转 USB/type-c 视频采集卡，输出 UVC 内容。
    - Windows/Linux/Mac 均可通过 [OBS Studio](https://github.com/obsproject/obs-studio) 播放或录制此卡输出，实现将笔记本作为显示器的功能。
    - Android 可安装 [USB OTG camera](https://play.google.com/store/apps/details?id=net.usb.usby6) 或者 [USB Camera](https://play.google.com/store/apps/details?id=com.shenyaocn.android.usbcamera)，同样能把手机或者平板当成显示器用，或者实现视频录制。
    - 如果再补充一根 type-c 转 HDMI 线，就能实现录制 Android 设备的输出了。
    - 把采集卡插 PC 上，就能把平板或者另一台笔记本当成副屏使用，很期待解锁此项新玩法~
  - 买的 WIFI6 双频路由器 中兴 ZTE AX5400Pro+ 到货了，简单体验了一把，感觉还行。
    - 打算后续拿它当主路由，再在 UM560 上开个 openwrt 虚拟机当旁路由。
    - 实现很简单，改下主路由 DHCP 分配的默认网关 IP 即可。

### 2022-10-29

- 发现了老板的博客 [我的时光记忆](http://dingjichang.com/)，记录了 2013 年到 2021 年每一年的年度总结。
  - 显然现在能说，老板年初对 2022 年的看法太乐观了，年初的计划已经随着这次裁员一起被推翻。
  - 本来去年年底的时候感觉自己在大宇站稳了脚跟，可现在又感觉到迷茫了。

### 2022-10-27 - 2022-10-28

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 51/100
  - The Time Machine                          - 17/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 52/270
- 跟朋友及同事聊了聊近况，网关技术、Web3，以及个人发展
- 大宇方向与团队结构调整，送走了很多人，包括去年带我一起冲浪的算法大佬。
  - 这短短两天，真的走了好多超强的大佬啊，其中很多在公司都呆了四五年了，当然也不乏才进公司不到一年的新人。第一次遇到这种场面，难免有些 emo
  - 翻了翻公司的邮件组，emo 之余，也能感觉到公司早期的时候，内部氛围真的很好，互相分享韩语、日语、设计技能。
- 因为一些意外，发现了大宇前 FE Leader 的博客，读了 [[Review] 2020](https://github.com/JasKang/blog/issues/11)，对做开源项目有了些新的感悟。


### 2022-10-23

- 看了些动态规划算法相关的文章，感觉很有意思
  - [动态规划详解进阶](https://github.com/jiajunhua/labuladong-fucking-algorithm/blob/master/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E7%B3%BB%E5%88%97/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E8%AF%A6%E8%A7%A3%E8%BF%9B%E9%98%B6.md)
  - [动态规划之四键键盘](https://github.com/jiajunhua/labuladong-fucking-algorithm/blob/master/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E7%B3%BB%E5%88%97/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E4%B9%8B%E5%9B%9B%E9%94%AE%E9%94%AE%E7%9B%98.md)
  - 起因是群友「山」想要使用动态规划算法，基于「编码表」自动分析出句子的「最短理论编码」。
  - 目前打字领域许多拆字工具、赛码器，底层实际都是基于「前缀匹配」+「按词长降序搜索」这样的思路进行句子的编码分析，但这样只能搜到一个此框架下的「相对最优解」。
    - 举个例子，使用小鹤码表时，前缀匹配思路下，只能搜到「我想 想象 一下」这种拆分，但实际上「我 想想 象 一下」才是「理论最优解」，比前一种拆分要短一码。
    - 通常来说用「相对最优解」来拆分也够用了，因为这种边际情况应该不多，所以问题也不大。
    - 不过如果追求完美，那大概就得学学「最短路径算法」，直接暴力搜索的思路大概如下（输入为一个中文句子）：
      1. 从句子第一个字符出发，首先从码表中找到这个位置所有可能的编码，它们就是下一跳的所有节点，并计算出到这些节点为止的行进路线、总的码长。
      2. 从上述所有节点出发，再去找到所有下一步所有可能的编码，同样计算出当前行进路线、总的码长。
      3. 这样递归直到句子迭代完毕
      4. 最终计算出总码长最短的路线，就是最短路径，它的编码就是「最短理论编码」。
  - 基于「动态规划」去优化「最短理论编码」算法，关键点在于它的「重叠子问题」是哪个？
- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 46/100
  - The Time Machine                          - 9/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 47/270

### 2022-10-19 - 2022-10-20

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 43/100
  - The Time Machine                          - 4/30
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 44/270
- 在英语学习规划中补充了 Cambly/Lingoda 等口语练习站点
- 在「一点英语」上过一遍 96 个单词，大概需要 90mins 的时间，另外在薄荷英语+知米阅读上还需要花差不多 40mins
- 发现最近英语学习成了我业余生活的主旋律，每天花大概 130mins 在英语学习上，基本上工作日没有任何时间去学习 Linux 跟 TCP/IP 了
  - 同时「下班没事干综合征」跟「网络小说成瘾」也被英语学习治好了...

### 2022-10-18

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 41/100
  - 感觉薄荷英语小程序做得不太行，一番查找发现了价格更亲民，小程序也做得更好的「知米阅读」，花 199 买了它的年费会员。并且开始在「知米阅读」上看《The Time Machine》这本书。
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 42/270
- 使用 [Test Your Vocabulary](https://preply.com/en/learn/english/test-your-vocab) 做了一次词汇量评估，发现相比去年词汇量上升了大概 400 词（隐约记得去年测试大概是 4700 左右）。说明最近的单词跟阅读学习，效果显著，有点成就感~
  - 目标词汇量增加速度：每天约 20 个单词，再用 5 个月的时间完成 8000 词的目标。
  - 也不能忽视「熟词生义」跟「词组」学习，这个主要通过「薄荷阅读」跟「知米阅读」来补充。
- 英语语法可以再放一放，等词汇量上来，后面再一次性补齐短板。

![](/images/learn-english-again/2022-10-18-test-your-vocabulary-result.webp "2022-10-18 词汇量测试结果：5100 词")

### 2022-10-17

- 英语阅读
  - The Unlikely Pilgrimage of Harold Fry - 40/100
- 英语单词与听力练习
  - 一点英语 270 天英语学习                  - 41/270
- 英语语法
  - 《英语语法新思维——初级教程》              - 8/366

### 2022-10-15 - 2022-10-16

- TCP/IP Illustrated, Volume 1, 2nd Edition 读完第一章 - 进度 31/920
  - 我以前听说这本书是 TCP/IP 圣经，一直望而却步，这次实际一读发现，第一卷还挺简单直观的
- 跟 0xFFFF 社区的朋友交流，积累了一点有价值的讨论：[记 QQ 群里一次关于日常笔记、学习规划、学习节奏的讨论](https://0xffff.one/d/1352-ji-qq-qun-li-yi-ci-guan-yu-ri-chang)
- 打游戏学英语，玩了玩 Genshin Impact 跟 Deemo 2，体验挺不错的。
- The Unlikely Pilgrimage of Harold Fry - 39/100
- 一点英语 270 天英语学习                  - 40/270

![](/images/learn-english-again/genshin-impact-noelle.webp "超飒的重剑女仆 Noelle")

![](/images/learn-english-again/demo2-talk-1.webp "DEEMO 2 中丰富的对话内容")

![](/images/learn-english-again/demo2-collections.webp "DEEMO 2 的一些设定")

### 2022-10-13

- 跟网友们分享自己做 [/history](/history) 跟 [/now](/now) 这两个页面的经验。
  - 我是从入职新公司开始，尝试在博客上做 /now 页面的，灵感来源于其他博友的 /now 页面。一开始直接断更了 5 个月，因为不知道写啥。到了今年 2 月份才慢慢找到感觉。
  - 写得多了发现自己的 /now 变成了单纯的流水账，缺少规划。就将 /now 的内容改成了「当前进展 + 学习规划」，而历史记录则拆分到了 /history。
  - 当然有内容可写肯定不是这个 /history 的功劳。更多的是因为找到了学习状态，学的东西多了，做的东西也更有意思了。另外日常读到看到一些内容，我也会尝试去做一些深度思考，跟朋友探讨交流，而不是一笔带过。如果觉得其中一些较长的探讨内容有价值，我会临时粘贴到手机记事本上，晚上再把它们整理到这个 /history 页面。
  - 如果发现其中一些想法有成文的价值，我会考虑把它们进行增补，形成一篇博客发表出来。最近的「Learn English Again」跟「刻意练习」两篇文章，就都来源于我跟朋友的群聊记录。

### 2022-10-12

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 35/100
  - 一点英语 270 天英语学习                  - 36/270
  - 重新读了一遍恶魔奶爸分享的词典文章，在平板上用欧路词典配置好了所有双解词典、英英词典、搭配用法词典、词根词缀 vocabulary builder。确实很好用。


### 2022-10-11

- 调研市面上的开源笔记软件，主要有双向链接、多维表格两大类。
  - 我的需求：
    1. 能使用 git 来管理笔记版本
    2. 使用 markdown 等流行文本格式编写笔记内容。
    3. 听说双链很牛逼，所以希望希望支持双链
    4. 希望能像 notion 一样，拥有更灵活的排版格式
    5. 希望能导出成静态站点
  - 最后我选择了 logseq，因为多维表格类的笔记软件目前没有特别出彩的，而且它的存储格式是个问题——markdown 的特性太弱不足以支撑多维表格的特性。而且 logseq 进阶可以用 emacs org mode，虽然没用过但是听说是功能更丰富的排版格式。
  - logseq 能直接导出成站点，但是目前还不支持自定义导出站点的样式（默认的暗色主题有点丑...）


### 2022-10-06 - 2022-10-08

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 31/100
  - 一点英语 270 天英语学习                  - 32/270
  - 打 galgame 学英语（剧情吸引人，日常用语跟某方面的词汇量也很丰富...）
    - 找英文 galgame 了解到一个黄油社区 f95zone...

### 2022-10-05

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 28/100
  - 一点英语 270 天英语学习                  - 29/270
  - 打 galgame 学英语（剧情吸引人，日常用语跟某方面的词汇量也很丰富...）
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 296/572
  - 完成了习题 12-3

### 2022-10-04

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 27/100
  - 一点英语 270 天英语学习                  - 28/270
  - 打 galgame 学英语（剧情吸引人，日常用语跟某方面的词汇量也很丰富...）
- 看完了《赛博朋克：边缘行者》
  - 剧情比较狗血，不带脑子看还是很爽的。
  - 赛博朋克世界底层人民的反抗，结局是血淋淋的，主角跟女二都直接没了。
  - 豆瓣上一条评语我很认同：浪漫、残酷、疯狂。

### 2022-10-01 - 2022-10-03

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 26/100
  - 一点英语 270 天英语学习                  - 27/270
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 296/572
  - 看完了 I/O 缓冲、文件系统、目录跟链接，而文件属性、拓展属性、ACL 不太感兴趣，就走马观花看了看。
  - 完成了 12 章的习题 1 跟 2，不太熟悉 C 语言，还是有点费劲的。

### 2022-09-30

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 23/100
  - 一点英语 270 天英语学习                  - 24/270
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 190/572
  - 完成第 12 章 /prod 文件系统与 uname 系统调用，明天做下习题。

### 2022-09-29

- 国庆回家度假
- 英语
  - The Unlikely Pilgrimage of Harold Fry - 22/100
  - 一点英语 270 天英语学习
    - 回到家后，忘记了打卡。虽然早就知道连续打卡 270 天很难，不过还是很错愕，居然在第 23 天就断掉了。

### 2022-09-26

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 19/100
  - 一点英语 270 天英语学习                  - 20/270
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 174/572
  - 略读了「进程凭证」、「时间」「系统限制与选项」三章，因为对其内容不太感兴趣，跳过了习题。
  - 第 12 章讲 /proc 我比较感兴趣，明天读


### 2022-09-24 - 2022-09-25

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 18/100
  - 一点英语 270 天英语学习                  - 19/270
    - 试了下每天靠通视频语料背 80 个单词（包含复习每日复习），花了 100 分钟，难度略高。暂时改成 50 个明天试试看。
  - [American Pronunciation Workshop](https://www.bilibili.com/video/BV1Ts411m7EU/) 美语发音教程 - 一周目 2/16

另外在 twitter 上看到了 [待业五年后的找工作经历](https://greyli.com/job-hunting/) 这篇文章，读完之后，敬佩之余也想到一个问题：「**如此专注在某一个很小的领域，在世俗意义上到底能取得多大的成功**？」

这位文章作者毕业五年一直没找工作，开源项目也仅仅专注于 Flask 开发跟写各种布道的文章、书籍。
从绝大部分公司普通公司的角度来讲，他的技术栈显然是不合格的，Java/Go 性能都秒杀 Python，Flask 你懂的再多也没用。
也因为这个原因，作者面了这么多公司，最终没几个拿到 offer.

但是作者确实取得了名望。
他的书写得不错，在技术圈里广受好评。
还组织过两场国内 PyCon 技术大会，技术圈内小有名气。
还运营了 hello-flask 社区，并且长期参与 flask 的开发维护，Github 跟 Twitter 上都有上万 followers.

而且现在，他也确实凭借自己的能力进了外企（即使有 90% 的职位都拒绝了他）。

感觉这位作者的经历，是我此前从未发现的一条出路，虽然这条出路很窄，他的成功也很难复制。

我目前从中学到两点：

- **得把英语学好**（我正在做这件事）
- **专注一个子领域深耕，才是提升技术能力跟影响力的捷径**！啥都想学的结果只会是不断上赶着追逐别人创造的知识，啥都不精。

### 2022-09-23

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 16/100
  - 一点英语 270 天英语学习                  - 17/270
  - [American Pronunciation Workshop](https://www.bilibili.com/video/BV1Ts411m7EU/) 美语发音教程 - 一周目 1/16
  - 多抓鱼上下单了《English Grammer In Use》跟《赖世雄经典英语语法》，语法几乎全忘光了，这次打算补一补语法
  - z-library 上下载了《Key words for fluency》前两本书，因为发现自己口语经常不太会表达自己的想法，打算靠这个补补看

### 2022-09-21

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 14/100
  - 一点英语 270 天英语学习                  - 15/270
- [APISIX 504 问题](https://github.com/apache/apisix/issues/7934)
  - 周会同步，同事提示我 node-exporter 的 network traffic 部分就有列出 nf_conntrack 表的监控。但是因为环境问题，我跑 APISIX 这批机器刚好没整这个监控...再次确认了完善的监控功能的重要性
  - 调整 nf_conntrack 相关参数后，问题暂时解决了。但是接下来遇到 TCP 连接数无法超过 65535 的问题，导致 504 报错...
    - 按理说我 nginx 有两个 worker，`worker_connections` 也设置到了 65535，至少应该也能撑住 65535 * 2 的连接数量？
    - 发现 alloc : orphaned : timewait 三类 TCP 连接数的比值大概为 66% : 13% : 21%，`dmesg` 命令能看到很多这样的错误：`TCP: too many orphaned sockets`
    - 搜索一番确定 orphaned 连接太多一般有两种可能：一是 tcp 连接的内存用尽导致无法为新连接分配内存，二是 TIME_WAIT 导致的 orphaned 连接。所以解决方法是调整 tcp 内存相关参数，启用 TIME_WAIT reuse
- 读了一点《深入理解 Linux 网络》这本书，因为这两天搞 APISIX 网关，深刻意识到自己对相关知识缺乏了解

### 2022-09-20

- 英语
  - The Unlikely Pilgrimage of Harold Fry - 13/100
  - 一点英语 270 天英语学习                  - 14/270
  - Moon Palace, by Pual Auster           - 10.6%
- [APISIX 504 问题](https://github.com/apache/apisix/issues/7934)
  - 上周给这个 case 提了个 issue 到 APISIX 社区，但是官方给出的思路并无参考价值。
  - 今天晚上左思右想，最可能还是 TCP/IP 协议栈有问题，网上搜了下「丢包 504 超时」，然后根据找到的流程排查了一下，第二个排查项直接命中，就是 nf_conntrack 满了导致的问题！
    - 就好像是找到了正确的房门钥匙是「丢包 超时 排查」，困扰我好几天的问题，瞬间就找到了突破口。
  - 此问题相关的笔记，我后续会在 [Linux 504 超时丢包问题解决思路.md](https://github.com/ryan4yin/knowledge/blob/master/linux/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/Linux%20504%20%E8%B6%85%E6%97%B6%E4%B8%A2%E5%8C%85%E9%97%AE%E9%A2%98%E8%A7%A3%E5%86%B3%E6%80%9D%E8%B7%AF.md) 更新


### 2022-09-18

- 沉迷学英语...
  - 薄荷英语 100 天阅读一本英文书 - 11/100
  - 一点英语 270 天英语学习      - 12/270
  - Moon Palace, by Paul Auster - 6.5%
- 完成 TLPI 第 5/6 章的习题
  - 习题告诉我 longjmp 是个大坑，能不用千万别用，出错的现象太诡异了。

### 2022-09-15 - 2022-09-17

- 沉迷学英语...
  - 薄荷英语 100 天阅读一本英文书 - 10/100
  - 一点英语 270 天英语学习      - 11/270
  - Moon Palace, by Paul Auster - 4.2%
- 最近一直在跟薄荷英语的原版书课程《The Unlikely Pilgrimage of Harold Fry》，就想再次挑战下自己直接去读英文原版书。结果发现 Paul Auster 的《Moon Palace》意外地好读，生词很少，读得很流畅。
  - 然后又陆续试了下《Sophie's World》、《Majo no Tabitabi（魔女之旅）》，难度都不高，只有《Tasogare-iro no Uta Tsukai（黄昏色的咏使）》生词偏多，读着费劲。
- 阅读了几篇介绍向量数据库与相似度检索技术的文章，写得非常简洁直观
  - 大概介绍了基于倒排索引的传统文本检索方式的缺点，以及基于向量的相似度检索如何对其形成降维打击，以及如何用简单的几行 Python 代码，实现基于向量的相似度检索功能。
  - [向量数据库入坑指南：聊聊来自元宇宙大厂 Meta 的相似度检索技术 Faiss](https://soulteary.com/2022/09/03/vector-database-guide-talk-about-the-similarity-retrieval-technology-from-metaverse-big-company-faiss.html)
  - [向量数据库入坑：传统文本检索方式的降维打击，使用 Faiss 实现向量语义检索](https://soulteary.com/2022/09/10/the-dimensionality-reduction-of-traditional-text-retrieval-methods-using-faiss-to-achieve-vector-semantic-retrieval.html)

### 2022-09-13 - 2022-09-14

- 学英语
- 完成 TLPI 练习题 4-1 与 4-2，节奏是每天晚上完成一个习题
  - 有点慢，不过毕竟是起步阶段，也能接受。
  - 习题 4-1 主要考察如何读写文件，如何使用 getopt 函数解析命令行参数
  - 习题 4-2 主要考察如何读写含有空洞的文件，主要就是遍历缓存空间，并使用 `lseek` 跳过空洞部分的写入操作。

### 2022-09-12

- 学英语
- 看了 TLPI 作者的演讲 [Kernel Recipes 2022 - Once upon an API](https://www.youtube.com/watch?v=l-i1DVjlAyA&t=2047s)
  - 以 prctl 为例介绍了 Linux 中一个 API 的错误设计如何影响到 Linux 的其他部分，而且因为缺少文档，也没人维护，其中部分问题直到十多年后才被发现。为了兼容性，这些错误的设计就成了永远不可能被修复的 bug
  - socket api 中有一些错误设计已经在 Linux 中存在了近 40 年，这类错误设计给 Linux 系统编程造成了太多的痛苦。
  - 还有 inotify api、cgroup v1，都是错误设计的典型，它们产生了很多作用，但是考虑的问题都过于片面，由此引发了许多问题。
  - 介绍了可用于避免这些 API 错误设计的一些方法。
- 看了 TLPI 作者的演讲 [An introduction to control groups (cgroups) version 2 - Michael Kerrisk - NDC TechTown 2021](https://www.youtube.com/watch?v=kcnFQgg9ToY&t=2162s)
  - 主要介绍了 cgroup v2 的历史，演示了如何使用 cgroup v2 进行 cpu/pid 限制，以及如何使用嵌套 cgroup v2 进行更细粒度的资源限制。
  - 发现 cgroup v2 跟目前内核领域最火的 eBPF 也有些交互，有点意思。
- TLPI 作者做了很多 cgroup/namespaces/capability model/seccomp 的演讲，可以在 [Conference presentations - man7.org](https://man7.org/conf/index.html) 中找到，有时间再看看其他的。

### 2022-09-11

- 学英语
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 136/572
  - 这本书的主要内容就是在介绍 Linux 的各种 C 语言 API，跟想象中的还是有些不一样。（我以为可能像《深入理解 Linux 内核》一样，还会讲内核的一些实现细节。）
    - 也能感觉到 Linux 中也存在相当多的历史包袱，比如说一个文件描述符复制就有 `dup()` `dup2()` `dup3()` 三个函数可用，大文件读写的支持也有好几种实现方式，另外标准 API 中错误值返回方式也存在一些特例需要记忆。总之就是很多地方都有补丁的痕迹，Linux 在不断地进化，许多旧的 API 会慢慢被弃用，新的 API 也会被不断地添加。
  - 虽然不是很有趣，但是还挺好读的，进度已经差不多 1/4 了。不过今天跳过了所有习题，打算明天把跳过的习题都做一遍（不然读了过两天就忘了，等于没读）
  - 这个月或许能把这本「上册」读完，并且完成对应的练习题。
- 迭代了一波旧文章，修改了几个 typo，调整了部分内容使其更易理解。
- 发现今天距离这份 history 记录的开始时间刚好一年半，犒劳自己一顿？emmmm

### 2022-09-10

- 「英语流利说 懂你英语 A+」的 AI 语音太枯燥，放弃继续该课程，卸载了「英语流利说」。
- 继续「一点英语」、「薄荷阅读」学习打卡
- 参与开言英语的 WeMeet 英语角，又遇到了 Felix，跟几位 partners 聊得很开心~
  - 主要交流了如何通过各类电影、电视剧等材料去学习英语。明确的一点就是单纯为了娱乐看美剧，对学英语的帮助是很小的。
  - 关键就是重复听，一直到不看字幕能听懂的程度，还可以去领会其中词组、语法、句式的用法。
- 下午到晚上在 Discord 的中英交流 Chatting Room 里泡了大半天，很多英语还听不太懂，但是氛围很好，聊得很舒服。
- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/)  - 进度 72/572


### 2022-09-05 - 2022-09-09

- 「一点英语」、「英语流利说 懂你英语 A+」打卡
- 2022-09-08 开始在「薄荷阅读」上阅读《一个人的朝圣》英文原著，体验甚佳~

### 2022-09-04

- 完成文章 [Learn English Again](https://thiscute.world/posts/learn-english-again/)

### 2022-09-03

- 试用了常见的各种英语学习软件，做了[一些笔记](https://github.com/ryan4yin/knowledge/tree/master/natural-language/english)
  - 为了提升阅读能力，购买了薄荷阅读 199 块钱 100 天会员，选的书是《一个人个朝圣》
  - 各个软件都做了一波能力测评，我目前的英语水平应该属于 CEFR 框架的 B1 到 B2 之间，其中最差的是语法跟口语交流能力，其次是词汇量。
  - 各英语学习软件使用体验（仅体验了匹配我当前水平的课程）
    - 流利说挺好用的，价格是 198 元 / 每月
    - 一点英语 APP 测出的水平测评偏高，但是它基于各种视频资料的学习过程真的做得很有趣~ 但是价格也比流利说贵了很多。
    - 开言英语是专业外教录制的视频课，体验也还不错，价格比流利说略高一点，2598 元一年。

![](/images/now/ryan4yin-english-level.webp "各 APP 的英语水平测评结果（一点英语的结果明显偏高）")

### 2022-09-02

- 偶然发现手机桌面上有一个安装了好久但是一直没用过的 APP 英语流利说，顺手用它测了下自己的英文水平
  - 流利说把英语分成 7 个 Level，它评价我属于 Lv.5。五个评级维度中我的发音是最好的，口语是最差的。而词汇量大概在 5000 这个档位（我觉得如果算上我懂的计算机名词可能会更高些 emmmm）。
  - 测出的结果跟我的自我感觉基本吻合，之前有跟 AWS 工程师做过几次英语沟通，发现我的口语勉强可以支撑日常技术沟通，但是感觉很费劲，原因显然是口语基本没怎么练过。而我的发音之所以好，主要是大三的时候专门跟着奶爸推荐的《赖世雄美语音标》、《American Spoken English》等资料练习过。
  - 深入探索了下英语流利说这个 APP，花 49 元买了一个月的个性化学习计划，还给分配微信学习社群跟班主任，每天坚持 30 到 60 分钟。第一天体验这个学习计划，感觉确实跟我比较契合，而且也不枯燥，打算坚持一个月试试。
  - 我学英语的目的：听说能力（日常对话）、阅读各类英文资料、写英文博客。
    - 听说能力（日常对话）：已经测过非常差了，亟待提升。
    - 阅读：目前可以无障碍阅读大多数编程相关的博客跟文档，但是我对自己的阅读速度以及词汇量还不够满意。
    - 写作：语法这么差，词汇量又低，而且高中后基本就没怎么练过英文写作，我的写作能力显然还有很大的提升空间。
- 英语流利说「懂你英语 A+ 学习计划」34 课 - 进度 1/34

### 2022-08-31

- 排查与解决了博客的一个隐藏 bug，记录下排查的思路与流程（省略了其中一些探索性的、方向不正确的步骤）
  1. 朋友反馈站点评论系统登录异常，我着手排查
  2. 通过 firefox devtools 定位到是点击登录后被重定向到了错误的页面
  3. 进一步确认是 utterances 的登录按钮上的 redirect url 参数有问题
  4. 在 DoIT 主题的 issues、代码中寻找 utterances 相关逻辑，未发现问题
  5. 尝试在 utterances issues 中搜索关键字 redirect，找到 https://github.com/utterance/utterances/issues/474
  6. 定位到是页面跳转时仅做了局部刷新，未更新 header 中的 canonical link 导致的问题。
  7. 进一步排查到 DoIt 主题使用了 PaperStrike/Pjax 做页面局部刷新，目的是提升性能
  8. 阅读 Pjax README 发现它的初始化代码格式为 `new Pjax({...})`，尝试在主题中搜索关键字 `new Pjax({` ，找到对应的代码块
  9. 找前端的朋友给了个 canonical link 的 CSS 选择语法，使用该语法修改主题，测试发现问题解决
  10. 提 PR 给这个 Hugo 主题的 github 仓库: https://github.com/HEIGE-PCloud/DoIt/pull/709
  11. 总共用时大约 1h
- 逛 [@Bensz](https://blognas.hwb0307.com/me) 的友链时，发现 [APISIX高级路由之通过Body参数转发请求 - 张戈博客](https://zhangge.net/5157.html)这篇文章，它为我正在解决的一个问题提供了非常优雅的思路——使用 apisix `route` 的 `filter_func` 功能，真的是意外之喜~

### 2022-08-28

一直很疑惑，我站点的访客数一直是起起伏伏，但是站点的流量却越来越高。而且流量是平缓地上涨，也不像是有人在恶意刷我流量。

之前没有做过详细的排查，不过觉得估计是跟图片啥的有关吧，把图片全换成了 webp，体积下降约 80%。
但是发现图片这波优化对流量没有任何帮助，流量还是在缓慢上升...

今天跟朋友讨论时，突然发现居然是 `index.xml` 在跑我的流量，我之前一直以为这个地方显示的是 `index.html` 首页，就没觉得它有问题...

最后确认这个是我站点的 RSS Feed 文件，也就是 RSS 订阅造成的。
我全站现在一个月也就大概 80G 流量，其中接近 90% 都是这个 RSS Feed 跑出来的 —_—||

排查之下发现是之前为了 RSS 订阅的体验，把所有文章的内容都嵌进去了，导致体积有 2.8M，可能因为订阅量越来越多，以及 RSS 订阅的周期性拉取，导致数据量一直在涨。

解决方法：

做了一波修改，现在只将最新的 15 篇文章内容嵌入到 RSS 里，其他文章只给个标题跟原文 URL，使 RSS Feed 文件的大小降到了 700K，暂时应该不用担心 Vercel 流量用光了...

![](/images/now/rss-feed-used-too-much-traffic.webp)


### 2022-08-25

- 根据 [APISIX 官方建议](https://github.com/apache/apisix/discussions/7773)，使用 `priority=-1` 跟 `proxy_next_upstream` 实现了请求的 fallback 功能，赞一个。
  - 直接使用 k8s service FQDN 作为 node host 了，因此实质是通过 APISIX + kube-proxy 实现的功能，kube-proxy 负责在 pods 之间做四层负载均衡，负载测试也很正常。
  - 在上游服务挂掉的情况下，所有请求都会首先尝试请求默认服务直到超时，这会导致延迟暴增，所以建议尽量调低 APISIX upstream 中的几个超时时间。
  - 在使用 APISIX 的 proxy-mirror 插件时也遇到了超时的问题，mirror 服务器挂掉导致请求延迟暴增，原因是未调整 proxy-mirror 插件的超时时间，所有请求都会卡在 mirror 请求这里，一直等待完 60s... 将 proxy-mirror 插件的超时时间调整为 `300ms` 后解决了这个问题。

### 2022-08-25

- 有个 HTTP 请求失败后 fallback 到备份服务器的需求，想写个 lua 插件来支持它，在 Github 上咨询 APISIX，聊了两天官方一直建议我看看这个 `nginx_next_retry`，之前一直感觉不太合适，APISIX 的文档也语焉不详，但是今天研究了一波 Nginx/OpenResty 的官方文档，好像又有戏 hhhh
  - https://github.com/apache/apisix/discussions/7773
    - 重点有二，一是设置 `proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_403 http_404 http_429 non_idempotent;`，二是设置 node 的 `priority=-1`
  - 也思考了一波，这类需求很特殊的专用网关，到底应该用 Envoy 还是 APISIX/OpenResty，还是说自己写一个...
- 了解 zig 语言时，读到一篇写得很好的[现代化 C 使用体验](https://liujiacai.net/blog/2022/04/30/modern-c/)，写得很好

### 2022-08-21

- 为了练习 C 语言，使用 ffmpeg 完成了一个 video2ascii 项目
  - 项目地址 [video2ascii-c](https://github.com/ryan4yin/video2ascii-c)
  - 花了较长时间研究 Makefile 语法跟 clang 的参数，然后又花了很长时间熟悉 ffmpeg 的 api
  - 目前已经集齐用五种不同语言实现的 video2ascii 工具，除了 C 语言是调用的原生 API 外，其他语言都是使用 ffmpeg/opencv 的 wrapper 实现的。


### 2022-08-20

- 读完 The ANSI C Programming Language
  - 笔记：[C 语言笔记](https://github.com/ryan4yin/knowledge/tree/master/pl/c)
  - 明天写几个小程序练练手，比如 video2chars 哈哈
- C 语言补完了，开始读 [Linux/Unix 系统编程手册](https://man7.org/tlpi/) - 进度 56/572
  - 挺好读的，慢慢来感觉了~

![](/images/now/the-asni-c-programming-language.webp "The ANSI C Programming Language")

![](/images/now/the-linux-programming-interface.webp "Linux/Unix 系统编程手册（上册）")


### 2022-08-19

- Nginx 网关的 TLS 加密：打算换一个思路，用 APISIX 搞个网关再测一波。下周搞搞看吧
- 晚上读完了《在峡江的转弯处 - 陈行甲人生笔记》
  - 这本书写得极好，作者分享的洞见非常契合我，感觉于我是很有益的。
  - 文字中的感情相当丰富，有人在豆瓣上评论说为此感觉到不适，可我觉得这才是真性情，如此丰富的感情其实正说明了作者的感性，以及对生活的态度。因为看到这样亮眼的光芒而难以直视的人，或许只是因为待在黑暗中太久了（如果是大四颓废的我读这本书，大概就会是这个感觉吧）。
  - 在这里，我也用书中一句话来回答一下 2017 年 2 月 6 日写下「[山岭就像时间一样看不到边，翻过了一座又是一座，这又是一种更大的痛苦](https://thiscute.world/posts/the-holiday-is-coming-to-an-end/)」的我，告诉他我现在的想法是「脚下虽有万水千山，但行者必至。」至于我是不是在说空话，事实胜于雄辩，就让时间来证明吧。

![](/images/now/life-notes-of-chenxingjia.webp "陈行甲人生笔记")

### 2022-08-18

- 尝试上线 Nginx Gateway 的 TLS 加密功能，使用了 Google Public CA 提供的三个月有效期 TLS 证书
  - AWS NLB 上观察到大量连接被 Client Reset，tcpdump 抓包后通过 wireshark 分析，确认是大量的 TLS 握手在 `Change Cipher Spec` 这一步后，被客户端强制 RST。正在到处查 TLS 握手的资料...
  - 奇怪的是，TLS 加密功能放量到 0.5% 左右后，各项 QPS、可用率、延迟等指标都没啥明显的变化，客户端上报的业务指标也正常，就好像 RESET 对业务没任何影响一样...
  - 本地压测一切正常，无法复现这个 RESET 问题
  - 还有一个问题是，发现 cert-manager 给出的证书文件包含了域名证书、中间证书、根证书，导致 TLS 握手阶段发一个证书给客户端直接用了 4000 bytes... 有点费流量...
- 听歌，看着《江城》，我意识到一件事——多记日记跟笔记，这样到了想要写些有意思的文字的时候，就能发现手边已经有了大量的一手资料，或者发现自己在这方面的积累还很少，或许现在还不是时机。


### 2022-08-17

- 阅读《在峡江的转弯处 - 陈行甲人生笔记》 - 进度 153/278
  - 第五记「密歇根湖上有一千种飞鸟」，其中有些言行我敬佩不已，有些瞬间让我唏嘘感叹，有些经历我感同身受。
  - 备考清华以及在清华两年学习生涯的描写让我惊觉自己已经工作三年多了，正好仍然是一人吃饱全家不饿的状态，得益于良好的公司文化跟领导带团队的风格，我工作闲暇时间好像也不少，也一直想在业余时间进行一些针对性的学习，提升自己的专业能力跟英文能力。看在大佬们在这个年纪都这么努力的份上，我也应该再加一把劲吧！

### 2022-08-16

- 阅读《在峡江的转弯处 - 陈行甲人生笔记》 - 进度 36/278
  - 读完了第一记「我和我的母亲」，很久没有这样被感动过了。
- 2022 年已经过去三分之二，回过头看看这份记录，发现自己确实还是学了不少东西的。值得肯定，周末犒劳下自己~

### 2022-08-11 - 2022-08-14

- 拿 VISA 信用卡开了个 Azure 云的试用账户，研究了一波。
  - 给 <https://thiscute.world> 加了个 Azure 的 Front Door 作为 vercel 的前置 CDN，发现效果出奇的好！现在站点访问速度跟国内服务器基本没差了，即使缓存不命中，回源速度也特别得快！
    - 不过价格也比较感人，也只有试用阶段才舍得用。
  - 据说 Azure CDN (Microsoft Standard) 在国内虽然比 Front Door 差一点，但是速度也要强过 CloudFalre/CloudFront，试用期之后可以试试。
    - 算了下 Azure CDN 一个月可能也就 10 刀出头，数据即使丢在 Azure Blob Storage 对象存储里，以我不到 1G 的总数据量一个月才不到 1 刀，完全可以接受。
  - 堪称免备案站点加速方案中的战斗机！
- 选 Azure 本来只是因为工作天天接触 AWS/GCP，想试用下全球排名第二的 Azure 是个啥感觉，结果意外发现它的国际 CDN 在国内这么快。
- 当然 Azure 的坑也多，我遇到的有
  - 资源的删除操作存在各种延迟。比如列表还显示该资源，点进去又提示 not available，提示删除失败，但是点进页面资源又已经没了...
  - Azure CDN 的坑
    - 不支持通过 CNAME 绑定根域名，这一点官方没有任何文档说明，但是根据[这个博客](https://arlanblogs.alvarnet.com/adding-a-root-domain-to-azure-cdn-endpoint/)，实际上可以通过添加值为 `cdnverify` 的 CNAME 记录到 `cdnverify.<endpoint-name>.azureedge.net`，就可以解决这个报错...但是即使这样解决了报错信息，仍然存在一个问题——Azure CDN 现在不再给根域名提供 TLS 证书服务，也就是说 HTTPS 没戏了...
    - HTTPS 证书的申请与部署、配置的修改速度特别的慢。
    - 但是 Azure CDN 的上述这些毛病 Azure Front Door 都没有！Azure Front Door 唯一的缺点就是太贵（这或许是我自己的缺点...）
  - 目录是用的 Active Directory，原生的多租户设计，但是感觉真的好难用啊，跟 AWS/Alicloud 的设计区别很大。
  - 所有资源都是 uuid 这一点，感觉不太友好。
  - 删掉了一个旧 CDN endpoint 后，又建了一个跟之前名字一样的 endpoint，结果创建成功了，但是页面到处报错 [s['@odata.type'] is not a function](https://docs.microsoft.com/en-us/answers/questions/964407/s34.html)
    - 2022-08-16 更新：这个 bug 持续四天了，而且我测试站点的 http 端口目前仍然报错... 我怀疑是 rules engine 配置错了，但是这个页面也挂了，现在没办法修改，简直离谱。
    - **不得不说 Azure CDN 是我用过的稳定性最差的 CDN，要不是国内速度确实快，我就直接弃坑了**...
  - CDN 如果把源站改为 custom origin，会有五六分钟的时间疯狂报错 404，之后又莫名其妙地恢复...
- 收费：[Azure 的大部分资源价格](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/#pricing)跟 [AWS](https://aws.amazon.com/cn/ec2/pricing/on-demand/) 相差无几，都是「平民止步」的定价策略。
  - 而且 AWS/Azure/GCP 的出网流量、跨可用区流量都是额外计费的，不像国内云厂商，云服务器跟网络带宽可以绑在一起买。
- InfoQ 翻译了一篇文章 [为了追求速度，我们测试了全球所有的 CDN](https://www.infoq.cn/article/n5tefmdbuvdxkpf8f_hq)，测试了全球的 CDN 速度，画出了一张全球速度最快的 CDN 厂商分布图。其中显示 Azure 的确是中国区域最快的 CDN（仅比较了国际 CDN 服务商，不包含国内）。
- 试用了通过 Github Action azcopy 将站点上传到 Azure Blob Storage，发现上传太慢了，居然跑了 4mins+，权衡之下还是决定先使用 Vercel 作为 CDN 源站，免费而且部署比 Azure Blob Storage 快多了。

### 2022-08-06 - 2022-08-07

- 整理与补充今年 5 月份做的学习笔记《分布式数据库的一致性问题与共识算法》，并发表到博客中
- 极客时间《OpenResty 从入门到实战》
  - 目前市面的网关产品中，性能、可定制性、稳定性三者兼得的仍然只有 openresty
    - 基于 OpenResty 的 APISIX 有丰富的插件，支持插件热加载与配置动态更新，还有实验性的多语言插件支持，长远看或许也是一个很好的选择。
  - 新兴的 envoy 等主推 wasm 插件的网关，性能仍然不如 openresty。另外 envoy 虽然也支持 lua，但是它的 lua 环境没有任何预置的 library，远不如 openresty 这样开箱即用
  - 我目前判断，新兴的 envoy/traefik 等网关的优势在于配置语法简单、支持动态配置。但是如果需要写一些复杂的流量处理逻辑，openresty 仍然是最佳选择。
  - openresty 仍然是最流行的 CDN/软 WAF/边缘网关，在绝大多数公司的网关/CDN 中，都有 openresty 的身影。

### 2022-07-28

- 研究了一波 Nginx 的配置调优
  - 关键点：`reuseport` `aio` `http2` `tls1.3`
  - 相关文章：
    - https://www.nginx.com/blog/performance-tuning-tips-tricks/
    - https://www.nginx.com/blog/tuning-nginx/
    - https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/
    - [【优化】nginx启用reuseport](https://wfhu.gitbooks.io/life/content/chapter7/nginx-enable-reuseport.html)
    - [digitalocean/nginxconfig.io](https://github.com/digitalocean/nginxconfig.io)
    - [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)
    - [nginx-admins-handbook](https://github.com/trimstray/nginx-admins-handbook)

### 2022-07-26

- Misaka 大佬在 twitter 上回复说，ambassador 可能最后会发现都不如 Istio 一把梭
  - 仔细想了下还真挺有道理...毕竟都是 Envoy，而研究一圈发现 ambassador 好像也没比 Istio 多很多功能。目前就看到个不太用得上的 OpenAPI 支持？

### 2022-07-25

- 今天研究了下 CNCF 中的 API 网关
  - 目前发现 ambassador 的文档是比较不错的，我关心的点（Istio 集成、HTTP/3、Gateway API）都有写到，值得研究一波。
  - 目前就找到这么两个 Istio 网关的潜在替代品：ambassador 跟之前研究过的 APISIX
  - 其他的网关项目有的是功能上不太契合、有的是性能差了点、还有的是不够成熟度或者活跃度不够。

### 2022-07-23 - 2022-07-24

- Nginx Gateway 进展
  - 在 AWS NLB 上添加 TLS 终止，遇到 AWS NLB 的 TLS 流量费用高、而且 Nginx 无法通过 `X-Forwarded-Proto` 判断客户端协议的问题
    - 解决方法：使用 cert-manager 在 Nginx 中进行 TLS 终止，AWS NLB 改为纯 TCP
    - 需要注意在 Nginx 上配置使用 OCSP stapling 等 TLS 性能优化手段，并淘汰掉旧的 TLS 协议与 ciphers.
- 研究了一波 cert-manager 通过 ACME 申请权威证书，并绑定到 Istio IngressGateeway 或者其他网关上

### 2022-06-29 - 2022-07-22

- 实施网关优化方案，使用 Go 语言写了一个 Nginx Gateway 控制器
  - 目标：
    - 将目前运行在虚拟机上的 Nginx 搬到 K8s 中运行，通过 Istio Sidecar 接入服务网格，并取代掉当前的 Istio IngressGateway 网关
    - 使用 AWS NLB 作为 Nginx 的前置负载均衡器
  - 功能：包含 Nginx 配置同步与 Reload、AccessLog 日志文件的收集与上传
  - 使用 kubernetes/client-go 监控 configmap/pod 的变动
    - watch 接口不会处理网络问题，失败会直接断开连接，实践中不建议直接使用它！
    - 更建议使用 informer，这是一个带缓存的接口，底层是使用 watch 接口 + 队列实现，而且会自动处理网络问题（自动重连），也提供接口强制更新本地缓存
  - 体验：
    - 是第一次用 Go 语言写项目，体验还不错，编译期检查跟语法提示比 Python 强多了
  - 遇到的问题与解决方法
    - Nginx 无法解析 K8s 内部域名
      - 解决方法：在 `http` 配置块中添加 `resolver kube-dns.kube-system.svc.cluster.local valid=10s;` 即可，另外所有 k8s 域名都得使用 FQDN 形式，因为 Nginx 不会使用搜索域配置！
    - 客户端 Host 透传：改用 `X-Forwarded-Host`，而原 `Host` Header 仅供 Istio/Nginx 用于流量管理。同时在流量走到 Istio SIDECAR_OUTBOUND 时，再通过 Envoy 参数 `host_rewrite_header: X-Forwarded-Host` 将 Host rewrite 回来。
    - 安全组问题：为了获取客户端 IP 需要在 NLB 上启用客户端 IP 透传，但是这样会导致流量被内网安全组拒绝！
      - 解决方法：在 Nginx 所在的 EC2 上添加安全组，允许公网 IP 访问其 http/https 端口即可
    - 使用 aws-load-balancer-controller 绑定 IP 模式的 NLB，发现 pod 被重新调度会导致请求超时！
      - 相关 issue: [pod termination might cause dropped connections](https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2366)
      - 解决方法：在 pod 上设置 350s 的 preStop 以及对应的 terminationGracePeriodSeconds，确保所有请求都能被正常处理！
    - Nginx 注入 Istio Sidecar 后，响应头里带了些 `x-envoy-` 开头的不必要 headers
      - 解决方法：参见 [Istio 去除响应 Headers](https://github.com/ryan4yin/knowledge/blob/master/kubernetes/service_mesh/istio/%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5.md#%E5%85%ADistio-%E5%8E%BB%E9%99%A4%E5%93%8D%E5%BA%94-headers)
    - Istio Sidecar 性能很差，Nginx 与 Sidecar 的 CPU 比值接近 1:2.3
      - 解决方法：为 pod 添加 annotation `traffic.sidecar.istio.io/includeInboundPorts: ""`，即可禁用掉 Istio Sidecar 的 inbound 流量拦截。
    - AWS NLB 跨可用区负载均衡会收跨区流量费
      - 解决方法：关闭跨区负载均衡功能，不同可用区的 Nginx 使用不同的 Deployment+HPA+PDB，就是都独立进行扩缩容。
- 2022/7/20，Leader 告诉我，我上半年的表现出乎他的意料，综合表现上看，得到的绩效评价是 S，第一次拿 S，还是挺开心的。
  - 我的优点：
    - 善于观察与思考，真正做到了目标驱动，积极挖掘各种可能性。
    - 善于将优秀前沿技术落地并取得价值，能够不盲从、玩的转、有落地。

### 2022-06-22

- The ANSI C Programming Language - 83/236
  - 快速过一遍语法

### 2022-06-16 ~ 2022-06-17

- 研究云上网关及 Kubernetes 集群的网络架构优化方案
  - 从之前的「多云+多集群网络方案」，先简化为各集群互相独立的网络方案，之后再往多集群、多云等方向去迭代（迂回策略）。
    - 将遗留的 Nginx 网关直接移到 K8s 集群内，并注入 Sidecar 以接入 Istio 服务网格，由 Sidecar 帮助 Nginx 实现集群内的服务发现、流量切分、多集群支持等能力。好处是遗留的一堆 Nginx 配置基本不需要什么改动，改造难度低，收益明显（动态扩缩容的 Nginx、更短的网关链路、更简洁的配置）。后续还可以逐渐切换到新的 API 网关提升可维护性。
    - Nginx 可以通过云服务商提供的 L4 负载均衡（如 AWS NLB）暴露到公网，也可以自建 keepalived 高可用方案（自己整个 Pod 动态注册控制器，或者搞套静态的节点组都行），不过要注意跨区流量，网关最好是每个可用区单独部署一套，互相隔离。
    - 相当于暂时使用 Nginx+Sidecar 彻底取代掉 Istio 的 IngressGateway。讲道理 Istio 的 IngressGateway 功能还是有点弱
    - 等这个方案实施后，我们可能会考虑使用 APISIX/Traefik 或其他基于 Envoy 的网关来取代掉这个容器化后的 Nginx。目的是提供更简单的网关配置方法，当前写 Nginx 配置的方式还是不太友好。

### 2022-06-13

- [Linux/Unix 系统编程手册（上册）](https://man7.org/tlpi/) - 进度 21/572
- 感觉最近学东西有点随心所欲，东一榔头西一棒槌，感觉自己还在找方向吧。不过 Linux 跟 Kubernetes 开发这两件事应该能坚持下来。

### 2022-06-11

- 《语言学的邀请》- 进度 68/288
  - 感觉解答了一些我以前的对人类的一些疑惑
- 《Intimate Relationship》 - 14/449
  - 读了文化对亲密关系的影响
- 跟堂弟大谈如何怀揣理想，平实生活，一点点地进步。
  谈我们这一代，我想不必悲观也不必绝望，我们的未来由我们自己创造。
  有学术大佬们走在学术前沿，有技术高手们工作在工程一线，我们也完全有能力去做一些有价值的事情，赚更多的钱，也帮助更多的人。

### 2022-06-10

- 读完了《在生命的尽头拥抱你-临终关怀医生手记》
  - 读这本书时，我也在持续回忆我的爷爷奶奶。很难去说明我从这本书中读懂了啥，本质上我只是想从这本书中找到一些慰藉，顺便了解下「死亡」，大概确实部分达成了目标。

### 2022-06-09

- 买了一千多块钱的书，最近陆续到货了，现在还差一本《我的青春恋爱物语果然有问题——原画集》
  - 多买了一本罗翔老师的《圆圈正义》，打算送给堂弟
- 阅读了《Intimate Relationships》的第一小节
  - 了解了人类社会性动物的本质，这可以用进化论解释——越社会性的个体存活率越高，基因也越容易传续。
  - 亲密关系的建立是很容易的，「你是我的唯一」更多的是一种浪漫的说法，只是「因为刚好遇到你」而已。
  - 一旦建立了亲密关系，我们就会抗拒这份亲密关系的解离。当亲密关系遭遇危机时，我们会茶不思饭不想。
  - 在 Youtube 上搜了下 Intimate Relationships，找了几个相关的 TED Talks 看了看。
  - 还找到 UCLA 一个比较老的课程：[Intimate Relationships: Undergraduate Lectures at UCLA](https://www.youtube.com/playlist?list=PLexCQI5fHYIdeWyOSJBclmFL8i4bkBT4H)，可以跟书一起看看。

### 2022-06-08

- 折腾一晚上博客的 Hugo 跟 DoIt 主题
  - 发现本地生成出的站点，mermaid 跟 music 两个插件的问题莫名其妙修复了，怀疑跟今天跑了一波 `brew upgrade` 有关
  - 但是云上 github action 跟 vercel 都还有问题，同样的命令同样的 hugo 版本，本地生成的静态文件 mermaid 跟 aplay 正常加载，云上生成的就有问题，也是醉了...

### 2022-06-05 ~ 2022-06-06

- 观看 [KubeCon + CloudNativeCon 2022](https://www.youtube.com/playlist?list=PLj6h78yzYM2MCEgkd8zH0vJWF7jdQ-GRR) 中我比较感兴趣的部分
  - 主要关注与当前工作相关的点：多云管理、多集群（karmada）管理与应用部署、跨集群网络（Istio）、API 网关
  - 有一些收获，但是都是比较浅的，只能提供个别方向的一些思路，主要还是得靠自己探索。
- 研究了一波 dapr，理念很先进，但是发现很多功能都还处于 alpha 阶段，不太适合向业务侧推广，继续观望吧。

### 2022-05-30 ~ 2022-06-02

- 研究跨云应用部署方案，如 karmada/kubevela
  - 以 karmada 为代表的多集群 Deployment/Service 管理，需要一个控制面集群+多个子集群
    - 配置只往控制面集群部署，karmada 负责按配置在子集群中创建或更新对应的资源
- 研究多云+多集群网络方案
  - 以 Istio 为代表的多集群服务网格，部署模型之一也是控制面集群+多个子集群
    - 配置只往控制面集群部署，istio 会将配置下发到数据面的 sidecar 与 gateway，完成相应的网络配置
  - 其他的如 karmada 等也集成了一些集群间的网络打通方案，但是感觉都还不太成熟
  - cilium 的 service mesh 也是一个潜在的多云 k8s 网络方案，但是还处于 beta 状态，有待观望
- 研究云上 L4/L7 层网关的开源/商业方案
  - 如 L4 的 dpvs/katran 与 L7 的 APISIX/Traefik/Contour，以及 AWS Gateway LoadBalancer
  - 暂时认为云上 L4 还是直接使用云服务商的方案最合适，没必要自己搭
  - L7 为了支持多集群切量，同时尽量缩短链路，目前感觉使用 Istio 最合适
- 研究各跨云网络方案（L7 负载均衡（ADC）、SD-WAN、WireGuard、服务网格等）：
  - 一是多云之间相互隔离，但是长远看不太现实
  - 二是多云使用不冲突的 CIDRs 作为它们的 VPC 网段，然后使用 VPN 把多云网络直接串起来
  - 三是直接在多云上搭建一套 overlay 网络，完全屏蔽掉不同云之间的网络差异
    - 仅针对 k8s 的方案主要是 kilo，基于 wireguard 直接通过公网实现 overlay 网络，但是感觉时延很可能难以接受，还是得用 VPN 才行。
    - 整个云通用的方案目前只有部分供应商在做，而且不开源，有 vendor lock-in 的可能，而且不清楚封装出的具体效果如何


### 2022-05-29

- [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh) - 14.3%
  - 学习第二章：预备知识
    - 微积分：复习了单变量函数的微分（导数） => 多变量函数的偏微分，单变量函数的斜率 => 多变量函数的梯度（梯度，即函数 $f(x)$ 关于输入向量 $x$ 的所有偏微分组成的一个向量）
      - 深度学习模型的训练，即搜索出使损失函数的值最小的模型参数。而梯度下降是应用最广泛的一种损失函数优化方法。
      - 梯度下降，即始终朝着损失函数的梯度值下降的方向进行模型参数的搜索
      - 深度学习中的多元（变量）函数通常是复合的，而链式法则 $\frac{dy}{dx} = \frac{dy}{du} \frac{du}{dx}$ 使我们能够微分复合函数。
    - 自动微分：为了计算梯度我们必须要对函数进行求导，而手工求复杂函数的导数不仅容易出错，而且函数的更新也过于繁琐。深度学习框架通过提供自动微分能力解决这个问题。
      - 实际上，深度学习框架会构建一个计算图（computational graph）用于跟踪所有数值是由哪些操作生成的，有了这个计算图后，我们还可以通过数值反向去更新每个参数的偏导数，这被称为反向传播（backpropagate）。
      - 自动微分的另一个好处是，即使输入函数是一个由代码定义的黑箱，根本不清楚它的具体表达式，仍然可以通过反向传播自动计算出它的微分。
    - 概率论：
      - 采样
      - 随机变量的分析方法：联合分布、条件分布、Bayes 定理、边缘化、独立性假设
      - 概率分布的关键特征度量方式：期望、平方差/标准差
  - 学习第三章：线性神经网络
    - 线性回归模型是一个简单的单层神经网络，只有输入与输出两层
    - 学习了「从零开始实现线性回归」的一小部分

### 2022-05-28

- [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh) - 10.6%
  - 学习第二章：预备知识
    - 通过搜索 cheat sheet + 《Python for Data Analysis》学了下 Numpy/Pandas/Matplotlib 的使用方法
    - 复习线性代数

### 2022-05-24

- [动手学深度学习 - Pytorch 版](https://github.com/d2l-ai/d2l-zh) - 7.8%
  - 完成第一章前言，了解了深度学习是机器学习的一个分支，机器学习的用途、分类，深度学习的简单原理及优势，近十年此领域的爆炸式发展
  - 监督学习、无监督学习、强化学习
  - 音视频数据生成领域的重要方法：GAN

### 2022-05-24

- 分布式系统与区块链
  - 极客时间《分布式协议与算法实战》 - 40%
- AI
  - 被 ACE 深度学习歌声合成激励到了，花了近两个小时简单学了点吴恩达的机器学习课程、微软的 ML for beginners，李沐的《动手深度学习》
  - 明确了目标是「快速学习，暂时只是为了玩一玩」，确定我应该通过《动手深度学习 - Pytorch》入门。

### 2022-05-24

- 极客时间《分布式协议与算法实战》 - 36%

### 2022-05-22 ~  2022-05-23

- 学习 [分布式系统的一致性问题与共识算法](https://thiscute.world/posts/consistency-and-consensus-algorithm/) 并记录笔记
  - 极客时间《分布式协议与算法实战》 - 22%

### 2022-05-20

- 学习极客时间的《深入剖析 Kuberntes》 - 100%
  - 学完后第一次做测验，拿了 50 分，陷入自我怀疑 emmmm
  - 容器运行时
    - Kubelet 控制循环 `SyncLoop` 绝对不会阻塞，任何长时间任务都会创建新的 goroutine 来异步执行
    - CRI 的接口非常简单宽松，给予了底层容器运行时足够大的自定义空间
  - 云原生的发展方向
    - Kubernetes 的强大之处：**声明式 API** 和以此为基础的**控制器模式**、**将「政治」与「技术」拆分开的社区运作模式**
    - Kubernetes 生态与传统 PaaS 的区别：Kubernetes 提供了基础设施层能力（编排、调度、资源管理等），使得其上的 PaaS 可以专注于应用服务和发布流程管理这两个最核心的功能，开始向更轻、更薄、更以应用为中心的方向进行演进。从而 Serverless 开始蓬勃发展
    - Serverless 的本质：高可扩展性、工作流驱动、按用量计费
    - 「云原生」是一个使用户能低心智负担的、敏捷的，以可扩展、可复制的方式，最大化利用“云”的能力、发挥“云”的价值的一条最佳路径。
- 学习[分布式系统的一致性问题与共识算法](https://thiscute.world/posts/consistency-and-consensus-algorithm/) 并记录笔记
  - 一致性问题的核心是「ACID 理论中的事务一致性」，与「CAP 理论中的数据一致性」
    - 数据一致性又分为强一致性与弱一致性，而弱一致性的最低限度就是最终一致性：数据最终会一致（再低就永远不会一致了）
    - 最终一致性太模糊，具体实现上往往会最加上一些限定，得到许多一致性模型：读自己写一致性/写后读一致性、单调读一致性、前缀一致性、线性一致性、因果一致性

### 2022-05-19

- 学习极客时间的《深入剖析 Kuberntes》 - 87%
  - 简单学习了 CRD + Controller 的编写，包含 Informer 机制等。不过内容太老了，还是之后看 Programming Kubernetes 再详细学吧。
  - K8s API 资源的组织方式为 `api/<apiGroup>/<GroupVersion>/<Resource>`，yaml 中的 `apiVersion` 为 `<apiGroup>/<GroupVersion>`，而 `Kind` 的值就是 `<Resouce>`
    - Pod/Node/configmap 等几个核心资源的 `<apiGroup>` 为空，因此可以直接省略掉
    - 其他核心资源都是以功能分类的，都有 `<apiGroup>` 属性
  - RBAC 是以 Role 为授权的基本单位，`Role` 的规则会指定用户对不同 apiGroups/Resources/resourceNames 可以执行哪些动作 `verbs`
    - apiGroups/Resources 属性跟前面介绍的 API 资源的组织方式是完全对应的，但是 Resources 需要使用复数形式，如 `pods`/`configmaps`/`nodes`
    - 如果是核心资源如 Pod/Node，则 `apiGroups` 应该设为空字符串 `apiGroups: [""]`
  - RoleBinding/ClusterRoleBinding 有两个部分：`subjects` 被作用者，以及 `roleRef`，用于声明这两者之间的绑定关系
    - `subjects` 被作用者可以是集群内的 ServiceAccount，也可以是外部定义的对象如 `User`
    - `User` 在集群中是一个不存在的对象，它的认证需要一台外部系统
  - RBAC 中还存在 `Groups` 用户组的概念
    - 比如任意名字空间中所有 serviceaccount 的用户组，名称为 `system:serviceaccounts:<Namespace名字>`
    - 每个 serviceAccount 的全名为 `system:serviceaccount:<Namespace名字>:<ServiceAccount名字>`
    - 我们可以在 subjects 中填写一个用户组，为整个用户组内所有的 ServiceAccount 授权
  - Kubernetes 中默认已经内置了多个 clusterrole，可通过 `kubectl get clusterroles` 查看
    - 开发测试时，我们可能会经常用的一个 clusterrole 就是 `cluster-admin`，这个 role 拥有整个集群的最高权限，相当于 root，非开发测试环境一定要谨慎使用它。
    - `view`/`edit` 这两个 clusterrole 分别拥有整个集群的查看/编辑权限
  - Kubernetes 存储
    - 存储的两个绑定阶段：
      - 第一阶段（AttachDetachController，运行在 kube-controller-manager 中），K8s 将 nodeName 传递给存储插件，插件将数据卷 attach 到该节点上
      - 第二阶段（VolumeManagerReconciler，运行在 kubelet 中），K8s 将 dir 传递给存储插件，插件将数据卷挂载到该目录下（如果是新数据卷还会提前格式化该卷）。
    - 云上 K8s 存储的一个缺陷：无法跨可用区调度。如果你通过 affinity 强制把一个 p8s 调度到别的可用区，因为它的数据卷不在目标可用区，这会导致它无法被调度，卡在 Pending 状态。
    - 学习了已被废弃的 FlexVolume 的实现方式，以及它的替代者 CSI
    - 以 [csi-digitalocean](https://github.com/digitalocean/csi-digitalocean) 为例，学习了一个 CSI 插件的实现原理
  - Kubernetes 调度
    - 根据容器的 requests/limits 参数，k8s 将 Pod 分为三种类型：BestEffort Burstable Guaranteed
    - 在因为资源不足而触发驱逐 Evection 时，会按 BestEffort => Burstable => Guaranteed 的顺序进行驱逐
    - 当 Pod 中所有容器的 requests/limits 都相等的时候，Pod 的 QoS 等级为 Guaranteed
      - **如果这时容器的 cpu requests 为整数值，K8s 会自动为容器进行绑核操作，这可以大幅提升容器性能，常用在在线应用场景下**
      - 疑问：如果 istio sidecar requests/limits 不相等，但是应用容器是设的相等的，这种情况下是否会执行绑核操作呢？
    - Pod 的优先级与抢占机制
      - 首先创建不同优先级的 PriorityClass，然后为 Pod 指定 priorityClassName
      - 调度失败的 Pod 会被放到 unschedulableQ 中，这会触发调度器为这些调度失败的 Pod 寻找牺牲者的逻辑
      - 基于优先级与抢占机制，创建一些优先级为 -1 的占位 Pod，可以实现为整个集群预留一部分资源。这种方法被称为[「Pod 空泡」资源预留法](https://aws.amazon.com/cn/blogs/china/improve-eks-elastic-scaling-efficiency-through-overprovisioning/)。
    - Device Plugin: 负责管理集群中的所有硬件加速设备如 GPU/FPGA 等
      - Device Plugin 只能基于「数量」进行调度，无法进行更复杂的异构调度策略，比如「运行在算力最强的节点上」
    - 日志与监控：对我来讲，没什么新东西
    - 容器运行时
      - gVisor - 在用户态重新实现了一遍 Linux ABI 接口、网络协议栈，启动速度跟资源占用小。但是工程量大，维护难度大，对于系统调用密集的应用，性能会急剧下降。
      - kata containers: 据说是性能比较差，运行了一个真正的 Linux 内核与 QEMU 虚拟设备实现强隔离
      - aws firecrackers: 跟 kata containers 的思路一致，但是使用 rust 实现了自己的 vmm，性能更高

### 2022-05-15

- 了解到 2021 年是区块链投资大涨的一年，总投资涨了 7 倍多到了 252 亿美元，NFT 更离谱直接从 2020 年的 37m 涨到 4802m 美元，感觉确实非常有前景
  - 数据来源 [State Of Blockchain 2021 Report - CB Insights Research](https://www.cbinsights.com/research/report/blockchain-trends-2021/)
- 分两次从币安转了 0.01 ETH + 0.05 ETH 到 Ethereum，币安收了固定手续费 0.0016 ETH * 2
  - 购买 ENS 域名 thiscute.eth 10 年并设为我的主域名，花了约 0.027 ETH，算上 gas 费一共花了 0.0321 ETH 也就是 67 刀
- 给自己再次整了一个 mirror.xyz 账号，有了 ENS 就是爽。
- 但是发现我现有的几个域名如 thiscute.world，其实可以直接通过 DNSSEC 导入到 ENS，感觉血亏 0.027 ETH...
- 阅读郭宇最近写的[《Web3 DApp 最佳编程实践指南》](https://guoyu.mirror.xyz/RD-xkpoxasAU7x5MIJmiCX4gll3Cs0pAd5iM258S1Ek)
  - 晚上去测核酸的路上还参与了他开的一个 twitter space 聊 web3 开发，发言的很多大佬，很多干货。
  - 也明确了，目前区块链还处于战国时代，百家争鸣
- 再次确认今年学习路线，精简与调整之前年度的计划（之前的计划太多了搞不定，而且当时没排区块链）
  - 先学好分布式原理与算法这块
  - 然后是 Kubernetes 编程，同时结合极客兔兔的几个教程深入学习 Go
  - 深入学下 Go 语言底层
  - 搞一搞区块链
  - 学习 C 语言
  - 通过 TLPR 学习 Linux 系统
  - 通过 CS144 系统学习计算机网络

### 2022-05-14

- 阅读 [Web 3.0：穿越十年的讨论 - 知乎](https://www.zhihu.com/special/1452635344142909440) 系列内容，了解 Web 3.0
- 阅读 [dcbuild3r/blockchain-development-guide](https://github.com/dcbuild3r/blockchain-development-guide)，了解如何进行区块链开发
  - 我把这个 guide 完整过了一遍（后面关于自我提升、社会影响力啥的仅走马观花看了看），真的好长的一篇文章啊。
  - 很多干货，现在我对搞区块链开发要学的东西，认知更清晰了。


### 2022-05-12

- 迭代博客内容《关于 NAT 网关、NAT 穿越以及虚拟网络》- 90%
  - 真的低估了 NAT 网关与 NAT 穿越技术的知识量，又折腾了一个晚上，文章还没完成...
  - 5/9 的时候我就觉得文章已经完成了 90%，结果今天又折腾了一晚上迭代了大量内容，现在感觉文章的进度还不到 90%...越学发现自己懂得越少

### 2022-05-11

- 学习极客时间的《深入剖析 Kuberntes》 - 53%
  - 学习了 NetoworkPolicy、kube-proxy 的实现原理，其实都是用 iptables 实现的，原理挺简单的。
  - 不过 kube-proxy 很早就支持了 ipvs 模式，它在大规模场景下比 iptables 性能更好一些。但是 AWS EKS 目前官方仍然并不支持 ipvs 模式，打开可能会有坑。
- 极客时间《分布式协议与算法实战》 - 4%
  - 过了一遍常见共识算法的名字：两阶段提交、Try-Confirm-Cancel、Paxos、ZAB、Raft、Gossip、PBFT、PoW、PoS、dPoS
  - 过了一遍上述共识算法的特性：是否支持拜占庭容错、支持哪种程度的一致性、性能、高可用性
- 了解了一些区块链相关公司的方向，区块链开发岗位的要求
- 还研究了一波性能测试工具：grafana/k6

### 2022-05-09

- 学习极客时间的《深入剖析 Kuberntes》 - 48%
  - 复习了 Linux 虚拟网络接口以及容器网络原理、学习了 CNI 网络插件的原理
  - 学习了两个 underlay 网络实现：flannel 的 host-gw 模式实现原理、calico 基于 BGP 的实现原理
  - calico 在跨 vlan 时需要使用 IPIP，学习了相关原理
- 完成博客《关于 NAT 网关、NAT 类型提升、NAT 穿透以及虚拟网络》- 90%
  - 简单研究了 Go 的 STUN/TURN/ICE 库，以及 coturn server
- 简单学习了零知识证明的应用，zk-SNARKs，区块链混币服务，以及拜占庭将军问题

### 2022-05-08

- 完成博客《关于 NAT 网关、NAT 类型提升、NAT 穿透以及虚拟网络》
  - 已发布，但是还有些细节需要填充，另外还需要补些示意图

### 2022-05-06

- 学习极客时间专栏《深入浅出 Kubernetes》 - 37%
  - 主要学了下 Pod 的结构、名字空间共享等细节信息，这部分我以前只了解个大概
  - 集群安装、Deployment、StatefulSet、Service 这几个部分我都已经比较熟了，走马观花看了看。
  - 粗略过了下目录，其中对我而言最有价值的，应该就是容器网络、调度器、容器运行时

### 2022-05-05

- 学习极客时间专栏《深入浅出 Kubernetes》 - 20%
  - Kubernetes 与其他败北的编排工具比，最大的优势在于它的设计思想：
    - 从更宏观的角度，以统一的方式来定义任务之间的各种关系（最底层是 Pod 与 PV，之上是各种控制器、亲和反亲和、拓扑扩散、自定义控制器，网络侧有 service，底层网络插件等等），并为将来支持更多种类的关系留有余地（开放、强大的自定义能力催生出了丰富的生态）
    - 基于状态的声明式配置，由控制器负责自动达成期望的状态
- 研究 FinOps 与 kubecost，总结工作上的经验，完成一篇 Kubernetes 成本分析的文章 - 100%

### 2022-05-02

- 学习[Go语言动手写Web框架](https://geektutu.com/post/gee.html) - 进度 20%


### 2022-05-01

- 研究 FinOps 与 kubecost，完成一篇 Kubernetes 成本分析的文章 - 50%

### 2022-04-26 - 2022-04-28

- 学习极客时间专栏《深入浅出 Kubernetes》，复习容器技术（Namespace/Cgroups/rootfs）
  - Docker 最核心的创新：
    - 将 rootfs 打包到镜像中，使镜像的运行环境一致（仅与宿主机共享内核）
    - 使用 Dockerfile 描述镜像的打包流程，使构建出的镜像可预期、可重新生成
- 2022-04-28 调薪结果出来了，突然觉得身心都有点累了，有点惆怅。总之还是继续努力吧，技术才是我的核心竞争力，少管他什么妖风邪雨。

### 2022-04-25

- 完成了 19 年创建的 go 项目：https://github.com/ryan4yin/video2ascii
- 失眠，半夜随便翻了翻，把《Go 程序设计语言（英文版）》走马观花过了剩下的一部分，算是完成了一周目
- 阅读 [Programming Kubernetes - Developing Cloud Native Applications](https://programming-kubernetes.info/) - 进度 7%
  - 主要是通过案例讲解 CRD Operator Controller 等 Kubernetes 编程技术

![](/images/now/the-go-programming-language.webp "Go 程序设计语言（英文版） 2022-08-19 补图")


### 2022-04-24

- 阅读《Go 程序设计语言（英文版）》 - 进度 90%
  - 目前还剩两章未读：反射 reflection 与底层编程 unsafe/uintptr

### 2022-04-22 - 2022-04-23

- 阅读《Go 程序设计语言（英文版）》 - 进度 72%
    - 主要完成了 goroutines/channels 以及「并发与变量共享 sync」两个章节


### 2022-04-21

- 多抓鱼买的一批新书到手了，大致读了下几本书的前几页。
  - 目前比较感兴趣的有：《复杂》、《陈行甲人生笔记》、《原则 - 应对变化中的世界秩序》、《这才是心理学》
  - 打算首先读《复杂》
- 使用 [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler) 实现集群弹性扩缩容
  - 发现社区的这个工具（简称 CA），确实没 aws 出品的 karpenter 好用。
  - CA 自身的实现很简单，主要是依靠 AWS ASG 实现扩缩容。
  - 而 EKS 的 NodeGroup 说实话做得太垃圾了，底层 ASG 的很多功能它都不支持，一旦创建很多参数（VPC 参数、实例类型、等等）就无法通过 EKS NodeGroup 变更了。如果越过 EKS NodeGroup 直接修改底层的 ASG 配置，它还会提示「Degraded」说配置不一致，真的是无力吐槽。

### 2022-04-20

- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 73%
- 使用 [aws/karpenter](https://github.com/aws/karpenter) 实现集群弹性扩缩容
  - 已上线 prod 环境，目前给 EMR on EKS 集群专用。
- 更新 /now 页面以及 knowledge 的内容

### 2022-04-18

- 研究使用 [aws/karpenter](https://github.com/aws/karpenter) 实现集群弹性扩缩容
- 阅读《Go 程序设计语言（英文版）》 - 进度 53%
  - 第 7 章「接口」读了一半，大概 22 pages，预计明天能完成
- [ ] 《[Operating Systems - Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)》
  - 读到 Introduction 一章，行文真的很有趣，看 projects 也有深度，决定了要把这本书看完，把习题做好。
  - OSTEP 后面的部分会涉及 vx6 源码，这要求比较深的 C 语言知识以及 x86 汇编知识，不过这些可以在学到的时候，再做补充。
  - 在需要用到的时候，学习 CSAPP 的 x86 汇编部分会是一个比较好的补充。

### 2022-04-17

- 阅读《Go 程序设计语言（英文版）》 - 进度 7/13
- 《在生命的尽头拥抱你-临终关怀医生手记》 - 进度 61%
- 重新整理书单，放到 /now 页面中
- 学习 NAT 原理知识

### 2022-04-15 ~ 2022-04-16 

- 阅读《Go 程序设计语言（英文版）》 - 进度 5/13

### 2022-04-14

- 阅读《Go 程序设计语言（英文版）》 - 进度 4/13

### 2022-04-13

- 阅读《Go 程序设计语言（英文版）》 - 进度 3/13

### 2022-04-10

- 学习 3D 引擎的使用，简单试用了 unity3d 与 unreal engine 5.
  - 确定学习方向：先学学 UE5 蓝图入个门，然后试试把 MMD 模型导入到 UE5 做做动画，中间也会简单接触下 Blender.
  - 感受：UE5 挺不错的，尤其是它还提供 VR 编辑模式，手上的 Quest 2 又能派上用场了
  - 输出文档：[3D 图形相关](https://github.com/ryan4yin/knowledge/tree/master/graphics)
- 阅读《Go 程序设计语言（英文版）》 - 进度 2/13
  - 第一章「导览」大概过了下 Go 的关键特性：完善的工具链，丰富的标准库，goroutine, channel
  - 第二章主要讲程序结构，包含变量、类型声明、指针、结构体、作用域、包与文件结构等等

### 2021-04-08 - 2021-04-09

- 学习区块链技术 Web3.0
  - [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook) - 以太坊入门
    - 进度：100%
    - 跳过了智能合约代码相关的内容，因为代码比较老了，新版本的 solidity 有了许多新变化。
  - [Youtube - Solidity, Blockchain, and Smart Contract Course – Beginner to Expert Python Tutorial](https://www.youtube.com/watch?v=M576WGiDBdQ)
    - 这个视频及相关的 Github 仓库，包含一些区块链可视化以及相关的介绍，更适合学习完理论后，实战合约编写
  - [区块链技术指南](https://github.com/yeasy/blockchain_guide): 《Docker - 从入门到实践》作者的新书，内容同样简洁易懂，侧重介绍原理及知识面，非常棒。

### 2021-03-26 - 2021-04-01

- 学习区块链技术 Web3.0
  - [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook) - 以太坊入门
    - 进度：7/14
    - 这书适合用于学习理论，solidity 开发相关的内容可以跳过，即 7/8 两章
  - [Youtube - Solidity, Blockchain, and Smart Contract Course – Beginner to Expert Python Tutorial](https://www.youtube.com/watch?v=M576WGiDBdQ)
    - 这个视频及相关的 Github 仓库，包含一些区块链可视化以及相关的介绍，更适合学习完理论后，实战合约编写


### 2021-03-23 - 2021-3-25

- 阅读《在生命的尽头拥抱你-临终关怀医生手记》
- 在 Manager 的帮助下申请职级晋升（初级 => 中级 SRE）
  - 再一次认识到我自己写的文字有多么随意... Manager 帮我提炼补充后，文字变得言简意赅，精确客观，瞬间高大上档次了。

### 2021-03-22

- 注册[模之屋](https://www.aplaybox.com)，简单学了下 MMD 跟 [Blender](https://www.blender.org/)

### 2021-03-15 - 2021-03-19

- 学习 Envoy，完成 [Envoy 笔记](https://github.com/ryan4yin/knowledge/tree/master/network/proxy%26server/envoy)


### 2021-03-11 - 2021-03-14

- 《写给开发人员的实用密码学》
  - 完成第七篇「非对称加密算法」的 ECC 部分，并为 RSA 部分补充了部分 Python 代码
  - 将去年写的文章《TLS 协议、TLS 证书、TLS 证书的配置方法、TLS 加密的破解手段》改写并补充内容，改名为《写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议》
  - 为第五篇「密钥交换」补充了 DHKE/ECDH 的代码示例，另外还补充了 DHE/ECDHE 一节
  - 此系列文章的其他小修改与润色
- 业务大佬在 gRPC 的基础上再添加了 gzip 压缩，TX 流量再次下降 80%+
  - 侧面说明以前业务侧对 HTTP 的用法是多么豪放 emmmm
  - 周末上 gzip 压缩功能，业务大佬太肝了啊...

### 2022-03-09

- 发布《写给开发人员的实用密码学》系列第七篇：非对称加密算法，但是暂时只完成了 RSA 部分

### 2022-03-07 - 2022-03-08

- 跟推荐系统大佬一起将服务从 HTTP 切换到 gRPC，效果立竿见影，服务流量下降 50% ~ 60%，延迟下降 30% ~ 50%
  - 提升了服务性能，降低了 AWS 跨区流量成本

### 2022-03-05 - 2022-03-06

- 发布《写给开发人员的实用密码学》系列的第六篇：对称加密算法

### 2022-03-01

- 深圳疫情形式严峻，开始居家办公
- 整理润色后，发布《写给开发人员的实用密码学》前五篇的内容

### 2022-02-19 - 2022-02-25

- 阅读 [Practical Cryptography for Developers](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)，同时完成我的密码学笔记
  - 起因是想学下区块链技术，结果发现课程一开始就讲加密哈希函数的基本性质，就决定先搞一波密码学。
- 完成了《写给开发人员的实用密码学》前五篇的草稿。
- [研究 istio 的 gRPC 支持与监控指标](https://github.com/ryan4yin/knowledge/blob/master/kubernetes/service_mesh/istio/Istio%20%E7%9B%91%E6%8E%A7%E6%8C%87%E6%A0%87.md)

### 2022-02-17

- 发现我们的 EKS 集群主使用的是 AWS Spot 实例，这类实例的 c6i/c6g 性能与价格差距并不高，做 ARM 化的 ROI 貌似并不高
- 发现对 aws 的 RDS/EC2-Volume/Redis 等资源进行全面评估，删掉闲置资源、缩小实例/集群规格，可以轻易节省大量成本（说明以前申请资源时风格比较豪放 2333）
- 继续迭代个人博客

### 2022-02-07 - 2022-02-16

- 迭代我的独立博客 <https://thiscute.world>
  - 添加「阅读排行」页，定期从 Google Analytics 同步数据
  - 从博客园迁移部分有价值的文章到独立博客


### 2022-01-08 - 2022-01-16

- 购入 Synthesizer V + 青溯 AI 声库，简单调了几首歌试试，效果非常棒。
- 也调研了下[歌声合成领域目前的进展](https://github.com/ryan4yin/knowledge/tree/master/music/vocal%20synthesizer)，试用了免费的移动端软件 [ACE 虚拟歌姬](https://www.taptap.com/app/189147?hreflang=zh_CN)，渲染效果真的媲美 CNY 999 的 SynthV AI 套装，不得不感叹 AI 的效果真的强啊。

### 2022-01-01

- 了解 APISIX/Nginx/Envoy 中的各种负载均衡算法，及其适用场景、局限性。

### 2021-12-12

- 练习二个半小时轮滑，学会了压步转弯技术
- 无聊，但是又啥都不想干，耽于网络小说...
- 感觉有点现充了，感觉需要找个更明确的、能给人动力的目标
  - 做个三年的职业规划以及生活规划？

### 2021-11-21

- 轮滑：复习前双鱼、前剪、前蛇，尝试侧压步、倒滑

### 2021-11-08 - 2021-11-12

- 将上次 EKS 升级过程中，有问题的服务迁移到 1.21 的 EKS 集群，直接切线上流量测试。
  - 复现了问题，通过 JFR + pods 数量监控，确认到是服务链路上的个别服务频繁扩缩容导致的，这些服务比较重，对扩缩容比较敏感。
  - 测试在 HPA 中添加 behavior 降低缩容速率，同时添加上 PodDisruptionBudget 以避免节点回收导致大量 Pod 被回收，经测试问题基本解决。
- 遭遇 AWS EKS 托管的控制平面故障，controller-manager 挂了一整天。现象非常奇怪，又是第一次遇到，导致长时间未排查到问题。
  - 确认问题[来自 HPA behavior 的 Bug](https://github.com/kubernetes/kubernetes/issues/107038)
    1. 储存于 etcd 中的 object 仅会有一个版本，透过 apiserver 读取时会转换成请求的 autoscaling API 版本。
    2. autoscaling/v2beta2 scaleUp 及 scaleDown 对象不能为 null，并在[其 Kubernetse 代码](https://github.com/kubernetes/kubernetes/blob/6ac2d8edc8606ab387924b8b865b4a69630080e0/pkg/apis/autoscaling/v2/defaults.go#L104)可以查看到相应的检查机制。
    3. 当使用 autoscaling/v1 时，v2beta2 版本中的相关对象字段将作为 annotation 保留，apiserver 不会检查 ScaleUp/ScaleDown 的 annotation是否为 non-null，而导致 kube-controller-manager panic 问题。
    4. 我们可以使用 v1 或 v2beta2 创建一个 HPA 对象，然后使用 v1 或 v2beta2 读取、更新或删除该对象。 etcd 中存储的对象只有一个版本，每当您使用 v1 或 v2beta2 获取 HPA 对象时，apiserver 从 etcd 读取它，然后将其转换为您请求的版本。
    5. 在使用 kubectl 时，客户端将默认使用 v1(`kubectl get hpa`)，因此我们必须明确请求 v2beta2 才能使用这些功能(`kubectl get hpa.v2beta2.autoscaling`)
    6. 如果在更新 v1 版本的 HPA 时（kubectl 默认用 v1），手动修改了 v2beta2 功能相关的 annotation 将 scaleUp/scaleDown 设为 null，会导致 controller-manager 挂掉.


### 2021-10-23

- 跟公司冲浪小分队，第一次玩冲浪，最佳成绩是在板上站了大概 6s...

### 2021-10/11 - 2021-10-19

- 将 EKS 集群从 1.17 升级到 1.21（新建集群切量的方式），但是遇到部分服务迁移后可用率抖动。
  - 未定位到原因，升级失败，回滚了流量。

### 2021-09-13 - 2021-09-17

- 学习极客时间《10X程序员工作法》
  - 以终推始
  - 识别关键问题
  - ownership

### 2021-09-02 - 2021-09-11

- EKS 集群升级
  - 了解 EKS 集群的原地升级的细节
  - 输出 EKS 集群原地升级的测试方案，以及生产环境的 EKS 集群升级方案
- 学习使用 kubeadm+containerd 部署 k8s 测试集群
  - 涉及到的组件：Kuberntes 控制面、网络插件 Cilium、kube-proxy、coredns、containerd

### 2021-08-31 - 2021-09-01

- 思考我在工作中遇到的一些非技术问题，寻找解法
    - 效率：如何在没人 push 的情况下（没有外部压力），维持住高效率的工作状态（早早干完活下班它不香么？）。
      - 建立有效的「自检」与「纠错」机制
        - 自检：
          - 列出目前已知的「异常」和「健康」两类工作状态，每日做一个对比。
          - 每日都列一下详细的工作计划，精确到小时（预留 1 小时 buffer 应对临时需求）。
    - 沟通：遇到问题（各种意义上的问题）时，及时沟通清楚再继续推进，是一件 ROI 非常高的事。否则几乎肯定会在后面的某个节点，被这个问题坑一把。
    - 目前的关键目标是啥？存在哪些关键问题（实现关键目标最大的阻碍）？我最近做的主要工作，是不是在为关键目标服务？
  - 如何把安排到手上的事情做好？
    - 思考这件事情真正的目标的什么？
      - 比如任务是排查下某服务状态码有无问题，真正的目的应该是想知道服务有没有异常
    - 达成真正的目标，需要做哪些事？
      - 不仅仅状态码需要排查，还有服务负载、内存、延迟的分位值，或许都可以看看。
    - 跟需求方沟通，询问是否真正需要做的，是前面分析得出的事情。

这些问题都是有解法的，关键是思路的转换。

---

### 2021-08-28 => 2021-08-29

- 容器底层原理：
  - linux namespace 与 cgroups
  - linux 虚拟网络接口 macvlan/ipvlan、vlan、vxlan

---

### 2021-08-19 => 2021-08-23

- 阅读 rust 语言的官方文档：the book
- 边读文档边做 rustlings 的小习题
  - 目前完成了除 macros 之外的所有题
  - 遇到的最难的题：conversions/{try_from_into, from_str}
- 使用 rust 重写了一版 video2chars

---

### 2021-08-12 => 2021-08-16

- Linux 的虚拟网络接口
- Linux 的 netfilter 网络处理框架，以及其子项目 iptables/conntrack

---

### 2021-03-11 => 2021-08-09

- 入职大宇无限
- 学习 nginx - openresty - apisix
- 工作中，在自己负责的领域，建立起 ownership
- 学习新公司的工作模式：OKR 工作法
- 学习新公司的思维模式（识别关键问题）
  - 如何从公司的角度去思考问题，找到我们目前最应该做的事情
  - 从以下角度去评价一件事情的重要性
    - 这件事情对我们目前的目标有多大帮助？
    - 需要投入多少资源和人力？
    - 在推进过程中，有哪些阶段性成果或者 check point？

---


{{< particles_effect_up  >}}
