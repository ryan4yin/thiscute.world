---
title: "常见压缩格式的区别，及 Linux 下的压缩相关指令"
date: 2019-01-14T19:51:00+08:00
draft: false
resources:
  - name: "featured-image"
    src: "tar-compression.webp"

tags: ["Linux", "Compression", "压缩", "tar"]
categories: ["tech"]

code:
  # whether to show the copy button of the code block
  copy: false
  # the maximum number of lines of displayed code by default
  maxShownLines: 100
---

> 可先浏览加粗部分

## 一、常见压缩档

    *.zip        |    zip 程序压缩打包的档案；  （很常见，但是因为不包含文档名编码信息，跨平台可能会乱码）
    *.rar        |    rar 程序压缩打包的档案；（在windows上很常见，但是是商业软件。）
    *.gz         |   gzip 程序压缩的档案； （linux目前使用最广泛的压缩格式）
    *.bz2        |   bzip2 程序压缩的档案；
    *.xz         |    xz 程序压缩的档案；
    *.tar        |    tar 程序打包的资料，并没有压缩过；
    *.tar.gz     |    tar 程序打包的档案，其中并且经过 gzip 的压缩 （最常见）
    *.tar.bz2    |   tar 程序打包的档案，其中并且经过 bzip2 的压缩
    *.tar.xz     |   tar 程序打包的档案，其中并且经过 xz 的压缩 （新一代压缩选择）
    *.7z         |  7zip 程序压缩打包的档案。

目前最常见的是 `tar.gz` `tar.xz` `tar.7z` 这三种格式。

## 二、以能否压缩多文档分类

1. `gzip` `bzip2` `xz` 这三个压缩格式都**只能压缩单个文档**。（换而言之，该进程的输入输出
   都是流，不包含文档树信息。）因此如果要用它们压缩多个文档或目录，需要使用另一个软件来先
   将要压缩的文档打包成一个文档（包含文档树信息），这个命令就是 `tar`. 先使用 `tar` 归档要
   压缩的多文档，再对生成的 `*.tar` 使用 上述压缩指令（或者直接使用管道重定向），Linux 下
   是这样实现多文档压缩的。

2. 而 `7z` 和 `zip`，以及 `rar` 格式，都**同时具有了 归档(tar) 和 压缩 两个功能**，（也就
   是该格式包含了文档树信息咯）也就是说它们可以直接压缩多个文档。

## 三、各格式使用的算法差别

1. `gzip` 成熟的格式，使用的算法基于 DEFLATE。（压缩比适中）
2. `7z` 新一代格式，使用的压缩算法可替换，默认是使用的 lzma/lzma2 算法，使用 AES-256 作为
   加密算法。
3. `xz` 同样使用的 lzma/lzma2 算法，不过只能压缩一个文档。（压缩比很高，相对的用时也更多）
4. `zip` 同样是支持多种算法的压缩格式，默认应该是使用的 DEFLATE 算法。诞生较早，有很多缺
   陷。（跨平台乱码、容易被破解等）
5. `rar` 使用 类DEFLATE 的专有算法，使用 AES 加密。(rar5.0 以后使用 AES-256CBC)

不过 `zip` 被广泛应用在安卓的 `apk` 格式、`java` 的 `jar`、电子书的 `epub`，还有 github、
云硬盘的多文档下载中，原因嘛大概是 `zip` 很流行，所以不用担心目标平台没解压软件吧。

## 四、如何选用压缩方案

1. `tar.gz` 在 linux 上最常见，在压缩率和压缩时间上拥有良好的平衡。如果有任何疑惑，就选用
   它吧，不会错。
2. `tar.xz` 是新一代的压缩格式，虽然拥有更好的压缩率，压缩/解压速度相对要慢很多倍。一般在
   电脑性能足够好的时候，可选用它。
3. `7z` 和 xz 同为新一代压缩格式，它更复杂，支持多文档压缩。而且更适合跨平台，推荐使用。
4. `zip` 因为跨平台容易导致文档名乱码，不建议使用。（虽然有这样的缺陷，但是却意外的用得很
   广泛，在前一节有说过）
5. `rar` 性能不差，但是是商业格式，不开源，不建议使用。（**做得比较好的是它的 recovery
   records，在网络环境不好，容易导致包损坏时，这个功能就特别棒**）
6. `tar.bz2` 算是 linux 压缩历史上，过渡时期的产物，性能也介于 gz 和 xz 之间，一般来说不需
   要考虑它。

总的来说，就是 Windows 上推荐使用 `7z`，而 Linux 上 推荐使用 `tar.gz` `tar.xz` `7z` 之一。
此外 `rar` 的损坏很容易修复，`zip` 受众多（要注意乱码问题），也可以考虑。

## 五、Linux 上的压缩相关指令

### 1. tar 指令

通过之前的介绍，可以看出常用的就是 tar gzip xz 等，如果要压缩多个文档，需要先使用tar，再用
管道重定向到 gzip 或 xz，比较麻烦，而这几个指令又很常用。于是后来对tar做了增强。tar 最初只
是一个归档进程，而压缩则由其他的压缩软件来完成（一个进程只干一件事）。后来为了方便，丧心病
狂地集成了各种压缩指令。因此这里就只介绍这一个命令了（它囊括了所有）。tar 的选项与参数非常
的多！我们只讲几个常用的选项，更多选项您可以自行 man tar 查询啰！

```bash
[dmtsai@study ~]$ tar [-z|-j|-J] [cv] [-f 待创建的新档名] filename... <==打包与压缩
[dmtsai@study ~]$ tar [-z|-j|-J] [tv] [-f 既有的 tar档名]             <==察看档名
[dmtsai@study ~]$ tar [-z|-j|-J] [xv] [-f 既有的 tar档名] [-C 目录]   <==解压缩
```

#### 选项与参数

    -c  ：创建打包档案，可搭配 -v 来察看过程中被打包的档名(filename)
    -t  ：察看打包档案的内容含有哪些档名，重点在察看『档名』就是了；
    -x  ：解打包或解压缩的功能，可以搭配 -C (大写) 在特定目录解开
          特别留意的是， -c, -t, -x 不可同时出现在一串指令列中。
    -z  ：透过 gzip  的支持进行压缩/解压缩：此时档名最好为 *.tar.gz
    -j  ：透过 bzip2 的支持进行压缩/解压缩：此时档名最好为 *.tar.bz2
    -J  ：透过 xz    的支持进行压缩/解压缩：此时档名最好为 *.tar.xz
          特别留意， -z, -j, -J 不可以同时出现在一串指令列中
    -v  ：在压缩/解压缩的过程中，将正在处理的档名显示出来！
    -f filename：-f 后面要立刻接要被处理的档名！建议 -f 单独写一个选项啰！(比较不会忘记)
    -C 目录    ：这个选项用在解压缩，若要在特定目录解压缩，可以使用这个选项。

其他后续练习会使用到的选项介绍：

> -p(小写) ：保留备份资料的原本权限与属性，常用于备份(-c)重要的设定档 -P(大写) ：保留绝对
> 路径，亦即允许备份资料中含有根目录存在之意；--exclude=FILE：在压缩的过程中，不要将 FILE
> 打包！

#### 其实最简单的使用 tar 就只要记忆底下的方式即可

- **压缩：`tar -zcv -f filename.tar.gz <要被压缩的档案或目录名称>`**
- **查看文档树：`tar -ztv -f filename.tar.gz`**
- **解压缩：`tar -zxv -f filename.tar.gz -C` <欲解压缩的目录>`**

上面的命令需要根据压缩格式的不同，选用 `-z` `-j` `-J` 选项，而实际上文档的后缀就已经表明了
它的压缩格式，不免让人觉得多余。因此就有这幺一条通用的压缩/解压 option

    -a, --auto-compress
                  Use archive suffix to determine the compression program.

使用这个，便有了**通用的解压指令**：

> **<font color=#0099ff size=4>tar -axv -f file.tar.\* </font> （它适用于上述三种压缩格
> 式）**

#### 仅解压指定的文档

1. 先查看文档树找到需要解压的文档的文档名
2. tar -zxv -f 打包档.tar.gz 待解开档名

#### 打包某目录，但不含该目录下的某些档案之作法

使用 --exclude=FILE 选项（支持文档名的模式匹配，而且可重复）

    tar -zcv -f filename.tar.gz directory --exclude=FILE1 --exclude=func*

##### 只打包目录中比指定时刻更新的文档

使用 `--newer-mtime="2015/06/17"` 选项。

##### tarfile, tarball

    tarfile  |  纯打包、未压缩的 tar 文档
    tarball  |  压缩了的 tar 文档

#### 2. zip格式（linux 一般也会自带，详细的请man）

1. 压缩命令：`zip`

   - 压缩目录：`zip -r filename.zip directory`
     - `r` 表示递归压缩，压缩包会包含这个目录

2. 解压命令：`unzip`
   - 解压到某目录：`unzip -d directory filename.zip` (`-d dir` 表示将内容解压到dir目录内)
     - -t 测试压缩档的完整性
     - -x filename 排除某文档

#### 3. 7z格式（需要p7zip，deepin自带，更多的请man）

1. 查看目录树：`7z l file.7z` (List contents of archive)
2. 压缩：`7z a file.7z file1 directory1` (a 为创建压缩档或向压缩档中添加文档/目录，一次可
   指定多个要压缩的文档或目录)
3. 解压：`7z x file.7z -o directory` (解压到指定目录)
4. 测试完整性： `7z t file.7z`

`p7zip` 安装好后，会提供 `7z`、`7za`、`7zr` 三个指令，一般来说直接用 `7z` 就行。

> P.S. `7z` 不会保存 Linux 文档的用户、用户组信息，因此不能直接用于 `Linux` 系统备份，此时
> 建议用 `tar.xz` 或 `tar.7z`（也就是先用tar打包）

#### 4. rar格式（还是那句话，更多的请man）

`rar` 是非开源的格式，Linux 默认是不会包含 `rar` 压缩软件的，但是它的解压软件是开源
的，`deepin` 自带 `unrar`，顺便 `7zip` 也可解压 `rar` 文档。若想用linux创建rar压缩档，需要
从[rarlab](https://www.rarlab.com)上下载 Linux 版，（deepin源自带）不过要注意的是该 linux
版是 40 天试用版，要长期使用的话，可能需要破解。（rar 的 key 网上一搜一大把）

1. 压缩：`rar a file.rar file` （这个是试用的）
2. 解压：`unrar x file.rar` （这个开源免费）

其实我挺中意 `rar` 的修复功能的，不知道为啥 `7z` `xz` 这样的新格式没有添加类似的
`recorvery records`。上次下个 `idea` 的 `tarball`，下了四五次才下到一个完整的，要是用
`rar` 的话，大概一键修复就好了，可 `tar.gz` 我不知道怎幺修复，只好一遍遍重复下载。。

### 六、参考

- [档案与档案系统的压缩,打包与备份](http://linux.vbird.org/linux_basic/0240tarcompress.php)
- 维基百科
- [rar tar gz zip 7z 有什幺区别? - 知乎](https://www.zhihu.com/question/26026741/answer/31869734)
- [为什幺linux的包都是.tar.gz？要解压两次 - 知乎](https://www.zhihu.com/question/37019479/answer/70054550)
