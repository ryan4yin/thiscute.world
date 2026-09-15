# Linux Desktop Series Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace seven published articles with nine system-learning articles, preserve
old entry points, and keep GA metrics for old and new pages separate.

**Architecture:** Nine semantic post URLs share the existing `tech` category and
`Linux 桌面系统` series. Seven rewritten descendants carry Hugo aliases for their old
URLs, while statistics represent old page visits as distinct legacy entries. Each article
is researched from authoritative online sources and local case history before safe command
checks and prose editing.

**Tech Stack:** Hugo 0.161.1, DoIt theme, YAML front matter, Markdown, Python 3, GA Data
API, Nix dev shell.

**Spec:** `docs/superpowers/specs/2026-09-15-linux-desktop-series-design.md`

## Global Constraints

- Read `/home/ryan/nix-config` only; no secret values, remote writes, deployments, or
  changes to running infrastructure.
- Consult online official/upstream documentation before writing technical claims; use
  Context7 sparingly when search is expensive, then corroborate against original source.
- Run each safe, applicable technical command locally and inspect its result; do not
  execute shutdown, suspend, repair, firewall changes, network changes, or service
  changes.
- Cite technical references adjacent to their claims; do not invent personal observations
  beyond recorded commits/configuration.
- Preserve `tech` category and `Linux 桌面系统` series taxonomy; keep historic chronology
  intact.
- Match author voice using `humanizer`; keep code, metadata, link targets, and factual
  claims under separate technical review.
- Existing canonical URLs become aliases; new canonical URLs are those listed in the spec;
  GA old and new `pagePath` metrics stay separate.
- Use `apply_patch` for authored file changes; verify formatting, links, aliases, and Hugo
  build; follow commit hooks.

---

### Task 1: Lock migration and evidence inventory

**Files:** Create `docs/superpowers/plans/2026-09-15-linux-desktop-evidence.md`; read
existing seven posts, `update_statistics.py`,
`layouts/shortcodes/statistics_trendingposts.html`, `static/_redirects`, and
`/home/ryan/nix-config` Git history.

- [ ] Identify seven exact legacy source paths with
      `rg --files content/posts/2025 | rg 'linux-desktop'`; record their current URL,
      title, date, image, and direct inbound link.
- [ ] Search all textual repository files for seven legacy slugs, title mentions, and
      fragment links; classify history/chronicle references as historical facts, not links
      to rewrite.
- [ ] Use local `git -C /home/ryan/nix-config log` and
      `git show --format=fuller --no-patch` to inventory commit IDs for boot UUID, session
      autologin, keyring/password, portal ordering, screen capture, audio/input,
      NIC/carrier/rules; inspect only relevant changed paths and redact host/private
      details.
- [ ] Write evidence inventory with nine canonical slugs, exact seven old-to-new links,
      candidate commit IDs and factual limits, online-source URLs per chapter,
      observed-command checklist with run/skip reasons.
- [ ] Verify the evidence file has no secrets, placeholders, contradictory URL mappings,
      or unsupported first-person claims; commit it as documentation with hooks.

### Task 2: Check alias mechanism and publication metadata

**Files:** Modify `docs/superpowers/plans/2026-09-15-linux-desktop-evidence.md`; inspect
`config.toml`, `vercel.json`, and `.github/workflows/main.yaml`. The nine pages are
authored in Tasks 3–11, seven under `content/posts/2025/Q*` and two under
`content/posts/2026/Q3`.

**Interfaces:** Old URL aliases are `/posts/linux-desktop-explained/`,
`/posts/linux-desktop-1-boot-security/`, `/posts/linux-desktop-2-systemd-services/`,
`/posts/linux-desktop-3-session-graphics/`, `/posts/linux-desktop-4-multimedia-input/`,
`/posts/linux-desktop-5-network/`, `/posts/linux-desktop-6-shutdown-troubleshooting/`;
each maps respectively to architecture, boot, system-foundations, login-session,
media-input, network, power.

- [ ] Read [Hugo URL management](https://gohugo.io/content-management/urls/#aliases) and
      repository permalinks/languages; record that each descendant's front matter has
      `aliases: ["/posts/<legacy-slug>/"]` and old content must not remain canonical.
- [ ] Inspect both hosting targets as configured, note whether Hugo-generated alias HTML
      works without additional rules and what local output must be checked. Keep series
      taxonomy unchanged so annual-summary series URL remains valid.
- [ ] In the evidence file record seven old front matter dates, seven cover-source bundle
      paths and two actual new publication dates, with YAML field example below. Review
      this independent migration contract and commit only evidence documentation.

```yaml
categories: ["tech"]
series: ["Linux 桌面系统"]
aliases: ["/posts/linux-desktop-explained/"]
```

### Task 3: System overview

**Files:** Create `content/posts/2025/Q3/linux-desktop-architecture/index.md`; replace
overview navigation from `content/posts/2025/Q3/linux-desktop-explained/index.md`.

- [ ] Search current official sources for systemd startup/session, Wayland, portal,
      PipeWire, networking and Hugo URL behavior; write a source ledger for overview
      claims.
- [ ] Build one coherent boot-to-shutdown timeline, nine-chapter navigation using
      canonical URLs, NixOS example boundaries, Arch/other distro distinctions; preserve
      author's personal motivation and AI-assistance disclosure. Move or re-reference the
      original cover and assign the original overview alias; do not keep old canonical
      content.
- [ ] Check nine target slugs and original old-overview alias, inspect language for
      inflated claims and over-formatting with `humanizer`.
- [ ] Build Hugo, check overview navigation against generated canonical output and
      `public/posts/linux-desktop-explained/index.html` alias, commit this standalone
      chapter.

### Task 4: Boot from firmware to root filesystem

**Files:** Create `content/posts/2025/Q4/linux-desktop-boot/index.md` and associated
original cover if applicable; replace original `linux-desktop-1-boot-security/index.md`.

- [ ] Find current official docs for UEFI/boot loader, Linux kernel/initramfs, NixOS boot
      config and Arch boot/initramfs; inspect boot UUID change commit `0504d050` and its
      actual file diff only after sensitivity screening.
- [ ] Write firmware → loader → kernel → initramfs → mounted root → PID 1, with UUID case
      and link ahead to login/PAM chapter. Remove unqualified boot-speed percentages and
      unsafe `fsck` as a default diagnostic.
- [ ] Run safe available local observation commands (for example `uname -r`,
      `findmnt -n -o SOURCE,TARGET /`, `systemd-analyze`, `bootctl status` after assessing
      output sensitivity); log exact run/skip evidence without secret or hardware
      identifiers in article.
- [ ] Hugo build, check boot old alias and new content, style review, commit.

### Task 5: System services, devices and communication

**Files:** Create `content/posts/2025/Q4/linux-desktop-system-foundations/index.md`;
replace `linux-desktop-2-systemd-services/index.md`.

- [ ] Consult current official systemd unit, journald, udev, D-Bus specifications, NixOS
      and Arch system management docs; examine relevant udev or startup history from
      evidence inventory.
- [ ] Explain system/user manager distinction only as required here, unit dependencies,
      journal evidence, udev/device nodes, system/session bus interfaces; move PAM, logind
      application and Flatpak proxy detail to their primary chapters; remove original
      `TODO`.
- [ ] Safely run applicable `systemctl --version`,
      `systemctl list-units --type=service --state=running`,
      `journalctl -b -n 10 --no-pager` only after checking for sensitive logs,
      `udevadm --version`, `busctl --version`; skip commands whose output risks sensitive
      disclosure.
- [ ] Check D-Bus method/property names against current primary sources rather than
      copying printed sample values; Hugo build, style review, commit.

### Task 6: Login, identity and user session

**Files:** Create `content/posts/2025/Q4/linux-desktop-login-session/index.md`; replace
the identity portion of boot article and the session portion of
`linux-desktop-3-session-graphics/index.md`.

- [ ] Research official PAM, polkit, Secret Service/keyring, logind, greetd and
      user-manager docs; inspect commit `d0cd0006` for passwd/keyring and `099752e8` for
      greetd autologin; distinguish commit account from reproduced evidence.
- [ ] Follow greeter → PAM → session/user manager → logind/seat → keyring/polkit, explain
      password/keyring desync and unauthenticated re-login as distinct documented cases;
      link graph chapter.
- [ ] Run safe applicable `loginctl list-sessions`, `systemctl --user show-environment`
      only if output can be redacted (prefer safer `systemctl --user status`),
      `busctl --system list` only after sensitivity review; never test live logouts or
      change authentication.
- [ ] Check old graphics/session alias points to this page and links onwards to graphics;
      Hugo build, style review, commit.

### Task 7: Display, input and graphics rendering

**Files:** Create `content/posts/2026/Q3/linux-desktop-graphics/index.md`; replace
graphics portion of `linux-desktop-3-session-graphics/index.md`.

- [ ] Consult official Wayland protocol, Linux DRM/KMS, Mesa, libinput and Arch Wayland
      docs; verify NixOS compositor implementation against `/home/ryan/nix-config` without
      outputting private config values.
- [ ] Explain device ownership → compositor → client surfaces → rendering → output and
      input events; keep XWayland context only where relevant; use recorded graphics
      compatibility issues if evidence suffices.
- [ ] Run safe local `loginctl show-session` only with explicit local session ID if known,
      `wayland-info` if installed without dumping app/private data, `glxinfo -B` if
      available; record skips.
- [ ] Link to app integration and system foundations; Hugo build, language review, commit.

### Task 8: Applications, portals and sandboxes

**Files:** Create `content/posts/2026/Q3/linux-desktop-app-integration/index.md`; replace
app/portal material from former system services and graphics chapters.

- [ ] Consult xdg-desktop-portal, Flatpak/bubblewrap/xdg-dbus-proxy, Wayland screen-cast,
      desktop-entry specs and NixOS/Arch integration docs; inspect portal startup commit
      `495c3669` and document save commit `7826934b`.
- [ ] Trace desktop entry/autostart → process/user service → session bus → portal backend
      → compositor/PipeWire, distinguishing portal permissions from bus/service
      authorization and preserving evidence limits of local commits.
- [ ] Safely inspect `systemctl --user list-units --type=service`, `busctl --user list`
      after redaction review; do not run sandboxed apps with privileges or mutate portal
      permissions.
- [ ] Check official proxy rule syntax and old TODO removal, Hugo build, style review,
      commit.

### Task 9: Audio, fonts and input methods

**Files:** Create `content/posts/2025/Q4/linux-desktop-media-input/index.md`; replace
`linux-desktop-4-multimedia-input/index.md`.

- [ ] Consult official PipeWire/WirePlumber, fontconfig, fcitx5/Wayland and NixOS/Arch
      docs; inspect recorded audio and input commits (`9d00eb39`, `fb0f89d9`) and choose
      cases with enough recorded evidence.
- [ ] Explain sound source → PipeWire session/routing → sink and font match →
      toolkit/rendering, plus input event → compositor/text-input → fcitx5 → app; keep
      screen-capture primary explanation in app chapter.
- [ ] Run applicable safe commands `wpctl status` only after assessing device names,
      `fc-match sans`, `fc-list : family` only with limited output or `fc-match`
      preferred, `fcitx5-remote -n` if available; record skipped/missing executables.
- [ ] Verify old multimedia URL alias, Hugo build, humanizer review, commit.

### Task 10: Network path to the application

**Files:** Create `content/posts/2025/Q4/linux-desktop-network/index.md`; replace
`linux-desktop-5-network/index.md`.

- [ ] Consult official Linux networking, systemd-networkd, nftables, NixOS/Arch network
      docs; inspect `77e31bd4` and related Clash/TUN history without publishing private
      topology.
- [ ] Trace interface → carrier → addresses → routing rules/default route → DNS → TUN/VPN
      → app; use recorded S3 resume fault as a case, qualified to this host and
      configuration; do not recommend clearing firewall or generic kernel tuning.
- [ ] Run safe applicable `ip -brief link`, `ip route get 1.1.1.1` only if output is
      scrubbed of private IP, `resolvectl status` only if addresses are scrubbed,
      `nft list ruleset` only if output can be safely summarized; no ping to third-party
      network unless necessary and authorized.
- [ ] Link power chapter, check old network alias, Hugo build, style review, commit.

### Task 11: Suspend, resume and shutdown

**Files:** Create `content/posts/2025/Q4/linux-desktop-power/index.md`; replace
`linux-desktop-6-shutdown-troubleshooting/index.md`.

- [ ] Consult current kernel power-management, systemd-logind/sleep/shutdown, NixOS and
      Arch suspend/hibernate docs; distinguish hardware capabilities and
      distribution-specific swap/resume configuration.
- [ ] Explain shutdown cleanup and memory/device/network state across
      suspend/hibernate/resume; link network case and document what its commit proves; cut
      unverified power/time numbers and generic cross-chapter troubleshooting cases.
- [ ] Run safe checks `cat /sys/power/state` only if readable, `cat /sys/power/mem_sleep`
      only if readable, `journalctl -b -u systemd-suspend --no-pager` only after checking
      sensitivity; never test actual power state changes or SysRq.
- [ ] Check old power alias, Hugo build, style review, commit.

### Task 12: GA legacy treatment and final integration

**Files:** Modify `update_statistics.py`,
`layouts/shortcodes/statistics_trendingposts.html`; create
`tests/test_statistics_legacy.py`; update overview/new articles' cross-links, and evidence
file; do not hand-edit `data/website_statistics.json` values.

**Interfaces:** The seven legacy URL-to-new URL pairs in Task 2 are the source of truth.
GA page metrics remain keyed by the `pagePath` of the visited old or new page, not the
redirection target.

- [ ] Write a `unittest` test using the fixture below: one legacy and one canonical
      `pagePath` with different counts remain two rows, and the old row gains a
      `legacyPage` indicator. A separate fixture of `/posts/sql-basic/` and
      `/posts/sql-basics-1/` must still aggregate under the existing unrelated remap.

```python
import unittest
from update_statistics import process_data

def report(rows):
    return {
        "dimensionHeaders": [{"name": "pageTitle"}, {"name": "pagePath"}],
        "metricHeaders": [{"name": "activeUsers"}, {"name": "screenPageViews"},
                          {"name": "userEngagementDuration"}],
        "rows": [{"dimensionValues": [{"value": title}, {"value": path}],
                  "metricValues": [{"value": str(users)}, {"value": str(views)},
                                   {"value": str(seconds)}]}
                 for title, path, users, views, seconds in rows],
    }

class LegacyStatisticsTest(unittest.TestCase):
    def test_legacy_and_current_posts_do_not_merge(self):
        items = process_data(report([
            ("旧版标题", "/posts/linux-desktop-explained/", 6, 8, 180),
            ("新稿标题", "/posts/linux-desktop-architecture/", 7, 10, 210),
        ]))
        by_path = {row["pagePath"]: row for row in items}
        self.assertEqual(len(by_path), 2)
        self.assertEqual(by_path["/posts/linux-desktop-explained/"]["screenPageViews"], 8)
        self.assertTrue(by_path["/posts/linux-desktop-explained/"]["legacyPage"])
        self.assertNotIn("legacyPage", by_path["/posts/linux-desktop-architecture/"])
```

- [ ] Run `python3 -m unittest tests/test_statistics_legacy.py -v` to see the intended
      failure before implementation; use project dev shell if installed dependencies are
      missing, without conventional package installers.
- [ ] Define `LEGACY_POST_PATHS` in `update_statistics.py` as the exact seven paths from
      Task 2; in `process_data` set `p["legacyPage"] = True` for matching pages before
      appending. In `statistics_trendingposts.html` render
      `{{ if $page.legacyPage }}（旧版文章）{{ end }}` after title; keep
      `<a href="{{ $page.pagePath }}">` and do not merge old paths into
      `modified_page_paths`.
- [ ] Re-run `python3 -m unittest tests/test_statistics_legacy.py -v` and
      `python3 -m py_compile update_statistics.py tests/test_statistics_legacy.py`; report
      missing checks or environment limitations.
- [ ] Search repository again for seven old slugs and new title references; update active
      links only, preserve historical narrative. Build Hugo production and confirm legacy
      rank sample reaches new post by alias, nine current URL pages, seven old alias HTML
      files, images, page titles, and all nav URLs.
- [ ] Run available formatter, `git diff --check`, content/source/command evidence audit
      and Hugo build with fresh output; commit coherent GA/link changes after hooks and
      report exact verification plus all skipped unsafe commands.
