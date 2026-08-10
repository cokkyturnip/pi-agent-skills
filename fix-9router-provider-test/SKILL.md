---
name: fix-9router-provider-test
description: Use when a 9router provider shows testStatus "error" with lastError "Provider test not supported", or when adding test support for a new provider so the WebUI test button stops reporting that error.
---

# Fix 9router "Provider test not supported"

## Overview

When a 9router provider shows `testStatus: "error"` and `lastError: "Provider test not supported"`, the cause is a **missing `switch` case in the provider test utility** — not a bad API key, missing model, or combo misconfiguration. Each provider must explicitly have a test handler in `src/app/api/providers/[id]/test/testUtils.js` inside the `testApiKeyConnection()` function.

**CORE PRINCIPLE:** Adding a provider to the registry (`open-sse/providers/registry/<alias>.js`) does NOT automatically make it testable. The test handler is a separate, mandatory piece of code.

## Diagnosis (confirm before changing code)

```bash
DB="${APPDATA:+$APPDATA/9router/db/data.sqlite}"
[ -z "$DB" ] && DB="$HOME/.9router/db/data.sqlite"
sqlite3 "$DB" "SELECT provider, json_extract(data,'$.testStatus'), json_extract(data,'$.lastError') FROM providerConnections WHERE provider='<alias>';"
```

Confirmed if output shows `error` + `Provider test not supported`.

## Edit Location

File: `src/app/api/providers/[id]/test/testUtils.js` (in the 9router repo)

Inside `testApiKeyConnection(connection, effectiveProxy)`, add a new `case` before `default:`. Use the provider registry's `transport.validateUrl` as the endpoint and Bearer auth:

```js
case "<alias>": {
  const baseUrl = connection.providerSpecificData?.baseUrl || "<validate-url-minus-/models>";
  const res = await fetchWithConnectionProxy(`${baseUrl.replace(/\/$/, "")}/models`, {
    headers: { Authorization: `Bearer ${connection.apiKey}` },
  }, effectiveProxy);
  return { valid: res.ok, error: res.ok ? null : "Invalid API key or base URL" };
}
```

Get the correct base URL from `open-sse/providers/registry/<alias>.js` → `transport.validateUrl` (strip `/models` and any path suffix to get the API root).

> Only the Next.js app build is required for this fix — the CLI bundle does NOT include the API route. `npm run build` in repo root is sufficient; `npm --prefix cli run build` is unnecessary.

## Workflow

1. `git checkout master && git pull upstream master` (upstream = `decolua/9router`; origin = your fork)
2. Create branch: `git checkout -b fix/<provider>-provider-test`
3. Add the `case` in `testUtils.js` as above.
4. Verify: `git diff --check`
5. Build: `npm run build` (root)
6. Restart service: `kill <9router-pid>` then `nohup npm start > router.log 2>&1 &`
7. Test provider in the WebUI → must show active.
8. Commit: `git commit -am "fix(providers): add <provider> to provider test support"`
9. Push: `git push origin fix/<provider>-provider-test`
10. PR: `gh pr create --repo decolua/9router --base master --head <you>:fix/<provider>-provider-test`

## PR Rules

- **Each provider fix is an INDEPENDENT PR.** Never reference other pending PRs (sibling provider fixes) in the body — reviewers have no context for them and they may not be merged.
- Body should state: what was added, which endpoint it tests against, and that it was tested locally after build+restart.
- No CONTRIBUTING.md exists in the repo as of 0.5.50 — follow the conventional-commit style used by existing fix branches.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Updating the registry only | Registry ≠ test handler; both needed |
| Building the CLI for API-route changes | Only `npm run build` (root) needed |
| Referencing other open PRs in the body | Keep each PR independent |
| Guessing the base URL | Read it from `open-sse/providers/registry/<alias>.js` |
