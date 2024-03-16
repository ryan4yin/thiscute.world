---
title: "Python 视频转字符动画（二）进阶"
date: 2018-05-25T18:08:02+08:00
lastmod: 2022-08-13T14:16:02+08:00
draft: false

resources:
  - name: "featured-image"
    src: "video2chars-html.webp"

tags: []
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false

code:
  # whether to show the copy button of the code block
  copy: true
  # the maximum number of lines of displayed code by default
  maxShownLines: 300
---

> 本文最初于 2018-05-25 发表在[博客园](https://www.cnblogs.com/kirito-c/p/9089873.html)，2022-08-13 搬迁至 <https://thiscute.world>

### 0. 话说在前头

最新版使用了画布方式实现，和本文相比改动非常大，如果对旧版本的实现没啥兴趣，可以直接移步 [video2chars](https://github.com/ryan4yin/video2chars/blob/master/doc/README-zh-cn.md)，它的效果动画见 [极乐净土](https://www.bilibili.com/video/av30469888/)。新版本的核心代码不算注释70行不到，功能更强大。

下面的效果动画是使用 html 实现的字符动画效果（上一篇的效果动画是 shell 版的）：

{{< video
src="/videos/video2chars-2/video2chars-html.webm"
type="video/webm"
preload="auto"
autoplay="true"
loop="true" >}}

> 本文的优化仍然是针对 shell 版本的，html 版由于缺陷太大就不写文章介绍了。

### 1. 速度优化

要是每次播放都要等个一分钟，也太痛苦了一点。
所以可以用 pickle 模块把 video_chars 保存下来，下次播放时，如果发现当前目录下有这个保存下来的数据，就跳过转换，直接播放了。这样就快多了。
只需要改一下测试代码，
先在开头添加两个依赖

```python
import os
import pickle
```

然后在文件结尾添加代码：

```python
def dump(obj, file_name):
    """
    将指定对象，以file_name为名，保存到本地
    """
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
    return


def load(filename):
    """
    从当前文件夹的指定文件中load对象
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def get_file_name(file_path):
    """
    从文件路径中提取出不带拓展名的文件名
    """
    # 从文件路径获取文件名 _name
    path, file_name_with_extension = os.path.split(file_path)

    # 拿到文件名前缀
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return file_name


def has_file(path, file_name):
    """
    判断指定目录下，是否存在某文件
    """
    return file_name in os.listdir(path)


def get_video_chars(video_path, size):
    """
    返回视频对应的字符视频
    """
    video_dump = get_file_name(video_path) + ".pickle"

    # 如果 video_dump 已经存在于当前文件夹，就可以直接读取进来了
    if has_file(".", video_dump):
        print("发现该视频的转换缓存，直接读取")
        video_chars = load(video_dump)
    else:
        print("未发现缓存，开始字符视频转换")

        print("开始逐帧读取")
        # 视频转字符动画
        imgs = video2imgs(video_path, size)

        print("视频已全部转换到图像， 开始逐帧转换为字符画")
        video_chars = imgs2chars(imgs)

        print("转换完成，开始缓存结果")
        # 把转换结果保存下来
        dump(video_chars, video_dump)
        print("缓存完毕")

    return video_chars


if __name__ == "__main__":
    # 宽，高
    size = (64, 48)
    # 视频路径，换成你自己的
    video_path = "BadApple.mp4"
    video_chars = get_video_chars(video_path, size)
    play_video(video_chars)
```

另一个优化方法就是边转换边播放，就是同时执行上述三个步骤。学会了的话，可以自己实现一下试试。

### 2. 字符视频和音乐同时播放

没有配乐的动画，虽然做出来了是很有成就感，但是你可能看上两遍就厌倦了。
所以让我们来给它加上配乐。（不要担心，其实就只需要添加几行代码而已）

首先我们需要找个方法来播放视频的配乐，怎么做呢？
先介绍一下一个跨平台视频播放器：[**mpv**](https://mpv.io)，它有很棒的命令行支持，请先安装好它。
要让 mpv 只播放视频的音乐部分，只需要命令：

```shell
mpv --no-video video_path
```

好了，现在有了音乐，可总不能还让人开俩shell，先放音乐，再放字符画吧。
这时候，我们需要的功能是：[使用 Python 调用外部应用](https://www.cnblogs.com/kirito-c/p/9088276.html#python-invoke).
但是 mpv 使用了类似 curses 的功能，标准库的 os.system 不能隐藏掉这个部分，播放效果不尽如人意。
因此我使用了 [pyinvoke](https://github.com/pyinvoke/invoke) 模块，只要给它指定参数`hide=True`，就可以完美隐藏掉被调用程序的输出（指 stdout，其实 subprocess 也可以的）。运行下面代码前，请先用pip安装好 invoke.（能够看到这里的，安装个模块还不是小菜一碟）

好了废话说这么多，上代码：

```python
import invoke

video_path = "BadApple.mp4"
invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)
```

运行上面的测试代码，如果听到了音乐，而shell啥都没输出，但是能听到音乐的话，就正常了。我们继续。（这里使用了python3.6的f字符串）

音乐已经有了，那就好办了。
添加一个播放音乐的函数

```python
import invoke
def play_audio(video_path):
    invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)
```

然后修改main()方法：

```python
def main():
    # 宽，高
    size = (64, 48)
    # 视频路径，换成你自己的
    video_path = "BadApple.mp4"

    # 只转换三十秒，这个属性是才添加的，但是上一篇的代码没有更新。你可能需要先上github看看最新的代码。其实就稍微改了一点。
    seconds = 30

    # 这里的fps是帧率，也就是每秒钟播放的的字符画数。用于和音乐同步。这个更新也没写进上一篇，请上github看看新代码。
    video_chars, fps = get_video_chars(video_path, size, seconds)

    # 播放音轨
    play_audio(video_path)

    # 播放视频
    play_video(video_chars, fps)


if __name__ == "__main__":
    main()
```

然后运行。。并不是我坑你，你只听到了声音，却没看到字符画。。原因是： invoke.run()函数是阻塞的，音乐没放完，代码就到不了`play_video(video_chars, fps)`这一行。

所以 `play_audio` 还要改一下，改成这样：

```python
import invoke
from threading import Thread

def play_audio(video_path):
    def call():
        invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)

    # 这里创建子线程来执行音乐播放指令，因为 invoke.run() 是一个阻塞的方法，要同时播放字符画和音乐的话，就要用多线程/进程。
    # P.S. 更新：现在发现可以用 subprocess.Popen 实现异步调用 mpv，不需要开新线程。有兴趣的同学可以自己试试。
    p = Thread(target=call)
    p.setDaemon(True)
    p.start()
```

这里使用标准库的 threading.Thread 类来创建子线程，让音乐的播放在子线程里执行，然后字符动画还是主线程执行，Ok，这就可以看到最终效果了。实际上只添加了十多行代码而已。

### 3. 彩色字符动画

1. html+javascript 方式：核心都是一样的内容，只是需要点 html 和 javascript 的知识。代码见 [video2chars-html](https://github.com/ryan4yin/video2chars/blob/v0.3/src/video2html.py)
2. 画布方式：直接把画在图片上，然后自动合成为 mp4 文件。这种方式要优于 html 方式，而且有个很方便的库能用，核心代码就 70 行的样子。代码见 [video2chars](https://github.com/ryan4yin/video2chars/)

### 参考

- [Python将视频转换为全字符视频（含音频）](https://blog.csdn.net/kongfu_cat/article/details/79681719)
