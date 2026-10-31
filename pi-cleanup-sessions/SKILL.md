---
name: pi-cleanup-sessions
description: Cleans up old/unused Pi sessions. Retains the 20 most recent sessions per project, with a maximum age of 14 days.
disable-model-invocation: true
---

# Skill: Cleanup Sessions

This skill manages Pi's session lifecycle by removing old or unused sessions. It ensures that only the 20 most recent sessions per project are retained, with a maximum age limit of 14 days, to keep the Pi agent lean and efficient.

---

## Session Management Strategy

Pi's session management follows a strict policy:

1.  **Retention Limit**: Maximum of 20 most recent sessions are kept per project.
2.  **Time Limit**: Sessions older than 14 days are automatically removed.
3.  **Manual invocation**: cleanup runs only when Lae invokes it — `/skill:pi-cleanup-sessions`. Nothing in `AGENTS.md` triggers it at session start.

This ensures that Pi's performance is not degraded by accumulating excessive session data.

---

## Core Actions

- **Session Pruning**: Removes sessions that exceed the defined limits (count or age).
- **Log Reporting**: If sessions are deleted, the skill logs the action, indicating how many sessions were removed.

---

## How to run

```bash
bash ~/.pi/agent/skills/pi-cleanup-sessions/scripts/cleanup-sessions.sh
```

The script skips itself if it ran successfully within the last 24 hours. To
force a run, delete the timestamp first:

```bash
rm -f ~/.pi/agent/.state/last-cleanup
```

Exit code 0 with `Session cleanup complete` means it ran; exit 1 means part of
retention was not applied (see Failure visibility).

## Failure visibility

The script reports problems instead of failing open:

- A project whose sessions cannot be sorted or deleted is reported as
  `retention NOT applied` and skipped; the remaining projects still run.
- Any problem makes the script exit non-zero with
  `Session cleanup INCOMPLETE`.
- `~/.pi/agent/.state/last-cleanup` is written only
  after a clean run, so a failed cleanup retries next session instead of
  being treated as done.

Never read the banner as success. Check the exit code, or wait for the
`Session cleanup complete` line. Session paths may contain spaces and
colons, which is why the script sorts with a bash read loop and not
`xargs`.

---

## Usage Contexts

This skill is most useful in the following scenarios:

- **System Maintenance**: Regularly performed to maintain optimal performance and storage usage for the Pi agent.
- **Resource Management**: Ensures that disk space is not consumed by outdated session data.
- **Agent Efficiency**: Helps keep the agent responsive by preventing slowdowns caused by a large number of sessions.
