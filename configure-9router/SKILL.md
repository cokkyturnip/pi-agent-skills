---
name: configure-9router
description: Configure, classify, and maintain 9router model combos via SQLite. Use when the user wants to set up provider combos, register/whitelist models, manage routing, blacklist models, or curate the 9router database for lean multi-provider coverage.
---

# Skill: Configure 9router

This skill provides the operational framework for classifying, configuring, and maintaining 9router model combos via SQLite. It ensures a lean, efficient, and future-proof set of models across multiple providers.

---

## 0. 9router Config Tables (SQLite, default: ~/.9router/db/data.sqlite)

The primary configuration of 9router is stored in an SQLite database. To inspect, update configuration, or query the real-time model registry, query these tables:

| Table | Description | Primary Use Case |
|---|---|---|
| combos | Combo definitions (name, strategy/kind, models array, metadata) | Combo listing & fallback routing |
| kv | Key-value store (scope=customModels: model metadata; scope=disabledModels: blacklist) | Model registry & blacklists |
| providerConnections | Connection state, API endpoints, authentication keys, and priorities | Active providers |
| settings | Global env/router preferences and defaults stored as JSON | Global settings |
| apiKeys | Provider-specific API credentials mapped to connections | Access credentials |
| usageHistory | Execution logs tracking successful and failed requests | History & debugging |

Common access points:
- `combos` → combo configurations, strategies, model lists, and meta-combos.
- `kv` (scope=customModels) → registered and active models.
- `providerConnections` → provider status and priority order.
- `settings` → global configuration.

---

## 1. Decision Rule Table

When determining which combo a model belongs to, use this **priority order** (Reasoning > Code > Chat):

| Condition | Target Combo | Action |
|---|---|---|
| **Chat only** | `-Chat` | Add to `...-Chat` |
| **Chat + Code** | `-Code` | Add to `...-Code` (Chat ignored if Code present) |
| **Chat + Reasoning** | `-Thinking` | Add to `...-Thinking` (Chat ignored if Reasoning present) |
| **Code only** | `-Code` | Add to `...-Code` |
| **Reasoning only** | `-Thinking` | Add to `...-Thinking` |
| **Code + Reasoning** | **BOTH** | Add to BOTH `...-Code` AND `...-Thinking` |

### Verification Sources (Priority Order)
1. **Explicit Third-Party Tags**: `freellm.net` or NVIDIA NIM tags (e.g., `textcode`, `textreasoning`)
2. **Official Provider Docs**: Google AI, MiniMax, Mistral, OpenAI, etc. for "Reasoning", "Coding", "Agentic" labels
3. **Provider-Specific Metadata**: OpenRouter or API docs for `reasoning_effort` or `thinking` params

### Combo Deduplication Rules:
- Always keep **latest** (most current) version or **N-1** (one version older).
- **Tagging priority**: Prefer models with `cloud` over other tags (e.g., `latest` vs `cloud` → `cloud` wins).
- **Cloud/latest priority**: If there is competition between `cloud`/`latest` and a detailed name (e.g., `256b`), keep `cloud`/`latest` first.
- **Detailed naming rules**: Prefer `256b-cloud` over `256b` (if available).
- **Same model multiple sizes**: Keep **two largest sizes** only, UNLESS a `cloud` tag exists (in which case, defer to tagged version).
- **Cross-provider redundancy**: Retain duplicate models with the same ID across different providers — redundancy improves routing resilience.
- **Cascading updates**: If renaming or deleting a combo, immediately update all dependent meta-combos to prevent broken references.

---

## 2. Combo Creation SOP

### Step 1: Register Model (if not auto-discovered)
```sql
-- OpenRouter
INSERT INTO kv (scope,key,value) VALUES ('customModels','openrouter/provider/model:free','{"providerAlias":"openrouter","id":"provider/model:free","type":"llm","name":"model-name"}');

-- Provider native (e.g., NVIDIA NIM)
INSERT INTO kv (scope,key,value) VALUES ('customModels','nvidia/provider/model','{"providerAlias":"nvidia","id":"provider/model","type":"llm","name":"model-name"}');
```

### Step 2: Create/Update Combo
```bash
ID=$(python3 -c "import uuid;print(uuid.uuid4().hex)")
NOW=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
sqlite3 ~/.9router/db/data.sqlite "INSERT INTO combos (id,name,kind,models,createdAt,updatedAt) VALUES ('$ID','Name-Combo','','[\"provider/model1\",\"provider/model2\"]','$NOW','$NOW');"
```

### Step 3: Update Meta-Combos
```bash
# Always update ALL 3 meta-combos when adding/changing combos
sqlite3 ~/.9router/db/data.sqlite "UPDATE combos SET models='[\"Combo1\",\"Combo2\"]' WHERE name='Chat';"
sqlite3 ~/.9router/db/data.sqlite "UPDATE combos SET models='[\"Combo1\",\"Combo2\"]' WHERE name='Thinking';"
sqlite3 ~/.9router/db/data.sqlite "UPDATE combos SET models='[\"Combo1\",\"Combo2\"]' WHERE name='Coding';"
```

---

## 3. Model Deletion SOP

Model deletion involves a two-stage process: remove the model from the registry (`kv`) and remove the model from combo definitions (`combos`). Both steps must be performed to ensure the model is fully purged from routing.

### Step 1: Delete from kv (Provider Registry)
```sql
-- Remove model from registry
DELETE FROM kv WHERE key = 'provider/model-id' AND scope = 'customModels';

-- Verify removal
SELECT * FROM kv WHERE key = 'provider/model-id';
```

### Step 2: Remove from Combos
```sql
-- Identify all combos containing the model
SELECT id, name, models FROM combos WHERE models LIKE '%provider/model-id%';

-- Update combo: remove model from the JSON array
-- Example: if "Deepseek-Code" combo contains the model to be deleted
UPDATE combos SET models = '["model1","model2"]' WHERE id = 'combo-id';
```

### Step 3: Update Meta-Combos (if combo is deleted)
If a combo is deleted entirely, update the meta-combos (`Chat`, `Coding`, `Thinking`) to remove the references:
```sql
-- Example: remove "Deepseek-Code" from the "Coding" meta-combo
UPDATE combos SET models = '["Gemini-Code","Qwen3-Code",...]' WHERE name = 'Coding';
```

### Final Verification
```sql
-- Confirm model is absent from kv
SELECT * FROM kv WHERE key LIKE '%model-id%';

-- Confirm model is absent from all combos
SELECT id, name FROM combos WHERE models LIKE '%model-id%';
```

### Critical Notes
- **API Provider Models**: Models loaded automatically from API providers (NVIDIA, OpenRouter, etc.) will remain visible in the provider UI even if removed from the local `kv`. To prevent routing selection, ensure they are removed from all active combos.
- **UI Cache**: Some interfaces may cache the model list. Clear the cache or restart the router service after applying changes.
- **Combo Cleanup**: Deleting from `kv` alone is insufficient — models remain selectable via combos that still include them.

---

## 4. Combo Audit (Health Check)

Use the `audit_combo.py` script located in the skill directory (`~/.pi/agent/skills/configure-9router/scripts/audit_combo.py`) to inspect the usage status of all models within a combo, including nested models in sub-combos.

### Usage:
```bash
python3 ~/.pi/agent/skills/configure-9router/scripts/audit_combo.py <ComboName>
```

### Examples:
```bash
python3 ~/.pi/agent/skills/configure-9router/scripts/audit_combo.py Coding
python3 ~/.pi/agent/skills/configure-9router/scripts/audit_combo.py Chat
python3 ~/.pi/agent/skills/configure-9router/scripts/audit_combo.py Thinking
```

### Output Categories:
- **🟢 OK Models**: Models that have been used successfully, including usage counts and last-used timestamps.
- **🔴 Error Models**: Models with status records other than `ok`, detailing failure counts, last failure timestamps, and error messages (if available in the `meta` column).
- **⚪ Unused Models**: Models present in a combo but never recorded in `usageHistory`.

### Audit Technical Details:
- The script reads the default SQLite database path at `~/.9router/db/data.sqlite`.
- Sub-combos are traversed recursively.
- The script checks **TWO ERROR SOURCES**:
  1. **`usageHistory`**: Records transactions with `status: 'ok'`. Errors here only appear if the request was definitively recorded as a failure in the database.
  2. **`providerConnections`**: Stores **provider-level errors** including model locks (models temporarily disabled due to errors). Errors such as 402 (insufficient credits), 429 (rate limit), 404 (entity not found), 500/502/503 (server errors), etc., are tracked here.
- **Note**: Errors observed in the 9router UI typically originate from `providerConnections`, not `usageHistory`. This clarifies why errors may appear in the UI while remaining absent from `usageHistory` logs.
- Models locked (`modelLock_*`) appear under `PROVIDER-LEVEL ERRORS` in the audit output.
- Audit utility objectives:
  - Prune unused models.
  - Identify models with high failure rates.
  - Inspect provider-specific errors (insufficient credits, timeouts, rate limits).

### Common Error Codes:
- **402**: Payment required / credits exhausted. Needs upgrade or max_token limit adjustments.
- **429**: Rate limit or daily free allocation exhausted.
- **404**: Model not found at provider.
- **500/502/503**: Server error / timeout / model overloaded.
- **modelLock_***: Models temporarily disabled due to the aforementioned errors.

---

## 5. Backup & Restore Config

Independent 9router backup/restore tools. Compatible with UI export/import.

### Backup
```bash
# Creates ~/Downloads/9router-backup-<timestamp>.json
python3 ~/.pi/agent/skills/configure-9router/scripts/backup.py

# Or specify output path:
python3 ~/.pi/agent/skills/configure-9router/scripts/backup.py -b /path/to/backup.json
```

### Restore
```bash
python3 ~/.pi/agent/skills/configure-9router/scripts/restore.py -i /path/to/backup.json

# Dry-run:
python3 ~/.pi/agent/skills/configure-9router/scripts/restore.py -i /path/to/backup.json --dry-run
```

---

## 6. Routing Strategy (via settings table)

> ⚠️ The `combos.kind` column in SQLite is **NOT read by the router**. Routing strategy lives in the `settings` table.

### Inventory Combo 9router (Current State)
Total 21 combos active:
- **Chat**: 2 models
- **Coding**: 8 models
- **Deepseek-Code**: 6 models
- **Deepseek-Thinking**: 9 models
- **GLM-5-Code**: 3 models
- **GLM-5-Thinking**: 3 models
- **Gemini-Chat**: 4 models
- **Gemini-Code**: 3 models
- **Gemini-Thinking**: 8 models
- **Kimi-Code**: 2 models
- **Minimax-Code**: 5 models
- **Minimax-Thinking**: 3 models
- **Mistral-Code**: 2 models
- **Nemotron-Thinking**: 5 models
- **OpenAI-Chat**: 3 models
- **OpenAI-Thinking**: 5 models
- **Qwen3-Code**: 6 models
- **Tencent-Thinking**: 2 models
- **Thinking**: 9 models
- **fetch-combo**: 2 models
- **search-combo**: 3 models

### Meta-Combos (Legacy mapping, reference settings.comboStrategies for live routing)
| Meta-Combo | Contains |
|---|---|
| **Chat** | OpenAI-Chat, Mistral-Chat |
| **Thinking** | Deepseek-Thinking, GLM-5-Thinking, Gemini-Thinking, Gemma4-Thinking, Mimo-Thinking, Minimax-Thinking, Nemotron-Thinking, OpenAI-Thinking, Tencent-Thinking |
| **Coding** | GLM-5-Code, Kimi-Code, Minimax-Code, Mistral-Code, Qwen3-Code |

---

## 7. `kind` (Routing Strategy) Values — **DEPRECATED/NOT USED**

> ⚠️ **CRITICAL DISCOVERY**: The `combos.kind` column in SQLite is **NOT read by the router**. It has no effect on routing behavior.

The **actual routing strategy** is stored in the **`settings`** table (JSON column `data`, key `comboStrategies`).

### Valid strategy values (in `settings.comboStrategies[name].fallbackStrategy`):

| Value | Behavior | Default? |
|:---|:---|:---|
| `"fallback"` | Tries models in order; falls to next on failure | ✅ **Yes — default when not set** |
| `"round-robin"` | Rotates evenly across all models each request | No — set manually |

### How to change strategy (must use settings table, NOT combos.kind):
```sql
-- Read current comboStrategies from settings
SELECT data FROM settings WHERE id=1;
```
Then update the JSON `comboStrategies` field with the desired `fallbackStrategy` per combo.

**Default policy**: Leave as `"fallback"` (default). Use `"round-robin"` only when explicitly requested by user.

---

**Legacy note**: Previously this skill incorrectly documented `kind` values. `combos.kind` is unused. The correct field is `settings.data.comboStrategies[*].fallbackStrategy`.

---

## 8. Key Rules (ALWAYS FOLLOW)

1. **Suffix consistency**: All Model-* combos must use `-Chat`, `-Code`, or `-Thinking` suffix. No bare names.
2. **Meta-combo alignment**: Meta-combos (`Chat`, `Coding`, `Thinking`) contain ONLY combo names with matching suffix. No mixed content.
3. **No dangling references**: When renaming/deleting, immediately update ALL meta-combos that reference it.
4. **File safety**: **NEVER use `write` to overwrite the full SKILL.md.** Always use `edit` to change specific blocks. Inventory at the bottom is a STATUS reference, not a replacement for rules.
5. **Backup before edit/write**: Always run the **pre-edit hook** **before** any `write` or `edit` to `SKILL.md`:
   ```bash
   bash scripts/hooks/pre-edit.sh
   ```
   This creates a timestamped backup in `configure-9router/scripts/backup/` and auto-deletes backups older than 14 days.
6. **Verify before trust**: When poking combos/models, always query SQLite directly (see §0). Never guess combo/model content from memory — confirm with `sqlite3`.