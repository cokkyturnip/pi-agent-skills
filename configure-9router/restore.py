#!/usr/bin/env python3
"""
Configure 9router - Restore tool
Usage: python3 restore.py [9router] -i <path> [--dry-run]
"""
import argparse, json, os, shutil, sqlite3
from pathlib import Path

def get_home():
    return Path.home()

def get_9router_db():
    return get_home() / ".9router" / "db" / "data.sqlite"

RESTORE_TABLES = [
    "providerConnections", "providerNodes", "proxyPools",
    "apiKeys", "combos",
]

TABLE_SCHEMAS = {
    "providerConnections": {
        "cols": ["id", "provider", "authType", "name", "email", "priority", "isActive", "data", "createdAt", "updatedAt"],
        "data_cols": ["id", "provider", "authType", "name", "email", "priority", "isActive", "createdAt", "updatedAt"],
    },
    "providerNodes": {
        "cols": ["id", "type", "name", "data", "createdAt", "updatedAt"],
        "data_cols": ["id", "type", "name", "createdAt", "updatedAt"],
    },
    "proxyPools": {
        "cols": ["id", "name", "data", "createdAt", "updatedAt"],
        "data_cols": ["id", "name", "createdAt", "updatedAt"],
    },
    "apiKeys": {
        "cols": ["id", "key", "name", "machineId", "isActive", "createdAt"],
        "data_cols": None,
    },
    "combos": {
        "cols": ["id", "name", "kind", "models", "createdAt", "updatedAt"],
        "data_cols": None,
    },
}

def restore_9router(input_path: Path, dry_run: bool = False):
    db_path = get_9router_db()

    if not input_path.exists():
        print(f"[!] Backup file not found: {input_path}")
        return False

    if not db_path.exists():
        print(f"[!] 9router DB not found: {db_path}")
        print("    Run 9router once first to create the database.")
        return False

    with open(input_path, "r", encoding="utf-8") as f:
        backup = json.load(f)

    if dry_run:
        print(f"[dry-run] would restore {len(backup.get('combos', []))} combos, "
              f"{len(backup.get('providerConnections', []))} connections")
        return True

    db_bak = db_path.with_suffix(f".restore-bak-{os.getpid()}")
    shutil.copy2(db_path, db_bak)
    print(f"✓ DB backed up → {db_bak.name}")

    con = sqlite3.connect(str(db_path))
    try:
        if "settings" in backup:
            settings_json = json.dumps(backup["settings"], ensure_ascii=False)
            con.execute("UPDATE settings SET data = ? WHERE id = 1", (settings_json,))
            print("✓ settings restored")

        if backup.get("customModels"):
            con.execute("DELETE FROM kv WHERE scope = 'customModels'")
            for model in backup["customModels"]:
                alias = model.get("providerAlias", "")
                model_id = model.get("id", "")
                key = f"{alias}/{model_id}" if alias else model_id
                con.execute(
                    "INSERT OR REPLACE INTO kv (scope, key, value) VALUES (?, ?, ?)",
                    ("customModels", key, json.dumps(model, ensure_ascii=False)),
                )
            print(f"✓ {len(backup['customModels'])} custom models restored")

        for table_name in RESTORE_TABLES:
            rows = backup.get(table_name, [])
            if not rows: continue

            schema = TABLE_SCHEMAS.get(table_name)
            if not schema: continue

            con.execute(f"DELETE FROM {table_name}")

            for row in rows:
                if schema["data_cols"] is not None:
                    known = schema["data_cols"]
                    data_extras = {k: v for k, v in row.items() if k not in known}
                    col_dict = {k: row[k] for k in known if k in row}
                    if "isActive" in col_dict:
                        col_dict["isActive"] = 1 if col_dict["isActive"] else 0
                    col_dict["data"] = json.dumps(data_extras, ensure_ascii=False)

                    cols = list(col_dict.keys())
                    placeholders = ",".join(["?"] * len(cols))
                    col_str = ",".join(cols)
                    con.execute(
                        f"INSERT OR REPLACE INTO {table_name} ({col_str}) VALUES ({placeholders})",
                        [col_dict[c] for c in cols],
                    )
                else:
                    col_vals = {}
                    for c in schema["cols"]:
                        if c in row:
                            v = row[c]
                            if isinstance(v, list):
                                v = json.dumps(v, ensure_ascii=False)
                            if c == "isActive":
                                v = 1 if v else 0
                            col_vals[c] = v
                        else:
                            col_vals[c] = None

                    cols = list(col_vals.keys())
                    placeholders = ",".join(["?"] * len(cols))
                    col_str = ",".join(cols)
                    con.execute(
                        f"INSERT OR REPLACE INTO {table_name} ({col_str}) VALUES ({placeholders})",
                        [col_vals[c] for c in cols],
                    )

            print(f"✓ {table_name}: {len(rows)} rows restored")

        con.commit()
        print(f"\n Previous DB saved as: {db_bak.name}")
        print(f" Delete after verifying: rm '{db_bak}'")

    except Exception as e:
        con.rollback()
        print(f"\n❌ Error: {e}")
        print(f"Restoring backup: {db_bak} → {db_path}")
        shutil.copy2(db_bak, db_path)
        return False
    finally:
        con.close()

    return True

def main():
    parser = argparse.ArgumentParser(description="Configure 9router - Restore")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input JSON backup file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    if restore_9router(input_path, args.dry_run):
        print("\n✅ 9router restore complete!")
    else:
        print("\n❌ Restore failed.")

if __name__ == "__main__":
    main()