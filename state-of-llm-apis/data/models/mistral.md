# Mistral AI Model Catalog

> **Source:** [Mistral API Pricing](https://mistral.ai/pricing) · [Mistral Docs Model Cards](https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04) · [OpenRouter](https://openrouter.ai/mistralai/mistral-medium-3-5) · **Verified:** 2026-07-13

---

## Current Models

### Mistral Medium 3.5 (Released 2026-04-29 Preview / GA 2026-05-05) 🆕 NEW

Mistral's new flagship model — merges instruction-following, reasoning, coding, and vision into a single 128B dense model. Replaces Mistral Medium 3.1 and Magistral in Le Chat; replaces Devstral 2 in the Vibe coding agent. Released as open weights under a **Modified MIT** license.

| Metric | Value |
|---|---|
| API name | `mistral-medium-3-5` |
| Parameters | 128B (dense) |
| Context window | 256,000 tokens |
| Input | **$1.50 / 1M** |
| Output | **$7.50 / 1M** |
| License | Modified MIT (open weights) |

**Capabilities:** Vision (custom encoder with variable image sizes), tool calling, configurable reasoning effort (`reasoning_effort` parameter), structured outputs, agentic tool use.  
**Self-hosting:** Requires as few as four GPUs.  
**Replaces:** `mistral-medium-3.1` in Le Chat and Magistral; `devstral-medium-2507` in Vibe.  
**Benchmarks:** 77.6% SWE-Bench Verified (treat as directional; see independent evaluations before production use).

> ⚠️ **Note:** Mistral Large 2.1 (`mistral-large-2411`) is deprecated — retires **2026-05-31**. Migrate to `mistral-large-latest` (Mistral Large 3).

*Source: [Mistral blog](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5) · [Official model card](https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04) · [OpenRouter](https://openrouter.ai/mistralai/mistral-medium-3-5) — verified 2026-05-11*

---

### Mistral Large 3 (Released 2025-12-01)

| Metric | Value |
|---|---|
| API name | `mistral-large-latest` / `mistral-large-2512` |
| Parameters | 675B total / 41B active (MoE) |
| Context window | 262,144 tokens |
| Input | **$0.50 / 1M** |
| Output | **$1.50 / 1M** |
| Cached input | $0.05 / 1M |
| License | Apache 2.0 (open weights) |
| Speed | ~44 tok/s |

**Best for:** Complex reasoning, instruction-following, multilingual tasks requiring large-model capability at low cost.  
> Note: Mistral Large 3 is a significant price reduction from Mistral Large 2411 (which was $2.00/$6.00). Output corrected from $2.00 → $1.50 per 1M tokens (verified 2026-04-15 via OpenRouter, PricePerToken, Serenities AI, Holori).

---

### Mistral Small 4 (Released 2026-03-16)

A major update that unifies Magistral (reasoning), Pixtral (vision), and Devstral (coding) into one model.

| Metric | Value |
|---|---|
| API name | `mistral-small-2603` |
| Context window | 262,144 tokens |
| Input | **$0.15 / 1M** |
| Output | **$0.60 / 1M** |
| Weights | Open — [HuggingFace](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) |

**Best for:** Multimodal tasks, coding, reasoning on a budget. Capable of vision, tools, and complex analysis in a single model.

---

### Mistral Medium 3 (Released 2025-05-07)

| Metric | Value |
|---|---|
| API name | `mistral-medium-3` |
| Context window | 131,072 tokens |
| Input | **$0.40 / 1M** |
| Output | **$2.00 / 1M** |
| Speed | ~56 tok/s |

**Best for:** Coding, retrieval-augmented generation, agentic workflows at moderate cost.

---

### Devstral 2 (Released 2025-12-01)

Coding-specialist model optimized for agentic software development. 262K context, open weights.

| Context | Input | Cached | Output |
|---|---|---|---|
| 262,144 tokens | **$0.40 / 1M** | $0.04 / 1M | **$0.90 / 1M** |

> Output price corrected from $2.00 → $0.90 per 1M tokens (verified 2026-04-15 via PricePerToken, OpenRouter).

---

### Mistral Nemo

Ultra-cheap 12B model for simple, high-volume tasks.

| Context | Input | Output |
|---|---|---|
| 128,000 tokens | **$0.02 / 1M** | **$0.06 / 1M** |

Cheapest Mistral model. Good for classification, extraction, simple summaries.

---

### Codestral

Code completion model with FIM (fill-in-middle) support.

| Context | Pricing |
|---|---|
| 32,000 tokens | Varies (check [mistral.ai/pricing](https://mistral.ai/pricing)) |

---

### Mistral Large 2411 (Legacy)

| Input | Output |
|---|---|
| $2.00 / 1M | $6.00 / 1M |

Older Mistral Large version. Largely superseded by Mistral Large 3 at a quarter of the price.

---

## Mistral OCR 4 (Released 2026-06-23) 🆕 NEW

State-of-the-art document intelligence model. Successor to OCR 3 (`mistral-ocr-2512`, released Dec 2024). Adds **bounding boxes**, **block classification** (title, table, equation, signature, etc.), and **inline confidence scores** alongside extracted text. Deployed in a single container for self-hosted setups.

| Metric | Value |
|---|---|
| API name | `mistral-ocr-4-0` / `mistral-ocr-latest` |
| Languages | 170 languages across 10 language groups |
| API pricing | **$4.00 / 1,000 pages** (Batch API: $2.00 / 1,000 pages — 50% off) |
| Document AI pricing | $5.00 / 1,000 pages |
| Max pages per request | 1,000 |
| Max file size | 50 MB |
| Self-hosting | ✅ Single container deployment |
| Available on | Mistral API, Mistral AI Studio, Amazon SageMaker, Microsoft Foundry, Snowflake (coming soon) |

**Key facts:**
- 72% preferred over competitors in blind human evaluations (600+ documents, 12+ languages)
- #1 on OlmOCRBench (score: 85.20)
- `mistral-ocr-latest` alias updated to point to OCR 4 as of 2026-06-23
- Accepts PDF, DOC, PPT, OpenDocument formats
- `include_blocks: true` parameter returns paragraph-level bounding boxes with structural labels in reading order
- `pages` parameter accepts comma-separated digits and ranges (e.g. `"0,2-4"`)

*Source: [Mistral — OCR 4](https://mistral.ai/news/ocr-4/) · [Mistral Changelog](https://docs.mistral.ai/resources/changelogs) — 2026-06-23 · verified 2026-07-09*

---

## Robostral Navigate (Released 2026-07-08) 🆕 NEW

Mistral's first **embodied navigation model**. An 8B model that enables robots to autonomously navigate complex environments using only a single RGB camera and plain-language instructions.

| Metric | Value |
|---|---|
| Parameters | 8B |
| Input | RGB image + text instruction |
| Benchmark | 76.6% success on unseen R2R-CE benchmarks |
| API access | **Enterprise/commercial only** — contact Mistral sales team |
| Pricing | Not publicly listed (enterprise licensing) |

**Key facts:**
- Hardware-agnostic — works with any robot platform
- No LiDAR or depth sensors required (single RGB camera only)
- Trained entirely on simulated data; generalizes to real-world obstacles unseen during training
- Combines pointing-based navigation with reinforcement learning
- Applications: manufacturing, delivery, logistics, hospitality
- No public hobbyist/non-commercial license announced

*Source: [Mistral — Robostral Navigate](https://mistral.ai/news/robostral-navigate/) — 2026-07-08 · verified 2026-07-09*

---

## Leanstral 1.5 (Released 2026-06-30) 🆕 NEW — Retires 2026-09-30

Updated Lean 4 formal proof engineering model. Successor to Leanstral (`labs-leanstral-2603`, retired June 30). Not a general-purpose LLM — specialized for theorem proving and formal verification in Lean 4.

| Metric | Value |
|---|---|
| API name | `labs-leanstral-1-5` |
| Category | Labs (experimental) |
| Release date | 2026-06-30 |
| Retirement date | **2026-09-30** |
| Improvements | Better SFT mixture quality; extended long-context reasoning |

**Developer note:** Only relevant for teams using Lean 4 for formal verification or theorem proving. Not a general instruction model.

*Source: [Mistral Changelog — June 30, 2026](https://docs.mistral.ai/resources/changelogs) — verified 2026-07-12*

---

## New: Voxtral TTS (Released 2026-03-26)

Open source text-to-speech model for enterprise voice agents.

- Supports 9 languages: English, French, German, Spanish, Dutch, Portuguese, Italian, Hindi, Arabic
- Optimized for edge devices (smartwatch, smartphone, laptop)
- Competing with ElevenLabs, Deepgram, OpenAI TTS
- Open source — self-hostable
- API pricing: TBD on la Plateforme

---

## Mistral Studio (Launched 2026-07-09) 🆕 NEW

Mistral launched **Studio** on July 9, 2026 — a prompt and skills management system for teams building AI applications. Described as "a system of record" for prompts and skills: versioned, owned, and traceable.

**Key capabilities:**
- **Version control for prompts and skills:** Full edit history, rollback, and diff view
- **Ownership and traceability:** Track who created or modified each prompt/skill, with timestamps
- **Integration with La Plateforme:** Connect directly to your running models; test prompt changes in-place without re-deploying
- **Team collaboration:** Share and fork prompts across workspaces
- **MCP connector integration:** Reuse prompt skills as MCP tools via the built-in and custom MCP connectors shipped in May 2026

**Access:** Available on Pro, Team, and Enterprise Le Chat plans. Also accessible via the API as prompt templates.

**Developer note:** Particularly useful for production prompt engineering workflows — replaces ad-hoc prompt version tracking in notebooks or git. Works alongside the Mistral Vibe coding agent and Mistral Search Toolkit (launched May 28, 2026).

*Source: [Mistral — Studio launch](https://mistral.ai/news/) — 2026-07-09 · verified 2026-07-13*

---

## Le Chat Subscription Plans

| Plan | Price | Notes |
|---|---|---|
| Free | $0 | ~25 messages/day on mid-tier models |
| Pro | **$14.99/month** | ~150 messages/day, all models, Mistral Vibe coding, 15 GB storage |
| Student | **$7.04/month** | Same as Pro, requires .edu email |
| Team | **$24.99/user/month** | 30 GB storage/user, domain verification, data export |
| Enterprise | Custom | SAML SSO, audit logs, white-label, admin API |

Cheapest premium AI chat subscription among major providers (vs. $20 for ChatGPT Plus or Claude Pro).

---

## API Free Tier

"Experiment" tier: rate-limited access for testing and prototyping. Add a payment method for production workloads.

---

## ⚠️ Security Advisory: PyPI Supply Chain Attack — `mistralai==2.4.6` (2026-05-11)

On May 11, 2026, a coordinated supply chain attack published a **malicious version** of the official Mistral Python SDK to PyPI: `mistralai==2.4.6`. This version was never released by Mistral AI.

**Impact:** The malicious package contained a backdoor that fires at import time on Linux hosts. It downloads and executes a credential-stealing payload targeting API keys, cloud credentials, CI/CD tokens, and GitHub access tokens. Some variants included a destructive branch (`rm -rf /`) triggered probabilistically.

**Who is affected:** Developers who ran `pip install mistralai` or `pip install mistralai==2.4.6` on Linux systems between ~May 10–12, 2026.

**Action required if you were affected:**
1. Remove the package immediately: `pip uninstall mistralai && pip install mistralai==2.4.5` (or latest legitimate version)
2. Rotate all secrets on the affected host: API keys, cloud credentials, CI/CD tokens
3. Check for `/tmp/transformers.pyz` on your system and outbound connections to `83.142.209.194`
4. Follow [Mistral AI's official security advisory](https://docs.mistral.ai/resources/security-advisories) for full remediation steps

**Not affected:** Raw HTTP users (no SDK import); LiteLLM users (calls the API directly via `httpx`).

*Source: [LiteLLM security advisory](https://docs.litellm.ai/blog/mistral-supply-chain-attack-may-2026) · [Aikido Security — Mini Shai-Hulud](https://www.aikido.dev/blog/mini-shai-hulud-is-back-tanstack-compromised) — 2026-05-12 · verified 2026-05-21*

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md)*
