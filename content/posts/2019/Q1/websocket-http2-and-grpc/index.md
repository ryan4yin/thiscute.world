---
title: "WebSocket、HTTP/2 与 gRPC"
date: 2019-02-11T18:26:36+08:00
draft: false

featuredImage: "protocols-banner.webp"
resources:
  - name: featured-image
    src: "protocols-banner.webp"
authors: ["ryan4yin"]

tags: ["WebSocket", "gRPC", "HTTP/2"]
categories: ["tech"]
---

## 一、WebSocket

WebSocket 是一个双向通信协议，它在握手阶段采用 HTTP/1.1 协议（暂时不支持 HTTP/2）。

<!--more-->

握手过程如下：

1. 首先客户端向服务端发起一个特殊的 HTTP 请求，其消息头如下：

```headers
GET /chat HTTP/1.1  // 请求行
Host: server.example.com
Upgrade: websocket  // required
Connection: Upgrade // required
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ== // required，一个 16bits 编码得到的 base64 串
Origin: http://example.com  // 用于防止未认证的跨域脚本使用浏览器 websocket api 与服务端进行通信
Sec-WebSocket-Protocol: chat, superchat  // optional, 子协议协商字段
Sec-WebSocket-Version: 13
```

2. 如果服务端支持该版本的 WebSocket，会返回 101 响应，响应标头如下：

```headers
HTTP/1.1 101 Switching Protocols  // 状态行
Upgrade: websocket   // required
Connection: Upgrade  // required
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo= // required，加密后的 Sec-WebSocket-Key
Sec-WebSocket-Protocol: chat // 表明选择的子协议
```

握手完成后，接下来的 TCP 数据包就都是 WebSocket 协议的帧了。

可以看到，这里的握手不是 TCP 的握手，而是在 TCP 连接内部，从 HTTP/1.1 upgrade 到 WebSocket
的握手。

WebSocket 提供两种协议：不加密的 `ws://` 和 加密的 `wss://`. 因为是用 HTTP 握手，它和 HTTP
使用同样的端口：ws 是 80（HTTP），wss 是 443（HTTPS）

在 Python 编程中，可使用 [websockets](https://github.com/aaugustin/websockets) 实现的异步
WebSocket 客户端与服务端。此外 aiohttp 也提供了 WebSocket 支持。

**Note**：如果你搜索 Flask 的 WebSocket 插件，得到的第一个结果很可能是
[Flask-SocketIO](https://github.com/miguelgrinberg/python-socketio)。但是
**Flask-ScoektIO** 使用的是它独有的 SocketIO 协议，并不是标准的 WebSocket。只是它刚好提供
与 WebSocket 相同的功能而已。

SocketIO 的优势在于只要 Web 端使用了 SocketIO.js，就能支持该协议。而纯 WS 协议，只有较新的
浏览器才支持。对于客户端非 Web 的情况，更好的选择可能是使用 Flask-Sockets。

### JS API

```javascript
// WebSocket API
var socket = new WebSocket("ws://websocket.example.com")

// Show a connected message when the WebSocket is opened.
socket.onopen = function (event) {
  console.log("WebSocket is connected.")
}

// Handle messages sent by the server.
socket.onmessage = function (event) {
  var message = event.data
  console.log(message)
}

// Handle any error that occurs.
socket.onerror = function (error) {
  console.log("WebSocket Error: " + error)
}
```

## 二、HTTP/2

HTTP/2 于 2015 年标准化，主要目的是优化性能。其特性如下：

1. 二进制协议：HTTP/2 的消息头使用二进制格式，而非文本格式。并且使用专门设计的 HPack 算法
   压缩。
1. 多路复用（Multiplexing）：就是说 HTTP/2 可以重复使用同一个 TCP 连接，并且连接是多路的，
   多个请求或响应可以同时传输。
   - 对比之下，HTTP/1.1 的长连接也能复用 TCP 连接，但是只能串行，不能「多路」。
1. 服务器推送：服务端能够直接把资源推送给客户端，当客户端需要这些文件的时候，它已经在客户
   端了。（该推送对 Web App 是隐藏的，由浏览器处理）
1. HTTP/2 允许取消某个正在传输的数据流（通过发送 RST_STREAM 帧），而不关闭 TCP 连接。
   - 这正是二进制协议的好处之一，可以定义多种功能的数据帧。

它允许服务端将资源推送到客户端缓存，我们访问淘宝等网站时，经常会发现很多请求的请求头部分会
提示「provisional headers are shown」，这通常就是直接从缓存加载了资源，因此请求根本没有被
发送。观察 Chrome Network 的 Size 列，这种请求的该字段一般都是 `from disk cache` 或者
`from memory cache`.

Chrome 可以通过如下方式查看请求使用的协议：
{{< figure src="/images/websocket-http2-and-grpc/chrome-protocol.webp" >}}

> 2019-02-10: 使用 Chrome 查看，目前主流网站基本都已经部分使用了 HTTP/2，知
> 乎、bilibili、GIthub 使用了 `wss` 协议，也有很多网站使用了 SSE（格式如
> `data:image/png;base64,<base64 string>`）而且很多网站都有使用 HTTP/2 + QUIC，该协议的新
> 名称是 HTTP/3，它是基于 UDP 的 HTTP 协议。

### SSE

服务端推送事件，是通过 HTTP 长连接进行信息推送的一个功能。它首先由浏览器向服务端建立一个
HTTP 长连接，然后服务端不断地通过这个长连接将消息推送给浏览器。JS API 如下：

```javascript
// create SSE connection
var source = new EventSource("/dates")

// 连接建立时，这些 API 和 WebSocket 的很相似
source.onopen = function (event) {
  // handle open event
}

// 收到消息时（它只捕获未命名 event）
source.onmessage = function (event) {
  var data = event.data // 发送过来的实际数据（string）
  var origin = event.origin // 服务器端URL的域名部分，即协议、域名和端口。
  var lastEventId = event.lastEventId // 数据的编号，由服务器端发送。如果没有编号，这个属性为空。
  // handle message
}

source.onerror = function (event) {
  // handle error event
}
```

### 具体的实现

在收到客户端的 SSE 请求（HTTP 协议）时，服务端返回的响应首部如下：

```headers
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

而 body 部分，SSE 定义了四种信息：

1. `data`：数据栏
2. `event`：自定义数据类型
3. `id` ：数据 id
4. `retry`：最大间隔时间，超时则重新连接

body 举例说明：

```text
: 这种格式的消息是注释，会被忽略\n\n
: 通常服务器每隔一段时间就会发送一个注释，防止超时 retry\n\n

: 下面这个是一个单行数据\n\n
data: some text\n\n

: 下面这个是多行数据，在客户端会重组成一个 data\n\n
data: {\n
data: "foo": "bar",\n
data: "baz", 555\n
data: }\n\n

: 这是一个命名 event，只会被事件名与之相同的 listener 捕获\n\n
event: foo\n
data: a foo event\n\n

: 未命名事件，会被 onmessage 捕获\n\n
data: an unnamed event\n\n

event: bar\n
data: a bar event\n\n

: 这个 id 对应 event.lastEventId\n\n
id: msg1\n
data: message\n\n
```

### WebSocket、HTTP/2 与 SSE 的比较

1. 加密与否：

   - WebSocket 支持明文通信 `ws://` 和加密 `wss://`，
   - 而 HTTP/2 协议虽然没有规定必须加密，但
     是[主流浏览器都只支持 HTTP/2 over TLS](https://en.wikipedia.org/wiki/HTTP/2#Encryption).
   - SSE 是使用的 HTTP 协议通信，支持 http/https

1. 消息推送：
   - WebSocket是全双工通道，可以双向通信。而且消息是直接推送给 Web App.
   - SSE 只能**单向串行地**从服务端将数据推送给 Web App.
   - HTTP/2 虽然也支持 Server Push，但是服务器只能主动将资源推送到客户端缓存！并不允许将数
     据推送到客户端里跑的 Web App 本身。服务器推送只能由浏览器处理，不会在应用程序代码中弹
     出服务器数据，这意味着应用程序没有 API 来获取这些事件的通知。
     - 为了接近实时地将数据推送给 Web App， HTTP/2 可以结合 SSE（Server-Sent Event）使用。

WebSocket 在需要接近实时双向通信的领域，很有用武之地。而 HTTP/2 + SSE 适合用于展示实时数
据。

另外在客户端非浏览器的情况下，使用不加密的 HTTP/2 也是可能的。

### requests 查看 HTTP 协议版本号

可以通过 `resp.raw.version` 得到响应的 HTTP 版本号：

```shell
>>> import requests
>>> resp = requests.get("https://zhihu.com")
>>> resp.raw.version
11
```

但是 requests 默认使用 HTTP/1.1，并且不支持 HTTP/2.（不过这也不是什么大问题，HTTP/2 只是做
了性能优化，用 HTTP/1.1 也就是慢一点而已。）

## 三、gRPC 协议

gRPC 是一个远程过程调用框架，默认使用 protobuf3 进行数据的高效序列化与 service 定义，使用
HTTP/2 进行数据传输。这里讨论的是
[gRPC over HTTP/2](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) 协议。

目前 gRPC 主要被用在微服务通信中，但是因为其优越的性能，它也很契合游戏、loT 等需要高性能低
延迟的场景。

其实光从协议先进程度上讲，gRPC 基本全面超越 REST:

1. 使用二进制进行数据序列化，比 json 更节约流量、序列化与反序列化也更快。
1. protobuf3 要求 api 被完全清晰的定义好，而 REST api 只能靠程序员自觉定义。
1. gRPC 官方就支持从 api 定义生成代码，而 REST api 需要借助 openapi-codegen 等第三方工具。
1. 支持 4 种通信模式：一对一(unary)、客户端流、服务端流、双端流。更灵活

只是目前 gRPC 对 browser 的支持仍然不是很好，如果你需要通过浏览器访问 api，那 gRPC 可能不
是你的菜。如果你的产品只打算面向 App 等可控的客户端，可以考虑上 gRPC。

对同时需要为浏览器和 APP 提供服务应用而言，也可以考虑 APP 使用 gRPC 协议，而浏览器使用 API
网关提供的 HTTP 接口，在 API 网关上进行 HTTP - gRPC 协议转换。

### gRPC over HTTP/2 定义

详细的定义参见官方文档
[gRPC over HTTP/2](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md).

这里是简要说明几点：

1. gRPC 完全隐藏了 HTTP/2 本身的 method、headers、path 等语义，这些信息对用户而言完全不可
   见了。
   1. 请求统一使用 POST，响应状态统一为 200。只要响应是标准的 gRPC 格式，响应中的 HTTP 状
      态码将被完全忽略。
1. gRPC 定义了自己的 status 状态码、格式固定的 path、还有它自己的 headers。

## 参考

- [深入探索 WebSockets 和 HTTP/2](https://www.oschina.net/translate/how-does-javascript-actually-work-part-5)
- [HTTP/2 特性与抓包分析](https://www.cnblogs.com/etoah/p/5891285.html)
- [SSE：服务器发送事件,使用长链接进行通讯](http://www.cnblogs.com/goody9807/p/4257192.html)
- [Using server-sent events - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- [Can I Use HTTP/2 on Browsers](https://caniuse.com/#search=http2)
- [Python 3.x how to get http version (using requests library)](https://stackoverflow.com/questions/37012486/python-3-x-how-to-get-http-version-using-requests-library)
- [WebSocket 是什么原理？](https://www.zhihu.com/question/20215561/answer/40316953)
- [原生模块打造一个简单的 WebSocket 服务器](https://zhuanlan.zhihu.com/p/26407649)
- [Google Cloud - API design: Understanding gRPC, OpenAPI and REST and when to use them](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them)
