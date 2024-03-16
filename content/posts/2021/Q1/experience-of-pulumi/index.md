---
title: "Pulumi 使用体验 - 基础设施代码化"
date: 2021-01-08T18:51:30+08:00
draft: false

resources:
  - name: "featured-image"
    src: "pulumi.webp"

tags: ["基础设施即代码", "云原生", "Pulumi", "Terraform"]
categories: ["tech"]
series: ["云原生相关"]

# 兼容旧的 Path（单词拼写错误）
aliases:
  - /posts/expirence-of-pulumi/
---

[Pulumi](https://github.com/pulumi/pulumi) 是一个基础设施的自动管理工具，使用
Python/TypeScript/Go/Dotnet 编写好声明式的资源配置，就能实现一键创建/修改/销毁各类资源，这
里的资源可以是：

<!--more-->

- AWS/阿里云等云上的负载均衡、云服务器、TLS 证书、DNS、CDN、OSS、数据库...几乎所有的云上资
  源
- 本地自建的 vSphere/Kubernetes/ProxmoxVE/libvirt 环境中的虚拟机、容器等资源

相比直接调用 AWS/阿里云/Kubernetes 的 API，使用 pulumi 的好处有：

- 声明式配置：你只需要声明你的资源属性就 OK，所有的状态管理、异常处理都由 pulumi 完成。
- 统一的配置方式：提供统一的配置方法，来声明式的配置所有 AWS/阿里云/Kubernetes 资源。
- 声明式配置的可读性更好，更便于维护

试想一下，通过传统的手段去从零搭建一个云上测试环境、或者本地开发环境，需要手工做多少繁琐的
工作。

而依靠 Pulumi 这类「基础设施即代码（Infrastructure as Code, IaC）」的工具，只需要一行命令
就能搭建好一个可复现的云上测试环境或本地开发环境。

比如我们的阿里云测试环境，包括两个 kubernetes 集群、负载均衡、VPC 网络、数据库、云监控告警
/日志告警、RAM账号权限体系等等，是一个比较复杂的体系。

人工去配置这么多东西，想要复现是很困难的，非常繁琐而且容易出错。

但是使用 pulumi，只需要一行命令，就能创建并配置好这五花八门一大堆的玩意儿。销毁整个测试环
境也只需要一行命令。

**实际使用体验**：我们使用 Pulumi 自动化了阿里云测试环境搭建 95%+ 的操作，这个比例随着阿里
云的 pulumi provider 的完善，还可以进一步提高！

## Pulumi vs Terraform vs CloudFormation

先介绍下 CloudFormation，它是 AWS 提供的一个 IaC 工具， 它使用 json/yaml 编写声明式配置文
件，然后完全在 AWS 云上进行资源的创建、管理、销毁。其所创建的资源跟 CloudFormation Task 同
生命周期，因此删除该 CloudFormation Task 就会自动销毁所有相关资源。因此它的好处应该是可以
完全在云上运行，本地客户端只是一个提交配置的工具。而缺点则是只能在 AWS 上使用。

而在通用的「基础设施即代码」领域，有一个工具比 Pulumi 更流行，它就是
[Terraform](https://www.terraform.io/).

实际上我们一开始使用的也是 Terraform，但是后来使用 Pulumi 完全重写了一遍。

主要原因是，Pulumi 解决了 Terraform 配置的一个痛点：配置语法太过简单，导致配置繁琐。而且还
要额外学习一门 DSL - HCL

Terraform 虽然应用广泛，但是它默认使用的 HCL 语言太简单，表现力不够强。这就导致在一些场景
下使用 Terraform，会出现大量的重复配置。

一个典型的场景是「批量创建资源，动态生成资源参数」。比如批量创建一批名称类似的 ECS 服务器
/VPC交换机。如果使用 terraform，就会出现大量的重复配置。

改用 terraform 提供的 module 能在一定程度上实现配置的复用，但是它还是解决不了问题。要使用
module，你需要付出时间去学习 module 的概念，为了拼接参数，你还需要学习 HCL 的一些高级用
法。

但是付出了这么多，最后写出的 module 还是不够灵活——它被 HCL 局限住了。

为了实现如此的参数化动态化，我们不得不引入 Python 等其他编程语言。于是构建流程就变成了：

1. 借助 Python 等其他语言先生成出 HCL 配置
2. 通过 `terraform` 命令行进行 plan 与 apply
3. 通过 Python 代码解析 `terraform.tfstat`，获取 apply 结果，再进行进一步操作。

这显然非常繁琐，主要困难就在于 Python 和 Terraform 之间的交互。

进一步思考，**既然其他编程语言如 Python/Go 的引入不可避免，那是不是能使用它们彻底替代掉
HCL 呢？能不能直接使用 Python/Go 编写配置**？如果 Terraform 原生就支持 Python/Go 来编写配
置，那就不存在交互问题了。

相比于使用领域特定语言 HCL，使用通用编程语言编写配置，好处有：

1. Python/Go/TypeScript 等通用的编程语言，也支持 Yaml 这样方便自动化生成的配置语言，能满足
   你的一切需求。
2. 作为一个开发人员/DevOps，你应该对 Python/Go 等语言相当熟悉，可以直接利用上已有的经验。
3. 更方便测试：可以使用各编程语言中流行的测试框架来测试 pulumi 配置！

于是 Pulumi 横空出世。

> 另一个和 Pulumi 功能类似的工具，是刚出炉没多久的
> [terraform-cdk](https://github.com/hashicorp/terraform-cdk)，但是目前它还很不成熟。

## Pulumi 特点介绍

4. 原生支持通过 Python/Go/TypeScript/Dotnet 等语言编写配置，也就完全解决了上述的 terraform
   和 python 的交互问题。
5. pulumi 是目前最流行的 真-IaaS 工具，对各语言的支持都很成熟。
6. 兼容 terraform 的所有 provider，只是需要自行使用
   [pulumi-tf-provider-boilerplate](https://github.com/pulumi/pulumi-tf-provider-boilerplate)
   重新打包，有些麻烦。
   1. pulumi 官方的 provider 几乎全都是封装的 terraform provider，包括
      aws/azure/alicloud，目前只发现 kubernetes 是原生的（独苗啊）。
7. 状态管理和 secrets 管理有如下几种选择：
   1. 使用 app.pulumi.com（默认）:免费版提供 stack 历史管理，可以看到所有的历史记录。另外
      还提供一个资源关系的可视化面板。总之很方便，但是多人合作就需要收费。
   2. 本地文件存储：`pulumi login file:///app/data`
   3. [云端对象存储](https://www.pulumi.com/docs/intro/concepts/state/#logging-into-the-aws-s3-backend)，
      支持 s3 等对象存储协议，因此可以使用 AWS 或者本地的 MinIO 来做 Backend.
      - `pulumi login 's3://<bucket-path>?endpoint=my.minio.local:8080&disableSSL=true&s3ForcePathStyle=true'`
      - minio/aws 的 credential 可以通过 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY` 两
        个环境变量设置。另外即使是使用 MinIO，`AWS_REGION` 这个没啥用的环境变量也必须设
        置！否则会报错。
   4. [gitlab 13 支持 Terraform HTTP State 协议](https://github.com/pulumi/pulumi/issues/4727)，
      等这个 pr 合并，pulumi 也能以 gitlab 为 backend 了。
   5. 使用 pulumi 企业版（自建服务）：比 app.pulumi.com 提供更多的特性，但是显然是收费
      的。。

总之，非常香，强烈推荐各位 DevOps 试用。

---

> 以下内容是我对 pulumi 的一些思考，以及使用 pulumi 遇到的各种问题+解决方法，适合对 pulumi
> 有一定了解的同学阅读。

> 如果你刚接触 Pulumi 而且有兴趣学习，建议先移步
> [pulumi get started](https://www.pulumi.com/docs/get-started/install/) 入个门，再接着看
> 下面的内容。

## 使用建议

1. **建议查看对应的 terraform provider 文档：pulumi 的 provider 基本都是封装的 terraform
   版本，而且文档是自动生成的，比（简）较（直）难（一）看（坨）懂（shi），examples 也
   少**。
2. stack: pulumi 官方提供了两种 stack 用
   法：[「单体」和「微-stack」](https://www.pulumi.com/docs/intro/concepts/organizing-stacks-projects/)
   1. 单体: one stack rule them all，通过 stack 参数来控制步骤。stack 用来区分环境 dev/pro
      等。
   2. 微-stack: 每一个 stack 是一个步骤，所有 stack 组成一个完整的项目。
   3. 实际使用中，我发现「微-stack」模式需要使用到 pulumi 的 inter-stack dependencies，报
      一堆的错，而且不够灵活。因此目前更推荐「单体」模式。

我们最近使用 pulumi 完全重写了以前用 terraform 编写的云上配置，简化了很多繁琐的配置，也降
低了我们 Python 运维代码和 terraform 之间的交互难度。另外我们还充分利用上了 Python 的类型
检查和语法检查，很多错误 IDE 都能直接给出提示，强化了配置的一致性和可维护性。

不过由于阿里云 provider 暂时还：

1. 不支持管理 ASM 服务网格、DTS 数据传输等资源
2. OSS 等产品的部分参数也暂时不支持配置（比如 OSS 不支持配置图片样式、ElasticSearch 暂时不
   支持自动创建 7.x 版本）
3. 不支持创建 ElasticSearch 7.x

这些问题，导致我们仍然有部分配置需要手动处理，另外一些耗时长的资源，需要单独去创建。因此还
不能实现完全的「一键」。

## 常见问题

### 1. `Output` 的用法

1. pulumi 通过资源之间的属性引用（`Output[str]`）来确定依赖关系，如果你通过自定义的属性
   (`str`)解耦了资源依赖，会导致资源创建顺序错误而创建失败。
2. `Output[str]` 是一个异步属性，类似 Future，不能被用在 pulumi 参数之外的地方！
3. `Output[str]` 提供两种方法能直接对 `Output[str]` 进行一些操作：
   1. `Output.concat("http://", domain, "/", path)`: 此方法将 str 与 `Output[str]` 拼接起
      来，返回一个新的 `Output[str]` 对象，可用做 pulumi 属性。
   2. `domain.apply(lambda it: print(it))`: `Output[str]` 的 `apply` 方法接收一个函数。在
      异步获取到数据后，pulumi 会调用这个函数，把具体的数据作为参数传入。
      - 另外 `apply` 也会将传入函数的返回值包装成 `Output` 类型返回出来。
      - 可用于：在获取到数据后，将数据打印出来/发送到邮箱/调用某个 API 上传数据等等。
   3. `Output.all(output1, output2, ...).apply(lambda it: print(it))` 可用于将多个
      `output` 值，拼接成一个 `Output` 类型，其内部的 raw 值为一个 tuple 对象
      `(str1, str2, ...)`.
      1. 官方举
         例：`connection_string = Output.all(sql_server.name, database.name).apply(lambda args: f"Server=tcp:{args[0]}.database.windows.net;initial catalog={args[1]}...")`

### 2. 如何使用多个云账号/多个 k8s 集群？

默认情况下 pulumi 使用默认的 provider，但是 pulumi 所有的资源都有一个额外的 `opts` 参数，
可用于设定其他 provider。

通过这个 `opts`，我们可以实现在一个 pulumi 项目中，使用多个云账号，或者管理多个 k8s 集群。

示例：

```python
from pulumi import get_stack, ResourceOptions, StackReference
from pulumi_alicloud import Provider, oss

# 自定义 provider，key/secret 通过参数设定，而不是从默认的环境变量读取。
# 可以自定义很多个 providers
provider = pulumi_alicloud.Provider(
   "custom-alicloud-provider",
   region="cn-hangzhou",
   access_key="xxx",
   secret_key="jjj",
)

# 通过 opts，让 pulumi 使用自定义的 provider（替换掉默认的）
bucket = oss.Bucket(..., opts=ResourceOptions(provider=provider))
```

### 3. inter-stack 属性传递

> 这东西还没搞透，待研究。

多个 stack 之间要互相传递参数，需要通过 `pulumi.export` 导出属性，通过 `stack.require_xxx`
获取属性。

从另一个 stack 读取属性的示例：

```python
from pulumi import StackReference

cfg = pulumi.Config()
stack_name = pulumi.get_stack()  # stack 名称
project = pulumi.get_project()
infra = StackReference(f"ryan4yin/{project}/{stack_name}")

# 这个属性在上一个 stack 中被 export 出来
vpc_id = infra.require("resources.vpc.id")
```

### 4. `pulumi up` 被中断，或者对资源做了手动修改，会发生什么？

1. 强行中断 `pulumi up`，会导致资源进入 `pending` 状态，必须手动修复。
   1. 修复方法：`pulumi stack export`，删除 pending 资源，再 `pulumi stack import`
2. 手动删除了云上资源，或者修改了一些对资源管理无影响的参数，对 `pulumi` 没有影响，它能正
   确检测到这种情况。
   1. 可以通过 `pulumi refresh` 手动从云上拉取最新的资源状态。
3. 手动更改了资源之间的依赖关系（比如绑定 EIP 之类的），很可能导致 pulumi 无法正确管理资源
   之间的依赖。
   - 这种情况必须先手动还原依赖关系（或者把相关资源全部手动删除掉），然后才能继续使用
     pulumi。

### 5. 如何手动声明资源间的依赖关系？

有时候因为一些问题（比如 pulumi provider 功能缺失，使用了 restful api 实现部分功
能），pulumi 可能无法识别到某些资源之间的依赖关系。

这时可以为资源添加 `dependsOn` 属性，这个属性能显式地声明依赖关系。

### 6. 如何导入已经存在的资源？

如果你司不是一开始就使用了 pulumi 这类工具，那通常绝大部分云上资源都是手动管理、或者由其他
工具自动化管理的，该如何将它们纳入 pulumi 管辖呢？

官方有提供一篇相关文档
[Importing Infrastructure](https://www.pulumi.com/docs/guides/adopting/import/).

文档有提到两种资源导入的方法，导入成功后都会自动生成资源的状态，以及对应的 pulumi 代码。第
一种是使用 `pulumi import` 命令，第二种是在代码中使用 `import` 参数。

除此之外，社区还有几个其他资源导入工具（reverse IaC）值得研究：

- [former2](https://github.com/iann0036/former2): 为已有的 AWS 资源生成
  terraform/pulumi/cloudformation 等配置，但是不支持生成 tfstate 状态
- [terraformer](https://github.com/GoogleCloudPlatform/terraformer): 为已有的
  AWS/GCP/Azure/Alicloud/DigitalOcean 等多种云资源生成 terraform 配置以及 tfstate 状态
- [terracognita](https://github.com/cycloidio/terracognita): 功能跟 terraformer 一样，都支
  持生成 terraform 配置以及 tfstate 状态，但是它支持 AWS/GCP/Azure 三朵云
- [pulumi-terraform](https://github.com/pulumi/pulumi-terraform): 这个 provider 使你可以在
  pulumi 项目里使用 tfstate 状态文件
- [tf2pulumi](https://github.com/pulumi/tf2pulumi): 将 terraform 配置转换为 pulumi
  typescript 配置

#### 6.1 通过 pulumi import 命令导入资源

使用 `pulumi import` 命令导入资源的好处是，不需要为每个资源手写代码，此命令会**自动生成资
源的 stack state 与配置代码**。

使用此命令导入的资源，默认会启用删除保护，你可通过参数 `--protect=false` 来关闭删除保护。

资源名称可通过命令行参数，或者 Json 文件来指定。

下面我们演示一个导入一个 s3 bucket 的流程：

```shell
# 导入一个名为 test-sre 的 s3 bucket，资源 ID 为 p-test-sre
$ pulumi import aws:s3/bucket:Bucket p-test-sre test-sre
......
Do you want to perform this import? yes
Importing (dev):
     Type                 Name             Status
 +   pulumi:pulumi:Stack  pulumi-test-dev  created
 =   └─ aws:s3:Bucket     p-test-sre       imported

Resources:
    + 1 created
    = 1 imported
    2 changes

Duration: 8s

Please copy the following code into your Pulumi application. Not doing so
will cause Pulumi to report that an update will happen on the next update command.

Please note that the imported resources are marked as protected. To destroy them
you will need to remove the `protect` option and run `pulumi update` *before*
the destroy will take effect.

import pulumi
import pulumi_aws as aws

p_test_sre = aws.s3.Bucket("p-test-sre",
    arn="arn:aws:s3:::test-sre",
    bucket="test-sre",
    hosted_zone_id="ZZBBCC332211KK",
    request_payer="BucketOwner",
    tags={
        "Name": "test-sre",
        "Team": "Platform",
    },
    opts=pulumi.ResourceOptions(protect=True))
```

能看到它会自动导入对应资源的 state，并同时打印出对应的 python 代码，要求我们手动将代码复制
粘贴到项目中。而且代码会自带 arn/hosted_zone_id/protect 等属性，说明这个资源实际上是无法像
普通 pulumi 资源一样，通过 `pulumi up`/`pulumi destroy` 自动创建销毁的。要通过 pulumi 删除
该资源，需要首先解除删除保护，然后将对应的代码片段删除掉，最后执行 `pulumi up`。

也可通过 json 来批量导入资源，首先编写一个 json 资源清单：

```
{
	"resources": [{
			"type": "aws:s3/bucket:Bucket",
			"name": "s3-bucket_xxx-debug",
			"id": "xxx-debug"
		},
		{
			"type": "aws:s3/accessPoint:AccessPoint",
			"name": "s3-accesspoint_xxx-debug",
			"id": "112233445566:xxx-debug"
		}
	]
}
```

然后执行如下命令批量导入资源：

```shell
$ pulumi import -f test-resources.json
......
Do you want to perform this import? yes
Importing (dev):
     Type                   Name                             Status
     pulumi:pulumi:Stack    pulumi-test-dev
 =   ├─ aws:s3:AccessPoint  s3-accesspoint_xxx-debug  imported
 =   └─ aws:s3:Bucket       s3-bucket_xxx-debug       imported

Resources:
    = 2 imported
    2 unchanged

Duration: 8s

Please copy the following code into your Pulumi application. Not doing so
will cause Pulumi to report that an update will happen on the next update command.

Please note that the imported resources are marked as protected. To destroy them
you will need to remove the `protect` option and run `pulumi update` *before*
the destroy will take effect.

import pulumi
import pulumi_aws as aws

s3_bucket_snappea_dl_debug = aws.s3.Bucket("s3-bucket_xxx-debug",
    arn="arn:aws:s3:::xxx-debug",
    bucket="xxx-debug",
    hosted_zone_id="ZZBBCC332211KK",
    request_payer="BucketOwner",
    tags={
        "Name": "xxx-debug",
        "Team": "Xxx",
    },
    opts=pulumi.ResourceOptions(protect=True))
s3_accesspoint_snappea_dl_debug = aws.s3.AccessPoint("s3-accesspoint_xxx-debug",
    account_id="112233445566",
    bucket="xxx-debug",
    name="xxx-debug",
    public_access_block_configuration=aws.s3.AccessPointPublicAccessBlockConfigurationArgs(
        block_public_acls=False,
        block_public_policy=False,
        ignore_public_acls=False,
        restrict_public_buckets=False,
    ),
    opts=pulumi.ResourceOptions(protect=True))
```

能看到同样的生成出了两个资源的 stack 状态，以及对应的代码。

#### 6.2 通过代码导入资源

通过代码导入资源，需要你手工为每个资源编写代码，并且确保代码的所有参数与资源本身的状态完全
一致。

因此可以看到这种导入方式很不灵活，通常不推荐使用，`pulumi import` 自动生成代码它不香么
emmmm

大概的流程如下，首先编写一个资源的配置代码，并将其标注为 `import`:

```python
p_test_sre = aws.s3.Bucket("p-test-sre",
    bucket="test-sre",
    tags={
        "Name": "test-sre",
        "Team": "xxx",  # 这里我故意写错了，pulumi 会检测到这里有问题，提示导入将失败
    },
    opts=pulumi.ResourceOptions(
       protect=True,
       import_="test-sre",  # 标记需要导入此资源，导入成功后需要手工删除此标记。
))
```

然后执行 `pulumi up` 就会开始导入此资源，如果设定的参数与资源状态不匹配，会有对应的错误提
示：

```
❯ pulumi up
Previewing update (dev):
     Type                 Name             Plan       Info
     pulumi:pulumi:Stack  pulumi-test-dev
 =   └─ aws:s3:Bucket     p-test-sre       import     [diff: -tags]; 1 warning

Diagnostics:
  aws:s3:Bucket (p-test-sre):
    warning: inputs to import do not match the existing resource; importing this resource will fail
```

在确保参数完全一致后，导入就会成功，导入成功后，需要手动删除代码中的 `import` 这个标记。

### 6.3 如何从 pulumi 中移除被导入的资源

格式如下：

```shell
pulumi state delete <resource URN> [flags]
```

比如要删除先前导入的 `arn:aws:s3:::test-sre`，首先删除对应的代码，然后执行
`pulumi preview`，就会报错并打印出对应的资源 urn:

```
$ pulumi preview
...
Diagnostics:
  aws:s3:Bucket (p-test-sre):
    error: Preview failed: unable to delete resource "urn:pulumi:dev::pulumi-test::aws:s3/bucket:Bucket::p-test-sre"
    as it is currently marked for protection. To unprotect the resource, either remove the `protect` flag from the resource in your Pulumi program and run `pulumi up` or use the command:
    `pulumi state unprotect 'urn:pulumi:dev::pulumi-test::aws:s3/bucket:Bucket::p-test-sre'`
```

接下来使用如下命令强制从 state 文件中移除此资源（仅修改配置，对实际资源无任何影响）：

```shell
pulumi state delete urn:pulumi:dev::pulumi-test::aws:s3/bucket:Bucket::p-test-sre --force
```

### 5. pulumi-kubernetes？

pulumi-kubernetes 是一条龙服务：

1. 在 yaml 配置生成这一步，它能结合/替代掉 helm/kustomize，或者你高度自定义的 Python 脚
   本。
2. 在 yaml 部署这一步，它能替代掉 argo-cd 这类 gitops 工具。
3. 强大的状态管理，argo-cd 也有状态管理，可以对比看看。

也可以仅通过 kubernetes_pulumi 生成 yaml，再通过 argo-cd 部署，这样 pulumi_kubernetes 就仅
用来简化 yaml 的编写，仍然通过 gitops 工具/kubectl 来部署。

使用 pulumi-kubernetes 写配置，要警惕逻辑和数据的混合程度。因为 kubernetes 的配置复杂度比
较高，如果动态配置比较多，很容易就会写出难以维护的 python 代码来。

渲染 yaml 的示例：

```python
from pulumi import get_stack, ResourceOptions, StackReference
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import (
	ContainerArgs,
	ContainerPortArgs,
	EnvVarArgs,
	PodSpecArgs,
	PodTemplateSpecArgs,
	ResourceRequirementsArgs,
	Service,
	ServicePortArgs,
	ServiceSpecArgs,
)
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs

provider = Provider(
   "render-yaml",
   render_yaml_to_directory="rendered",
)

deployment = Deployment(
	"redis",
	spec=DeploymentSpecArgs(...),
   opts=ResourceOptions(provider=provider),
)
```

如示例所示，pulumi-kubernetes 的配置是完全结构化的，比 yaml/helm/kustomize 要灵活非常多。

总之它非常灵活，既可以和 helm/kustomize 结合使用，替代掉 argocd/kubectl。也可以和
argocd/kubectl 使用，替代掉 helm/kustomize。

具体怎么使用好？我也还在研究。

### 6. 阿里云资源 replace 报错？

阿里云有部分资源，只能创建删除，不允许修改，比如「资源组」。对这类资源做变更时，pulumi 会
直接报错：「Resources aleardy exists」，这类资源，通常都有一个「force」参数，指示是否强制
修改——即先删除再重建。

### 7. 有些资源属性无法使用 pulumi 配置？

这得看各云服务提供商的支持情况。

比如阿里云很多资源的属性，pulumi 都无法完全配置，因为 alicloud provider 的功能还不够全面。

目前我们生产环境，大概 95%+ 的东西，都可以使用 pulumi 实现自动化配置。而其他 OSS 的高级参
数、新出的 ASM 服务网格、kubernetes 的授权管理、ElasticSearch7 等资源，还是需要手动配置。

这个没办法，只能等阿里云提供支持。

### 8. CI/CD 中如何使 pulumi 将状态保存到文件？

CI/CD 中我们可能会希望 pulumi 将状态保存到本地，避免连接 pulumi 中心服务器。这一方面能加快
速度，另一方面一些临时状态我们可能根本不想存储，可以直接丢弃。

方法：

```shell
# 指定状态文件路径
pulumi login file://<file-path>
# 保存到默认位置: ~/.pulumi/credentials.json
pulumi login --local

# 保存到远程 S3 存储（minio/ceph 或者各类云对象存储服务，都兼容 aws 的 s3 协议）
pulumi login s3://<bucket-path>
```

登录完成后，再进行 `pulumi up` 操作，数据就会直接保存到你设定的路径下。

### 9. 如何估算资源变更导致的成本变化？

目前 pulumi 貌似没有类似的工具，但是 terraform 有一个
[infracost](https://github.com/infracost/infracost) 可以干这个活，值得关注。

## 缺点

### 1. 报错信息不直观

pulumi 和 terraform 都有一个缺点，就是封装层次太高了。

封装的层次很高，优点是方便了我们使用，可以使用很统一很简洁的声明式语法编写配置。而缺点，则
是出了 bug，报错信息往往不够直观，导致问题不好排查。

### 2. 资源状态被破坏时，修复起来非常麻烦

在很多情况下，都可能发生资源状态被破坏的问题：

1. 在创建资源 A，因为参数是已知的，你直接使用了常量而不是 `Output`。这会导致 pulumi 无法识
   别到依赖关系！从而创建失败，或者删除时资源状态被破坏！
1. 有一个 pulumi stack 一次在三台物理机上创建资源。你白天创建资源晚上删除资源，但是某一台
   物理机晚上会关机。这将导致 pulumi 无法查询到这台物理机上的资源状态，这个 pulumi stack
   在晚上就无法使用，它会一直报错！

## 常用 Provider

- [pulumi-alicloud](https://github.com/pulumi/pulumi-alicloud): 管理阿里云资源
- [pulumi-vault](https://github.com/pulumi/pulumi-vault): 我这边用它来快速初始化 vault，创
  建与管理 vault 的所有配置。

## 我创建维护的 Provider

由于 Pulumi 生态还比较小，有些 provider 只有 terraform 才有。

我为了造(方)福(便)大(自)众(己)，创建并维护了两个本地虚拟机相关的 Providers:

- [ryan4yin/pulumi-proxmox](https://github.com/ryan4yin/pulumi-proxmox): 目前只用来自动创
  建 PVE 虚拟机
  - 可以考虑结合 kubespray/kubeadm 快速创建 k8s 集群
- [ryan4yin/pulumi-libvirt](https://github.com/ryan4yin/pulumi-libvirt): 快速创建 kvm 虚拟
  机
  - 可以考虑结合 kubespray/kubeadm 快速创建 k8s 集群
