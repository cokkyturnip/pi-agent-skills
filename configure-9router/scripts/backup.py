#!/usr/bin/env python3
"""
Configure 9router - Backup tool
Usage: python3 backup.py [9router] [-b path]
"""
import argparse, json, os, sqlite3
from datetime import datetime, timezone
from pathlib import Path

def get_home():
    return Path.home()

def get_9router_db():
    return get_home() / ".9router" / "db" / "data.sqlite"

def get_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

def backup_9router(out_path: Path):
    db = get_9router_db()
    if not db.exists():
        print(f"[!] 9router DB not found: {db}")
        return False

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    row = con.execute("SELECT data FROM settings WHERE id=1").fetchone()
    settings = json.loads(row["data"]) if row else {}

    def get_rows(table):
        if table not in tables: return []
        results = []
        cursor = con.execute(f"SELECT * FROM {table}")
        colnames = [d[0] for d in cursor.description]
        for r in cursor.fetchall():
            d = dict(r)
            if "data" in colnames and d.get("data"):
                try: d.update(json.loads(d["data"])); del d["data"]
                except Exception: pass
            if "models" in d and isinstance(d["models"], str):
                try: d["models"] = json.loads(d["models"])
                except Exception: pass
            if "isActive" in d: d["isActive"] = bool(d["isActive"])
            results.append(d)
        return results

    # customModels & disabledModels disimpan di table kv, bukan table sendiri
    def get_kv_models(scope_name):
        results = []
        if "kv" not in tables: return results
        rows = con.execute("SELECT key, value FROM kv WHERE scope=?", (scope_name,)).fetchall()
        for key, val in rows:
            try:
                obj = json.loads(val)
            except Exception:
                obj = {"id": key, "value": val}
            results.append(obj)
        return results

    backup = {
        "settings": settings,
        "providerConnections": get_rows("providerConnections"),
        "providerNodes": get_rows("providerNodes"),
        "proxyPools": get_rows("proxyPools"),
        "apiKeys": get_rows("apiKeys"),
        "combos": get_rows("combos"),
        "modelAliases": settings.get("modelAliases", {}),
        "customModels": get_kv_models("customModels"),
        "mitmAlias": {},
        "pricing": {},
    }
    con.close()

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)
    print(f"✓ 9router backup written → {out_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Configure 9router - Backup")
    parser.add_argument("--backup-dir", "-b", type=str, default=None, help="Output JSON file path")
    args = parser.parse_args()

    if args.backup_dir:
        out = Path(args.backup_dir)
    else:
        out = Path('.') / f"9router-backup-{get_timestamp()}.json"

    if backup_9router(out):
        print("✅ 9router backup complete!")
    else:
        print("❌ Backup failed.")

if __name__ == "__main__":
    main()