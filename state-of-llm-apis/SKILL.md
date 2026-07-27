---
name: state-of-llm-apis
description: Referensi database LLM API yang di-update otomatis tiap hari. Berisi spesifikasi, pricing, perbandingan model, changelog, dan jadwal deprecation dari semua major provider (OpenAI, Anthropic, Google, Mistral, xAI, DeepSeek, Cohere, Meta). Gunakan ketika user bertanya tentang detail model LLM tertentu, perbandingan harga, rekomendasi model, atau status deprecation.
---

# Skill: State of LLM APIs

Skill ini menyediakan akses ke **living knowledge base** LLM API yang di-maintain otomatis oleh Model Tracker agent dari repo [janwilmake/state-of-llm-apis](https://github.com/janwilmake/state-of-llm-apis). Data di-update setiap hari dari official provider documentation.

---

## ⚡ Auto-Update Mechanism (WAJIB)

Setiap kali skill ini dipanggil (user nanya tentang model LLM), **WAJIB** jalankan auto-check ini **SEBELUM** baca data:

```bash
# 1. Baca timestamp update terakhir
LAST_UPDATE=$(cat ~/.pi/agent/skills/state-of-llm-apis/.last_update)
NOW=$(date +%s)
DIFF=$((NOW - LAST_UPDATE))

# 2. Kalo udah > 24 jam (86400 detik), update dulu
if [ $DIFF -gt 86400 ]; then
  echo "Data udah >24 jam. Update dulu..."
  cd ~/.pi/agent/skills/state-of-llm-apis/data && git pull
  date +%s > ~/.pi/agent/skills/state-of-llm-apis/.last_update
  echo "✅ Data updated: $(date)"
fi
```

> **Aturan:** Jangan tanya user dulu. Langsung update otomatis kalo udah lebih dari 24 jam sejak `.last_update`.

---

## 📁 Struktur Data

Semua data ada di direktori: `~/.pi/agent/skills/state-of-llm-apis/data/`

| File | Deskripsi |
|---|---|
| `comparison.md` | Side-by-side pricing & feature matrix semua major provider |
| `changelog.md` | Chronological log perubahan harga, rilis model, deprecations |
| `deprecated.md` | Sunset dates dan migration paths |
| `models/openai.md` | OpenAI — GPT-5.x, o-series, GPT-4.1 |
| `models/anthropic.md` | Anthropic — Claude Fable/Mythos/Opus/Sonnet/Haiku |
| `models/google.md` | Google — Gemini 3.x, 2.5 series |
| `models/mistral.md` | Mistral — Large/Medium/Small/Nemo |
| `models/xai.md` | xAI — Grok 4.x series |
| `models/deepseek.md` | DeepSeek — V4 series |
| `models/cohere.md` | Cohere — Command A/R series |
| `models/meta.md` | Meta — Llama 4 Scout/Maverick |

---

## 🔍 Cara Pakai

### 1. Menjawab pertanyaan tentang model spesifik

Baca file model yang relevan:

```bash
# Contoh: OpenAI
read ~/.pi/agent/skills/state-of-llm-apis/data/models/openai.md

# Contoh: Anthropic  
read ~/.pi/agent/skills/state-of-llm-apis/data/models/anthropic.md
```

### 2. Perbandingan harga dan spesifikasi

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/comparison.md
```

### 3. Tracking perubahan terbaru

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/changelog.md
```

### 4. Cek jadwal deprecation

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/deprecated.md
```

---

## 📊 Quick Reference: File per Provider

| Provider | File Path |
|---|---|
| OpenAI | `~/.pi/agent/skills/state-of-llm-apis/data/models/openai.md` |
| Anthropic | `~/.pi/agent/skills/state-of-llm-apis/data/models/anthropic.md` |
| Google | `~/.pi/agent/skills/state-of-llm-apis/data/models/google.md` |
| Mistral | `~/.pi/agent/skills/state-of-llm-apis/data/models/mistral.md` |
| xAI | `~/.pi/agent/skills/state-of-llm-apis/data/models/xai.md` |
| DeepSeek | `~/.pi/agent/skills/state-of-llm-apis/data/models/deepseek.md` |
| Cohere | `~/.pi/agent/skills/state-of-llm-apis/data/models/cohere.md` |
| Meta | `~/.pi/agent/skills/state-of-llm-apis/data/models/meta.md` |
| Comparison Matrix | `~/.pi/agent/skills/state-of-llm-apis/data/comparison.md` |
| Changelog | `~/.pi/agent/skills/state-of-llm-apis/data/changelog.md` |
| Deprecation | `~/.pi/agent/skills/state-of-llm-apis/data/deprecated.md` |

---

## 🔄 Update Manual dari Terminal

Kalo mau update dari terminal langsung:

```bash
update-llm-models
```

---

## 📝 Catatan Penting

- **Last updated** timestamp ada di header setiap file — selalu cek ini untuk tau seberapa fresh datanya
- Harga dalam USD per 1M token kecuali disebut lain
- Status deprecation ada tanda ⚠️ atau ❌ di comparison.md
- Provider coverage: OpenAI, Anthropic, Google, Mistral, xAI, DeepSeek, Cohere, Meta