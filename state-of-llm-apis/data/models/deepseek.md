# DeepSeek Model Catalog

> **Source:** [DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing) · **Verified:** 2026-08-01

---

## Current Models

### DeepSeek V4 (Released 2026-04-24) 🆕

DeepSeek's latest generation. Two variants with 1M context, both open-weight. Both support OpenAI-compatible and Anthropic-compatible APIs. Both support thinking mode and non-thinking mode.

> ❌ **`deepseek-chat` and `deepseek-reasoner` were RETIRED on 2026-07-24 15:59 UTC.** API calls using these aliases now **return errors** — there is no silent redirect and no grace period. Only `deepseek-v4-flash` and `deepseek-v4-pro` remain. Update your `model` field now. (Note: `deepseek-reasoner` previously routed to V4-Flash, not Pro — explicitly switch to `deepseek-v4-pro` if you need stronger reasoning.)

| Model | API name | Context | Max output | Input (cache miss) | Input (cache hit) | Output |
|---|---|---|---|---|---|---|
| V4 Flash | `deepseek-v4-flash` | 1,000,000 tokens | 384,000 tokens | **$0.14 / 1M** | $0.0028 / 1M | **$0.28 / 1M** |
| V4 Pro | `deepseek-v4-pro` | 1,000,000 tokens | 384,000 tokens | **$0.435 / 1M** | $0.003625 / 1M | **$0.87 / 1M** |

> ✅ **V4 Pro promotional price is now permanent.** On **2026-05-24**, DeepSeek made the 75% discount permanent — the list price was lowered from $1.74/$3.48 to $0.435/$0.87. This is the ongoing price, not a promotional rate. *Source: [The Next Web](https://thenextweb.com/news/deepseek-v4-pro-75-percent-price-cut-permanent) — 2026-05-24 · [Official pricing docs](https://api-docs.deepseek.com/quick_start/pricing) confirmed $0.435/$0.87 as current price — verified 2026-07-11*

> 🚨 **Peak/off-peak pricing still NOT activated (verified 2026-08-01).** DeepSeek announced (2026-06-29) that the stable V4 release would introduce **time-of-day pricing** — approximately 2× rates during peak hours. As of 2026-07-24, the pricing page still shows flat rates. A 24-hour advance notice email will be sent before the change activates; no such notice has been sent. **Watch your email.** Announced rates:
>
> | Period | Hours (Beijing Time, UTC+8) | V4 Flash input | V4 Flash output | V4 Pro input | V4 Pro output |
> |---|---|---|---|---|---|
> | Off-peak (regular) | All other hours | $0.14 / 1M | $0.28 / 1M | $0.435 / 1M | $0.87 / 1M |
> | Peak | 09:00–12:00 & 14:00–18:00 | ~$0.29 / 1M | ~$0.59 / 1M | ~$0.88 / 1M | ~$1.76 / 1M |
>
> A 24-hour advance notice will be sent before the change takes effect. Continued API usage after the notice = acceptance of new pricing. Opt-out (with refund) available before the change. Cache hit rates also double during peak hours. This is the first time DeepSeek has introduced time-based surcharging. *Source: [Reddit r/DeepSeek](https://www.reddit.com/r/DeepSeek/comments/1uio6yf/) · [Tech Buzz China on X](https://x.com/TechBuzzChina/status/2071745549917688075) — 2026-06-29 · verified 2026-07-11*

**V4 Flash moved to `DeepSeek-V4-Flash-0731` (2026-07-31):** The `deepseek-v4-flash` API ID was advanced to the `DeepSeek-V4-Flash-0731` checkpoint (public beta) — a post-training refresh of the Flash model. **Pricing and the model ID are unchanged.** DeepSeek had **not** published open weights for the 0731 update as of July 31 (the April V4 preview checkpoints remain the latest self-hostable weights). The **Responses API** currently supports only `deepseek-v4-flash`; `deepseek-v4-pro` Responses API support is slated for **early August 2026**. *Source: [DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing/) — verified 2026-08-01*

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

DeepSeek V4 Flash via official API (cache miss, at current list price):
- V4 Flash ($0.14/$0.28) is ~21× cheaper than Claude Sonnet 4.6 ($3/$15) on input; ~54× cheaper on output
- ~18× cheaper than GPT-5.4 ($2.50/$15) on input; ~54× cheaper on output
- Cheaper than Gemini 2.5 Flash ($0.30/$2.50) on both input and output
- V4 Pro ($0.435/$0.87 — now permanent price) is 7× cheaper than Claude Sonnet 4.6 ($3/$15) on input
- V4 Pro ($0.435/$0.87) is ~97% cheaper than GPT-5.5 ($5/$30) on output
- **Open weights allow self-hosting** — third-party providers offer V4 Pro at ~$1.74/$3.48/M (DeepInfra, Fireworks, Together)
- For best pricing, compare official API vs. hosted providers (OpenRouter, Fireworks, Together, DeepInfra)

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md)*
