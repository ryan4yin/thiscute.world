---
title: "曾经的我"
date: 2021-02-01T14:14:35+08:00
draft: false

toc:
  enable: false
---

记录下我的学习轨迹。（结果写着写着有点像是技术笔记跟日记的混合了 hhhh）

这份记录并不是为了让谁记得我，而是为了让我自己记住我自己，去理解过去的自己，从而更好地「活在当下」。

### 2022-08-25

- 有个 HTTP 请求失败后 fallback 到备份服务器的需求，想写个 lua 插件来支持它，在 Github 上咨询 APISIX，聊了两天官方一直建议我看看这个 nginx_next_retry，之前一直感觉不太合适，APISIX 的文档也语焉不详，但是今天研究了一波 Nginx/OpenResty 的官方文档，好像又有戏 hhhh
  - https://github.com/apache/apisix/discussions/7773
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

- 学习[分布式系统的一致性问题与共识算法](https://github.com/ryan4yin/knowledge/blob/master/blockchain/%E4%B8%80%E8%87%B4%E6%80%A7%E9%97%AE%E9%A2%98%E4%B8%8E%E5%85%B1%E8%AF%86%E7%AE%97%E6%B3%95.md) 并记录笔记
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
- 学习[分布式系统的一致性问题与共识算法](https://github.com/ryan4yin/knowledge/blob/master/blockchain/%E4%B8%80%E8%87%B4%E6%80%A7%E9%97%AE%E9%A2%98%E4%B8%8E%E5%85%B1%E8%AF%86%E7%AE%97%E6%B3%95.md) 并记录笔记
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
  - 确认问题来自 HPA behavior 的 Bug
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
