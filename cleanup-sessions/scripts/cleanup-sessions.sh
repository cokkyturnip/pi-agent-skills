#!/usr/bin/env bash
# Session cleanup script — retains 20 latest sessions per project + 14-day age limit
# Runs via startup routine in AGENTS.md (checks .last_cleanup timestamp)

set -euo pipefail

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

echo "Running session cleanup (retain $RETAIN_COUNT latest + $RETAIN_DAYS days per project)..."

# Process each project directory
shopt -s nullglob
for project_dir in "$SESSIONS_DIR"/*/; do
  [[ -d "$project_dir" ]] || continue
  
  project=$(basename "$project_dir")
  sessions=("$project_dir"*.jsonl)
  [[ ${#sessions[@]} -eq 0 ]] && continue
  
  # Sort by mtime descending (newest first)
  IFS=$'\n' sorted=($(printf '%s\n' "${sessions[@]}" | xargs -I{} stat -f '%m %N' {} | sort -rn | cut -d' ' -f2-))
  
  deleted=0
  keep_count=0
  cutoff_epoch=$(( $(date +%s) - RETAIN_DAYS * 86400 ))
  
  for session in "${sorted[@]}"; do
    mtime=$(stat -f '%m' "$session" 2>/dev/null || stat -c '%Y' "$session" 2>/dev/null || echo 0)
    basename=$(basename "$session")
    
    # Check both criteria: keep if within count AND within age
    if [[ $keep_count -lt $RETAIN_COUNT && $mtime -gt $cutoff_epoch ]]; then
      ((keep_count++))
    else
      echo "  Deleting: $project/$basename"
      rm -f "$session"
      ((deleted++))
    fi
  done
  
  [[ $deleted -gt 0 ]] && echo "  $project: deleted $deleted, kept $keep_count"
done

# Update last cleanup timestamp
date +%s > "$LAST_CLEANUP_FILE"
echo "Session cleanup complete"