# OpenAI Model Catalog

> **Source:** [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing) · [OpenAI Models](https://platform.openai.com/docs/models) · **Verified:** 2026-07-17

---

## Current Recommended Models

### GPT-5.6 Family (GA – Released 2026-07-09) 🆕 NEW

OpenAI's latest generation, introducing a three-tier naming system: **Sol** (flagship), **Terra** (balanced), and **Luna** (cost-efficient). This naming convention replaces the single-model-per-generation pattern — each tier can now advance independently. Launched following a limited government-review preview period (from June 26) under a new U.S. executive order requiring 30-day government review of frontier AI models.

> **New caching model:** For GPT-5.6 and all future OpenAI models, cache **writes** are billed at **1.25× the uncached input rate** (previously free). Cache **reads** continue at a 90% discount. GPT-5.6 also introduces explicit cache breakpoints and a 30-minute minimum cache life.

| Model | API name | Context | Input | Cache write | Cache read | Output | Input (long >272K) | Output (long >272K) | Notes |
|---|---|---|---|---|---|---|---|---|---|
| GPT-5.6 Sol | `gpt-5.6-sol` | 1 M tokens | $5.00 | $6.25 | $0.50 | $30.00 | $10.00 | $45.00 | Flagship; hard reasoning, coding, security, agentic |
| GPT-5.6 Sol Pro | `gpt-5.6-sol-pro` | 1 M tokens | $30.00 | — | — | $180.00 | $60.00 | $270.00 | Highest capability; complex tasks, long workflows |
| GPT-5.6 Terra | `gpt-5.6-terra` | 1 M tokens | $2.50 | $3.125 | $0.25 | $15.00 | $5.00 | $22.50 | Balanced; competitive with GPT-5.5 at 2× lower cost |
| GPT-5.6 Luna | `gpt-5.6-luna` | 1 M tokens | $1.00 | $1.25 | $0.10 | $6.00 | $2.00 | $9.00 | Fast, affordable; high-volume and simple tasks |

**Key facts:**
- Limited preview launched **2026-06-26** (government-coordinated); GA rollout began **2026-07-09**
- **Sol** = same price as GPT-5.5 ($5/$30) but improved capability; fewer hallucinations
- **Terra** = performance competitive with GPT-5.5 at half the price ($2.50/$15) — 16% fewer tokens on agent tasks
- **Luna** = new lowest-cost OpenAI tier at $1/$6 — defends against cheap competitors
- Reasoning effort: `low`, `medium` (default), `high`, `max` (max = `ultra` in Codex; available on Sol); `max` runs with 4 parallel subagents in multi-agent mode
- **ChatGPT routing:** Plus/Pro/Business/Enterprise access Sol via medium+ effort settings; Free/Go access Terra in ChatGPT Work and Codex; all four plans access all three tiers in Codex
- GPT-5.5 Instant remains the default for ChatGPT fast everyday responses; Sol powers Medium/High/Extra High effort
- **Cerebras integration (July 2026):** GPT-5.6 Sol launching on Cerebras at up to **750 tokens/second** for select customers
- **Programmatic Tool Calling (Responses API):** GPT-5.6 can write and run programs in-memory to coordinate tools; Zero Data Retention (ZDR) compatible
- Multi-agent beta: Responses API supports parallel subagents and synthesis for complex separable tasks
- ARC-AGI-3 scores: Sol 7.78%, Terra 0.8%, Luna 0.18% (vs GPT-5.5 0.43%, Claude Opus 4.8 1.5%, Gemini 3.1 Pro Preview 0.42%)
- Available across ChatGPT, Codex, and OpenAI API; Microsoft 365 Copilot using GPT-5.6 as preferred model

**Pricing tiers:** Batch/Flex: 50% off; Priority: 2.5× standard rate. **Long-context pricing (>272K tokens):** Input doubles (2×), output rate also rises — see table above. Confirmed on official pricing page 2026-07-17.

*Source: [OpenAI — GPT-5.6: Frontier intelligence](https://openai.com/index/gpt-5-6/) · [OpenAI — Previewing GPT-5.6 Sol](https://openai.com/index/previewing-gpt-5-6-sol/) · [OpenAI Help Center — GPT-5.6](https://help.openai.com/en/articles/20001325-a-preview-of-gpt-56-sol-terra-and-luna) · [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — verified 2026-07-10*

---

### GPT-5.5 Family (Released 2026-04-23)

OpenAI's most capable model. Positioned as "a new class of intelligence for coding and professional work." More token-efficient than GPT-5.4 — OpenAI claims ~40% fewer output tokens on Codex/agentic tasks. As of **2026-05-05**, GPT-5.5 Instant is the new default model for all ChatGPT users (replacing GPT-5.3 Instant). The "Instant" variant is accessible via the API as `chat-latest` — same token pricing as `gpt-5.5`.

| Model | API name | Context | Max output | Input (std) | Cached input | Output (std) | Input (long >272K) | Output (long >272K) |
|---|---|---|---|---|---|---|---|---|
| GPT-5.5 | `gpt-5.5` | 1,050 K tokens | 128 K | $5.00 | $0.50 | $30.00 | $10.00 | $45.00 |
| GPT-5.5 Pro | `gpt-5.5-pro` | 1,050 K tokens | 128 K | $30.00 | — | $180.00 | $60.00 | $270.00 |

**Key facts:**
- Released in ChatGPT (Plus/Pro/Business/Enterprise) on **2026-04-23**; API access live **2026-04-24**
- **GPT-5.5 Instant** became default ChatGPT model for all users on **2026-05-05**; API alias: `chat-latest`
- `gpt-5.5-2026-04-23` is the pinned snapshot; `gpt-5.5` alias available
- Reasoning effort configurable: `none`, `low`, `medium` (default), `high`, `xhigh`
- In Codex: 400K context window, includes **Fast mode** (1.5× faster, 2.5× cost)
- **Pricing tiers:** Batch/Flex: 50% off; Priority: 2.5× standard rate
- All tools supported: web search, file search, image generation, code interpreter, computer use, MCP
- **Regional processing (data residency):** +10% uplift
- GPT-5.3 Instant (previously `chat-latest`) has been replaced but is still accessible for paid users for ~3 months

*Source: [OpenAI — Introducing GPT-5.5](https://openai.com/index/introducing-gpt-5-5/) · [OpenAI — GPT-5.5 Instant](https://openai.com/index/gpt-5-5-instant/) · [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — verified 2026-05-12*

---

### GPT-5.4 Family (Released 2026-03-05)

Strong general-purpose model. First mainline model with **native computer-use** capabilities. Absorbs frontier coding from GPT-5.3-Codex into a single unified model.

| Model | API name | Context | Max output | Input (std) | Cached input | Output (std) | Input (long >272K) | Output (long >272K) |
|---|---|---|---|---|---|---|---|---|
| GPT-5.4 | `gpt-5.4` | 1 M tokens | 128 K | $2.50 | $0.25 | $15.00 | $5.00 | $22.50 |
| GPT-5.4 Pro | `gpt-5.4-pro` | 1 M tokens | 128 K | $30.00 | — | $180.00 | $60.00 | $270.00 |

**GPT-5.4 Mini** (Released 2026-03-17)

| Model | API name | Context | Input | Cached input | Output |
|---|---|---|---|---|---|
| GPT-5.4 Mini | `gpt-5.4-mini` | 400 K tokens | $0.75 | $0.075 | $4.50 |

**GPT-5.4 Nano** (Released 2026-03-17)

| Model | API name | Context | Input | Cached input | Output |
|---|---|---|---|---|---|
| GPT-5.4 Nano | `gpt-5.4-nano` | 1 M tokens | $0.20 | $0.02 | $1.25 |

**Key facts:**
- Standard context window: **272K tokens**; tokens beyond 272K billed at 2× rate (long-context pricing)
- Native computer-use: **75% OSWorld-Verified** (surpasses human expert baseline of 72.4%)
- SWE-bench Pro: **57.7%** (GPT-5.4), **54.38%** (Mini)
- GPT-5.2 Thinking retires **2026-06-05**; GPT-5.4 Thinking is the replacement in ChatGPT
- Regional processing (data residency) adds **+10% uplift** on all gpt-5.4 models

**Pricing tiers available:** Standard, Batch (50% off), Flex (50% off, async), Priority (2× standard, fast queuing)

---

### GPT-4.1 Family (Released 2025-04-14)

Long-context workhorses with 1 M token context at lower price than GPT-5.4.

| Model | API name | Context | Input | Cached input | Output |
|---|---|---|---|---|---|
| GPT-4.1 | `gpt-4.1` | 1 M tokens | $2.00 | $0.50 | $8.00 |
| GPT-4.1 Mini | `gpt-4.1-mini` | 1 M tokens | $0.40 | $0.10 | $1.60 |
| GPT-4.1 Nano | `gpt-4.1-nano` | 1 M tokens | $0.10 | $0.025 | $0.40 |

Available for fine-tuning: `gpt-4.1`, `gpt-4.1-mini`

---

### GPT-5.3-Codex (Released 2026-02-24)

OpenAI's dedicated agentic coding model. Optimized for long-running, tool-using development workflows: debugging, deployment, and iterative product work. Combines frontier software engineering performance (GPT-5.2-Codex) with broader reasoning capabilities (GPT-5.2). The model behind Codex cloud tasks and code reviews.

| Metric | Value |
|---|---|
| API name | `gpt-5.3-codex` |
| Context window | 400,000 tokens |
| Max output | 128,000 tokens |
| Input (std) | **$1.75 / 1M** |
| Cached input | $0.175 / 1M |
| Output (std) | **$14.00 / 1M** |
| Priority tier | $3.50 / $28.00 per 1M input/output |
| Batch tier | Not available |
| Knowledge cutoff | 2025-08-31 |
| GPQA Diamond | 91.5% |

**Key facts:**
- Default model for Codex cloud tasks and code reviews in ChatGPT
- `GPT-5.3-Codex-Spark` (research preview, Pro only): faster variant for day-to-day coding tasks; token pricing TBD
- ~25% faster and more token-efficient than prior Codex models
- Supports reasoning, tool calling, vision (image/PDF input)

*Source: [OpenRouter gpt-5.3-codex](https://openrouter.ai/openai/gpt-5.3-codex) · [PricePerToken](https://pricepertoken.com/pricing-page/model/openai-gpt-5.3-codex) · [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — verified 2026-05-16*

---

### Reasoning Models

| Model | API name | Context | Input | Cached input | Output | Notes |
|---|---|---|---|---|---|---|
| o3 | `o3` | 200 K | $10.00 | $2.50 | $40.00 | Deep reasoning; released 2025-04-16 |
| o4-mini | `o4-mini` | 200 K | $1.10 | $0.275 | $4.40 | Cost-efficient reasoning; released 2025-04-16 |
| o3 Deep Research | `o3-deep-research` | 200 K | $10.00 | — | $40.00 | Research agent |
| o4-mini Deep Research | `o4-mini-deep-research` | 200 K | $2.00 | — | $8.00 | Budget research agent |

---

### Legacy / Still Active

| Model | API name | Context | Input | Cached input | Output | Notes |
|---|---|---|---|---|---|---|
| GPT-4o | `gpt-4o` | 128 K | $2.50 | $1.25 | $10.00 | GA; older flagship |
| GPT-4o Mini | `gpt-4o-mini` | 128 K | $0.15 | $0.075 | $0.60 | GA |
| GPT-4.5 Preview | `gpt-4.5-preview` | 128 K | — | — | — | **Deprecated** – see [deprecated.md](../deprecated.md) |

---

## Realtime Voice Models

Current realtime models (verified on official pricing page 2026-07-17). `gpt-realtime-2.1` and `gpt-realtime-2.1-mini` are the current production versions; they supersede `gpt-realtime-2` and `gpt-realtime-mini` respectively.

| Model | API name | Modality | Input | Cached input | Output |
|---|---|---|---|---|---|
| GPT-Realtime-2.1 | `gpt-realtime-2.1` | Audio | $32.00/1M | $0.40/1M | $64.00/1M |
| | | Text | $4.00/1M | $0.40/1M | $24.00/1M |
| | | Image | $5.00/1M | $0.50/1M | — |
| GPT-Realtime-2.1 Mini | `gpt-realtime-2.1-mini` | Audio | $10.00/1M | $0.30/1M | $20.00/1M |
| | | Text | $0.60/1M | $0.06/1M | $2.40/1M |
| | | Image | $0.80/1M | $0.08/1M | — |
| GPT-Realtime-Translate | `gpt-realtime-translate` | Audio translation | — | — | **$0.034 / minute** |
| GPT-Realtime-Whisper | `gpt-realtime-whisper` | Streaming STT | — | — | **$0.017 / minute** |
| GPT-Realtime-2 (prev) | `gpt-realtime-2` | Audio + Text + Image | Same as 2.1 | Same | Same |
| GPT-Realtime-1.5 (legacy) | `gpt-realtime-1.5` | Audio + Text + Image | Audio: $32.00/1M | $0.40/1M | Text out: **$16.00/1M** |
| GPT-Realtime-Mini (legacy) | `gpt-realtime-mini` | Audio + Text + Image | Audio: $10.00/1M | $0.30/1M | Audio out: $20.00/1M |

**Key facts:**
- **GPT-Realtime-2.1 / 2.1-mini:** Current production versions per official pricing page (2026-07-17). Same price structure as their 2.x predecessors; the `.1` bump reflects capability/stability improvements.
- **GPT-Realtime-Translate:** Real-time speech translation; 70+ input languages → 13 output languages.
- **GPT-Realtime-Whisper:** Live speech-to-text; transcribes in real-time as the speaker talks.
- All models available via the [OpenAI Realtime API](https://developers.openai.com/api/docs/guides/realtime).

*Source: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — verified 2026-07-17*

---

## Fine-Tuning API — WINDING DOWN

> ⚠️ **Announced 2026-05-07:** OpenAI is winding down the self-serve fine-tuning platform.

| Milestone | Date |
|---|---|
| New orgs can no longer create training jobs | **2026-05-07** (effective immediately) |
| Orgs inactive for 60+ days lose fine-tuning access | **2026-07-02** |
| All customers lose ability to create new training jobs | **2027-01-06** |
| Existing fine-tuned model inference | Continues until the underlying **base model is deprecated** |

**Available fine-tuning models (still accessible for existing users):**
- `o4-mini-2025-04-16`: Training $100.00/hour; Input $4.00/1M (cached $1.00); Output $16.00/1M
- `gpt-4.1`, `gpt-4.1-mini`: Check [OpenAI deprecation docs](https://developers.openai.com/api/docs/deprecations) for inference-only end dates

**Migration path:** Move to prompt engineering, RAG, or system-prompt customization with standard API models. OpenAI's GPT-5.4+ family is capable enough that fine-tuning is rarely needed for instruction-following tasks.

*Source: [OpenAI fine-tuning announcement — May 8, 2026](https://openai.com/index/introducing-improvements-to-the-fine-tuning-api-and-expanding-our-custom-models-program/) · [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations) — verified 2026-06-18*

---

## Sora 2 API — Deprecating (Sunset 2026-09-24)

> ⚠️ **Sora consumer app discontinued 2026-04-26.** Sora 2 API remains accessible but is on a deprecated track with a hard shutdown of **September 24, 2026**. No successor video product has been announced.

*Source: [OpenAI Help Center — Sora discontinuation](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) — verified 2026-06-18*

---

## Batch API Pricing

Batch processing offers **50% off** standard prices for all models (asynchronous, up to 24 h turnaround). Use the `v1/batches` endpoint.

## Prompt Caching

Cached input tokens are charged at **10% of standard input price** for most models. Caching kicks in automatically after the first 1 024 tokens of a repeated prefix.

## Codex (Agentic Coding)

- **Pay-as-you-go** for teams via `codex-mini-latest` and Codex CLI (available April 2026)
- Enterprise: new **Codex seat** type at flexible token-based pricing (announced 2026-04-02)
- ChatGPT Business price reduced to **$20/seat/month** (down from $25) with Codex rollout

## ChatGPT Subscription Tiers (Updated 2026-04-09)

| Plan | Price | Key features |
|---|---|---|
| Free | $0 | Limited models, includes ads |
| Go | $8/month | Includes ads, higher limits than Free |
| Plus | $20/month | Ad-free, daily Codex usage |
| **Pro** | **$100/month** | 5× more Codex than Plus; competes with Anthropic Max 5x |
| Pro (high) | $200/month | Maximum usage; still available |

*ChatGPT subscriptions are separate from API billing.*

## Image Models

| Model | API name | Release | Notes |
|---|---|---|---|
| GPT-Image-2 | `gpt-image-2` | 2026-04-21 | Current image generation model; token-based billing |
| DALL-E 3 | `dall-e-3` | — | ❌ **RETIRED 2026-05-12** — migrate to `gpt-image-2` |
| DALL-E 2 | `dall-e-2` | — | ❌ **RETIRED 2026-05-12** — migrate to `gpt-image-2` |

**GPT-Image-2 pricing:** Image input $8.00/1M, cached $2.00/1M; Image output $30.00/1M; Text input $5.00/1M, cached $1.25/1M. ~$0.211 per 1024×1024 high-quality generation.

---

## Notes for Developers

- **`gpt-5.6-sol`** is the new top-tier model (GA 2026-07-09), matching GPT-5.5 pricing ($5/$30) with improved capability. **`gpt-5.6-terra`** ($2.50/$15) is the best value at GPT-5.5-class performance for half the price. **`gpt-5.6-luna`** ($1/$6) is the cheapest capable OpenAI model.
- ⚠️ **New caching model for GPT-5.6+:** cache writes now billed at 1.25× uncached input rate; cache reads still 10% of input. Budget accordingly.
- `gpt-5.5` is still available and `chat-latest` alias points to GPT-5.5 Instant (ChatGPT default since 2026-05-05)
- `gpt-5.4` remains the best value for agentic and computer-use tasks (same context, half the price of 5.5)
- `gpt-5.4-mini` is recommended for high-volume latency-sensitive workloads (400K context)
- `gpt-4.1-nano` / `gpt-5.4-nano` are the cheapest OpenAI options ($0.10–$0.20 input)
- `o4-mini` is the best cost-to-performance reasoning choice
- `gpt-5.3-codex` is the dedicated agentic coding model ($1.75/$14.00) — highest GPQA (91.5%) among OpenAI models; powers Codex cloud tasks and code reviews
- New voice models (`gpt-realtime-2`, `gpt-realtime-translate`, `gpt-realtime-whisper`) replace `gpt-realtime-1.5` for voice applications
- ❌ `dall-e-2` and `dall-e-3` retired **2026-05-12** — migrate to `gpt-image-2` immediately
- ⚠️ Fine-tuning platform winding down — new orgs blocked since 2026-05-07; all new training jobs disabled by **2027-01-06**
- ⚠️ Sora 2 API on deprecated track — sunset **2026-09-24**; no successor video product announced
- All prices **per 1M tokens** (USD)

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md) · [deprecated.md](../deprecated.md)*
