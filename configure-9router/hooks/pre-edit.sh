#!/usr/bin/env bash
# pre-edit hook for configure-9router skill
# This script creates a timestamped backup of SKILL.md before any edit operation.
# It also cleans up backups older than 14 days.

SKILL_DIR="$(dirname "${BASH_SOURCE[0]}")/.."  # skill root directory
BACKUP_DIR="$SKILL_DIR/backup"
SKILL_FILE="$SKILL_DIR/SKILL.md"

mkdir -p "$BACKUP_DIR"
# Create timestamped backup
cp "$SKILL_FILE" "$BACKUP_DIR/$(date +%Y%m%d_%H%M%S)_SKILL.md"
# Delete backups older than 14 days
find "$BACKUP_DIR" -type f -mtime +14 -delete

# Optional: output latest backup name for logging
echo "Backup created: $(ls -t "$BACKUP_DIR" | head -1)"
