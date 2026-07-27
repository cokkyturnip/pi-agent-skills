# Deprecated & Sunset Models

> Track sunset dates and migration paths. **Last updated:** 2026-07-15.
>
> ⚠️ = Deprecated, still accessible. ❌ = Shut down, no longer accessible.

---

## Upcoming Shutdowns (Action Required)

### Anthropic — June 15, 2026 ✅ COMPLETED (2026-06-15)

❌ **Shut down today.** The following models are no longer accessible as of 2026-06-15. API calls return errors.

| Model | API name | Deprecated | Shutdown date | Replacement |
|---|---|---|---|---|
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | 2026-04-14 | **2026-06-15** ❌ | `claude-sonnet-4-6` |
| Claude Opus 4 | `claude-opus-4-20250514` | 2026-04-14 | **2026-06-15** ❌ | `claude-opus-4-7` |

Replacement pricing is unchanged: `claude-sonnet-4-6` at $3/$15 per 1M; `claude-opus-4-7` at $5/$25 per 1M.  
*Source: [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — verified 2026-05-14 / confirmed retired 2026-06-15*

> ✅ **Also live today (2026-06-15):** Anthropic's **Agent SDK billing split** is now in effect. Autonomous/programmatic Claude Code usage (Agent SDK, `claude -p`, GitHub Actions, third-party tools like OpenClaw/Zed/Cursor) now draws from a dedicated monthly credit pool billed at API rates. Credits: Pro = $20/month, Max 5x = $100/month, Max 20x = $200/month. Overflow charges at standard API per-token rates. See [anthropic.md](models/anthropic.md) for details.

---

### Google — June 18, 2026 ✅ COMPLETED TODAY

> ❌ **Shutdown completed today, June 18, 2026.** Gemini CLI and the Gemini Code Assist IDE extensions for consumer users are now offline. If you are a **Google AI Pro**, **Ultra**, or **free Gemini Code Assist for individuals** user and have not yet migrated, switch to the **Antigravity CLI** (`agy`) immediately.

| Product | Shutdown date | Replacement |
|---|---|---|
| Gemini CLI (`gemini` binary) | **2026-06-18** ❌ | Antigravity CLI (`agy`) — new binary, new config |
| Gemini Code Assist IDE extensions (consumer) | **2026-06-18** ❌ | Antigravity CLI / IDE integration |
| Gemini Code Assist for GitHub (new orgs) | **2026-06-18** ❌ | No new org installations permitted; existing installs stop in following weeks |

> ✅ **Enterprise exception:** Organizations on **Gemini Code Assist Standard or Enterprise** licenses, or using paid Gemini / Gemini Enterprise Agent Platform API keys, are **not affected**. This is a consumer-tier shutdown only.

**Migration:** Install the Antigravity CLI (`agy`) from [antigravity.google/download](https://antigravity.google/download). The config layout changed — the migration script does not update CI/CD pipelines. One known silent failure: a specific MCP `serverUrl` config field fails without error. Test before cutting over automated workflows.  
*Source: [Google I/O 2026 announcement — May 19, 2026](https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud) · [Antigravity migration guide](https://www.digitalapplied.com/blog/gemini-cli-to-antigravity-cli-migration-june-18-2026-guide) — verified 2026-06-18*

---

### xAI — May 15, 2026 Retirements ✅ COMPLETED (2026-05-15)

**Effective 2026-05-15 at 12:00 pm PT**, the following models were retired from the xAI API. Requests to these IDs now **automatically redirect to `grok-4.3`** (not return errors as previously noted — see correction below).

| Model retired | Auto-redirect | Explicit replacement |
|---|---|---|
| `grok-4-1-fast-reasoning` | `grok-4.3` (low reasoning) | `grok-4.3` |
| `grok-4-1-fast-non-reasoning` | `grok-4.3` (no reasoning) | `grok-4.3` |
| `grok-4-fast-reasoning` | `grok-4.3` (low reasoning) | `grok-4.3` |
| `grok-4-fast-non-reasoning` | `grok-4.3` (no reasoning) | `grok-4.3` |
| `grok-4-0709` | `grok-4.3` (low reasoning) | `grok-4.3` |
| `grok-code-fast-1` | `grok-4.3` (low reasoning) | `grok-4.3` |
| `grok-3` | `grok-4.3` (no reasoning) | `grok-4.3` |
| `grok-imagine-image-pro` | `grok-imagine-image-quality` | `grok-imagine-image-quality` |

> ⚠️ **Correction (2026-05-15):** Previous changelog entries stated retired slugs "will return errors." The actual behavior per the [official xAI migration guide](https://docs.x.ai/developers/migration/may-15-retirement) is that **slugs redirect to `grok-4.3`**. However, if you haven't explicitly updated your `model` field, you are now being **silently billed at `grok-4.3` rates** ($1.25/$2.50 per 1M) instead of Fast model rates ($0.20/$0.50) — a ~6× cost increase. Update your `model` field immediately.

*Source: [xAI Migration Guide — May 15 Retirement](https://docs.x.ai/developers/migration/may-15-retirement) — verified 2026-05-15*

---

### Google Gemini — May 25, 2026

| Model | Shutdown date | Migrate to |
|---|---|---|
| `gemini-3.1-flash-lite-preview` | **2026-05-25** | `gemini-3.1-flash-lite` (GA, identical pricing) |

> Deprecated 2026-05-11. The stable GA model `gemini-3.1-flash-lite` was released 2026-05-07. Same pricing ($0.25/$1.50 per 1M tokens), same model. Just update the model ID.  
*Source: [Google Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) — verified 2026-05-12*

---

### ⚠️ Gemini Interactions API — Breaking Schema Change (May 26 / June 8, 2026)

This is a **code change**, not a model retirement, but it will break integrations that use the Interactions API (v1beta).

| Deadline | Event |
|---|---|
| **2026-05-26** | New schema becomes default; old schema still works with explicit `Api-Revision` header |
| **2026-06-08** | Legacy schema removed entirely — integrations without SDK update will break |

**What's changing:** `outputs` array → `steps` schema; `response_format` field restructured.  
**Fix:** Upgrade Python SDK to ≥2.0.0 or JavaScript SDK to ≥2.0.0. Or add `Api-Revision: 2026-05-26` header to raw HTTP requests.  
*Source: [Google — Interactions API: Breaking changes migration guide (May 2026)](https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026) — 2026-05-06 · verified 2026-05-12*

---

### Google Gemini — June 2026 deadlines

**2026-06-01** ❌ COMPLETED: `gemini-2.0-flash` and `gemini-2.0-flash-lite` shut down. See "Already Shut Down" section.

**2026-06-25** — ⚠️ **11 DAYS** — Google Gemini image preview models retiring:

| Model | Shutdown date | Migrate to |
|---|---|---|
| `gemini-3.1-flash-image-preview` | **2026-06-25** ⚠️ | `gemini-3.1-flash-image` (GA as of 2026-05-28) |
| `gemini-3-pro-image-preview` | **2026-06-25** ⚠️ | `gemini-3-pro-image` (GA as of 2026-05-28) |

*Source: [Google Gemini API changelog — May 28, 2026](https://ai.google.dev/gemini-api/docs/changelog) — verified 2026-06-12*

---

**2026-08-17** — ~~2026-06-24~~ ✅ **DATE CORRECTED 2026-06-17** — Imagen 4.0 models retiring on the Gemini Developer API:

> ⚠️ **Correction (2026-06-17):** Previous entries showed a June 24, 2026 shutdown date for Imagen 4.0 models. The [official Google deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) (verified 2026-06-17) shows the actual shutdown date is **August 17, 2026**. No action required before August 17.

| Model | Shutdown date | Migrate to |
|---|---|---|
| `imagen-4.0-generate-001` | **2026-08-17** | `gemini-3.1-flash-image` (GA) |
| `imagen-4.0-ultra-generate-001` | **2026-08-17** | `gemini-3.1-flash-image` (GA) |
| `imagen-4.0-fast-generate-001` | **2026-08-17** | `gemini-3.1-flash-image` (GA) |

*Source: [Google Gemini Deprecations](https://ai.google.dev/gemini-api/docs/deprecations) — corrected 2026-06-17*

---

**2026-10-16** — `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` retiring:

> ⚠️ **Dates corrected (2026-06-12):** The official [Google Gemini deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) (last updated 2026-06-01) shows **October 16, 2026** as the shutdown date for all three models — NOT June 17 / July 22 as previously tracked. The June 17 date appeared in an earlier version of the page as "earliest possible" but has since been updated. Take no migration action before October 16.

| Model | Shutdown date | Migrate to |
|---|---|---|
| `gemini-2.5-pro` | **2026-10-16** | `gemini-3.1-pro-preview` or `gemini-3.5-flash` |
| `gemini-2.5-flash` | **2026-10-16** | `gemini-3.5-flash` |
| `gemini-2.5-flash-lite` | **2026-10-16** | `gemini-3.1-flash-lite` (GA) |

**Migration price notes:**
- `gemini-2.5-pro` ($1.25/$10.00) → `gemini-3.1-pro-preview` ($2.00/$12.00): ~1.6× price increase; or → `gemini-3.5-flash` ($1.50/$9.00) for faster agentic workloads at similar cost
- `gemini-2.5-flash` ($0.30/$2.50) → `gemini-3.5-flash` ($1.50/$9.00): 5× output price increase but dramatically better benchmarks

*(Previous June 1 entries moved to "Already Shut Down" section below.)*

> ⚠️ **Note (Vertex AI):** As of 2026-03-06, `gemini-2.0-flash-001` and `gemini-2.0-flash-lite-001` are unavailable to **new** Vertex AI projects. Existing customers retain access until June 1, 2026.

---

### Mistral — May 31, 2026 ✅ COMPLETED

> ❌ **Retired 2026-05-31.** These models are no longer accessible. See "Already Shut Down" section.

| Model | API name | Retired | Replacement |
|---|---|---|---|
| Mistral Large 2.1 | `mistral-large-2411` | **2026-05-31** | `mistral-large-latest` (Mistral Large 3) |
| Pixtral Large | `pixtral-large-2411` | **2026-05-31** | `mistral-large-latest` (Mistral Large 3) |
| Devstral Medium 1.0 | `devstral-medium-2507` | **2026-05-31** | `mistral-medium-3-5` |
| Voxtral Mini | `voxtral-mini-2507` | **2026-05-31** | `voxtral-mini-transcribe-2` |
| Mistral OCR 2 | `mistral-ocr-2505` | **2026-05-31** | `mistral-ocr-3` (OCR 3) |

*Source: [Mistral Models Overview](https://docs.mistral.ai/models/overview) — verified 2026-06-11*

---

### OpenAI — June 27, 2026 (ChatGPT only)

| Model | ChatGPT retirement | Notes |
|---|---|---|
| GPT-4.5 | **2026-06-27** | Retiring from ChatGPT only (announced 2026-05-28). No API change. |

*Source: [ChatGPT Release Notes — May 28, 2026](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) — verified 2026-06-14*

---

### Google — June 30, 2026 ✅ COMPLETED

| Model | API name | Retirement date | Replacement |
|---|---|---|---|
| Veo 3.0 (standard) | `veo-3.0-generate-001` | **2026-06-30** ❌ | `veo-3.1-generate-001` |
| Veo 3.0 Fast | `veo-3.0-fast-generate-001` | **2026-06-30** ❌ | `veo-3.1-fast-generate-001` |
| Veo 2.0 | `veo-2.0-generate-001` | **2026-06-30** ❌ | `veo-3.1-generate-001` |

*Source: [Google Cloud — Model versions and lifecycle](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) — verified 2026-06-15*

---

### Mistral — June 30, 2026 ✅ COMPLETED

| Model | API name | Deprecated | Retirement date | Replacement |
|---|---|---|---|---|
| Leanstral | `labs-leanstral-2603` | 2026-05-22 | **2026-06-30** ❌ | — (no published replacement) |
| Mistral Moderation v2 | `mistral-moderation-2411` | 2026-03-31 | **2026-06-30** ❌ | `mistral-moderation-2` |

*Source: [Mistral Models Overview](https://docs.mistral.ai/models/overview) — verified 2026-06-10*

---

### Mistral — July 31, 2026

| Model | API name | Deprecated | Retirement date | Replacement |
|---|---|---|---|---|
| Mistral Small 3.2 | `mistral-small-2506` | 2026-04-30 | **2026-07-31** | `mistral-small-2603` (Mistral Small 4) |
| Magistral Small 1.2 | `magistral-small-2509` | 2026-04-30 | **2026-07-31** | `mistral-small-2603` (Mistral Small 4) |
| Devstral 2 | `devstral-2512` | 2026-05-22 | **2026-07-31** | `mistral-medium-3-5` |
| Mistral NeMo 12B | `open-mistral-nemo-2407` | 2026-05-22 | **2026-07-31** | `ministral-3b-2410` (Ministral 3B 8B) |

*Source: [Mistral Models Overview](https://docs.mistral.ai/models/overview) — verified 2026-06-18*

---

### Mistral — August 31, 2026

| Model | API name | Deprecated | Retirement date | Replacement |
|---|---|---|---|---|
| Mistral Medium 3.1 | `mistral-medium-2508` | 2026-05-22 | **2026-08-31** | `mistral-medium-3-5` |

*Source: [Mistral Models Overview](https://docs.mistral.ai/models/overview) — verified 2026-06-18*

---

### Mistral — September 30, 2026

| Model | API name | Released | Retirement date | Replacement |
|---|---|---|---|---|
| Leanstral 1.5 | `labs-leanstral-1-5` | 2026-06-30 | **2026-09-30** | TBD |

This is a Labs (experimental) model for Lean 4 formal proof engineering. Not a general-purpose LLM.

*Source: [Mistral Changelog — June 30, 2026](https://docs.mistral.ai/resources/changelogs) — verified 2026-07-12*

---

### DeepSeek — July 24, 2026 🚨 **9 DAYS** — Hard cutoff

| Alias | Currently points to | Retirement date | Replacement |
|---|---|---|---|
| `deepseek-chat` | `deepseek-v4-flash` (non-thinking mode) | **2026-07-24 15:59 UTC** | `deepseek-v4-flash` |
| `deepseek-reasoner` | `deepseek-v4-flash` (thinking mode) | **2026-07-24 15:59 UTC** | `deepseek-v4-flash` or `deepseek-v4-pro` |

> 🚨 **URGENT — 9 DAYS REMAINING (2026-07-15).** No silent redirect after July 24. DeepSeek has confirmed that calls to `deepseek-chat` and `deepseek-reasoner` will **return errors** (not redirect) after the deadline. This is a hard cutoff with no announced extension. **Migrate now.** Update your `model` parameter to `deepseek-v4-flash` (for chat/non-thinking workflows) or `deepseek-v4-pro` (for higher capability).
>
> **Also note:** DeepSeek V4 stable release is arriving mid-July, and will introduce **peak/off-peak pricing** (~2× during 09:00–12:00 & 14:00–18:00 Beijing Time UTC+8). You will receive 24-hour advance notice before it takes effect. Cache hit rates also double during peak. See [models/deepseek.md](models/deepseek.md) for rate tables.

*Source: [DeepSeek API Docs — Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) — verified 2026-07-09*

---

### Google — July 14, 2026 ✅ COMPLETED TODAY — Gemini Embedding 001

> ❌ **Shut down 2026-07-14.** `gemini-embedding-001` is now retired. API calls to this model return errors. Migrate to `gemini-embedding-2` immediately.

| Model | API name | Release date | Shutdown date | Replacement |
|---|---|---|---|---|
| Gemini Embedding 001 | `gemini-embedding-001` | July 14, 2025 | **2026-07-14** ❌ | `gemini-embedding-2` |

**Migration:** Replace `gemini-embedding-001` with `gemini-embedding-2` in your API calls. No base URL change needed. Verify embedding dimensions match your vector store schema before cutting over.

*Source: [Google Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations) — verified 2026-07-14*

---

### Google — August 10, 2026

| Model | API name | Deprecation | Retirement date | Replacement |
|---|---|---|---|---|
| Gemini Embedding 2 Preview | `embedding-2-preview` | ~2026-03 | **2026-08-10** | `gemini-embedding-2` |

*Source: [Google Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations) — verified 2026-07-11*

---

### Google — October 2, 2026

| Model | API name | Deprecation | Retirement date | Replacement |
|---|---|---|---|---|
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | ~2026-07 | **2026-10-02** | `gemini-3.1-flash-image` (GA) |

*Source: [Google Cloud — Model versions and lifecycle](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) — verified 2026-07-10*

---

### Anthropic — July 24, 2026 ⚠️ — Claude Opus 4.7 Fast Mode retirement

Anthropic is deprecating **Fast mode for Claude Opus 4.7** on July 24, 2026. As of June 29, 2026, fast mode is also no longer available on Claude Opus 4.6 — requests to `claude-opus-4-6` with `speed: "fast"` run at standard speed and are billed at standard rates.

| Feature | Retirement date | Migration |
|---|---|---|
| Fast mode on `claude-opus-4-7` | **2026-07-24** | Migrate to `claude-opus-4-8` Fast Mode ($10/$50 per 1M, 3× cheaper than Opus 4.7 Fast) |
| Fast mode on `claude-opus-4-6` | **Already removed (2026-06-29)** ❌ | Use standard mode or `claude-opus-4-8` |

*Source: [Anthropic API Pricing](https://platform.claude.com/docs/en/about-claude/pricing) — verified 2026-07-09*

---

### OpenAI — September 24, 2026

| Product | Status | Notes |
|---|---|---|
| Sora 2 API | Deprecated; **shuts down 2026-09-24** | Sora consumer app was discontinued April 26, 2026. Sora 2 API remains on a deprecated track until September 24, 2026. No announced successor product. |

*Source: [OpenAI Help Center — Sora discontinuation](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) · [TechTimes](https://www.techtimes.com/articles/318635/20260618) — verified 2026-06-18*

---

### OpenAI — November 30, 2026

| Product | Status | Replacement |
|---|---|---|
| Agent Builder | Deprecated 2026-06-03; **shuts down 2026-11-30** | Agents SDK or ChatGPT Workspace Agents |

*Source: [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations) — verified 2026-06-14*

---

### OpenAI — December 1, 2026

| Model | API name | Deprecated | Shutdown date | Replacement |
|---|---|---|---|---|
| GPT Image 1 Mini | `gpt-image-1-mini` | 2026-06-02 | **2026-12-01** | `gpt-image-2` |
| GPT Image 1.5 | `gpt-image-1.5` | 2026-06-02 | **2026-12-01** | `gpt-image-2` |
| ChatGPT Image Latest | `chatgpt-image-latest` | 2026-06-02 | **2026-12-01** | `gpt-image-2` |

*Source: [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations) — verified 2026-06-14*

---

### OpenAI DALL-E 2 and DALL-E 3 image models ❌ RETIRED 2026-05-12

| Model | Retirement date | Replacement |
|---|---|---|
| `dall-e-2` | **2026-05-12** ❌ RETIRED | `gpt-image-2` |
| `dall-e-3` | **2026-05-12** ❌ RETIRED | `gpt-image-2` |

*Source: [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing) — verified 2026-05-12*

---

### OpenAI GPT-5.2 Thinking

| Model | Retirement date | Migration |
|---|---|---|
| GPT-5.2 Thinking (ChatGPT) | **2026-06-05** | GPT-5.4 Thinking (already deployed) |

GPT-5.4 replaced GPT-5.2 Thinking in ChatGPT as of 2026-03-05. GPT-5.2 Thinking remains in the Legacy Models section of the model picker for paid users until June 5, 2026. Enterprise/Edu users: enable via admin settings.

---

## Recently Deprecated (Still Accessible)

### Anthropic

| Model | API name | Deprecated | Retirement date | Replacement |
|---|---|---|---|---|
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | 2026-04-14 | **2026-06-15** | `claude-sonnet-4-6` |
| Claude Opus 4 | `claude-opus-4-20250514` | 2026-04-14 | **2026-06-15** | `claude-opus-4-7` |

> ⚠️ Both Claude Sonnet 4 and Claude Opus 4 retire **June 15, 2026**. See Upcoming Shutdowns above.  
*Source: [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — verified 2026-05-14*

### OpenAI

| Model | Deprecated | Notes |
|---|---|---|
| `gpt-4.5-preview` | 2025-04-14 | Announced deprecated at GPT-4.1 launch. Check [OpenAI changelog](https://developers.openai.com/api/docs/changelog) for sunset date. |

### Google (Preview models — upcoming retirement)

| Model | Shutdown date | Replacement |
|---|---|---|
| `gemini-robotics-er-1.5-preview` | **2026-04-30** | `gemini-robotics-er-1.6-preview` |

*Source: [Google AI for Developers — Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) — 2026-04-14*

### Google (Preview models — retired)

| Model | Retired | Replacement |
|---|---|---|
| `gemini-3-pro-preview` | **2026-03-09** | `gemini-3.1-pro-preview` |
| `gemini-2.5-flash-lite-preview-09-2025` | **2026-03-31** | `gemini-3.1-flash-lite-preview` |
| `gemini-2.0-flash-lite-preview` | 2025-12-09 | `gemini-2.5-flash-lite` |
| `gemini-2.0-flash-live-001` | 2025-12-09 | `gemini-3.1-flash-live-preview` |
| `gemini-2.0-flash-preview-image-generation` | 2025-11-14 | `gemini-2.5-flash-image` |
| `imagen-4.0-generate-preview-06-06` | 2026-02-17 | `imagen-4.0-generate-001` |

---

## Already Shut Down

### Anthropic (2026-06-15)

| Model | API name | Retired | Replacement |
|---|---|---|---|
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | **2026-06-15** | `claude-sonnet-4-6` ($3/$15 per 1M) |
| Claude Opus 4 | `claude-opus-4-20250514` | **2026-06-15** | `claude-opus-4-7` ($5/$25 per 1M) |

*Source: [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — verified 2026-06-15*

---

### Mistral (2026-05-31)

| Model | API name | Retired | Replacement |
|---|---|---|---|
| Mistral Large 2.1 | `mistral-large-2411` | **2026-05-31** | `mistral-large-latest` |
| Pixtral Large | `pixtral-large-2411` | **2026-05-31** | `mistral-large-latest` |
| Devstral Medium 1.0 | `devstral-medium-2507` | **2026-05-31** | `mistral-medium-3-5` |
| Voxtral Mini | `voxtral-mini-2507` | **2026-05-31** | `voxtral-mini-transcribe-2` |
| Mistral OCR 2 | `mistral-ocr-2505` | **2026-05-31** | `mistral-ocr-3` |

*Source: [Mistral Models Overview](https://docs.mistral.ai/models/overview) — verified 2026-06-11*

---

### OpenAI (2026-05-12)

| Model | Retired | Replacement |
|---|---|---|
| `dall-e-2` | **2026-05-12** | `gpt-image-2` |
| `dall-e-3` | **2026-05-12** | `gpt-image-2` |

---

### Cohere (2026-04-04)

Effective April 4, 2026, Cohere retired the following models. API requests to these IDs now fail.

| Model | Retired | Replacement |
|---|---|---|
| `embed-english-v2.0` | **2026-04-04** | `embed-english-v3.0` or `embed-v4.0` |
| `embed-english-light-v2.0` | **2026-04-04** | `embed-english-v3.0` |
| `embed-multilingual-v2.0` | **2026-04-04** | `embed-multilingual-v3.0` or `embed-v4.0` |
| `c4ai-aya-expanse-8b` | **2026-04-04** | `command-r7b-12-2024` or `command-a-03-2025` |
| `c4ai-aya-vision-8b` | **2026-04-04** | `command-a-03-2025` |

*Source: [Cohere deprecations page](https://docs.cohere.com/docs/deprecations) — verified 2026-04-13*

---

### Anthropic

| Model | API name | Retired | Was replaced by |
|---|---|---|---|
| Claude 3 Haiku | `claude-3-haiku-20240307` | **2026-04-20** | `claude-haiku-4-5-20251001` |
| Claude 3.5 Haiku | `claude-3-5-haiku-20241022` | **2026-02-19** | `claude-haiku-4-5-20251001` |
| Claude Sonnet 3.7 | `claude-3-7-sonnet-20250219` | **2026-02-19** | `claude-sonnet-4-5-20250929` |
| Claude 3 Opus | `claude-3-opus-20240229` | 2026-01-05 | `claude-opus-4-6` (preserved via special request) |
| Claude 3.5 Sonnet | `claude-3-5-sonnet-*` | 2025-10-28 | `claude-opus-4-6` |

> **Note:** Claude Opus 3 is retired but still accessible to paid claude.ai subscribers and on the API [by request](https://www.anthropic.com/research/deprecation-updates-opus-3) — special exception under Anthropic's model preservation commitments.

### Google

| Model | Shut down | Was replaced by |
|---|---|---|
| `gemini-2.0-flash` | **2026-06-01** | `gemini-2.5-flash` or `gemini-3-flash-preview` |
| `gemini-2.0-flash-001` | **2026-06-01** | `gemini-2.5-flash` |
| `gemini-2.0-flash-lite` | **2026-06-01** | `gemini-2.5-flash-lite` |
| `gemini-2.0-flash-lite-001` | **2026-06-01** | `gemini-2.5-flash-lite` |
| `gemini-1.5-pro-001` | 2025-05-24 | `gemini-2.0-flash` |
| `gemini-1.5-pro-002` | 2025-09-24 | `gemini-2.0-flash` |
| `gemini-1.5-flash-001` | 2025-05-24 | `gemini-2.0-flash-lite` |
| `gemini-1.5-flash-002` | 2025-09-24 | `gemini-2.0-flash-lite` |
| `gemini-1.0-pro-001` | 2025-04-21 | `gemini-2.0-flash` |
| `gemini-1.0-pro-vision-001` | 2025-04-21 | `gemini-2.0-flash` |
| `text-embedding-004` | 2026-01-14 | `gemini-embedding-001` |
| `gemini-2.5-flash-preview-05-20` | 2025-11-18 | `gemini-3-flash-preview` |

---

## Migration Notes

### Switching from `gemini-2.0-flash` to `gemini-2.5-flash`

**Price change:** $0.10/$0.40 → $0.30/$2.50 per 1M tokens (3× input, 6.25× output increase)  
**Capability improvement:** Significantly better reasoning and multimodal understanding  
**Action:** Update model identifier. Test system prompt behavior — 2.5 is more capable but may behave differently on edge cases.

### Switching from `gemini-2.0-flash-lite` to `gemini-2.5-flash-lite`

**Price change:** $0.075/$0.30 → $0.10/$0.40 per 1M tokens (~1.3× increase)  
**Action:** Update model identifier. Run regression tests.

### Switching from `gemini-2.5-pro` to `gemini-3.1-pro-preview`

**Price change:** $1.25/$10.00 → $2.00/$12.00 per 1M tokens (~1.6× increase)  
**Capability improvement:** Better GPQA (94.3% vs ~90%), stronger coding  
**Action:** Preview model — evaluate stability before committing to production. Use `gemini-2.5-pro` as fallback until GA.

### 🚨 Switching from `claude-3-haiku-20240307` to `claude-haiku-4-5-20251001` (Deadline: 2026-04-20 — **3 days**)

**Price change:** $0.25/$1.25 → $1.00/$5.00 per 1M tokens (4× more expensive)  
**Capability improvement:** Extended thinking support, 64K max output (vs 4K), significantly higher quality  
**Action required:** Update model identifier **immediately** — shutdown in 3 days. Run regression tests — Haiku 4.5 may respond differently on edge cases.  
**Tip:** Haiku 3.5 (`claude-3-5-haiku-20241022`) is already retired (2026-02-19) — do not use.

### Switching from `gpt-4.5-preview` to `gpt-5.4` or `gpt-4.1`

`gpt-4.1` provides 1 M context at lower cost. `gpt-5.4` is the current flagship.

### Anthropic Claude subscription → API for agents

From 2026-04-04, Claude Pro/Max subscriptions do **not** power third-party agent tools (OpenClaw, etc.). Switch to API key + pay-as-you-go. See [Anthropic models](models/anthropic.md).

---

*See also: [changelog.md](changelog.md)*
