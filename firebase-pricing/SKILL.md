---
name: firebase-pricing
description: Use when querying Firebase/Google Cloud pricing, estimating Firebase costs, or checking Firebase free tier limits. Covers Google Cloud Billing API methodology and Firebase pricing structure without hardcoded prices.
---

# Firebase Pricing

## Overview

Methodology for querying official Firebase/Google Cloud pricing per service and configuration. **No prices are hardcoded in this skill** — all figures must be queried from the Google Cloud Billing API to stay current.

## Price Source of Truth

### Google Cloud Billing API
- **API Reference**: https://cloud.google.com/billing/docs/reference/pricing-api/rest
- **Get Pricing Information**: https://cloud.google.com/billing/docs/how-to/get-pricing-information-api
- **Firebase Pricing Page**: https://firebase.google.com/pricing
- **Firebase Pricing Plans**: https://firebase.google.com/docs/projects/billing/firebase-pricing-plans

### Firebase Pricing Plans

| Plan | Description |
|------|-------------|
| **Spark (No-cost)** | Free, no credit card required. Free quota for all services. |
| **Blaze (Pay as you go)** | Pay per usage. $300 free credit for new projects. Spark free quota still applies. |

## Query Methodology

### 1. Google Cloud Billing Catalog API

```python
# List all available services
GET https://cloudbilling.googleapis.com/v1/services

# List products for a specific service
GET https://cloudbilling.googleapis.com/v1/services/{serviceId}/skus

# Filter by region
# Use filter parameter for specific region
```

### 2. Firebase Console
- Open Firebase Console → Project Settings → Billing
- Check pricing page for each service

### 3. Manual via Google Cloud Pricing Calculator
- **URL**: https://cloud.google.com/products/calculator
- Select Firebase/Google Cloud product → enter configuration → get cost estimate

## Firebase Components Relevant for Infrastructure Capacity Planning

| Component | Price Source | Notes |
|-----------|-------------|-------|
| **FCM (Cloud Messaging)** | Firebase Pricing Page | Free unlimited on all plans |
| **Auth (Email/Password)** | Firebase Pricing Page | 50K MAU free on Spark |
| **Auth (Phone/SMS)** | Google Cloud Identity Platform | $0.01 per SMS |
| **Crashlytics** | Firebase Pricing Page | Free unlimited on all plans |
| **Firestore** | Google Cloud Firestore Pricing | Per GB stored, per read/write/delete |
| **Cloud Functions** | Google Cloud Functions Pricing | Per invocation, per GB-second |
| **Cloud Storage** | Google Cloud Storage Pricing | Per GB stored, per operation |
| **Hosting** | Firebase Hosting Pricing | Per GB stored, per data transfer |
| **Realtime Database** | Firebase Realtime Database Pricing | Per GB stored, per connection |

## How to Calculate Costs (Methodology)

### Step 1: Identify Components
List all Firebase components in use:
- FCM (push notification)
- Auth (Email/Password, Phone, etc.)
- Crashlytics (error monitoring)
- Firestore (database)
- Cloud Functions (backend logic)
- Storage (file storage)
- Hosting (web hosting)

### Step 2: Query Official Prices
For each component, query the Google Cloud Billing API or reference Firebase Pricing Page:
- Filter by region/project
- Check Spark free tier vs Blaze pricing

### Step 3: Calculate Per Component
```
Cost per component = (usage per month) × (price per unit)
```

Example Firestore:
```
Monthly cost = (reads per month × price per read)
             + (writes per month × price per write)
             + (stored GB × price per GB)
```

### Step 4: Total + Free Tier Deduction
```
Total = Σ (component cost) - free tier quota
```

### Step 5: Convert to IDR (if needed)
```
Total IDR = Total USD × exchange rate (e.g., Rp 18,000/USD)
```

## Analysis for Field Sales Canvassing (400 Agents)

### Scenario: FCM + Auth + Crashlytics

| Component | Requirement | Spark Quota | Status |
|-----------|-------------|-------------|--------|
| FCM messages | 400 agents × 2 push/day = 800/day | Unlimited | ✅ **FREE** |
| Auth (Email/Password) | 400 MAU | 50,000 MAU | ✅ **FREE** |
| Crashlytics | Unlimited | Unlimited | ✅ **FREE** |
| **Firebase Cost** | - | - | **$0** |

### Scenario: FCM + Phone Auth

| Component | Requirement | Spark Quota | Status |
|-----------|-------------|-------------|--------|
| FCM messages | 800/day | Unlimited | ✅ **FREE** |
| MAU (Phone Auth) | 400 MAU | 50,000 MAU | ✅ **FREE** |
| SMS verification | 400 × 12 months = 4,800/year | ❌ **NOT FREE** | ⚠️ **$48/year** ($0.01 × 4,800) |

## Cross-Document Consistency

When any Firebase figure changes, check and update simultaneously:
- [ ] PRD (summary: infra cost, upload mechanism)
- [ ] INFRASTRUCTURE_CAPACITY_PLANNING.md (sizing & detailed cost)
- [ ] Google Cloud Billing API (verify latest prices)

Do not wait for the user to ask — cross-check automatically after editing.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Hardcode prices in skill/doc | Figures become stale when prices change | Always query official API |
| Forget to check Spark vs Blaze | Over estimate cost | Spark = free, Blaze = pay as you go |
| Forget Phone Auth cost | Phone auth cost missed | Phone Auth = $0.01 per SMS |
| Forget Firestore limits | Over or under estimate | Check daily read/write quota |
| Forget currency conversion | USD figures ≠ IDR | Always convert with a clear exchange rate |

## Important Notes

- **Firebase/Google Cloud prices can change** — always query the latest API, do not rely on hardcoded figures
- **Spark plan** = free, no credit card, limited quota
- **Blaze plan** = pay per usage, $300 free credit for new projects
- **FCM 100% free** on all plans — no message limit
- **Email/Password Auth** = free 50K MAU on Spark
- **Phone Auth** = paid per SMS ($0.01)
- **Crashlytics** = free unlimited on all plans
- **Cloud Functions** not available on Spark plan — requires Blaze
