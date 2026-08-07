---
name: configure-pi
description: Sync pi agent configuration across machines via 3 git repos (pi-agent-config, pi-agent-skills, pi-skill-workspace). Setup on a new machine or sync between machines. Independent from configure-9router.
---

# Skill: configure-pi

Syncs the pi agent configuration (`~/.pi/agent/`) across machines using
**three git repositories — no physical backup**. Works on Windows
(Git-Bash) and macOS/Linux. Independent from `configure-9router`.

The agent executes every command below with its own bash/git tools —
**no helper scripts**.

## The three repos

| Repo | Local path | Content |
|------|-----------|---------|
| `cokkyturnip/pi-agent-config` | `~/.pi/agent` (rooted) | `AGENTS.md`, `prompts/`; gitignored: auth, settings, sessions, caches |
| `cokkyturnip/pi-agent-skills` | `~/.pi/agent/skills` | skills (its own repo) |
| `cokkyturnip/pi-skill-workspace` | `~/Documents/pi-skill-workspace` | observation log, cross-cutting principles |

All paths use `~` — **the shell expands it** (Git-Bash on Windows,
zsh/bash on Mac). Never pass `~` to python code (`Path("~/.pi/agent")`
does not expand); use `Path.home()` or let the shell expand first.

## Setup on a new machine

Prereqs: pi installed and run once (`npm i -g @earendil-works/pi-coding-agent`,
run `pi`, then Ctrl+C).

```bash
# 1. Root the config repo into ~/.pi/agent
[ -d ~/.pi/agent/.git ] || { cd ~/.pi/agent && git init -b main && git remote add origin https://github.com/cokkyturnip/pi-agent-config.git && git pull origin main; }
# 2. Skills repo
[ -d ~/.pi/agent/skills/.git ] || git clone https://github.com/cokkyturnip/pi-agent-skills.git ~/.pi/agent/skills
# 3. Observation workspace
[ -d ~/Documents/pi-skill-workspace/.git ] || git clone https://github.com/cokkyturnip/pi-skill-workspace.git ~/Documents/pi-skill-workspace
```

Then:
- Reload pi: `/reload` (or restart)
- **Re-auth credentials** (never in any repo): Notion MCP, provider keys —
  see Credentials below

## Daily sync ritual

Pull before a session, push after:

```bash
git -C ~/.pi/agent pull
git -C ~/.pi/agent/skills pull
git -C ~/Documents/pi-skill-workspace pull
```

```bash
git -C ~/.pi/agent push
git -C ~/.pi/agent/skills push
git -C ~/Documents/pi-skill-workspace push
```

On a `pull` conflict: never force — inspect `git status`, resolve, commit.
A conflict means two machines changed the same file.

## What is NOT synced (by design)

| Item | Why | How it reaches a new machine |
|------|-----|------------------------------|
| `auth.json`, `notion-mcp-auth.json` | credentials — never in a repo | re-auth manually |
| `settings.json` | machine-specific (`shellPath`, provider config) | re-create / adjust per machine |
| `sessions/` | chat history embeds absolute paths, not portable | start fresh |
| `git/`, `npm/`, `bin/` | package caches managed by `pi install` | `pi install` again |
| `models-store.json` | cache | regenerated |

## Credentials (re-auth on a new machine)

- **Notion MCP**: run the `setup-oauth` skill.
- **9router / providers**: re-enter API keys in pi settings.
- `auth.json` and `notion-mcp-auth.json` are gitignored in
  `pi-agent-config` and must never be committed.

## Verification (pre-flight — once per machine)

```bash
git -C ~/.pi/agent remote get-url origin && git -C ~/.pi/agent branch --show-current
git -C ~/.pi/agent/skills remote get-url origin && git -C ~/.pi/agent/skills branch --show-current
git -C ~/Documents/pi-skill-workspace remote get-url origin && git -C ~/Documents/pi-skill-workspace branch --show-current
```

Expected: the three URLs above; branch `main` each.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation (command-based, no scripts) |

## See Also

- **`configure-9router`** — 9router DB backup/restore
- **`setup-oauth`** — Notion MCP OAuth re-auth
