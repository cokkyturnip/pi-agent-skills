---
name: configure-pi
description: Sync pi agent configuration across machines via 3 git repos (pi-agent-config, pi-agent-skills, pi-skill-workspace). Setup on a new machine or sync between machines. Independent from configure-9router.
disable-model-invocation: true
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
| `cokkyturnip/pi-agent-skills` | `~/Documents/geek/codespace/pi-agent-skills` | **source of truth** for skills; `install.sh` copies selected skills into `~/.pi/agent/skills` |
| `cokkyturnip/pi-skill-workspace` | `~/Documents/pi-skill-workspace` | observation log, cross-cutting principles |

The skills repository and the live skills directory are **different
directories**: the repo is authoritative, `~/.pi/agent/skills` is an install
target populated by `install.sh` (a copy, not a clone). Editing the live
directory looks like a save but is lost on the next install — see Edit direction
below.

All paths use `~` — **the shell expands it** (Git-Bash on Windows,
zsh/bash on Mac). Never pass `~` to python code (`Path("~/.pi/agent")`
does not expand); use `Path.home()` or let the shell expand first.

## Setup on a new machine

Prereqs: pi installed and run once (`npm i -g @earendil-works/pi-coding-agent`,
run `pi`, then Ctrl+C).

```bash
# 1. Root the config repo into ~/.pi/agent
[ -d ~/.pi/agent/.git ] || { cd ~/.pi/agent && git init -b main && git remote add origin https://github.com/cokkyturnip/pi-agent-config.git && git pull origin main; }
# 2. Skills source repo, then install the skills you want
[ -d ~/Documents/geek/codespace/pi-agent-skills/.git ] || git clone https://github.com/cokkyturnip/pi-agent-skills.git ~/Documents/geek/codespace/pi-agent-skills
bash ~/Documents/geek/codespace/pi-agent-skills/install.sh   # copies selected skills into ~/.pi/agent/skills
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
git -C ~/Documents/geek/codespace/pi-agent-skills pull
git -C ~/Documents/pi-skill-workspace pull
```

```bash
git -C ~/.pi/agent push
git -C ~/Documents/geek/codespace/pi-agent-skills push
git -C ~/Documents/pi-skill-workspace push
```

On a `pull` conflict: never force — inspect `git status`, resolve, commit.
A conflict means two machines changed the same file.

## Edit direction (skills)

The repository is the source of truth. Two rules follow:

1. **Port live edits back before the next install.** If you edited a skill in
   `~/.pi/agent/skills/<name>`, copy it into the repo (`rsync -a` excluding
   `.DS_Store` and `.last_*`), otherwise the next `install.sh` run reverts it
   silently.
2. **A skill created only in the live directory is not backed up.** Add it to
   the repo and to the `SKILLS` array in `install.sh` in the same session.

Verify the direction with a cheap diff before installing:

```bash
diff -rq ~/.pi/agent/skills ~/Documents/geek/codespace/pi-agent-skills 2>/dev/null \
  | grep "^Files" | grep -v '\.DS_Store' | grep -v '\.last_'
```

Any line printed is a skill whose live copy differs from the repo — resolve
those into the repo first.

## What is NOT synced (by design)

| Item | Why | How it reaches a new machine |
|------|-----|------------------------------|
| `auth.json`, `notion-mcp-auth.json` | credentials — never in a repo | re-auth manually |
| `settings.json` | machine-specific (`shellPath`, provider config) | re-create / adjust per machine |
| `sessions/` | chat history embeds absolute paths, not portable | start fresh |
| `git/`, `npm/`, `bin/` | package caches managed by `pi install` | `pi install` again |
| `models-store.json` | cache | regenerated |

## Shared Skills — Cross-Agent Symlink Technique

For cross-agent skill sharing, use a single shared namespace:

- `~/.agents/skills/<skill-name>` — symlink → source skill dir.

Sources:
- skills source repo: `~/Documents/geek/codespace/pi-agent-skills/<name>`
- pi-local install target: `~/.pi/agent/skills/<name>`
- package/upstream: `~/.pi/agent/git/github/<org>/<repo>/skills/<name>`

No subfolder indirection (e.g. `~/.agents/upstream/...`); symlink name =
skill name, target = source.

OS:
- macOS/Linux: `ln -s <target> ~/.agents/skills/<name>`
- Windows: `mklink /J <target> ~/.agents/skills/<name>` (directory junction)

## Credentials (re-auth on a new machine)

- **Notion MCP**: run the `setup-oauth` skill.
- **9router / providers**: re-enter API keys in pi settings.
- `auth.json` and `notion-mcp-auth.json` are gitignored in
  `pi-agent-config` and must never be committed.

## Verification (pre-flight — once per machine)

First confirm each path is its own repository and that the skills repo is the
source, not the install target:

```bash
for p in ~/.pi/agent ~/Documents/geek/codespace/pi-agent-skills ~/Documents/pi-skill-workspace; do
  printf '%-55s ' "$p"; git -C "$p" rev-parse --show-toplevel 2>/dev/null || echo "NOT A REPO"
done
```

Expected: every line prints its own path. A nested directory that prints the
**parent** path is not a repo of its own — if `~/.pi/agent/skills` prints
`~/.pi/agent`, the live skills directory is inside the config repo (or
gitignored by it), and nothing written there is backed up. On that result:
stop, tell the user, and ask whether to re-clone the skills repo. Never
`git init` a replacement silently.

Then check remotes and branches:

```bash
git -C ~/.pi/agent remote get-url origin && git -C ~/.pi/agent branch --show-current
git -C ~/Documents/geek/codespace/pi-agent-skills remote get-url origin && git -C ~/Documents/geek/codespace/pi-agent-skills branch --show-current
git -C ~/Documents/pi-skill-workspace remote get-url origin && git -C ~/Documents/pi-skill-workspace branch --show-current
```

Expected: the three URLs above; branch `main` each.

Finally, confirm no live skill has drifted from the repo (see Edit direction):

```bash
diff -rq ~/.pi/agent/skills ~/Documents/geek/codespace/pi-agent-skills 2>/dev/null \
  | grep "^Files" | grep -v '\.DS_Store' | grep -v '\.last_'
```

Empty output means live and repo agree. After adding or moving a skill
directory, also confirm the host sees it: check the resource selector (or
`pi list`) and, when the active pi version does not auto-register the
directory, add it to `settings.json`, then reload. File placement alone is not
proof of registration.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation (command-based, no scripts) |

## See Also

- **`configure-9router`** — 9router DB backup/restore
- **`setup-oauth`** — Notion MCP OAuth re-auth
