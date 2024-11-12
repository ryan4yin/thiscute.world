---
title: "EE 入门（二） - 使用 ESP32 与 SPI 显示屏绘图、显示图片、跑贪吃蛇"
date: 2023-03-05T21:57:01+08:00
lastmod: 2023-03-05T21:57:01+08:00
draft: false

featuredImage: "tft_esp32_show_image-2.webp"
resources:
  - name: featured-image
    src: "tft_esp32_show_image-2.webp"
authors: ["ryan4yin"]

tags:
  [
    "电子电路",
    "Electrical Engineering",
    "MCU",
    "ESP32",
    "SPI",
    "GPIO",
    "贪吃蛇",
    "显示屏",
  ]
categories: ["tech"]
series: ["EE 入门"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false

# 兼容旧的 Path（单词拼写错误）
aliases:
  - /posts/ee-basics-esp32-display/
---

## 零、硬件准备与依赖库调研

之前淘货买了挺多显示屏的，本文使用的是这一块：

- [3.5 寸电阻触摸屏，480 \* 320，SPI 协议，显示屏驱动 IC 为 ILI9488](http://www.lcdwiki.com/3.5inch_SPI_Module_ILI9488_SKU:MSP3520)

开发板是 ESP-WROOM-32 模组开发板。其他需要的东西：杜邦线、面包板、四个 10 K$\Omega$ 电阻、
四个按键。

至于需要的依赖库，我找到如下几个 stars 数较高的支持 ILI9488 + ESP32 的显示屏驱动库：

- [Bodmer/TFT_eSPI](https://github.com/Bodmer/TFT_eSPI): 一个基于 Arudino 框架的 tft 显示
  屏驱动，支持 STM32/ESP32 等多种芯片。
- [lv_port_esp32](https://github.com/lvgl/lv_port_esp32): lvgl 官方提供的 esp32 port，但是
  几百年不更新了，目前仅支持到 esp-idf v4，试用了一波被坑了，不建议使用。
- [esp-idf/peripherals/lcd](https://github.com/espressif/esp-idf/tree/master/examples/peripherals/lcd):
  ESP 官方的 lcd 示例，不过仅支持部分常见显示屏驱动，比如我这里用的 ili9488 官方就没有。

总之强烈推荐 TFT_eSPI 这个库，很好用，而且驱动支持很齐全。

## 一、开发环境搭建、电路搭建与测试

### 1. 创建项目并配置好环境

ESP32 开发有好几种方式：

1. vscode 的 esp-idf 插件 + 官方的 esp-idf 工具
2. vscode 的 platformio 插件 + arudino 框架

[Bodmer/TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) 这个依赖库两种方式都支持，不过看了下
官方文档，仓库作者表示 ESP-IDF 的支持是其他人提供的，他不保证能用，所以稳妥起见我选择了
PlatformIO + Arduino 框架作为开发环境。

首先当然是创建一个空项目，点击 VSCode 侧栏的 PlatformIO 图标，再点击列表中的
`PlatformIO Core CLI` 选项进入 shell 执行如下命令：

```shell
pio project init --ide=vscode -d tft_esp32_arduino
```

这条命令会创建一个空项目，并配置好 vscode 插件相关配置，这样就算完成了一个空的项目框架。

### 1. 显示屏接线与项目参数配置

网上简单搜了下 ESP32 pinout，找到这张图，引脚定义与我的 ESP32 开发板完全一致，用做接线参
考：

{{<figure src="/images/ee-basics-2-esp32-display/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.webp" width="70%">}}

可以看到这块 ESP32 开发板有两个 SPI 端口：HSPI 跟 VSPI，这里我们使用 HSPI，那么
MOSI/MISO/SCK 三个引脚的接线必须与上图的定义完全一致。而其他引脚随便找个普通 GPIO 口接上就
行。

此外背光灯的线我试了下接 GPIO 口不好使，建议直接接在 3V3 引脚上（缺点就是没法通过程序关闭
背光，问题不大）。

我的接线如下：

{{<figure src="/images/ee-basics-2-esp32-display/esp32-spi-display-wiring.webp" width="70%" title="使用 wokwi.com 制作的示意图">}}
{{<figure src="/images/ee-basics-2-esp32-display/esp32-spi-display-wiring-real.webp" width="70%" title="接线实操">}}

线接好后需要更新下 PlatformIO 项目根目录 `platformio.ini` 的配置，使其显示屏引脚相关的参数
与我们的接线完全对应起来，这样才能正常驱动这个显示屏。

这里我以驱动库官方提供的模板
[Bodmer/TFT_eSPI/docs/PlatformIO](https://github.com/Bodmer/TFT_eSPI/tree/master/docs/PlatformIO)
为基础，更新了其构建参数对应的引脚，加了点注释，得到的内容如下（如果你的接线与我一致，直接
抄就行）：

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
  bodmer/TFT_eSPI@^2.5.0
  Bodmer/TFT_eWidget@^0.0.5
monitor_speed = 115200
build_flags =
  -Os
  -DCORE_DEBUG_LEVEL=ARDUHAL_LOG_LEVEL_DEBUG
  -DUSER_SETUP_LOADED=1

  ; Define the TFT driver, pins etc here:
  ; 显示屏驱动要对得上
  -DILI9488_DRIVER=1
  # 宽度与高度
  -DTFT_WIDTH=480
  -DTFT_HEIGHT=320
  # SPI 引脚的接线方式，
  -DTFT_MISO=12
  -DTFT_MOSI=13
  # SCLK 在显示屏上对应的引脚可能叫 SCK，是同一个东西
  -DTFT_SCLK=14
  -DTFT_CS=15
  # DC 在显示屏上对应的引脚可能叫 RS 或者 DC/RS，是同一个东西
  -DTFT_DC=4
  -DTFT_RST=2
  # 背光暂时直接接在 3V3 上
  ; -DTFT_BL=27
  # 触摸，暂时不用
  ;-DTOUCH_CS=22
  -DLOAD_GLCD=1
  # 其他配置，保持默认即可
  -DLOAD_FONT2=1
  -DLOAD_FONT4=1
  -DLOAD_FONT6=1
  -DLOAD_FONT7=1
  -DLOAD_FONT8=1
  -DLOAD_GFXFF=1
  -DSMOOTH_FONT=1
  -DSPI_FREQUENCY=27000000
```

修好后保存修改，platformio 将会自动检测到配置文件变更，并根据配置文件下载 Arduino/ESP32 工
具链，更新构建配置、拉取依赖库（建议开个全局代理，不然下载会贼慢）。

### 3. 测试验证

现在找几个 demo 跑跑看，新建文件 `src/main.ino`，从如下文件夹中随便找个 demo copy 进去然后
编译上传，看看效果：

- [Bodmer/TFT_eSPI - examples/480x320](https://github.com/Bodmer/TFT_eSPI/blob/master/examples/480%20x%20320)

> 可以直接从 libdeps 中 copy examples 代码过来测
> 试：`cp .pio/libdeps/esp32dev/TFT_eSPI/examples/480\ x\ 320/TFT_Meters/TFT_Meters.ino src/main.ino`

我跑出来的效果：

{{<figure src="/images/ee-basics-2-esp32-display/tft_esp32_meters_demo_2.webp" width="60%">}}
{{<figure src="/images/ee-basics-2-esp32-display/tft_esp32_sin_cosin_chart_2.webp" width="60%">}}

## 二、显示图片、文字

这需要首先将图片/文字转换成 bitmap 格式的 C 代码，可使用在线工具
[javl/image2cpp](https://github.com/javl/image2cpp) 进行转换，简单演示下：

{{<figure src="/images/ee-basics-2-esp32-display/how-to-use-image2cpp.webp" width="50%">}}

注意高度与宽度调整为与屏幕大小一致，设置放缩模式，然后色彩改为 RGB565，最后上传图片、生成
代码。

将生成好的代码贴到 `src/test_img.h` 中：

```c
// We need this header file to use FLASH as storage with PROGMEM directive:

// Icon width and height
const uint16_t imgWidth = 480;
const uint16_t imgHeight = 320;

// 'evt_source', 480x320px
const uint16_t epd_bitmap_evt_source [] PROGMEM = {
  // 这里省略掉图片内容......
}
```

然后写个主程序 `src/main.ino` 显示图像：

```c
#include <TFT_eSPI.h>       // Hardware-specific library

TFT_eSPI tft = TFT_eSPI();  // Invoke custom library

// Include the header files that contain the icons
#include "test_img.h"

void setup()
{
  Serial.begin(115200);
  tft.begin();
  tft.setRotation(1);	// landscape

  tft.fillScreen(TFT_BLACK);
  // Swap the colour byte order when rendering
  tft.setSwapBytes(true);

  // 显示图片
  tft.pushImage(0, 0, imgWidth, imgHeight, epd_bitmap_evt_source);

  delay(2000);
}

void loop() {}
```

编译上传，效果如下：

{{<figure src="/images/ee-basics-2-esp32-display/tft_esp32_show_image-2.webp" width="60%">}}

## 三、写个极简贪吃蛇游戏

N 年前我写的第一篇博客文章，是用 C 语言写一个贪吃蛇，这里把它移植过来玩玩看~

我的旧文章地址
为：[贪吃蛇—C—基于easyx图形库(下):从画图程序到贪吃蛇【自带穿墙术】 ](https://www.cnblogs.com/kirito-c/p/5596160.html)，
里面详细介绍了程序的思路。

那么现在开始代码移植，TFT 屏幕前面已经接好了不需要动，要改的只有软件部分，还有就是添加上下
左右四个按键的电路。

首先清空 `src` 文件夹，新建文件 `src/main.ino`，内容如下，其中主要逻辑均移植自我前面贴的文
章：

```c
#include <math.h>
#include <stdio.h>
#include <TFT_eSPI.h> // Hardware-specific library

#define WIDTH 480
#define HEIGHT 320

// 四个方向键对应的 GPIO 引脚
#define BUTTON_UP_PIN     5
#define BUTTON_LEFT_PIN   18
#define BUTTON_DOWN_PIN   19
#define BUTTON_RIGHT_PIN  21

TFT_eSPI tft = TFT_eSPI(); // Invoke custom library

typedef struct Position // 坐标结构
{
  int x;
  int y;
} Pos;

Pos SNAKE[3000] = {0};
Pos DIRECTION;
Pos EGG;
long SNAKE_LEN;

void setup()
{
  Serial.begin(115200);
  tft.begin();
  tft.setRotation(1); // landscape

  tft.fillScreen(TFT_BLACK);
  // Swap the colour byte order when rendering
  tft.setSwapBytes(true);

  // initialize the pushbutton pin as an input: the default state is LOW
  pinMode(BUTTON_UP_PIN, INPUT);
  pinMode(BUTTON_LEFT_PIN, INPUT);
  pinMode(BUTTON_DOWN_PIN, INPUT);
  pinMode(BUTTON_RIGHT_PIN, INPUT);

  init_game();
}

void loop()
{
  command(); // 获取按键消息
  move();    // 修改头节点坐标-蛇的移动
  eat_egg();
  draw(); // 作图
  eat_self();
  delay(100);
}

void init_game() {
  // 初始化小蛇
  SNAKE_LEN = 1;
  SNAKE[0].x =  random(50, WIDTH - 50); // 头节点位置随机化
  SNAKE[0].y =  random(50, HEIGHT - 50);
  DIRECTION.x = pow(-1, random()); // 初始化方向向量
  DIRECTION.y = 0;
  creat_egg();

  Serial.println("GAM STARTED, Having Fun~");
}

void creat_egg()
{
  while (true)
  {
    int ok = 0;
    EGG.x = random(50, WIDTH - 50); // 头节点位置随机化
    EGG.y = random(50, HEIGHT - 50);
    for (int i = 0; i < SNAKE_LEN; i++)
    {
      if (SNAKE[i].x == 0 && SNAKE[i].y == 0)
        continue;
      if (fabs(SNAKE[i].x - EGG.x) <= 10 && fabs(SNAKE[i].y - EGG.y) <= 10)
        ok = -1;
      break;
    }
    if (ok == 0)
      return;
  }
}

void command() // 获取按键命令命令
{
  if (digitalRead(BUTTON_LEFT_PIN) == HIGH) {
      if (DIRECTION.x != 1 || DIRECTION.y != 0)
      { // 如果不是反方向，按键才有效
        Serial.println("Turn Left!");
        DIRECTION.x = -1;
        DIRECTION.y = 0;
      }
  } else if (digitalRead(BUTTON_RIGHT_PIN) == HIGH) {
      if (DIRECTION.x != -1 || DIRECTION.y != 0)
      {
        Serial.println("Turn Right!");
        DIRECTION.x = 1;
        DIRECTION.y = 0;
      }
  } else if (digitalRead(BUTTON_UP_PIN) == HIGH) {
      if (DIRECTION.x != 0 || DIRECTION.y != 1)
      {  // 注意 Y 轴，向上是负轴，因为屏幕左上角是原点 (0,0)
        Serial.println("Turn Up!");
        DIRECTION.x = 0;
        DIRECTION.y = -1;
      }
  } else if (digitalRead(BUTTON_DOWN_PIN) == HIGH) {
      if (DIRECTION.x != 0 || DIRECTION.y != -1)
      {
        Serial.println("Turn Down!");
        DIRECTION.x = 0;
        DIRECTION.y = 1;
      }
  }
}

void move() // 修改各节点坐标以达到移动的目的
{
  // 覆盖尾部走过的痕迹
  tft.drawRect(SNAKE[SNAKE_LEN - 1].x - 5, SNAKE[SNAKE_LEN - 1].y - 5, 10, 10, TFT_BLACK);

  for (int i = SNAKE_LEN - 1; i > 0; i--)
  {
    SNAKE[i].x = SNAKE[i - 1].x;
    SNAKE[i].y = SNAKE[i - 1].y;
  }
  SNAKE[0].x += DIRECTION.x * 10; // 每次移动10pix
  SNAKE[0].y += DIRECTION.y * 10;

  if (SNAKE[0].x >= WIDTH) // 如果越界，从另一边出来
    SNAKE[0].x = 0;
  else if (SNAKE[0].x <= 0)
    SNAKE[0].x = WIDTH;
  else if (SNAKE[0].y >= HEIGHT)
    SNAKE[0].y = 0;
  else if (SNAKE[0].y <= 0)
    SNAKE[0].y = HEIGHT;
}

void eat_egg()
{
  if (fabs(SNAKE[0].x - EGG.x) <= 5 && fabs(SNAKE[0].y - EGG.y) <= 5)
  {
    // shade old egg
    tft.drawCircle(EGG.x, EGG.y, 5, TFT_BLACK);
    creat_egg();
    // add snake node
    SNAKE_LEN += 1;
    for (int i = SNAKE_LEN - 1; i > 0; i--)
    {
      SNAKE[i].x = SNAKE[i - 1].x;
      SNAKE[i].y = SNAKE[i - 1].y;
    }
    SNAKE[0].x += DIRECTION.x * 10; // 每次移动10pix
    SNAKE[0].y += DIRECTION.y * 10;
  }
}

void draw() // 画出蛇和食物
{
  for (int i = 0; i < SNAKE_LEN; i++)
  {
    tft.drawRect(SNAKE[i].x - 5, SNAKE[i].y - 5, 10, 10, TFT_BLUE);
  }
  tft.drawCircle(EGG.x, EGG.y, 5, TFT_RED);
}

void eat_self()
{
  if (SNAKE_LEN == 1)
    return;
  for (int i = 1; i < SNAKE_LEN; i++)
    if (fabs(SNAKE[i].x - SNAKE[0].x) <= 5 && fabs(SNAKE[i].y - SNAKE[0].y) <= 5)
    {
      delay(1000);
      tft.setTextColor(TFT_RED, TFT_BLACK);
      tft.drawString("GAME OVER!", 200, 150, 4);
      delay(3000);

      setup();
      break;
    }
}
```

代码就这么点，没几行，接下来我们来接一下按键电路，这部分是参考了 arduino 的官方文档
[How to Wire and Program a Button](https://docs.arduino.cc/built-in-examples/digital/Button)

接线方式如下，主要原理就是通过 GND 接线，使四个方向键对应的 GPIO 口默认值为低电平。当按键
按下时，GPIO 口会被拉升成高电平，从而使程序识别到该按键被按下。

接线示意图如下（简单起见，省略了前面的显示屏接线部分）：

{{<figure src="/images/ee-basics-2-esp32-display/esp32-wiring-4-buttons.webp" width="60%" title="使用 wokwi.com 制作的示意图">}}

现在运行程序，效果如下（手上只有两个按键，所以是双键模式请见谅...）：

{{< bilibili id=BV1jT411e7HJ >}}

<!--
因为买的摇秆有问题，没焊好，各种锡把引脚连在了一起，暂时放弃此想法。

## 四、换成用摇杆控制贪吃蛇吧

用按键控制总还是差了点意思，换成用摇杆控制看看是不是更爽一点。

之前在淘宝上买的一堆元件中有一个 HW-504 摇秆，查了下找到这篇文章 [arduino-joystick](https://arduinogetstarted.com/tutorials/arduino-joystick) 详细说明了怎么在 Arduino 中用它，在 ESP32-Arduino 上使用方法也完全类似。

根据其说明，HW-504 这类摇秆的五个引脚功能分别如下：

- GDN: 接地
- VCC/5V: 接 5V 电源
- VRx 与 VRy: 分别输出 X 轴与 Y 轴的偏移量，是模拟信号
- SW: 对应摇秆内部的按键，按下摇秆会使 SW 输出高电平

我们暂时用不到摇秆的按键，所以只需要接上另外四根引脚就行，而 VRx 与 VRy 因为输出的是模拟量，需要用到 ESP32 的 ADC 功能（Analog to Digital Converter 模数转换器）。

根据 ESP32 官方文档 [Analog to Digital Converter (ADC) - ESP32  Peripherals API](https://docs.espressif.com/projects/esp-idf/en/v4.4.4/esp32/api-reference/peripherals/adc.html) 描述，ESP32 包含两个模数转换器 ADC1 与 ADC2，其中 ADC2 在启用 Wi-Fi 时会被 WiFi 占用导致无法使用，所以我们写程序通常仅使用 ADC1。

然后根据前面的文章内容修改 C 代码，用摇秆控制逻辑取代掉按键相关的内容，改好后的代码内容如下：

```c

``` -->
