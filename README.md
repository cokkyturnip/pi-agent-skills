# 🧠 Pi Agent Skills

A collection of modular skills for [Pi](https://github.com/earendil-works/pi), an AI coding agent harness. Skills load on demand: only `name` and `description` sit in the prompt until a task matches.

**Contents:** 20 skill directories, each with a `SKILL.md`. Nothing here is installed automatically.

---

## 📦 Installation

Copy the skill directory you want into a skill location.

```bash
# shared skill — read by pi, Codex and OpenCode as user scope
rm -rf ~/.agents/skills/markitdown          # only when replacing an old copy
cp -R markitdown ~/.agents/skills/

# pi-only skill
cp -R pi-cleanup-sessions ~/.pi/agent/skills/
```

Removing the old copy first keeps `cp` behaviour identical on macOS and Linux: GNU `cp` nests a directory inside an existing same-named target, BSD `cp` merges.

Copy the whole directory, not just `SKILL.md`. Keep `references/`, `scripts/` and `assets/` beside it, then reload the agent (`/reload` in pi).

| Location | For |
|----------|-----|
| `~/.agents/skills/` | skills another harness may also use |
| `~/.pi/agent/skills/` | pi-only skills (prefix `pi-`) |

### Verification

```bash
ls ~/.agents/skills/ ~/.pi/agent/skills/
```

A directory containing `SKILL.md` is one skill. A missing `SKILL.md` means an incomplete copy, and the agent ignores it.

---

## 🗂️ Skills in this repository

### ☁️ Cloud & cost estimation

| Skill | What it does |
|-------|--------------|
| **[aws-pricing](aws-pricing/)** | AWS pricing queries, cost estimates and infrastructure sizing. Price List API methodology, Fargate/EC2/Lambda approach, cross-document consistency checks. |
| **[firebase-pricing](firebase-pricing/)** | Firebase and Google Cloud pricing, cost estimates, free-tier limits. Billing API methodology without hardcoded prices. |
| **[capacity-planning](capacity-planning/)** | Capacity planning documents: sizing, TPS and request estimates, cost estimates. Also for checking numbers in PRD or architecture docs for consistency. |
| **[creatio-ai-cost-estimator](creatio-ai-cost-estimator/)** | Cost estimates for the Creatio AI platform (AI Actions, credits) and custom LLM usage. Per-module token math and multi-tier model strategies. |

### 📄 Documents, media & knowledge

| Skill | What it does |
|-------|--------------|
| **[markitdown](markitdown/)** | Convert PDF, DOCX, PPTX, XLSX/XLS, EPUB, Outlook MSG, HTML, CSV, JSON, XML, notebooks, audio and ZIP into Markdown. Documents per-format dependencies and the silent-failure cases (0-byte image output, empty stdin without a format hint). |
| **[youtube-summarizer](youtube-summarizer/)** | Summarise YouTube videos from their transcript, with fallbacks when the primary extraction path fails. Key points, themes, timestamps. |
| **[state-of-llm-apis](state-of-llm-apis/)** | LLM API reference: specifications, pricing, model comparisons, changelogs and deprecation schedules for major providers. Wrapper around a git-pulled database; run its sync manually before relying on freshness. |
| **[graphify](graphify/)** | Turn a codebase, document set or media corpus into a queryable knowledge graph, then query, path-find or explain over it. |

### 🛠️ Pi operations

| Skill | What it does |
|-------|--------------|
| **[pi-cleanup-sessions](pi-cleanup-sessions/)** | Session cleanup: keeps the 20 most recent sessions per project, maximum age 14 days. Manual-only; the script reports failures and exits non-zero instead of failing silently. |
| **[configure-9router](configure-9router/)** | Manage 9router model combos through SQLite: register and whitelist models, maintain routing combos, blacklist, audit usage, back up before edits. |
| **[opencode-go-quota](opencode-go-quota/)** | Check OpenCode Go subscription quota windows (rolling, weekly, monthly) and detect expired credentials. |
| **[pi-router-pintar](pi-router-pintar/)** | Work on the pi-router-pintar project itself: an auto-model router extension for the pi coding agent, published on npm. |
| **[herdr](herdr/)** | Control Herdr, a terminal multiplexer for coding agents: panes, tabs, workspaces, agent targets. Use only when the user mentions Herdr explicitly. |

### 🤝 Development workflow

| Skill | What it does |
|-------|--------------|
| **[github-collaboration](github-collaboration/)** | Contribute to an upstream repository via fork, branch and PR. Reads CONTRIBUTING.md, follows repo conventions, watches CI, answers review comments. |
| **[security-review](security-review/)** | Three-layer security review: pattern warnings, LLM diff review, cross-file data flow. For authentication, authorization, user input, databases, file uploads and API endpoints. |
| **[find-skills](find-skills/)** | Search the open agent-skills ecosystem (skills.sh) and vet candidates before recommending them. Read-then-copy install policy: it does not run `npx skills add -y`, and it treats a third-party `SKILL.md` as code to review. |
| **[stop-slop](stop-slop/)** | Remove predictable AI writing patterns from prose: filler phrases, formulaic structures, passive voice, register drift. Comes with reference lists for phrases, structures and before/after examples. |

### 📝 Notion & project management

| Skill | What it does |
|-------|--------------|
| **[notion](notion/)** | Create, append or update Notion pages. MCP OAuth as the primary path, REST API with Python as the fallback when browser-based auth is unavailable. |
| **[project-schedule](project-schedule/)** | Generate and maintain MS Project XML schedules that open in Microsoft Project and ProjectLibre: tasks, dependencies, milestones, holidays. |
| **[proposal-creation](proposal-creation/)** | Draft and review IT procurement proposals from RKS, RFI, RFP, tender specifications or pengadaan documents: scope, pricing, schedule, Notion publication. |

---

## 🧩 How skills load in pi

**Auto-detection.** pi scans `~/.agents/skills/*/SKILL.md` and `~/.pi/agent/skills/*/SKILL.md` at startup and puts each skill's `name`, `description` and path into the system prompt. The body stays on disk.

**Progressive disclosure.** Three levels:

| Level | What loads | When |
|-------|-----------|------|
| Metadata | `name` and `description` | always, one short line per skill |
| Instructions | `SKILL.md` | when a task matches the description |
| Resources | `references/`, `scripts/`, `assets/` | when the instructions point at them |

`scripts/` never enters context: the agent runs the script and reads its output.

**Selecting a skill.** The description decides. Write it as *what it does* plus *when to use it*; as an example, `markitdown` names the file types it handles because that is what a user actually says. If a skill should never be picked automatically, set `disable-model-invocation: true` in its frontmatter and call it as `/skill:<name>`.

---

## 🙏 Sources & License

Skills adapted from other projects keep their original license:

| Skill | Upstream | Author |
|-------|----------|--------|
| `stop-slop` | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | hardikpandya |
| `state-of-llm-apis` | [janwilmake/state-of-llm-apis](https://github.com/janwilmake/state-of-llm-apis) | janwilmake |
| `markitdown` | [microsoft/markitdown](https://github.com/microsoft/markitdown) | Microsoft |
| `configure-9router` | [decolua/9router](https://github.com/decolua/9router) | decolua |
| `find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) | vercel-labs |
| `security-review` | inspired by Anthropic's `security-guidance` and `obra/superpowers` | — |

The remaining skills were written for this collection.

Original skills: **MIT**. See [LICENSE](LICENSE).

---

## 🤝 Contributing

1. One skill per directory, containing `SKILL.md`.
2. Keep `SKILL.md` lean; move long reference material into `references/` and load it on demand.
3. Preserve attribution when adapting existing work.
4. No secrets or API keys in files; read them from the environment.
