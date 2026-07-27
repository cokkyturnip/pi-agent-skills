---
name: cleanup-sessions
description: Cleans up old/unused Pi sessions. Retains the 20 most recent sessions per project, with a maximum age of 14 days.
---

# Skill: Cleanup Sessions

This skill manages Pi's session lifecycle by removing old or unused sessions. It ensures that only the 20 most recent sessions per project are retained, with a maximum age limit of 14 days, to keep the Pi agent lean and efficient.

---

## Session Management Strategy

Pi's session management follows a strict policy:

1.  **Retention Limit**: Maximum of 20 most recent sessions are kept per project.
2.  **Time Limit**: Sessions older than 14 days are automatically removed.
3.  **Automatic Cleanup**: The cleanup process runs automatically, typically at the beginning of each session, provided the cleanup script is in place.

This ensures that Pi's performance is not degraded by accumulating excessive session data.

---

## Core Actions

- **Session Pruning**: Removes sessions that exceed the defined limits (count or age).
- **Log Reporting**: If sessions are deleted, the skill logs the action, indicating how many sessions were removed.

---

## Usage Contexts

This skill is most useful in the following scenarios:

- **System Maintenance**: Regularly performed to maintain optimal performance and storage usage for the Pi agent.
- **Resource Management**: Ensures that disk space is not consumed by outdated session data.
- **Agent Efficiency**: Helps keep the agent responsive by preventing slowdowns caused by a large number of sessions.
