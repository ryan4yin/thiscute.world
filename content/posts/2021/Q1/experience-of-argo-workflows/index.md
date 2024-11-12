---
title: "云原生流水线 Argo Workflows 的安装、使用以及个人体验"
date: 2021-01-27T15:37:27+08:00
draft: false

featuredImage: "argo-workflows.webp"
resources:
  - name: featured-image
    src: "argo-workflows.webp"
authors: ["ryan4yin"]

tags: ["云原生", "CI", "持续集成", "流水线", "Kubernetes"]
categories: ["tech"]
series: ["云原生相关"]

# 兼容旧的 Path（单词拼写错误）
aliases:
  - /posts/expirence-of-argo-workflow/
---

> 注意：这篇文章并不是一篇入门教程，学习 Argo Workflows 请移步官方文档
> [Argo Documentation](https://argoproj.github.io/argo-workflows/)

[Argo Workflows](https://github.com/argoproj/argo-workflows/) 是一个云原生工作流引擎，专注
于**编排并行任务**。它的特点如下：

<!--more-->

1. 使用 Kubernetes 自定义资源(CR)定义工作流，其中工作流中的每个步骤都是一个容器。
2. 将多步骤工作流建模为一系列任务，或者使用有向无环图（DAG）描述任务之间的依赖关系。
3. 可以在短时间内轻松运行用于机器学习或数据处理的计算密集型作业。
4. Argo Workflows 可以看作 Tekton 的加强版，因此显然也可以通过 Argo Workflows 运行 CI/CD
   流水线(Pipielines)。

阿里云是 Argo Workflows 的深度使用者和贡献者，另外 Kubeflow 底层的工作流引擎也是 Argo
Workflows.

## 一、Argo Workflows 对比 Jenkins

我们在切换到 Argo Workflows 之前，使用的 CI/CD 工具是 Jenkins，下面对 Argo Workflows 和
Jenkins 做一个比较详细的对比，以了解 Argo Workflows 的优缺点。

### 1. Workflow 的定义

`Workflow` 使用 kubernetes CR 进行定义，因此显然是一份 yaml 配置。

一个 Workflow，就是一个运行在 Kubernetes 上的流水线，对应 Jenkins 的一次 Build.

而 WorkflowTemplate 则是一个可重用的 Workflow 模板，对应 Jenkins 的一个 Job.

`WorkflowTemplate` 的 yaml 定义和 `Workflow` 完全一致，只有 `Kind` 不同！

WorkflowTemplate 可以被其他 Workflow 引用并触发，也可以手动传参以生成一个 Workflow 工作
流。

### 2. Workflow 的编排

Argo Workflows 相比其他流水线项目(Jenkins/Tekton/Drone/Gitlab-CI)而言，最大的特点，就是它
强大的流水线编排能力。

其他流水线项目，对流水线之间的关联性考虑得很少，基本都假设流水线都是互相独立的。

而 Argo Workflows 则假设「任务」之间是有依赖关系的，针对这个依赖关系，它提供了两种协调编排
「任务」的方法：Steps 和 DAG

再借助
[templateRef](https://argoproj.github.io/argo-workflows/workflow-templates/#referencing-other-workflowtemplates)
或者
[Workflow of Workflows](https://argoproj.github.io/argo-workflows/workflow-of-workflows/)，
就能实现 Workflows 的编排了。

**我们之所以选择 Argo Workflows 而不是 Tekton，主要就是因为 Argo 的流水线编排能力比 Tekton
强大得多**。（也许是因为我们的后端中台结构比较特殊，导致我们的 CI 流水线需要具备复杂的编排
能力）

一个复杂工作流的示例如下：

![](/images/experience-of-argo-workflows/complex-workflows.webp "https://github.com/argoproj/argo/issues/1088#issuecomment-445884543")

### 3. Workflow 的声明式配置

Argo 使用 Kubernetes 自定义资源(CR)来定义 Workflow，熟悉 Kubernetes Yaml 的同学上手应该都
很快。

下面对 Workflow 定义文件和 Jenkinsfile 做个对比：

1. argo 完全使用 yaml 来定义流水线，学习成本比 Jenkinsfile 的 groovy 低。对熟悉 Kubernetes
   的同学尤其如此。
2. 将 jenkinsfile 用 argo 重写后，代码量出现了明显的膨胀。一个 20 行的 Jenkinsfile，用
   Argo 重写可能就变成了 60 行。

配置出现了膨胀是个问题，但是考虑到它的可读性还算不错，而且 Argo 的 Workflow 编排功能，能替
代掉我们目前维护的部分 Python 构建代码，以及一些其他优点，配置膨胀这个问题也就可以接受了。

### 4. Web UI

Argo Workflows 的 Web UI 感觉还很原始。确实该支持的功能都有，但是它貌似不是面向「用户」
的，功能比较底层。

它不像 Jenkins 一样，有很友好的使用界面(虽然说 Jenkins 的 UI 也很显老...)

另外它所有的 Workflow 都是相互独立的，没办法直观地找到一个 WorkflowTemplate 的所有构建记
录，只能通过 label/namespace 进行分类，通过任务名称进行搜索。

而 Jenkins 可以很方便地看到同一个 Job 的所有构建历史。

### 5. Workflow 的分类

#### 为何需要对 Workflow 做细致的分类

常见的微服务项目，往往会拆分成众多 Git 仓库（微服务）进行开发，众多的 Git 仓库会使我们创建
众多的 CI/CD 流水线。如果没有任何的分类，这一大堆的流水线如何管理，就成了一个难题。

最显见的需求：前端和后端的流水线最好能区分一下，往下细分，前端的 Web 端和客户端最好也能区
分，后端的业务层和中台最好也区分开来。

另外我们还希望将运维、自动化测试相关的任务也集成到这个系统中来（目前我们就是使用 Jenkins
完成运维、自动化测试任务的），如果没有任何分类，这一大堆流水线将混乱无比。

#### Argo Workflows 的分类能力

当 Workflow 越来越多的时候，如果不做分类，一堆 WorkflowTemplate 堆在一起就会显得特别混乱。
（没错，我觉得 Drone 就有这个问题...）

Argo 是完全基于 Kubernetes 的，因此目前它也只能通过 namespace/labels 进行分类。

这样的分类结构和 Jenkins 的视图-文件夹体系大相径庭，目前感觉不是很好用（也可能纯粹是 Web
UI 的锅）。

### 6. 触发构建的方式

Argo Workflows 的流水线有多种触发方式：

- 手动触发：手动提交一个 Workflow，就能触发一次构建。可以通过
  [workflowTemplateRef](https://argoproj.github.io/argo-workflows/workflow-templates/#create-workflow-from-workflowtemplate-spec)
  直接引用一个现成的流水线模板。
- 定时触发：[CronWorkflow](https://argoproj.github.io/argo-workflows/cron-workflows/)
- 通过 Git 仓库变更触发：借助 [argo-events](https://github.com/argoproj/argo-events) 可以
  实现此功能，详见其文档。
  - 另外目前也不清楚 WebHook 的可靠程度如何，会不会因为宕机、断网等故障，导致 Git 仓库变更
    了，而 Workflow 却没触发，而且还没有任何显眼的错误通知？如果这个错误就这样藏起来了，就
    可能会导致很严重的问题！

### 7. secrets 管理

Argo Workflows 的流水线，可以从 kubernetes secrets/configmap 中获取信息，将信息注入到环境
变量中、或者以文件形式挂载到 Pod 中。

Git 私钥、Harbor 仓库凭据、CD 需要的 kubeconfig，都可以直接从 secrets/configmap 中获取到。

另外因为 Vault 很流行，也可以将 secrets 保存在 Vault 中，再通过 vault agent 将配置注入进
Pod。

### 8. Artifacts

Argo 支持接入对象存储，做全局的 Artifact 仓库，本地可以使用 MinIO.

使用对象存储存储 Artifact，最大的好处就是可以在 Pod 之间随意传数据，Pod 可以完全分布式地运
行在 Kubernetes 集群的任何节点上。

另外也可以考虑借助 Artifact 仓库实现跨流水线的缓存复用（未测试），提升构建速度。

### 9. 容器镜像的构建

借助 Buildkit 等容器镜像构建工具，可以实现容器镜像的分布式构建。

Buildkit 对构建缓存的支持也很好，可以直接将缓存存储在容器镜像仓库中。

> 不建议使用 Google 的 Kaniko，它对缓存复用的支持不咋地，社区也不活跃。

### 10. 客户端/SDK

Argo 有提供一个命令行客户端，也有 HTTP API 可供使用。

如下项目值得试用：

- [argo-client-python](https://github.com/argoproj-labs/argo-client-python): Argo
  Workflows 的 Python 客户端
  - 说实话，感觉和 kubernetes-client/python 一样难用，毕竟都是 openapi-generator 生成出来
    的...
- [argo-python-dsl](https://github.com/argoproj-labs/argo-python-dsl): 使用 Python DSL 编
  写 Argo Workflows
  - 感觉使用难度比 yaml 高，也不太好用。
- [couler](https://github.com/couler-proj/couler): 为 Argo/Tekton/Airflow 提供统一的构建与
  管理接口
  - 理念倒是很好，待研究

感觉 couler 挺不错的，可以直接用 Python 写 WorkflowTemplate，这样就一步到位，所有 CI/CD 代
码全部是 Python 了。

此外，因为 Argo Workflows 是 kubernetes 自定义资源 CR，也可以使用 helm/kustomize 来做
workflow 的生成。

目前我们一些步骤非常多，但是重复度也很高的 Argo 流水线配置，就是使用 helm 生成的——关键数据
抽取到 values.yaml 中，使用 helm 模板 + `range` 循环来生成 workflow 配置。

## 二、安装 Argo Workflows

> 参考官方文档：https://argoproj.github.io/argo-workflows/installation/

安装一个集群版(cluster wide)的 Argo Workflows，使用 MinIO 做 artifacts 存储：

```shell
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml
```

部署 MinIO:

```shell
helm repo add minio https://helm.min.io/ # official minio Helm charts
# 查看历史版本
helm search repo minio/minio -l | head
# 下载并解压 chart
helm pull minio/minio --untar --version 8.0.9

# 编写 custom-values.yaml，然后部署 minio
kubectl create namespace minio
helm install minio ./minio -n argo -f custom-values.yaml
```

minio 部署好后，它会将默认的 `accesskey` 和 `secretkey` 保存在名为 `minio` 的 secret 中。
我们需要修改 argo 的配置，将 minio 作为它的默认 artifact 仓库。

在 configmap `workflow-controller-configmap` 的 data 中添加如下字段：

```shell
  artifactRepository: |
    # 是否将 main 容器的日志保存为 artifact，这样 pod 被删除后，仍然可以在 artifact 中找到日志
    archiveLogs: true
    s3:
      bucket: argo-bucket   # bucket 名称，这个 bucket 需要先手动创建好！
      endpoint: minio:9000  # minio 地址
      insecure: true
      # 从 minio 这个 secret 中获取 key/secret
      accessKeySecret:
        name: minio
        key: accesskey
      secretKeySecret:
        name: minio
        key: secretkey
```

现在还差最后一步：手动进入 minio 的 Web UI，创建好 `argo-bucket` 这个 bucket. 直接访问
minio 的 9000 端口（需要使用 nodeport/ingress 等方式暴露此端口）就能进入 Web UI，使用前面
提到的 secret `minio` 中的 key/secret 登录，就能创建 bucket.

### ServiceAccount 配置

> https://argoproj.github.io/argo-workflows/service-accounts/

Argo Workflows 依赖于 ServiceAccount 进行验证与授权，而且默认情况下，它使用所在 namespace
的 `default` ServiceAccount 运行 workflow.

可 `default` 这个 ServiceAccount 默认根本没有任何权限！所以 Argo 的 artifacts, outputs,
access to secrets 等功能全都会因为权限不足而无法使用！

为此，Argo 的官方文档提供了两个解决方法。

方法一，直接给 default 绑定 `cluster-admin` ClusterRole，给它集群管理员的权限，只要一行命
令（但是显然安全性堪忧）：

```shell
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=<namespace>:default -n <namespace>
```

方法二，官方给出
了[Argo Workflows 需要的最小权限的 Role 定义](https://argoproj.github.io/argo-workflows/workflow-rbac/)，
方便起见我将它改成一个 ClusterRole:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: argo-workflows-role
rules:
  # pod get/watch is used to identify the container IDs of the current pod
  # pod patch is used to annotate the step's outputs back to controller (e.g. artifact location)
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - get
      - watch
      - patch
  # logs get/watch are used to get the pods logs for script outputs, and for log archival
  - apiGroups:
      - ""
    resources:
      - pods/log
    verbs:
      - get
      - watch
```

创建好上面这个最小的 ClusterRole，然后为每个名字空间，跑一下如下命令，给 default 账号绑定
这个 clusterrole:

```shell
kubectl create rolebinding default-argo-workflows --clusterrole=argo-workflows-role  --serviceaccount=<namespace>:default -n <namespace>
```

这样就能给 default 账号提供最小的 workflow 运行权限。

或者如果你希望使用别的 ServiceAccount 来运行 workflow，也可以自行创建 ServiceAccount，然后
再走上面方法二的流程，但是最后，要记得在 workflow 的 `spec.serviceAccountName` 中设定好
ServiceAccount 名称。

### Workflow Executors

> https://argoproj.github.io/argo-workflows/workflow-executors/

Workflow Executor 是符合特定接口的一个进程(Process)，Argo 可以通过它执行一些动作，如监控
Pod 日志、收集 Artifacts、管理容器生命周期等等...

Workflow Executor 有多种实现，可以通过前面提到的 configmap `workflow-controller-configmap`
来选择。

可选项如下：

1. docker(默认): 目前使用范围最广，但是安全性最差。它要求一定要挂载访问 `docker.sock`，因
   此一定要 root 权限！
2. kubelet: 应用非常少，目前功能也有些欠缺，目前也必须提供 root 权限
3. Kubernetes API (k8sapi): 直接通过调用 k8sapi 实现日志监控、Artifacts 手机等功能，非常安
   全，但是性能欠佳。
4. Process Namespace Sharing (pns): 安全性比 k8sapi 差一点，因为 Process 对其他所有容器都
   可见了。但是相对的性能好很多。

在 docker 被 kubernetes 抛弃的当下，如果你已经改用 containerd 做为 kubernetes 运行时，那
argo 将会无法工作，因为它默认使用 docker 作为运行时！

我们建议将 workflow executore 改为 `pns`，兼顾安全性与性
能，`workflow-controller-configmap` 按照如下方式修改：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: workflow-controller-configmap
data:
  config: |
    # ...省略若干配置...

    # Specifies the container runtime interface to use (default: docker)
    # must be one of: docker, kubelet, k8sapi, pns
    containerRuntimeExecutor: pns
    # ...
```

## 三、使用 Argo Workflows 做 CI 工具

官方的 Reference 还算详细，也有提供非常多的 examples 供我们参考，这里提供我们几个常用的
workflow 定义。

1. 使用 buildkit 构建镜
   像：https://github.com/argoproj/argo-workflows/blob/master/examples/buildkit-template.yaml
   1. buildkit 支持缓存，可以在这个 example 的基础上自定义参数
   2. 注意使用 PVC 来跨 step 共享存储空间这种手段，速度会比通过 artifacts 高很多。

## 四、常见问题

### 1. workflow 默认使用 root 账号？

workflow 的流程默认使用 root 账号，如果你的镜像默认使用非 root 账号，而且要修改文件，就很
可能遇到 Permission Denined 的问题。

解决方法：通过 Pod Security Context 手动设定容器的 user/group:

- [Workflow Pod Security Context](https://argoproj.github.io/argo-workflows/workflow-pod-security-context/)

安全起见，我建议所有的 workflow 都手动设定 `securityContext`，示例：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: xxx
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
```

或者也可以通过 `workflow-controller-configmap` 的 `workflowDefaults` 设定默认的 workflow
配置。

### 2. 如何从 hashicorp vault 中读取 secrets?

> 参考
> [Support to get secrets from Vault](https://github.com/argoproj/argo-workflows/issues/3267#issuecomment-650119636)

hashicorp vault 目前可以说是云原生领域最受欢迎的 secrets 管理工具。我们在生产环境用它做为
分布式配置中心，同时在本地 CI/CD 中，也使用它存储相关的敏感信息。

现在迁移到 argo，我们当然希望能够有一个好的方法从 vault 中读取配置。

目前最推荐的方法，是使用 vault 的 vault-agent，将 secrets 以文件的形式注入到 pod 中。

通过 valut-policy - vault-role - k8s-serviceaccount 一系列认证授权配置，可以制定非常细粒度
的 secrets 权限规则，而且配置信息阅后即焚，安全性很高。

### 3. 如何在多个名字空间中使用同一个 secrets?

使用 Namespace 对 workflow 进行分类时，遇到的一个常见问题就是，如何在多个名字空间使用
`private-git-creds`/`docker-config`/`minio`/`vault` 等 workflow 必要的 secrets.

常见的方法是把 secrets 在所有名字空间 create 一次。

但是也有更方便的 secrets 同步工具：

比如，使用 [kyverno](https://github.com/kyverno/kyverno) 进行 secrets 同步的配置：

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: sync-secrets
spec:
  background: false
  rules:
    # 将 secret vault 从 argo Namespace 同步到其他所有 Namespace
    - name: sync-vault-secret
      match:
        resources:
          kinds:
            - Namespace
      generate:
        kind: Secret
        name: regcred
        namespace: "{{request.object.metadata.name}}"
        synchronize: true
        clone:
          namespace: argo
          name: vault
  # 可以配置多个 rules，每个 rules 同步一个 secret
```

上面提供的 kyverno 配置，会实时地监控所有 Namespace 变更，一但有新 Namespace 被创建，它就
会立即将 `vault` secret 同步到该 Namespace.

或者，使用专门的 secrets/configmap 复制工
具：[kubernetes-replicator](https://github.com/mittwald/kubernetes-replicator)

### 4. Argo 对 CR 资源的验证不够严谨，写错了 key 都不报错

待研究

### 5. 如何归档历史数据？

Argo 用的时间长了，跑过的 Workflows/Pods 全都保存在 Kubernetes/Argo Server 中，导致 Argo
越用越慢。

为了解决这个问题，Argo 提供了一些配置来限制 Workflows 和 Pods 的数量，详
见：[Limit The Total Number Of Workflows And Pods](https://argoproj.github.io/argo-workflows/cost-optimisation/#limit-the-total-number-of-workflows-and-pods)

这些限制都是 Workflow 的参数，如果希望设置一个全局默认的限制，可以按照如下示例修改 argo 的
`workflow-controller-configmap` 这个 configmap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: workflow-controller-configmap
data:
  config: |
    # Default values that will apply to all Workflows from this controller, unless overridden on the Workflow-level
    # See more: docs/default-workflow-specs.md
    workflowDefaults:
      spec:
        # must complete in 8h (28,800 seconds)
        activeDeadlineSeconds: 28800
        # keep workflows for 1d (86,400 seconds)
        ttlStrategy:
          secondsAfterCompletion: 86400
          # secondsAfterSuccess: 5
          # secondsAfterFailure: 500
        # delete all pods as soon as they complete
        podGC:
          # 可选项："OnPodCompletion", "OnPodSuccess", "OnWorkflowCompletion", "OnWorkflowSuccess"
          strategy: OnPodCompletion
```

### 6. Argo 的其他进阶配置

Argo Workflows 的配置，都保存在 `workflow-controller-configmap` 这个 configmap 中，我们前
面已经接触到了它的部分内容。

这里给出此配置文件的完整 examples:
<https://github.com/argoproj/argo-workflows/blob/master/docs/workflow-controller-configmap.yaml>

其中一些可能需要自定义的参数如下：

- `parallelism`: workflow 的最大并行数量
- `persistence`: 将完成的 workflows 保存到 postgresql/mysql 中，这样即使 k8s 中的 workflow
  被删除了，还能查看 workflow 记录
  - 也支持配置过期时间
- `sso`: 启用单点登录

### 7. 是否应该尽量使用 CI/CD 工具提供的功能？

我从同事以及网络上，了解到部分 DevOps 人员主张尽量自己使用 Python/Go 来实现 CI/CD 流水
线，CI/CD 工具提供的功能能不使用就不要使用。

因此有此一问。下面做下详细的分析：

尽量使用 CI/CD 工具提供的插件/功能，好处是不需要自己去实现，可以降低维护成本。但是相对的运
维人员就需要深入学习这个 CI/CD 工具的使用，另外还会和 CI/CD 工具绑定，会增加迁移难度。

而尽量自己用 Python 等代码去实现流水线，让 CI/CD 工具只负责调度与运行这些 Python 代码，那
CI/CD 就可以很方便地随便换，运维人员也不需要去深入学习 CI/CD 工具的使用。缺点是可能会增加
CI/CD 代码的复杂性。

我观察到 argo/drone 的一些 examples，发现它们的特征是：

1. 所有 CI/CD 相关的逻辑，全都实现在流水线中，不需要其他构建代码
2. 每一个 step 都使用专用镜像：golang/nodejs/python
   1. 比如先使用 golang 镜像进行测试、构建，再使用 kaniko 将打包成容器镜像

那是否应该尽量使用 CI/CD 工具提供的功能呢？ **其实这就是有多种方法实现同一件事，该用哪种方
法的问题。这个问题在各个领域都很常见**。

以我目前的经验来看，需要具体问题具体分析，以 Argo Workflows 为例：

1. 流水线本身非常简单，那完全可以直接使用 argo 来实现，没必要自己再搞个 python 脚本
   1. 简单的流水线，迁移起来往往也非常简单。没必要为了可迁移性，非要用 argo 去调用 python
      脚本。
2. 流水线的步骤之间包含很多逻辑判断/数据传递，那很可能是你的流水线设计有问题！
   1. **流水线的步骤之间传递的数据应该尽可能少！复杂的逻辑判断应该尽量封装在其中一个步骤
      中**！
   2. 这种情况下，就应该使用 python 脚本来封装复杂的逻辑，而不应该将这些逻辑暴露到 Argo
      Workflows 中！
3. 我需要批量运行很多的流水线，而且它们之间还有复杂的依赖关系：那显然应该利用上 argo
   workflow 的高级特性。
   1. argo 的 dag/steps 和 workflow of workflows 这两个功能结合，可以简单地实现上述功能。

## 8. 如何提升 Argo Workflows 的创建和销毁速度？

我们发现 workflow 的 pod，创建和销毁消耗了大量时间，尤其是销毁。这导致我们单个流水线在
argo 上跑，还没在 jenkins 上跑更快。

## 使用体验

目前已经使用 Argo Workflows 一个月多了，总的来说，最难用的就是 Web UI。

其他的都是小问题，只有 Web UI 是真的超难用，感觉根本就没有好好做过设计...

急需一个第三方 Web UI...

## 画外 - 如何处理其他 Kubernetes 资源之间的依赖关系

Argo 相比其他 CI 工具，最大的特点，是它假设「任务」之间是有依赖关系的，因此它提供了多种协
调编排「任务」的方法。

但是貌似 Argo CD 并没有继承这个理念，Argo CD 部署时，并不能在 kubernetes 资源之间，通过
DAG 等方法定义依赖关系。

微服务之间存在依赖关系，希望能按依赖关系进行部署，而 ArgoCD/FluxCD 部署 kubernetes yaml 时
都是不考虑任何依赖关系的。这里就存在一些矛盾。

解决这个矛盾的方法有很多，我查阅了很多资料，也自己做了一些思考，得到的最佳实践来
自[解决服务依赖 - 阿里云 ACK 容器服务](https://developer.aliyun.com/article/573791)，它给
出了两种方案：

1. **应用端服务依赖检查**: 即在微服务的入口添加依赖检查逻辑，确保所有依赖的微服务/数据库都
   可访问了，就续探针才能返回 200. 如果超时就直接 Crash
2. **独立的服务依赖检查逻辑**: 部分遗留代码使用方法一改造起来或许会很困难，这时可以考虑使
   用 **pod initContainer** 或者容器的启动脚本中，加入依赖检查逻辑。

但是这两个方案也还是存在一些问题，在说明问题前，我先说明一下我们「**按序部署**」的应用场
景。

我们是一个很小的团队，后端做 RPC 接口升级时，通常是直接在开发环境做全量升级+测试。因此运维
这边也是，每次都是做全量升级。

因为没有协议协商机制，新的微服务的「RPC 服务端」将兼容 v1 v2 新旧两种协议，而新的「RPC 客
户端」将直接使用 v2 协议去请求其他微服务。这就导致我们**必须先升级「RPC 服务端」，然后才能
升级「RPC 客户端」**。

为此，在进行微服务的全量升级时，就需要沿着 RPC 调用链路按序升级，这里就涉及到了 Kubernetes
资源之间的依赖关系。

> 我目前获知的关键问题在于：我们使用的并不是真正的微服务开发模式，而是在把整个微服务系统当
> 成一个「单体服务」在看待，所以引申出了这样的依赖关键的问题。我进入的新公司完全没有这样的
> 问题，所有的服务之间在 CI/CD 这个阶段都是解耦的，CI/CD 不需要考虑服务之间的依赖关系，也
> 没有自动按照依赖关系进行微服务批量发布的功能，这些都由开发人员自行维护。或许这才是正确的
> 使用姿势，如果动不动就要批量更新一大批服务，那微服务体系的设计、拆分肯定是有问题了，生产
> 环境也不会允许这么轻率的更新。

前面讲了，阿里云提供的「应用端服务依赖检查」和「独立的服务依赖检查逻辑」是最佳实践。它们的
优点有：

1. 简化部署逻辑，每次直接做全量部署就 OK。
2. 提升部署速度，具体体现在：GitOps 部署流程只需要走一次（按序部署要很多次）、所有镜像都提
   前拉取好了、所有 Pod 也都提前启动了。

但是这里有个问题是「灰度发布」或者「滚动更新」，这两种情况下都存在**新旧版本共存**的问题。

如果出现了 RPC 接口升级，那就必须先完成「RPC 服务端」的「灰度发布」或者「滚动更新」，再去
更新「RPC 客户端」。

否则如果直接对所有微服务做灰度更新，只依靠「服务依赖检查」，就会出现这样的问题——「RPC 服务
端」处于「薛定谔」状态，你调用到的服务端版本是新还是旧，取决于负载均衡的策略和概率。

**因此在做 RPC 接口的全量升级时，只依靠「服务依赖检查」是行不通的**。我目前想到的方案，有
如下几种：

- 我们当前的使用方案：**直接在 yaml 部署这一步实现按序部署**，每次部署后就轮询
  kube-apiserver，确认全部灰度完成，再进行下一阶段的 yaml 部署。
- **让后端加个参数来控制客户端使用的 RPC 协议版本，或者搞一个协议协商**。这样就不需要控制
  微服务发布顺序了。
- 社区很多有状态应用的部署都涉及到部署顺序等复杂操作，目前流行的解决方案是**使用
  Operator+CRD 来实现这类应用的部署**。Operator 会自行处理好各个组件的部署顺序。

## 参考文档

- [Argo加入CNCF孵化器，一文解析Kubernetes原生工作流](https://www.infoq.cn/article/fFZPvrKtbykg53x03IaH)

视频:

- [How to Multiply the Power of Argo Projects By Using Them Together - Hong Wang](https://www.youtube.com/watch?v=fKiU7txd4RI&list=PLj6h78yzYM2Pn8RxfLh2qrXBDftr6Qjut&index=149)
