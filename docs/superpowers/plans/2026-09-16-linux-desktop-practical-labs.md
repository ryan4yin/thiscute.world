# Linux Desktop Practical Labs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the old Linux desktop series' practical learning depth by adding safe,
reproducible observation labs to the rewritten nine-chapter series without restoring
inaccurate, destructive, or server-focused material.

**Architecture:** Keep the current lifecycle-based chapter structure, concept definitions,
diagrams, self-contained cases, and canonical URLs. Add short labs immediately after the
mechanism they verify, using a consistent sequence: question, read-only command, selected
output, fields to inspect, and limits of the conclusion. Commands target generic Linux
first; NixOS and Arch notes explain tool availability without making either distribution
prerequisite knowledge.

**Tech Stack:** Hugo 0.165.0, Markdown, Mermaid, systemd 261.1, Linux 7.2.0, Nix/NixOS,
Arch package references, upstream Linux/freedesktop/systemd documentation.

**Spec:** `docs/superpowers/specs/2026-09-15-linux-desktop-series-design.md`

## Global Constraints

- Primary readers are Linux enthusiasts; NixOS and Arch receive extra configuration notes
  but are not prerequisites.
- Preserve all canonical article URLs, aliases, numbering, `series_weight`, GA migration
  behavior, and legacy redirects.
- Every technical claim must remain grounded in upstream documentation already cited or
  newly verified against upstream documentation.
- Run every safe command locally when possible. Use elevated host access for read-only
  commands when sandbox isolation hides the desktop state.
- Use `nix run` or `nix shell` for missing tools; do not install packages into the system
  profile.
- Never publish secrets, usernames, hostnames, MAC/IP addresses, device serial numbers,
  private paths, complete process lists, complete routing tables, or complete journal
  output.
- Do not include sandbox failures, missing-tool failures, exit-code audit prose, or
  descriptions of the writing process in article bodies.
- Do not restore destructive commands from the old series, including forced poweroff,
  SysRq triggers, writes to `/sys/power`, filesystem repair, service disruption, or live
  configuration mutations.
- Keep the complete AI and verification disclosure only in chapter one; chapters two
  through nine retain the short AI disclosure.
- Preserve the user's unrelated `assets/jsconfig.json` modification and never stage it.

---

### Task 1: Build the old-to-new coverage inventory

**Files:**

- Modify: `docs/superpowers/plans/2026-09-17-linux-desktop-practical-labs.md`
- Reference: legacy articles under
  `origin/main:content/posts/2025/Q3/linux-desktop-explained/` and
  `origin/main:content/posts/2025/Q4/linux-desktop-{1..6}-*/`

**Interfaces:**

- Consumes: the seven legacy articles and nine current articles.
- Produces: the chapter-specific lab checklist used by Tasks 2-6.

- [x] **Step 1: Record the retained legacy topics**

  Add a coverage checklist under each chapter task for useful legacy observations: boot
  entries, initramfs inputs, unit dependencies, structured journal fields, udev matching,
  D-Bus inspection, sessions and seats, DRM connectors, renderer selection, portal
  services, PipeWire objects, font matching, Fcitx control, network layers, inhibitors,
  sleep capabilities, and shutdown history.

  Coverage inventory:
  - Chapter 1: component boundaries, system/user managers, target dependencies, and the
    limits of each observation.
  - Chapter 2: UEFI/boot-loader state, boot entries, kernel command line, block-device
    identifiers, live mounts, initrd timing, and the critical chain.
  - Chapter 3: unit source and runtime properties, dependency trees, structured journal
    fields, udev properties/rule evaluation, and D-Bus object introspection.
  - Chapter 4: logind sessions/seats, the user manager, display-manager state, PAM
    generation, Secret Service ownership, and polkit agents.
  - Chapter 5: TTY, GPU driver binding, DRM connectors, Wayland globals, renderer
    selection, XWayland, scoped protocol tracing, and coredumps.
  - Chapter 6: desktop entries, application scopes, portal front-end/back-end services,
    D-Bus names, portal configuration, and document mounts.
  - Chapter 7: PipeWire devices/nodes/links, WirePlumber policy, font matching, font
    caches, Fcitx input-method state, and process-local environment variables.
  - Chapter 8: driver/carrier/manager state, IPv4/IPv6 addresses and routes, DNS, sockets,
    nftables hooks, and TUN interfaces.
  - Chapter 9: inhibitors, supported sleep states, swap and hibernation prerequisites,
    wakeup settings, suspend logs, previous-boot shutdown history, deactivating units, and
    busy mounts.

- [x] **Step 2: Record material that must not return**

  Confirm that forced shutdown, SysRq, writes to sysfs, speculative performance
  percentages, server-only network tuning, generic container networking, and unverified
  environment-variable fixes remain excluded.

  Exclusion inventory: forced poweroff and reboot flags, SysRq triggers, writes to
  `/sys/power` or device wakeup files, live filesystem repair, stopping production
  services for demonstration, flushing or replacing firewall rules, changing routes,
  persistent environment-variable “fixes”, speculative performance percentages,
  server-only sysctl tuning, bonding/VLAN tutorials, and generic container-networking
  digressions.

- [x] **Step 3: Verify coverage boundaries**

  Run:

  ```bash
  git show origin/main:content/posts/2025/Q4/linux-desktop-1-boot-security/index.md
  git show origin/main:content/posts/2025/Q4/linux-desktop-2-systemd-services/index.md
  git show origin/main:content/posts/2025/Q4/linux-desktop-3-session-graphics/index.md
  git show origin/main:content/posts/2025/Q4/linux-desktop-4-multimedia-input/index.md
  git show origin/main:content/posts/2025/Q4/linux-desktop-5-network/index.md
  git show origin/main:content/posts/2025/Q4/linux-desktop-6-shutdown-troubleshooting/index.md
  ```

  Expected: all legacy source files are readable without modifying the worktree.

### Task 2: Restore architecture, boot, and system-foundation labs

**Files:**

- Modify: `content/posts/2025/Q3/linux-desktop-architecture/index.md`
- Modify: `content/posts/2025/Q4/linux-desktop-boot/index.md`
- Modify: `content/posts/2025/Q4/linux-desktop-system-foundations/index.md`

**Interfaces:**

- Consumes: Task 1 coverage inventory and locally verified systemd/boot/udev observations.
- Produces: reusable observation vocabulary for later chapters: unit, journal field,
  device property, bus name, object path, interface, and method.

- [x] **Step 1: Expand the series-level observation method**

  Add a compact boundary-oriented workflow to chapter one: identify the component, query
  its state, follow the handoff, and state what remains unverified. Include
  `systemctl show`, `systemctl --user show`, and one dependency query with selected
  output.

- [x] **Step 2: Restore boot inspection labs**

  Add safe labs for `bootctl status/list`, `/proc/cmdline`, `lsblk`/`blkid`, `findmnt`,
  and `systemd-analyze critical-chain`. Explain ESP/boot-entry data, kernel command-line
  inputs, stable storage identifiers, mount observations, and dependency-critical timing.
  Use selected, redacted output only.

- [x] **Step 3: Restore unit and journal labs**

  Add `systemctl cat/show/list-dependencies` examples and a reversible journal experiment
  using `systemd-cat` or `logger` with a unique non-sensitive identifier, followed by a
  filtered `journalctl` query. Do not restart services or change unit state.

- [x] **Step 4: Restore udev and D-Bus labs**

  Add `udevadm info` for a non-sensitive device, a safe rule-evaluation query such as
  `udevadm test-builtin` only when it does not mutate state, and `busctl tree/introspect`
  against the bus daemon or another stable service with automatic activation disabled
  where supported.

- [x] **Step 5: Verify the three chapters**

  Run all included commands on the NixOS host, redact outputs, then run Prettier, typos,
  `git diff --check`, and a Hugo production build.

### Task 3: Restore login, session, and graphics labs

**Files:**

- Modify: `content/posts/2025/Q4/linux-desktop-login-session/index.md`
- Modify: `content/posts/2026/Q3/linux-desktop-graphics/index.md`

**Interfaces:**

- Consumes: unit/D-Bus vocabulary from Task 2.
- Produces: a session-to-device-to-renderer observation chain used by application and
  media chapters.

- [x] **Step 1: Add session and seat observations**

  Add safe queries for the current session, active seat, user manager, and
  greetd/display-manager state. If the agent process has no logind session, discover the
  graphical session read-only and publish only generic selected fields such as `Type`,
  `Class`, `Active`, `Remote`, and `State`.

- [x] **Step 2: Add PAM, keyring, and polkit observations**

  Show how to inspect generated PAM configuration, identify the Secret Service owner, and
  locate a polkit authentication agent without reading secrets or changing authentication
  state.

- [x] **Step 3: Add graphics device observations**

  Restore `tty`, `lspci -k`, `/sys/class/drm`, selected DRM journal fields,
  `wayland-info`, `glxinfo -B`, and XWayland process/socket observations. Explain which
  layer each command observes.

- [x] **Step 4: Add opt-in protocol debugging**

  Document `WAYLAND_DEBUG=1` as an application-scoped diagnostic command with privacy and
  volume warnings, not as a persistent environment setting. Add `coredumpctl list/info` as
  a read-only crash-inspection path without publishing arguments or dumps.

- [x] **Step 5: Verify the two chapters**

  Run safe commands from the graphical session, obtain missing tools through Nix, redact
  output, then run formatting, spelling, diff, link, and Hugo checks.

### Task 4: Restore application, portal, media, font, and input labs

**Files:**

- Modify: `content/posts/2026/Q3/linux-desktop-app-integration/index.md`
- Modify: `content/posts/2025/Q4/linux-desktop-media-input/index.md`

**Interfaces:**

- Consumes: session, D-Bus, Wayland, and renderer observations from Tasks 2-3.
- Produces: application-to-portal-to-PipeWire and input-context observation workflows.

- [x] **Step 1: Add application-launch observations**

  Show how to locate a desktop entry, inspect `Exec`/`DBusActivatable`, map a running app
  to a generated user unit, and inspect the relevant unit dependencies without launching
  an arbitrary application.

- [x] **Step 2: Add portal observations**

  Restore portal front-end/back-end checks, selected D-Bus names, unit status, portal
  configuration lookup, and Documents portal mount observations. Do not trigger screen
  capture or grant permissions merely for the article.

- [x] **Step 3: Add PipeWire object observations**

  Use `wpctl status`, `wpctl inspect`, and, where useful, `pw-cli ls` to connect device,
  sink/source, stream, node, port, and link concepts. Withhold local application and
  device names while showing stable field names.

- [x] **Step 4: Add font and input observations**

  Expand beyond `fc-match`: include `fc-list`, a verbose `fc-match` or `fc-pattern` query,
  cache status where useful, `fcitx5-remote --check -n`, selected `fcitx5-diagnose`
  sections, and environment-variable inspection scoped to the current process.

- [x] **Step 5: Verify the two chapters**

  Run the commands in the active desktop session, use Nix for missing tools, redact
  output, then run formatting, spelling, diff, link, and Hugo checks.

### Task 5: Restore network and power labs

**Files:**

- Modify: `content/posts/2025/Q4/linux-desktop-network/index.md`
- Modify: `content/posts/2025/Q4/linux-desktop-power/index.md`

**Interfaces:**

- Consumes: device, service, journal, and application-boundary observations from earlier
  tasks.
- Produces: end-to-end interface-to-application and running-to-sleep/shutdown workflows.

- [x] **Step 1: Expand link and manager observations**

  Add driver/firmware checks, carrier state, network-manager ownership, networkd/iwd
  state, and selected journal queries. Keep NetworkManager alternatives where relevant
  without assuming it is installed.

- [x] **Step 2: Expand address, route, DNS, and socket observations**

  Add a layered IPv4/IPv6 checklist using `ip`, `resolvectl query/status`, route
  selection, and `ss` for application sockets. Preserve the distinction between
  configuration state, route calculation, DNS response, and real application connectivity.

- [x] **Step 3: Expand nftables and TUN observations**

  Show how to identify tables, base chains, hooks, and TUN interfaces with read-only
  commands. Do not publish a full local ruleset or advise flushing rules.

- [x] **Step 4: Expand power and shutdown observations**

  Add `systemd-inhibit --list`, `/sys/power/state`, `/sys/power/disk`, `mem_sleep`,
  `swapon --show`, selected wakeup settings, suspend journal queries, previous-boot
  shutdown logs, and read-only checks for deactivating units or busy mounts.

- [x] **Step 5: Verify the two chapters**

  Run all safe commands without suspending, hibernating, stopping services, changing
  routes, or changing power settings. Redact output, then run formatting, spelling, diff,
  link, and Hugo checks.

### Task 6: Cross-series editorial and verification pass

**Files:**

- Modify: all nine canonical Linux desktop article files only when needed for consistency.
- Test: generated production site under `/tmp/thiscute-linux-desktop-practical-verify`.

**Interfaces:**

- Consumes: all chapter changes from Tasks 2-5.
- Produces: the final coherent series and evidence for completion.

- [x] **Step 1: Enforce lab structure**

  Confirm every major chapter has multiple practical checkpoints and every checkpoint
  states its question, command, fields, and conclusion boundary. Avoid an arbitrary
  command-count target when a mechanism has no useful safe observation.

- [x] **Step 2: Enforce distribution neutrality**

  Confirm commands and mechanisms are generic Linux first. Put NixOS module/options and
  Arch package/config locations in clearly labeled follow-up paragraphs.

- [x] **Step 3: Enforce prose quality**

  Search for translationese, audit prose, sandbox prose, unexplained naked command lists,
  unsafe commands, fabricated output, and repeated disclaimers. Apply the humanizer rules
  without deleting technical detail.

- [x] **Step 4: Run full verification**

  Run:

  ```bash
  prettier --check <nine article files>
  typos <nine article files>
  git diff --check
  hugo --environment production --destination /tmp/thiscute-linux-desktop-practical-verify --cleanDestinationDir
  ```

  Parse generated pages to verify numbering, series order, diagrams, command blocks,
  retained nix-config links, internal URLs, and heading fragments.

- [x] **Step 5: Commit and update PR**

  Stage the plan and nine article files only, derive a Conventional Commit message from
  the staged diff, commit without skipping hooks, push `codex/linux-desktop-rewrite`, and
  inspect PR #53 checks. Leave `assets/jsconfig.json` unstaged.
