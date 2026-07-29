---
name: creatio-ai-cost-estimator
description: Use when estimating costs for Creatio AI platform (AI Actions/credits) and custom LLM model usage. Covers per-module token calculations, multi-tier model strategies, user profiling, and budget forecasting for BUMN/enterprise deployment. Use when user asks about AI cost, budget, pricing, ROI, or feasibility of Creatio + LLM integration.
---

# Creatio AI Cost Estimator

Skill personal — **JANGAN di-push ke GitHub publik**. Hanya untuk konsumsi pribadi.

---

## 1. Framework Dasar

Setiap estimasi biaya AI punya **dua komponen terpisah** yang tidak boleh dicampur:

| Komponen | Dibayar ke | Basis tagihan |
|----------|-----------|---------------|
| **Creatio AI Actions** | Creatio (langganan) | Per AI Action (bukan per token) |
| **Token LLM** | Provider LLM (OpenAI, Deka LLM, dll.) | Per 1M token (input / output) |

> **Aturan emas:** 1 AI Action = 1 completed interaction AI Agent dengan LLM. Mau pake GPT-4.1 atau Nemotron-120B, tetap 1 AI Action. Harga AI Action TIDAK berubah berdasarkan model.

---

## 2. Referensi Pricing

### 2.1 Default — state-of-llm-apis

Gunakan skill `state-of-llm-apis` sebagai referensi default untuk:
- Harga token per provider (OpenAI, Anthropic, Google, DeepSeek, dll.)
- Perbandingan model dan kapabilitas
- Deprecation schedule

> **Wajib update** `state-of-llm-apis` jika >24 jam sejak update terakhir (skill sudah punya auto-update mechanism).

### 2.2 Khusus Residensi Indonesia — Deka LLM (Cloudeka/Lintasarta)

Jika user menyebut **NFR-11**, **data residency Indonesia**, atau **regulasi BUMN**, gunakan pricing Deka LLM:

| Model | Input/1M token (Rp) | Output/1M token (Rp) | Kategori |
|-------|:-------------------:|:--------------------:|:--------:|
| Gemma-4 | 2,394 | 6,840 | Low (7B-10B) |
| Nemotron-3-Super 120B | 2,736 | 13,680 | Medium/High (≥70B) |

> **Sumber:** docs.cloudeka.ai/deka-llm/model-catalog. Verifikasi harga terbaru sebelum final.

### 2.3 Tier Paket Creatio AI (per 2026)

| Paket | AI Actions/tahun | Estimasi harga |
|-------|:----------------:|:--------------:|
| Start | 500,000 | ~$5k |
| **Grow** | **1,500,000** | **~$25k** |
| Accelerate | 4,000,000 | ~$75k? |
| Scale | 8,000,000 | ~$125k? |

> **⚠️** Pricing perlu konfirmasi dari sales Creatio. Angka di atas estimasi berdasarkan diskusi dengan user.

---

## 3. Metodologi Estimasi

### 3.1 Profil User

Jangan pernah pakai total user tanpa filter. Rasio standar:

| Tipe User | Persentase | Contoh aktivitas |
|-----------|:----------:|------------------|
| Power user (analis, auditor, humas) | ~10% | 15 actions/hari |
| Regular user (staff operasional) | ~10% | 8 actions/hari |
| Viewer/ringan (manajemen, reviewer) | ~80% | 1 action/hari |

> Rasio **20% aktif : 80% viewer** adalah asumsi default untuk enterprise. Sesuaikan jika user punya data aktual.

### 3.2 Kategori Konsumsi Token per AI Action

Setiap AI action di Creatio mengirimkan: **system prompt + task input + CoT + few-shot + format instructions**. System prompt di-repeat setiap action, tidak di-cache.

| Kategori | Input/action | Output/action | Contoh modul |
|:--------:|:------------:|:-------------:|:-------------|
| **Low** | 12,000 | 1,200 | Sentiment, entity extraction, EWS alert, talent search |
| **Medium** | 30,000 | 4,500 | Summarization, RAG, legal Q&A, financial analysis |
| **High** | 75,000 | 12,000 | Audit summary, multi-doc reasoning, compliance deep-dive |

> **3× multiplier dari naive estimate** — berdasarkan pengalaman nyata bahwa enterprise AI action menghabiskan 20-30k+ token setelah system prompt, CoT, skill instructions, dan context.

### 3.3 Strategi Multi-Tier Model

Jika biaya custom model perlu ditekan, bagi model per kategori:

| Kategori | % Actions | Model ideal |
|:--------:|:---------:|:------------|
| Low | 60% | Model ringan (Gemma-4, Llama-3-8B) |
| Medium | 30% | Model enterprise (Llama-3-70B, Qwen-2.5-72B) |
| High | 10% | Model heavy (Nemotron-120B, >100B) |

### 3.4 Buffer

Selalu tambahkan **buffer 25%** untuk:
- Retry dan error recovery
- Testing oleh pengembang
- Lonjakan pemakaian (end of quarter, audit season)
- Prompt iterations

---

## 4. Rumus Cepat

### Total AI Actions / tahun

```
(total_user × rasio_aktif × actions_per_hari × 25_hari) + batch_actions
```

### Biaya Token Custom Model

```
(total_input_tokens × harga_input + total_output_tokens × harga_output) × 1.25_buffer
```

### Total Biaya

```
biaya_creatio_ai_package + biaya_token_provider
```

> **Built-in GPT**: biaya token = $0 (termasuk dalam AI Actions).
> **Custom model**: bayar AI Actions + token provider.

---

## 5. Alur Kerja

1. **Tanya profil user** — Berapa total user? Berapa yang aktif? Dari BUMN apa saja?
2. **Tanya modul** — Modul Creatio apa saja yang pakai AI? (Media monitoring, audit, legal, dll.)
3. **Hitung AI Actions** — Batch (system) + Interactive (user queries)
4. **Tentukan model** — Built-in GPT atau custom? Jika custom, pilih provider.
5. **Hitung token** — Per kategori Low/Medium/High. Jangan lupa 3× multiplier.
6. **Cek pricing** — state-of-llm-apis untuk default, Deka LLM untuk NFR-11.
7. **Tambahkan buffer 25%**.
8. **Cocokkan ke tier Creatio** — Start/Grow/Accelerate/Scale.
9. **Sajikan dua skenario**: Built-in GPT vs Custom Model.

---

## 6. Catatan Penting

- **AI Action ≠ token cost**: Dua hal terpisah. AI Action = biaya platform, token = biaya komputasi model.
- **Custom model = double cost**: Tetap bayar AI Actions + token ke provider. Built-in GPT sudah include token.
- **Selisih Built-in vs Custom** bisa 0-40% tergantung volume token dan model yang dipilih.
- **Embedding untuk RAG** belum termasuk hitungan di atas. Estimasi Rp 500-1,000/1k token untuk model embedding.
- Jika user aktif bertambah, AI Actions bisa naik drastis — pantau utilisasi paket.
