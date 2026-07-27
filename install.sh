#!/usr/bin/env bash
#=============================================================================
# Pi Agent Skills — Interactive Installer
#   • Checkbox-style: toggle individual skills
#   • Default: all selected
#   • Standalone via curl | bash  OR  run from cloned repo
#=============================================================================
set -euo pipefail

SKILL_DIR="${HOME}/.pi/agent/skills"
CLAUDE_SKILL_DIR="${HOME}/.claude/skills"
REPO_URL="https://github.com/cokkyturnip/pi-agent-skills"

# sync-upstream wajib — selalu terinstall, tidak bisa di-uncheck
MANDATORY=("sync-upstream")

SKILLS=(
  "banner-design"     "brand"             "cleanup-sessions"
  "code-review"       "configure-9router"  "configure-pi"
  "design"            "design-system"     "notion"
  "project-schedule"  "security-review"   "slides"
  "state-of-llm-apis" "stop-slop"         "sync-upstream"
  "ui-styling"        "ui-ux-pro-max"     "youtube-summarizer"
)

# State: all selected by default
SELECTED=()
for _ in "${SKILLS[@]}"; do SELECTED+=(1); done

bold()      { printf "\033[1m%s\033[0m" "$1"; }
green()     { printf "\033[32m%s\033[0m" "$1"; }
red()       { printf "\033[31m%s\033[0m" "$1"; }
dim()       { printf "\033[2m%s\033[0m" "$1"; }
cls()       { printf "\033[2J\033[H"; }

selected_count() {
  local n=0 i
  for i in "${SELECTED[@]}"; do [[ $i -eq 1 ]] && n=$((n + 1)); done
  echo "$n"
}

show_menu() {
  cls
  echo "╔══════════════════════════════════════════════════╗"
  echo "║      $(bold 'Pi Agent Skills — Interactive Installer')      ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  echo "$(dim 'Number → toggle   a → select all   n → select none')"
  echo "$(dim '  i → install     q → quit')"
  echo ""
  for i in "${!SKILLS[@]}"; do
    s="${SKILLS[$i]}"
    if [[ " ${MANDATORY[*]} " == *" ${s} "* ]]; then
      printf "  [%2d] %s %s  %s $(dim '(mandatory)')\n" "$i" "$(green '■')" " " "$s"
    elif [[ ${SELECTED[$i]} -eq 1 ]]; then
      printf "  [%2d] %s %s  %s\n" "$i" "$(green '✔')" " " "$s"
    else
      printf "  [%2d] %s %s  %s\n" "$i" "$(dim '·')" " " "$s"
    fi
  done
  echo ""
  printf "  $(bold 'Selected:') %d / %d\n" "$(selected_count)" "${#SKILLS[@]}"
  echo ""
}

do_install() {
  local src=$1 count=0
  mkdir -p "$SKILL_DIR" "$CLAUDE_SKILL_DIR"

  # Install mandatory skills first
  for s in "${MANDATORY[@]}"; do
    if [[ -d "$src/$s" ]]; then
      mkdir -p "$SKILL_DIR/$s"
      shopt -s dotglob
      for entry in "$src/$s"/*; do
        bn=$(basename "$entry")
        if [[ "$bn" != "scripts" ]]; then
          cp -r "$entry" "$SKILL_DIR/$s/"
        fi
      done
      shopt -u dotglob
      if [[ -d "$src/$s/scripts" ]] && [[ ! -d "$CLAUDE_SKILL_DIR/$s/scripts" ]]; then
        mkdir -p "$CLAUDE_SKILL_DIR/$s"
        cp -r "$src/$s/scripts" "$CLAUDE_SKILL_DIR/$s/"
      fi
      echo "  $(green '■') $s $(dim '(mandatory)')"
      count=$((count + 1))
    fi
  done

  for i in "${!SKILLS[@]}"; do
    s="${SKILLS[$i]}"
    # Skip mandatory — already installed
    if [[ " ${MANDATORY[*]} " == *" ${s} "* ]]; then
      continue
    fi
    [[ ${SELECTED[$i]} -eq 0 ]] && continue
    if [[ -d "$src/$s" ]]; then
      mkdir -p "$SKILL_DIR/$s"
      shopt -s dotglob
      for entry in "$src/$s"/*; do
        bn=$(basename "$entry")
        if [[ "$bn" != "scripts" ]]; then
          cp -r "$entry" "$SKILL_DIR/$s/"
        fi
      done
      shopt -u dotglob
      if [[ -d "$src/$s/scripts" ]] && [[ ! -d "$CLAUDE_SKILL_DIR/$s/scripts" ]]; then
        mkdir -p "$CLAUDE_SKILL_DIR/$s"
        cp -r "$src/$s/scripts" "$CLAUDE_SKILL_DIR/$s/"
      fi
      echo "  $(green '✔') $s"
      count=$((count + 1))
    else
      echo "  $(red '✖') $s $(dim '(not found)')"
    fi
  done
  for f in .gitignore LICENSE README.md; do
    [[ -f "$src/$f" ]] && cp "$src/$f" "$SKILL_DIR/$f" 2>/dev/null || true
  done
  echo ""
  echo "  $(bold 'Done!') $count skill(s) installed"
  echo "  SKILL.md  → $SKILL_DIR"
  echo "  Scripts   → $CLAUDE_SKILL_DIR"
  echo "  Pi will auto-detect them on next startup."
}

# ── Setup env compatibility ──
setup_env() {
  local profile=""
  if [[ -n "${ZSH_VERSION:-}" ]]; then
    profile="${HOME}/.zshrc"
  elif [[ -n "${BASH_VERSION:-}" ]]; then
    if [[ -f "${HOME}/.bash_profile" ]]; then
      profile="${HOME}/.bash_profile"
    elif [[ -f "${HOME}/.bashrc" ]]; then
      profile="${HOME}/.bashrc"
    fi
  fi

  if [[ -z "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    local line='export CLAUDE_PLUGIN_ROOT="$HOME"'
    if [[ -n "$profile" ]] && grep -q "CLAUDE_PLUGIN_ROOT" "$profile" 2>/dev/null; then
      echo "  $(dim '·') CLAUDE_PLUGIN_ROOT already in '"$(basename "$profile")"'"
    elif [[ -n "$profile" ]]; then
      echo "" >> "$profile"
      echo "# Pi Agent Skills: CLAUDE_PLUGIN_ROOT for ui-ux-pro-max compatibility" >> "$profile"
      echo "$line" >> "$profile"
      echo "  $(green '✔') Added CLAUDE_PLUGIN_ROOT to '"$(basename "$profile")"'"
    else
      echo "  $(yellow '!') Cannot detect shell profile. Set manually:"
      echo "      echo 'export CLAUDE_PLUGIN_ROOT=\"\$HOME\"' >> ~/.bashrc"
    fi
    export CLAUDE_PLUGIN_ROOT="$HOME"
  else
    echo "  $(green '✔') CLAUDE_PLUGIN_ROOT already set (value: ${CLAUDE_PLUGIN_ROOT})"
  fi
}

# ==== Main ====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IS_CLONED=false
[[ -d "$SCRIPT_DIR/.git" ]] && IS_CLONED=true

while true; do
  show_menu
  read -rp "  $(bold '→') " input
  case "$input" in
    [qQ]) echo "  Aborted."; exit 0 ;;
    [iI]) break ;;
    [aA]) for i in "${!SELECTED[@]}"; do SELECTED[$i]=1; done ;;
    [nN]) for i in "${!SELECTED[@]}"; do SELECTED[$i]=0; done ;;
    *)
      if [[ "$input" =~ ^[0-9]+$ ]] && (( input >= 0 && input < ${#SKILLS[@]} )); then
        [[ ${SELECTED[$input]} -eq 1 ]] && SELECTED[$input]=0 || SELECTED[$input]=1
      else
        input="${input//,/ }"
        for n in $input; do
          [[ "$n" =~ ^[0-9]+$ ]] && (( n >= 0 && n < ${#SKILLS[@]} )) && \
            [[ ${SELECTED[$n]} -eq 1 ]] && SELECTED[$n]=0 || SELECTED[$n]=1
        done
      fi
      ;;
  esac
done

echo ""
echo "$(bold 'Installing selected skills…')"
echo ""

if $IS_CLONED; then
  do_install "$SCRIPT_DIR"
else
  TMP=$(mktemp -d)
  trap "rm -rf $TMP" EXIT
  echo "  $(dim 'Cloning repo…')"
  git clone --depth 1 "$REPO_URL" "$TMP/repo" 2>/dev/null || {
    echo "  $(red '✖') Failed to clone. Check internet and try again."
    exit 1
  }
  do_install "$TMP/repo"
fi

echo ""
setup_env
echo ""
echo "  $(dim 'Tip: ls ~/.pi/agent/skills/  to verify.')"