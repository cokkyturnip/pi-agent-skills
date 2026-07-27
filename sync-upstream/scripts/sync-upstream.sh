#!/usr/bin/env bash
#=============================================================================
# Sync Upstream — Update Pi skills from upstream repositories
# Usage: bash sync-upstream.sh [upstream-name] [skill-name]
#   - No args: list available upstreams
#   - upstream-name only: sync all skills from that upstream
#   - upstream-name skill-name: sync specific skill
#
# Config: ./upstreams.json (same directory)
#=============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/upstreams.json"
PI_SKILL_DIR="${HOME}/.pi/agent/skills"
CLAUDE_SKILL_DIR="${HOME}/.claude/skills"
TMPDIR="${TMPDIR:-/tmp}"
WORK_TREE="${TMPDIR}/pi-sync-upstream"

bold()    { printf "\033[1m%s\033[0m" "$1"; }
green()   { printf "\033[32m%s\033[0m" "$1"; }
yellow()  { printf "\033[33m%s\033[0m" "$1"; }
red()     { printf "\033[31m%s\033[0m" "$1"; }
dim()     { printf "\033[2m%s\033[0m" "$1"; }

cleanup() { rm -rf "$WORK_TREE"; }
trap cleanup EXIT

# ── Parse JSON with bash (no jq dependency)
parse_config() {
  # Extract upstream names
  if [[ "$1" == "list-upstreams" ]]; then
    grep -oP '"[A-Za-z0-9_/-]+":\s*\{' "$CONFIG" | sed 's/": {$//' | sed 's/"//g'
    return
  fi
  # Get URL for upstream
  if [[ "$1" == "get-url" ]]; then
    local name="$2"
    grep -A10 "\"${name}\":" "$CONFIG" | grep '"url"' | head -1 | sed 's/.*"url": "\(.*\)".*/\1/'
    return
  fi
  # Get type for upstream
  if [[ "$1" == "get-type" ]]; then
    local name="$2"
    grep -A10 "\"${name}\":" "$CONFIG" | grep '"type"' | head -1 | sed 's/.*"type": "\(.*\)".*/\1/'
    return
  fi
  # Get repo path for upstream
  if [[ "$1" == "get-repo-path" ]]; then
    local name="$2"
    grep -A10 "\"${name}\":" "$CONFIG" | grep '"repoPath"' | head -1 | sed 's/.*"repoPath": "\(.*\)".*/\1/'
    return
  fi
  # List skills for upstream
  if [[ "$1" == "list-skills" ]]; then
    local name="$2"
    # Extract lines between "skills": { and the next }
    sed -n "/\"${name}\":/,/^  \}/p" "$CONFIG" | sed -n '/"skills": {/,/    \}/p' | \
      grep -oP '"[A-Za-z0-9_-]+":\s*\[' | sed 's/": \[$//' | sed 's/"//g'
    return
  fi
}

# ── Sync a single skill from upstream clone
sync_skill() {
  local upstream="$1" skill="$2" repo_dir="$3" repo_path="$4"
  local src="${repo_dir}/${repo_path}/${skill}"
  local pi_dst="${PI_SKILL_DIR}/${skill}"
  local claude_dst="${CLAUDE_SKILL_DIR}/${skill}"

  echo ""
  echo "  $(bold "→ Sync: ${skill} (${upstream})")"

  if [[ ! -d "$src" ]]; then
    echo "  $(red "✖") Skill '${skill}' not found in upstream repo at ${src}"
    return 1
  fi

  # ── Sync scripts/ to ~/.claude/skills/ (runtime)
  if [[ -d "${src}/scripts" ]]; then
    if [[ ! -d "${claude_dst}/scripts" ]]; then
      mkdir -p "${claude_dst}"
      cp -r "${src}/scripts" "${claude_dst}/"
      echo "  $(green "✔") scripts/ → ~/.claude/skills/${skill}/ (new)"
    else
      # Check for changes
      local changes
      changes=$(diff -rq "${src}/scripts" "${claude_dst}/scripts" 2>/dev/null || true)
      if [[ -n "$changes" ]]; then
        rsync -a --delete "${src}/scripts/" "${claude_dst}/scripts/"
        echo "  $(green "✔") scripts/ → ~/.claude/skills/${skill}/ (updated)"
        echo "  $(dim "${changes}")"
      else
        echo "  $(dim "·") scripts/ — no changes"
      fi
    fi
  fi

  # ── Sync SKILL.md and references/ to ~/.pi/agent/skills/ (documentation)
  local pi_changes=false
  for item in "SKILL.md" "references" "data"; do
    if [[ -e "${src}/${item}" ]]; then
      if [[ ! -e "${pi_dst}/${item}" ]]; then
        mkdir -p "$(dirname "${pi_dst}/${item}")"
        cp -r "${src}/${item}" "${pi_dst}/${item}"
        echo "  $(green "✔") ${item} → ~/.pi/agent/skills/${skill}/ (new)"
        pi_changes=true
      else
        if [[ -f "${src}/${item}" && -f "${pi_dst}/${item}" ]]; then
          if ! diff -q "${src}/${item}" "${pi_dst}/${item}" >/dev/null 2>&1; then
            cp "${src}/${item}" "${pi_dst}/${item}"
            echo "  $(yellow "!") ${item} → ~/.pi/agent/skills/${skill}/ (updated)"
            pi_changes=true
          fi
        fi
      fi
    fi
  done

  if [[ "$pi_changes" == false ]] && [[ ! -d "${src}/scripts" || -z "$(diff -rq "${src}/scripts" "${claude_dst}/scripts" 2>/dev/null || echo "changed")" ]]; then
    echo "  $(dim "·") up to date"
  fi
}

# ── Main ──

if [[ ! -f "$CONFIG" ]]; then
  echo "$(red "✖") Config not found: ${CONFIG}"
  exit 1
fi

UPSTREAM="${1:-}"
SKILL="${2:-}"

# No args: list upstreams
if [[ -z "$UPSTREAM" ]]; then
  echo "$(bold "Available upstreams:")"
  echo ""
  for u in $(parse_config "list-upstreams"); do
    echo "  $(green "•") ${u}"
    for s in $(parse_config "list-skills" "$u"); do
      echo "      └ ${s}"
    done
  done
  echo ""
  echo "  Usage: $(bold "$(basename "$0") <upstream> [skill]")"
  exit 0
fi

# Validate upstream
if ! grep -q "\"${UPSTREAM}\":" "$CONFIG" 2>/dev/null; then
  echo "$(red "✖") Unknown upstream: ${UPSTREAM}"
  echo "  Available:"
  for u in $(parse_config "list-upstreams"); do echo "    ${u}"; done
  exit 1
fi

URL=$(parse_config "get-url" "$UPSTREAM")
REPO_PATH=$(parse_config "get-repo-path" "$UPSTREAM")
TYPE=$(parse_config "get-type" "$UPSTREAM" || echo "git")

echo "$(bold "Sync Upstream: ${UPSTREAM}")"
echo "  $(dim "Repo: ${URL}")"
echo ""

# Clone/fetch upstream
echo "  $(dim "Fetching upstream...")"
if [[ "$TYPE" == "submodule" ]]; then
  echo "  $(dim "Updating submodule from: ${URL}")"
  git submodule update --init --remote 2>&1 || \
    git submodule sync && git submodule update --init --remote 2>&1
  echo "  $(green "✔") Submodule updated."
else
  rm -rf "$WORK_TREE"
  git clone --depth 1 "$URL" "$WORK_TREE" 2>&1 | sed 's/^/    /'
  echo "  $(green "✔") Cloned ${URL}"
fi
echo ""

if [[ -n "$SKILL" ]]; then
  # Sync single skill
  if [[ "$TYPE" == "submodule" ]]; then
    echo "  $(dim "·") ${SKILL} (submodule — already updated above)"
  else
    sync_skill "$UPSTREAM" "$SKILL" "$WORK_TREE" "$REPO_PATH"
  fi
else
  # Sync all skills from this upstream
  for s in $(parse_config "list-skills" "$UPSTREAM"); do
    if [[ "$TYPE" == "submodule" ]]; then
      echo "  $(dim "·") ${s} (submodule — already updated above)"
    else
      sync_skill "$UPSTREAM" "$s" "$WORK_TREE" "$REPO_PATH"
    fi
  done
fi

echo ""
echo "$(green "✔") Done."