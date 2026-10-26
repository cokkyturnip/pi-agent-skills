---
name: opencode-go-quota
description: Check OpenCode Go subscription quota windows (rolling, weekly, monthly) and detect expired OpenCode credentials. Use when asking how much OpenCode Go/Zen quota is used or remaining, when a plan limit or rate limit may be the cause of a failed request, when checking whether an OpenCode Console session or Go API key is still valid, or when setting up quota monitoring/alerting.
---

# OpenCode Go Quota

Reports how much of each OpenCode Go subscription window is already consumed.
Reads live state from OpenCode's usage endpoint; adds no stored state.

## Run it

```bash
python3 scripts/check_quota.py
```

```
OpenCode Go quota
----------------------------------------------
window       used  status   reset
rolling        0%  ok       2026-10-26 14:41 WIB (in 4h 24m)
weekly         0%  ok       2026-11-02 07:00 WIB (in 6d 20h)
monthly       68%  ok       2026-11-13 18:21 WIB (in 18d 8h)
----------------------------------------------
```

Resolve `scripts/` relative to this skill's directory. Stdlib only — no
install step, no npm/python dependencies.

Flags:

| Flag | Effect |
|---|---|
| `--json` | print the raw usage payload (for other tools) |
| `--threshold N` | exit **2** when the monthly window is at or above `N` percent |
| `--models` | also report whether the models catalogue is reachable |

Exit codes: `0` ok, `1` error, `2` threshold exceeded.

## Data source

`GET https://opencode.ai/zen/go/v1/usage` returns:

```json
{"usage":{"rolling":{"status":"ok","percent":0,"resetsAt":"...Z"},
          "weekly":{"status":"ok","percent":0,"resetsAt":"...Z"},
          "monthly":{"status":"ok","percent":68,"resetsAt":"...Z"}}}
```

`percent` is the share of that window's allowance already consumed, not what
remains. Windows observed in the wild: `rolling` (short, hours),
`weekly`, `monthly`. The script renders any additional window keys it finds.

This route is **not in OpenCode's published API docs** — it landed as an
internal console endpoint. Do not present it to a user as a stable contract.

## Authentication

The endpoint takes the **OpenCode Console session token**, not a Go API key.

The script obtains it by shelling out to `opencode auth export` and reading the
`opencode` integration's `access` value. The token stays in memory: it is never
printed, logged, or written to disk, and when the transport is `curl` it travels
over stdin via `--config -` so it does not appear in the process list.

A **Go API key** (`OPENCODE_API_KEY`, or the `opencode-go` auth entry) is a
different credential. When one is expired the server answers:

```json
{"error":{"type":"authentication_error","code":"api_key_expired",
 "message":"This API key has expired. Create a new API key in OpenCode Console and replace it in your client or secret store. Signing in again will not renew this key."}}
```

That means inference through the `opencode-go` provider will fail until the key
is replaced in OpenCode Console. Report this to the user as a blocking problem —
a quota check can still succeed with a stale key, because quota uses the console
session instead.

If the script reports `no OpenCode Console session found`, the user must run
`opencode auth login`.

## Interpreting results

- `0%` on rolling and weekly with a high `monthly` is a **plan-allowance**
  situation, not a short-term rate limit — short-window throttling is not the
  cause of a failure.
- A high `monthly` near its `resetsAt` means the plan is nearly spent for the
  rest of that period; suggest cheaper or free models rather than retrying.
- `status` other than `ok` means the provider is reporting a degraded window —
  surface it verbatim instead of guessing.
- Never claim a request failed *because of* quota without showing the numbers.

## Notes

- Requires the `opencode` CLI on `PATH` for credential retrieval; `curl` is used
  for HTTP when present, otherwise Python's `urllib`.
- On macOS, `urllib` may fail with `CERTIFICATE_VERIFY_FAILED` when Python lacks
  a CA bundle. The `curl` transport exists for this reason — keep it preferred.
- Reads only. This skill never buys credits, changes plans, or rotates keys.
