# Anthropic Model Catalog

> **Source:** [Anthropic API Pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) · **Verified:** 2026-08-01

---

## Current Recommended Models (Fable 5 / Mythos-class)

### Claude Fable 5 (Released 2026-06-09) ✅ RESTORED 2026-07-01

> ✅ **ACCESS RESTORED 2026-07-01.** Export controls on Fable 5 were lifted on June 30, 2026. Fable 5 returned globally on July 1 across Claude Platform, claude.ai, Claude Code, and Claude Cowork. AWS, Google Cloud, and Microsoft Foundry access is being restored as quickly as possible.
>
> ✅ **FREE WINDOW CLOSED 2026-07-12 at 11:59 PM PT.** The promotional free-access window for Pro, Max, Team, and select Enterprise plans has now ended. As of July 13, 2026, access to Fable 5 requires **usage credits** billed at $10/$50 per 1M tokens. If you have not enabled usage credits and are calling `claude-fable-5`, requests will fail. Enable usage credits in the [Claude Console](https://platform.claude.com/settings/billing) or fall back to `claude-opus-4-8` ($5/$25 per 1M).
>
> ⚠️ **Data retention requirement:** Claude Fable 5 requires 30-day data retention — not available under zero data retention. | **Caution:** Keep `claude-opus-4-8` in fallback configuration for production systems.
>
> *Source: [Anthropic — Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5) — 2026-06-30 · [@claudeai on X — Jul 7, 2026](https://x.com/claudeai/status/2074548242386178258) · verified 2026-07-13*

Anthropic's most capable widely available model. The first **Mythos-class** model released for general use — sits above the Opus tier. Built for the most demanding reasoning, long-horizon agentic work, large-scale coding, and complex knowledge work. Uses the same underlying model as Claude Mythos 5 but with strict safety classifiers for cybersecurity, biology, chemistry, and model distillation domains.

> ⚠️ **Data retention requirement:** Claude Fable 5 requires **30-day data retention** on the Claude API — it is **not available under zero data retention**. Plan accordingly for compliance requirements.

| Metric | Value |
|---|---|
| API name | `claude-fable-5` |
| Context window | 1,000,000 tokens |
| Max output | 128,000 tokens |
| Input | **$10.00 / 1M** |
| Output | **$50.00 / 1M** |
| Prompt cache (read) | ~10% of input ($1.00 / 1M) |
| Thinking mode | **Adaptive thinking — always on; cannot be disabled** |

**Key facts:**
- Released **2026-06-09** on Claude API, Amazon Bedrock, Vertex AI, Microsoft Foundry
- ❌ **SUSPENDED 2026-06-12** — 2026-07-01 ✅ **RESTORED** — U.S. export control directive lifted June 30; global access restored July 1
- **Pricing: ~2× Claude Opus 4.8** ($5/$25 → $10/$50 per 1M). Cheaper than Mythos Preview (~$25/$125)
- **SWE-bench Pro: 80.3%** — 11 points ahead of second-best model (Claude Opus 4.8 at 69.2%)
- **GDPval-AA: 1,932** (vs 1,890 for Opus 4.8, 1,769 for GPT-5.5, 1,314 for Gemini 3.1 Pro)
- **GDPpdf: 29.8%** on visual document reasoning (vs 22.5% Opus 4.8, 24.9% GPT-5.5)
- Adaptive thinking is the **only** thinking mode: `thinking: {"type": "disabled"}` is not supported (returns 400)
- `thinking.display` defaults to `"omitted"` — set `display: "summarized"` to receive readable thinking summaries
- Safety classifiers trigger `stop_reason: "refusal"` — not billed if refused before any output is generated
- Optional `fallbacks` parameter: on refusal, re-runs on another Claude model (beta on Claude API and AWS)
- **Subscription rollout:** Pro, Max, Team, and select Enterprise plans had Fable 5 included for up to 50% of weekly usage limits through **July 12, 2026 at 11:59 PM PT** (now closed). As of July 13, usage credits are required ($10/$50 per 1M). AWS, Google Cloud, and Microsoft Foundry access is restored.
- Also available: **Claude Mythos 5** (`claude-mythos-5`) — same model without safety classifiers; restricted to **approved U.S. organizations** (Project Glasswing) as of 2026-07-01 restoration

**Supported features:** `effort` parameter, task budgets, memory tool, context editing, compaction, vision (text, image, file inputs)

*Source: [Anthropic — Introducing Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [Claude API docs](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) — 2026-06-09 · [Anthropic suspension statement](https://www.anthropic.com/news/fable-mythos-access) — 2026-06-12 · verified 2026-06-13*

---

## Claude Sonnet 5 (Released 2026-06-30) 🆕 NEW

Anthropic's most agentic Sonnet model. Closes the gap with Opus 4.8 on agentic tasks at significantly lower cost. Default model for Free and Pro Claude plans as of 2026-06-30.

> ⚠️ **Tokenizer change:** Sonnet 5 uses an updated tokenizer (same type as introduced with Opus 4.7). Input can map to up to 1.35× more tokens vs. Sonnet 4.6 for code, JSON/XML, and non-English text. Introductory pricing is set to make the transition roughly cost-neutral.

> ⚠️ **Pricing step-up:** Introductory pricing of $2/$10 per 1M tokens is in effect **through August 31, 2026**. Standard pricing of $3/$15 takes effect **September 1, 2026**.

| Metric | Value |
|---|---|
| API name | `claude-sonnet-5` |
| Context window | 1,000,000 tokens |
| Max output | 128,000 tokens |
| Input (intro, through 2026-08-31) | **$2.00 / 1M** |
| Output (intro, through 2026-08-31) | **$10.00 / 1M** |
| Input (standard, from 2026-09-01) | $3.00 / 1M |
| Output (standard, from 2026-09-01) | $15.00 / 1M |
| 5-min Cache write (intro) | $2.50 / 1M |
| 1-hr Cache write (intro) | $4.00 / 1M |
| Cache read (intro) | $0.20 / 1M |
| Batch input (intro) | $1.00 / 1M |
| Batch output (intro) | $5.00 / 1M |

**Best for:** Agentic workflows, multi-step tool use, coding, browser/terminal tasks, professional deliverables. Near-Opus-4.8 performance at Sonnet pricing.

**Key facts:**
- Default model for **Free and Pro** plans; available to Max, Team, Enterprise, Claude Code
- Available on Claude Platform API, AWS Bedrock, Google Vertex AI, Microsoft Foundry, GitHub Copilot
- Supports all Fable/Opus features: effort parameter, task budgets, memory tool, context editing, compaction, vision
- Long context: full 1M token window at standard pricing (no long-context premium)
- Rate limits increased across all tiers on April 26, 2026 (Chat, Cowork, Claude Code, API)
- Three tiers simplified: Start, Build, Scale

*Source: [Anthropic — Introducing Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5) — 2026-06-30 · [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing) — verified 2026-07-09*

---

## Claude 5 Opus Generation

### Claude Opus 5 (Released 2026-07-24) 🆕 NEW

Anthropic's current Opus-tier flagship — a step-change upgrade over Opus 4.8 for deep reasoning, long-horizon agentic coding, and test-time compute scaling. Delivers near-Fable-5 performance at roughly half the cost (Fable 5 is $10/$50). New default model on Claude Max; strongest model available on Claude Pro.

| Metric | Value |
|---|---|
| API name | `claude-opus-5` |
| AWS Bedrock ID | `anthropic.claude-opus-53` |
| Google Cloud ID | `claude-opus-5` |
| Context window | 1,000,000 tokens (1M is both default and maximum; no smaller variant) |
| Max output | 128,000 tokens |
| Input (≤200K) | **$5.00 / 1M** |
| Output (≤200K) | **$25.00 / 1M** |
| Input (>200K) | $10.00 / 1M |
| Output (>200K) | $37.50 / 1M |
| Batch input / output (50% off) | $2.50 / $12.50 per 1M |
| **Fast Mode input** | **$10.00 / 1M** (2.5× default speed, 2× price) |
| **Fast Mode output** | **$50.00 / 1M** |
| Thinking | **Adaptive thinking — on by default; cannot be disabled** (manual `thinking` budget removed, returns 400) |
| Effort parameter | Supports `low`, `medium`, `high`, and the new **`max`** level |
| Bash tool system prompt | Adds 325 input tokens (same as Opus 4.8 / 4.7) |
| Training data cutoff | May 2026 |
| Knowledge cutoff (reliable) | January 2026 |

**Best for:** Complex agentic coding, long-horizon multi-step tasks, deep multi-step reasoning, professional knowledge work, scientific research. Same price as Opus 4.8 with materially stronger capability.

**Key facts:**
- Released **2026-07-24** on Claude API, Amazon Bedrock, Google Cloud Vertex AI, Microsoft Foundry
- **Same price as Opus 4.8** ($5/$25) — drop-in capability upgrade
- **Frontier-Bench v0.1:** more than doubled Opus 4.8's score at lower cost per completed task
- **CursorBench 3.2** (max effort): within 0.5% of Fable 5's peak at ~half the cost per task
- **ARC-AGI 3:** 3× the next-best model's score
- **OSWorld 2.0:** better than Fable 5's peak at just over one-third of the cost
- **New `max` reasoning effort** — converts extra compute into better results (test-time scaling)
- `low`/`medium` effort produce strong quality at a fraction of the tokens/latency of higher settings
- Strong code review / bug-finding: high true-positive rate, few false positives, accurate at low effort
- Mid-conversation tool changes supported; improved vision (charts, docs, diagrams, UI replication) and 1M long-context instruction following
- **Cyber posture:** close to Mythos 5 at finding vulnerabilities, but not trained on cyber tasks; "substantially behind" Mythos 5 on exploitation — generally available (no Glasswing gating)
- No tokenizer-penalty caveat relative to Opus 4.8 (uses the same Opus-4.7+ tokenizer family)

**Migration from Opus 4.8:** Update `model` to `claude-opus-5`. Pricing identical. If you used manual `thinking: {type: "enabled", budget_tokens: N}`, switch to adaptive thinking with the `effort` parameter (returns 400 otherwise). Opus 4.8 remains available as a fallback.

*Source: [Anthropic — Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5) · [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5) · [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) — verified 2026-07-25*

---

## Claude 4.x Generation

### Claude Opus 4.8 (Released 2026-05-28)

Anthropic's previous Opus flagship (superseded by Opus 5 on 2026-07-24 at the same price — see above). Builds on Opus 4.7 with stronger agentic coding, better tool triggering, and improved long-context coherence. Adds Dynamic Workflows (parallel multi-step coding), Effort Control (per-call reasoning depth), and Fast Mode now 3× cheaper than previous generations.

| Metric | Value |
|---|---|
| API name | `claude-opus-4-8` |
| Context window | 1,000,000 tokens (200K on Microsoft Foundry) |
| Max output | 128,000 tokens (300K via Batch API) |
| Input (≤200K) | **$5.00 / 1M** |
| Output (≤200K) | **$25.00 / 1M** |
| Input (>200K) | $10.00 / 1M |
| Output (>200K) | $37.50 / 1M |
| Cache write | $12.50 / 1M |
| Cache read | $1.00 / 1M |
| **Fast Mode input** | **$10.00 / 1M** (research preview; request via account manager) |
| **Fast Mode output** | **$50.00 / 1M** |

**Best for:** Complex software engineering, long-horizon agentic tasks, autonomous coding, multi-step reasoning, professional knowledge work.  
**SWE-bench Pro:** 69.2% (vs 64.3% on Opus 4.7) | **Terminal-Bench:** +8.5 pts vs Opus 4.7  
**Prompt cache minimum:** 1,024 tokens (reduced from 4,096 on Opus 4.7)

**New features vs Opus 4.7:**
- **Dynamic Workflows** (Claude Code, research preview): parallel sub-agent coordination for very large-scale coding tasks
- **Effort Control:** per-call reasoning depth for cost management
- **Mid-conversation system messages:** `role: "system"` messages accepted after user turns — preserves prompt cache on long agentic loops; no beta header required
- **Fast Mode** at $10/$50 per 1M — 3× cheaper than Opus 4.7's $30/$150 (access: contact account manager)
- **Better tool triggering:** fewer missed tool calls vs Opus 4.7

**No tokenizer change:** Migrating from Opus 4.7 to 4.8 carries no additional token-count penalty. (The tokenizer warning still applies to teams migrating from Opus 4.6 → 4.8.)

*Source: [Anthropic announcement](https://www.anthropic.com/news/claude-opus-4-8) · [What's new in Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) — 2026-05-28 · [CloudZero Opus 4.8 pricing](https://www.cloudzero.com/blog/claude-opus-4-8-pricing/) — verified 2026-06-09*

---

### Claude Opus 4.7 (Released 2026-04-16)

Previous flagship; still active. Stronger than 4.6 on coding and vision. Fast Mode available at $30/$150 per 1M (6× standard) — compare with Opus 4.8's new $10/$50 rate.

| Metric | Value |
|---|---|
| API name | `claude-opus-4-7` |
| Context window | 1,000,000 tokens |
| Max output | 128,000 tokens |
| Input (≤200K) | **$5.00 / 1M** |
| Output (≤200K) | **$25.00 / 1M** |
| Input (>200K) | $10.00 / 1M |
| Output (>200K) | $37.50 / 1M |
| Cache write | $6.25 / 1M |
| Cache read | $0.50 / 1M |

**CursorBench:** 70% (vs 58% for Opus 4.6) | **Rakuten-SWE-Bench:** 3× more production tasks resolved vs Opus 4.6  
**Cyber safeguards:** Built-in detection for prohibited cybersecurity uses; apply to [Cyber Verification Program](https://claude.com/form/cyber-use-case)

> ⚠️ **Tokenizer change (vs Opus 4.6):** Opus 4.7 introduced a new tokenizer that may use **up to 35% more tokens** for the same input text versus Opus 4.6. Effective per-request cost can be up to 1.35× higher on code, JSON/XML, and non-English text. This warning does **not** apply to Opus 4.7 → 4.8 migrations.

*Source: [Anthropic announcement](https://www.anthropic.com/news/claude-opus-4-7) — 2026-04-16 · [CloudZero tokenizer analysis](https://www.cloudzero.com/blog/claude-opus-4-7-pricing/) — verified 2026-06-09*

---

### Claude Opus 4.6 (Released 2026-02-04)

Legacy; still active. 1 M token context at standard pricing — no long-context premium.

| Metric | Value |
|---|---|
| API name | `claude-opus-4-6` |
| Context window | 1,000,000 tokens |
| Max output | 128,000 tokens |
| Input (≤200K) | **$5.00 / 1M** |
| Output (≤200K) | **$25.00 / 1M** |
| Input (>200K) | $10.00 / 1M |
| Output (>200K) | $37.50 / 1M |
| Cache write | $6.25 / 1M |
| Cache read | $0.50 / 1M |

**Best for:** Complex reasoning, full-codebase analysis, autonomous agents, scientific research.  
**GPQA Diamond:** 91.3%

---

### Claude Sonnet 4.6

Balanced performance and cost. Same price as Sonnet 4.5.

| Metric | Value |
|---|---|
| API name | `claude-sonnet-4-6` |
| Context window | 1,000,000 tokens |
| Input (≤200K) | **$3.00 / 1M** |
| Output (≤200K) | **$15.00 / 1M** |
| Input (>200K) | $6.00 / 1M |
| Output (>200K) | $22.50 / 1M |
| Cache write | $3.75 / 1M |
| Cache read | $0.30 / 1M |

**Best for:** Production chatbots, coding assistants, balanced cost/quality workloads.

---

### Claude Sonnet 4.5

Previous Sonnet; identical pricing to 4.6. Still supported and available.

| Input | Output | Cache write | Cache read |
|---|---|---|---|
| $3.00 / 1M | $15.00 / 1M | $3.75 / 1M | $0.30 / 1M |

---

### Claude Haiku 4.5

Fastest and cheapest in the current lineup.

| Metric | Value |
|---|---|
| API name | `claude-haiku-4-5` |
| Context window | 200,000 tokens |
| Input (≤200K) | **$1.00 / 1M** |
| Output (≤200K) | **$5.00 / 1M** |
| Input (>200K) | $2.00 / 1M |
| Output (>200K) | $7.50 / 1M |
| Cache write | $1.25 / 1M |
| Cache read | $0.10 / 1M |

**Best for:** High-volume classification, summarization, simple Q&A, latency-sensitive tasks.

---

## Batch API

**50% discount** on all models. Asynchronous processing via the Message Batches API. No SLA on turnaround, typically a few minutes to several hours.

## Prompt Caching

- **Cache write:** 25% premium over standard input rate (charged once to store)
- **Cache read:** ~10% of standard input rate (very cheap on re-use)
- Useful for multi-turn conversations, repeated system prompts, large document contexts

## Extended Thinking

Claude models support `extended_thinking` mode, which enables multi-step chain-of-thought reasoning. Thinking tokens are billed at standard output rates. Useful for complex math, coding, and analytical tasks.

---

## Subscription Tiers (claude.ai)

| Plan | Price | Key features |
|---|---|---|
| Free | $0 | Limited access to Claude Sonnet |
| Pro | $20/month | Higher limits, Claude Code access, priority |
| Max 5x | $100/month | 5× more usage than Pro, priority access |
| Max 20x | $200/month | 20× more usage than Pro, priority access |
| Team Standard | $25/user/month (annual) | SSO, admin controls, Slack/M365 integration |
| Team Premium | $150/user/month | All Standard + Claude Code access |
| Enterprise | Custom | SCIM, audit logs, compliance API, custom data retention |

---

## Agent SDK Billing Split — ANNOUNCED but PAUSED (Announced 2026-05-14, Paused 2026-06-15)

> ⚠️ **UPDATE 2026-06-16:** Anthropic **paused this change before it took effect** on June 15, 2026. The Agent SDK credit split is **not currently live**. Subscription usage (interactive and autonomous) continues drawing from the same pool as before. Anthropic has said it will re-announce the change with advance notice before it ships. No new date announced.

Anthropic announced plans to separate autonomous/programmatic Claude usage from interactive usage, with an original effective date of **June 15, 2026** (now paused).

**As announced, the two usage buckets would have been:**
1. **Human-in-the-loop** (interactive): terminal Claude Code, web/desktop chat, Cowork — draws from existing subscription limits.
2. **Autonomous / programmatic** (agentic): Agent SDK, `claude -p`, GitHub Actions, third-party tools (OpenClaw, Zed via ACP, Cursor, etc.) — would draw from a new **Agent SDK credit pool** billed at standard API rates.

**Announced monthly Agent SDK credits per plan:**

| Plan | Included credit (API rates) | Overage |
|---|---|---|
| Pro ($20/mo) | $20 | Billed at API rates if extra usage enabled; else stops |
| Max 5x ($100/mo) | $100 | Billed at API rates if extra usage enabled |
| Max 20x ($200/mo) | $200 | Billed at API rates if extra usage enabled |

**Developer impact (when/if it ships):** Subscriptions previously subsidized autonomous workloads at roughly 15–30× below API rates. The credit pool is billed at standard API token prices ($3/$15 per 1M on Sonnet 4.6; $5/$25 on Opus 4.7). Heavy `claude -p` or OpenClaw/Zed users who treat their plan as "unlimited agentic compute" will face major cost increases. Interactive Claude Code use is unaffected.

*Source: [Anthropic — Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) · [Zed Blog](https://zed.dev/blog/anthropic-subscription-changes) · [InfoWorld](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) — announced 2026-05-14 · paused 2026-06-15 · [Digital Applied](https://www.digitalapplied.com/blog/anthropic-claude-credit-overhaul-june-15-2026) — verified 2026-06-16*

---

## Claude Managed Agents — Scheduled Deployments & Vault Credentials (2026-06-09) 🆕

Two new public-beta capabilities added to Claude Managed Agents on **June 9, 2026** (same day as Fable 5 launch):

1. **Scheduled deployments:** Agents can now run on a cron schedule — each fire starts a new session that runs to completion. No scheduler to build or host. Use cases: nightly data syncs, weekly compliance scans, daily digests. Configurable via the platform (pause, resume, archive, trigger on demand).

2. **Vault environment variables:** Vaults now support injecting environment variables (API keys) into agent sandboxes for CLIs, SDKs, and other tools. The agent never sees the actual key — it's attached at the network boundary only for approved domains. Supports: Browserbase, KERNEL, Notion, Ramp, Sentry CLIs. Browserbase and KERNEL give agents **browser capabilities** for the first time.

*Source: [Anthropic — Claude Managed Agents update](https://www.anthropic.com/news/claude-managed-agents-scheduled-deployments) · [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview) — 2026-06-09 · verified 2026-06-10*

---

## Enterprise Analytics API (Released 2026-05-07)

Anthropic launched the **Enterprise Analytics API** — gives Enterprise plan Primary Owners programmatic access to per-user cost and adoption data across Claude, Claude Code, Cowork, and Office agents.

**Nine endpoints in two categories:**
1. **Engagement & Adoption (5 endpoints):** Per-user activity (conversations, commits, PRs, lines of code, Cowork sessions), organization-wide DAU/WAU/MAU, seat utilization
2. **Usage & Cost (4 endpoints, beta):** Per-user token consumption and USD spend, broken down by model, context window, inference region, or speed; cost over time; token usage over time

**Key facts:**
- Available on **Enterprise plans only**
- Data starts January 1, 2026; 90-day history for engagement, 365 days for cost
- 3-day engagement data delay; 4–24 hour cost data refresh; revisions possible up to 30 days
- Rate limit: 60 req/min (customizable)
- Does **not** include Bedrock-routed Claude Code data

*Source: [Anthropic Enterprise Analytics API docs](https://support.claude.com/en/articles/13694757-get-started-with-the-claude-enterprise-analytics-api) — 2026-05-07*

---

## API Rate Limit Increase (May 2026)

Effective **2026-05-06**, Anthropic raised API rate limits for Claude Opus models — enabled by new compute capacity (SpaceX Colossus 1 deal: 300MW+ / 220K+ NVIDIA GPUs). Three changes effective immediately:
1. **Claude Code 5-hour rate limits doubled** for Pro, Max, Team, and seat-based Enterprise plans
2. **Peak hours limit reduction removed** for Claude Code on Pro and Max accounts
3. **API rate limits raised considerably** for Claude Opus models (see [official rate limits page](https://platform.claude.com/docs/en/api/rate-limits))

*Source: [Anthropic — Higher limits and SpaceX compute deal](https://www.anthropic.com/news/higher-limits-spacex) — 2026-05-06*

## API Policy Change (April 2026)

Effective **2026-04-04**, Claude Pro and Max subscriptions can **no longer be used to power third-party agent frameworks** (e.g. OpenClaw). Users must connect via direct API key with pay-as-you-go token billing. Affected subscribers received a one-time credit equal to their monthly plan cost. *Source: TechCrunch, 2026-04-04*

---

## Claude Mythos Preview (2026-04-07) — Gated / Not Publicly Available

> ⚠️ **Not available via public API.** Access is restricted to ~50 partner organizations under **Project Glasswing** for cybersecurity use only.

Anthropic's most capable model to date, described as a "step change" above Claude Opus 4.6. Excels at reasoning, coding, and — most notably — autonomous vulnerability discovery in software systems. Named internally "Capybara".

| Metric | Value |
|---|---|
| API name | `claude-mythos-preview` (gated) |
| Public API | ❌ No general availability |
| Preview pricing | **~$25.00 / 1M input** · **~$125.00 / 1M output** |
| General release date | Not announced |

**Why gated:** Anthropic identified Mythos as a cybersecurity risk if broadly released. Under Project Glasswing, ~50 infrastructure partners use it solely for defensive security scanning. In internal testing, it identified thousands of zero-day vulnerabilities, many decades old.

**What developers should know:** Mythos is the precursor to the next Claude generation. Its benchmark scores substantially exceed Opus 4.6 on software engineering and reasoning. No timeline for general availability has been announced. *Source: TechCrunch, Anthropic System Card — 2026-04-07*

---

## Claude 5 Roadmap

Anthropic's Claude 5 generation is now substantially shipped. **Claude Opus 5** (`claude-opus-5`) was released **2026-07-24** — fulfilling the previously-anticipated Q3 2026 Opus milestone. **Sonnet 5** was released 2026-06-30 (intro pricing $2/$10 through Aug 31, then $3/$15). Above the Opus tier, the **Mythos-class** tier was introduced with **Claude Fable 5** (GA 2026-06-09, restored globally 2026-07-01). The current frontier is Fable 5 / Mythos 5. Separately, Anthropic's [draft S-1 filing](https://futurumgroup.com/insights/will-anthropics-draft-s-1-ignite-a-new-phase-in-the-ai-platform-race/) (2026-06-02) reported a $965B valuation and ~$30B annualized revenue run rate.

---

## Legacy Models

| Model | Status | Retirement | Notes |
|---|---|---|---|
| Claude Opus 4.7 | Active (legacy) | Not before 2026-11-28 | $5/$25 — previous flagship; still high quality |
| Claude Opus 4.6 | Active (legacy) | Not before 2026-11-24 | $5/$25 — two generations behind current |
| Claude Opus 4.5 | Active (legacy) | Not before 2026-11-24 | $5/$25 — same price as newer Opus versions |
| Claude Opus 4.1 | ⚠️ **Retires 2026-08-05** (4 days) | **2026-08-05** | `claude-opus-4-1-20250805`; $15/$75 — 3× more expensive than Opus 4.8; migrate to `claude-opus-4-8` or `claude-opus-5` (both $5/$25) |
| Claude Sonnet 4.5 | Active (legacy) | Not before 2026-09-29 | $3/$15 — same price as Sonnet 4.6 but older |
| Claude Sonnet 4 | ❌ **RETIRED 2026-06-15** | — | API name `claude-sonnet-4-20250514` — calls return errors; migrate to `claude-sonnet-4-6` |
| Claude Opus 4 | ❌ **RETIRED 2026-06-15** | — | API name `claude-opus-4-20250514` — calls return errors; migrate to `claude-opus-4-7` or `claude-opus-4-8` |
| Claude 3 Haiku | ❌ **RETIRED 2026-04-20** | **2026-04-20** | Migrate to `claude-haiku-4-5-20251001` |
| Claude 3.5 Haiku | Retired 2026-02-19 | — | Use Haiku 4.5 |
| Claude Sonnet 3.7 | Retired 2026-02-19 | — | Use Sonnet 4.6 |
| Claude 3 Opus | Retired 2026-01-05 | — | Available to paid claude.ai subscribers by special request |

*See [deprecated.md](../deprecated.md) for sunset dates.*

---

*See also: [comparison.md](../comparison.md) · [changelog.md](../changelog.md) · [deprecated.md](../deprecated.md)*
