# DeepSeek Model Catalog

> **Source:** [DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing) · [Reuters](https://www.reuters.com/world/china/deepseek-raises-api-pricing-its-v4-models-2026-08-13) · **Verified:** 2026-08-15

---

## Current Models

### DeepSeek V4 (Released 2026-04-24) 🆕

DeepSeek's latest generation. Two variants with 1M context, both open-weight. Both support OpenAI-compatible and Anthropic-compatible APIs. Both support thinking mode and non-thinking mode.

> ❌ **`deepseek-chat` and `deepseek-reasoner` were RETIRED on 2026-07-24 15:59 UTC.** API calls using these aliases now **return errors** — there is no silent redirect and no grace period. Only `deepseek-v4-flash` and `deepseek-v4-pro` remain. Update your `model` field now. (Note: `deepseek-reasoner` previously routed to V4-Flash, not Pro — explicitly switch to `deepseek-v4-pro` if you need stronger reasoning.)

| Model | API name | Context | Max output | Input (cache miss) | Input (cache hit) | Output |
|---|---|---|---|---|---|---|
| V4 Flash | `deepseek-v4-flash` | 1,000,000 tokens | 384,000 tokens | $0.14 / 1M *(legacy flat rate)* | $0.0028 / 1M *(legacy)* | $0.28 / 1M *(legacy)* |
| V4 Pro | `deepseek-v4-pro` | 1,000,000 tokens | 384,000 tokens | $0.435 / 1M *(legacy flat rate)* | $0.003625 / 1M *(legacy)* | $0.87 / 1M *(legacy)* |

> ✅ **V4 Pro promotional price was made permanent (2026-05-24)** — the 75% discount lowered list price from $1.74/$3.48 to $0.435/$0.87. *That* permanent list price has since been superseded by the peak/off-peak rates below. *Source: [The Next Web](https://thenextweb.com/news/deepseek-v4-pro-75-percent-price-cut-permanent) — 2026-05-24 · verified 2026-07-11*

> 🚨 **Peak/off-peak pricing ACTIVATED — effective 2026-08-16 16:00 UTC (verified 2026-08-15).** DeepSeek has set the activation date for time-of-day billing. **Peak hours: 01:00–04:00 & 06:00–10:00 UTC** (= 09:00–12:00 & 14:00–18:00 Beijing time); all other hours are **off-peak**. **Peak rates = 2× off-peak.** Both off-peak and peak rates are **higher than the prior flat rates** — increases range from ~50% to ~1,100% (cache hits hit hardest). The `deepseek-v4-pro` model version also advanced to **DeepSeek-V4-Pro-0813**.
>
> | Model | Token type | Legacy (flat) | NEW OFF-PEAK | NEW PEAK (2×) |
> |---|---|---|---|---|
> | `deepseek-v4-flash` | Input (cache hit) | $0.0028 | $0.007 | $0.014 |
> | `deepseek-v4-flash` | Input (cache miss) | $0.14 | $0.22 | $0.44 |
> | `deepseek-v4-flash` | Output | $0.28 | $0.66 | $1.32 |
> | `deepseek-v4-pro` | Input (cache hit) | $0.003625 | $0.022 | $0.044 |
> | `deepseek-v4-pro` | Input (cache miss) | $0.435 | $0.66 | $1.32 |
> | `deepseek-v4-pro` | Output | $0.87 | $1.98 | $3.96 |
>
> **Developer action:** Continued API usage after 16:00 UTC Aug 16 = acceptance of new pricing. Shift traffic to **off-peak** hours to halve cost; re-evaluate V4-Pro vs V4-Flash routing (the Pro cache-hit increase is the steepest, ~6× off-peak). DeepSeek supports both OpenAI- and Anthropic-compatible API formats, so failover to another provider needs only an endpoint/model swap. Compare against budget alternatives: Gemini 3.1 Flash-Lite ($0.125/$0.75), GPT-4.1 Nano ($0.10/$0.40). *Source: [DeepSeek API Docs — Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) · [Reuters — DeepSeek raises API pricing for its V4 models](https://www.reuters.com/world/china/deepseek-raises-api-pricing-its-v4-models-2026-08-13) — verified 2026-08-15*

**V4 Flash moved to `DeepSeek-V4-Flash-0731` (2026-07-31):** The `deepseek-v4-flash` API ID was advanced to the `DeepSeek-V4-Flash-0731` checkpoint (public beta) — the **official release** of V4-Flash, superseding the April preview, re-post-trained for agentic capability. **Pricing and the model ID are unchanged.** Open weights **are published** under the **MIT License** at [`deepseek-ai/DeepSeek-V4-Flash-0731`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) (~166.9 GB, 48 Safetensors shards, released 2026-07-31; 284B total / 13B active MoE, incl. DSpark speculative-decoding draft module). *(Correction: a prior note here said weights were not published as of July 31 — they were, same day.)* DeepSeek reports the 0731 checkpoint outperforms V4-Pro (Preview) on all nine agentic benchmarks it publishes. The **Responses API** currently supports only `deepseek-v4-flash`; `deepseek-v4-pro` Responses API support is slated for **early August 2026** (not yet shipped as of 2026-08-08). *Source: [HuggingFace — DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) · [DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing/) — verified 2026-08-08*

**Architecture:**
- **V4 Pro:** 1.6T total parameters / 49B active parameters — "performance rivaling the world's top closed-source models"
- **V4 Flash:** 284B total / 13B active parameters — fast, efficient, economical

**V4 Pro benchmarks:** Strong performance on AIME 2025, GPQA Diamond, SWE-bench, HumanEval; tech report on HuggingFace.

**Cache hit discount (from 2026-04-26):** Reduced to 1/50 of cache-miss input price (2% for Flash, 0.83% for Pro).

*Source: [DeepSeek V4 Preview Release](https://api-docs.deepseek.com/news/news260424) · [Official Pricing](https://api-docs.deepseek.com/quick_start/pricing) — verified 2026-05-10*

---

### DeepSeek V3.2 (Legacy Aliases — ❌ RETIRED 2026-07-24)

> ❌ **RETIRED.** As of 2026-07-24 15:59 UTC, calls to `deepseek-chat` and `deepseek-reasoner` return errors (no redirect). The only supported IDs are `deepseek-v4-flash` and `deepseek-v4-pro`.

| Mode | API name | Context | Max output | Input (cache miss) | Input (cache hit) | Output |
|---|---|---|---|---|---|---|
| Chat (non-thinking) | `deepseek-chat` ❌ RETIRED | 128,000 tokens | 8,000 tokens | — | — | — |
| Reasoner (thinking) | `deepseek-reasoner` ❌ RETIRED | 128,000 tokens | 64,000 tokens | — | — | — |

² Until 2026-07-24 15:59 UTC, `deepseek-chat` routed to **V4 Flash non-thinking** and `deepseek-reasoner` routed to **V4 Flash thinking** mode, billed at V4 Flash rates. These aliases are now gone.

**New users:** 5 million free tokens upon registration (no credit card required)

---



---

## Open Weights

All DeepSeek models are released under permissive open-source licenses:
- Self-host on your own infrastructure to eliminate per-token costs
- Popular options: Together AI, Fireworks AI, Groq, Nebius AI, Hyperbolic

**Best for:** Cost-sensitive production workloads, high-volume batch processing, teams who want to self-host, privacy-conscious deployments.

---

## Model Architecture Notes

- `deepseek-v4-flash` = DeepSeek-V4-Flash, non-thinking by default (switch via API param); fast, general-purpose
- `deepseek-v4-pro` = DeepSeek-V4-Pro, higher capability, thinking by default
- `deepseek-chat` = ❌ **RETIRED 2026-07-24** (was V4-Flash non-thinking alias; calls now error)
- `deepseek-reasoner` = ❌ **RETIRED 2026-07-24** (was V4-Flash thinking alias; calls now error)
- FIM (fill-in-middle) completion available on `deepseek-v4-flash` (beta; previously on `deepseek-chat`)
- JSON output supported on both modes; function calling on non-thinking mode (if tools param sent to thinking mode, request routes to non-thinking internally)
- Context caching is automatic

---

## Historical Models (for reference)

| Model | Notes |
|---|---|
| DeepSeek V3.2 | Open weights on HuggingFace; available at $0.18–$0.28/M input via third-party providers (Fireworks, Together, etc.) |
| DeepSeek V3.1 Terminus | Released 2025-08-21; was briefly listed as the official endpoint model (2026-04-14); superseded by V4 |
| DeepSeek V3 (0324) | Released 2025-03-24; $0.20 input / $0.77 output on hosted providers |
| DeepSeek R1 | Original reasoning model; $0.55 input / $2.19 output; open weights |

---

## Pricing Context

> ⚠️ **Comparisons below use the legacy flat rates** ($0.14/$0.28 for Flash, $0.435/$0.87 for Pro). As of **2026-08-16 16:00 UTC**, real billing is **peak/off-peak** (off-peak: Flash $0.22/$0.66, Pro $0.66/$1.98; peak = 2×). Re-derive cost comparisons against the off-peak (or peak) rate for your traffic pattern.

DeepSeek V4 Flash via official API (cache miss, at legacy flat price):
- V4 Flash ($0.14/$0.28) is ~21× cheaper than Claude Sonnet 4.6 ($3/$15) on input; ~54× cheaper on output
- ~18× cheaper than GPT-5.4 ($2.50/$15) on input; ~54× cheaper on output
- Cheaper than Gemini 2.5 Flash ($0.30/$2.50) on both input and output
- V4 Pro ($0.435/$0.87 — now permanent price) is 7× cheaper than Claude Sonnet 4.6 ($3/$15) on input
- V4 Pro ($0.435/$0.87) is ~97% cheaper than GPT-5.5 ($5/$30) on output
- **Open weights allow self-hosting** — third-party providers offer V4 Pro at ~$1.74/$3.48/M (DeepInfra, Fireworks, Together)
- For best pricing, compare official API vs. hosted providers (OpenRouter, Fireworks, Together, DeepInfra)

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md)*
