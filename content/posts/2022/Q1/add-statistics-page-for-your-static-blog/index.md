---
title: "为你的静态博客添加阅读排行页"
date: 2022-02-13T19:22:19+08:00
draft: true

featuredImage: "website-statistics.webp"
authors: ["ryan4yin"]

tags: ["博客", "Google Analytics", "阅读统计"]
categories: ["tech"]
---

## 前言

前段时间偶然读到了@极客兔兔
的[博客折腾记(七) - Gitalk Plus ](https://geektutu.com/post/blog-experience-7.html)，里面
有一段描述让我意识到，静态博客确实缺少一些访客需要的统计数据跟相关性推荐能力。

> 如果文章旁边的推荐链接显示了阅读量，我很可能会被阅读量最大的那一篇文章吸引，并点进去。如
> 果发现有意思，可能会进入更多的页面。如果每天访问的童鞋有 30% 因为推荐链接显示了阅读量这
> 么做了，人均 PV 自然就能上一个台阶了。

于是说做就做，我就给博客做了一个[「阅读排行」](https://thiscute.world/statistics/)，个人感
觉效果非常棒~ 不仅是方便了访客们，就连我自己也多了很多 insight！

以后有空，也会慢慢将统计数据、相关文档推荐添加到每篇文章的 Page 页，慢慢优化呗~

感觉这样一个「阅读排行」，应该对其他博主们也有些参考价值，所以这里记录下我的实现方法，供各
位参考。

## 大概的流程

本文使用的静态网站生成器是 Hugo，站点分析是使用的 Google Analytics，并没有接入 busuanzi 之
类的其他统计脚本。

「阅读排行」的生成与更新流程是这样的：

- 通过 Python 脚本，从 Google Analytics 拉取我需要的网站统计数据，清洗后保存到一个 json 文
  件中，提交到博客 git 仓库。
- 在 Hugo 中创建一个「阅读排行」页面，通过自定义 shortcodes 将前面获取到的 json 数据渲染成
  html，插入到这个页面中。
- 生成出静态网站并部署。
- 编写一个 GitHub Action，定期（比如 1h）执行上面三个步骤。

主要使用到的技术有：

- Google Analytics API
- Python
- Hugo 自定义 shortcodes
- GitHub Action

如果你使用的是其他网站生成器或者网站统计工具，也大致可以参考这个流程。

## 一、从 Google Analytics 获取数据

首先，请确认你的网站已经接入了 Google Analytics，这个接入方法及流程就请自行搜索了。

这里有一个需要注意的点，Google Analytics 接入网站时，有两个版本可选择，而且分别对应不同的
API：

- 当前默认版本：GA4, Google Analytics 4
  - API: [Google Analytics Data API v1beta][ga4-data-api]
- 旧版本：UA, Universal Analytics
  - API: [Google Analytics Reporting API v4][ua-reporting-api-v4]

我是直接使用默认参数接入的 Google Analytics，也就是 GA4，因此本文会使用 [Google Analytics
Data API v1beta][ga4-data-api] 获取 Google Analytics 数据。

如果你使用的是旧版本 UA，建议参考 [Use Google Analytics to Show Popular Content on Your
Static Blog][hugo-popular-content] 进行操作，或者升级到 GA4.

### 1. 启用 Google API

为了调用 Google API，我们首先需要在 GCP(Google Cloud Platform) 上创建一个 project，并启用
Google Analytics 的 API.

方法建议直接参考官方文档，同样不同的 Google Analytics 版本对应不同的 API：

- GA4: [Google Analytics Data API v1beta][ga4-data-api]
- UA: [Google Analytics Reporting API v4][ua-reporting-api-v4]

### 2. 创建服务账号

创建好服务后，我们应该是到手一个 `client_secrets.json` 文件，这个问题就是我们用于访问
Google API 的身份凭证。

### 3. 授权服务账号查询 Google Analytics 数据的权限

待续

### 4. 使用脚本查询 Google Analytics 数据

<https://github.com/ryan4yin/ryan4yin.space/blob/main/update_statistics.py>

## 二、编写「阅读排行」页

```shell
hugo new statistics/index.md
```

### 1. 编写 shortcodes

自定义的 shortcodes 直接放在项目的 `/layout/shortcodes` 目录下即可，本博客「阅读排行」用到
的 Hugo shortcodes 都在 [Hugo Custom shortcodes][custom-hugo-shortcodes] 这，以
`statistics_` 开头的就是了。

主要用到的语法为 html + go templates，博主比较懒就不详细介绍了，建议直接看 Hugo 文档...

### 2. 使用 shortcodes

语法为 `{{</* xxx */>}}`，可以参考我的用法：

<https://github.com/ryan4yin/ryan4yin.space/blob/main/content/statistics/index.md>

## 三、编写 GitHub Action

同样懒得介绍了，请直接看我的 action 配置：

<https://github.com/ryan4yin/ryan4yin.space/blob/main/.github/workflows/gh-pages.yaml>

## 参考

- [Use Google Analytics to Show Popular Content on Your Static Blog][hugo-popular-content]

[ga4-data-api]: https://developers.google.com/analytics/devguides/reporting/data/v1
[ua-reporting-api-v4]:
  https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
[hugo-popular-content]: https://pakstech.com/blog/hugo-popular-content/
[custom-hugo-shortcodes]:
  https://github.com/ryan4yin/ryan4yin.space/tree/main/layouts/shortcodes
