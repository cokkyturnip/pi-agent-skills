#!/usr/bin/env bash
#=============================================================================
# Pi Agent Skills — Interactive Installer
#   • Checkbox-style: toggle individual skills
#   • Default: all selected
#   • Standalone via curl | bash  OR  run from cloned repo
#=============================================================================
set -euo pipefail

SKILL_DIR="${HOME}/.pi/agent/skills"
REPO_URL="https://github.com/cokkyturnip/pi-agent-skills"

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
    if [[ ${SELECTED[$i]} -eq 1 ]]; then
      printf "  [%2d] %s %s  %s\n" "$i" "$(green '✔')" " " "${SKILLS[$i]}"
    else
      printf "  [%2d] %s %s  %s\n" "$i" "$(dim '·')" " " "${SKILLS[$i]}"
    fi
  done
  echo ""
  printf "  $(bold 'Selected:') %d / %d\n" "$(selected_count)" "${#SKILLS[@]}"
  echo ""
}

do_install() {
  local src=$1 count=0
  mkdir -p "$SKILL_DIR"
  for i in "${!SKILLS[@]}"; do
    [[ ${SELECTED[$i]} -eq 0 ]] && continue
    s="${SKILLS[$i]}"
    if [[ -d "$src/$s" ]]; then
      cp -r "$src/$s" "$SKILL_DIR/"
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
  echo "  $(bold 'Done!') $count skill(s) installed → $SKILL_DIR"
  echo "  Pi will auto-detect them on next startup."
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
      # Try single number first
      if [[ "$input" =~ ^[0-9]+$ ]] && (( input >= 0 && input < ${#SKILLS[@]} )); then
        [[ ${SELECTED[$input]} -eq 1 ]] && SELECTED[$input]=0 || SELECTED[$input]=1
      else
        # Space/comma separated list
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
echo "  $(dim 'Tip: ls ~/.pi/agent/skills/  to verify.')"