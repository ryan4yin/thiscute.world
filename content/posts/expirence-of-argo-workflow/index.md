---
title: "云原生流水线 Argo Workflow 的安装、使用以及个人体验"
date: 2021-01-27T15:37:27+08:00
draft: true

resources:
- name: "featured-image"
  src: "argo-workflow.png"

tags: ["云原生", "CI","持续集成", "流水线"]
categories: ["技术"]
---

[Argo Workflow](https://github.com/argoproj/argo/) 是一个云原生工作流引擎，专注于**编排并行任务**。它的特点如下：

1. 使用 Kubernetes 自定义资源(CR)定义工作流，其中工作流中的每个步骤都是一个容器。
2. 将多步骤工作流建模为一系列任务，或者使用有向无环图（DAG）描述任务之间的依赖关系。
3. 可以在短时间内轻松运行用于机器学习或数据处理的计算密集型作业。
4. Argo Workflow 可以看作 Tekton 的加强版，因此显然也可以通过 Argo Workflow 运行 CI/CD 流水线(Pipielines)。

阿里云是 Argo Workflow 的深度使用者和贡献者，另外 Kubeflow 底层的工作流引擎也是 Argo Workflow.

## 一、Argo Workflow 对比 Jenkins

我们在切换到 Argo Workflow 之前，使用的 CI/CD 工具是 Jenkins，下面对 Argo Workflow 和 Jenkins 做一个比较详细的对比，
以了解 Argo Workflow 的优缺点。

### 1. Workflow 的重用 - WorkflowTemplate

将 yaml 定义中的 `Kind` 从 `Workflow` 修改为 `WorkflowTemplate`，就能得到一个 WorkflowTemplate.

WorkflowTemplate 可以被其他 Workflow 引用并触发，也可以正常传参。

### 2. Workflow 的编排

Argo Workflow 相比其他流水线项目(Jenkins/Tekton/Drone/Gitlab-CI)而言，最大的特点，就是它强大的流水线编排能力。

其他流水线项目，对流水线之间的关联性考虑得很少，基本都假设流水线都是互相独立的。

而 Argo Workflow 能够将多个 Workflows 通过 Steps/DAG 编排起来，让流水线的各个步骤按依赖顺序分批地运行。

再借助 `templateRef` 或者 `Workflow of Workflows`，就能实现 Workflows 的编排了。

**我们之所以选择 Argo Workflow 而不是 Tekton，主要就是因为 Argo 的流水线编排能力比 Tekton 强大得多。**

### 3. Web UI

Argo Workflow 的 Web UI 感觉还很原始。确实该支持的功能都有，但是它貌似不是面向「用户」的，功能比较底层。

它不像 Jenkins 一样，有很友好的使用界面。

另外它所有的 Workflow 都是相互独立的，没办法直观地找到一个 WorkflowTemplate 的所有构建记录，只能通过 label/namespace 进行分类，通过任务名称进行搜索。

而 Jenkins 可以很方便地看到同一个 Job 的所有构建历史。

现在特别想要一个第三方 Web UI 来帮我们脱离苦海...

### 4. Workflow 的分类

#### 为何需要对 Workflow 做细致的分类

常见的微服务项目，往往会拆分成众多 Git 仓库（微服务）进行开发，众多的 Git 仓库会使我们创建众多的 CI/CD 流水线。
如果没有任何的分类，这一大堆的流水线如何管理，就成了一个难题。

最显见的需求：前端和后端的流水线最好能区分一下，往下细分，前端的 Web 端和客户端最好也能区分，后端的业务层和中台最好也区分开来。

另外我们还希望将运维、自动化测试相关的任务也集成到这个系统中来（目前我们就是使用 Jenkins 完成运维、自动化测试任务的），
如果没有任何分类，这一大堆流水线将混乱无比。

#### Argo Workflow 的分类能力

当 Workflow 越来越多的时候，如果不做分类，一堆 WorkflowTemplate 堆在一起就会显得特别混乱。（没错，我觉得 Drone 就有这个问题...）

Argo 是完全基于 Kubernetes 的，因此目前它也只能通过 namespace/labels 进行分类。

这样的分类结构和 Jenkins 的视图-文件夹体系大相径庭，目前感觉不是很好用（也可能纯粹是 Web UI 的锅）。

### 5. 触发构建的方式

Argo Workflow 的流水线有多种触发方式：

- 手动触发：手动提交一个 Workflow，就能触发一次构建。可以通过 `workflowTemplateRef` 直接引用一个现成的流水线模板。
- 定时触发：CronWorkflow
- 通过 Git 仓库变更触发：[Argo Workflow - Webhooks](https://argoproj.github.io/argo/webhooks/) 支持通过 webhook 集成 github/gitlab.
  - 不过感觉很难用，貌似也有人通过 [NATS](https://github.com/nats-io) 之类的消息系统来触发构建(比如 Knative)，可以参考.
  - 另外目前也不清楚 WebHook 的可靠程度如何，会不会因为宕机、断网等故障，导致 Git 仓库变更了，而 Workflow 却没触发，而且还没有任何显眼的错误通知？如果这个错误就这样藏起来了，就可能会导致很严重的问题！


### 6. secrets 管理

Argo Workflow 的流水线，可以从 kubernetes secrets/configmap 中获取信息，将信息注入到环境变量中、或者以文件形式挂载到 Pod 中。

Git 私钥、Harbor 仓库凭据、CD 需要的 kubeconfig，都可以直接从 secrets/configmap 中获取到。

另外因为 Vault 很流行，也可以将 secrets 保存在 Vault 中，再通过 vault agent 将配置注入进 Pod。


### 7. Artifacts

Argo 支持接入对象存储，做全局的 Artifact 仓库，本地可以使用 MinIO.

使用对象存储存储 Artifact，最大的好处就是可以在 Pod 之间随意传数据，Pod 可以完全分布式地运行在 Kubernetes 集群的任何节点上。

另外也可以考虑借助 Artifact 仓库实现跨流水线的缓存复用（未测试），提升构建速度。


### 8. 容器镜像的构建

借助 Kaniko 等容器镜像构建工具，可以实现容器镜像的分布式构建。

Kaniko 对构建缓存的支持也很好，可以直接将缓存存储在容器镜像仓库中。


### 9. 客户端/SDK

Argo 有提供一个命令行客户端，也有 HTTP API 可供使用。

如下项目值得试用：

- [argo-client-python](https://github.com/argoproj-labs/argo-client-python): Argo Workflow 的 Python 客户端
- [couler](https://github.com/couler-proj/couler): 为  Argo/Tekton/Airflow 提供统一的构建与管理接口
- [argo-python-dsl](https://github.com/argoproj-labs/argo-python-dsl): 使用 Python DSL 编写 Argo Workflow

感觉 couler 挺不错的，可以直接用 Python 写 WorkflowTemplate，这样就一步到位，所有 CI/CD 代码全部是 Python 了。

此外，因为 argo workflow 是 kubernetes 自定义资源 CR，也可以使用 helm/kustomize 来做 workflow 的生成。

目前我们一些步骤非常多，但是重复度也很高的 Argo 流水线配置，就是使用 helm 生成的——关键数据抽取到 values.yaml 中，使用 helm 模板 + `range` 循环来生成 workflow 配置。


## 二、[安装 Argo Workflow](https://argoproj.github.io/argo/installation/)

安装一个集群版(cluster wide)的 Argo Workflow，使用 MinIO 做 artifacts 存储：

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

现在还差最后一步：手动进入 minio 的 Web UI，创建好 `argo-bucket` 这个 bucket.
直接访问 minio 的 9000 端口（需要使用 nodeport/ingress 等方式暴露此端口）就能进入 Web UI，使用前面提到的 secret `minio` 中的 key/secret 登录，就能创建 bucket.


### [ServiceAccount 配置](https://argoproj.github.io/argo/service-accounts/)

Argo Workflow 依赖于 ServiceAccount 进行验证与授权，而且默认情况下，它使用所在 namespace 的 `default` ServiceAccount 运行 workflow.

可 `default` 这个 ServiceAccount 默认根本没有任何权限！所以 Argo 的 artifacts, outputs, access to secrets 等功能全都会因为权限不足而无法使用！

为此，Argo 的官方文档提供了两个解决方法。

方法一，直接给 default 绑定 `cluster-admin` ClusterRole，给它集群管理员的权限，只要一行命令（但是显然安全性堪忧）： 

```shell
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=<namespace>:default -n <namespace>
```

方法二，官方给出了[Argo Workflow 需要的最小权限的 Role 定义](https://argoproj.github.io/argo/workflow-rbac/)，方便起见我将它改成一个 ClusterRole:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: argo-workflow-role
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

创建好上面这个最小的 ClusterRole，然后为每个名字空间，跑一下如下命令，给 default 账号绑定这个 clusterrole:

```shell
kubectl create rolebinding default-argo-workflow --clusterrole=argo-workflow-role  --serviceaccount=<namespace>:default -n <namespace>
```

这样就能给 default 账号提供最小的 workflow 运行权限。

或者如果你希望使用别的 ServiceAccount 来运行 workflow，也可以自行创建 ServiceAccount，然后再走上面方法二的流程，但是最后，要记得在 workflow 的 `spec.serviceAccountName` 中设定好 ServiceAccount 名称。


### [Workflow Executors](https://argoproj.github.io/argo/workflow-executors/)

Workflow Executor 是符合特定接口的一个进程(Process)，Argo 可以通过它执行一些动作，如监控 Pod 日志、收集 Artifacts、管理容器生命周期等等...

Workflow Executor 有多种实现，可以通过前面提到的 configmap `workflow-controller-configmap` 的 `containerRuntimeExecutor` 这个参数来选择。

可选项如下：

1. docker(默认): 目前使用范围最广，但是安全性最差。它要求一定要挂载访问 `docker.sock`，因此一定要 root 权限！
2. kubelet: 应用非常少，目前功能也有些欠缺，目前也必须提供 root 权限
3. Kubernetes API (k8sapi): 直接通过调用 k8sapi 实现日志监控、Artifacts 手机等功能，非常安全，但是性能欠佳。
4. Process Namespace Sharing (pns): 安全性比 k8sapi 差一点，因为 Process 对其他所有容器都可见了。但是相对的性能好很多。

在 docker 被 kubernetes 抛弃的当下，如果你已经改用 containerd 做为 kubernetes 运行时，那 argo 将会无法工作，因为它默认使用 docker 作为运行时！

我们建议将 workflow executore 改为 `pns`，兼顾安全性与性能。


## 三、常见问题

### 1. workflow 默认使用 root 账号？

workflow 的流程默认使用 root 账号，如果你的镜像默认使用非 root 账号，而且要修改文件，就很可能遇到 Permission Denined 的问题。

解决方法：通过 Pod Security Context 手动设定容器的 user/group:

- [Workflow Pod Security Context](https://argoproj.github.io/argo/workflow-pod-security-context/)


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

或者也可以通过 `workflow-controller-configmap` 的 `workflowDefaults` 设定默认的 workflow 配置。

### 2. 如何从 hashicorp vault 中读取 secrets?

>参考 [Support to get secrets from Vault](https://github.com/argoproj/argo/issues/3267#issuecomment-650119636)

hashicorp vault 目前可以说是云原生领域最受欢迎的 secrets 管理工具。
我们在生产环境用它做为分布式配置中心，同时在本地 CI/CD 中，也使用它存储相关的敏感信息。

现在迁移到 argo，我们当然希望能够有一个好的方法从 vault 中读取配置。

目前最推荐的方法，是使用 vault 的 vault-agent，将 secrets 以文件的形式注入到 pod 中。

通过 valut-policy - vault-role - k8s-serviceaccount 一系列认证授权配置，可以制定非常细粒度的 secrets 权限规则，而且配置信息阅后即焚，安全性很高。


### 3. 如何在多个名字空间中使用同一个 secrets?

使用 Namespace 对 workflow 进行分类时，遇到的一个常见问题就是，如何在多个名字空间使用 `private-git-creds`/`docker-config`/`minio`/`vault` 等 workflow 必要的 secrets.

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

上面提供的 kyverno 配置，会实时地监控所有 Namespace 变更，一但有新 Namespace 被创建，它就会立即将 `vault` secret 同步到该 Namespace.

或者，使用专门的 secrets/configmap 复制工具：[kubernetes-replicator](https://github.com/mittwald/kubernetes-replicator)

### 4. Argo 对 CR 资源的验证不够严谨，写错了 key 都不报错

待研究


## 参考文档

- [Argo加入CNCF孵化器，一文解析Kubernetes原生工作流](https://www.infoq.cn/article/fFZPvrKtbykg53x03IaH)


视频:

- [How to Multiply the Power of Argo Projects By Using Them Together - Hong Wang](https://www.youtube.com/watch?v=fKiU7txd4RI&list=PLj6h78yzYM2Pn8RxfLh2qrXBDftr6Qjut&index=149)


