#!/usr/bin/env bash
# Session cleanup script — retains 20 latest sessions per project + 14-day age limit
# Runs via startup routine in AGENTS.md (checks .last_cleanup timestamp)
#
# Failure policy: a failed project is reported and skipped, the remaining
# projects still run, and the script exits non-zero with the timestamp NOT
# written — so retention is retried next session instead of being silently
# considered done. No xargs: session paths contain spaces and colons.

set -uo pipefail

SESSIONS_DIR="${PI_CODING_AGENT_SESSION_DIR:-$HOME/.pi/agent/sessions}"
LAST_CLEANUP_FILE="$HOME/.pi/agent/skills/sync-upstream/.last_session_cleanup"
RETAIN_COUNT=20
RETAIN_DAYS=14

# Check if we should run (skip if already run today)
if [[ -f "$LAST_CLEANUP_FILE" ]]; then
  LAST_CLEANUP=$(cat "$LAST_CLEANUP_FILE" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  DIFF=$((NOW - LAST_CLEANUP))
  if [[ $DIFF -lt 86400 ]]; then
    echo "Session cleanup skipped (already run today)"
    exit 0
  fi
fi

if [[ ! -d "$SESSIONS_DIR" ]]; then
  echo "Session cleanup FAILED: sessions directory not found: $SESSIONS_DIR" >&2
  exit 1
fi

echo "Running session cleanup (retain $RETAIN_COUNT latest + $RETAIN_DAYS days per project)..."

failed=0
total_deleted=0
shopt -s nullglob

for project_dir in "$SESSIONS_DIR"/*/; do
  [[ -d "$project_dir" ]] || continue

  project=$(basename "$project_dir")
  sessions=("$project_dir"*.jsonl)
  [[ ${#sessions[@]} -eq 0 ]] && continue

  # Newest first. A bash read loop keeps state in the parent shell and
  # survives spaces/colons in paths; xargs -I{} does neither.
  sorted=()
  while IFS= read -r line; do
    sorted+=("${line#* }")
  done < <(
    for f in "${sessions[@]}"; do
      mtime=$(stat -f '%m' "$f" 2>/dev/null || stat -c '%Y' "$f" 2>/dev/null || echo 0)
      printf '%s %s\n' "$mtime" "$f"
    done | sort -rn
  )

  if [[ ${#sorted[@]} -ne ${#sessions[@]} ]]; then
    echo "  ERROR: $project — could not sort ${#sessions[@]} sessions (got ${#sorted[@]}); retention NOT applied" >&2
    failed=$((failed + 1))
    continue
  fi

  cutoff_epoch=$(( $(date +%s) - RETAIN_DAYS * 86400 ))
  deleted=0
  keep_count=0

  for session in "${sorted[@]}"; do
    mtime=$(stat -f '%m' "$session" 2>/dev/null || stat -c '%Y' "$session" 2>/dev/null || echo 0)

    if [[ $keep_count -lt $RETAIN_COUNT && $mtime -gt $cutoff_epoch ]]; then
      keep_count=$((keep_count + 1))
    else
      if ! rm -f "$session"; then
        echo "  ERROR: $project/$(basename "$session") — delete failed" >&2
        failed=$((failed + 1))
        continue
      fi
      echo "  Deleting: $project/$(basename "$session")"
      deleted=$((deleted + 1))
      total_deleted=$((total_deleted + 1))
    fi
  done

  [[ $deleted -gt 0 ]] && echo "  $project: deleted $deleted, kept $keep_count"
done

if [[ $failed -gt 0 ]]; then
  echo "Session cleanup INCOMPLETE: $failed problem(s), $total_deleted session(s) deleted" >&2
  echo "Retention NOT fully applied — timestamp not written, will retry next session" >&2
  exit 1
fi

# Update last cleanup timestamp only after a clean run
date +%s > "$LAST_CLEANUP_FILE"
echo "Session cleanup complete ($total_deleted deleted)"
