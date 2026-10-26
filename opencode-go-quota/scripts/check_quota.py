#!/usr/bin/env python3
"""Query OpenCode Go (and Zen) subscription quota windows.

Auth: reuses the OpenCode Console session that the `opencode` CLI already
stores. The token is read in-memory from `opencode auth export` and is never
printed or written to disk.

Endpoint: GET https://opencode.ai/zen/go/v1/usage
  -> {"usage":{"rolling":{...},"weekly":{...},"monthly":{...}}}
  Each window: {"status":"ok","percent":N,"resetsAt":"ISO8601"}

Stdlib only. Exit codes: 0 ok, 1 error, 2 threshold exceeded.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USAGE_URL = "https://opencode.ai/zen/go/v1/usage"
MODELS_URL = "https://opencode.ai/zen/v1/models"
TIMEOUT = 20
ORDER = ("rolling", "weekly", "monthly")
LABELS = {
    "rolling": "rolling",
    "weekly": "weekly",
    "monthly": "monthly",
}


def console_token() -> tuple[str | None, str | None]:
    """Return (access_token, error). Reads `opencode auth export`."""
    try:
        proc = subprocess.run(
            ["opencode", "auth", "export"],
            capture_output=True,
            text=True,
            timeout=40,
        )
    except FileNotFoundError:
        return None, "`opencode` CLI not found in PATH"
    except subprocess.TimeoutExpired:
        return None, "`opencode auth export` timed out"

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        return None, f"`opencode auth export` failed: {detail[0] if detail else proc.returncode}"

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, "could not parse `opencode auth export` output as JSON"

    entries = payload if isinstance(payload, list) else payload.get("entries", [])
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("integrationID") != "opencode":
            continue
        value = entry.get("value") or {}
        token = value.get("access")
        if token:
            return token, None
    return None, "no OpenCode Console session found - run `opencode auth login`"


def fetch(url: str, token: str) -> tuple[dict | None, str | None]:
    """GET a JSON endpoint.

    Uses curl when available (system CA store, and the bearer token travels
    over stdin so it never appears in the process list). Falls back to urllib.
    """
    curl = shutil.which("curl")
    if curl:
        config = (
            f'header = "Authorization: Bearer {token}"\n'
            'header = "Accept: application/json"\n'
            'header = "User-Agent: pi-opencode-go-quota/1.0"\n'
        )
        proc = subprocess.run(
            [curl, "-sS", "--config", "-", "-m", str(TIMEOUT), "-w", "\n%{http_code}", url],
            input=config,
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 15,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or "").strip().splitlines()
            return None, f"curl failed: {detail[0] if detail else proc.returncode}"
        body, _, status_line = proc.stdout.rpartition("\n")
        try:
            status = int(status_line.strip())
        except ValueError:
            return None, f"could not read HTTP status from curl output"
        return _parse_response(body, status, url)

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "pi-opencode-go-quota/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as exc:
        return _parse_response(exc.read().decode(errors="replace"), exc.code, url)
    except urllib.error.URLError as exc:
        return None, f"network error reaching {url}: {exc.reason}"
    except TimeoutError:
        return None, f"timeout reaching {url}"


def _parse_response(body: str, status: int, url: str) -> tuple[dict | None, str | None]:
    if 200 <= status < 300:
        try:
            return json.loads(body), None
        except json.JSONDecodeError:
            return None, f"non-JSON response from {url}: {body[:200]}"

    code = ""
    message = body[:200]
    try:
        err = json.loads(body).get("error", {})
        code = err.get("code", "")
        message = err.get("message", message)
    except (json.JSONDecodeError, AttributeError):
        pass
    if code == "api_key_expired" or status == 401:
        return None, (
            "401 unauthorized - the credential is expired or invalid.\n"
            "  Fix: create a new API key in OpenCode Console, then "
            "`opencode auth login`.\n"
            f"  Server said: {message}"
        )
    return None, f"HTTP {status} from {url}: {message}"


def local_time(iso: str | None) -> str:
    if not iso:
        return "-"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return iso
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone().strftime("%Y-%m-%d %H:%M %Z")


def human_delta(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    seconds = (dt - datetime.now(timezone.utc)).total_seconds()
    if seconds <= 0:
        return "resetting"
    days, rem = divmod(int(seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"in {days}d {hours}h"
    if hours:
        return f"in {hours}h {minutes}m"
    return f"in {minutes}m"


def render(usage: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(usage, indent=2, sort_keys=True))
        return

    print("OpenCode Go quota")
    print("-" * 46)
    print(f"{'window':<10} {'used':>6}  {'status':<8} reset")
    for key in ORDER:
        window = usage.get(key)
        if not isinstance(window, dict):
            continue
        percent = window.get("percent")
        status = window.get("status", "?")
        resets = window.get("resetsAt")
        pct = f"{percent}%" if percent is not None else "?"
        print(
            f"{LABELS.get(key, key):<10} {pct:>6}  {status:<8} "
            f"{local_time(resets)} ({human_delta(resets)})"
        )

    extra = sorted(set(usage) - set(ORDER))
    for key in extra:
        window = usage[key]
        if isinstance(window, dict):
            print(
                f"{key:<10} {str(window.get('percent', '?')) + '%':>6}  "
                f"{window.get('status', '?'):<8} {local_time(window.get('resetsAt'))}"
            )
    print("-" * 46)
    print("percent = share of that window's allowance already consumed")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check OpenCode Go subscription quota windows.",
    )
    parser.add_argument(
        "--json", action="store_true", help="print the raw usage payload"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        metavar="N",
        help="exit 2 if the monthly window is at or above N percent (for scripts/alerts)",
    )
    parser.add_argument(
        "--models",
        action="store_true",
        help="also report whether the models catalogue is reachable",
    )
    args = parser.parse_args()

    token, err = console_token()
    if not token:
        print(f"error: {err}", file=sys.stderr)
        return 1

    payload, err = fetch(USAGE_URL, token)
    if err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    usage = payload.get("usage") if isinstance(payload, dict) else None
    if not isinstance(usage, dict):
        print(f"error: unexpected payload from {USAGE_URL}: {payload!r}", file=sys.stderr)
        return 1

    render(usage, args.json)

    if args.models:
        _, model_err = fetch(MODELS_URL, token)
        print(
            "models catalogue: "
            + ("unreachable - " + model_err if model_err else "reachable")
        )

    if args.threshold is not None:
        monthly = usage.get("monthly") or {}
        percent = monthly.get("percent")
        if isinstance(percent, (int, float)) and percent >= args.threshold:
            print(
                f"threshold: monthly usage {percent}% >= {args.threshold}%",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
