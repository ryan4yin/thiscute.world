---
title: "Python 视频转字符动画（一）60 行代码"
date: 2016-10-18T08:37:02+08:00
lastmod: 2022-08-13T14:16:02+08:00
draft: false

resources:
  - name: "featured-image"
    src: "video2chars-cli.webp"

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

> 本文最初于 2016-10-18 发表在[博客园](http://www.cnblogs.com/kirito-c/p/5971988.html)，2022-08-13 搬迁至 <https://thiscute.world>

昨晚我朋友 @三十六咲 跟我说在网上看到了别人做的视频转字符动画，觉得很厉害，我于是也打算玩玩。今天中午花时间实现了这样一个小玩意。
顺便把过程记录在这里。

> 注：最新版使用了画布方式实现，和本文相比改动非常大，如果对旧版本的实现没啥兴趣，可以直接移步 [video2chars](https://github.com/ryan4yin/video2chars/blob/master/doc/README-zh-cn.md)，它的效果动画见 [极乐净土](https://www.bilibili.com/video/av30469888/)。新版本的核心代码不算注释 70 行不到，功能更强大。

### 效果

先上效果，来点动力。

源视频 [【東方】Bad Apple!! ＰＶ【影絵】](https://www.bilibili.com/video/av706/) 转换后的效果如下：

{{< video
src="/videos/video2chars-1-basics/video2chars-cli-badapple.webm"
type="video/webm"
preload="auto"
autoplay="true"
loop="true" >}}

### 步骤

1. 将视频转化为一帧一帧的图片
2. 把图片转化为字符画
3. 按顺序播放字符画

### 一、准备

#### 1. 模块

这个程序需要用到这样几个模块:

1. opencv-python # 用来读取视频和图片
2. numpy # opencv-python 依赖于它

准备阶段，首先安装依赖：

```shell
pip3 install numpy opencv-python
```

然后新建 python 代码文档，在开头添加上下面的导入语句

```python
#-*- coding:utf-8 -*-

# numpy 是一个矩阵运算库，图像处理需要用到。
import numpy as np
```

#### 2. 材料

材料就是需要转换的视频文件了，我这里用的是[BadApple.mp4](https://github.com/ryan4yin/video2chars/blob/v0.3/resources/BadApple.mp4)，下载下来和代码放到同一目录下
你也可以换成自己的，建议是学习时尽量选个短一点的视频，几十秒就行了，不然调试起来很痛苦。（或者自己稍微修改一下函数，只转换一定范围、一定数量的帧。）
此外，要选择对比度高的视频。否则的话，就需要彩色字符才能有足够好的表现，有时间我试试。

### 二、按帧读取视频

现在继续添加代码，实现第一步：按帧读取视频。
下面这个函数，接受视频路径和字符视频的尺寸信息，返回一个 img 列表，其中的 img 是尺寸都为指定大小的灰度图。

```python
#导入 opencv
import cv2

def video2imgs(video_name, size):
    """

    :param video_name: 字符串, 视频文件的路径
    :param size: 二元组，(宽, 高)，用于指定生成的字符画的尺寸
    :return: 一个 img 对象的列表，img对象实际上就是 numpy.ndarray 数组
    """

    img_list = []

    # 从指定文件创建一个VideoCapture对象
    cap = cv2.VideoCapture(video_name)

    # 如果cap对象已经初始化完成了，就返回true，换句话说这是一个 while true 循环
    while cap.isOpened():
        # cap.read() 返回值介绍：
        #   ret 表示是否读取到图像
        #   frame 为图像矩阵，类型为 numpy.ndarry.
        ret, frame = cap.read()
        if ret:
            # 转换成灰度图，也可不做这一步，转换成彩色字符视频。
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # resize 图片，保证图片转换成字符画后，能完整地在命令行中显示。
            img = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)

            # 分帧保存转换结果
            img_list.append(img)
        else:
            break

    # 结束时要释放空间
    cap.release()

    return img_list
```

写完后可以写个 main 方法测试一下，像这样：

```python
if __name__ == "__main__":
    imgs = video2imgs("BadApple.mp4", (64, 48))
    assert len(imgs) > 10
```

如果运行没报错，就没问题
代码里的注释应该写得很清晰了，继续下一步。

### 三、图像转化为字符画

视频转换成了图像，这一步便是把图像转换成字符画
下面这个函数，接受一个 img 对象为参数，返回对应的字符画。

```python
# 用于生成字符画的像素，越往后视觉上越明显。。这是我自己按感觉排的，你可以随意调整。
pixels = " .,-'`:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"

def img2chars(img):
    """

    :param img: numpy.ndarray, 图像矩阵
    :return: 字符串的列表：图像对应的字符画，其每一行对应图像的一行像素
    """
    res = []

    # 灰度是用8位表示的，最大值为255。
    # 这里将灰度转换到0-1之间
    # 使用 numpy 的逐元素除法加速，这里 numpy 会直接对 img 中的所有元素都除以 255
    percents = img / 255

    # 将灰度值进一步转换到 0 到 (len(pixels) - 1) 之间，这样就和 pixels 里的字符对应起来了
    # 同样使用 numpy 的逐元素算法，然后使用 astype 将元素全部转换成 int 值。
    indexes = (percents * (len(pixels) - 1)).astype(np.int)

    # 要注意这里的顺序和 之前的 size 刚好相反（numpy 的 shape 返回 (行数、列数)）
    height, width = img.shape
    for row in range(height):
        line = ""
        for col in range(width):

            index = indexes[row][col]
            # 添加字符像素（最后面加一个空格，是因为命令行有行距却没几乎有字符间距，用空格当间距）
            line += pixels[index] + " "
        res.append(line)

    return res
```

上面的函数只接受一帧为参数，一次只转换一帧，可我们需要的是转换所有的帧，所以就再把它包装一下：

```python
def imgs2chars(imgs):
    video_chars = []
    for img in imgs:
        video_chars.append(img2chars(img))

    return video_chars
```

好了，现在我们可以测试一下：

```python
if __name__ == "__main__":
    imgs = video2imgs("BadApple.mp4", (64, 48))
    video_chars = imgs2chars(imgs)
    assert len(video_chars) > 10
```

没报错的话，就可以下一步了。(这一步比较慢，测试阶段建议用短一点的视频，或者稍微改一下，只处理前 30 秒之类的)

### 四、播放字符视频

写了这么多代码，现在终于要出成果了。现在就是最激动人心的一步：播放字符画了。
同样的，我把它封装成了一个函数。下面这个函数接受一个字符画的列表并播放。

1. 通用版（**使用 shell 的 clear 命令清屏，但是因为效率不高，可能会有一闪一闪的问题**）
   这个版本适用于 linux/windows

```python
# 导入需要的模块
import time
import subprocess

def play_video(video_chars):
    """
    播放字符视频
    :param video_chars: 字符画的列表，每个元素为一帧
    :return: None
    """
    # 获取字符画的尺寸
    width, height = len(video_chars[0][0]), len(video_chars[0])

    for pic_i in range(len(video_chars)):
        # 显示 pic_i，即第i帧字符画
        for line_i in range(height):
            # 将pic_i的第i行写入第i列。
            print(video_chars[pic_i][line_i])
        time.sleep(1 / 24)  # 粗略地控制播放速度。

        # 调用 shell 命令清屏
        subprocess.run("clear", shell=True)  # linux 版
        # subrpocess.run("cls", shell=True)  # cmd 版，windows 系统请用这一行。
```

2. Unix 系版本（**使用了只支援 unix 系 的 curses 库，比 clear 更流畅**）

```python
# 导入需要的模块
import time
import curses

def play_video(video_chars):
    """
    播放字符视频，
    :param video_chars: 字符画的列表，每个元素为一帧
    :return: None
    """
    # 获取字符画的尺寸
    width, height = len(video_chars[0][0]), len(video_chars[0])

    # 初始化curses，这个是必须的，直接抄就行
    stdscr = curses.initscr()
    curses.start_color()
    try:
        # 调整窗口大小，宽度最好略大于字符画宽度。另外注意curses的height和width的顺序
        stdscr.resize(height, width * 2)

        for pic_i in range(len(video_chars)):
            # 显示 pic_i，即第i帧字符画
            for line_i in range(height):
                # 将pic_i的第i行写入第i列。(line_i, 0)表示从第i行的开头开始写入。最后一个参数设置字符为白色
                stdscr.addstr(line_i, 0, video_chars[pic_i][line_i], curses.COLOR_WHITE)
            stdscr.refresh()  # 写入后需要refresh才会立即更新界面

            time.sleep(1 / 24)  # 粗略地控制播放速度(24帧/秒)。更精确的方式是使用游戏编程里，精灵的概念
    finally:
        # curses 使用前要初始化，用完后无论有没有异常，都要关闭
        curses.endwin()
    return
```

好，接下来就是见证奇迹的时刻
**不过开始前要注意，字符画的播放必须在 shell 窗口下运行，在 pycharm 里运行会看到一堆无意义字符。另外播放前要先最大化 shell 窗口**

```python
if __name__ == "__main__":
    imgs = video2imgs("BadApple.mp4", (64, 48))
    video_chars = imgs2chars(imgs)
    input("`转换完成！按enter键开始播放")
    play_video(video_chars)
```

写完后，开个 shell，最大化窗口，然后键入（文件名换成你的）

```shell
python3 video2chars.py
```

可能要等很久。我使用示例视频大概需要 12 秒左右。看到提示的时候，按回车，开始播放！

**这样就完成了视频到字符动画的转换, 除去注释, 大概七十行代码的样子. 稍微超出了点预期, 不过效果真是挺棒的. **

### 五、进一步优化

到了这里，核心功能基本都完成了。
不过仔细想想，其实还有很多可以做的：

- 能不能手动指定要转换的区间、帧率？
- 每次转换都要很久的时间，能不能边转换边播放？或者转换后把数据保存起来，下次播放时，就直接读缓存。
- 为啥我的字符动画没有声音，看无声电影么？
- 视频的播放速度能不能精确控制？
- 能不能用彩色字符？

这些东西，就不写这里了，再写下去，你们肯定要说我这标题是骗人了哈哈。
所以如果有兴趣的，请移步这个系列的下一篇：[视频转字符动画（二）进阶](https://thiscute.world/posts/video2chars-2/)

### 六、总结

完整代码见 [video2chars.py](https://github.com/ryan4yin/video2chars/blob/v0.3/src/video2chars.py)，要注意的是代码库的代码，包含了第二篇文章的内容（音频、缓存、帧率控制等），而且相对这篇文章也有一些小改动（目的是方便使用，但是稍微增加了点代码量，所以改动没有写在这篇文章里了）
想运行起来的话，还是建议跟着文章做。。

### 七、参考

- [Opencv-Python Tutorials - Video Playing](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html#display-video)
- [Python 图片转字符画](https://www.shiyanlou.com/courses/370)

> 允许转载, 但是要求附上来源链接: [Python 视频转字符动画（一）60 行代码](/posts/video2chars-1-basics/)
