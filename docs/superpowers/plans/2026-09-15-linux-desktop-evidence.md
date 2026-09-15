# Linux 桌面系统系列：迁移与证据清单

日期：2026-09-16。此清单是重写前的事实边界，不是对尚未发生的改写、构建或部署的声明。

## 旧稿与 URL 迁移

仓库的 `config.toml` 将 posts 的 permalink 设为
`posts/:contentbasename`；下列「当前 URL」据此及各 bundle 的目录名得出。七个 bundle 都在
`rg --files content/posts/2025` 的结果中，front matter 的 `featuredImage`
指向同 bundle 的封面文件。迁移时保留表中的日期，并把每张封面从列出的 source
path 移到对应的新 bundle。

| 旧 source path                                                            | 当前 URL                                           | 标题                                                        | 保留的日期                  | 封面 source path                                                                     | 直接入站链接 / 处理                                                |
| ------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `content/posts/2025/Q3/linux-desktop-explained/index.md`                  | `/posts/linux-desktop-explained/`                  | Linux 桌面系统故障排查指南（零） - 组件概览                 | `2025-09-09T20:17:33+08:00` | `content/posts/2025/Q3/linux-desktop-explained/featured-image.webp`                  | 未发现站点正文的直接链接；迁移为概览                               |
| `content/posts/2025/Q4/linux-desktop-1-boot-security/index.md`            | `/posts/linux-desktop-1-boot-security/`            | Linux 桌面系统故障排查指南（一） - 系统启动与安全框架       | `2025-10-19T10:17:33+08:00` | `content/posts/2025/Q4/linux-desktop-1-boot-security/featured-image.webp`            | 概览第 72 行的 Markdown 链接；迁移为启动篇                         |
| `content/posts/2025/Q4/linux-desktop-2-systemd-services/index.md`         | `/posts/linux-desktop-2-systemd-services/`         | Linux 桌面系统故障排查指南（二） - systemd 全家桶与服务管理 | `2025-10-19T10:18:33+08:00` | `content/posts/2025/Q4/linux-desktop-2-systemd-services/featured-image.webp`         | 概览第 81 行的 Markdown 链接；迁移为系统基础篇                     |
| `content/posts/2025/Q4/linux-desktop-3-session-graphics/index.md`         | `/posts/linux-desktop-3-session-graphics/`         | Linux 桌面系统故障排查指南（三） - 桌面会话与图形渲染       | `2025-10-19T10:19:33+08:00` | `content/posts/2025/Q4/linux-desktop-3-session-graphics/featured-image.webp`         | 概览第 92 行的 Markdown 链接；迁移为登录会话篇，并从该篇链接图形篇 |
| `content/posts/2025/Q4/linux-desktop-4-multimedia-input/index.md`         | `/posts/linux-desktop-4-multimedia-input/`         | Linux 桌面系统故障排查指南（四） - 多媒体处理与中文支持     | `2025-10-19T10:20:33+08:00` | `content/posts/2025/Q4/linux-desktop-4-multimedia-input/featured-image.webp`         | 概览第 104 行的 Markdown 链接；迁移为音频、字体与输入法篇          |
| `content/posts/2025/Q4/linux-desktop-5-network/index.md`                  | `/posts/linux-desktop-5-network/`                  | Linux 桌面系统故障排查指南（五） - 网络                     | `2025-10-19T10:21:33+08:00` | `content/posts/2025/Q4/linux-desktop-5-network/featured-image.webp`                  | 概览第 114 行的 Markdown 链接；迁移为网络篇                        |
| `content/posts/2025/Q4/linux-desktop-6-shutdown-troubleshooting/index.md` | `/posts/linux-desktop-6-shutdown-troubleshooting/` | Linux 桌面系统故障排查指南（六） - 系统关机与电源管理       | `2025-10-19T10:22:33+08:00` | `content/posts/2025/Q4/linux-desktop-6-shutdown-troubleshooting/featured-image.webp` | 概览第 126 行的 Markdown 链接；迁移为电源篇                        |

九个规范 slug（均带末尾 `/`）及七个精确 alias 映射：

| 新 slug                                    | 旧 URL（若有）                                     |
| ------------------------------------------ | -------------------------------------------------- |
| `/posts/linux-desktop-architecture/`       | `/posts/linux-desktop-explained/`                  |
| `/posts/linux-desktop-boot/`               | `/posts/linux-desktop-1-boot-security/`            |
| `/posts/linux-desktop-system-foundations/` | `/posts/linux-desktop-2-systemd-services/`         |
| `/posts/linux-desktop-login-session/`      | `/posts/linux-desktop-3-session-graphics/`         |
| `/posts/linux-desktop-graphics/`           | 无：新篇                                           |
| `/posts/linux-desktop-app-integration/`    | 无：新篇                                           |
| `/posts/linux-desktop-media-input/`        | `/posts/linux-desktop-4-multimedia-input/`         |
| `/posts/linux-desktop-network/`            | `/posts/linux-desktop-5-network/`                  |
| `/posts/linux-desktop-power/`              | `/posts/linux-desktop-6-shutdown-troubleshooting/` |

映射是一对一，旧 URL 不同时指向多个目标。七篇由旧稿重写而来的目标页必须保留各自原来的日期。新增页面使用实际写作时间，未写入的页面不得预填：

- 图形篇：`2026-09-16T01:14:00+08:00`，Task 7 写作时实际执行 `date --iso-8601=seconds`
  取得；为本地新稿日期，不表示已经部署发布。
- 桌面应用篇：`2026-09-16T01:27:11+08:00`，Task 8 写作时实际执行 `date --iso-8601=seconds`
  取得；为本地新稿日期，不表示已经部署发布。

## Alias 与 front matter 契约

Hugo 的 `aliases` 在构建时会解析为带内容维度前缀的 server-relative
path，默认生成一个带 canonical link 与 meta
refresh 的 HTML 文件。[Hugo URL management: aliases](https://gohugo.io/content-management/urls/#aliases)
本站设定 `defaultContentLanguage = "zh-cn"`，没有启用默认语言子目录。以 Hugo `v0.165.0`
建立的隔离 fixture 使用同一默认语言、语言表、permalink 和
`aliases: ["/posts/linux-desktop-explained/"]`；生成的文件是
`public/posts/linux-desktop-explained/index.html`，目标为
`https://thiscute.world/posts/linux-desktop-architecture/`，不是 `/zh-cn/posts/...`。

因此，每个有旧址的 descendant 都在其 YAML front matter 写 site-relative
alias，格式如下。不得把 alias 写进旧稿，也不得同时保留旧稿作为规范内容。旧 bundle 被替换或移走后，旧 URL 只能由新目标页生成的 alias 文件抵达其规范 URL。

```yaml
categories: ["tech"]
series: ["Linux 桌面系统"]
aliases: ["/posts/linux-desktop-explained/"]
```

实际写入时，alias 值按上面的七项映射替换；`categories` 和 `series`
保持不变。这样现有年度总结使用的系列页仍可用。

## 托管与构建检查

`vercel.json` 只固定 Hugo
`0.165.0`，没有本系列的 rewrite 或 redirect 规则；Vercel 需要部署 Hugo 输出的实体 alias 文件。GitHub
Actions 同样以 Hugo `0.165.0` 构建，并把 `./public` 发布到 GitHub
Pages；工作流没有为这些路径另设服务器端跳转。因此，按当前配置，Hugo 的 client-side alias
HTML 是两个静态托管目标共用的跳转机制，不需要额外规则。

在七个 descendant 都存在后，执行本地 Hugo 构建，并逐一确认以下内容：

- `public/posts/<legacy-slug>/index.html` 存在，且没有
  `public/zh-cn/posts/<legacy-slug>/index.html`。
- 每个 alias 文件的 canonical link 和 `meta http-equiv="refresh"` 都指向对应的
  `/posts/linux-desktop-<target>/` 规范 URL。
- 七个旧 bundle 不再生成自身的规范页面，旧 URL 没有循环跳转；九个规范 URL 均可生成。

## 全仓文本引用扫描

已以七个 slug、完整系列名和可能的 fragment 形式扫描 Markdown、模板、脚本、配置及静态文本（排除 theme 与生成目录）。没有发现指向这七个旧 URL 的
`#fragment` 链接。

- `content/posts/2025/Q3/linux-desktop-explained/index.md`
  的六个正文导航链接是唯一应改为规范 URL 的站点内容入站链接，见上表。
- 各旧稿自身的 front matter、正文的系列名和收尾语，是待替换内容而非独立入站链接。
- `CHRONICLE.md` 和 `content/history/2025/index.md`
  的「故障排查指南」文字是发布史事实；不要因重写标题而改写。当前扫描没有发现它们包含旧 URL。
- `docs/superpowers/specs/2026-09-15-linux-desktop-series-design.md`
  与既有实施计划中的旧 URL 是开发资料，不是已发布的站内导航；后续计划可更新，但不能把它们误报为读者入口。
- `update_statistics.py` 只按 GA `pagePath` 归一化/合并其既有
  `modified_page_paths`；其中没有本系列路径。后续实现必须使旧路径继续独立统计并标为「旧版文章」，不能把其指标归并到新 URL。`layouts/shortcodes/statistics_trendingposts.html`
  以 `pagePath` 同时作为链接和排序键；`static/_redirects`
  目前只有域名规范化规则，未含本系列规则。

## 本地提交证据（仅候选，已脱敏）

只读取了 `/home/ryan/nix-config`
的 Git 元数据和以下相关差异路径；没有读取 secret 文件、secret
value 或远端。提交信息及配置 diff 是作者记录的线索，不是完整日志、独立复现，不能单独写成「我观察到」或「已经验证」。主机名、设备名、接口名、具体路由表/规则编号、私有地址和任何凭据均不进入后续正文。

| 机制 / 可用案例线索                           | 候选提交                                                                                                                                                     | 已检查的相关路径（泛化）                                   | 可以有限陈述                                                                                                                            | 不可推断                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 启动设备名改为 UUID                           | `0504d0503ba7d62882f47798ff77c2449d2da4ff`（主证据）；`a5295500f14bf9bbf26b48ee4db87e41a9cbe544`（后续存储迁移线索）                                         | 一台机器的挂载与硬件配置；后续磁盘布局、硬件配置和安装文档 | 主提交将启动文件系统的设备名替换为 UUID 路径；后续迁移也涉及声明式文件系统标识与启动资料                                                | UUID 值、机器标识、实际启动日志、失败原因的完整链路或迁移结果                     |
| 自动登录与锁屏                                | `099752e89faf9fb8472ce576bbc1273335a71392`                                                                                                                   | 一台机器的登录管理器配置                                   | 直接启动会话会绕过预期认证边界的配置风险                                                                                                | 用户身份、所有会话的行为或安全结论                                                |
| 登录密码与密钥环同步                          | `d0cd00069d0c9113bb2607921912f3b8f2e23bf6`                                                                                                                   | 通用桌面安全模块                                           | 为 `passwd` 服务启用密钥环 PAM 集成，以处理密码变更后的同步问题                                                                         | 密钥环内容、密码、任何应用凭据或通用发行版默认值                                  |
| portal 启动顺序                               | `495c36693809a0f97205f17b241a5575dbfb3709`                                                                                                                   | 通用 XDG/自动启动模块                                      | 自动启动单元可被安排在 portal stack 之后，以避免竞态                                                                                    | 所有 portal 后端、所有沙盒或每次登录都失败                                        |
| 文档 portal 保存 / 屏幕捕获资料               | `7826934b23ae947eba4dfc98a4a170a0fa8bbd9d`；`20dac3bb848e55e7f146d10c34256e90fb6e9fdb`                                                                       | 沙盒通用模块；通用媒体模块                                 | 有文档 portal 保存修复和屏幕捕获模式的配置/记录线索                                                                                     | 捕获的画面、权限授予结果或某应用的可复现性                                        |
| PipeWire PulseAudio 兼容服务与 Wayland 输入法 | `9d00eb39f94bfa36a744edb1d140320bdc82306f`；`fb0f89d975221f330f2562b11f13faa0f659b79c`；`cdfa33297005f3d29fb38d81898e2dc8547bd0c2`（补充的每机音频预设线索） | 通用桌面 PipeWire 模块；通用 Fcitx5 模块；每机音频预设     | PipeWire 修复移除一个 package override，配置仍保留 ALSA/PulseAudio 兼容选项；Fcitx5 配置启用了 Wayland frontend；音频预设可以按机器声明 | 服务启动日志、确切失败根因、音频设备/音量值、输入设备标识、远程会话拓扑或性能效果 |
| 网卡 carrier、地址/路由与 policy rule         | `4098b0282e656ad3cb878472feda0f571132932c`；`77e31bd4cbe7b7dd7a66fd8484b5446a33e626f1`                                                                       | 集中网络变量；一台机器的网络配置                           | 更换硬件可改变接口名称；短暂 carrier loss 会触发 networkd 重配置，需明确如何对待 foreign policy rules                                   | 任何真实接口名、网卡型号、地址、VPN/TUN 名称、规则优先级或恢复是否普遍成功        |

提交 `77e31bd4`
的正文还描述了恢复后的网络问题，但该描述仍只可作为选择「观察 networkd 重配置和路由变化」案例的依据；文章须由官方文档解释机制，且只报告未来实际运行的安全观察命令。

## 各篇的官方资料起点

以下是写作前已取得或直达的一手资料 URL。它们是资料入口，不表示尚未撰写的段落已经受逐句核验。

| 规范 URL / 篇章    | 官方资料                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| architecture       | [systemd overview](https://www.freedesktop.org/software/systemd/man/latest/systemd.html)、[NixOS manual](https://nixos.org/manual/nixos/stable/)                                                                                                                                                                                                                                                                                                                                   |
| boot               | [systemd-boot](https://www.freedesktop.org/software/systemd/man/latest/systemd-boot.html)、[NixOS boot loader options](https://search.nixos.org/options?query=boot.loader)                                                                                                                                                                                                                                                                                                         |
| system-foundations | [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)（canonical）、[upstream systemd.unit XML](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml)（已读取的上游 fallback）、[journalctl](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)、[udev](https://www.freedesktop.org/software/systemd/man/latest/udev.html)、[D-Bus specification](https://dbus.freedesktop.org/doc/dbus-specification.html) |
| login-session      | [logind.conf](https://www.freedesktop.org/software/systemd/man/latest/logind.conf.html)、[Linux-PAM documentation](https://linux-pam.org/Linux-PAM-html/)                                                                                                                                                                                                                                                                                                                          |
| graphics           | [Wayland protocol documentation](https://wayland.freedesktop.org/docs/html/)、[kernel DRM documentation](https://docs.kernel.org/gpu/drm-uapi.html)                                                                                                                                                                                                                                                                                                                                |
| app-integration    | [XDG Desktop Portal](https://flatpak.github.io/xdg-desktop-portal/docs/)、[portal configuration](https://flatpak.github.io/xdg-desktop-portal/docs/portal-configuration.html)                                                                                                                                                                                                                                                                                                      |
| media-input        | [PipeWire documentation](https://docs.pipewire.org/)、[Fontconfig user documentation](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html)、[Fcitx 5 documentation](https://fcitx-im.org/wiki/Documentation)                                                                                                                                                                                                                                                      |
| network            | [systemd-networkd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd-networkd.service.html)（canonical）、[upstream systemd-networkd.service XML](https://github.com/systemd/systemd/blob/main/man/systemd-networkd.service.xml)（已读取的上游 fallback）、[systemd.network](https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html)、[ip-route](https://man7.org/linux/man-pages/man8/ip-route.8.html)                                |
| power              | [systemd-suspend.service](https://www.freedesktop.org/software/systemd/man/latest/systemd-suspend.service.html)（canonical）、[upstream systemd-suspend.service XML](https://github.com/systemd/systemd/blob/main/man/systemd-suspend.service.xml)（已读取的上游 fallback）、[systemd-sleep.conf](https://www.freedesktop.org/software/systemd/man/latest/sleep.conf.d.html)                                                                                                       |

The Hugo and XDG portal pages were successfully read online. Direct fetches of several
freedesktop.org systemd manpages returned HTTP 403 in this environment; the matching
upstream-maintained XML sources above were read as a fallback. The canonical URLs remain
recorded, and a specific claim must still be checked against the applicable upstream text
or matching local manpage before use. No Context7 query was used.

## 命令观察清单

Only read-only, non-secret commands were run. Version output establishes command
availability only; it does not establish the machine's boot, session, audio graph, network
topology, or power behavior.

| 命令                                                                                                                                                                                              | 状态与观察                                       | 理由 / 限制                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hugo version`                                                                                                                                                                                    | ran, exit 0: `hugo v0.165.0+extended+withdeploy` | Confirms the actual local Hugo version for later build checks.                                                                                                                                                                                                               |
| `nix --version`                                                                                                                                                                                   | ran, exit 0: `2.34.8`                            | Confirms Nix CLI availability only.                                                                                                                                                                                                                                          |
| `systemctl --version`; `busctl --version`; `bootctl --version`; `loginctl --version`                                                                                                              | ran, all exit 0: systemd `261 (261.1)`           | Safe availability check only; no service/session/boot status was read.                                                                                                                                                                                                       |
| `pw-cli --version`                                                                                                                                                                                | ran, exit 0: PipeWire `1.6.8`                    | Confirms client/library availability, not a running audio graph.                                                                                                                                                                                                             |
| `fc-match --version`                                                                                                                                                                              | ran, exit 0: fontconfig `2.18.2`                 | Confirms fontconfig availability, not installed font inventory.                                                                                                                                                                                                              |
| `ip -V`                                                                                                                                                                                           | ran, exit 0: iproute2 `7.1.0`                    | Corrected a failed `ip --version` attempt (exit 255; unsupported option); no interfaces, routes, addresses or rules were queried.                                                                                                                                            |
| `bootctl status`, `loginctl list-sessions`, `journalctl`, `pw-cli list-objects`, `ip address/route/rule`, screen sharing, suspend/hibernate/shutdown, service start/stop, network reconfiguration | skipped                                          | Would either disclose local identifiers/topology/log material or change availability/state; not appropriate for this inventory. Future articles may use narrowly scoped, redacted, read-only observation only after checking the official command semantics and environment. |

## Pre-handoff self-review

- No secret literal, credential path, UUID, host name, interface name, address, route,
  policy-rule number, or topology detail is present.
- The seven aliases are unique and their targets match the nine-slug table and design
  mapping.
- Historical chronicle/yearly references are explicitly retained as history rather than
  migration links.
- No unsupported first-person observation is asserted: local results are labeled as
  command observations; repository claims are limited to commits/diffs; all other items
  are future verification work.

## 音频、字体与输入法篇的核查补充

Task 9 保留原发布日期与封面，实际修订时间为 `2026-09-16T01:44:50+08:00`。旧 multimedia
URL 由新篇的 alias 生成，规范路径为
`/posts/linux-desktop-media-input/`。屏幕共享主解释仍由桌面应用篇负责。

- 精确检查 `9d00eb39`：标题记录 `pipewire-pulse.service`
  启动失败；diff 仅注释包覆盖，ALSA 与 PulseAudio 兼容选项保留。没有启动日志或恢复测试。
- 精确检查 `fb0f89d9`：已经启用 Fcitx 5 的 Home Manager 配置增加
  `fcitx5.waylandFrontend = true;`。没有某个应用的失败或恢复记录。文中另以 Home Manager
  26.05 源码解释当前选项实现，不用当前实现倒推历史生成文件。
- `wpctl status`
  实际运行，退出 2，提示连接失败与权限拒绝；没有取得设备图，未发布原始设备描述。
- 三个 `fc-match` 查询实际运行，退出 0。`sans` 与 `sans-serif:lang=zh-cn` 返回
  `Source Sans 3`，`monospace:lang=zh-cn` 返回
  `Maple Mono NF CN`。这不证明实际字符回退和渲染结果；未遍历字体清单。
- [Fcitx 上游 remote.cpp](https://github.com/fcitx/fcitx5/blob/master/src/tools/remote.cpp)
  表明 `-n` 单独使用可能触发 D-Bus 激活，因此练习采用
  `--check -n`。本机帮助与带保护的查询均异常退出，未取得输入法名称；没有启动、切换、重载或停止输入法。
- fontconfig 旧 freedesktop URL 被拒绝，改用可读的
  [项目文档站](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)。text-input-v3 的 freedesktop 托管原文不可读，正文明确标记使用 XML 镜像，并另查 Fcitx 官方输入法侧实现。
- Hugo 0.165.0 隔离构建、旧址 canonical/meta
  refresh、规范页与封面字节一致性已核对；已有图形、应用、登录会话篇链接可达。网络篇目标等待 Task
  10，完整导航检查仍归 Task 12。

## 网络篇的核查补充

Task 10 保留原发布日期 `2025-10-19T10:21:33+08:00` 与封面字节，实际修订时间为
`2026-09-16T01:59:13+08:00`。规范路径为 `/posts/linux-desktop-network/`，旧 network
URL 由新篇的 alias 生成。

- `4098b028` 的精确差异只替换一个接口变量的值，没有恢复结果；不公开接口名。
- `77e31bd4`
  的提交与配置注释记录 S3 恢复时 carrier 变化、networkd 重配置及外部 VPN/TUN 策略规则丢失的解释。差异增加
  `ManageForeignRoutingPolicyRules = false` 与
  `IgnoreCarrierLoss = "10s"`，分别调整规则清理边界与短暂断链处理时间。没有路由快照或独立恢复验证。
- 已先查 Linux 网络运行状态与 TUN/TAP 文档、iproute2 手册、systemd 上游 XML、nftables 官方手册、NixOS 文档及 26.05 模块、Arch 提供的 networkd/iwd 手册。freedesktop 手册页被拒绝或超时，Arch
  Wiki 返回反爬页面，改用上述一手来源；未消耗 Context7。
- `ip -brief link`、`ip -brief address`、IPv4/IPv6 的 `rule show` 与
  `route show table all`、`ip route get 1.1.1.1`
  均实际运行，退出 1，权限拒绝。预先设计了进程内输出脱敏，没有接口、地址、规则或拓扑进入报告。最后一条仅查询路由，不发包。
- 没有可用的 `nft`；`systemctl is-active systemd-resolved.service`
  也被权限拒绝，未能确认服务正在运行，因此未继续调用
  `resolvectl status`。未实际查询 DNS、抓包或向第三方发起连通性测试。
- Hugo 0.165.0 隔离构建退出 0；已检查规范页、旧址 canonical/meta
  refresh、原日期、封面字节与可用站内链接。电源篇仍待 Task 11，完整导航检查归 Task
  12。没有网络重配、防火墙修改、挂起、服务停启或远端写入。
