#!/usr/bin/env python3
"""
audit_combo.py - Audit 9router combo health, including nested combos.
Checks usageHistory AND providerConnections for errors.
"""
import sqlite3
import json
import os
import sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/.9router/db/data.sqlite")

def get_db_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_nested_models(conn, item):
    """Recursively fetch models from a combo name or return [item] if it's a model."""
    if "/" in item:
        return [item]
    
    cursor = conn.cursor()
    cursor.execute("SELECT models FROM combos WHERE name = ?", (item,))
    row = cursor.fetchone()
    if not row:
        return [item]
        
    try:
        models_list = json.loads(row["models"])
    except Exception:
        return [item]
        
    nested = []
    for m in models_list:
        nested.extend(get_nested_models(conn, m))
    return nested

def get_provider_errors(conn):
    """Fetch all provider-level errors from providerConnections."""
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT provider, name, data FROM providerConnections")
        rows = cursor.fetchall()
        errors = {}
        for row in rows:
            try:
                conn_data = json.loads(row["data"])
            except Exception:
                conn_data = {}
            
            provider = row["provider"] or "unknown"
            
            # Extract error info
            last_error = conn_data.get("lastError")
            last_error_at = conn_data.get("lastErrorAt")
            error_code = conn_data.get("errorCode")
            test_status = conn_data.get("testStatus")
            backoff_level = conn_data.get("backoffLevel", 0)
            
            # Extract model locks (models temporarily disabled due to errors)
            model_locks = {}
            for key, value in conn_data.items():
                if key.startswith("modelLock_") and value is not None:
                    model_name = key.replace("modelLock_", "")
                    model_locks[model_name] = value
            
            if last_error or model_locks:
                errors[provider] = {
                    "last_error": last_error,
                    "last_error_at": last_error_at,
                    "error_code": error_code,
                    "test_status": test_status,
                    "backoff_level": backoff_level,
                    "model_locks": model_locks
                }
        
        return errors
    except Exception:
        return {}

def get_disabled_models(conn):
    """Fetch all disabled/blacklisted models."""
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM kv WHERE scope = 'disabledModels'")
    rows = cursor.fetchall()
    
    disabled = {}
    for row in rows:
        provider = row["key"]
        try:
            models = json.loads(row["value"])
        except:
            models = []
        disabled[provider] = models
    
    return disabled

def audit_combo(combo_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Resolve all models
    cursor.execute("SELECT models FROM combos WHERE name = ?", (combo_name,))
    combo_row = cursor.fetchone()
    if not combo_row:
        print(f"Error: Combo '{combo_name}' not found.")
        conn.close()
        return
        
    try:
        raw_items = json.loads(combo_row["models"])
    except Exception as e:
        print(f"Error decoding JSON models for combo {combo_name}: {e}")
        conn.close()
        return

    all_models = []
    for item in raw_items:
        all_models.extend(get_nested_models(conn, item))
    all_models = sorted(list(set(all_models)))
    
    if not all_models:
        print(f"No models found in combo '{combo_name}'.")
        conn.close()
        return

    # 2. Get provider-level errors and disabled models
    provider_errors = get_provider_errors(conn)
    disabled_models = get_disabled_models(conn)
    
    # Flatten disabled models for easy lookup
    all_disabled = []
    for provider, models in disabled_models.items():
        for m in models:
            all_disabled.append(f"{provider}/{m}" if not m.startswith("@") else m)

    print(f"\n{'='*60}")
    print(f"AUDIT REPORT FOR COMBO: {combo_name}")
    print(f"Total resolved models: {len(all_models)}")
    print(f"{'='*60}\n")

    ok_models = []
    error_models = []
    no_usage_models = []
    disabled_in_combo = []

    # 3. Query usageHistory for resolved models
    for model in all_models:
        # Check if model is disabled/blacklisted
        clean_model = model.split('/')[-1] if '/' in model else model
        is_disabled = any(d == model or d.endswith(f"/{clean_model}") for d in all_disabled)
        
        # Check exact and suffix
        cursor.execute("""
            SELECT status, COUNT(*) as count, MAX(timestamp) as last_used, meta
            FROM usageHistory 
            WHERE model = ? OR model = ? OR model LIKE ?
            GROUP BY status
        """, (model, clean_model, f"%/{clean_model}"))
        
        rows = cursor.fetchall()
        
        if not rows:
            if is_disabled:
                disabled_in_combo.append({"model": model, "reason": "blacklisted/disabled"})
            else:
                no_usage_models.append(model)
            continue
            
        for row in rows:
            status = row["status"]
            count = row["count"]
            last_used = row["last_used"]
            
            # Extract error message if present in meta
            err_msg = None
            if row["meta"]:
                try:
                    meta_data = json.loads(row["meta"])
                    if isinstance(meta_data, dict):
                        err_msg = meta_data.get("error") or meta_data.get("message") or meta_data.get("errorMessage")
                except:
                    pass

            entry = {
                "model": model,
                "count": count,
                "last_used": last_used,
                "error_msg": err_msg,
                "status": status,
                "disabled": is_disabled
            }
            
            if status == "ok":
                ok_models.append(entry)
            else:
                error_models.append(entry)

    # 4. Check provider-level errors that might affect these models
    provider_affected_models = []
    for provider, error_info in provider_errors.items():
        if error_info["model_locks"]:
            for locked_model, lock_time in error_info["model_locks"].items():
                # Check if locked model is in our combo
                for combo_model in all_models:
                    if locked_model in combo_model or combo_model.endswith(f"/{locked_model}"):
                        provider_affected_models.append({
                            "model": combo_model,
                            "provider": provider,
                            "error": error_info["last_error"],
                            "error_code": error_info["error_code"],
                            "locked_at": lock_time,
                            "test_status": error_info["test_status"]
                        })

    # Output OK Models
    print(f"🟢 OK MODELS ({len(ok_models)}):")
    if ok_models:
        for m in sorted(ok_models, key=lambda x: x["last_used"] or "", reverse=True):
            print(f"  - {m['model']} (Used {m['count']}x, Last: {m['last_used']})")
    else:
        print("  None")

    # Output Error Models (from usageHistory)
    print(f"\n🔴 USAGE HISTORY ERRORS ({len(error_models)}):")
    if error_models:
        for m in sorted(error_models, key=lambda x: x["last_used"] or "", reverse=True):
            err_str = f" | Error: {m['error_msg']}" if m['error_msg'] else ""
            print(f"  - {m['model']} (Status: {m['status']}, Failed {m['count']}x, Last: {m['last_used']}{err_str})")
    else:
        print("  None")

    # Output Provider-Level Errors (from providerConnections)
    print(f"\n⚠️  PROVIDER-LEVEL ERRORS AFFECTING COMBO ({len(provider_affected_models)}):")
    if provider_affected_models:
        for m in sorted(provider_affected_models, key=lambda x: x["locked_at"] or "", reverse=True):
            print(f"  - {m['model']}")
            print(f"    Provider: {m['provider']} | Status: {m['test_status']}")
            print(f"    Error [{m['error_code']}]: {m['error']}")
            print(f"    Locked at: {m['locked_at']}")
    else:
        print("  None")

    # Output Disabled/Blacklisted Models
    print(f"\n🚫 DISABLED/BLACKLISTED MODELS IN COMBO ({len(disabled_in_combo)}):")
    if disabled_in_combo:
        for m in disabled_in_combo:
            print(f"  - {m['model']} ({m['reason']})")
    else:
        print("  None")

    # Output Unused Models
    print(f"\n⚪ UNUSED MODELS IN HISTORY ({len(no_usage_models)}):")
    if no_usage_models:
        for m in no_usage_models:
            print(f"  - {m}")
    else:
        print("  None")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY:")
    print(f"  Total models in combo: {len(all_models)}")
    print(f"  Successfully used: {len(ok_models)}")
    print(f"  Usage history errors: {len(error_models)}")
    print(f"  Provider-level errors: {len(provider_affected_models)}")
    print(f"  Disabled/blacklisted: {len(disabled_in_combo)}")
    print(f"  No usage recorded: {len(no_usage_models)}")
    print(f"{'='*60}\n")

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 audit_combo.py <ComboName>")
        print("Example: python3 audit_combo.py Coding")
        sys.exit(1)
    audit_combo(sys.argv[1])
