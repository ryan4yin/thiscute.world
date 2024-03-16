---
title: "Kubernetes 微服务最佳实践"
date: 2022-01-25T00:13:00+08:00
draft: false

resources:
  - name: "featured-image"
    src: "kubernetes-best-practices.webp"

tags: ["Kubernetes", "最佳实践", "云原生"]
categories: ["tech"]
series: ["云原生相关"]
---

> 本文由个人笔记
> [ryan4yin/knowledge](https://github.com/ryan4yin/knowledge/tree/master/kubernetes) 整理
> 而来

本文主要介绍我个人在使用 Kubernetes 的过程中，总结出的一套「Kubernetes 配置」，是我个人的
「最佳实践」。其中大部分内容都经历过线上环境的考验，但是也有少部分还只在我脑子里模拟过，请
谨慎参考。

阅读前的几个注意事项：

- 这份文档比较长，囊括了很多内容，建议当成参考手册使用，先参照目录简单读一读，有需要再细读
  相关内容。
- 这份文档需要一定的 Kubernetes 基础才能理解，而且如果没有过实践经验的话，看上去可能会比较
  枯燥。
  - 而有过实践经验的大佬，可能会跟我有不同的见解，欢迎各路大佬评论~

我会视情况不定期更新这份文档。

## 零、示例

首先，这里给出一些本文遵守的前提，这些前提只是契合我遇到的场景，可灵活变通：

- 这里只讨论无状态服务，有状态服务不在讨论范围内
- 我们不使用 Deployment 的滚动更新能力，而是为每个服务的每个版本，都创建不同的Deployment +
  HPA + PodDisruptionBudget，这是为了方便做金丝雀/灰度发布
- 我们的服务可能会使用 IngressController / Service Mesh 来进行服务的负载均衡、流量切分

下面先给出一个 Deployment + HPA + PodDisruptionBudget 的 demo，后面再拆开详细说下：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-v3
  namespace: prod # 建议按业务逻辑划分名字空间，prod 仅为示例
  labels:
    app: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    # 因为服务的每个版本都使用各自的 Deployment，服务更新时其实是用不上这里的滚动更新策略的
    # 这个配置应该只在 SRE 手动修改 Deployment 配置时才会生效（通常不应该发生这种事）
    rollingUpdate:
      maxSurge: 10% # 滚动更新时，每次最多更新 10% 的 Pods
      maxUnavailable: 0 # 滚动更新时，不允许出现不可用的 Pods，也就是说始终要维持 3 个可用副本
  selector:
    matchLabels:
      app: my-app
      version: v3
  template:
    metadata:
      labels:
        app: my-app
        version: v3
    spec:
      affinity:
        # 注意，podAffinity/podAntiAffinity 可能不是最佳方案，这部分配置待更新
        # topologySpreadConstraints 可能是更好的选择
        podAffinity:
          preferredDuringSchedulingIgnoredDuringExecution: # 非强制性条件
            - weight: 100 # weight 用于为节点评分，会优先选择评分最高的节点（只有一条规则的情况下，这个值没啥意义）
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - my-app
                    - key: version
                      operator: In
                      values:
                        - v3
                # pod 尽量使用同一种节点类型，也就是尽量保证节点的性能一致
                topologyKey: node.kubernetes.io/instance-type
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution: # 非强制性条件
            - weight: 100 # weight 用于为节点评分，会优先选择评分最高的节点（只有一条规则的情况下，这个值没啥意义）
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - my-app
                    - key: version
                      operator: In
                      values:
                        - v3
                # 将 pod 尽量打散在多个可用区
                topologyKey: topology.kubernetes.io/zone
          requiredDuringSchedulingIgnoredDuringExecution: # 强制性要求（这个建议按需添加）
            # 注意这个没有 weights，必须满足列表中的所有条件
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - my-app
                  - key: version
                    operator: In
                    values:
                      - v3
              # Pod 必须运行在不同的节点上
              topologyKey: kubernetes.io/hostname
      securityContext:
        # runAsUser: 1000  # 设定用户
        # runAsGroup: 1000  # 设定用户组
        runAsNonRoot: true # Pod 必须以非 root 用户运行
        seccompProfile: # security compute mode
          type: RuntimeDefault
      nodeSelector:
        nodegroup: common # 使用专用节点组，如果希望使用多个节点组，可改用节点亲和性
      volumes:
        - name: tmp-dir
          emptyDir: {}
      containers:
        - name: my-app-v3
          image: my-app:v3 # 建议使用私有镜像仓库，规避 docker.io 的镜像拉取限制
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - mountPath: /tmp
              name: tmp-dir
          lifecycle:
            preStop: # 在容器被 kill 之前执行
              exec:
                command:
                  - /bin/sh
                  - -c
                  - "while [ $(netstat -plunt | grep tcp | wc -l | xargs) -ne 0 ]; do
                    sleep 1; done"
          resources: # 资源请求与限制
            # 对于核心服务，建议设置 requests = limits，避免资源竞争
            requests:
              # HPA 会使用 requests 计算资源利用率
              # 建议将 requests 设为服务正常状态下的 CPU 使用率，HPA 的目前指标设为 80%
              # 所有容器的 requests 总量不建议为 2c/4G 4c/8G 等常见值，因为节点通常也是这个配置，这会导致 Pod 只能调度到更大的节点上，适当调小 requests 等扩充可用的节点类型，从而扩充节点池。
              cpu: 1000m
              memory: 1Gi
            limits:
              # limits - requests 为允许超卖的资源量，建议为 requests 的 1 到 2 倍，酌情配置。
              cpu: 1000m
              memory: 1Gi
          securityContext:
            # 将容器层设为只读，防止容器文件被篡改
            ## 如果需要写入临时文件，建议额外挂载 emptyDir 来提供可读写的数据卷
            readOnlyRootFilesystem: true
            # 禁止 Pod 做任何权限提升
            allowPrivilegeEscalation: false
            capabilities:
              # drop ALL 的权限比较严格，可按需修改
              drop:
                - ALL
          startupProbe: # 要求 kubernetes 1.18+
            httpGet:
              path: /actuator/health # 直接使用健康检查接口即可
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 20 # 最多提供给服务 5s * 20 的启动时间
            successThreshold: 1
          livenessProbe:
            httpGet:
              path: /actuator/health # spring 的通用健康检查路径
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
          # Readiness probes are very important for a RollingUpdate to work properly,
          readinessProbe:
            httpGet:
              path: /actuator/health # 简单起见可直接使用 livenessProbe 相同的接口，当然也可额外定义
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
---
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  labels:
    app: my-app
  name: my-app-v3
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-v3
  maxReplicas: 50
  minReplicas: 3
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-v3
  namespace: prod
  labels:
    app: my-app
spec:
  minAvailable: 75%
  selector:
    matchLabels:
      app: my-app
      version: v3
```

## 一、优雅停止（Gracful Shutdown）与 502/504 报错

如果 Pod 正在处理大量请求（比如 1000 QPS+）时，因为节点故障或「竞价节点」被回收等原因被重
新调度，你可能会观察到在容器被 terminate 的一段时间内出现少量 502/504。

为了搞清楚这个问题，需要先理解清楚 terminate 一个 Pod 的流程：

1. Pod 的状态被设为 `Terminating`（几乎）同时该 Pod 被从所有关联的 Service Endpoints 中移
   除
2. 如果配置了 `preStop` 参数，开始执行如下步骤
   1. 执行 `preStop` 钩子
      1. 它的执行阶段很好理解：在容器被 stop 之前执行
      2. 它可以是一个命令，或者一个对 Pod 中容器的 http 调用
      3. 如果在收到 SIGTERM 信号时，无法优雅退出，要支持优雅退出比较麻烦的话，用 `preStop`
         实现优雅退出是一个非常好的方式
      4. preStop 的定义位
         置：<https://github.com/kubernetes/api/blob/master/core/v1/types.go#L2515>
   2. `preStop` 执行完毕后，SIGTERM 信号被发送给 Pod 中的所有容器
3. 如果未配置 `preStop`，则 SIGTERM 信号将被立即发送给 Pod 中的所有容器
4. 继续等待，直到容器停止或者超时。
   1. `spec.terminationGracePeriodSeconds` 为超时时间，默认为 30s
   2. 需要注意的是，这个优雅退出的等待计时是与 `preStop` 同步开始的！
5. 如果超过了 `spec.terminationGracePeriodSeconds` 容器仍然没有停止，k8s 将会发送 SIGKILL
   信号给容器
6. 进程全部终止后，整个 Pod 完全被清理掉

**注意**：「从 Service Endpoints 中移除 Pod IP」跟后续的步骤是异步发生的，所以在未设置
`preStop` 时，可能会出现「Pod 还在 Service Endpoints 中，但是 `SIGTERM` 已经被发送给 Pod
导致容器都挂掉」的情况，我们需要考虑到这种状况的发生。

了解了上面的流程后，我们就能分析出两种错误码出现的原因：

- 502：应用程序在收到 SIGTERM 信号后直接终止了运行，导致部分还没有被处理完的请求直接中断，
  代理层返回 502 表示这种情况
- 504：Service Endpoints 移除不够及时，在 Pod 已经被终止后，仍然有个别请求被路由到了该
  Pod，得不到响应导致 504

通常的解决方案是，在 Pod 的 `preStop` 步骤加一个 15s 的等待时间。其原理是：在 Pod 处理
terminating 状态的时候，就会被从 Service Endpoints 中移除，也就不会再有新的请求过来了。在
`preStop` 等待 15s，基本就能保证所有的请求都在容器死掉之前被处理完成（一般来说，绝大部分请
求的处理时间都在 300ms 以内吧）。

一个简单的示例如下，它使 Pod 被 Terminate 时，总是在 stop 前先等待 15s，再发送 SIGTERM 信
号给容器：

```yaml
containers:
  - name: my-app
    # 添加下面这部分
    lifecycle:
      preStop:
        exec:
          command:
            - /bin/sleep
            - "15"
```

更好的解决办法，是直接等待所有 tcp 连接都关闭（需要镜像中有 netstat）：

```yaml
containers:
  - name: my-app
    # 添加下面这部分
    lifecycle:
    preStop:
      exec:
        command:
          - /bin/sh
          - -c
          - "while [ $(netstat -plunt | grep tcp | wc -l | xargs) -ne 0 ]; do sleep 1;
            done"
```

### 如果我的服务还使用了 Sidecar 代理网络请求，该怎么处理？ {#k8s-istio-pod-prestop}

以服务网格 Istio 为例，在 Envoy 代理了 Pod 流量的情况下，502/504 的问题会变得更复杂一点——
还需要考虑 Sidecar 与主容器的关闭顺序：

- 如果在 Envoy 已关闭后，有新的请求再进来，将会导致 504（没人响应这个请求了）
  - 所以 Envoy 最好在 Terminating 至少 3s 后才能关，确保 Istio 网格配置已完全更新
- 如果在 Envoy 还没停止时，主容器先关闭，然后又有新的请求再进来，Envoy 将因为无法连接到
  upstream 导致 503
  - 所以主容器也最好在 Terminating 至少 3s 后，才能关闭。
- 如果主容器处理还未处理完遗留请求时，Envoy 或者主容器的其中一个停止了，会因为 tcp 连接直
  接断开连接导致 502
  - 因此 Envoy 必须在主容器处理完遗留请求后（即没有 tcp 连接时），才能关闭

所以总结下：Envoy 及主容器的 `preStop` 都至少得设成 3s，并且在「没有 tcp 连接」时，才能关
闭，避免出现 502/503/504.

主容器的修改方法在前文中已经写过了，下面介绍下 Envoy 的修改方法。

和主容器一样，Envoy 也能直接加 `preStop`，修改 `istio-sidecar-injector` 这个 `configmap`，
在 sidecar 里添加 preStop sleep 命令:

```yaml
containers:
  - name: istio-proxy
    # 添加下面这部分
    lifecycle:
    preStop:
      exec:
        command:
          - /bin/sh
          - -c
          - "while [ $(netstat -plunt | grep tcp | grep -v envoy | wc -l | xargs) -ne 0 ];
            do sleep 1; done"
```

### 参考

- [Kubernetes best practices: terminating with grace](https://cloud.google.com/blog/products/containers-kubernetes/kubernetes-best-practices-terminating-with-grace)
- [Graceful shutdown in Kubernetes is not always trivial](https://medium.com/flant-com/kubernetes-graceful-shutdown-nginx-php-fpm-d5ab266963c2)

## 二、服务的伸缩配置 - HPA {#k8s-hpa}

Kubernetes 官方主要支持基于 Pod CPU 的伸缩，这是应用最为广泛的伸缩指标，需要部署
[metrics-server](https://github.com/kubernetes-sigs/metrics-server) 才可使用。

先回顾下前面给出的，基于 Pod CPU 使用率进行伸缩的示例：

```yaml
apiVersion: autoscaling/v2beta2 # k8s 1.23+ 此 API 已经 GA
kind: HorizontalPodAutoscaler
metadata:
  labels:
    app: my-app
  name: my-app-v3
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-v3
  maxReplicas: 50
  minReplicas: 3
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### 1. 当前指标值的计算方式

提前总结：每个 **Pod 的指标是其中所有容器指标之和**，如果计算百分比，就再除以 Pod 的
requests.

HPA 默认使用 Pod 的当前指标进行计算，以 CPU 使用率为例，其计算公式为：

```
「Pod 的 CPU 使用率」= 100% * 「所有 Container 的 CPU 用量之和」/「所有 Container 的 CPU requests 之和」
```

注意分母是总的 requests 量，而不是 limits.

#### 1.1 存在的问题与解决方法

在 Pod 只有一个容器时这没啥问题，但是当 Pod 注入了 envoy 等 sidecar 时，这就会有问题了。

因为 Istio 的 Sidecar requests 默认为 `100m` 也就是 0.1 核。在未 tuning 的情况下，服务负载
一高，sidecar 的实际用量很容易就能涨到 0.2-0.4 核。把这两个值代入前面的公式，会发现 **对于
QPS 较高的服务，添加 Sidecar 后，「Pod 的 CPU 利用率」可能会高于「应用容器的 CPU 利用
率」**，造成不必要的扩容。主容器的 requests 与 limits 差距越小，这样的扩容造成的资源浪费就
越大。

而且还有个问题是，不同应用的 Pod，数据流特征、应用负载特征等都有区别（请求/响应的数据量、
处理时长等），这会造成 sidecar 与主容器的 cpu 利用率不一，加大了优化 HPA 机制的困难度。

解决方法：

- 方法一：HPA 改用绝对指标进行扩缩容，即 Pod 的总 CPU 用量。这使 HPA 不受任何容器 requests
  设置的影响。
  - 但是因为不同服务负载的区别，需要根据实际负载为每个服务调整 HPA 的期望指标。
- 方法二：HPA 仍然使用 Pod 利用率进行扩缩容，但是针对每个服务的 CPU 使用情况，为每个服务的
  sidecar 设置不同的 requests/limits，降低 sidecar 对扩缩容的影响。
- 方法三：使用 KEDA 等第三方组件，获取到应用容器的 CPU 利用率（排除掉 Sidecar），使用它进
  行扩缩容
- 方法四：使用 k8s 1.20 提供的 alpha 特
  性：[Container Resource Metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#container-resource-metrics).
  - 这种方式可以将 Pod 的不同容器的指标区分看待，算是最佳的处理方法了，但是该特性仍未进入
    beta 阶段，慎用。

### 2. HPA 的扩缩容算法

HPA 什么时候会扩容，这一点是很好理解的。但是 HPA 的缩容策略，会有些迷惑，下面简单分析下。

1. HPA 的「目标指标」可以使用两种形式：绝对度量指标和资源利用率。
   - 绝对度量指标：比如 CPU，就是指 CPU 的使用量
   - 资源利用率（资源使用量/资源请求 \* 100%）：在 Pod 设置了资源请求时，可以使用资源利用
     率进行 Pod 伸缩
2. HPA 的「当前指标」是一段时间内所有 Pods 的平均值，不是峰值。

HPA 的扩缩容算法为：

```
期望副本数 = ceil[当前副本数 * ( 当前指标 / 目标指标 )]
```

从上面的参数可以看到：

1. 只要「当前指标」超过了目标指标，就一定会发生扩容。
2. `当前指标 / 目标指标`要小到一定的程度，才会触发缩容。
   1. 比如双副本的情况下，上述比值要小于等于 1/2，才会缩容到单副本。
   2. 三副本的情况下，上述比值的临界点是 2/3。
   3. 五副本时临界值是 4/5，100副本时临界值是 99/100，依此类推。
   4. 如果 `当前指标 / 目标指标` 从 1 降到 0.5，副本的数量将会减半。（虽然说副本数越多，发
      生这么大变化的可能性就越小。）
3. `当前副本数 / 目标指标`的值越大，「当前指标」的波动对「期望副本数」的影响就越大。

为了防止扩缩容过于敏感，HPA 有几个相关参数：

1. Hardcoded 参数
   1. HPA Loop 延时：默认 15 秒，每 15 秒钟进行一次 HPA 扫描。
   2. 缩容冷却时间：默认 5 分钟。
2. 对于 K8s 1.18+，HPA 通过 `spec.behavior` 提供了多种控制扩缩容行为的参数，后面会具体介
   绍。

### 3. HPA 的期望值设成多少合适？如何兼顾资源利用率与服务稳定性？

这个需要针对每个服务的具体情况，具体分析。

以最常用的按 CPU 值伸缩为例，

- 核心服务
  - requests/limits 值: 建议设成相等的，保
    证[服务质量等级](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/)为
    Guaranteed
    - 需要注意 CPU 跟 Memory 的 limits 限制策略是不同的，CPU 是真正地限制了上限，而 Memory
      是用超了就干掉容器（OOMKilled）
    - k8s 一直使用 cgroups v1 (`cpu_shares`/`memory.limit_in_bytes`)来限制 cpu/memory，但
      是对于 `Guaranteed` 的 Pods 而言，内存并不能完全预留，资源竞争总是有可能发生的。1.22
      有 alpha 特性改用 cgroups v2，可以关注下。
  - HPA: 一般来说，期望值设为 60% 到 70% 可能是比较合适的，最小副本数建议设为 2 - 5. （仅
    供参考）
  - PodDisruptionBudget: 建议按服务的健壮性与 HPA 期望值，来设置 PDB，后面会详细介绍，这里
    就先略过了
- 非核心服务
  - requests/limits 值: 建议 requests 设为 limits 的 0.6 - 0.9 倍（仅供参考），对应的服务
    质量等级为 Burstable
    - 也就是超卖了资源，这样做主要的考量点是，很多非核心服务负载都很低，根本跑不到 limits
      这么高，降低 requests 可以提高集群资源利用率，也不会损害服务稳定性。
  - HPA: 因为 requests 降低了，而 HPA 是以 requests 为 100% 计算使用率的，我们可以提高 HPA
    的期望值（如果使用百分比为期望值的话），比如 80% ~ 90%，最小副本数建议设为 1 - 3. （仅
    供参考）
  - PodDisruptionBudget: 非核心服务嘛，保证最少副本数为 1 就行了。

相关资料：

- [最佳实践｜Kubernetes集群利用率提升的思路和实现方式 - 腾讯云原生](https://mp.weixin.qq.com/s/NRd7G1c_SkjHSZYBLFgncA)

### 4. HPA 的常见问题

#### 4.1. Pod 扩容 - VM 预热陷阱

Java/C# 这类运行在 VM 上的语言，在启动阶段与第一次执行请求时，往往需要初始化一些资源。这导
致在容器刚启动的一段时间，它需要消**耗更多的 CPU** 去将字节码编译成机器码并缓存起来。这就
是 VM 语言的「预热」问题。

相关文档：

- [How to Warm Up the JVM](https://www.baeldung.com/java-jvm-warmup)
- [How to cold start fast a java service on k8s (EKS)](https://itnext.io/how-to-cold-start-fast-a-java-service-on-k8s-eks-3a7b4450845d)

因为上述「预热」问题在使用 HPA 扩缩容 Java/C# 等运行在 VM 上的程序时，HPA 一扩容，服务可用
率就会抖动，甚至引发雪崩。

举例说明，在有大量用户访问的时候，只要请求被转发到新建的 Java Pod 上，这个请求就会「卡
住」。如果请求速度太快，Pod 启动的瞬间「卡住」的请求就越多，这可能会导致新建 Pod 因为压力
过大而垮掉。然后 Pod 每次刚重启就被打垮，进入 CrashLoopBackoff 循环。

如果是在使用多线程做负载测试时，效果更明显：50 个线程在不间断地请求，别的 Pod 响应时间是
「毫秒级」，而新建的 Pod 的首次响应是「秒级」。几乎是一瞬间，50 个线程就会全部陷在新建的
Pod 这里。而新建的 Pod 在启动的瞬间可能特别脆弱，瞬间的 50 个并发请求就可以将它压垮。然后
Pod 一重启就被压垮，进入 CrashLoopBackoff 循环。

**解决方法**：

可以在「应用层面」解决：

1. 大 Pod 策略：JVM 预热阶段需要使用更多的 CPU，假设在 HPA 为 60% CPU 的情况下，越大的 Pod
   它的可超卖 CPU （40%）显然就更多，这就能缓解 JVM 预热问题。
   1. 实测将 Pod 的 requests/limits 从 3.7c/7.5G 扩容到 7.4c/15G，服务的扩容明显更平滑了。
2. JVM 参数调优：不完全举例如下
   1. 提前分配 G1New 内存：`-XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=60`，避
      免 JVM 启动阶段因为内存不足频繁 GC
3. 使用「AOT 预编译」技术：预热通常都是因为「JIT 即时编译」导致的问题，在需要用到时它才编
   译。而 AOT 是预先编译，在使用前完成编译，因此 AOT 能解决预热的问题。比如说 Java 的
   GraalVM.
   1. [Sprint Native](https://docs.spring.io/spring-native/docs/current/reference/htmlsingle/)
      是使用 GralalVM 实现 的，但还在 beta 阶段，而且有些兼容性问题
4. 其他资料
   1. [steinsag/warm-me-up](https://github.com/steinsag/warm-me-up)
   2. [How to Warm Up the JVM](https://www.baeldung.com/java-jvm-warmup)

也可以在「基础设施层面」解决：

1. 像 AWS ALB TargetGroup 以及其他云服务商的 ALB 服务，通常都可以设置 `slow_start` 时长，
   即对新加入的实例，使用一定时间慢慢地把流量切过去，最终达到预期的负载均衡状态。这个可以
   解决服务预热问题。
2. Envoy 也已经支持 `slow_start` 模式，支持在一个设置好的时间窗口内，把流量慢慢负载到新加
   入的实例上，达成预热效果。

#### 4.2. HPA 扩缩容过于敏感，导致 Pod 数量震荡

通常来讲，K8s 上绝大部分负载都应该选择使用 CPU 进行扩缩容。因为 CPU 通常能很好的反映服务的
负载情况

但是有些服务会存在其他影响 CPU 使用率的因素，导致使用 CPU 扩缩容变得不那么可靠，比如：

- 有些 Java 服务堆内存设得很大，GC pause 也设得比较长，因此内存 GC 会造成 CPU 间歇性飙
  升，CPU 监控会有大量的尖峰。
- 有些服务有定时任务，定时任务一运行 CPU 就涨，但是这跟服务的 QPS 是无关的
- 有些服务可能一运行 CPU 就会立即处于一个高位状态，它可能希望使用别的业务侧指标来进行扩
  容，而不是 CPU.

因为上述问题存在，使用 CPU 扩缩容，就可能会造成服务频繁的扩容然后缩容，或者无限扩容。而有
些服务（如我们的「推荐服务」），对「扩容」和「缩容」都是比较敏感的，每次扩缩都会造成服务可
用率抖动。

对这类服务而言，HPA 有这几种调整策略：

- 选择使用 **QPS** 等相对比较平滑，没有 GC 这类干扰的指标来进行扩缩容，这需要借助 KEDA 等
  社区组件。
- 对 kubernetes 1.18+，可以直接使用 HPA 的 `behavior.scaleDown` 和 `behavior.scaleUp` 两个
  参数，控制每次扩缩容的最多 pod 数量或者比例。 示例如下：

```yaml
---
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: podinfo
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  minReplicas: 3
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50 # 期望的 CPU 平均值
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0 # 默认为 0，只使用当前值进行扩缩容
      policies:
        - periodSeconds: 180 # 每 3 分钟最多扩容 5% 的 Pods
          type: Percent
          value: 5
        - periodSeconds: 60 # 每分钟最多扩容 1 个 Pod，扩的慢一点主要是为了一个个地预热，避免一次扩容太多未预热的 Pods 导致服务可用率剧烈抖动
          type: Pods
          value: 1
      selectPolicy: Min # 选择最小的策略
    # 以下的一切配置，都是为了更平滑地缩容
    scaleDown:
      stabilizationWindowSeconds: 600 # 使用过去 10 mins 的最大 cpu 值进行缩容计算，避免过快缩容
      policies:
        - type: Percent # 每 3 mins 最多缩容 `ceil[当前副本数 * 5%]` 个 pod（20 个 pod 以内，一次只缩容 1 个 pod）
          value: 5
          periodSeconds: 180
        - type: Pods # 每 1 mins 最多缩容 1 个 pod
          value: 1
          periodSeconds: 60
      selectPolicy: Min # 上面的 policies 列表，只生效其中最小的值作为缩容限制（保证平滑缩容）
```

而对于扩容不够平滑这个问题，可以考虑提供类似 AWS ALB TargetGroup `slow_start` 的功能，在扩
容时缓慢将流量切到新 Pod 上，以实现预热服务（JVM 预热以及本地缓存预热），这样就能达到比较
好的平滑扩容效果。

### 5. HPA 注意事项

注意 kubectl 1.23 以下的版本，默认使用 `hpa.v1.autoscaling` 来查询 HPA 配置，`v2beta2` 相
关的参数会被编码到 `metadata.annotations` 中。

比如 `behavior` 就会被编码到 `autoscaling.alpha.kubernetes.io/behavior` 这个 key 所对应的
值中。

因此如果使用了 v2beta2 的 HPA，一定要明确指定使用 `v2beta2` 版本的 HPA：

```shell
kubectl get hpa.v2beta2.autoscaling
```

否则不小心动到 `annotations` 中编码的某些参数，可能会产生意料之外的效果，甚至直接把控制面
搞崩... 比如这个 issue:
[Nil pointer dereference in KCM after v1 HPA patch request](https://github.com/kubernetes/kubernetes/issues/107038)

### 6. 参考

- [Pod 水平自动伸缩 - Kubernetes Docs](https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Horizontal Pod Autoscaler演练 - Kubernetes Docs](https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)

## 三、节点维护与Pod干扰预算 {#k8s-PodDistruptionBuget}

> https://kubernetes.io/zh/docs/tasks/run-application/configure-pdb/

在我们通过 `kubectl drain` 将某个节点上的容器驱逐走的时候，kubernetes 会依据 Pod 的
「PodDistruptionBuget」来进行 Pod 的驱逐。

如果不设置任何明确的 PodDistruptionBuget，Pod 将会被直接杀死，然后在别的节点重新调度，**这
可能导致服务中断**！

PDB 是一个单独的 CR 自定义资源，示例如下：

```yaml
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: podinfo-pdb
spec:
  # 如果不满足 PDB，Pod 驱逐将会失败！
  minAvailable: 1 # 最少也要维持一个 Pod 可用
  #   maxUnavailable: 1  # 最大不可用的 Pod 数，与 minAvailable 不能同时配置！二选一
  selector:
    matchLabels:
      app: podinfo
```

如果在进行节点维护时(kubectl drain)，Pod 不满足 PDB，drain 将会失败，示例：

```shell
> kubectl drain node-205 --ignore-daemonsets --delete-local-data
node/node-205 cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/calico-node-nfhj7, kube-system/kube-proxy-94dz5
evicting pod default/podinfo-7c84d8c94d-h9brq
evicting pod default/podinfo-7c84d8c94d-gw6qf
error when evicting pod "podinfo-7c84d8c94d-h9brq" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.
evicting pod default/podinfo-7c84d8c94d-h9brq
error when evicting pod "podinfo-7c84d8c94d-h9brq" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.
evicting pod default/podinfo-7c84d8c94d-h9brq
error when evicting pod "podinfo-7c84d8c94d-h9brq" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.
evicting pod default/podinfo-7c84d8c94d-h9brq
pod/podinfo-7c84d8c94d-gw6qf evicted
pod/podinfo-7c84d8c94d-h9brq evicted
node/node-205 evicted
```

上面的示例中，podinfo 一共有两个副本，都运行在 node-205 上面。我给它设置了干扰预算 PDB
`minAvailable: 1`。

然后使用 `kubectl drain` 驱逐 Pod 时，其中一个 Pod 被立即驱逐走了，而另一个 Pod 大概在 15
秒内一直驱逐失败。因为第一个 Pod 还没有在新的节点上启动完成，它不满足干扰预算 PDB
`minAvailable: 1` 这个条件。

大约 15 秒后，最先被驱逐走的 Pod 在新节点上启动完成了，另一个 Pod 满足了 PDB 所以终于也被
驱逐了。这才完成了一个节点的 drain 操作。

> ClusterAutoscaler 等集群节点伸缩组件，在缩容节点时也会考虑 PodDisruptionBudget. 如果你的
> 集群使用了 ClusterAutoscaler 等动态扩缩容节点的组件，强烈建议设置为所有服务设置
> PodDisruptionBudget.

#### 在 PDB 中使用百分比的注意事项

在使用百分比时，计算出的实例数都会被向上取整，这会造成两个现象：

- 如果使用 `minAvailable`，实例数较少的情况下，可能会导致 ALLOWED DISRUPTIONS 为 0，所有实
  例都无法被驱逐了。
- 如果使用 `maxUnavailable`，因为是向上取整，ALLOWED DISRUPTIONS 的值一定不会低于 1，至少
  有 1 个实例可以被驱逐。

因此从「便于驱逐」的角度看，如果你的服务至少有 2-3 个实例，建议在 PDB 中使用百分比配置
`maxUnavailable`，而不是 `minAvailable`. 相对的从「确保服务稳定性」的角度看，我们则应该使
用 `minAvailable`，确保至少有 1 个实例可用。

### 最佳实践 Deployment + HPA + PodDisruptionBudget

一般而言，一个服务的每个版本，都应该包含如下三个资源：

- Deployment: 管理服务自身的 Pods 嘛
- HPA: 负责 Pods 的扩缩容，通常使用 CPU 指标进行扩缩容
- PodDisruptionBudget(PDB): 建议按照 HPA 的目标值，来设置 PDB.
  - 比如 HPA CPU 目标值为 60%，就可以考虑设置 PDB `minAvailable=65%`，保证至少有 65% 的
    Pod 可用。这样理论上极限情况下 QPS 均摊到剩下 65% 的 Pods 上也不会造成雪崩（这里假设
    QPS 和 CPU 是完全的线性关系）

## 四、节点亲和性与节点组 {#k8s-affinity}

我们一个集群，通常会使用不同的标签为节点组进行分类，比如 kubernetes 自动生成的一些节点标
签：

- `kubernetes.io/os`: 通常都用 `linux`
- `kubernetes.io/arch`: `amd64`, `arm64`
- `topology.kubernetes.io/region` 和 `topology.kubernetes.io/zone`: 云服务的区域及可用区

我们使用得比较多的，是「节点亲和性」以及「Pod 反亲和性」，另外两个策略视情况使用。

### 1. 节点亲和性

如果你使用的是 aws，那 aws 有一些自定义的节点标签：

- `eks.amazonaws.com/nodegroup`: aws eks 节点组的名称，同一个节点组使用同样的 aws ec2 实例
  模板
  - 比如 arm64 节点组、amd64/x64 节点组
  - 内存比例高的节点组如 m 系实例，计算性能高的节点组如 c 系列
  - 竞价实例节点组：这个省钱啊，但是动态性很高，随时可能被回收
  - 按量付费节点组：这类实例贵，但是稳定。

假设你希望优先选择竞价实例跑你的 Pod，如果竞价实例暂时跑满了，就选择按量付费实例。那
`nodeSelector` 就满足不了你的需求了，你需要使用 `nodeAffinity`，示例如下:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xxx
  namespace: xxx
spec:
  # ...
  template:
    # ...
    spec:
      affinity:
        nodeAffinity:
          # 优先选择 spot-group-c 的节点
          preferredDuringSchedulingIgnoredDuringExecution:
            - preference:
                matchExpressions:
                  - key: eks.amazonaws.com/nodegroup
                    operator: In
                    values:
                      - spot-group-c
              weight: 80 # weight 用于为节点评分，会优先选择评分最高的节点
            - preference:
                matchExpressions:
                  # 优先选择 aws c6i 的机器
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values:
                      - "c6i.xlarge"
                      - "c6i.2xlarge"
                      - "c6i.4xlarge"
                      - "c6i.8xlarge"
              weight: 70
            - preference:
                matchExpressions:
                  # 其次选择 aws c5 的机器
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values:
                      - "c5.xlarge"
                      - "c5.2xlarge"
                      - "c5.4xlarge"
                      - "c5.9xlarge"
              weight: 60
          # 如果没 spot-group-c 可用，也可选择 ondemand-group-c 的节点跑
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: eks.amazonaws.com/nodegroup
                    operator: In
                    values:
                      - spot-group-c
                      - ondemand-group-c
      containers:
        # ...
```

### 2. Pod 反亲和性

> Pod 亲和性与反亲和性可能不是最佳的实现手段，这部分内容待更新

> 相关 Issue: <https://github.com/kubernetes/kubernetes/issues/72479>

> 相关替代方
> 案：<https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/>

通常建议为每个 Deployment 的 template 配置 Pod 反亲和性，把 Pods 打散在所有节点上：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xxx
  namespace: xxx
spec:
  # ...
  template:
    # ...
    spec:
      replicas: 3
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution: # 非强制性条件
            - weight: 100 # weight 用于为节点评分，会优先选择评分最高的节点
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - xxx
                    - key: version
                      operator: In
                      values:
                        - v12
                # 将 pod 尽量打散在多个可用区
                topologyKey: topology.kubernetes.io/zone
          requiredDuringSchedulingIgnoredDuringExecution: # 强制性要求
            # 注意这个没有 weights，必须满足列表中的所有条件
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - xxx
                  - key: version
                    operator: In
                    values:
                      - v12
              # Pod 必须运行在不同的节点上
              topologyKey: kubernetes.io/hostname
```

## 五、Pod 的就绪探针、存活探针与启动探针 {#k8s-container-probe}

Pod 提供如下三种探针，均支持使用 Command、HTTP API、TCP Socket 这三种手段来进行服务可用性
探测。

- `startupProbe` 启动探针（Kubernetes v1.18 [beta]）: 此探针通过后，「就绪探针」与「存活探
  针」才会进行存活性与就绪检查
  - 用于对慢启动容器进行存活性检测，避免它们在启动运行之前就被杀掉
    - startupProbe 显然比 livenessProbe 的 initialDelaySeconds 参数更灵活。
    - 同时它也能延迟 readinessProbe 的生效时间，这主要是为了避免无意义的探测。容器都还没
      startUp，显然是不可能就绪的。
  - 程序将最多有 `failureThreshold * periodSeconds` 的时间用于启动，比如设置
    `failureThreshold=20`、`periodSeconds=5`，程序启动时间最长就为 100s，如果超过 100s 仍
    然未通过「启动探测」，容器会被杀死。
- `readinessProbe` 就绪探针:
  - 就绪探针失败次数超过 `failureThreshold` 限制（默认三次），服务将被暂时从 Service 的
    Endpoints 中踢出，直到服务再次满足 `successThreshold`.
- `livenessProbe` 存活探针: 检测服务是否存活，它可以捕捉到死锁等情况，及时杀死这种容器。
  - 存活探针失败可能的原因：
    - 服务发生死锁，对所有请求均无响应
    - 服务线程全部卡在对外部 redis/mysql 等外部依赖的等待中，导致请求无响应
  - 存活探针失败次数超过 `failureThreshold` 限制（默认三次），容器将被杀死，随后根据重启策
    略执行重启。
    - `kubectl describe pod` 会显示重启原因为
      `State.Last State.Reason = Error, Exit Code=137`，同时 Events 中会有
      `Liveness probe failed: ...` 这样的描述。

上述三类探测器的参数都是通用的，五个时间相关的参数列举如下：

```yaml
# 下面的值就是 k8s 的默认值
initialDelaySeconds: 0 # 默认没有 delay 时间
periodSeconds: 10
timeoutSeconds: 1
failureThreshold: 3
successThreshold: 1
```

示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-v3
spec:
  # ...
  template:
    #  ...
    spec:
      containers:
        - name: my-app-v3
          image: xxx.com/app/my-app:v3
          imagePullPolicy: IfNotPresent
          # ... 省略若干配置
          startupProbe:
            httpGet:
              path: /actuator/health # 直接使用健康检查接口即可
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 20 # 最多提供给服务 5s * 20 的启动时间
            successThreshold: 1
          livenessProbe:
            httpGet:
              path: /actuator/health # spring 的通用健康检查路径
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
          # Readiness probes are very important for a RollingUpdate to work properly,
          readinessProbe:
            httpGet:
              path: /actuator/health # 简单起见可直接使用 livenessProbe 相同的接口，当然也可额外定义
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
```

在 Kubernetes 1.18 之前，通用的手段是为「就绪探针」添加较长的 `initialDelaySeconds` 来实现
类似「启动探针」的功能动，避免容器因为启动太慢，存活探针失败导致容器被重启。示例如下：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-v3
spec:
  # ...
  template:
    #  ...
    spec:
      containers:
        - name: my-app-v3
          image: xxx.com/app/my-app:v3
          imagePullPolicy: IfNotPresent
          # ... 省略若干配置
          livenessProbe:
            httpGet:
              path: /actuator/health # spring 的通用健康检查路径
              port: 8080
            initialDelaySeconds: 120 # 前两分钟，都假设服务健康，避免 livenessProbe 失败导致服务重启
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
          # 容器一启动，Readiness probes 就会不断进行检测
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 3 # readiness probe 不需要设太长时间，使 Pod 尽快加入到 Endpoints.
            periodSeconds: 5
            timeoutSeconds: 1
            failureThreshold: 5
            successThreshold: 1
```

## 六、Pod 安全 {#k8s-pod-security}

这里只介绍 Pod 中安全相关的参数，其他诸如集群全局的安全策略，不在这里讨论。

### 1. Pod SecurityContext

> https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

通过设置 Pod 的 SecurityContext，可以为每个 Pod 设置特定的安全策略。

SecurityContext 有两种类型：

1. `spec.securityContext`: 这是一个
   [PodSecurityContext](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#podsecuritycontext-v1-core)
   对象
   - 顾名思义，它对 Pod 中的所有 containers 都有效。
2. `spec.containers[*].securityContext`: 这是一个
   [SecurityContext](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#securitycontext-v1-core)
   对象
   - container 私有的 SecurityContext

这两个 SecurityContext 的参数只有部分重叠，重叠的部分 `spec.containers[*].securityContext`
优先级更高。

我们比较常遇到的一些**提升权限**的安全策略：

1. 特权容器：`spec.containers[*].securityContext.privileged`
2. 添加（Capabilities）可选的系统级能力:
   `spec.containers[*].securityContext.capabilities.add`
   1. 只有 ntp 同步服务等少数容器，可以开启这项功能。请注意这非常危险。
3. Sysctls: 系统参数: `spec.securityContext.sysctls`

**权限限制**相关的安全策略有（**强烈建议在所有 Pod 上按需配置如下安全策略**！）：

1. `spec.volumes`: 所有的数据卷都可以设定读写权限
2. `spec.securityContext.runAsNonRoot: true` Pod 必须以非 root 用户运行
3. `spec.containers[*].securityContext.readOnlyRootFileSystem:true` **将容器层设为只读，防
   止容器文件被篡改**。
   1. 如果微服务需要读写文件，建议额外挂载 `emptydir` 类型的数据卷。
4. `spec.containers[*].securityContext.allowPrivilegeEscalation: false` 不允许 Pod 做任何
   权限提升！
5. `spec.containers[*].securityContext.capabilities.drop`: 移除（Capabilities）可选的系统
   级能力

还有其他诸如指定容器的运行用户(user)/用户组(group)等功能未列出，请自行查阅 Kubernetes 相关
文档。

一个无状态的微服务 Pod 配置举例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <Pod name>
spec:
  containers:
  - name: <container name>
    image: <image>
    imagePullPolicy: IfNotPresent
    # ......此处省略 500 字
    securityContext:
      readOnlyRootFilesystem: true  # 将容器层设为只读，防止容器文件被篡改。
      allowPrivilegeEscalation: false  # 禁止 Pod 做任何权限提升
      capabilities:
        drop:
        # 禁止容器使用 raw 套接字，通常只有 hacker 才会用到 raw 套接字。
        # raw_socket 可自定义网络层数据，避开 tcp/udp 协议栈，直接操作底层的 ip/icmp 数据包。可实现 ip 伪装、自定义协议等功能。
        # 去掉 net_raw 会导致 tcpdump 无法使用，无法进行容器内抓包。需要抓包时可临时去除这项配置
        - NET_RAW
        # 更好的选择：直接禁用所有 capabilities
        # - ALL
  securityContext:
    # runAsUser: 1000  # 设定用户
    # runAsGroup: 1000  # 设定用户组
    runAsNonRoot: true  # Pod 必须以非 root 用户运行
    seccompProfile:  # security compute mode
      type: RuntimeDefault
```

### 2. seccomp: security compute mode

seccomp 和 seccomp-bpf 允许对系统调用进行过滤，可以防止用户的二进制文对主机操作系统件执行
通常情况下并不需要的危险操作。它和 Falco 有些类似，不过 Seccomp 没有为容器提供特别的支持。

视频:

- [Seccomp: What Can It Do For You? - Justin Cormack, Docker](https://www.youtube.com/watch?v=Ro4QRx7VPsY&list=PLj6h78yzYM2Pn8RxfLh2qrXBDftr6Qjut$index=22)

## 六、隔离性

这个我的了解暂时有限，不过有几个建议应该是值得参考的：

- 推荐按业务线或者业务团队进行名字空间划分，方便对每个业务线/业务团队分别进行资源限制
- 推荐使用 network policy 对服务实施强力的网络管控，避免长期发展过程中，业务服务之间出现混
  乱的跨业务线相互调用关系，也避免服务被黑后，往未知地址发送数据。

## 其他问题

- 不同节点类型的性能有差距，导致 QPS 均衡的情况下，CPU 负载不均衡
  - 解决办法（未验证）：
    - 尽量使用性能相同的实例类型：通过 `podAffinity` 及 `nodeAffinity` 添加节点类型的亲和
      性

## 参考

- [istio 实践指南 - imroc.cc](https://imroc.cc/istio/)
- [Kubernetes 实践指南 - imroc.cc](https://imroc.cc/kubernetes/)
