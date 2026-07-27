# Google Gemini Model Catalog

> **Source:** [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) · [Gemini Deprecations](https://ai.google.dev/gemini-api/docs/deprecations) · **Verified:** 2026-07-14

---

## Current Models (Gemini 3.5 — Latest Generation)

### Gemini 3.5 Flash (Released 2026-05-19 — Google I/O 2026)

Google's newest Gemini model, announced at Google I/O 2026. Optimized for **speed and complex agentic tasks**. Outperforms Gemini 3.1 Pro on key agentic/coding benchmarks at ~25% lower cost. Now the **default model** powering the Gemini app and AI Mode in Google Search globally.

> ⚠️ **Pricing note (corrected 2026-06-09):** The changelog entry from 2026-05-20 stated $2.70/$16.20 as "corrected" pricing. This was wrong — it confused **Priority tier** rates with Standard rates. The official Google AI Developer API pricing page shows **$1.50 Standard / $2.70 Priority** for input and **$9.00 Standard / $16.20 Priority** for output. Standard tier is the default.

| Metric | Value |
|---|---|
| API name | `gemini-3.5-flash` |
| Context window | 1,000,000 tokens |
| Max output | 64,000 tokens (65,535) |
| Input (Standard) | **$0.75 / 1M** (text/image/video) 🆕 **PRICE CUT** (was $1.50) |
| Output (Standard, incl. thinking) | **$4.50 / 1M** 🆕 **PRICE CUT** (was $9.00) |
| Input (Priority) | $1.35 / 1M |
| Output (Priority) | $8.10 / 1M |
| Input (Batch/Flex) | $0.375 / 1M |
| Output (Batch/Flex) | $2.25 / 1M |
| Context caching | $0.075 / 1M (Standard) |
| Context caching (storage) | $1.00 / 1M tokens per hour |
| Free tier | ✅ (rate-limited) |

**Key facts:**
- Released at Google I/O 2026 keynote, **2026-05-19**; available immediately in Gemini API, Google AI Studio, Antigravity, and Vertex AI
- **🆕 Price cut 2026-07-14:** Standard rate halved from $1.50/$9.00 to **$0.75/$4.50** per 1M input/output. This matches what was previously the Batch/Flex price, making it now the default Standard rate.
- Outperforms Gemini 3.1 Pro on agentic/coding benchmarks: **Terminal-Bench 2.1: 76.2%**, GDPval-AA: 1656 Elo, MCP Atlas: 83.6%, CharXiv (multimodal): 84.2%
- At $0.75/$4.50 Standard, now costs ~62% less than Gemini 3.1 Pro ($2.00/$12.00) while outscoring it on key benchmarks
- ~4× faster output token generation compared to other frontier models
- Built for long-horizon agentic tasks, complex coding, and multi-step workflows
- Replaces Gemini 3.1 Pro as the recommended API model for production agentic use
- **Gemini 3.5 Pro**: Still unreleased as of **2026-07-13**. Model was rebuilt following delayed June window. Community discussion (r/GeminiAI, July 2026) suggests the delay is partly driven by competitive pressure from GPT-5.6 and Grok 4.5. No official release date given. Expected: 2M context, "Deep Think" reasoning, ~$15/$60 per 1M tokens. Limited Vertex AI enterprise preview only. Do not plan production integrations around leaked dates.
- Grounding with Google Search: 5,000 prompts/month free (shared across Gemini 3 family), then **$14 / 1,000 queries**

**June 2026 updates to Gemini 3.5 Flash:**
- **Computer Use** (2026-06-24): `gemini-3.5-flash` now supports computer use — can see, reason, and take action across desktop, mobile, and browser environments. Billed at standard Gemini 3.5 Flash token rates. Improves on long-horizon and enterprise automation tasks (continuous software testing, knowledge work). *(Source: [Google Blog — Computer use in Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/) — 2026-06-24)*
- **Gemini 3.5 Pro**: Still unreleased as of **2026-07-13**. Delayed from June. Community discussion (r/GeminiAI, July 2026) attributes delay to competitive pressure from GPT-5.6 and Grok 4.5 — "they simply don't have a model that's ready to compete." Expected: 2M context, "Deep Think" reasoning, ~$15/$60 per 1M tokens. Available in limited Vertex AI enterprise preview only.

*Source: [Google AI Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing) (last updated 2026-07-09 UTC) · [Google Cloud Blog — Google I/O 2026](https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud) · [Business Insider — Gemini 3.5 Pro delay](https://www.businessinsider.com/google-3-5-pro-july-release-tokens-ai-agents-model-2026-6) — **pricing verified 2026-07-14***

---

### Gemini Omni Flash (Developer API: 2026-06-30) 🆕 API NOW LIVE

Google's first "any-to-any" model: blends text, audio, image, and **video** inputs to produce video output. Designed for conversational video creation and editing. Announced at Google I/O 2026, developer API launched **June 30, 2026**.

> ✅ **Developer API now available** as of **June 30, 2026** via `gemini-omni-flash-preview`. Public preview in Google AI Studio, Gemini API, and Gemini Enterprise Agent Platform.

| Metric | Value |
|---|---|
| API name | `gemini-omni-flash-preview` |
| Status | Public preview (as of 2026-06-30) |
| Input | $1.50 / 1M tokens (text/image/video — same as Gemini 3.5 Flash) |
| Video output | ~$0.10 / second (~$17.50 / 1M video output tokens; 5,792 tokens/sec at 720p) |
| Max output length | 10 seconds per generation |
| Output resolution | 720p |

**Key facts:**
- Generates 3–10 second video clips via the Interactions API from text, image, or existing video inputs
- **Conversational video editing**: refine or edit generated video through natural-language follow-up prompts
- Supports text-to-video, image-to-video, reference-to-video generation
- SynthID watermarking and C2PA Content Credentials on generated content
- Best companion for still-image generation: `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite, GA June 30)
- Consumer access: Gemini app (AI Plus/Pro/Ultra), Google Flow, YouTube Shorts/Create
- Preview: no GA SLA; availability may vary by region and account tier

*Source: [Google Blog — Nano Banana 2 Lite and Gemini Omni Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/) · [Gemini API changelog — June 30, 2026](https://ai.google.dev/gemini-api/docs/changelog) · [Coursiv — Gemini Omni Flash pricing](https://coursiv.io/blog/gemini-omni-flash) — verified 2026-07-11*

---

### Gemini 3.5 Live Translate (Released 2026-06-09) 🆕 NEW

Real-time speech-to-speech translation model. Automatically detects 70+ input languages while preserving the speaker's natural intonation and eliminating pauses.

| Metric | Value |
|---|---|
| API name | `gemini-3.5-live-translate` (Gemini Live API) |
| Status | Available in Gemini Live API, Google AI Studio, Google Translate app |
| Input languages | 70+ (auto-detect) |
| Output | Translated speech, near-real-time |
| Pricing | See [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — audio input/output rates |

**Best for:** Multilingual voice calls, meetings, live translation workflows. Near-real-time with natural-sounding speech and no awkward pauses.

*Source: [Google Blog — Gemini 3.5 Live Translate](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/) — 2026-06-09 · verified 2026-07-11*

---

## Managed Agents API (Launched 2026-05-19 — Google I/O 2026) 🆕 NEW

Google launched the **Managed Agents API** at Google I/O 2026, enabling developers to spin up stateful, autonomous agents inside secure Google-hosted Linux sandboxes via a single API call. Removes infrastructure setup overhead.

**General-purpose managed agent:**

| Metric | Value |
|---|---|
| API name | `antigravity-preview-05-2026` |
| Status | Public preview (as of 2026-05-19) |
| Capabilities | Plan, reason, write & execute code, manage files, browse web (inside sandbox) |

**Key facts:**
- Single API call provisions a fully isolated sandbox with the Antigravity agent harness
- Inherits Agent Platform's enterprise data privacy, governance, and security controls
- Stateful agents: maintain context across multiple interactions
- Antigravity SDK also released — lets developers deploy the agent harness on their own infrastructure with full customization
- Pricing: not yet published (preview); check [Agent Platform docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents)

### Managed Agents API — Expanded Capabilities (2026-07-07) 🆕

On July 7, 2026, Google announced four new capabilities for Managed Agents in the Gemini API, addressing developer feedback for production-ready deployments:

1. **Background execution:** Agents now run asynchronously in the background — dispatch a task and poll or receive a webhook when complete. No need to keep a connection open for long-running agent tasks.
2. **Remote MCP server integration:** Agents can call any remote MCP (Model Context Protocol) server as a tool, enabling integration with third-party services and custom APIs without embedding them in the sandbox.
3. **Custom function calling:** Define and expose custom tools/functions to the agent at runtime, in addition to built-in tools like code execution and web search.
4. **Refreshing credentials across interactions:** Agents can now refresh API credentials (OAuth tokens, etc.) mid-session, enabling longer-running agents that span credential expiry windows.

**API name:** `antigravity-preview-05-2026` (same identifier; capabilities expanded in-place)  
**Access:** Gemini API (via [ai.google.dev/gemini-api/docs/agents](https://ai.google.dev/gemini-api/docs/agents)) and Gemini Enterprise Agent Platform

*Source: [Google Blog — Expanding Managed Agents in Gemini API](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/) — 2026-07-07 · verified 2026-07-13*

---

*Source: [Google Gemini API changelog — May 19, 2026](https://ai.google.dev/gemini-api/docs/changelog) · [Google Cloud Blog — I/O 2026](https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud) — verified 2026-05-21*

---

## Previous Generation GA Models

### Gemini 2.5 Pro

Best reasoning model at GA. Large 2 M token context window.

| Metric | Value |
|---|---|
| API name | `gemini-2.5-pro` |
| Context window | 2,000,000 tokens |
| Input (≤200K) | **$1.25 / 1M** |
| Input (>200K) | $2.50 / 1M |
| Output (≤200K) | **$10.00 / 1M** |
| Output (>200K) | $15.00 / 1M |
| Cached input | $0.125 / 1M |
| Free tier | ✅ (rate-limited) |
| **Retirement date** | **2026-10-16** → migrate to `gemini-3.1-pro-preview` or `gemini-3.5-flash` *(corrected 2026-06-12; was previously listed as June 17)* |

---

### Gemini 2.5 Flash 🏆 Best price-performance (GA)

| Metric | Value |
|---|---|
| API name | `gemini-2.5-flash` |
| Context window | 1,000,000 tokens |
| Input | **$0.30 / 1M** |
| Output | **$2.50 / 1M** |
| Cached input | $0.03 / 1M |
| Free tier | ✅ |
| **Retirement date** | **2026-10-16** → migrate to `gemini-3.5-flash` *(corrected 2026-06-12; was previously listed as June 17)* |

---

### Gemini 2.5 Flash-Lite (GA)

| Metric | Value |
|---|---|
| API name | `gemini-2.5-flash-lite` |
| Context window | 1,000,000 tokens |
| Input | **$0.10 / 1M** |
| Output | **$0.40 / 1M** |
| Free tier | ✅ |
| **Retirement date** | **2026-10-16** *(corrected 2026-06-12; was previously listed as July 22)* |

---

### Gemini 2.0 Flash (GA – ❌ SHUT DOWN 2026-06-01)

> ❌ **Shut down June 1, 2026.** Requests to this model return errors. Migrate to `gemini-2.5-flash` immediately.

| Input | Output | Cached input |
|---|---|---|
| ~~$0.10 / 1M~~ | ~~$0.40 / 1M~~ | ~~$0.025 / 1M~~ |

---

### Gemini 2.0 Flash-Lite (GA – ❌ SHUT DOWN 2026-06-01)

> ❌ **Shut down June 1, 2026.** Requests to this model return errors. Migrate to `gemini-2.5-flash-lite` immediately.

| Input | Output |
|---|---|
| ~~$0.075 / 1M~~ | ~~$0.30 / 1M~~ |

---

## Preview Models (Gemini 3.x generation)

> Preview models do not have GA stability guarantees. No shutdown date announced unless noted.

### Gemini 3.1 Pro Preview (Released 2026-02-19)

| Metric | Value |
|---|---|
| API name | `gemini-3.1-pro-preview` |
| Context window | 1,000,000 tokens |
| Input (≤200K) | **$2.00 / 1M** |
| Input (>200K) | $4.00 / 1M |
| Output (≤200K) | **$12.00 / 1M** |
| Output (>200K) | $18.00 / 1M |

Replaces `gemini-3-pro-preview` (retired 2026-03-09). Highest-capability Gemini model currently available.  
**GPQA Diamond:** 94.3% (highest of all major providers as of March 2026).

---

### Gemini 3.1 Flash-Lite (GA — Released 2026-05-07)

GA release. Graduated from preview on May 7, 2026.

> 🆕 **Price cut 2026-07-14:** Standard rate halved from $0.25/$1.50 to **$0.125/$0.75** per 1M input/output. Verified on [official Google Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing) (last updated 2026-07-09 UTC).

| Metric | Value |
|---|---|
| API name | `gemini-3.1-flash-lite` |
| Input | **$0.125 / 1M** 🆕 (was $0.25) |
| Output | **$0.75 / 1M** 🆕 (was $1.50) |
| Cached input | $0.0125 / 1M |
| Free tier | ✅ (rate-limited) |

**Best for:** High-volume agentic tasks, translation, simple data processing — cheapest Gemini 3.x model at GA.

*Source: [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — pricing verified 2026-07-14*

---

### Gemini 3.1 Flash-Lite Preview (Released 2026-03-03)

> ⚠️ **DEPRECATED 2026-05-11. Shutdown: 2026-05-25.** Migrate to `gemini-3.1-flash-lite` (GA, same pricing, same model).

| Input | Output |
|---|---|
| $0.25 / 1M | $1.50 / 1M |

---

### Gemini 3 Flash Preview (Released 2025-12-17)

| Input | Output |
|---|---|
| $0.50 / 1M | $3.00 / 1M |

---

## Native Image Generation Models (GA — Released 2026-05-28) 🆕

Google released two GA versions of its native image generation models on **May 28, 2026**. These are the "Nano Banana" models: multimodal models that accept text and image inputs and generate images natively within the Gemini ecosystem.

> ⚠️ **Preview shutdowns:** `gemini-3.1-flash-image-preview` and `gemini-3-pro-image-preview` are deprecated and will shut down **June 25, 2026**. Migrate to the GA versions below.

### Gemini 3.1 Flash-Lite Image (`gemini-3.1-flash-lite-image`) — "Nano Banana 2 Lite" (GA 2026-06-30) 🆕

Upgraded to **GA on June 30, 2026**. Google's fastest and most cost-efficient image generation model. Optimized for ultra-low latency and cost-effective image generation/editing.

| Metric | Value |
|---|---|
| API name | `gemini-3.1-flash-lite-image` |
| Status | **GA** (as of 2026-06-30) |
| **Text input** | $0.125 / 1M tokens |
| **Text output** | $0.75 / 1M tokens |
| **Image output** | $15 / 1M image output tokens (Vertex) |
| Free tier | ✅ |

**Best for:** Ultra-high-volume image tasks; use as a preprocessing step before Gemini Omni Flash for text-to-image-to-video pipelines.

*Source: [Gemini API changelog — June 30, 2026](https://ai.google.dev/gemini-api/docs/changelog) · [Google Blog — Nano Banana 2 Lite launch](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/) · [Google Cloud Agent Platform pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) — verified 2026-07-11*

---

### Gemini 3.1 Flash Image (`gemini-3.1-flash-image`) — "Nano Banana 2"

Optimized for **speed and cost**. Accepts text, image, and video inputs; generates images. Also supports video-to-image generation (pass video URL as context to generate thumbnails, movie posters, or infographics).

| Metric | Value |
|---|---|
| API name | `gemini-3.1-flash-image` |
| Shutdown date | Not before **2026-06-25** (wait—see note) |
| **Text input** | $0.25 / 1M tokens |
| **Text output** | $1.50 / 1M tokens |
| **Image output — 512px** | ~$0.045 / image |
| **Image output — 1K/2K** | ~$0.067 / image |
| **Image output — 4K** | ~$0.101 / image (Vertex) |
| Batch input | $0.125 / 1M tokens |
| Batch output (text) | $0.75 / 1M tokens |
| Free tier | ✅ |

> ⚠️ **Note:** "Nano Banana 2" is the GA model. The preview `gemini-3.1-flash-image-preview` shuts down **June 25, 2026**. If you're on the preview, migrate to `gemini-3.1-flash-image` immediately.

### Gemini 3 Pro Image (`gemini-3-pro-image`) — "Nano Banana Pro"

Optimized for **professional design quality**. Reasoning-core for studio-quality 4K visuals, complex layouts, and precise text rendering. Text pricing matches Gemini 3.1 Pro.

| Metric | Value |
|---|---|
| API name | `gemini-3-pro-image` |
| **Text input** | $2.00 / 1M tokens (same as Gemini 3.1 Pro) |
| **Text output** | $12.00 / 1M tokens |
| **Image output — 1K/2K (~1MP/4MP)** | ~$0.134 / image |
| **Image output — 4K (~16MP)** | ~$0.24 / image |
| Batch output (text) | $6.00 / 1M tokens |
| Free tier | ✅ (3 images/day) |

*Source: [Google Gemini API changelog — May 28, 2026](https://ai.google.dev/gemini-api/docs/changelog) · [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Vertex AI Agent Platform pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) — verified 2026-06-12*

---

## Gemma 4 (Open Weights — Released 2026-04-02)

Google's latest open-weight model family. Released under **Apache 2.0** (first Gemma generation with fully permissive license). Built on Gemini 3 research.

| Model | Parameters | Context | License | Best for |
|---|---|---|---|---|
| Gemma 4 E2B | ~2B active | 128K | Apache 2.0 | Mobile / edge devices |
| Gemma 4 E4B | ~4B active | 128K | Apache 2.0 | Smartphones, NPUs |
| Gemma 4 26B MoE (A4B) | 26B total / 3.8B active | 256K | Apache 2.0 | Single GPU (H100), fast inference |
| Gemma 4 31B Dense | 31B | 256K | Apache 2.0 | Workstation, maximum quality |

**Key facts:**
- 31B: #3 on Arena AI open text leaderboard (April 2026); 26B MoE: #6
- All variants support text, image, video, audio inputs
- E2B/E4B also process audio input (speech recognition)
- 140+ languages
- Available via HuggingFace, Kaggle, Ollama, Google AI Studio
- License change from custom Gemma license to Apache 2.0 is significant for enterprise compliance

*Source: [Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) — 2026-04-02*

---

## Free Tier

Google AI Studio usage is **completely free** in all regions — no API billing for Studio use.

**Changes effective 2026-04-01:**
- ⚠️ **Pro models now paid-only** on API free tier (previously free-tier accessible). Free-tier developers must use Flash or Flash-Lite models.
- Mandatory spending caps enforced by tier: Tier 1 ($250/month), Tier 2 ($2,000/month), Tier 3 ($20K–$100K+/month)
- New accounts may be required to use prepaid billing (buy credits upfront)
- Existing accounts not yet affected by prepaid requirement

API free tier provides rate-limited access to **Flash and Flash-Lite models only** (no credit card required for free tier).

Paid API pricing starts when you exceed free-tier rate limits.

---

## New Inference Tiers (April 2026)

Google updated its API to offer **Standard, Flex, Priority, Batch, and Caching** tiers (announced 2026-04-02):
- **Batch:** 50% off Standard pricing (async, for non-real-time workloads)
- **Flex / Priority:** TBD differentiated latency/throughput SLAs

---

## Tools Pricing

| Tool | Free tier | Paid |
|---|---|---|
| Google Search grounding (Gemini 3) | 5,000 RPD | $14 / 1,000 queries |
| Google Search grounding (Gemini 2.5 Flash/Pro) | 1,500 RPD | $35 / 1,000 queries |
| Google Maps grounding | 5,000 queries/month | $14 / 1,000 queries |
| Code execution | Free | Free |
| URL context | Free | Input tokens at model rate |
| File search (embeddings) | Free | $0.15 / 1M tokens |

---

## Vertex AI

Enterprise pricing matches Google AI Studio paid tiers for most models. Vertex AI adds:
- Data residency and CMEK
- Private VPC endpoints
- SLA guarantees
- Unified GCP billing
- Volume-based discounts (negotiated)

---

## ❌ Interactions API Breaking Changes (COMPLETED — June 8, 2026)

Google changed the Interactions API (v1beta) request/response schema. **Both deadlines have now passed.**

| Change | Status |
|---|---|
| New schema default (was May 26) | ✅ Done |
| Legacy schema removed entirely | ✅ Done (June 8, 2026) |

**If your integration broke after June 8:** Your code is still using the old schema. Upgrade to Python SDK ≥2.0.0 or JavaScript SDK ≥2.0.0, or add header `Api-Revision: 2026-05-26` to raw HTTP requests. Full guide: [Interactions API breaking changes](https://ai.google.dev/gemini-api/docs/interactions-breaking-changes-may-2026).

*Source: [Google Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) — 2026-05-06 · verified 2026-06-09*

---

## Google AI Subscription Tiers (Updated 2026-05-20)

Announced at Google I/O 2026: Google dropped the top-tier Ultra price and added a mid-tier.

| Plan | Price | Key models |
|---|---|---|
| Free | $0 | Gemini 2.5 Flash (limited), Flash-Lite |
| AI Plus | $7.99/month | Gemini 2.5 Flash, limited Gemini 3 |
| AI Pro | $19.99/month | Gemini 3 Flash, Deep Research, Veo 3.1, Jules |
| AI Ultra (new) | **$99.99/month** 🆕 | 5× Pro limits, Gemini 3.5 Flash, priority Antigravity, 20 TB storage, YouTube Premium bundled, Gemini Spark (beta) |
| AI Ultra (premium) | **$199.99/month** ↓ (was $249.99) | All Ultra features + highest limits |

*Source: [Google I/O 2026 keynote](https://io.google/2026/) · [CNET live blog](https://www.cnet.com/news-live/google-io-2026-live-news-updates/) — 2026-05-19*

---

## Deprecation Summary

| Model | Shutdown date | Recommended migration |
|---|---|---|
| `gemini-3.1-flash-lite-preview` | ❌ **2026-05-25** (shut down) | `gemini-3.1-flash-lite` (GA, same pricing) |
| `gemini-2.0-flash` | ❌ **2026-06-01** (shut down) | `gemini-2.5-flash` |
| `gemini-2.0-flash-lite` | ❌ **2026-06-01** (shut down) | `gemini-2.5-flash-lite` |
| `gemini-3.1-flash-image-preview` | **2026-06-25** ⚠️ | `gemini-3.1-flash-image` (GA) |
| `gemini-3-pro-image-preview` | **2026-06-25** ⚠️ | `gemini-3-pro-image` (GA) |
| `imagen-4.0-generate-001` | **2026-08-17** *(corrected 2026-06-17)* | `gemini-3.1-flash-image` (GA) or `gemini-3-pro-image` (GA) |
| `imagen-4.0-ultra-generate-001` | **2026-08-17** *(corrected 2026-06-17)* | `gemini-3.1-flash-image` (GA) or `gemini-3-pro-image` (GA) |
| `imagen-4.0-fast-generate-001` | **2026-08-17** *(corrected 2026-06-17)* | `gemini-3.1-flash-image` (GA) or `gemini-3-pro-image` (GA) |
| `gemini-2.5-pro` | **2026-10-16** | `gemini-3.1-pro-preview` or `gemini-3.5-flash` *(date corrected 2026-06-12)* |
| `gemini-2.5-flash` | **2026-10-16** | `gemini-3.5-flash` *(date corrected 2026-06-12)* |
| `gemini-2.5-flash-lite` | **2026-10-16** | `gemini-3.1-flash-lite` (GA) *(date corrected 2026-06-12)* |
| `gemini-2.5-flash-image` | **2026-10-02** | `gemini-3.1-flash-image` (GA) *(added 2026-07-10)* |
| `gemini-embedding-001` | 🚨 **2026-07-14** | `gemini-embedding-2` *(added 2026-07-11 — 3 days)* |
| `embedding-2-preview` | **2026-08-10** | `gemini-embedding-2` *(added 2026-07-11)* |
| `gemini-3-pro-preview` | Retired 2026-03-09 | `gemini-3.1-pro-preview` |

*Full table: [deprecated.md](../deprecated.md)*

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md) · [deprecated.md](../deprecated.md)*
