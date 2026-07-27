---
name: sync-upstream
description: Sync Pi skills from upstream repositories. Manage source-of-truth for scripts and documentation.
---

# Skill: Sync Upstream

This skill synchronizes Pi skills from their original upstream repositories. It handles the separation between documentation (kept in Pi) and executable scripts (kept in the canonical Claude path).

---

## Workflow

1. **Clone** upstream repositories into a working directory.
2. **Compare** upstream files (SKILL.md, references/, scripts/) with local Pi installations.
3. **Sync** scripts to `~/.claude/skills/<skill>/scripts/` (runtime directory).
4. **Sync** documentation to `~/.pi/agent/skills/<skill>/` (documentation directory).

---

## Usage

### List Available Upstreams
```bash
bash ~/.pi/agent/skills/sync-upstream/scripts/sync-upstream.sh
```

### Sync All Skills from an Upstream
```bash
bash ~/.pi/agent/skills/sync-upstream/scripts/sync-upstream.sh nextlevelbuilder/ui-ux-pro-max-skill
```

### Sync a Specific Skill
```bash
bash ~/.pi/agent/skills/sync-upstream/scripts/sync-upstream.sh nextlevelbuilder/ui-ux-pro-max-skill design
```

---

## Configuration (`upstreams.json`)

The `upstreams.json` file in `~/.pi/agent/skills/sync-upstream/scripts/` maps upstream repositories to Pi skills. 

- **Key**: Upstream repository name (e.g., `nextlevelbuilder/ui-ux-pro-max-skill`).
- **url**: Clone URL of the upstream repo.
- **repoPath**: Internal path where the skill folders reside.
- **skills**: List of skills provided by this upstream.

---

## Automation Rules

- **Documentation Updates**: Whenever `SKILL.md` or `references/` files are updated in the upstream repo, the sync script will detect the change and copy the latest version to `~/.pi/agent/skills/<skill>/`.
- **Script Updates**: Scripts (`scripts/`) are synced to `~/.claude/skills/<skill>/scripts/` to ensure full compatibility with Claude CLI.
- **No Overwrite**: Existing configuration files in `~/.claude/` will not be overwritten unless changes are explicitly detected by the `rsync` logic.
