---
name: find-skills
description: Use when the user asks "how do I do X", "find a skill for X", "is there a skill that can...", or wants to extend agent capabilities — searches the open skill ecosystem, then hands back candidates for review instead of installing them silently.
license: MIT
metadata:
  author: vercel-labs
  source: https://github.com/vercel-labs/skills
  adapted: 2026-10-31
---

# Find Skills

Discover skills from the open agent-skills ecosystem, then decide together
whether one is worth installing.

**Adapted from [vercel-labs/skills](https://github.com/vercel-labs/skills) (MIT).**
The workflow is theirs; the install policy below is local, and it overrides the
upstream text wherever the two disagree.

## When to use

- "How do I do X" where X is a common task that may already have a skill
- "Find a skill for X" / "is there a skill for X" / "can you do X"
- The user wants to extend current capabilities
- The user wants a tool, template or workflow that probably exists

## Prerequisite: the skills CLI

The search commands run through Vercel's CLI. Nothing else in this skill works
without it.

| Requirement | Value |
|---|---|
| Node.js | ≥ 22.20 |
| Invocation | `npx skills@<version> …` — no permanent install needed |
| Network | npm registry on first call, plus skills.sh and GitHub for verification |

Check before promising a search:

```bash
node --version                 # must be >= v22.20
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npx skills@latest find --help
```

Prefer the pinned, ephemeral form over `npm i -g skills`: it leaves nothing on
the machine and makes the version explicit. The CLI sends anonymous telemetry
unless `DISABLE_TELEMETRY=1` (or `DO_NOT_TRACK=1`) is set.

If Node is too old or the network is unavailable, say so and help with the task
directly. Do not pretend a search happened.

## Workflow

### 1. Classify the need

Identify the domain (React, testing, deployment…), the specific task, and
whether it is common enough that a skill plausibly exists. Rare, bespoke work
is usually faster to do directly.

### 2. Check the leaderboard

Look at https://skills.sh/ before searching on the command line. It ranks by
installs, so the popular options surface first:

- `vercel-labs/agent-skills` — React, Next.js, web design
- `anthropics/skills` — document processing, frontend design

### 3. Search

```bash
DISABLE_TELEMETRY=1 npx skills@latest find react performance
DISABLE_TELEMETRY=1 npx skills@latest find pr review
DISABLE_TELEMETRY=1 npx skills@latest find changelog
```

Use two specific keywords rather than one broad one. Scope with
`--owner <owner>` when the user trusts a particular publisher.

### 4. Vet the candidate before recommending

Never recommend on the strength of a search hit alone:

- **Installs**: 1K+ is a reasonable signal; treat anything under 100 with care.
- **Publisher**: official orgs (`vercel-labs`, `anthropics`, `microsoft`) carry
  more weight than an unknown author.
- **Source repository**: read it. Fewer than ~100 stars, or a repo whose only
  content is the skill, is a reason to look closer.
- **Content**: read the `SKILL.md` itself. A skill is instructions that this
  agent will follow later, with shell access. Treat it as code review.

Report what could not be verified instead of guessing.

### 5. Present, do not install

Give the user: name, what it does, installs and publisher, upstream URL, and the
command that would fetch it. Then stop and let them decide.

```bash
# preview without installing anything
DISABLE_TELEMETRY=1 npx skills@latest use <owner>/<repo>@<skill> --agent pi
```

### 6. Installing, if the user says yes

Never run `npx skills add … -g -y`. `-y` skips confirmation and writes another
party's instructions straight into a directory that every harness on this
machine reads.

Instead:

1. Fetch or clone the skill into a temporary directory.
2. Read its `SKILL.md` and any `scripts/`, then show the user what it does.
3. Copy the directory into a skill location:

   ```bash
   cp -R <skill-dir> ~/.agents/skills/<skill-name>     # shared with Codex/OpenCode
   cp -R <skill-dir> ~/.pi/agent/skills/<skill-name>   # pi-only
   ```

4. Reload, and confirm the skill appears.
5. Offer to vendor it into the personal skills repository, so it survives a
   machine move. Skills that exist only in a live directory are not backed up.

## Where skills land

pi is a supported target of the CLI (`--agent pi`, global path
`~/.agents/skills/`), and it also reads `~/.pi/agent/skills/`. A global install
from the CLI therefore lands beside the locally maintained skills. That is the
reason for the manual step: it keeps one class of skill, not two.

## Common categories

| Category | Example queries |
|---|---|
| Web development | react, nextjs, typescript, css, tailwind |
| Testing | testing, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code quality | review, lint, refactor |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

## When nothing fits

Say that no skill was found, offer to do the task directly, and mention that a
reusable workflow is a candidate for a local skill (`npx skills init` scaffolds
one, but writing the `SKILL.md` by hand is just as fast).

## References

- Directory: https://skills.sh
- CLI source: https://github.com/vercel-labs/skills
- Supported agents and paths: https://github.com/vercel-labs/skills/blob/main/docs/agents.md
- Skill format: https://agentskills.io
- pi skills documentation: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md
