# Linux Desktop Series Retirement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the nine unpublished rewritten Linux desktop articles into
`learn-tlpi/linux-desktop/` and remove every published and unpublished version of the
series, its site references, and its statistics from the blog.

**Architecture:** Copy and convert the rewritten articles before deleting their Hugo
sources. Treat the two repositories as separate deliverables: `learn-tlpi` receives
portable Markdown with relative navigation, while `thiscute.world` removes content and
filters the seven historically published URLs from future GA-derived statistics.

**Tech Stack:** Markdown, Hugo 0.165.0, Python 3, `unittest`, Prettier, typos, Git.

**Spec:** `docs/superpowers/specs/2026-09-20-linux-desktop-retirement-design.md`

## Global Constraints

- Migrate only the nine rewritten articles from PR #53; do not migrate the seven old
  articles.
- Remove Hugo frontmatter and blog-only AI declarations from the migrated Markdown while
  preserving technical content, diagrams, commands, official references, and public
  `nix-config` links.
- Exclude only the seven published legacy URLs from GA-derived statistics; the nine
  rewritten URLs were never published and need no statistics exclusion.
- Do not create redirects, 410 pages, or placeholders for retired URLs.
- Preserve the user's unstaged `assets/jsconfig.json` change and never stage it.
- Create separate commits in the two repositories. Push only `codex/linux-desktop-rewrite`
  to PR #53; do not push `learn-tlpi`.
- Verify the migrated copy before deleting any source article.

---

### Task 1: Add a failing retirement-statistics test

**Files:**

- Modify: `tests/test_statistics_legacy.py`
- Modify: `update_statistics.py`

**Interfaces:**

- Consumes: GA-style reports accepted by `process_data(data: dict) -> list[dict]`.
- Produces: `RETIRED_POST_PATHS: set[str]` containing the seven published old URLs;
  `process_data()` omits matching rows after normalizing a missing trailing slash.

- [x] **Step 1: Replace the legacy marker expectation with retirement expectations**

  Keep the report fixture and add tests asserting that every path below is absent from
  `process_data()` results, both with and without its trailing slash:

  ```python
  RETIRED_PATHS = (
      "/posts/linux-desktop-explained/",
      "/posts/linux-desktop-1-boot-security/",
      "/posts/linux-desktop-2-systemd-services/",
      "/posts/linux-desktop-3-session-graphics/",
      "/posts/linux-desktop-4-multimedia-input/",
      "/posts/linux-desktop-5-network/",
      "/posts/linux-desktop-6-shutdown-troubleshooting/",
  )
  ```

  Retain tests proving unrelated paths are normalized, merged, title-adjusted, and
  quality-filtered as before.

- [x] **Step 2: Run the focused test and confirm it fails**

  Run: `python3 -m unittest tests.test_statistics_legacy -v`

  Expected: FAIL because the current implementation returns retired pages and adds
  `legacyPage`.

- [x] **Step 3: Implement early retirement filtering**

  Rename `LEGACY_POST_PATHS` to `RETIRED_POST_PATHS`. After fragment removal and
  trailing-slash normalization, skip a row when `page_path in RETIRED_POST_PATHS`. Delete
  the later `legacyPage` mutation.

- [x] **Step 4: Run the focused test**

  Run: `python3 -m unittest tests.test_statistics_legacy -v`

  Expected: all tests PASS.

### Task 2: Convert the nine articles into portable Markdown

**Files:**

- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/README.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/01-architecture.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/02-boot.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/03-system-foundations.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/04-login-session.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/05-graphics.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/06-app-integration.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/07-media-input.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/08-network.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/09-power.md`
- Create: `/home/ryan/codes/learn-tlpi/linux-desktop/images/featured-image.webp`
- Modify: `/home/ryan/codes/learn-tlpi/README.md`

**Interfaces:**

- Consumes: the nine Hugo `index.md` files in PR #53.
- Produces: ordinary Markdown with one H1 per article and only relative links for series
  navigation.

- [x] **Step 1: Compare article images before copying**

  Run a Python SHA-256 inventory over all `featured-image.webp` files. Copy one shared
  image only if hashes match; otherwise copy distinct images as
  `images/NN-featured-image.webp` and reference the matching file.

- [x] **Step 2: Convert each source article**

  For each file, remove the complete YAML frontmatter and the leading AI declaration,
  insert the frontmatter title as `# ...`, and replace internal routes using this exact
  mapping:

  ```text
  /posts/linux-desktop-architecture/       -> 01-architecture.md
  /posts/linux-desktop-boot/               -> 02-boot.md
  /posts/linux-desktop-system-foundations/ -> 03-system-foundations.md
  /posts/linux-desktop-login-session/      -> 04-login-session.md
  /posts/linux-desktop-graphics/           -> 05-graphics.md
  /posts/linux-desktop-app-integration/    -> 06-app-integration.md
  /posts/linux-desktop-media-input/        -> 07-media-input.md
  /posts/linux-desktop-network/            -> 08-network.md
  /posts/linux-desktop-power/              -> 09-power.md
  ```

- [x] **Step 3: Add the directory README and repository entry**

  `linux-desktop/README.md` must describe the system-learning-first goal and list all nine
  files in order. Add `- [Linux desktop system notes](./linux-desktop/)` to the root
  README alongside the existing learning resources.

- [x] **Step 4: Validate the migrated copy before source deletion**

  Run a Python checker that asserts exactly nine numbered article files, no YAML opening
  delimiter, no `AI 创作声明`, no `/posts/linux-desktop-` link, all relative Markdown
  targets exist, and every referenced local image exists.

  Expected: zero validation errors.

- [x] **Step 5: Format and commit `learn-tlpi`**

  Run:

  ```text
  prettier --write README.md linux-desktop/*.md
  prettier --check README.md linux-desktop/*.md
  git diff --check
  ```

  Stage only `README.md` and `linux-desktop/`, then commit with
  `docs: add Linux desktop system notes`. Do not push.

### Task 3: Remove the series and its site references

**Files:**

- Delete: all nine rewritten `content/posts/**/linux-desktop-*/` directories in the PR
  branch
- Delete: Linux desktop rewrite specs and plans under `docs/superpowers/`, except this
  retirement spec and plan
- Modify: `CHRONICLE.md`
- Modify: `content/history/2025/index.md`
- Modify: `content/posts/2025/Q4/2025-summary/index.md`
- Inspect: `static/_redirects`, `config.toml`, and all tracked text files

**Interfaces:**

- Consumes: the validated and committed `learn-tlpi/linux-desktop/` archive from Task 2.
- Produces: a Hugo content tree with no Linux desktop article, alias, series link, or
  rewrite-process document.

- [x] **Step 1: Delete the exact article and rewrite-document paths**

  Delete the nine rewritten article directories. Confirm the seven old directories are
  already absent; if any remain, delete them too. Delete the 2026-09-15 series design,
  rewrite plan, evidence plan, and practical-labs plan. Preserve the retirement spec and
  this plan as the audit trail for the removal.

- [x] **Step 2: Rewrite historical references without inventing history**

  Remove recommendation/navigation links to the series. Where a yearly reflection records
  that the author worked on Linux desktop notes, keep a short unlinked statement only when
  needed for the surrounding narrative; otherwise remove the sentence.

- [x] **Step 3: Scan all tracked text for retired content**

  Search for all sixteen slugs, `Linux 桌面系统`, and `桌面系统故障排查`. Every remaining
  hit must be either the retirement spec/plan or a non-link historical sentence explicitly
  retained in Step 2.

### Task 4: Remove current and future statistics records

**Files:**

- Modify: `data/website_statistics.json`
- Modify: `data/posts_count.json`
- Modify: `update_statistics.py`
- Modify: `tests/test_statistics_legacy.py`

**Interfaces:**

- Consumes: `RETIRED_POST_PATHS` and the post-deletion content tree.
- Produces: statistics JSON without the retired URLs and post counts matching the
  remaining published content.

- [x] **Step 1: Remove legacy rows from website statistics**

  Parse `data/website_statistics.json`, recursively remove list entries whose `pagePath`
  is in `RETIRED_POST_PATHS`, preserve ordering and unrelated values, and write valid
  formatted JSON using the file's existing indentation convention.

- [x] **Step 2: Regenerate post counts**

  Run `python3 process_posts.py`, inspect its diff, and retain only changes explained by
  deleting the Linux desktop posts. If the script requires unavailable external state,
  compute the count change from the content tree using the same frontmatter rules
  implemented in `process_posts.py`.

- [x] **Step 3: Re-run statistics tests and validate JSON**

  Run:

  ```text
  python3 -m unittest tests.test_statistics_legacy -v
  python3 -m json.tool data/website_statistics.json
  python3 -m json.tool data/posts_count.json
  ```

  Expected: tests PASS and both JSON files parse successfully.

### Task 5: Verify, commit, and update PR #53

**Files:**

- Modify only as required by Tasks 1-4 and formatting.
- Preserve unstaged: `assets/jsconfig.json`

**Interfaces:**

- Consumes: the complete blog retirement diff.
- Produces: one tested blog commit pushed to `codex/linux-desktop-rewrite`.

- [x] **Step 1: Run repository checks**

  Run:

  ```text
  prettier --check <all changed Markdown, Python, and JSON files supported by Prettier>
  typos <all changed text files>
  python3 -m unittest discover -s tests -v
  git diff --check
  hugo --environment production --destination /tmp/thiscute-linux-desktop-retired --cleanDestinationDir
  ```

- [x] **Step 2: Verify generated-site absence**

  Assert that the production output contains none of the seven old URL directories, nine
  rewritten URL directories, or the `Linux 桌面系统` series taxonomy page. Search
  generated HTML for links to all sixteen slugs; expected count is zero.

- [x] **Step 3: Verify both worktrees and staged scope**

  Confirm `learn-tlpi` contains only its intended committed migration. In the blog, stage
  the retirement files but not `assets/jsconfig.json`; run `git diff --staged --check` and
  inspect `git diff --staged --stat`.

- [x] **Step 4: Commit and push the blog change**

  Commit using a Conventional Commit message derived from the staged diff, then push only
  `codex/linux-desktop-rewrite` to `origin` for PR #53. Do not push `learn-tlpi`.

- [x] **Step 5: Read back PR state**

  Use `gh pr view 53` to confirm its head SHA and `gh pr checks 53` to report CI as
  passed, failed, or pending. Do not claim pending checks passed.
