---
name: capacity-planning
description: Use when creating, updating, or reviewing infrastructure capacity planning documents (sizing, TPS/request estimates, cost estimates) for systems with field teams, mobile agents, or API backends. Also use when numbers in PRD/architecture docs are questioned for consistency, or when a request breakdown, TPS calculation, or cloud cost estimate needs to be derived from scratch.
---

# Capacity Planning (Infrastructure Capacity Planning)

## Overview

Capacity planning methodology for field-force/API systems where **every number is traceable** — bottom-up from business volume, not vague assumptions. The source of truth is the per-endpoint request breakdown; TPS, sizing, and cost are derived from there.

## Core Principles

1. **Bottom-up, not guessing**: start from business volume (number of users × frequency), derive requests/day per endpoint, then calculate TPS & sizing.
2. **Every number must be traceable**: the "Calculation" column (volume × frequency) is mandatory — users will ask "where does this number come from?".
3. **Do not double-count**: count once per unit (e.g., 1 visit = 1 check-in, not 7 check-ins per visit). Distinguish "per visit" vs "per agent".
4. **Mark number status**: derived (✅) vs assumed (⚠️). Assumptions must have a validation path (load test).
5. **Sync all documents**: PRD + capacity docs must be updated together whenever a number changes.

## Number Status — Must Be Marked

| Status | Meaning | Example |
|--------|---------|---------|
| **Derived** | Calculated from data/volume | 2,800 visits = 400 agents × 7 |
| **Assumed** | Engineering estimate, not measured | burst factor 3–5×, capacity 50–100 TPS |
| **Conservative** | Deliberately lower than mid estimate | photos 10,000 (while range is 8–12K) |

> If an assumed number is used as the basis for a decision, **always add a note**: "ASSUMPTION for sizing (not a measurement) — validate during load test before go-live; if actual results are below the assumption, sizing should be reviewed."

## Methodology Steps

### 1. Derive Base Business Volume

| Input | Example |
|-------|---------|
| Active users (agents) | 400 |
| Work units per user per day | 7 visits |
| Total units/day | 400 × 7 = 2,800 |

### 2. Breakdown API Requests per Endpoint (Source of Truth)

Table with columns: `Endpoint | Frequency | Volume basis | Requests/day | Calculation`.

Example row (2,800 visits/day):
```
| GET /api/v1/merchants/:id | 1×/visit | 2,800 visits | 2,800 | 2,800 × 1 |
| POST /api/v1/photos/signed-url | 4×/visit | 2,800 visits | 11,200 | 2,800 × 4 |
```

**Anti-double-count rules:**
- `1×/visit` + volume 2,800 → 2,800 (not 2,800 × 7 again)
- Per-agent endpoints (login, start shift) → 400 × 1
- Photos/lamps uploaded directly to S3 via pre-signed URL → **not via API** → do not count as API requests
- Overhead (web portal, cron, health check) → +5–10% of total, not counted per endpoint

### 3. Calculate TPS per Time Window

```
Average TPS = window volume ÷ window duration (seconds)
Peak 5-minute TPS = busiest 5-minute volume ÷ 300 seconds
```

Allocate total requests/day to time windows (morning/afternoon/evening/night) with % per endpoint, then divide by duration.

**Example:** morning (06:30–09:00, 9,000 seconds) handling 11,640 requests → `11,640 ÷ 9,000 = 1.29 TPS`.

**Peak TPS = assumed burst factor 3–5× from the busiest average window** (basis: users start simultaneously). Mark as ASSUMPTION.

### 4. Sizing per Component

| Component | Reference |
|-----------|-----------|
| API Backend | Peak TPS vs instance capacity (estimate); 2 instances minimum for HA, not because of load |
| Worker | Queue length, not TPS |
| PostgreSQL | Text/number data volume only (photos NOT in DB); connections → PgBouncer |
| Redis | Queue (BullMQ) + cache + session; HA required |
| Object Storage | Photo volume × average size; hot/cold tier + lifecycle |
| Bandwidth | Peak upload volume ÷ duration (MB/s) |

**Common for 400–800 agent systems: peak TPS 3–10 << 1 Node instance capacity (50–100+ TPS). Real load is on photos/storage + queue, not API CPU.**

### 5. Estimate Cost

- Create a table per cloud (AWS/GCP/Azure) per component/month → subtotal → yearly → IDR (exchange rate assumption, e.g., Rp 18,000/USD) → + staging 20–30%.
- Use the smallest instance tier that is sufficient (e.g., 2 vCPU/4 GB, not 8 GB).
- Firebase (FCM/Auth/Crashlytics) = $0 on Spark plan — include as a free component.

## Cross-Document Consistency Checklist

When any number changes, check and update simultaneously in:
- [ ] PRD (summary: visits/day, photos/day, TPS, cost, upload mechanism)
- [ ] Capacity planning doc (breakdown, TPS, sizing, cost)
- [ ] Pricing/firebase doc (if relevant)

Do not wait for the user to ask — cross-check automatically after editing.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Calculate TPS from vague "60–80%" | Not traceable | Derive from total requests ÷ duration |
| Double-count 2,800 visits × 7 again | Double-count | `per visit` already includes the visit |
| Include photo upload in API request count | Over-estimate | Pre-signed upload directly to S3 = not an API request |
| Include photos in DB estimate | DB over-sized | Photos in Object Storage, DB only text/numbers |
| Claim measured number when it is an assumption | Misleading | Mark "estimate/ASSUMPTION + load test validation" |
| Different numbers between PRD and capacity doc | Inconsistency | Update both in a single edit block |
| Back-calculate a number and present it as a source | Deceptive | Always state the direction of calculation (forward from volume) |

## Additional Knowledge from Practical Sessions

### Schedule XML (MS Project / ProjectLibre)
- **XML** (`*.xml`): source of truth for schedule data, assignments, and resources — can be parsed directly
- **POD** (`*.pod`): ProjectLibre binary (Java serialization), **cannot be parsed** with XML parser — use XML instead
- **Generator**: `build_schedule.py` generates `Field_Sales_Canvassing.xml` compatible with MS Project & ProjectLibre

### Backend Task Structure (decomposed by category)
```
2. Backend Core
├── 2.A Shared API (Auth, RBAC, Master Data, SAP Sync)
├── 2.B API for Mobile (Visit Plan, Check-in/out, Merchant, Order, Survey, Sync, FCM)
├── 2.C API for Portal (Dashboard, User Mgmt, Reports, SAP Monitor)
└── 2.D API for Worker (SAP Sync, Queue, Photo, FCM, Carry-forward)
```

### Person-Day Calculation
- **Technical PD**: from schedule XML assignments (total hours ÷ 8)
- **PM PD**: calendar project duration × 20% (not from schedule assignment)
- **Total PD** = technical PD + PM PD

### Standard Rates (Project-Specific)
> **IMPORTANT**: Rate per hour/day varies per project/program. Do not hardcode rates — **ask the user** before calculating costs.

### Cost Formula
```
Cost = Σ (PD per role × Rate per role)
PM Cost = (Calendar days × 20%) × PM Rate
```

### Task Naming Convention
Tasks in the schedule **do not need numbering** (e.g., 1, 1.1, 1.A.1, 2.A.1, etc.). Use **descriptive names only** to make it easier to:
- Edit tasks (change name, duration, dependencies)
- Delete tasks
- Add new tasks

**Reason:**
- Numbers change automatically when tasks are added/removed in the middle
- Without numbers, the schedule is more flexible for manual editing
- Descriptive names are sufficient for task identification
