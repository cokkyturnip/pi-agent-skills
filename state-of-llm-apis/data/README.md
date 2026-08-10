# State of LLM APIs

A living knowledge base of LLM API specs, pricing, and changes — maintained automatically by the Model Tracker agent.

**Last updated:** 2026-08-08

---

## Quick Navigation

| File | Description |
|---|---|
| [comparison.md](comparison.md) | Side-by-side pricing and feature matrix for all major providers |
| [changelog.md](changelog.md) | Chronological log of model releases, price changes, deprecations |
| [deprecated.md](deprecated.md) | Sunset dates and migration paths |
| [models/openai.md](models/openai.md) | OpenAI — GPT-5.6 Sol/Terra/Luna, GPT-5.5, GPT-4.1, o3/o4-mini |
| [models/anthropic.md](models/anthropic.md) | Anthropic — Claude Opus 5/Fable 5, Sonnet 5, Haiku 4.5 |
| [models/google.md](models/google.md) | Google — Gemini 3.6 Flash, 3.5 Flash-Lite, 3.1 Pro (preview) |
| [models/mistral.md](models/mistral.md) | Mistral AI — Medium 3.5, Small 4, Large 3, Nemo |
| [models/xai.md](models/xai.md) | xAI — Grok 4.5, Grok 4.3, Grok 4 |
| [models/deepseek.md](models/deepseek.md) | DeepSeek — V4 Flash + V4 Pro |
| [models/cohere.md](models/cohere.md) | Cohere — Command A+, Command A, R series |
| [models/meta.md](models/meta.md) | Meta — Muse Spark 1.2 (API) + Llama 4 Scout/Maverick (open weights) |

---

## At a Glance: April 2026

### Top Models by Category

| Category | Winner | Price (input/output) |
|---|---|---|
| Best reasoning accuracy | Gemini 3.1 Pro Preview (GPQA 94.3%) | $2.00/$12.00 |
| Best computer use | GPT-5.4 (75% OSWorld) | $2.50/$15.00 |
| Best coding | Claude Opus 4.6 (SWE-bench 74%+) | $5.00/$25.00 |
| Best price-performance | Gemini 2.5 Flash ⚠️ | $0.30/$2.50 |
| Cheapest billed | Gemini 2.0 Flash-Lite ⚠️ | $0.075/$0.30 |
| Cheapest open-weight | Llama 4 Scout (self-host) | ~$0.11/$0.34 (3P API) |
| Largest context | Llama 4 Scout | 10,000,000 tokens |
| Best long context | Grok 4.20 / Grok 4.1 Fast | 2,000,000 tokens |

> ⚠️ Gemini 2.5 Flash and 2.0 Flash-Lite are deprecated; retiring June/July 2026.

### Urgent Action Items

- 🔴 **Gemini 2.0 Flash/Flash-Lite** — Shutdown **2026-06-01**. Migrate to 2.5 Flash / 2.5 Flash-Lite.
- 🔴 **Gemini 2.5 Pro / 2.5 Flash** — Shutdown **2026-06-17**. Migrate to Gemini 3.x.
- 🟡 **OpenAI GPT-5.2 Thinking** — Retires **2026-06-05** in ChatGPT.
- 🟡 **Anthropic Claude subscriptions for agents** — Now require direct API key (since 2026-04-04).

---

## About

This repository is automatically maintained by the **Model Tracker** agent (see `selfdrivingrepo.json`). It runs daily and updates content when it finds new model releases, pricing changes, or deprecations.

Data is sourced from official provider documentation, pricing pages, and verified release announcements. Every data point includes a verification date.

**Write for developers who need to pick a model.** Numbers first, narrative second.
