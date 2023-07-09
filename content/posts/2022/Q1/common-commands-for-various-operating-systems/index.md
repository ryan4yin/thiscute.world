---
title: "Linux/Windows/MacOSX 系统常用命令集锦"
date: 2022-02-13T16:09:00+08:00
draft: false

resources:
  - name: "featured-image"
    src: "terminal.webp"

tags:
  [
    "Linux",
    "MacOSX",
    "Windows",
    "CLI",
    "Powershell",
    "Shell",
    "tmux",
    "rsync",
    "vim",
    "awk",
  ]
categories: ["tech"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 个人笔记，只会列出我自己容易忘掉的命令，方便查阅。

> 内容比较多，适合当参考手册用。可能不太适合从头读到尾...

> 本文主要介绍 Linux 命令，顺带介绍下 Windows/MacOSX.

## 一、Linux

### 1. 后台运行

```shell
# 1. 后台运行命令
nohup python xxx.py &
```

也可以使用 tmux，tmux 提供的 session 功能比 nohup 更好用，后面会介绍 tmux

### 2. 查找替换 sed/awk 与 json/yaml 处理 jq/yq

sed 常用命令：

```shell
## 只在目录中所有的 .py 和 .dart 文件中递归搜索字符"main()"
grep "main()" . -r --include *.{py, dart}

## 在 .js 文件中搜索关键字 xxxxx 并仅展示关键字前后 40 个字符（用在 .js 等被压缩过的文本文件上很有效）
cat *.js | grep -o -P '.{0,40}xxxxx.{0,40}'

# 在文件夹中递归查找所有中文字符（在做中英双语内容维护时比较有用）
grep -P '[\x{4e00}-\x{9f5a}]' -r .

## 1） 全文搜索并替换
### -i --in-place 原地替换（修改原文件）
### -i=SUFFIX  替换后的文件添加 SUFFIX 这个后缀
### -r  使用拓展的正则表达式，注意此正则不支持 \d\w\s 等语法，必须使用 [0-9] [a-zA-Z] 等来替换！！！
sed -ri "s/pattern_str/replace_str/g" `grep "key_pattern" 'path_pattern' -rl`

## 2）文件名搜索，替换文件内容
sed -ri "s/pattern_str/replace_str/g" `find . -name "pattern"`

## 3）批量转换大小写
# 将当前文件夹内，所有的 gitlab URL 都转换成小写
# \L 转小写  \U 转大写
sed -ri 's@http://GITLAB.*.git@\L&@g' `find . -name pubspec*`


## 4) 拷贝文件，并且保持文件夹结构（--parents 表示保持文件夹结构）
cp --parents `find <src-dir> -name *.py` <dst-dir>
```

awk 用于按列处理文本，它比 sed 更强大更复杂，常用命令：

```shell
## 1. 单独选出第 1 列的文本
cat xxx.txt | awk -F '{print $1}' | head

## 2. 可以使用 -F 指定分隔符，打印出多列
awk -F ',' '{print $1,$2}'| head

## 3. 打印出行数
cat log_test | awk '{print NR,$1}' | more

## 4. if 判断语句
cat log_test | awk '{if($11>300) print($1,$11)}'

cat log_test | awk '{print $11}' | sort -n | uniq -c

# 求和
cat data|awk '{sum+=$1} END {print "Sum = ", sum}'

# 求平均
cat data|awk '{sum+=$1} END {print "Average = ", sum/NR}'

# 求最大值
cat data|awk 'BEGIN {max = 0} {if ($1>max) max=$1 fi} END {print "Max=", max}'

# 求最小值（min的初始值设置一个超大数即可）
awk 'BEGIN {min = 1999999} {if ($1<min) min=$1 fi} END {print "Min=", min}'
```

[jq](https://github.com/stedolan/jq)/[yq](https://github.com/mikefarah/yq) 常用命令：

```shell
# 1. jq 是一个命令行 json 处理工具

## 从 json 中查询某一个字段的值
jq -r '.message' xxx.json
## 也可从 stdin 读取 json
cat xxx.json | jq -r '.message'

## 从 json 内容中删除多个 key
## -r 表示输出文本采用 raw 格式
jq -r "del(.dataplane.insync, .dataplane.outdated)" xxx.json

## 更多 jq 的用法参见官方文档：https://stedolan.github.io/jq/tutorial/

# 2. yq 是用于处理 yaml 配置的命令行工具，参数跟 jq 高度相似

## 从 yaml 配置中删除多个 key
yq "del(.dataplane.insync, .dataplane.outdated)" xxx.yaml
## 或者从 stdin 读取输入
cat xxx.yaml | yq "del(.dataplane.insync, .dataplane.outdated)"

## 原地更新某 yaml 配置文件
yq -i '.a.b[0].c = "cool"' file.yaml

## yq 的更多用法参见官方说明: https://github.com/mikefarah/yq
```

### 3. 压缩相关

```shell
# 直接 cat 压缩文件的内容
zcat xxx.gz | more  # gzip
xzcat xxx.xz | more  # xz

tar -axvf xxx.tar.*  # 通过后缀识别压缩格式，智能解压
```

更多命令参见 [常见压缩格式的区别，及 Linux 下的压缩相关指令](https://thiscute.world/posts/compression-related-instructions-under-linux/)

### 4. 文件拷贝与同步

各种 Linux 发行版都自带 scp/ssh，这两个工具功能简单，一般够用。

另外就是更强大也更复杂的 rsync，部分发行版会自带 rsync。

下面分别介绍下。

#### 1. ssh/scp

```shell
# 如果使用 ssh 命令进行文件传输，可安装 pv 命令查看传输速度（pipeviewer）
## ubuntu
sudo apt-get install pv
##  centos
sudo yum install epel-release
sudo yum install pv

## 1)从本地上传到服务器

### 使用 ssh 的好处是流式传输不会占用目标机器的存储空间，适合传输可能引起空间不足的大文件，并在目标机器上实时处理该文件。
cat <filename> | pv | ssh <user>@<host> -p 22 "cat - > <new-filename>"
tar cz <filename or foldername or glob> | pv | ssh <user>@<host> -p 22 "tar xz"  # 压缩传输

## scp 命令比 ssh 命令更简洁（但是不适合用于传文件夹，它会破坏文件的权限设置，把文件夹弄得一团糟）
scp -P 22 <filename> <user>@<host>:<folder-name or filename>  # 通过 scp 传输，传文件夹时记得添加 -r 参数（recursive）

## 2) 从服务器下载到本地
ssh <user>@<host> -p 22 "tar cz <filename or foldername or glob>" | pv | tar xz  # 压缩传输
scp -P 22 <user>@<host>:<folder-name or filename> <filename>  # 通过 scp 传输，传文件夹时记得添加 -r 参数（recursive）
```

#### 2. rsync

rsync 的功能其实和前面的 scp/(tar+ssh) 是一样的，将文件从一个地方拷贝到另一个地方。
区别在于它只做增量同步，在多次拷贝文件时，只拷贝（同步）修改过的部分，很多场景下可以大大加快拷贝/备份速度。

rsync 的常用命令：

```shell
# 将一个文件夹归档、压缩，并通过 ssh 协议（默认）同步到另一个地方
# -a, --archive   # 归档模式，保留文件的所有元信息，等同于 `-rlptgoD`
# -r, --recursive # 递归复制文件夹，`-a` 隐含了这个参数，通常都用 -a。
# -v, --verbose   # 输出详细信息
# --progress      # 显示传输进度
# -z, --compress  # 传输文件时进行压缩
rsync -avz --progress src host:dest
rsync -avz --progress -e "ssh -p225" /path/src user@host:dest  # 使用非默认的 ssh 端口进行传输
rsync -avz --progress -e "ssh -i id_xxx" /path/src user@host:dest  # 使用指定的私钥连接 ssh 服务端，其他各种 ssh 参数都可以在这里指定

# --exclude 排除掉某些不需要的文件(夹)
rsync -avz --progress --exclude "foor/bar" src user@host:dest

# 有时我们希望在同步数据时修改文件的 user/group
# --chown    # 设置文件的 user:group，必须与 `-og`/`--owner --group` 同时使用！（`-a` 隐含了 `-og`）
rsync -avz --progress --chown=root:root src user@host:dest  # 传输时修改 user/group 为 root

# 详细说明 src 和 dest 的位置
rsync -avz --progress path/src user@host:/tmp  # 将 src 拷贝到远程主机的 /tmp 中（得到 /tmp/src）
## 注意 src 结尾有 /
rsync -avz --progress path/src/ user@host:/tmp/src  # 将 src 目录中的文件拷贝到远程主机的 /tmp/src 目录中（同样得到 /tmp/src）

# 有时候我们在传输文件时不希望保留文件的元信息

# rsync 默认不会删除 dest 中多余的文件，使用 --delete 可让 rsync 删除这部分无关的文件
# 对 src 文件夹进行完全镜像，保证两个文件夹的内容一模一样，不多不少
rsync -avz --progress --delete src user@host:dest

# 也可以使用 --ignore-existing 让 rsync 忽略掉 dest 已经存在的文件。就是只同步新增的文件。
rsync -avz --progress --ignore-existing src user@host:dest
```

另外也有使用双冒号 `::` 分隔的传输命令，这种命令使用 `rsync` 协议进行传输，要求目标主机启用 rsync-daemon。用得会比 ssh 少一些，暂时不做介绍。

rsync 详细文档参见 https://rsync.samba.org/documentation.html，或者 `man rsync`.

### 5. Tmux

1. 输入 `tmux` 启动一个 tmux 会话。（或者用 `tmux new -s <session-name>` 启动一个命名会话）
2. 输入 `python xxx.py`，python 进程开始运行。
3. 按快捷键 `ctrl+b`，然后再按一下 `d` 脱离(detatch)当前会话。此时 python 进程进入后台运行，关闭当前终端对 python 进程没有影响。
4. 输入 `tmux ls` 可以查看当前正在后台运行的会话。（命名会话会显示名称，否则只显示 id）
5. 通过 `tmux attach -t <session-name/id>` 重新接入后台会话。
   1. 缩写 `tmux a -t <session>`
6. 或者通过 `tmux kill-session -t <session-name/id>` 杀死一个后台会话。

常用快捷键：

```yaml
# prefix 表示 `ctrl`+`b`

# pane 的切分与选择
prefix "  # 在下方新建一个 pane
prefix %  # 在右侧新建一个 pane
prefix `方向键`  # 光标移动到指定方向的 pane 中

# 使用方向键滚动窗口内容
prefix [  # 进入翻页模式，可使用 page up/down，或者方向键来浏览 pane 的内容
# 使用鼠标滚轮来滚动窗口内容（也可以把此命令添加到 `~/.tmux.conf` 中使它永久生效）
prefix `:` 然后输入 `set-window-option -g mode-mouse on`

# （调整 pane 大小）将当前的 pane 向给定的方向扩容 5 行或者 5 列
# 按住 ALT 时快速重复敲击「方向键」，能快速调整，否则就得从 prefix 开始重新输入
prefix `Alt` + `方向键`
# 将当前窗格全屏显示，第二次使用此命令，会将窗格还原
prefix z

# 交换 pane 的位置
prefix {  # 当前窗格与上一个窗格交换位置
prefix }  # 当前窗格与下一个窗格交换位置

# session 相关操作
prefix s  # 查看 session 列表，并通过方向键选择 session
prefix `number`  # 通过数字标签选择 session

# window 相关操作（关系：每个 session 可以包含多个 window，每个 window 里面又可以有多个 pane）
prefix c # 新建 window
prefix w # 通过数字标签选择 window
```

参考文档：

- https://github.com/tmux/tmux/wiki/Getting-Started
- https://www.ruanyifeng.com/blog/2019/10/tmux.html

### 6. Bash Shell 基础

目标：能使用 shell 编写 10 行以内的脚本。更长的脚本可以使用 Python 编写，就没必要折腾 Shell 了。

#### 1. For 循环

单行 for 循环，有时候很有用：

```shell
# 数字枚举
for i in $(seq 1 5); do echo $i; done  # sh/bash 都支持
for i in {1..5}; do echo $i; done  # sh 不支持此语法


# 文件枚举，可使用 glob 语法进行文件匹配
for f in *; do echo $f; done
for f in /etc/*.py; do echo $f; done

# 使用 find 进行文件枚举
for f in $(find . -name *.py); do echo $f; done
```

单行 for 循环加几个换行就得到多行 for 循环，格式如下：写脚本用得到，不过更建议用 python:

```shell
for i in $(seq 1 5)
do
  echo $i
done  # sh/bash 都支持
```

#### 2. if 语句

```shell
# 单行 if 语句
if [ true ]; then <command>; fi

#  if else
if [ expression ]
then
   Statement(s) to be executed if expression is true
else
   Statement(s) to be executed if expression is not true
fi
```

#### 3. Shell 脚本中的 set 指令，比如 set -x 和 set -e

参见：[Shell 脚本中的 set 指令，比如 set -x 和 set -e](https://www.cnblogs.com/robinunix/p/11635560.html)

#### 4. 实用小工具

```shell
# URL 编解码
alias urldecode='python3 -c "import sys, urllib.parse as ul; print(ul.unquote_plus(sys.stdin.read()))"'
alias urlencode='python3 -c "import sys, urllib.parse as ul; print(ul.quote_plus(sys.stdin.read()))"'

# 使用方法
echo "xxx" | urldecode
cat file | urlencode
```

#### 5. 查询历史记录

临时版：

```shell
# 查询命令行历史记录，并带上时间
HISTTIMEFORMAT="%F %T %z " history
```

一劳永逸版：

```shell
# 将环境变量加入 .bashrc
echo 'HISTTIMEFORMAT="%F %T "' >> ~/.bashrc
source ~/.bashrc

# 查询历史记录
history
```

#### 6. 其他资料

- [shell_scripts](https://github.com/mritd/shell_scripts): 实用 shell 小脚本

### 7. socket 连接查询 - ss/netcat/lsof {#socket-commands}

查看 socket 信息可以帮我们回答下列问题：

1. 我的程序是不是真的在监听我指定的端口？
1. 我的程序是在监听 127.0.0.1（本机），还是在监听 0.0.0.0（整个网络）
1. 进程们分别在使用哪些端口？
1. 我的连接数是否达到了上限？

> 现在较新版本的 Ubuntu 和 CentOS 都已经使用 `iproute2` 替换掉了 `net-tools`，
> 如果你还需要使用陈旧的 `route` `netstat` 等命令，需要手动安装 `net-tools`。

我们可以使用 ss(socket statistics) 或者 netstat 命令来查看 socket 信息:

```shell
# 查看 socket 连接的统计信息
# 主要统计处于各种状态的 tcp sockets 数量，以及其他 sockets 的统计信息
ss --summary
ss -s  # 缩写

# 查看哪个进程在监听 80 端口
# --listening 列出所有正在被监听的 socket
# --processes 显示出每个 socket 对应的 process 名称和 pid
# --numeric 直接打印数字端口号（不解析协议名称）
ss --listening --processes --numeric | grep 80
ss -nlp | grep 80  # 缩写
ss -lp | grep http  # 解析协议名称，然后通过协议名搜索监听

## 使用过时的 netstat
### -t tcp
### -u udp
netstat -tunlp | grep ":80"

# 查看 sshd 当前使用的端口号
ss --listening --processes | grep sshd
## 使用过时的 netstat
netstat -tunlp | grep <pid>  # pid 通过 ps 命令获得

# 列出所有的 tcp sockets，包括所有的 socket 状态
ss --tcp --all

# 只列出正在 listen 的 socket
ss --listening

# 列出所有 ESTABLISHED 的 socket（默认行为）
ss

# 统计 TCP 连接数
ss | grep ESTAB | wc -l

# 列出所有 ESTABLISHED 的 socket，并且给出连接的计时器
ss --options

# 查看所有来自 192.168.5 的 sockets
ss dst 192.168.1.5

# 查看本机与服务器 192.168.1.100 建立的 sockets
ss src 192.168.1.5
```

TCP 连接数受 Linux 文件描述符上限控制，可以通过如下方法查看已用文件句柄的数量。

```shell
# 已用文件描述符数量
lsof | wc -l
# 文件描述符上限
ulimit -n
```

### 8. 其他网络相关命令

主要是 iproute2 dhclient lsof 等

```shell
# 查看路由表
routel       # 旧的 net-tools 包中的命令
ip route ls  # iproute2 提供的新命令

# DHCP，先释放旧租约，再建立新租约
sudo dhclient -r eth0 && sudo dhclient eth0
# 查看 DHCP 租期
cat /var/lib/dhcp/dhcpd.leases

# 清理 DNS 缓存
## 1. 如果你使用的是 systemd-resolve，使用此命令
sudo systemd-resolve --flush-caches
sudo systemd-resolve --statistics  # 查看缓存状态
## 2. 如果使用的是 dnsmasq，使用此命令
sudo systemctl restart dnsmasq
sudo killall -HUP dnsmasq  # 直接发送 HUP 信号也可以
```

### 9. 容器网络诊断 - nsenter

Docker 容器有自己的 namespace，直接通过宿主机的 ss 命令是查看不到容器的 socket 信息的。

比较直观的方法是直接通过 `docker exec` 在容器中通过 ss 命令。但是这要求容器中必须自带 ss 等程序，有的精简镜像可能不会自带它。

通过 `nsenter` 可以直接进入到容器的指定 namespace 中，这样就能直接查询容器网络相关的信息了。

```shell
docker ps | grep xxx

echo CONTAINER=xxx  # 容器名称或 ID

# 1. 查询到容器对应的 pid
PID=$(docker inspect --format {{.State.Pid}} $CONTAINER)

# 2. nsenter 通过 pid 进入容器的 network namespace，执行 ss 查看 socket 信息
nsenter --target $PID --net ss -s
```

`nsenter` 这个工具貌似是 docker 自带的或者是系统内置命令，只要装了 docker，ubuntu/centos 都可以直接使用这个命令。

> nsenter 是一个进入名字空间的工具，功能不仅仅局限在「网络诊断」，还有更多用法。

### 10. 用户与群组

```shell
## 查看用户属于哪些群组
groups <user-name>  # 方法一
id <username>       # 方法二，它会额外列出 gid/uid
cat /etc/group | grep <user-name>  # 方法三，直接查看配置
## 查看群组中有哪些用户，第一列是群组，最后一列是用户名
cat /etc/group | grep <group-name>
```

## 二、Powershell

Powershell 是微软推出的一款新一代 shell，它的特点之一是，命令都有一致的命名规则：**谓词-名词**，
谓词表示动作：Get/Set/Stop/Start 等，名词指示操作对象：Service/Member/ChildItem/Command 等。

这样的命名格式使我们可以很容易地猜测到自己需要的命令的名称。

为了使用方便，powershell 还提供了一些常用命令的缩写，并且添加了大量类似 Linux 命令的别名。

还有就是，Windows 默认不区分字母大小写，日常使用可以全部小写。

### 1. 实用命令

```powershell
# 删除文件/文件夹
remove-item xxx  -confirm
ri xxx  # 别名1
rm xxx  # 别名2
rmdir xxx  # etc...

# 复制
copy-item xxx xx -r
cp -r xxx xx

# 显示工作目录
get-location
gl
pwd

# 切换工作目录
set-location xxx
sl xxx
cd xxx

# 查看环境变量
get-childitem env:
gci env:
gci env:PATH  # 查看 PATH 变量

$env:XXX="value"   # 临时设置环境变量
$env:Path += ";SomeRandomPath"  # 临时在 Path 末尾添加新路径
## 以下三行命令只对 windows 有效，linux 下无效
[Environment]::SetEnvironmentVariable("XXX", $env:XXX + ";value", [EnvironmentVariableTarget]::User)  # 修改当前用户的环境变量（永久），只对新进程有效
[Environment]::SetEnvironmentVariable("XXX", "value", [EnvironmentVariableTarget]::Machine)  # 给这台电脑设置环境变量（永久），只对新进程有效，需要管理员权限
[Environment]::SetEnvironmentVariable("XXX", $env:XXX + ";value", "User")  # target 也可用字符串指定

# 删除文件/文件夹
rm xxx  # 删除文件夹时会进入交互界面，按提示输入就行。

# 查看命名位置（类似 Linux Shell 的 which）
get-command xxx
gcm xxx

# 通过关键字查找 powershell 命令
gcm | select-string <keyword>

# 通过关键字查找 powershell 命令和环境变量中的程序，比较慢
gcm * | select-string <keyword>

# 查看别名对应的真实命令
get-alias

# 类似 linux 的 find/ls 命令
get-childitem -Recurse -Include *.py
gci -r -i *.py

# 清空终端的输出
clear-host
clear

# 查看文件内容
get-content xx.py | more
get-content xx.py | out-host -paging
cat xx.py
gc xx.py

# 字符串搜索，不能对对象使用
# 类似 linux 的 grep 命令
cat xxx.log | select-string <pattern>
gci env: | out-string  -stream | select-string <pattern>  # 需要先使用 out-string 将对象转换成 string
gci env: | where-object {$_.Name -like <pattern>}

# 计算输出的行数/对象个数
gci env: | measure-object
gci env: | measure  # 这是缩写

# 关机/重启
stop-computer
restart-computer

# windows 计算 hash 值
# 功能等同于 linux 下的 sha256sum/sha1sum/sha512sum/md5sum
Get-FileHash -Path /path/to/file -Algorithm SHA256
Get-FileHash -Path /path/to/file -Algorithm SHA256  | Format-List  # 用 format 修改格式化效果

# base64 编解码
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("xxx"))  # base64 编码
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("eHh4"))  # 解码

```

另外 windows 同样自带 ssh/scp 命令，参数也和 linux 一致

### 2. 进程相关命令

```powershell
# 查看所有进程
get-process | more
ps | more  # 别名

# 查找某进程（替代掉 tasklist）
get-process -name exp*,power*  # 使用正则查找进程
get-process | select-string <pattern>  # 效果同上

# 通过 id 杀掉某进程（替代掉 taskkill）
# 也可以通过 -Name 用正则匹配进程
stop-process <pid>
kill <pid>  # 别名
```

### 3. 网络相关命令

```powershell
## 1. dns 相关(dns-client)
Clear-DnsClientCache  # 清除 dns 缓存（替换掉 `ipconfig /flushdns`）
Get-DnsClientCache  # 查看 dns 缓存
Resolve-DnsName baidu.com  # 解析域名

# 更新 DHCP 租约
ipconfig /renew

## 2. TCP/IP 相关命令
Get-Command Get-Net*  # 查看所有 TCP/IP 相关的命令

Get-NetIPAddress  # 查看 IP 地址
Get-NetIPInterface  # 查看 IP 接口
Get-NetRoute        # 查看路由表
Get-NetNeighbor     # 获取链路层 MAC 地址缓存
Get-NetTCPConnection   # 查看 TCP 连接
### 也可以对 TCP/IP 的 IP 地址、接口、路由表进行增删改
New-NetRoute
Remove-NetNeighbor  # 清除 MAC 地址缓存
```

### 4. socket 信息查询 - netstat

Windows 系统和 macOS 一样，也没有 `ss`，但是自带 `netstat`，该命令和 Linux 下的 `netstat` 有一定差别，具体使用方法如下：

```powershell
netstat -?  # 查看使用帮助，很清晰易懂

# 查看那个进程在监听 80 端口，最后一列是进程的 Pid
netstat -ano | findstr 80        # windows 命令
netstat -ano | select-string 80  # powershell 命令，就是把 findstr 替换成 select-string

# 不仅列出 Pid，还给出 Pid 对应的可执行文件名称（需要管理员权限）
netstat -ano -b | select-string 80  # powershell 命令

# 列出所有 ESTABLISHED 的 socket（默认行为）
netstat

# 列出所有正在监听的端口
netstat -ano | findstr LISTENING

# 只列出 TCP 连接
netstat -ano -p TCP


# 查看路由表
route -?  # 查看使用帮助，很清晰易懂
route print    # 查看所有路由信息
route print -4  # 仅 ipv4
```

比如我们遇到端口占用问题时，就可以通过上述命令查找到端口对应的 Pid，然后使用 `kill <Pid>` 命令（powershell `stop-process` 的别名）杀死对应的进程。

## 三、Mac OS X

Mac OS X 系统也是 unix-like 系统，也使用 zsh/bash，因此大部分命令基本都跟 Linux 没啥区别，可以直接参考前面 Linux 一节的内容。

但是要注意一些坑：

- macos 自带的 tar 并不是 gnutar，命令使用方式不一样！
  - 解决：`brew install gnu-tar`，安装好后通过 `gtar` 调用，参数就跟 linux 一致了。
- 网络相关的命令区别较大，后面会详细介绍。
- MacOSX 使用 launchpad 作为系统服务管理器，跟 systemd 区别很大。

### 1. 查看 socket 信息

Mac OS X 系统目前没有 `ss`，但是自带 `netstat`，该命令和 Linux 下的 `netstat` 有一定差别，而且还很慢，还不能显示 pid.

所以 stackoverflow 上更推荐使用 `lsof`，几条常用命令记录如下

```shell
# -n 表示不显示主机名
# -P 表示不显示端口俗称
# 不加 sudo 只能查看以当前用户运行的程序
# 通用格式：
sudo lsof -nP -iTCP:端口号 -sTCP:LISTEN

# 查看所有 tcp 连接
lsof -nP -iTCP

# 查看所有监听端口相关的信息（command/pid）
lsof -nP -iTCP -sTCP:LISTEN
```

### 2. 其他网络相关命令

清理 DNS 缓存：

```shell
# macos 10.10+
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# 其他版本请自己网上搜...
```

```shell
# 查看所有网络接口及相关参数（ip/mac/type...）
ifconfig

# 查看路由表
netstat -nr
```

## 四、跨平台程序

### 1. vim

#### 常用技巧

移动：

- `0`/`^` 回到行首，`$` 去到行末
- w 跳到下个单词的首部，e 跳到下个单词末尾
  - 也能使用 2w 2e 这种命令按单词数量跳转

删除 `d` 或修改 `c`:

- dw 删除单词，d2w 删除两个单词
- d$ 删除到行末，`d0`/`d^` 删除到行首
- `d(`/`d{`/`d[[` 删除到文件首部，`d)`/`d}`/`d]]` 删除到文件末尾
- `r` 替换一个字符，`R` 持续往后替换

#### 多行修改

多行插入，主要用于加注释之类的：

- 光标停留在你需要插入文本的地方
- `ctrl`+`v` 进入 visual block 模式，选中多行
- 输入 `I`，进入编辑模式
- 输入 `#` 注释或者其他字符，但是注意不能输入换行符！也不能删除？
- 按两下 `Esc`，依次退出 Insert 和 visual block 模式，就插入成功了

多行删除：

- `v` 进入 visual 模式，在第一行，选中你想要删除的文本块
  - 或者也可以先进入 visual block 模式，再通过左右方向键选择文本。
- `ctrl`+`v` 进入 visual block 模式，选中多行
  - visual block 的特点是它是垂直选择，而 visual 模式是段落选择
- 按 `d` 键就能删除被选中的所有内容。

#### 多行替换（基本和 sed 一致）

多行行首插入注释符号 `#`

      :1,6 s/^/#/g
      :2,$ s/^/#/g   注：此为2行至尾行
      :% s/^/#/g     注：此为所有行

这里使用了正则表达式 `^` 匹配行首，改成 `$` 就可在行尾进行批量修改。

此外，它的分隔符也不仅限于 `\`，也可以用 `@` 等符号，方便阅读。比如：

      :1,6 s@^@#@g
      :2,$ s@^@#@g   注：此为2行至尾行
      :% s@^@#@g     注：此为所有行

使用 vim 的这个正则匹配功能，不仅能进行插入，也能完成删除、替换的功能。

#### 将选中部分写入到文件

- 首先按 `v` 进入 visual 模式，选中需要的内容
- 按 `:`，应该会显示 `:'<,'>`，表示对选中部分进行操作
- 输入内容 `w new.txt`，此时显示效果应该是 `:'<,'>w new.txt`
- 回车就能完成文件写入

#### 问题：在 vim 中粘贴 yaml 时缩进会变得一团糟

解决方法：在命令模式下输入 `:set paste` 进入粘贴模式，然后再粘贴 yaml 内容。

注意行首可能会丢失几个字符，需要手动补上。

## 参考

- [如何在 Linux 中查看进程占用的端口号](https://zhuanlan.zhihu.com/p/45920111)
- [github - nsenter](https://github.com/jpetazzo/nsenter#how-do-i-use-nsenter)
- [使用 lsof 代替 Mac OS X 中的 netstat 查看占用端口的程序](https://tonydeng.github.io/2016/07/07/use-lsof-to-replace-netstat/)
- [aws 常用命令](https://zhuanlan.zhihu.com/p/81123584)
