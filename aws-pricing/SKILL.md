---
name: aws-pricing
description: Use when querying AWS pricing, estimating cloud costs, or sizing infrastructure. Covers AWS Price List API methodology, Fargate/EC2/Lambda pricing approach, and cross-document consistency checks.
---

# AWS Pricing

## Overview

Methodology for querying official AWS pricing per service, region, and configuration. **No prices are hardcoded in this skill** — all figures must be queried from the AWS Price List API to stay current.

## Price Source of Truth

### AWS Price List API
- **Main URL**: https://aws.amazon.com/billing/aws-price-list/
- **Query API**: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-price-list-query-api.html
- **Bulk download**: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api.html
- **Region**: `ap-southeast-3` (Jakarta) — available for most services

### AWS Products Relevant for Infrastructure Capacity Planning

| Service | API/Page Reference | Notes |
|---------|-------------------|-------|
| ECS Fargate | AWS Price List API → `AmazonECS` | Per vCPU-hour, per GB-hour |
| EC2 (On-Demand) | AWS Price List API → `AmazonEC2` | Per instance type, per hour |
| RDS PostgreSQL | AWS Price List API → `AmazonRDS` | Per instance, per storage GB |
| S3 Standard | AWS Price List API → `AmazonS3` | Per GB/month |
| S3-IA | AWS Price List API → `AmazonS3` | Per GB/month (lower storage class) |
| NAT Gateway | AWS Price List API → `AWSNATGateway` | Per hour + per GB processed |
| CloudWatch | AWS Price List API → `AmazonCloudWatch` | Per metric, per log ingest |
| Secrets Manager | AWS Price List API → `AWSSecretsManager` | Per secret per month |
| CloudTrail | AWS Price List API → `AWSCloudTrail` | Per trail, per event |
| ECR | AWS Price List API → `AmazonEC2ContainerRegistry` | Per GB storage, per PUT request |
| Lambda | AWS Price List API → `AWSLambda` | Per request, per GB-second |

## Query Methodology

### 1. Bulk Download (for all prices at once)

```bash
# Download price list JSON for all services
# URL format: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{ServiceCode}/current/index.json
# Example:
curl https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECS/current/index.json
```

### 2. Price List Query API (for specific products)

```python
import boto3

client = boto3.client('pricing', region_name='us-east-1')

response = client.get_products(
    ServiceCode='AmazonECS',
    Filters=[
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'Asia Pacific (Jakarta)'},
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': 'Fargate'},
    ],
    MaxResults=10
)
```

### 3. Manual via AWS Pricing Calculator
- **URL**: https://calculator.aws/
- Select region → select service → enter configuration → get cost estimate

## How to Calculate Costs (Methodology)

### Step 1: Identify Components
List all components in use:
- Compute (Fargate task, EC2 instance, Lambda)
- Storage (S3, EBS, RDS)
- Networking (NAT Gateway, Data Transfer)
- Monitoring (CloudWatch metrics, logs)
- Other (Secrets Manager, CloudTrail, ECR)

### Step 2: Query Official Prices
For each component, query the AWS Price List API with filters:
- `location` = region (e.g., `Asia Pacific (Jakarta)`)
- `instanceType` / `productFamily` = service type
- `termType` = OnDemand or Reserved

### Step 3: Calculate Per Component
```
Cost per component = (unit usage per hour/month) × (price per unit)
```

Example Fargate:
```
Monthly cost = (vCPU per task × hours per month) × price per vCPU-hour
             + (memory per task × hours per month) × price per GB-hour
```

### Step 4: Total + Staging
```
Total = Production + Staging (on-demand, typically 20-30% of prod)
```

### Step 5: Convert to IDR
```
Total IDR = Total USD × exchange rate (e.g., Rp 18,000/USD)
```

## Cross-Document Consistency

When any infrastructure figure changes, check and update simultaneously:
- [ ] PRD (summary: infra cost, upload mechanism)
- [ ] INFRASTRUCTURE_CAPACITY_PLANNING.md (sizing & detailed cost)
- [ ] AWS Price List API (verify latest prices)

Do not wait for the user to ask — cross-check automatically after editing.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Hardcode prices in skill/doc | Figures become stale when prices change | Always query official API |
| Use wrong region pricing | Under/over estimate | Ensure `location` filter matches the correct region |
| Forget NAT Gateway | Network cost missed | NAT = $35/month per AZ |
| Forget CloudWatch metrics | Monitoring cost missed | $0.30/metric/month |
| Forget ECR | Registry cost missed | ~$1-2/month |
| Use EC2 pricing for Fargate | Over estimate | Fargate pricing differs from EC2 |
| Forget currency conversion | USD figures ≠ IDR | Always convert with a clear exchange rate |

## Important Notes

- **AWS prices can change** — always query the latest API, do not rely on hardcoded figures
- **Jakarta region (ap-southeast-3)** — not all services are available in this region, check availability first
- **Fargate pricing** = per vCPU-hour + per GB-hour (not per instance)
- **S3 pricing** = per GB storage + per request (PUT/GET) + per data transfer
- **Staging on-demand** = turn on only when needed, turn off after → lower cost
