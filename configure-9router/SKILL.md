---
name: configure-9router
description: Configure, classify, and maintain 9router model combos via SQLite. Use when the user wants to set up provider combos, register/whitelist models, manage routing, blacklist models, or curate the 9router database for lean multi-provider coverage.
---

# Skill: Configure 9router

This skill provides the operational framework for classifying, configuring, and maintaining 9router model combos via SQLite. It ensures a lean, efficient, and future-proof set of models across multiple providers.

---

## 0. 9router Config Tables (SQLite, default: ~/.9router/db/data.sqlite)

Konfigurasi utama 9router tersimpan di database SQLite. Untuk melihat/set konfigurasi atau daftar model real-time, gunakan table ini:

| Table                | Isi utama                                                                                                       | Penting untuk |
|----------------------|---------------------------------------------------------------------------------------------------------------|---------------|
| combos               | Definisi combo (name, kind/strategy, models array, created/updated)                                            | Daftar combo + routing |
| kv                   | Key-value (scope=customModels: metadata/registrasi model, disabledModels: blacklist, scope lainnya: env/dev)  | Model registry, blacklist, misc |
| providerConnections  | Data koneksi/provider (API key/jenis auth/status, id, priority, dsb)                                           | Provider aktif |
| settings             | Dict JSON untuk env global/router, preferensi dan default                                                      | Setting global |
| apiKeys              | API key, per provider, linked ke koneksi                                                                      | Kunci akses |
| usageHistory         | Log pemakaian, untuk analitik/history                                                                         | History, debugging |

Akses paling umum:
- `combos` → daftar combo, strategi, model, meta-combo
- `kv` (scope=customModels) → model yang diregistrasi/di-enable
- `providerConnections` → status & urutan prioritas provider "aktif"
- `settings` → global config

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
- **Tagging priority:** Prefer models with `cloud` over other tags (e.g., `latest` vs `cloud` → `cloud` wins).
- **Cloud/latest priority:** If there is competition between `cloud`/`latest` and a detailed name (e.g., `256b`), keep `cloud`/`latest` first.
- **Detailed naming rules:** Prefer `256b-cloud` over `256b` (if available).
- **Same model multiple sizes:** Keep **two largest sizes** only, UNLESS a `cloud` tag exists (in which case, defer to tagged version).
- **Cross-provider preservation:** Retain duplicate models with the same ID across different providers — redundancy improves routing resilience.
- **Rename/Delete cascading:** If renaming or deleting a combo, immediately update all meta-combos and references to avoid dangling entries.
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

Model deletion melibatkan dua tahap: hapus dari registry (`kv`) dan hapus dari combo (`combos`). Kedua langkah harus dilakukan agar model benar-benar hilang dari routing.

### Step 1: Delete from kv (Provider Registry)
```sql
-- Hapus model dari registry
DELETE FROM kv WHERE key = 'provider/model-id' AND scope = 'customModels';

-- Verifikasi sudah tidak ada
SELECT * FROM kv WHERE key = 'provider/model-id';
```

### Step 2: Remove from Combos
```sql
-- Cari semua combo yang mengandung model tersebut
SELECT id, name, models FROM combos WHERE models LIKE '%provider/model-id%';

-- Update combo: hapel model dari array JSON
-- Contoh: jika combo Deepseek-Code mengandung model yang akan dihapus
UPDATE combos SET models = '["model1","model2"]' WHERE id = 'combo-id';
```

### Step 3: Update Meta-Combos (jika combo dihapus)
Jika combo dihapus sepenuhnya, update meta-combos (`Chat`, `Coding`, `Thinking`) untuk menghapus referensi:
```sql
-- Contoh: hapus Deepseek-Code dari meta-combo Coding
UPDATE combos SET models = '["Gemini-Code","Qwen3-Code",...]' WHERE name = 'Coding';
```

### Verifikasi Akhir
```sql
-- Pastikan model tidak ada di kv
SELECT * FROM kv WHERE key LIKE '%model-id%';

-- Pastikan model tidak ada di combo manapun
SELECT id, name FROM combos WHERE models LIKE '%model-id%';
```

### Catatan Penting
- **Model dari API Provider**: Model yang di-load otomatis dari API provider (NVIDIA, OpenRouter, dll) akan tetap muncul di UI provider meskipun sudah dihapus dari `kv` lokal. Untuk mencegah penggunaan, pastikan model juga dihapus dari semua combo.
- **Cache UI**: Beberapa UI mungkin mem-cache daftar model. Clear cache atau restart layanan router setelah perubahan.
- **Jangan lupa combo**: Hapus dari `kv` saja tidak cukup — model masih bisa dipilih via combo yang memuatnya.

---

## 4. Combo Audit (Health Check)

Gunakan script `audit_combo.py` yang sudah disertakan di dalam direktori skill (`~/.pi/agent/skills/configure-9router/audit_combo.py`) untuk memeriksa status penggunaan semua model dalam sebuah combo (termasuk model nested di sub-combo).

### Cara penggunaan:
```bash
python3 ~/.pi/agent/skills/configure-9router/audit_combo.py <NamaCombo>
```

### Contoh:
```bash
python3 ~/.pi/agent/skills/configure-9router/audit_combo.py Coding
python3 ~/.pi/agent/skills/configure-9router/audit_combo.py Chat
python3 ~/.pi/agent/skills/configure-9router/audit_combo.py Thinking
```

### Output:
- **🟢 OK Models**: model yang pernah digunakan dan selalu sukses, dengan jumlah pemakaian dan waktu terakhir.
- **🔴 Error Models**: model dengan record status selain `ok`, dengan jumlah kegagalan, waktu terakhir, dan pesan error (jika tersedia di kolom `meta`).
- **⚪ Unused Models**: model yang ada di combo tapi belum pernah muncul di `usageHistory`.

### Catatan Penting Audit:
- Script membaca database default di `~/.9router/db/data.sqlite`.
- Semua sub-combo ditelusuri secara rekursif.
- Script sekarang memeriksa **DUA SUMBER ERROR**:
  1. **`usageHistory`**: Mencatat transaksi yang berhasil (`status: 'ok'`). Error dari sini hanya muncul jika request benar-benar tercatat gagal di database.
  2. **`providerConnections`**: Menyimpan **provider-level errors** termasuk model locks (model yang sementara dinonaktifkan karena error). Error seperti 402 (kredit habis), 429 (rate limit), 404 (entity tidak ditemukan), 500/502/503 (server error), dsb. tercatat di sini.
- **PENTING**: Error yang terlihat di UI 9router biasanya berasal dari `providerConnections`, bukan `usageHistory`. Ini menjelaskan mengapa ada error di UI tetapi tidak ditemukan di log `usageHistory`.
- Model yang terkunci (`modelLock_*`) akan terlihat di bagian `PROVIDER-LEVEL ERRORS` dalam output audit.
- Audit ini berguna untuk:
  - Membersihkan model-model yang tidak pernah dipakai.
  - Mengidentifikasi model dengan tingkat kegagalan tinggi.
  - Melihat error spesifik dari provider (kredit habis, timeout, rate limit, dll).

### Contoh Temuan Error:
- **402**: Kredit/provider habis, perlu upgrade atau kurangi max_tokens.
- **429**: Rate limit / daily free allocation exhausted.
- **404**: Model tidak ditemukan di provider.
- **500/502/503**: Server error / timeout / model sedang sibuk.
- **modelLock_***: Model yang sementara dinonaktifkan karena error tersebut.

---

## 5. Backup & Restore Config

Independent 9router backup/restore tools. Compatible with UI export/import.

### Backup
```bash
# Creates ~/Downloads/9router-backup-<timestamp>.json
python3 ~/.pi/agent/skills/configure-9router/backup.py

# Or specify output path:
python3 ~/.pi/agent/skills/configure-9router/backup.py -b /path/to/backup.json
```

### Restore
```bash
python3 ~/.pi/agent/skills/configure-9router/restore.py -i /path/to/backup.json

# Dry-run:
python3 ~/.pi/agent/skills/configure-9router/restore.py -i /path/to/backup.json --dry-run
```

---

## 6. Routing Strategy (via settings table)

> ⚠️ `combos.kind` column in SQLite is **NOT read by the router**. Routing strategy lives in `settings` table.

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

## 5. `kind` (Routing Strategy) Values — **DEPRECATED/NOT USED**

> ⚠️ **CRITICAL DISCOVERY**: The `combos.kind` column in SQLite is **NOT read by the router**. It has no effect on routing behavior.

The **actual routing strategy** is stored in the **`settings`** table (JSON column `data`, key `comboStrategies`).

### Valid strategy values (in `settings.comboStrategies[name].fallbackStrategy`):

| Value | Behavior | Default? |
|:---|:---|:---|
| `"fallback"` | Tries model in order; falls to next on failure | ✅ **Yes — default when not set** |
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

## 6. Key Rules (ALWAYS FOLLOW)

1. **Suffix consistency**: All Model-* combos must use `-Chat`, `-Code`, or `-Thinking` suffix. No bare names.
2. **Meta-combo alignment**: Meta-combos (`Chat`, `Coding`, `Thinking`) contain ONLY combo names with matching suffix. No mixed content.
3. **No dangling references**: When renaming/deleting, immediately update ALL meta-combos that reference it.
4. **File safety**: **NEVER use `write` to overwrite the full SKILL.md.** Always use `edit` to change specific blocks. Inventory at the bottom is a STATUS reference, not a replacement for rules.
5. **Backup before edit/write**: Always run the **pre-edit hook** **before** any `write` or `edit` to `SKILL.md`:
   ```bash
   bash hooks/pre-edit.sh
   ```
   This creates a timestamped backup in `configure-9router/backup/` and auto-deletes backups older than 14 days.
6. **Verify before trust**: When poking combos/models, always query SQLite directly (see §0). Never guess combo/model content from memory — confirm with `sqlite3`.