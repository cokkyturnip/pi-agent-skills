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

# ---- Skill catalogue ----
SKILLS=(
  "banner-design"
  "brand"
  "cleanup-sessions"
  "code-review"
  "configure-9router"
  "configure-pi"
  "design"
  "design-system"
  "notion"
  "project-schedule"
  "security-review"
  "slides"
  "state-of-llm-apis"
  "stop-slop"
  "ui-styling"
  "ui-ux-pro-max"
  "youtube-summarizer"
)

# ---- State ----
SELECTED=()
for _ in "${SKILLS[@]}"; do SELECTED+=(1); done  # all on by default

# ---- Helpers ----
bold()      { printf "\033[1m%s\033[0m" "$1"; }
green()     { printf "\033[32m%s\033[0m" "$1"; }
dim()       { printf "\033[2m%s\033[0m" "$1"; }
clear_screen() { printf "\033[2J\033[H"; }

toggle() {
  local idx=$1
  [[ ${SELECTED[$idx]} -eq 1 ]] && SELECTED[$idx]=0 || SELECTED[$idx]=1
}

selected_count() {
  local n=0 i
  for i in "${SELECTED[@]}"; do [[ $i -eq 1 ]] && n=$((n + 1)); done
  echo "$n"
}

clamp() {
  local val=$1 lo=$2 hi=$3
  [[ $val -lt $lo ]] && echo $lo || ([[ $val -gt $hi ]] && echo $hi || echo $val)
}

show_menu() {
  clear_screen
  echo "╔══════════════════════════════════════════════════╗"
  echo "║      $(bold 'Pi Agent Skills — Interactive Installer')      ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  echo "$(dim 'Number → toggle   a → select all   n → select none')"
  echo "$(dim '  i → install     q → quit')"
  echo ""

  local i pad
  for i in "${!SKILLS[@]}"; do
    pad=$(( i < 10 ? 1 : 0 ))
    if [[ ${SELECTED[$i]} -eq 1 ]]; then
      printf "  [%d] %s $(green '✔')  %s\n" "$i" "$(dim "${SKILLS[$i]//?/ }")" "${SKILLS[$i]}"
    else
      printf "  [%d] %s $(dim '·')  %s\n" "$i" " " "${SKILLS[$i]}"
    fi
  done

  echo ""
  printf "  $(bold 'Selected:') %d / %d\n" "$(selected_count)" "${#SKILLS[@]}"
  echo ""
}

install_skills() {
  local src=$1
  local count=0
  mkdir -p "$SKILL_DIR"

  for i in "${!SKILLS[@]}"; do
    [[ ${SELECTED[$i]} -eq 0 ]] && continue
    local skill="${SKILLS[$i]}"
    if [[ -d "$src/$skill" ]]; then
      cp -r "$src/$skill" "$SKILL_DIR/"
      count=$((count + 1))
      echo "  $(green '✔') $skill"
    else
      echo "  $(bold '⚠') $skill $(dim '(not found, skipped)')"
    fi
  done

  # Also copy root files if they exist
  for f in .gitignore LICENSE; do
    [[ -f "$src/$f" ]] && cp "$src/$f" "$SKILL_DIR/$f" 2>/dev/null || true
  done

  echo ""
  echo "  $(bold 'Done!') $count skill(s) installed to $SKILL_DIR"
  echo "  Pi will detect them automatically on next startup."
}

# ======== Main (standalone mode — clones repo) ========
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
  # Script is being sourced — not meant for that
  return
fi

# ---- Determine source location ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IS_CLONED=false
[[ -d "$SCRIPT_DIR/.git" ]] && IS_CLONED=true

# ---- Interactive prompt ----
while true; do
  show_menu
  read -rp "  $(bold '→') " input

  case "$input" in
    q|Q)   echo "  Aborted."; exit 0 ;;
    i|I)   break ;;
    a|A)   for i in "${!SELECTED[@]}"; do SELECTED[$i]=1; done ;;
    n|N)   for i in "${!SELECTED[@]}"; do SELECTED[$i]=0; done ;;
    all)   for i in "${!SELECTED[@]}"; do SELECTED[$i]=1; done ;;
    none)  for i in "${!SELECTED[@]}"; do SELECTED[$i]=0; done ;;
    *)
      if [[ "$input" =~ ^[0-9]+$ ]] && (( input >= 0 && input < ${#SKILLS[@]} )); then
        toggle "$input"
      elif [[ "$input" =~ ^[0-9, ]+$ ]]; then
        # comma/space separated numbers
        IFS=', ' read -ra nums <<< "$input"
        for n in "${nums[@]}"; do
          n=$((n))
          (( n >= 0 && n < ${#SKILLS[@]} )) && toggle "$n"
        done
      fi
      ;;
  esac
done

# ---- Install ----
echo ""
echo "$(bold 'Installing selected skills…')"
echo ""

if $IS_CLONED; then
  install_skills "$SCRIPT_DIR"
else
  # Standalone mode (curl | bash) — clone to temp
  TMP=$(mktemp -d) && trap "rm -rf $TMP" EXIT
  echo "  $(dim 'Cloning repo…')"
  git clone --depth 1 "$REPO_URL" "$TMP/repo" 2>/dev/null || {
    echo "  $(bold '✖') Failed to clone repo. Check your internet."
    exit 1
  }
  install_skills "$TMP/repo"
fi

echo ""
echo "  $(dim "Tip: run 'ls ~/.pi/agent/skills/' to verify.")"