#!/usr/bin/env python3
"""
Configure Pi - Backup tool
Usage: python3 backup.py [pi] [-b path]
"""
import argparse, json, os, shutil
from datetime import datetime, timezone
from pathlib import Path

def get_home():
    return Path.home()

def get_pi_dir():
    return get_home() / ".pi" / "agent"

def get_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

PI_FILES = [
    "auth.json",
    "settings.json",
    "9router-config.json",
    "AGENTS.md",
    "notion.json",
    "notion-mcp-auth.json",
    "web-search.json",
    "stitch-api-key",
]

PI_DIRS = ["skills", "extensions"]
EXCLUDE_DIRS = {"sessions"}
EXCLUDE_FILES = {"models-store.json", "settings.json.bak"}

def backup_pi(target: Path) -> bool:
    src = get_pi_dir()
    if not src.exists():
        print(f"[!] Pi agent dir not found: {src}")
        return False

    target.mkdir(parents=True, exist_ok=True)

    for f in PI_FILES:
        fp = src / f
        if fp.exists():
            shutil.copy2(fp, target / f)
            print(f"  ✓ {f}")

    for d in PI_DIRS:
        dp = src / d
        if dp.exists():
            shutil.copytree(
                dp, target / d,
                ignore=shutil.ignore_patterns(*EXCLUDE_DIRS, *EXCLUDE_FILES),
                ignore_dangling_symlinks=True,
                dirs_exist_ok=True
            )
            print(f"  ✓ {d}/")

    hooks_eng = src / "hooks" / "engine"
    if hooks_eng.exists():
        hooks_out = target / "hooks" / "engine"
        hooks_out.mkdir(parents=True, exist_ok=True)
        for f in hooks_eng.iterdir():
            if f.is_file():
                shutil.copy2(f, hooks_out / f.name)
        print(f"  ✓ hooks/engine/")

    return True

def main():
    parser = argparse.ArgumentParser(description="Configure Pi - Backup")
    parser.add_argument("--backup-dir", "-b", type=str, default=None)
    args = parser.parse_args()

    if args.backup_dir:
        out = Path(args.backup_dir)
    else:
        out = Path('.') / f"pi-backup-{get_timestamp()}"

    out.mkdir(parents=True, exist_ok=True)
    print(f"Backup Pi → {out}\n")

    if backup_pi(out):
        print(f"\n✅ Backup complete: {out}")
    else:
        print("\n❌ Backup failed")

if __name__ == "__main__":
    main()