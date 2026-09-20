# Linux 桌面系统系列下架与迁移设计

## 目标

将 PR #53 中的九篇新版 Linux 桌面文章迁入 `/home/ryan/codes/learn-tlpi`
作为独立学习资料，同时从博客中彻底移除新旧文章、站内入口、历史引用和统计记录。

迁移完成后：

- `learn-tlpi/linux-desktop/` 保存九篇新版文章，按编号排列，可脱离 Hugo 阅读；
- 博客不再生成新旧文章页面、系列页或旧 URL 跳转页；
- Google Analytics 的历史数据不会让这些已下架 URL 重新出现在站点统计中；
- 博客中的文章数量、年度记录和站内链接与下架后的状态一致。

## 来源与目标

唯一迁移来源是 PR #53 分支 `codex/linux-desktop-rewrite` 中的九篇新版文章：

1. 系统全景与阅读路径
2. 从固件到根文件系统
3. 系统服务、设备与通信
4. 登录、身份与用户会话
5. 显示、输入与图形渲染
6. 桌面应用、portal 与沙盒
7. 音频、字体与输入法
8. 网络如何到达应用
9. 挂起、恢复与关机

七篇旧文章只从博客中删除，不迁入目标仓库。新版已经吸收旧文中仍有价值的内容，目标仓库不再保存重复版本。

目标目录为：

```text
learn-tlpi/
└── linux-desktop/
    ├── README.md
    ├── 01-architecture.md
    ├── 02-boot.md
    ├── 03-system-foundations.md
    ├── 04-login-session.md
    ├── 05-graphics.md
    ├── 06-app-integration.md
    ├── 07-media-input.md
    ├── 08-network.md
    ├── 09-power.md
    └── images/
        └── featured-image.webp
```

九篇文章使用同一张封面时只保存一份。若实际图片内容不同，则按文章编号分别命名，不做有损合并。

## Markdown 转换

目标仓库中的文章使用普通 Markdown，不保留 Hugo frontmatter。转换规则如下：

- frontmatter 的 `title` 转为一级标题；
- 保留正文、命令、选取后的输出、表格、Mermaid、ASCII 图和外部资料链接；
- 移除博客专属的 AI 创作声明、系列 taxonomy、aliases、评论、搜索、封面和页面渲染配置；
- `/posts/linux-desktop-.../` 形式的系列内链接改成相对 Markdown 链接；
- 返回系列首页的链接改为 `README.md`，前后篇链接改为对应编号文件；
- 保留作者 `nix-config` 的公开链接和正文中自包含的配置摘录；
- 不新增依赖 Hugo shortcode 的语法。

`linux-desktop/README.md` 说明系列目标、阅读顺序，并列出九篇文章。根目录
`learn-tlpi/README.md` 增加一个简短入口，将该目录与 TLPI 习题、内核笔记并列。

## 博客删除范围

在 PR
#53 分支中删除九篇新版文章的 Markdown 和图片资源，并确认七篇旧文章目录不在最终树中。删除以下仅服务于本次重写的内部资料：

- `docs/superpowers/specs/2026-09-15-linux-desktop-series-design.md`
- Linux desktop 重写、证据和实操实验相关的 `docs/superpowers/plans/` 文件
- 其他只描述本系列重写过程、最终不再有实现对象的文档

从博客内容中移除或改写指向该系列的入口：

- `CHRONICLE.md`
- `content/history/2025/index.md`
- `content/posts/2025/Q4/2025-summary/index.md`
- 其他由全仓搜索发现的系列页、文章 URL 或失效链接

历史文字不伪造事实。若一段话只是记录当年曾写过相关内容，则改成不再链接到已下架页面的简短描述；若整句仅用于推荐或导航该系列，则直接删除。

不为旧 URL 创建 410、占位文章或重定向。下架后这些地址由站点正常返回 404。

## 统计处理

`update_statistics.py`
增加明确的已下架路径集合，只包含七个已经发布过的旧 URL。九个新版 URL 从未发布，没有 GA 历史数据，不加入排除集合。`process_data()`
在合并和质量过滤前跳过旧 URL，避免后续 GA 拉取把历史访问记录重新写入站点数据。

现有 `LEGACY_POST_PATHS` 及 `legacyPage` 标记不再需要，删除对应实现。测试改为覆盖：

- 带或不带结尾斜杠的已下架 URL 都会被规范化后排除；
- 七个旧 URL 均不会出现在 `process_data()` 的结果中；
- 不相关页面的合并、标题替换与过滤行为保持不变。

同时清理：

- `data/website_statistics.json` 中已有的旧文章记录；
- `data/posts_count.json` 中受文章删除影响的计数。

文章计数优先使用项目现有的 `process_posts.py`
重新生成；若脚本还执行其他更新，则先检查 diff，只提交本次删除导致的变化。

## Git 与远端边界

两个仓库分别形成一个逻辑提交：

- `learn-tlpi`：新增独立 Linux desktop 学习资料；
- `thiscute.world`：下架文章并清理统计、引用和重写文档。

博客提交推送到现有 PR #53 的 `codex/linux-desktop-rewrite` 分支。`learn-tlpi`
只创建本地提交，不推送远端，除非用户另行明确授权。

博客工作区已有的 `assets/jsconfig.json`
修改属于用户，不修改、不暂存，也不让格式化工具覆盖它。

## 验证标准

### `learn-tlpi`

- 九篇 Markdown 文件和目录页存在，编号连续；
- 系列内相对链接和图片引用全部可解析；
- 不残留 Hugo frontmatter、`/posts/linux-desktop-.../` 链接或博客专属配置；
- Mermaid、代码块和 Markdown 格式通过仓库现有 Prettier 配置；
- `git diff --check` 通过。

### `thiscute.world`

- 全仓不再包含新旧文章目录或相关静态资源；
- Hugo production
  build 不再生成七个旧 URL、九个新版 URL、系列 taxonomy 页面或 alias 页面；
- 全仓搜索不存在指向已下架文章的站内链接；
- 统计测试覆盖七个旧路径并通过；
- `data/website_statistics.json` 不包含相关路径，文章计数与内容树一致；
- Prettier、typos、`git diff --check`、项目测试和 Hugo production build 通过；
- staged diff 不包含 `assets/jsconfig.json`。

推送后只读确认 PR
#53 指向新提交并检查 CI 状态。CI 尚未结束时如实报告 pending，不把 pending 当作通过。
