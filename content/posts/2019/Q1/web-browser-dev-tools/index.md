---
title: "Chrome 与 Firefox-Dev 的 DevTools"
date: 2019-02-11T16:53:26+08:00
draft: false

featuredImage: "featured-image.webp"
resources:
  - name: featured-image
    src: "featured-image.webp"
authors: ["ryan4yin"]

tags: ["Chrome", "Firefox", "DevTools", "Browser"]
categories: ["tech"]

lightgallary: true
---

不管是做爬虫还是写 Web App，Chrome 和 Firefox 的 DevTools 都是超常用的，但是经常发现别人的
截图有什么字段我找不到，别人的什么功能我的 Chrome 没有，仔细一搜索才知道，原来是我不会
用。。

---

`Ctrl + Shift + I`：打开 DevTools `Ctrl + Shift + J`：打开控制台

### 搜索

1. `Ctrl + F`：在当前位置搜索关键字

   - 在网页界面用这个快捷键，就是页内搜索
   - 在 Network 的 Response 页面，就是在 Response 中搜索

1. `Ctrl + Shift + F`：全文搜索，在当前 Web App 的所有文件中搜索。
   - **爬虫必备**！！！要寻找一些特殊字符串的来源，用它搜索屡试不爽。

### Command

在 DevTools 里按快捷键 `Ctrl + Shift + P` 就能打开 Command 输入框，它和 vscode/sublime 的
Command 一样，用好了特别方便。

### Network

#### 1. 属性列

Chrome 可以右键属性列名来增减属性列，Firefox-Dev 也是一样：

{{< figure src="/images/web-browser-dev-tools/968138-20190211093455289-773908727.webp" >}}

{{< figure src="/images/web-browser-dev-tools/968138-20190211150559673-23181676.webp" >}}

#### 2. copy

在 Chrome 中右键某个请求，选中 copy，会给出几个 options：

{{< figure src="/images/web-browser-dev-tools/968138-20190211134155594-369771298.webp" >}}

而 Firefox-Dev 的更强一点，可以复制消息头（请求头和响应头）：

{{< figure src="/images/web-browser-dev-tools/968138-20190211134845686-1048423446.webp" >}}

#### 3. response 的 pretty print

Chrome 的 Response 页面左下角，有`{}`按钮，可以 beautify 响应。

{{< figure src="/images/web-browser-dev-tools/968138-20190211145915794-1971618603.webp" >}}

而 Firefox-Dev 只在 Debugger 页面提供该按钮，Response 中不支持。

Firefox 响应的 preview 和 payload 是放在 Response 页面下。而 Chrome 是分成了两个标签页

{{< figure src="/images/web-browser-dev-tools/968138-20190211150146579-1141462696.webp" >}}

{{< figure src="/images/web-browser-dev-tools/968138-20190211150217505-933154713.webp" >}}

#### 4. 导出 HAR

右键任意一个请求，选择 `save all as HAR`，就可以导出 HAR 文件。（Chrome 有 with content，
导出的 HAR 文件会含有所有请求与响应的 body）

该文件可用于存储当前监听到的所有浏览器请求信息。在以后需要分析这些请求时，将 HAR 文件拖到
Network 页面即可恢复所有请求。

#### 5. Raw Headers（原始消息头）

Chrome 只支持查看 HTTP/1.x 的 Raw Headers，对这种请求，会给出 `view source` 选项。

{{< figure src="/images/web-browser-dev-tools/968138-20190211142152309-1418680644.webp" >}}

Chrome 不能查看 HTTP/2 的 Raw Headers。

{{< figure src="/images/web-browser-dev-tools/968138-20190211142301777-1440991898.webp" >}}

而 Firefox 则支持查看 HTTP/2 的 Raw Headers。（是恢复后的，HTTP/2 的原始消息头是二进制压缩
形式）

{{< figure src="/images/web-browser-dev-tools/968138-20190211142424361-986461531.webp" >}}

它还提供 Edit and Resend 请求的功能，这点要给个赞～

{{< figure src="/images/web-browser-dev-tools/968138-20190211172845339-1004306694.webp" >}}

#### 6. 审查 WebSocket（Chrome only）

在 NetWork 中点击对应的 WebSocket 请求，在右侧选择 Frames 标签，就可以看到所有的消息了

{{< figure src="/images/web-browser-dev-tools/968138-20190211161734224-864236086.webp" >}}

#### 7. 跨页面加载时，保留网络请求记录

当页面重载或者页面跳转时，默认情况下，Network面板下的网络请求记录表也是刷新的。如果想保留
之前页面的网络请求数据，可以勾选Preserve log.

{{< figure src="/images/web-browser-dev-tools/968138-20190211191616024-1591891666.webp" >}}

常用的一个应用场景：登录/注册时会调用登录/注册API，开发者想查看这个接口返回的情况，但是登
录/注册成功后一般会跳转到新的页面，导致了Network面板的请求记录被刷新从而看不到登录/注册接
口返回的情况。此时勾选上Preserve log，无论跳转到那个页面，都能在Network网络请求记录表中查
看到之前接口返回的情况。

### JavaScript 控制台

1. 可以通过 `$x(<xpath>, <DOM-element>)`，用 xpath 查询 DOM 元素。

{{< figure src="/images/web-browser-dev-tools/968138-20190211151856683-1227556897.webp" >}}

1. 通过控制台左上方的选单，可以切换 JS 的环境，它默认是当前页面（top）。

### Elements 页面（Firefox-Dev 是 Inspector 页面）

#### 1. DOM 元素断点（Chrome only）

在 `Elements` 页面，右键一个元素，有一个 `Break on` 选项，可以控制在特定事件发生时
Break. - subtree modification: 子节点被修改 - attribute modification：当前节点的属性被修
改。（inline style 被修改也会触发此事件）- node removal：节点被移除

{{< figure src="/images/web-browser-dev-tools/968138-20190211152916189-42263251.webp" >}}

#### 2. 检索元素上注册的事件（Chrome only）

在 Elements 页面选中一个元素（或者直接右键检查该元素），然后在右侧窗口，选择 Event
Listeners 标签，就可以看到该元素上注册的所有事件。

{{< figure src="/images/web-browser-dev-tools/968138-20190211154036983-2040723318.webp" >}}

#### 3. 颜色选择器

选中任一元素，在右侧选择 Styles 选单，会显示当前元素的 css 属性。

其中所有的颜色小方块都是可以点击的，点击颜色方块后

{{< figure src="/images/web-browser-dev-tools/968138-20190211160511912-2063790850.webp" >}}

1. 可以将颜色属性转换成多个格式（Chrome only）
   - 默认格式：`#207981`
   - RGB格式：`rgb(32, 121, 129)`
   - HSL格式：`hsl(185, 60%, 32%)`
1. 提供 color picker，可用于在网页任意位置取色。（Firefox-Dev 也有）
1. 提供复制按键，直接将该颜色当前格式的表达复制到剪切板

### 元素审查

`Ctrl + Shift + C` 或者点击 DevTools 最左上角的小箭头按钮，就能进入元素审查模式。

该模式下会自动审查鼠标所指的元素，Elements 页面也会自动定位到该元素。

### Sources 页面（Firefox-Dev 是 Debuuger 页面）

Sources 右侧的 Debugger 支持各种断点调试。

1. 条件断点 Sources 中，在任意 JS 代码的行号上单击鼠标左键，就能在该行设置一个普通断点（在
   Response 中可不行）。在行号上右键，能直接设置条件断点。
   {{< figure src="/images/web-browser-dev-tools/968138-20190211154841386-1840257581.webp" >}}
1. XHR 断点：在右侧 Debugger 中，可以添加 XHR 断点。
   - 如果条件留空，一旦有 XHR 发起，就会无条件进入调试。
   - 条件是 「Break When URL Contaions <your string>」
1. Watch Expressions：表达式审查
   - 双击选中 JS 代码中的任意变量，然后右键它，可以将该变量添加到 Watch 中，这样就可以随时
     观察它的值。
   - 也可以在右侧 Watch 中手动输入 JS 表达式。
1. DOM 元素断点（Chrome only）：在 Elements 部分讲过了。

Chrome 的断点功能比 Firefox-Dev 的更丰富。

### Screenshot

#### 1. For Chrome

方法一：在 DevTools 界面，按快捷键 `Ctrl + Shift + P` 打开 Command 窗口，然后输入
`screenshot`，在下拉栏里选择你需要的截图命令就行。

{{< figure src="/images/web-browser-dev-tools/968138-20190212163124375-995667384.webp" >}}

方法二：先进 dev tools，点击 左上角的设备图标（toggle device toolbar），然后页面顶部就会出
现一个导航栏，在这里好选择设备或者自定义图像尺寸，然后点击该导航栏右侧（不是 dev tools 右
侧）的 options 图标，会有两个选项：「截图（capture screenshot）」和「截网页全图（capture
full size screenshot）」，如下：

{{< figure src="/images/web-browser-dev-tools/968138-20190211102530072-2093584274.webp" >}}

#### 2. For Firefox

1. 只截显示出来的部分：和 Chrome 一样点击设备图标，然后在页面上面的 toolbar 就有截图按钮
2. {{< figure src="/images/web-browser-dev-tools/968138-20190211163703764-1641229843.webp" >}}
3. 截网页全图：在 DevTools 右边的 options 中进入 Settings，勾选
   `take a screenshot of the entire page`，DevTools 右上角就会出现截图按钮了。

{{< figure src="/images/web-browser-dev-tools/968138-20190211163941562-1320561581.webp" >}}

### 其他

#### 1. Fake Geolocation（Chrome only）

在 Chrome 中进入 DevTools，点击右上角的 options 按钮，选择 More tools -> Sensors，在
Geolocation 处选择 Custom location，就可以修改地理位置了。

{{< figure src="/images/web-browser-dev-tools/968138-20190211161131091-420638637.webp" >}}

#### 2. 自定义请求头

#### For Chrome

和 上一小节一样，先进 More tools，选择 Network conditions，取消勾选 Select atuomatically，
就可以修改请求头了。

{{< figure src="/images/web-browser-dev-tools/968138-20190211170346973-560763838.webp" >}}

上面的演示中，使用 `python-requests/2.21.0` 做 user agent，知乎返回 404.

#### For Firefox

打开设备模拟，在 toolbar 的右上角勾选 `show user agent`，然后就可以在 toolbar 修改 user
agent 了：

{{< figure src="/images/web-browser-dev-tools/968138-20190211170804371-405922156.webp" >}}

### 3. Request Blocking（Chrome only）

在 Network 的任意请求上右键，菜单中就有 Block request URL（阻塞该 URL）和 Block request
domain（阻塞请求所在的整个域）

{{< figure src="/images/web-browser-dev-tools/968138-20190211171736248-156227886.webp" >}}

然后就可以在 More tools -> Request blocking 中看到你设置的阻塞条件。

{{< figure src="/images/web-browser-dev-tools/968138-20190211172032733-566193435.webp" >}}

### 参考

- [你不知道的 Chrome 调试技巧](https://juejin.im/book/5c526902e51d4543805ef35e/section/5c526998e51d4506953e5574)
- [Chrome Dev Tools 中文手册](https://legacy.gitbook.com/book/leeon/devtools/details)
- [Firefox Quantum：开发者版本](https://www.mozilla.org/zh-CN/firefox/developer/)
- [How to Capture Screenshots in Google Chrome without using Extensions](https://www.labnol.org/internet/web-page-screenshots-in-google-chrome/19851/)
- [Chrome DevTools - Network](https://segmentfault.com/a/1190000008407729)
