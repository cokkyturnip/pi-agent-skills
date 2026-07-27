# Meta Llama Model Catalog

> **Source:** [Meta AI](https://ai.meta.com) · [OpenRouter](https://openrouter.ai) · [Together AI](https://together.ai) · **Verified:** 2026-04-11

---

## Overview

Meta has two parallel model tracks as of April 2026:
1. **Muse series** (new) — Proprietary models from Meta Superintelligence Labs (MSL). Led by Alexandr Wang (former Scale AI CEO).
2. **Llama series** — Open-weight models under the [Meta Llama Community License](https://llama.meta.com/license). Accessed via third-party providers.

---

## Muse Spark (Released 2026-04-08) — Current Meta Flagship

First model from Meta Superintelligence Labs. Proprietary (closed weights), rebuilt from scratch with new infrastructure and architecture. Internally codenamed "Avocado".

| Metric | Value |
|---|---|
| API availability | Private preview to select partners only |
| Public API | ❌ Not yet available |
| Consumer access | ✅ Meta AI app, meta.ai website |
| Platform rollout | WhatsApp, Instagram, Facebook, Messenger, Ray-Ban AI glasses (coming weeks) |
| Modalities | Text, images, video, multimodal perception |
| Special modes | "Contemplating mode" (multi-agent orchestration) |
| Strengths | Multimodal perception, reasoning, health responses (1,000 physician collaboration), shopping recommendations |
| Current gaps | Long-horizon agentic systems, coding workflows |
| Next model | "Watermelon" (in development) |

**Key context:** Meta's shift from open-source Llama to a proprietary model. The company says it may open-source parts of Muse Spark in the future. API pricing not announced; commercial API launch date TBD.  
*Source: [Meta blog](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/), TechCrunch, NYT — 2026-04-08*

---

## Llama Models (Open Weights)

Meta releases Llama models as **open weights** under the [Meta Llama Community License](https://llama.meta.com/license). There is no official Meta-hosted API with per-token billing — you access Llama models through:
1. **Third-party API providers** (Together AI, Groq, Fireworks AI, AWS Bedrock, Azure AI, etc.)
2. **Self-hosting** (on your own infrastructure using vLLM, Ollama, llama.cpp, etc.)
3. **Meta's own apps** (Meta AI on WhatsApp/Messenger/Instagram — consumer product, not API)

Pricing below reflects typical third-party provider rates as of April 2026.

---

## Current Models

### Llama 4 Scout (Released 2025-04-05)

Meta's open-weight frontier model. Mixture-of-Experts architecture. Extraordinary 10 M token context window.

| Metric | Value |
|---|---|
| Parameters | 109B total (17B active per forward pass × 16 experts) |
| Context window | 10,000,000 tokens (10 M) |
| Modalities | Text + Images |
| Typical API price (input) | ~$0.08 / 1M tokens (OpenRouter, DeepInfra) |
| Typical API price (output) | ~$0.30 / 1M tokens |
| Weights | Open — [HuggingFace](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) |

**Best for:** Long-document reasoning, multimodal tasks, cost-sensitive production at frontier quality.

---

### Llama 4 Maverick (Released 2025-04-05)

Larger MoE model in the Llama 4 family.

| Parameters | Context | Input (typical) | Output (typical) |
|---|---|---|---|
| 400B total (17B active × 128E) | 1,000,000 tokens | ~$0.15 / 1M | ~$0.60 / 1M |

---

### Llama 3.3 70B Instruct (Released 2024-12)

Previous-generation flagship. Still widely used and supported.

| Context | Typical input | Typical output |
|---|---|---|
| 128,000 tokens | ~$0.59 / 1M | ~$0.79 / 1M |

---

### Llama 3.1 405B Instruct

Largest dense Llama model. Higher cost than MoE variants.

| Context | Typical input | Typical output |
|---|---|---|
| 128,000 tokens | ~$3.50 / 1M | ~$3.50 / 1M |

---

## Key Provider Options for Llama

| Provider | Notable features |
|---|---|
| **Together AI** | Broadest Llama selection, fine-tuning, competitive pricing |
| **Groq** | Fastest inference (LPU hardware), limited models |
| **Fireworks AI** | Low latency, strong uptime SLAs |
| **AWS Bedrock** | Enterprise compliance, managed service |
| **Azure AI** | Enterprise compliance, integrated with Azure ecosystem |
| **Cloudflare Workers AI** | Edge inference, generous free tier |
| **Nebius AI** | European data residency option |
| **Ollama** | Local/self-hosted, free |

---

## Self-Hosting Guidance

For >10M tokens/month, self-hosting on cloud GPUs typically becomes cost-competitive with managed APIs:
- 70B model requires 2× A100 80GB or 4× A10G
- 8B model runs on single A10G or consumer 4090

Use [vLLM](https://github.com/vllm-project/vllm) for production inference or [Ollama](https://ollama.ai) for local development.

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md)*
