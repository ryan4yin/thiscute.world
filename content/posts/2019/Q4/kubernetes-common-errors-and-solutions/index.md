---
title: "Kubernetes 常见错误、原因及处理方法"
date: 2019-11-24T19:26:54+08:00
draft: false

resources:
  - name: "featured-image"
    src: "featured-image.webp"

tags: ["Kubernetes"]
categories: ["tech"]
series: ["云原生相关"]
---

## Pod 常见错误

1. OOMKilled: Pod 的内存使用超出了 resources.limits 中的限制，被强制杀死。
2. [SandboxChanged: Pod sandbox changed, it will be killed and re-created](https://cloud.tencent.com/developer/article/1411527):
   很可能是由于内存限制导致容器被 OOMKilled，或者其他资源不足
   1. 如果是 OOM，容器通常会被重启，`kubectl describe` 能看到容器上次被重启的原因
      `State.Last State.Reason = OOMKilled, Exit Code=137`.
3. Pod 不断被重启，`kubectl describe` 显示重启原因
   `State.Last State.Reason = Error, Exit Code=137`，137 对应 SIGKILL(`kill -9`) 信号，说
   明容器被强制重启。可能的原因：
   1. 最有可能的原因是，存活探针（livenessProbe）检查失败
   2. 节点资源不足，内核强制关闭了进程以释放资源，这种情况可以通过 `journalctl -k` 查看详
      细的系统日志。
4. CrashLoopBackoff: Pod 进入 **崩溃-重启**循环，重启间隔时间从 10 20 40 80 一直翻倍到上限
   300 秒，然后以 300 秒为间隔无限重启。
5. Pod 一直 Pending: 这说明没有任何节点能满足 Pod 的要求，容器无法被调度。比如端口被别的容
   器用 hostPort 占用，节点有污点等。
6. [FailedCreateSandBox: Failed create pod sandbox: rpc error: code = DeadlineExceeded desc = context deadline exceeded]()：
   很可能是 CNI 网络插件的问题（比如 ip 地址溢出），
7. [FailedSync: error determining status: rpc error: code = DeadlineExceeded desc = context deadline exceeded](https://github.com/kubernetes/kubernetes/issues/55094):
   常和前两个错误先后出现，很可能是 CNI 网络插件的问题。
8. 开发集群，一次性部署所有服务时，各 Pod 互相争抢资源，导致 Pod 生存探针失败，不断重启，
   重启进一步加重资源使用。恶性循环。
   - **需要给每个 Pod 加上 resources.requests，这样资源不足时，后续 Pod 会停止调度，直到资
     源恢复正常**。
9. Pod 出现大量的 Failed 记录，Deployment 一直重复建立 Pod: 通过
   `kubectl describe/edit pod <pod-name>` 查看 pod `Events` 和 `Status`，一般会看到失败信
   息，如节点异常导致 Pod 被驱逐。
10. [Kubernetes 问题排查：Pod 状态一直 Terminating](https://zhuanlan.zhihu.com/p/70031676)
11. 创建了 Deployment 后，却没有自动创建 Pod: 缺少某些创建 Pod 必要的东西，比如设定的
    ServiceAccount 不存在。
12. Pod 运行失败，状态为 MatchNodeSelector: 对主节点进行关机、迁移等操作，导致主调度器下线
    时，会在一段时间内导致 Pod 调度失败，调度失败会报这个错。
13. Pod 仍然存在，但是 `Service` 的 Endpoints 却为空，找不到对应的 Pod IPs: 遇到过一次，是
    因为时间跳变（从未来的时间改回了当前时间）导致的问题。
14. Pod 无法调度，报错 `x node(s) had volume node affinity conflict`: 说明该 pod 所绑定的
    PV 有 nodeAffinity 无法满足，可以 check 对应的 PV yaml. 通常原因是 PV 所在的可用区，没
    有可用的节点，导致 Pod 无法调度。
    1. 最简单的解决方法是，在对应的可用区补充节点
    2. 如果数据可以丢，也可以考虑直接删除重建 PV/PVC

### 控制面故障可能会导致各类奇怪的异常现象

对于生产环境的集群，因为有高可用，通常我们比较少遇到控制面故障问题。但是一旦控制面发生故
障，就可能会导致各类奇怪的异常现象。如果能在排查问题时，把控制面异常考虑进来，在这种情况
下，就能节约大量的排查时间，快速定位到问题。

其中比较隐晦的就是 controller-manager 故障导致的异常：

1. 节点的服务器已经被终止，但是 Kubernetes 里还显示 node 为 Ready 状态，不会更新为
   NotReady.
2. 被删除的 Pods 可能会卡在 Terminating 状态，只有强制删除才能删除掉它们。并且确认 Pod 没
   有 `metadata.finalizers` 属性
3. HPA 的动态伸缩功能失效
4. ...

如果这些现象同时发生，就要怀疑是否是 kube-controller-manager 出问题了.

最简单的排查命令：

```bash
$ kubectl get componentstatuses
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS    MESSAGE   ERROR
scheduler            Healthy   ok
controller-manager   Healthy   ok
etcd-0               Healthy   ok

# 类似这种错误
$ kubectl events --types=Warning -n your-namespace
LAST SEEN   TYPE      REASON                     OBJECT                                   MESSAGE
56m         Warning   UpdateLoadBalancerFailed   Service/xxx-xxx   Error updating load balancer with new hosts [xxx-4-3dsiuh <1 more>], error: failed to update load-balancer with ID xxx: xxx error
```

如果三个组件任一个显示 Unhealthy，就能确定是控制面出现了问题。

> 这个 API 已被废弃，有人建议使用 `kubectl get --raw='/readyz?verbose'` 来替代。但我实测发
> 现即使这个命令返回全都 OK，但 controller-manager/scheduler 仍旧可能出问题。

其他控制面异常的详细分析，参见
[kubernetes 控制面故障现象及分析](https://github.com/ryan4yin/knowledge/blob/master/kubernetes/kubernetes%20%E6%8E%A7%E5%88%B6%E9%9D%A2%E6%95%85%E9%9A%9C%E7%8E%B0%E8%B1%A1%E5%8F%8A%E5%88%86%E6%9E%90.md)

### Pod 无法删除

可能是某些资源无法被GC，这会导致容器已经 Exited 了，但是 Pod 一直处于 Terminating 状态。

这个问题在网上能搜到很多案例,但大都只是提供了如下的强制清理命令，未分析具体原因：

```shell
kubectl delete pods <pod> --grace-period=0 --force
```

最近找到几篇详细的原因分析文章，值得一看：

- [腾讯云原生 -【Pod Terminating原因追踪系列】之 containerd 中被漏掉的 runc 错误信息](https://cloud.tencent.com/developer/article/1680612)
- [腾讯云原生 -【Pod Terminating原因追踪系列之二】exec连接未关闭导致的事件阻塞](https://cloud.tencent.com/developer/article/1680613)
- [腾讯云原生 -【Pod Terminating原因追踪系列之三】让docker事件处理罢工的cancel状态码](https://cloud.tencent.com/developer/article/1689486)
- [Pod terminating - 问题排查 - KaKu Li](https://www.likakuli.com/posts/docker-pod-terminating/)

大致总结一下，主要原因来自 docker 18.06 以及 kubernetes 的 docker-shim 运行时的底层逻辑，
已经在新版本被修复了。

### initContainers 不断 restart，但是 Containers 却都显示已 ready

Kubernetes 应该确保所有 initContainers 都 Completed，然后才能启动 Containers.

但是我们发现有一个节点上，所有包含 initContainers 的 Pod，状态全都是
`Init:CrashLoopBackOff` 或者 `Init:Error`.

而且进一步 `kubectl describe po` 查看细节，发现 initContainer 的状态为:

```
...
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    2
      Started:      Tue, 03 Aug 2021 06:02:42 +0000
      Finished:     Tue, 03 Aug 2021 06:02:42 +0000
    Ready:          False
    Restart Count:  67
...
```

而 Containers 的状态居然是 ready:

```
...
    Host Port:      0/TCP
    State:          Running
      Started:      Tue, 03 Aug 2021 00:35:30 +0000
    Ready:          True
    Restart Count:  0
...
```

initContainers 还未运行成功，而 Containers 却 Ready 了，非常疑惑。

仔细想了下，早上因为磁盘余量告警，有手动运行过 `docker system prune` 命令，那么问题可能就
是这条命令清理掉了已经 exited 的 initContainers 容器，导致 k8s 故障，不断尝试重启该容器。

网上一搜确实有相关的信息：

- https://stackoverflow.com/questions/62333064/cant-delete-exited-init-container
- https://github.com/kubernetes/kubernetes/issues/62362

结论：使用外部的垃圾清理命令可能导致 k8s 行为异常。

## 节点常见错误

1.  [DiskPressure](https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/#node-conditions)：
    节点的可用空间不足。（通过`df -h` 查看，保证可用空间不小于 15%）
1.  The node was low on resource: ephemeral-storage: 同上，节点的存储空间不够了。

节点存储告警可能的原因：

1. kubelet 的资源 GC 设置有问题，遗留的镜像等资源未及时 GC 导致告警
2. 存在运行的 pod 使用了大量存储空间，在节点上通过 `docker ps -a --size | grep G` 可以查看
   到
3. 如果使用的是 EKS，并且磁盘告警的挂载点为
   `/var/lib/kubelet/plugins/kubernetes.io/aws-ebs/mounts/aws/us-east-1b/vol-xxxxx`
   1. 显然是 EBS 存储卷快满了导致的
   2. 可通过 ` kubectl get pv -A -o yaml | grep -C 30 vol-xxxxx` 来定位到具体的存储卷

## 网络常见错误

### 1. Ingress/Istio Gateway 返回值

1. 404：不存在该 Service/Istio Gateway，或者是服务自身返回 404
1. 500：大概率是服务自身的错误导致 500，小概率是代理（Sidecar/Ingress 等）的错误
1. 503：服务不可用，有如下几种可能的原因：
   1. Service 对应的 Pods 不存在，endpoints 为空
   2. Service 对应的 Pods 全部都 NotReady，导致 endpoints 为空
   3. 也有可能是服务自身出错返回的 503
   4. 如果你使用了 envoy sidecar， 503 可能的原因就多了。基本上 sidecar 与主容器通信过程中
      的任何问题都会使 envoy 返回 503，使客户端重试。
      1. 详见 [Istio：503、UC 和 TCP](https://blog.fleeto.us/post/istio-503-uc-debug/)
1. 502：Bad Gateway，通常是由于上游未返回正确的响应导致的，可能的根本原因：
   1. 应用程序未正确处理 SIGTERM 信号，在请求未处理完毕时直接终止了进程。详见
      [优雅停止（Gracful Shutdown）与 502/504 报错 - K8s 最佳实践](./最佳实践.md)
   2. 网络插件 bug
1. 504：网关请求 upstream 超时，主要有两种可能
   1. 考虑是不是 Ingress Controller 的 IP 列表未更新，将请求代理到了不存在的 ip，导致得不
      到响应
   1. Service Endpoints 移除不够及时，在 Pod 已经被终止后，仍然有个别请求被路由到了该
      Pod，得不到响应导致 504。详见
      [优雅停止（Gracful Shutdown）与 502/504 报错 - K8s 最佳实践](./最佳实践.md)
   1. Pod 响应太慢，代码问题

再总结一下常见的几种错误：

- 未设置优雅停止，导致 Pod 被重新终止时，有概率出现 502/504
- 服务的所有 Pods 的状态在「就绪」和「未就绪」之间摆动，导致间歇性地出现大量 503 错误
- 服务返回 5xx 错误导致客户端不断重试，请求流量被放大，导致服务一直起不来
  - 解决办法：限流、熔断（网关层直接返回固定的相应内容）

Ingress 相关网络问题的排查流程：

1. Which ingress controller?
2. Timeout between client and ingress controller, or between ingress controller and
   backend service/pod?
3. HTTP/504 generated by the ingress controller, proven by logs from the ingress
   controller?
4. If you port-forward to skip the internet between client and ingress controller, does
   the timeout still happen?

### 2. 上了 istio sidecar 后，应用程序偶尔（间隔几天半个月）会 redis 连接相关的错误

考虑是否和 tcp 长时间使用有关，比如连接长时间空闲的话，可能会被 istio sidecar 断开。如果程
序自身的重连机制有问题，就会导致这种现象。

确认方法：

1. 检查 istio 的 `idleTimeout` 时长（默认 1h）
2. 创建三五个没流量的 Pod 放置 1h（与 istio idleTimeout 时长一致），看看是否会准时开始报
   redis 的错。
3. 对照组：创建三五个同样没流量的 Pod，但是不注入 istio sidecar，应该一直很正常

这样就能确认问题，后续处理：

1. 抓包观察程序在出错后的 tcp 层行为
1. 查阅 redis sdk 的相关 issue、代码，通过升级 SDK 应该能解决问题。

## 名字空间常见错误

### 名字空间无法删除

这通常是某些资源如 CR(custom resources)/存储等资源无法释放导致的。比如常见的 monitoring 名
字空间无法删除，应该就是 CR 无法 GC 导致的。

可手动删除 namespace 配置中的析构器（spec.finalizer，在名字空间生命周期结束前会生成的配置
项），这样名字空间就会直接跳过 GC 步骤：

```shell
# 编辑名字空间的配置
kubectl edit namespace <ns-name>
# 将 spec.finalizers 改成空列表 []
```

如果上述方法也无法删除名字空间，也找不到具体的问题，就只能直接从 etcd 中删除掉它了(有风
险，谨慎操作！)。方法如下：

```shell
# 登录到 etcd 容器中，执行如下命令：
export ETCDCTL_API=3
cd /etc/kubernetes/pki/etcd/
# 列出所有名字空间
etcdctl --cacert ca.crt --cert peer.crt --key peer.key get /registry/namespaces --prefix --keys-only

# （谨慎操作！！！）强制删除名字空间 `monitoring`。这可能导致相关资源无法被 GC！
etcdctl --cacert ca.crt --cert peer.crt --key peer.key del /registry/namespaces/monitoring
```

## kubectl/istioctl 等客户端工具异常

1. `socat not found`: kubectl 使用 `socat` 进行端口转发，集群的所有节点，以及本机都必须安
   装有 `socat` 工具。

## 批量清理 Evicted 记录

有时候 Pod 因为节点选择器的问题，被不断调度到有问题的 Node 上，就会不断被 Evicted，导致出
现大量的 Evicted Pods。排查完问题后，需要手动清理掉这些 Evicted Pods.

批量删除 Evicted 记录:

```shell
kubectl get pods | grep Evicted | awk '{print $1}' | xargs kubectl delete pod
```

## 容器镜像GC、Pod驱逐以及节点压力

节点压力 DiskPressure 会导致 Pod 被驱逐，也会触发容器镜像的 GC。

根据官方文档
[配置资源不足时的处理方式](https://kubernetes.io/zh/docs/tasks/administer-cluster/out-of-resource)，Kubelet
提供如下用于配置容器 GC 及 Evicetion 的阈值：

1. `--eviction-hard` 和 `eviction-soft`: 对应旧参数 `--image-gc-high-threshold`，这两个参
   数配置镜像 GC 及驱逐的触发阈值。磁盘使用率的阈值默认为 85%
   1. 区别在于 `eviction-hard` 是立即驱逐，而 `eviction-soft` 在超过
      `eviction-soft-grace-period` 之后才驱逐。
2. `--eviction-minimum-reclaim`: 对应旧参数 `--image-gc-low-threshold`。这是进行资源回收
   （镜像GC、Pod驱逐等）后期望达到的磁盘使用率百分比。磁盘使用率的阈值默认值为 80%。

问：能否为 ImageGC 设置一个比 DiskPressure 更低的阈值？因为我们希望能自动进行镜像 GC，但是
不想立即触发 Pod 驱逐。

答：这应该可以通过设置 `eviction-soft` 和长一点的 `eviction-soft-grace-period` 来实现。另
外 `--eviction-minimum-reclaim` 也可以设小一点，清理得更干净。示例如下：

```shell
--eviction-soft=memory.available<1Gi,nodefs.available<2Gi,imagefs.available<200Gi
--eviction-soft-grace-period=3m
--eviction-minimum-reclaim=memory.available=0Mi,nodefs.available=1Gi,imagefs.available=2Gi
```

## 监控/HPA 常见错误

### 服务设置了 HPA 阈值为 50% CPU，所有业务容器在启动后不久就会 OOM，CPU 暴涨然后挂掉。但是无法触发 CPU 扩缩容，Prometheus 监控指标也不对劲。

根据
[metrics-sever - how-often-metrics-are-scraped](https://github.com/kubernetes-sigs/metrics-server/blob/master/FAQ.md#how-often-metrics-are-scraped)
描述，metrics-sever 默认情况下每 60s 采集一次指标，而 Prometheus 的采集间隔通常会配置为
15s/30s。

这说明如果业务容器每次重启后，都坚持不过 60s 就会挂掉，就很可能导致 metrics-sever 采集不到
足够的指标，HPA 查询到的平均 CPU 将会是 0%，无法触发扩容操作。

Prometheus 也是一样的逻辑，如果容器每次启动都坚持不过 30s，那就会导致 prometheus 经常抓不
到指标，监控图表或者告警就会出问题。

## 其他问题

### 隔天 Istio 等工具的 sidecar 自动注入莫名其妙失效了

如果服务器晚上会关机，可能导致第二天网络插件出问题，导致 sidecar 注入器无法观察到 pod 的创
建，也就无法完成 sidecar 注入。

### 如何重新运行一个 Job？

我们有一个 Job 因为外部原因运行失败了，修复好后就需要重新运行它。

方法是：删除旧的 Job，再使用同一份配置重建 Job.

如果你使用的是 fluxcd 这类 GitOps 工具，就只需要手工删除旧 Pod，fluxcd 会定时自动 apply 所
有配置，这就完成了 Job 的重建。

## 参考

- [Kubernetes管理经验](https://yq.aliyun.com/articles/703971?type=2)
- [504 Gateway Timeout when accessing workload via ingress](https://www.reddit.com/r/kubernetes/comments/ced0py/504_gateway_timeout_when_accessing_workload_via/)
- [Kubernetes Failure Stories](https://k8s.af/)
- [Istio：503、UC 和 TCP](https://blog.fleeto.us/post/istio-503-uc-debug/)
- [istio 实践指南 - imroc.cc](https://imroc.cc/istio/)
- [Kubernetes 实践指南 - imroc.cc](https://imroc.cc/kubernetes/)
