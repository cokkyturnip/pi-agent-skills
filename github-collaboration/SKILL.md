---
name: github-collaboration
description: Use when contributing to an upstream repository via fork, branch, PR, or any GitHub collaboration workflow
---

# GitHub Collaboration

## Overview

**Core principle:** Always read and follow the target repository's CONTRIBUTING.md before submitting any contribution. Never submit a PR without verifying CI checks pass and the contribution guidelines are met.

## When to Use

- Before opening a pull request to an upstream repository
- When unsure about a repository's contribution rules
- After making code changes that need to be submitted upstream
- When CI checks fail and you need to verify compliance
- When managing forks, branches, or remote repositories for collaboration

## Prompt Template

When you need to contribute to an upstream repository, use this template to structure your workflow:

```
I want to contribute to <owner>/<repo>. Follow the github-collaboration skill:

1. Read the CONTRIBUTING.md at https://raw.githubusercontent.com/<owner>/<repo>/main/CONTRIBUTING.md
2. Fork the repo: gh repo fork <owner>/<repo> --remote
3. Clone: git clone https://github.com/<my-username>/<repo>.git
4. Add upstream: git remote add upstream https://github.com/<owner>/<repo>.git
5. Create branch: git checkout -b <descriptive-name>
6. Make changes
7. Run CI checks: <commands from CONTRIBUTING.md>
8. Push: git push -u origin <branch-name>
9. Create PR: gh pr create --repo <owner>/<repo> --title "<title>" --body "<description>"
10. Monitor CI and respond to review
```

Replace `<owner>`, `<repo>`, `<my-username>`, `<descriptive-name>`, `<title>`, and `<description>` with actual values.

## The Five Phases

### Phase 1: Read CONTRIBUTING.md

**BEFORE doing anything else**, fetch and read the target repository's `CONTRIBUTING.md`:

```
1. Fetch: https://raw.githubusercontent.com/<owner>/<repo>/main/CONTRIBUTING.md
2. If not found, try: https://raw.githubusercontent.com/<owner>/<repo>/master/CONTRIBUTING.md
3. If not found, check for CONTRIBUTING.md in the repo root via GitHub web UI
4. Read the entire document — every rule matters
```

**Key things to look for:**
- Required CI checks (lint, format, typecheck, test)
- Branch naming conventions
- PR title/description templates
- Required reviews or approvals
- Version bump requirements
- License agreements

### Phase 2: Prepare Your Branch

```bash
# Fork the repo if you haven't already
gh repo fork <owner>/<repo> --remote

# Clone your fork
git clone https://github.com/<your-username>/<repo>.git
cd <repo>

# Add upstream remote
git remote add upstream https://github.com/<owner>/<repo>.git

# Create a descriptive branch name
git checkout -b <descriptive-branch-name>
```

### Phase 3: Make Changes and Verify Locally

**Run ALL checks the CONTRIBUTING.md requires before pushing:**

```bash
# Example (adjust based on what CONTRIBUTING.md specifies):
bun run ci              # lint + format
bun run typecheck       # TypeScript checking
bun test                # all tests
```

**If any check fails:**
- Fix the issue locally
- Re-run the checks
- Only push when ALL checks pass

### Phase 4: Push and Create PR

```bash
# Push your branch
git push -u origin <branch-name>

# Create PR using gh CLI (preferred)
gh pr create \
  --title "<clear, descriptive title>" \
  --body "<description of changes, referencing any relevant issues>" \
  --repo <owner>/<repo>
```

**If `gh` is not available**, use the GitHub web UI:
1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill in the PR template exactly as CONTRIBUTING.md specifies
4. Submit

### Phase 5: After PR Submission

- Monitor CI checks on the PR page
- If CI fails, fix locally and push again
- Respond to review feedback promptly
- Once merged, clean up your branch and fork if desired

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping CONTRIBUTING.md | Always read it first — it saves time |
| Pushing without running CI locally | Run all checks before pushing |
| Vague PR title | Use clear, descriptive titles |
| Ignoring CI failures | Fix them before asking for review |
| Merging without approval | Wait for maintainer approval |

## Quick Reference

| Step | Command |
|------|---------|
| Fetch CONTRIBUTING.md | `curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/CONTRIBUTING.md` |
| Fork repo | `gh repo fork <owner>/<repo> --remote` |
| Create branch | `git checkout -b <name>` |
| Run CI checks | `bun run ci` (or per CONTRIBUTING.md) |
| Push branch | `git push -u origin <branch>` |
| Create PR | `gh pr create --repo <owner>/<repo>` |
| Check PR status | `gh pr checks <pr-number> --repo <owner>/<repo>` |

## Real-World Impact

Following CONTRIBUTING.md ensures your PR is accepted quickly without unnecessary back-and-forth. It shows respect for the maintainer's workflow and increases the chances of your contribution being merged.
