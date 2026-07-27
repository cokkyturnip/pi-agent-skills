---
name: configure-pi
description: Backup and restore pi agent configuration (~/.pi/agent/ - settings, skills, auth, extensions). Independent from configure-9router. Use when migrating pi config to a new machine.
---

# Skill: configure-pi

This skill handles **only the pi agent configuration** (`~/.pi/agent/`). Fully independent from `configure-9router`.

Works on **Windows, macOS, and Linux**.

---

## Backup

```bash
# Creates ~/Downloads/pi-backup-<timestamp>/
python3 ~/.pi/agent/skills/configure-pi/backup.py

# Or specify output directory:
python3 ~/.pi/agent/skills/configure-pi/backup.py -b /path/to/backup-dir
```

---

## Restore (on new machine)

```bash
# 1. Install pi: npm i -g @earendil-works/pi-coding-agent
# 2. Run pi once, then Ctrl+C
# 3. Copy backup folder to new machine

# 4. Restore:
python3 ~/.pi/agent/skills/configure-pi/restore.py -b /path/to/pi-backup-<timestamp>

# Dry-run:
python3 ~/.pi/agent/skills/configure-pi/restore.py -b /path/to/pi-backup-<timestamp> --dry-run
```

Restore auto-runs `npm install` for packages declared in `settings.json`.

---

## Files

| File | Purpose |
|------|---------|
| `backup.py` | Exports `~/.pi/agent/` → timestamped folder |
| `restore.py` | Imports backup folder → `~/.pi/agent/` |
| `SKILL.md` | This documentation |

---

## Backup Output Structure

```
pi-backup-2026-07-20T05-30-00Z/
├── auth.json
├── settings.json
├── 9router-config.json
├── AGENTS.md
├── notion.json
├── notion-mcp-auth.json
├── web-search.json
├── stitch-api-key
├── skills/
└── extensions/
```

---

## What Gets Backed Up

**Included:** `auth.json`, `settings.json`, `9router-config.json`, `AGENTS.md`, `notion.json`, `notion-mcp-auth.json`, `web-search.json`, `stitch-api-key`, `skills/`, `extensions/`, `hooks/engine/`.

**Excluded:** `sessions/` (chat history), `models-store.json` (cache).

---

## Cross-Platform

| Platform | Config Path |
|----------|-------------|
| **macOS/Linux** | `~/.pi/agent/` |
| **Windows** | `%USERPROFILE%\.pi\agent\` |

All paths resolved via `pathlib.Path.home()` — no hardcoded paths.

---

## See Also

- **`configure-9router`** — for 9router DB backup/restore
