---
name: readme
description: Repository README with skill directory overview, installation guide, and credits for the Pi Agent Skills collection.
disable-model-invocation: true
---

# 🧠 Pi Agent Skills

A curated collection of modular skills for [Pi](https://github.com/earendil-works/pi) — an AI coding agent harness. Skills auto-activate when relevant tasks are detected.

> **Status:** Active development. Tested with Pi on Node.js.
>
> **Philosophy:** Modular, on-demand, progressive disclosure. No skill loads unless needed.

This repository began as a personal inventory — tracking skills I had written myself or adapted from other open-source projects, all in one place to keep my Pi agent consistent across machines. Over time, it grew into a structured collection, and I realized it might help others too.

The collection will keep evolving. Skills get added as needs arise, not because of a grand roadmap. If something here saves you time, that's the point.

---

## 📦 Installation

### Interactive Installer (Recommended)

Pick only the skills you want via checkbox menu:

**Linux/macOS (bash):**
```bash
bash <(curl -s https://raw.githubusercontent.com/cokkyturnip/pi-agent-skills/main/install.sh)
```

**Windows (PowerShell 5+ / 7+):**
```powershell
iex (iwr -Uri https://raw.githubusercontent.com/cokkyturnip/pi-agent-skills/main/install.ps1).Content
```

> **⚠️ Upstream skill scripts** — Scripts for upstream skills (brand, design, etc.)
> are copied to `~/.claude/skills/` during installation.
> Run `sync-upstream` after installation to keep them up to date.

### Verification

Skills are auto-detected by Pi on startup:

```bash
ls ~/.pi/agent/skills/
# → aws-pricing  banner-design  brand  capacity-planning  cleanup-sessions
#   configure-9router  configure-pi  design  design-system  firebase-pricing
#   github-collaboration  notion  project-schedule  proposal-creation
#   security-review  slides  state-of-llm-apis  stop-slop  sync-upstream
#   ui-styling  ui-ux-pro-max  youtube-summarizer
```

### Per-Skill Dependencies

Some skills have optional runtime dependencies:

| Skill | Dependency | Required? |
|-------|-----------|-----------|
| `slides` | Chart.js (CDN-loaded in HTML output) | No |
| `design` | Gemini API key via `GEMINI_API_KEY` env | For image generation only |
| `state-of-llm-apis` | Git pull (auto: daily data sync) | Auto-handled |
| `youtube-summarizer` | Python + youtube-transcript-api | For local transcript fallback |
| `project-schedule` | Python (XML generation) | No (inline XML works) |

---

## 🗂️ Skill Directory

This collection contains **24 bundled skills** in `~/.pi/agent/skills/`. Additional skills are installed separately from upstream repositories — see [Upstream Skills](#-upstream-skills-installed-separately) below.

### 🎨 Design & Branding

| Skill | Description | Source |
|-------|-------------|--------|
| **[ui-ux-pro-max](ui-ux-pro-max/)** | UI/UX design intelligence database — 84 styles, 192 palettes, 74 font pairings, 22 tech stacks, 98 UX guidelines, 16 GSAP motion presets, 25 chart types. Progressive-loading CSV data. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[design](design/)** | Comprehensive design engine — 55 logo styles (Gemini AI), 50-deliverable corporate identity program (CIP), HTML presentations with Chart.js, 22 banner styles, 15 icon styles, social media photo generation. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[design-system](design-system/)** | Token architecture — primitive → semantic → component layers. CSS variable generation, spacing/typography scales, component specifications. Strategic slide creation for design system presentations. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[brand](brand/)** | Brand identity management — voice guidelines, visual identity, messaging frameworks, color palette management, typography specs, logo usage rules, asset organization, consistency checklists. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[banner-design](banner-design/)** | Banner design engine — 22 visual styles across 12 platforms (Facebook, Twitter/X, LinkedIn, YouTube, Instagram, Google Display, website hero, print). Art direction options with platform-specific sizing. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[slides](slides/)** | Strategic HTML presentation generator — Chart.js integration, design tokens, responsive layouts, copywriting formulas. Slide strategies for different audience contexts. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |
| **[ui-styling](ui-styling/)** | Beautiful UIs with shadcn/ui (Radix UI + Tailwind), Tailwind CSS utility-first styling, canvas-based visual designs. Accessible components (dialogs, dropdowns, tables), dark mode, responsive layouts. | **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** |

### ✅ Code Quality & Review

| Skill | Description | Source |
|-------|-------------|--------|
| **[security-review](security-review/)** | Three-layer security review — Layer 1: pattern warnings (unsafe deserialization, XSS, hardcoded secrets, SQL injection, eval). Layer 2: LLM diff review. Layer 3: cross-file data flow tracing. HARD GATE for auth/user-input/database/file-upload/API code. | **Original** (Inspired by Anthropic's `security-guidance` plugin and `obra/superpowers` methodology) |
| **[stop-slop](stop-slop/)** | AI writing pattern removal — eliminates predictable AI tells from prose. Pattern references for phrases, structures, and examples. Use for copywriting, summaries, proposals, editorial, and redaksi. | **[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)** |

> 💡 **`code-review` skill is installed separately** via the [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill) upstream repo (not bundled in this collection to keep this repo lean). See [Upstream Skills](#-upstream-skills-installed-separately).

### ☁️ Cloud & Infrastructure Pricing

| Skill | Description | Source |
|-------|-------------|--------|
| **[aws-pricing](aws-pricing/)** | AWS pricing queries, cloud cost estimation, infrastructure sizing. AWS Price List API methodology, Fargate/EC2/Lambda pricing approach, cross-document consistency checks. | **Original** |
| **[firebase-pricing](firebase-pricing/)** | Firebase/Google Cloud pricing queries, Firebase cost estimation, free tier limit checks. Google Cloud Billing API methodology and Firebase pricing structure without hardcoded prices. | **Original** |
| **[capacity-planning](capacity-planning/)** | Infrastructure capacity planning documents (sizing, TPS/request estimates, cost estimates) for systems with field teams, mobile agents, or API backends. Also use when numbers in PRD/architecture docs are questioned for consistency, or when a request breakdown, TPS calculation, or cloud cost estimate needs to be derived from scratch. | **Original** |

### 🔧 Configuration & Utilities

| Skill | Description | Source |
|-------|-------------|--------|
| **[configure-9router](configure-9router/)** | 9router model combo management via SQLite — register/whitelist models, manage routing combos, blacklist models, audit usage. Backup automation, pre-edit hooks, inventory tracking. | **Original** (Built on [9router](https://9router.com) CLI) |
| **[configure-pi](configure-pi/)** | Pi agent configuration backup & restore — settings, skills, auth, extensions. Machine migration tool. Independent from 9router config. | **Original** |
| **[cleanup-sessions](cleanup-sessions/)** | Session cleanup — retains 20 most recent sessions per project, max 14 days. Keeps Pi lean. | **Original** |
| **[sync-upstream](sync-upstream/)** *(mandatory)* | Sync Pi skills from upstream repositories. Manage source-of-truth for scripts and documentation. | **Original** |

### 📝 Notion & Project Management

| Skill | Description | Source |
|-------|-------------|--------|
| **[notion](notion/)** | Append content to Notion pages — preview-first workflow. Safe append with user confirmation before changes. | **Original** |
| **[project-schedule](project-schedule/)** | MS Project XML schedule generation — tasks, dependencies, milestones, holidays. ProjectLibre-compatible. | **Original** |
| **[proposal-creation](proposal-creation/)** | IT procurement proposal creation from procurement documents (RKS, RFI, RFP, tender specifications). Document analysis, scope, pricing, schedule, and Notion publication. | **Original** |

### 🤝 Development Workflow

| Skill | Description | Source |
|-------|-------------|--------|
| **[github-collaboration](github-collaboration/)** | Contribute to an upstream repository via fork, branch, PR. Reads CONTRIBUTING.md, follows repo conventions, monitors CI, responds to review. | **Original** |

### 🤖 LLM & Media

| Skill | Description | Source |
|-------|-------------|--------|
| **[state-of-llm-apis](state-of-llm-apis/)** | Living knowledge base of LLM API specifications, pricing, model comparisons, changelog, and deprecation schedules. Auto-updated daily from official provider docs. Covers OpenAI, Anthropic, Google, Mistral, xAI, DeepSeek, Cohere, Meta. | **Data:** [janwilmake/state-of-llm-apis](https://github.com/janwilmake/state-of-llm-apis) — **Skill wrapper:** Original |
| **[youtube-summarizer](youtube-summarizer/)** | YouTube video summarizer — transcript extraction, multi-fallback strategy (primary: Pi fetch_content, fallback: local Python, final: 9router). Analysis with key themes, arguments, conclusions. | **Original** |

---

## 🌐 Upstream Skills (Installed Separately)

Some skills are **not bundled** in this repository. They are installed as separate Git checkouts under `~/.pi/agent/git/github.com/<owner>/<repo>/skills/` and registered with Pi as external skill sources. Use [`sync-upstream`](sync-upstream/) to keep them current.

### [`awesome-skills/code-review-skill`](https://github.com/awesome-skills/code-review-skill)

Comprehensive code review methodology — 4-phase process (Context → High-Level → Line-by-Line → Summary), severity labeling (🔴 blocking / 🟡 important / 🟢 nit), 20+ language-specific guides, cross-cutting guides for architecture, performance, security, N+1, XSS, SQL injection, error handling, async/concurrency.

**Location:** `~/.pi/agent/git/github.com/awesome-skills/code-review-skill/`

### [`hardikpandya/stop-slop`](https://github.com/hardikpandya/stop-slop)

*(Bundled copy in this repo for convenience — see [Code Quality & Review](#-code-quality--review). The upstream clone is kept for reference and provenance.)*

**Location:** `~/.pi/agent/git/github.com/hardikpandya/stop-slop/`

### [`obra/superpowers`](https://github.com/obra/superpowers)

Process & methodology skills that govern *how* Pi works — used at conversation start, before coding, before debugging, before claiming work complete.

**Location:** `~/.pi/agent/git/github.com/obra/superpowers/skills/`

| Skill | Description |
|-------|-------------|
| **[brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming)** | **Mandatory before creative work** — creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| **[using-superpowers](https://github.com/obra/superpowers/tree/main/skills/using-superpowers)** | **Mandatory at conversation start** — establishes how to find and use skills, requiring skill invocation before any response including clarifying questions. |
| **[systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging)** | **Mandatory before proposing bug fixes** — root-cause investigation before any fix. |
| **[test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development)** | **Mandatory before implementing features/bugfixes** — write the test first, watch it fail, then implement. |
| **[writing-plans](https://github.com/obra/superpowers/tree/main/skills/writing-plans)** | Use when you have a spec or requirements for a multi-step task, before touching code. |
| **[writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills)** | Use when creating new skills, editing existing skills, or verifying skills work before deployment. |
| **[using-git-worktrees](https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees)** | Use when starting feature work that needs isolation from current workspace or before executing implementation plans. |
| **[verification-before-completion](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion)** | **Mandatory before claiming work complete** — evidence before assertions, always. |
| **[receiving-code-review](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review)** | Use when receiving code review feedback — requires technical rigor, not performative agreement. |
| **[requesting-code-review](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review)** | Use when completing tasks, implementing major features, or before merging. |
| **[subagent-driven-development](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development)** | Use when executing implementation plans with independent tasks in the current session. |
| **[dispatching-parallel-agents](https://github.com/obra/superpowers/tree/main/skills/dispatching-parallel-agents)** | Use when facing 2+ independent tasks that can be worked on without shared state. |
| **[executing-plans](https://github.com/obra/superpowers/tree/main/skills/executing-plans)** | Use when you have a written implementation plan to execute in a separate session with review checkpoints. |
| **[finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch)** | Use when implementation is complete and tests pass, to decide how to integrate the work. |

### Keeping Upstream Skills Current

```bash
# Manual sync (per repo)
cd ~/.pi/agent/git/github.com/obra/superpowers && git pull
cd ~/.pi/agent/git/github.com/awesome-skills/code-review-skill && git pull

# Or use the bundled sync-upstream skill (recommended)
# Pi auto-invokes this if registered, or run its script directly
```

---

## 🧩 How Skills Work in Pi

### Auto-Detection

Pi scans `~/.pi/agent/skills/*/SKILL.md` on startup. Each skill has a `name` and `description` in YAML frontmatter that Pi uses for context routing.

### Progressive Disclosure

Skills **never load their full content** unless activated. When you ask Pi to review code, Pi reads:
1. The skill's `SKILL.md` (~200-300 lines, the "how-to")
2. On-demand: language-specific reference files (e.g., `reference/react.md`) only when reviewing React code

This keeps token usage minimal even with 24+ skills installed.

### Activation Criteria

| Trigger | Skill |
|---------|-------|
| "Check security of this code" | `security-review` |
| "Review this PR / code change" | `code-review` *(upstream)* |
| "Summarize a YouTube video" | `youtube-summarizer` |
| "Design a logo / banner / brand" | `design`, `banner-design`, `brand` |
| "Create a UI component / layout" | `ui-styling`, `ui-ux-pro-max` |
| "Build a presentation deck" | `slides`, `design-system` |
| "Fix AI-sounding prose" | `stop-slop` |
| "Configure LLM models / routing" | `configure-9router` |
| "Backup / migrate Pi config" | `configure-pi` |
| "Generate a project timeline" | `project-schedule` |
| "Append to Notion page" | `notion` |
| "Create a proposal / tender response" | `proposal-creation` |
| "Estimate AWS / Firebase costs" | `aws-pricing`, `firebase-pricing` |
| "Plan infrastructure capacity" | `capacity-planning` |
| "Contribute to upstream via fork+PR" | `github-collaboration` |
| "Sync skills from upstream" | `sync-upstream` |
| "What's the latest LLM API data?" | `state-of-llm-apis` |
| "Compare model pricing / capabilities" | `state-of-llm-apis` |

**Process skills from `obra/superpowers`** are auto-invoked at conversation start and before/after major actions (brainstorming, debugging, TDD, verification). See [Upstream Skills](#-upstream-skills-installed-separately).

---

## 🙏 Credits & License

This collection adapts and builds upon several open-source projects. Each skill's `SKILL.md` or source repository contains its original license. We are deeply grateful to:

### Bundled Skills (in this repo)

| Project | Author | License |
|---------|--------|--------|
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [nextlevelbuilder](https://github.com/nextlevelbuilder) | MIT |
| [stop-slop](https://github.com/hardikpandya/stop-slop) | [hardikpandya](https://github.com/hardikpandya) | MIT |
| [state-of-llm-apis](https://github.com/janwilmake/state-of-llm-apis) | [janwilmake](https://github.com/janwilmake) | MIT |
| [9router](https://github.com/decolua/9router) | [decolua](https://github.com/decolua) | MIT |

### Upstream Skills (separate repos)

| Project | Author | License |
|---------|--------|--------|
| [code-review-skill](https://github.com/awesome-skills/code-review-skill) | [awesome-skills](https://github.com/awesome-skills) | MIT |
| [superpowers](https://github.com/obra/superpowers) | [obra](https://github.com/obra) | MIT |

### Tools

| Tool | Description |
|------|-------------|
| [Pi](https://github.com/earendil-works/pi) | AI coding agent harness by earendil-works |
| [shadcn/ui](https://ui.shadcn.com/) | UI component library (referenced by `ui-styling`) |
| [21st.dev](https://21st.dev/) | UI component marketplace (referenced by `ui-styling`, `ui-ux-pro-max`) |
| [Chart.js](https://www.chartjs.org/) | Charting library (referenced by `slides`, `design`) |

### Original Skills in This Collection

The following skills were created from scratch for this collection:

- `aws-pricing` — AWS cloud cost estimation workflow
- `capacity-planning` — Infrastructure capacity sizing & TPS estimation
- `cleanup-sessions` — Session lifecycle management for Pi
- `configure-9router` — 9router combo management workflow
- `configure-pi` — Pi config migration tooling
- `firebase-pricing` — Firebase/Google Cloud cost estimation
- `github-collaboration` — Fork/branch/PR workflow for upstream contributions
- `notion` — Safe Notion append workflow
- `proposal-creation` — IT procurement proposal generation
- `project-schedule` — MS Project XML generation
- `security-review` — Three-layer security review (inspired by Anthropic's security-guidance & obra/superpowers)
- `state-of-llm-apis` — LLM API knowledge wrapper around janwilmake's database
- `sync-upstream` — Upstream skill sync utility
- `youtube-summarizer` — YouTube transcript analysis

---

## 📄 License

Unless otherwise noted per-skill:

- Skills adapted from open-source projects retain their original license (see individual `SKILL.md` or original repository).
- Original skills in this collection are shared under **MIT License**.

See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

PRs welcome! Please follow existing structure:
1. Each skill in its own directory with `SKILL.md`
2. Progressive disclosure — keep core `SKILL.md` lean, load references on-demand
3. Credit sources — if adapting existing work, preserve attribution
4. No real secrets or API keys in files — use environment variables

---

*Made with ❤️ for the Pi ecosystem.*