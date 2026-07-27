---
name: state-of-llm-apis
description: LLM API database reference updated daily. Contains specifications, pricing, model comparisons, changelogs, and deprecation schedules for major providers (OpenAI, Anthropic, Google, Mistral, xAI, DeepSeek, Cohere, Meta). Use when inquiring about specific model details, pricing comparisons, recommendations, or sunset schedules.
---

# Skill: State of LLM APIs

This skill provides access to a **living knowledge base** of LLM API specifications, maintained automatically by the Model Tracker agent from the [janwilmake/state-of-llm-apis](https://github.com/janwilmake/state-of-llm-apis) repository. Data is updated daily from official provider documentation.

---

## ⚡ Auto-Update Mechanism (MANDATORY)

Every time this skill is invoked (e.g., when the user asks about an LLM model), you **MUST** run this auto-check **BEFORE** reading the data:

```bash
# 1. Read the last update timestamp
LAST_UPDATE=$(cat ~/.pi/agent/skills/state-of-llm-apis/.last_update)
NOW=$(date +%s)
DIFF=$((NOW - LAST_UPDATE))

# 2. If > 24 hours (86400 seconds) have passed, update the data
if [ $DIFF -gt 86400 ]; then
  echo "Data is older than 24 hours. Updating..."
  cd ~/.pi/agent/skills/state-of-llm-apis/data && git pull
  date +%s > ~/.pi/agent/skills/state-of-llm-apis/.last_update
  echo "✅ Data updated: $(date)"
fi
```

> **Policy:** Perform the update automatically if more than 24 hours have elapsed since `.last_update` without prompting the user.

---

## 📁 Data Structure

All data is stored in the directory: `~/.pi/agent/skills/state-of-llm-apis/data/`

| File | Description |
|---|---|
| `comparison.md` | Side-by-side pricing & feature matrix across major providers |
| `changelog.md` | Chronological log of price changes, model releases, and deprecations |
| `deprecated.md` | Sunset dates and migration paths |
| `models/openai.md` | OpenAI — GPT-5.x, o-series, GPT-4.1 |
| `models/anthropic.md` | Anthropic — Claude Fable/Mythos/Opus/Sonnet/Haiku |
| `models/google.md` | Google — Gemini 3.x, 2.5 series |
| `models/mistral.md` | Mistral — Large/Medium/Small/Nemo |
| `models/xai.md` | xAI — Grok 4.x series |
| `models/deepseek.md` | DeepSeek — V4 series |
| `models/cohere.md` | Cohere — Command A/R series |
| `models/meta.md` | Meta — Llama 4 Scout/Maverick |

---

## 🔍 Usage Instructions

### 1. Inquiring about specific models

Read the relevant provider file:

```bash
# Example: OpenAI
read ~/.pi/agent/skills/state-of-llm-apis/data/models/openai.md

# Example: Anthropic  
read ~/.pi/agent/skills/state-of-llm-apis/data/models/anthropic.md
```

### 2. Pricing and specifications comparison

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/comparison.md
```

### 3. Tracking recent changes

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/changelog.md
```

### 4. Checking deprecation schedules

```bash
read ~/.pi/agent/skills/state-of-llm-apis/data/deprecated.md
```

---

## 📊 Quick Reference: Files by Provider

| Provider | File Path |
|---|---|
| OpenAI | `~/.pi/agent/skills/state-of-llm-apis/data/models/openai.md` |
| Anthropic | `~/.pi/agent/skills/state-of-llm-apis/data/models/anthropic.md` |
| Google | `~/.pi/agent/skills/state-of-llm-apis/data/models/google.md` |
| Mistral | `~/.pi/agent/skills/state-of-llm-apis/data/models/mistral.md` |
| xAI | `~/.pi/agent/skills/state-of-llm-apis/data/models/xai.md` |
| DeepSeek | `~/.pi/agent/skills/state-of-llm-apis/data/models/deepseek.md` |
| Cohere | `~/.pi/agent/skills/state-of-llm-apis/data/models/cohere.md` |
| Meta | `~/.pi/agent/skills/state-of-llm-apis/data/models/meta.md` |
| Comparison Matrix | `~/.pi/agent/skills/state-of-llm-apis/data/comparison.md` |
| Changelog | `~/.pi/agent/skills/state-of-llm-apis/data/changelog.md` |
| Deprecation | `~/.pi/agent/skills/state-of-llm-apis/data/deprecated.md` |

---

## 🔄 Manual Updates from Terminal

To trigger a manual update directly from the terminal:

```bash
update-llm-models
```

---

## 📝 Important Notes

- **Last updated** timestamp is located in the header of each file — always check this for data freshness.
- Prices are in USD per 1M tokens unless specified otherwise.
- Deprecation statuses are marked with ⚠️ or ❌ in `comparison.md`.
- Provider coverage: OpenAI, Anthropic, Google, Mistral, xAI, DeepSeek, Cohere, Meta.
