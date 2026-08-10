# LLM API Comparison Matrix

> **Last updated:** 2026-08-08. Prices per 1M tokens (USD), standard tier unless noted.

---

## Flagship Models (Best-in-class)

| Provider | Model | Context | Input | Output | GPQA | SWE-bench | Notes |
|---|---|---|---|---|---|---|---|
| [Anthropic](models/anthropic.md) | Claude Fable 5 ✅ | 1 M | $10.00 | $50.00 | — | **80.3%** (Pro) | ✅ **RESTORED 2026-07-01** — suspended Jun 12–Jul 1; now globally available. Requires 30-day data retention. |
| [Anthropic](models/anthropic.md) | Claude Opus 5 🆕 | 1 M | $5.00 | $25.00 | — | near Fable 5 (CursorBench within 0.5%) | **NEW GA 2026-07-24** — step-change over Opus 4.8 at same price; default on Claude Max. Fast Mode $10/$50. |
| [OpenAI](models/openai.md) | GPT-5.6 Sol 🆕 | 1 M | $5.00 | $30.00 | — | — | **NEW GA 2026-07-09** — Next-gen flagship; fewer hallucinations; 750 t/s on Cerebras. Long context >272K: $10/$45 |
| [OpenAI](models/openai.md) | GPT-5.6 Terra 🆕 | 1 M | $2.50 | $15.00 | — | — | **NEW GA 2026-07-09** — GPT-5.5 performance at 2× lower cost. Long context >272K: $5/$22.50 |
| [OpenAI](models/openai.md) | GPT-5.6 Luna 🆕 | 1 M | $1.00 | $6.00 | — | — | **NEW GA 2026-07-09** — Cheapest capable OpenAI model. Long context >272K: $2/$9 |
| [OpenAI](models/openai.md) | GPT-5.5 | 1 M | $5.00 | $30.00 | — | — | Previous flagship; still available; `chat-latest` alias |
| [OpenAI](models/openai.md) | GPT-5.4 | 1 M | $2.50 | $15.00 | 92.8% | 57.7% | Native computer-use; tokens >272K billed at 2× |
| [OpenAI](models/openai.md) | GPT-5.4 Pro / GPT-5.5 Pro / GPT-5.6 Sol Pro | 1 M | $30.00 | $180.00 | — | — | Max capability |
| [Anthropic](models/anthropic.md) | Claude Opus 4.8 | 1 M | $5.00 | $25.00 | — | 69.2% (SWE-bench Pro) | Released 2026-05-28; superseded by Opus 5 (same price). Fast Mode $10/$50 |
| [Google](models/google.md) | Gemini 3.1 Pro Preview | 1 M | $2.00 | $12.00 | 94.3% | 80.6% | Preview (no GA SLA) |
| [xAI](models/xai.md) | Grok 4.5 🆕 | 500 K | $2.00 | $6.00 | — | — | **NEW 2026-07-08** — #1 agentic tool-use; MoE, co-trained w/ Cursor; $0.50 cached |
| [xAI](models/xai.md) | Grok 4.3 | 1 M | $1.25 | $2.50 | — | — | Previous xAI flagship; 1M context; voice API |
| [xAI](models/xai.md) | Grok 4 | 256 K | $3.00 | $15.00 | 87.7% | — | Always-on reasoning |

**Verdict:** **Claude Fable 5** ($10/$50) restored July 1, 2026 — best SWE-bench Pro (80.3%) but requires 30-day data retention. **Claude Opus 5** ($5/$25) launched July 24 — near-Fable-5 quality at half the cost, same price as Opus 4.8 (drop-in upgrade), new default on Claude Max. **GPT-5.6 Sol** ($5/$30) and **Terra** ($2.50/$15) launched July 9 — Terra delivers GPT-5.5 class performance at half the price; confirmed long-context pricing: Sol $10/$45, Terra $5/$22.50, Luna $2/$9 (>272K tokens). **Grok 4.5** ($2/$6) launched July 8 — #1 agentic tool-use, best cost/efficiency ratio among frontier models. For best reasoning accuracy, Gemini 3.1 Pro (94.3% GPQA) is top. For computer-use, GPT-5.4 is unmatched at 75% OSWorld. **Gemini 3.5 Flash** ($0.75/$4.50 after 50% price cut July 14) is now the fastest and most cost-efficient frontier-class model (~4× token gen speed vs competitors).

---

## Mid-Range Models (Best price-performance)

| Provider | Model | Context | Input | Output | Notes |
|---|---|---|---|---|---|
| [OpenAI](models/openai.md) | GPT-5.3-Codex | 400 K | $1.75 | $14.00 | GPQA 91.5%; agentic coding specialist; powers Codex tasks |
| [OpenAI](models/openai.md) | GPT-5.4 Mini | 400 K | $0.75 | $4.50 | 54.38% SWE-bench; 6× cheaper than flagship |
| [OpenAI](models/openai.md) | GPT-4.1 | 1 M | $2.00 | $8.00 | 1 M context at lower price |
| [Anthropic](models/anthropic.md) | Claude Sonnet 4.6 | 1 M | $3.00 | $15.00 | Best production Claude model |
| [Google](models/google.md) | Gemini 2.5 Pro | 2 M | $1.25 | $10.00 | ⚠️ Retiring 2026-10-16 |
| [Google](models/google.md) | Gemini 3.5 Flash 🆕 | 1 M | **$0.75** | **$4.50** | 🆕 **50% price cut (2026-07-14)** — was $1.50/$9.00; ~4× token gen speed; strongest agentic/coding; default Gemini model |
| [Google](models/google.md) | Gemini 3 Flash Preview | 1 M | $0.50 | $3.00 | Preview; fast |
| [Mistral](models/mistral.md) | Mistral Medium 3.5 🆕 | 256 K | $1.50 | $7.50 | 128B dense; vision + coding + agents; GA 2026-05-05 |
| [Mistral](models/mistral.md) | Mistral Medium 3 | 131 K | $0.40 | $2.00 | Good for coding/RAG |
| [xAI](models/xai.md) | Grok 4.5 🆕 | 500 K | $2.00 | $6.00 | NEW 2026-07-08; #1 agentic tool-use; $0.50 cached |
| [xAI](models/xai.md) | Grok Build 0.1 | 256 K | $1.00 | $2.00 | Agentic coding; powers Grok Build CLI |
| [Cohere](models/cohere.md) | Command A+ 🆕 | 128 K | $2.50 | $10.00 | **NEW 2026-05-20** — Apache 2.0 MoE (218B/25B active); vision, 48 langs; requires sales for prod API |
| [Cohere](models/cohere.md) | Command A | 256 K | $2.50 | $10.00 | Self-serve flagship; enterprise RAG; citation support |
| [Meta](models/meta.md) | Muse Spark 1.2 🆕 | 1.05 M | $1.25 | $4.25 | **NEW GA 2026-08-05** — Meta's first proprietary LLM API; reasoning + tool use; powers Muse Code. Contributor tier $0.10/$0.20 (Meta uses your data). ❌ Not open weights |
| [Meta](models/meta.md) | Llama 4 Maverick | 1 M | ~$0.15 | ~$0.60 | Open weights; self-hostable |

---

## Budget / High-Volume Models

| Provider | Model | Context | Input | Output | Notes |
|---|---|---|---|---|---|
| [OpenAI](models/openai.md) | GPT-5.4 Nano | 1 M | $0.20 | $1.25 | Newest cheapest OpenAI |
| [OpenAI](models/openai.md) | GPT-4.1 Nano | 1 M | $0.10 | $0.40 | Very cheap; 1 M context |
| [OpenAI](models/openai.md) | GPT-4o Mini | 128 K | $0.15 | $0.60 | Legacy; still widely used |
| [Anthropic](models/anthropic.md) | Claude Haiku 4.5 | 200 K | $1.00 | $5.00 | Fastest Claude |
| [Google](models/google.md) | Gemini 3.5 Flash 🏆 | 1 M | $0.75 | $4.50 | **New best balance** — 50% price cut 2026-07-14; beats 3.1 Pro on coding at far lower cost |
| [Google](models/google.md) | Gemini 3.1 Flash-Lite | 1 M | $0.125 | $0.75 | 🆕 50% price cut 2026-07-14 (was $0.25/$1.50); cheapest Gemini 3.x |
| [Google](models/google.md) | Gemini 2.5 Flash | 1 M | $0.30 | $2.50 | ⚠️ retires 2026-10-16; migrate to Gemini 3.5 Flash |
| [Google](models/google.md) | Gemini 2.5 Flash-Lite | 1 M | $0.10 | $0.40 | ⚠️ retires 2026-10-16 |
| [Google](models/google.md) | Gemini 2.0 Flash-Lite | 1 M | $0.075 | $0.30 | ❌ Shut down 2026-06-01 — migrate to `gemini-3.1-flash-lite` ($0.125/$0.75) |
| [Mistral](models/mistral.md) | Mistral Small 4 | 262 K | $0.15 | $0.60 | Vision + coding + reasoning unified |
| [Mistral](models/mistral.md) | Mistral Nemo | 128 K | $0.02 | $0.06 | Cheapest Mistral |
| [xAI](models/xai.md) | Grok 4.3 | 1 M | $1.25 | $2.50 | ✅ Recommended xAI default; replaces all Fast/grok-4 models |
| [DeepSeek](models/deepseek.md) | V4 Flash | 1 M | $0.14 | $0.28 | Open weights; cheapest frontier-class option |
| [DeepSeek](models/deepseek.md) | V4 Pro | 1 M | $0.435 | $0.87 | Permanent price (75% cut made permanent 2026-05-24) |
| [Cohere](models/cohere.md) | Command R7B | 128 K | $0.0375 | $0.15 | Cheapest Cohere |
| [Meta](models/meta.md) | Llama 4 Scout | 10 M | ~$0.08 | ~$0.30 | Open weights; 10 M context |

---

## Reasoning Models

| Provider | Model | Context | Input | Output | Notes |
|---|---|---|---|---|---|
| [OpenAI](models/openai.md) | o3 | 200 K | $10.00 | $40.00 | Deep reasoning flagship |
| [OpenAI](models/openai.md) | o4-mini | 200 K | $1.10 | $4.40 | Best cost-efficient reasoning |
| [xAI](models/xai.md) | Grok 4 | 256 K | $3.00 | $15.00 | Always-on reasoning |
| [DeepSeek](models/deepseek.md) | V4 Flash (thinking) | 1 M | $0.14 | $0.28 | Use `deepseek-v4-flash` with thinking mode enabled |

---

## Context Window Comparison

| Model | Context window |
|---|---|
| Llama 4 Scout | **10,000,000 tokens** |
| Claude Fable 5 🆕 | **1,000,000 tokens** |
| Grok 4.20 / Grok 4.1 Fast | **2,000,000 tokens** |
| Gemini 2.5 Pro | **2,000,000 tokens** |
| GPT-5.4 Mini | **400,000 tokens** |
| GPT-5.4, Claude Opus 4.6, Claude Sonnet 4.6 | **1,000,000 tokens** |
| GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano | **1,000,000 tokens** |
| Gemini 3.5 Flash 🆕 | **1,000,000 tokens** |
| Gemini 2.5 Flash, 2.0 Flash | **1,000,000 tokens** |
| Gemini 3.1 Pro Preview | **1,000,000 tokens** |
| Mistral Large 3, Mistral Small 4, Devstral 2 | **262,144 tokens** |
| Grok 4 | **256,000 tokens** |
| Command A+ 🆕 | **128,000 tokens** |
| Command A | **256,000 tokens** |
| Claude Haiku 4.5, o3, o4-mini | **200,000 tokens** |
| GPT-4o, GPT-4o Mini | **128,000 tokens** |
| Mistral Medium 3 | **131,072 tokens** |
| DeepSeek V4 Flash / V4 Pro | **1,000,000 tokens** |

---

## Feature Matrix

| Feature | OpenAI | Anthropic | Google | Mistral | xAI | DeepSeek | Cohere |
|---|---|---|---|---|---|---|---|
| Vision/Multimodal | ✅ | ✅ | ✅ | ✅ (Small 4) | ✅ | ❌ | ✅ (A+ only) |
| Function calling / tools | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt caching | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| Batch API (50% off) | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Streaming | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fine-tuning | ✅ | ❌ | ✅ (2.0 Flash) | ❌ | ❌ | ❌ | ❌ |
| Web search (built-in) | ✅ ($10/1K) | ❌ | ✅ ($14–35/1K) | ❌ | ✅ ($2.5–5/1K) | ❌ | ❌ |
| Computer use | ✅ (GPT-5.4) | ✅ | ✅ (Computer Use Preview) | ❌ | ❌ | ❌ | ❌ |
| Open weights | ❌ | ❌ | ✅ (Gemma 4 – Apache 2.0) | ✅ (some) | ❌ | ✅ | ❌ |
| Free API tier | ✅ (trial) | ❌ | ✅ | ✅ (experiment) | ❌ | ✅ (5 M tokens) | ✅ (1K calls/mo) |

---

## Pricing Tiers Available

| Provider | Standard | Batch (50% off) | Cached input | Priority queue |
|---|---|---|---|---|
| OpenAI | ✅ | ✅ | ✅ (~10%) | ✅ (2× price) |
| Anthropic | ✅ | ✅ | ✅ (~10%) | ❌ |
| Google | ✅ | ✅ | ✅ (~10%) | ✅ (new) |
| Mistral | ✅ | ❌ | ❌ | ❌ |
| xAI | ✅ | ✅ (new) | ✅ | ✅ (Provisioned Throughput) |
| DeepSeek | ✅ | ❌ | ✅ (~5%) | ❌ |
| Cohere | ✅ | ❌ | ❌ | ❌ |

---

## Decision Guide

| Use case | Recommended model | Rationale |
|---|---|---|
| **Best overall capability** | **Claude Fable 5** ✅ (restored Jul 1) | SWE-bench Pro 80.3%; $10/$50; requires 30-day data retention; fallback: Opus 5 ($5/$25) |
| **Frontier coding at $5/$25** | **Claude Opus 5** 🆕 | Near-Fable-5 quality at half the cost; same price as Opus 4.8 (drop-in upgrade); default on Claude Max |
| Best general reasoning | Gemini 3.1 Pro Preview | Highest GPQA (94.3%) |
| Fastest token generation | Gemini 3.5 Flash | ~4× token gen speed vs other frontier models; **$0.75/$4.50 Standard** (50% price cut 2026-07-14) |
| Computer use / desktop agents | GPT-5.4 | 75% OSWorld (above human baseline) |
| Coding agents (best, frontier) | Claude Fable 5 / Opus 5 / Grok 4.5 | SWE-bench Pro 80.3% (Fable 5); Opus 5 near-Fable-5 at $5/$25; Grok 4.5 #1 agentic tool-use |
| Coding agents (cost-efficient) | GPT-5.3-Codex / Grok Build 0.1 / GPT-5.6 Terra | GPQA 91.5% (Codex); $1.00/$2.00 (Grok Build); $2.50/$15.00 (Terra) |
| Best value frontier (new) | **GPT-5.6 Terra** | GPT-5.5 performance at half the price ($2.50/$15); GA July 9 |
| Long documents (>200K tokens) | Llama 4 Scout (10 M) or Gemini 3.1 Pro Preview (1 M) | Largest context windows |
| Production chatbot (balanced) | Claude Sonnet 5 (intro) / Sonnet 4.6 | Sonnet 5 intro $2/$10 through Aug 31; Sonnet 4.6 $3/$15 |
| High-volume cheap tasks | Gemini 3.1 Flash-Lite ($0.125/$0.75) or Mistral Nemo ($0.02/$0.06) | Cheapest current options; Flash-Lite halved in price 2026-07-14 |
| Cheapest frontier (open weight) | DeepSeek V4 Flash ($0.14/$0.28) | Open weights, 1M context, extremely cheap |
| Enterprise RAG / retrieval | Cohere Command A | Built-in citation, Rerank/Embed tools |
| Real-time X/Twitter data | Grok 4.5 + X Search | Native X integration; new flagship |
| Reasoning on a budget | o4-mini ($1.10/$4.40) or DeepSeek V4 Flash (thinking mode, $0.14/$0.28) | Cheap chain-of-thought |

---

## Action Items (As of 2026-07-25)

| Deadline | Action |
|---|---|
| **2026-05-12** ❌ PASSED | ❌ `dall-e-2` and `dall-e-3` **retired 2026-05-12** — calls now failing; migrate to `gpt-image-2` |
| **2026-05-15** ❌ PASSED | xAI `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning`, `grok-4.1-fast`, `grok-4-0709`, `grok-code-fast-1`, `grok-3`, `grok-imagine-image-pro` **retired 2026-05-15 at 12pm PT** — slugs now **redirect silently to `grok-4.3`** (not errors). If you haven't updated your `model` field, you are being billed at 6× your old Fast model rates. Fix immediately. |
| **2026-05-25** ❌ PASSED | `gemini-3.1-flash-lite-preview` — deprecated and shut down; use `gemini-3.1-flash-lite` (GA, same pricing) |
| **2026-06-01** ❌ PASSED | `gemini-2.0-flash` and `gemini-2.0-flash-lite` — shut down; migrate to `gemini-2.5-flash` / `gemini-2.5-flash-lite` |
| **2026-06-05** ❌ PASSED | GPT-5.2 Thinking removed from ChatGPT legacy picker |
| **2026-06-08** ❌ PASSED | Gemini Interactions API legacy schema removed entirely |
| **2026-07-01** ✅ DONE | ✅ **Claude Fable 5 RESTORED** globally — US export controls lifted June 30. Access restored on API, claude.ai, Claude Code, Cowork. Mythos 5 remains restricted to Glasswing partners. |
| **2026-06-30** ✅ DONE | 🆕 **Gemini Omni Flash API launched** — `gemini-omni-flash-preview` now available to developers; ~$0.10/sec video output. Nano Banana 2 Lite (`gemini-3.1-flash-lite-image`) also reached GA. |
| **2026-07-06** ✅ DONE | 🆕 **xAI: 21 new Grok Voice voices** — multilingual, across Voice Agent API, TTS API, and Voice Agent Builder. Speech tags ([pause], etc.) and voice cloning added. |
| **2026-07-08** ✅ DONE | 🆕 **Grok 4.5 launched** — xAI's new flagship at $2/$6 per 1M, $0.50 cached input, 500K context. #1 agentic tool-use. MoE co-trained with Cursor. Now default in Grok Build. |
| **2026-07-09** ✅ DONE | 🆕 **GPT-5.6 Sol, Terra, Luna GA** — OpenAI's new generation: Sol $5/$30, Terra $2.50/$15, Luna $1/$6. New caching: writes at 1.25× input, reads at 10%. Available in ChatGPT, Codex, API. |
| **2026-07-12 11:59 PM PT** ✅ DONE | ✅ **CLOSED** — Claude Fable 5 free subscription window closed. Usage credits now required ($10/$50 per 1M). Check your console billing settings if Fable 5 calls are failing. |
| **2026-07-14** ✅ DONE | ✅ `gemini-embedding-001` **retired** — hard cutoff; calls now failing. Migrate to `gemini-embedding-2` immediately. |
| **2026-07-14** ✅ DONE | 🆕 **Google: Gemini 3.5 Flash price cut 50%** — Standard rate dropped from $1.50/$9.00 to **$0.75/$4.50**. Gemini 3.1 Flash-Lite also halved: $0.25/$1.50 → **$0.125/$0.75**. |
| **2026-07-24** ✅ DONE | 🆕 **Claude Opus 5 released** (`claude-opus-5`, $5/$25, Fast Mode $10/$50) — step-change over Opus 4.8 at the same price; near-Fable-5 quality at half the cost; new default on Claude Max. Drop-in upgrade from `claude-opus-4-8`. |
| **2026-07-24 15:59 UTC** ✅ DONE | ❌ **DeepSeek `deepseek-chat` / `deepseek-reasoner` RETIRED** — hard cutoff reached; calls now return errors (no redirect). Only `deepseek-v4-flash` and `deepseek-v4-pro` remain. Note: `deepseek-reasoner` mapped to V4-Flash, not Pro — switch to `deepseek-v4-pro` if you need stronger reasoning. Peak/off-peak pricing still NOT activated (verified 2026-07-24). |
| **2026-07-24** ✅ DONE | ✅ **Anthropic Claude Opus 4.7 Fast Mode retired** — migrate to `claude-opus-5` Fast Mode or `claude-opus-4-8` Fast Mode ($10/$50 per 1M). |
| **2026-07-31** | ⚠️ **6 DAYS** — Mistral retirements: `mistral-small-2506`, `magistral-small-2509`, `devstral-2512`, `open-mistral-nemo-2407` → `mistral-small-2603` or `mistral-medium-3-5` |
| **2026-08-17** | Imagen 4.0 models retire on Gemini Dev API: `imagen-4.0-*` → `gemini-3.1-flash-image` |
| **2026-08-31** | Mistral `mistral-medium-2508` (Medium 3.1) → `mistral-medium-3-5` |
| **2026-09-24** | OpenAI Sora 2 API shuts down — no announced replacement |
| **2026-09-30** | Mistral `labs-leanstral-1-5` (Leanstral 1.5) retires — specialized Lean 4 model |
| **2026-10-02** | Gemini `gemini-2.5-flash-image` retires — migrate to `gemini-3.1-flash-image` |
| **2026-10-16** | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` retire → `gemini-3.5-flash` / `gemini-3.1-flash-lite` |
| **2026-11-30** | OpenAI Agent Builder shuts down → Agents SDK or ChatGPT Workspace Agents |
| **2026-12-01** | `gpt-image-1-mini`, `gpt-image-1.5`, `chatgpt-image-latest` → `gpt-image-2` |
| **2027-01-06** | OpenAI fine-tuning: last date to create new training jobs |

---

*See provider pages for full details: [OpenAI](models/openai.md) · [Anthropic](models/anthropic.md) · [Google](models/google.md) · [Mistral](models/mistral.md) · [xAI](models/xai.md) · [DeepSeek](models/deepseek.md) · [Cohere](models/cohere.md) · [Meta](models/meta.md)*
