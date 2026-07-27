<#
.SYNOPSIS
  Pi Agent Skills — Interactive Installer for Windows (PowerShell)
.DESCRIPTION
  Checkbox-style interactive installer. Select which skills to install.
  Run standalone from web or after cloning the repo.
.EXAMPLE
  # From web (run-as mode)
  iex (iwr -Uri https://raw.githubusercontent.com/cokkyturnip/pi-agent-skills/main/install.ps1).Content

  # From cloned repo
  .\install.ps1
#>

$RepoUrl  = "https://github.com/cokkyturnip/pi-agent-skills"
$SkillDir = "$env:USERPROFILE\.pi\agent\skills"
$ClaudeSkillDir = "$env:USERPROFILE\.claude\skills"

$Mandatory = @("sync-upstream")

$Skills = @(
  "banner-design",      "brand",             "cleanup-sessions"
  "code-review",        "configure-9router",  "configure-pi"
  "design",             "design-system",     "notion"
  "project-schedule",   "security-review",   "slides"
  "state-of-llm-apis",  "stop-slop",         "sync-upstream"
  "ui-styling",         "ui-ux-pro-max",     "youtube-summarizer"
)

# State: all 1 (selected) by default
$Selected = @($Skills | ForEach-Object { 1 })

function Write-Colored($Text, $Color = "White") {
  $colors = @{
    green   = "32"
    red     = "31"
    dim     = "2"
    bold    = "1"
    default = "0"
  }
  $code = if ($colors.ContainsKey($Color)) { $colors[$Color] } else { "0" }
  "`e[${code}m${Text}`e[0m"
}

function Show-Menu {
  [Console]::Clear()
  Write-Host "╔══════════════════════════════════════════════════╗"
  Write-Host "║      $(Write-Colored 'Pi Agent Skills — Interactive Installer' bold)      ║"
  Write-Host "╚══════════════════════════════════════════════════╝"
  Write-Host ""

  $selectedCount = ($Selected | Where-Object { $_ -eq 1 } | Measure-Object).Count
  $total = $Skills.Count
  Write-Host "$(Write-Colored 'Number → toggle   a → select all   n → select none' dim)"
  Write-Host "$(Write-Colored '  i → install     q → quit' dim)"
  Write-Host ""

  for ($i = 0; $i -lt $total; $i++) {
    $s = $Skills[$i]
    if ($Mandatory -contains $s) {
      Write-Host "  [$("{0:D2}" -f $i)] $(Write-Colored '■' green)  $s $(Write-Colored '(mandatory)' dim)"
    } else {
      $check = if ($Selected[$i] -eq 1) { $(Write-Colored '✔' green) } else { $(Write-Colored '·' dim) }
      Write-Host "  [$("{0:D2}" -f $i)] $check  $($Skills[$i])"
    }
  }

  Write-Host ""
  Write-Host "  $(Write-Colored "Selected: $selectedCount / $total" bold)"
  Write-Host ""
}

function Install-Skills($Src) {
  $count = 0
  New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
  New-Item -ItemType Directory -Path $ClaudeSkillDir -Force | Out-Null

  # Install mandatory skills first
  foreach ($s in $Mandatory) {
    $srcPath = Join-Path $Src $s
    if (Test-Path $srcPath) {
      # Copy skill (exclude scripts)
      $items = Get-ChildItem -Path $srcPath -Exclude "scripts"
      foreach ($item in $items) {
        if ($item.PSIsContainer) {
          Copy-Item -Path $item.FullName -Destination "$SkillDir\$s\" -Recurse -Force
        } else {
          Copy-Item -Path $item.FullName -Destination "$SkillDir\$s" -Force
        }
      }
      # Copy scripts to Claude
      $scriptsSrc = Join-Path $srcPath "scripts"
      $scriptsDst = "$ClaudeSkillDir\$s\scripts"
      if (Test-Path $scriptsSrc -and -not (Test-Path $scriptsDst)) {
        New-Item -ItemType Directory -Path "$ClaudeSkillDir\$s" -Force | Out-Null
        Copy-Item -Path $scriptsSrc -Destination "$ClaudeSkillDir\$s\" -Recurse -Force
      }
      Write-Host "  $(Write-Colored '■' green) $s $(Write-Colored '(mandatory)' dim)"
      $count++
    }
  }

  for ($i = 0; $i -lt $Skills.Count; $i++) {
    if ($Selected[$i] -eq 0) { continue }
    $s = $Skills[$i]
    if ($Mandatory -contains $s) { continue } # already installed
    $srcPath = Join-Path $Src $s
    if (Test-Path $srcPath) {
      # Copy skill (exclude scripts)
      $items = Get-ChildItem -Path $srcPath -Exclude "scripts"
      foreach ($item in $items) {
        if ($item.PSIsContainer) {
          Copy-Item -Path $item.FullName -Destination "$SkillDir\$s\" -Recurse -Force
        } else {
          Copy-Item -Path $item.FullName -Destination "$SkillDir\$s" -Force
        }
      }
      # Copy scripts to Claude (skip if exists)
      $scriptsSrc = Join-Path $srcPath "scripts"
      $scriptsDst = "$ClaudeSkillDir\$s\scripts"
      if (Test-Path $scriptsSrc -and -not (Test-Path $scriptsDst)) {
        New-Item -ItemType Directory -Path "$ClaudeSkillDir\$s" -Force | Out-Null
        Copy-Item -Path $scriptsSrc -Destination "$ClaudeSkillDir\$s\" -Recurse -Force
        Write-Host "  $(Write-Colored '✔' green) $s (scripts → ~/.claude/skills/$s/)"
      }
      Write-Host "  $(Write-Colored '✔' green) $s"
      $count++
    } else {
      Write-Host "  $(Write-Colored '✖' red) $s (not found)"
    }
  }

  # Copy root files
  foreach ($f in @(".gitignore", "LICENSE", "README.md")) {
    $fp = Join-Path $Src $f
    if (Test-Path $fp) { Copy-Item $fp $SkillDir -Force }
  }

  Write-Host ""
  Write-Host "  $(Write-Colored "Done! $count skill(s) installed" bold)"
  Write-Host "  SKILL.md  → $SkillDir"
  Write-Host "  Scripts   → $ClaudeSkillDir"
  Write-Host "  Pi will auto-detect them on next startup."
}

function Setup-Env {
  if (-not [Environment]::GetEnvironmentVariable("CLAUDE_PLUGIN_ROOT", "User")) {
    [Environment]::SetEnvironmentVariable("CLAUDE_PLUGIN_ROOT", $env:USERPROFILE, "User")
    $env:CLAUDE_PLUGIN_ROOT = $env:USERPROFILE
    Write-Host "  $(Write-Colored '✔' green) CLAUDE_PLUGIN_ROOT set to `"$env:USERPROFILE`" (persistent)"
  } else {
    Write-Host "  $(Write-Colored '✔' green) CLAUDE_PLUGIN_ROOT already set (value: $([Environment]::GetEnvironmentVariable('CLAUDE_PLUGIN_ROOT', 'User')))"
  }
}

# ====== Main ======
$IsCloned = Test-Path (Join-Path $PSScriptRoot ".git")

while ($true) {
  Show-Menu
  $input = Read-Host "  $(Write-Colored '→' bold) "

  switch -Regex ($input) {
    "^[qQ]$"      { Write-Host "  Aborted."; exit 0 }
    "^[iI]$"      { break }
    "^[aA]$"      { for ($i = 0; $i -lt $Skills.Count; $i++) { $Selected[$i] = 1 } }
    "^[nN]$"      { for ($i = 0; $i -lt $Skills.Count; $i++) { $Selected[$i] = 0 } }
    default {
      if ($input -match "^\d+$" -and [int]$input -ge 0 -and [int]$input -lt $Skills.Count) {
        $idx = [int]$input
        $Selected[$idx] = if ($Selected[$idx] -eq 1) { 0 } else { 1 }
      } else {
        # comma/space separated list
        $input = $input -replace ",", " "
        foreach ($n in ($input -split "\s+" | Where-Object { $_ -ne "" })) {
          if ($n -match "^\d+$" -and [int]$n -ge 0 -and [int]$n -lt $Skills.Count) {
            $idx = [int]$n
            $Selected[$idx] = if ($Selected[$idx] -eq 1) { 0 } else { 1 }
          }
        }
      }
    }
  }
}

Write-Host ""
Write-Host "$(Write-Colored 'Installing selected skills…' bold)"
Write-Host ""

if ($IsCloned) {
  Install-Skills $PSScriptRoot
} else {
  $tmp = Join-Path $env:TEMP "pi-skills-$([System.IO.Path]::GetRandomFileName())"
  New-Item -ItemType Directory -Path $tmp -Force | Out-Null
  try {
    Write-Host "  $(Write-Colored 'Cloning repo…' dim)"
    & git clone --depth 1 $RepoUrl "$tmp\repo" 2>&1 | Out-Null
    if (-not $?) { throw "git clone failed" }
    Install-Skills "$tmp\repo"
  } finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
  }
}

Write-Host ""
Setup-Env
Write-Host ""
Write-Host "  $(Write-Colored 'Tip: ls ~/.pi/agent/skills/  to verify.' dim)"