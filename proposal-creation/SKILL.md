---
name: proposal-creation
description: Use when creating IT procurement proposals from procurement documents (RKS, RFI, RFP, tender specifications). Covers document analysis, scope, pricing, schedule, and Notion publication.
---

# Proposal Creation for IT Procurement

## Overview

Create comprehensive IT procurement proposals from various procurement documents — RKS, RFI, RFP, tender specifications, and pengadaan documents. Covers document analysis, requirements mapping, scope definition, resource-based pricing, MS Project schedule generation, and Notion publication.

## Workflow

### 1. Extract Procurement Document Content

```python
# Read PDF using PyMuPDF
import fitz
doc = fitz.open("dokumen-pengadaan.pdf")
text = ""
for page in doc:
    text += page.get_text()
```

Save extracted text for reference. Keep original formatting where possible.

### 2. Parse Checklist Requirements

Use openpyxl to read Excel checklists:

```python
import openpyxl
wb = openpyxl.load_workbook("checklist.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

Map each checklist item to a compliance status (Comply / Partial / Excluded). Include a Requirements Compliance Matrix (table) in the proposal referencing the source document.

### 3. Proposal Structure

```
1.  Ringkasan Eksekutif (tabular format)
2.  Profil Perusahaan
3.  Scope of Work (mapping to procurement requirements)
4.  Out of Scope
5.  Penjelasan Kebutuhan Proyek
6.  Pendekatan dan Metodologi
7.  Fitur Aplikasi
8.  Requirements Compliance Matrix
9.  Timeline Proyek
10. Kebutuhan Resources / Man Power
11. Teknologi dan Infrastruktur
12. Rincian Biaya (resource + transport + maintenance)
13. Penawaran Harga (DPP + PPN + Total)
14. Penawaran Maintenance & SLA
15. Jaminan & Garansi
16. Kepatuhan Regulasi & Keamanan
17. Join Development & Knowledge Transfer
18. Penutup
```

### 4. Ringkasan Eksekutif Format

Always use tabular format (key-value table):

| Item | Detail |
|------|--------|
| Nama Proyek | [nama] |
| Nilai HPS | [HPS] |
| Nilai Penawaran | [total harga termasuk PPN] |
| Efisiensi | [persentase] di bawah HPS |
| DPP | [nilai] |
| PPN 12% | [nilai] |
| Durasi Proyek | [durasi] |
| Masa Pemeliharaan | [durasi] |
| Metodologi | [metodologi] |
| Tim Inti | [jumlah] resource roles, [total] man-days |
| Platform | [platform stack] |
| Fitur | [jumlah] item checklist Comply |

### 5. Pricing Strategy

**Cost components (4 lines):**
| Komponen | Metode |
|----------|--------|
| A. Resource Cost | Sum of (man-days × rate per resource) from schedule |
| B. Transportasi & Akomodasi | Trip-based calculation (tiket PP + hotel + per diem + transport lokal) |
| C. Maintenance | Monthly rate × months post-go-live |
| D. AI Token / License Budget | Lump sum if needed |

**Rate guidelines (IT consulting):**
- Project Manager: Rp5.000.000/man-day (20% alokasi × project duration)
- Functional/Tech Lead: Rp4.500.000/man-day
- Technical/Developer/QA/DevOps: Rp4.000.000/man-day
- Technical Writer: Rp3.500.000/man-day

**Transport unit cost:**
- Tiket PP: Rp2.500.000/trip
- Hotel: Rp700.000/malam
- Per diem: Rp450.000/hari
- Transport lokal: Rp350.000/hari

**Payment terms:** 40/40/10/10 (after SIT, after UAT, after Go-Live, after Maintenance)

**Tax:** PPN 12% using DPP Nilai Lain (11/12) → PPN = DPP × 11%.

### 6. MS Project XML Schedule

Generate schedule using `project-schedule` skill. Critical rules:

**XML structure requirements:**
- `<Calendars>` wrapper (plural, not `<Calendar>`)
- `<SaveVersion>14</SaveVersion>` (MS Project 2010 compatible)
- Task elements: `<Summary>` (not `<IsSummary>`), `<Active>` (not `<IsActive>`), `<Manual>0</Manual>`
- Duration format: `PT8H0M0S` (not `P1D`)
- DurationFormat per task type: 7=days, 21=elapsed_days
- Assignments: separate `<Assignments>` section (not inline), `<Units>1</Units>` (not 100)
- Work=Duration for leaf tasks; summary tasks sum children
- Project settings: `<DefaultTaskType>0</DefaultTaskType>`, `<ScheduleFromStart>1</ScheduleFromStart>`

**Working days:** Skip weekends (Sat/Sun). Use `_add_working_days()` helper.

**Resource utilization:** Calculate from actual schedule assignments, not estimated headcount.

### 7. Graphify — Knowledge Graph (Optional)

If a Graphify knowledge graph exists for the project (`graphify_status` confirms), use it to:
- **Query** project structure, dependencies, and context before writing (`graphify_query`)
- **Explain** specific files, functions, or concepts (`graphify_explain`)
- **Check blast radius** of changes (`graphify_affected`)
- **Build/update** the graph after significant changes (`graphify_build --update`)

This helps ground the proposal in actual project architecture rather than assumptions.

### 8. Notion Publication

Use dual-path approach:
1. **Primary:** Notion MCP tool (`notion_create_pages`, `notion-update-page`)
2. **Fallback:** Python REST API with `NOTION_TOKEN` if OAuth callback fails

**Key Notion formatting rules:**
- Use `<table>`, `<tr>`, `<td>` for tables
- Use plain text in table cells (no `<strong>` or `**` — they render as literal text in Notion)
- For large content, split into batch uploads
- Use `update_content` (replace_by_match) for targeted edits
- For complete section replacements, use `replace_content` for the whole page

### 9. Resource-Costing Integration

1. Build schedule → generate XML → open in MS Project
2. Export with resources → get `resource.xml` with actual hours per resource
3. Calculate man-days (hours ÷ 8) per resource
4. Apply rates to get Resource Cost
5. Add Transport (trip-based), Maintenance, AI Token
6. Compute DPP → PPN → Total

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `<strong>` in table cells | Use plain text only |
| `<Calendar>` instead of `<Calendars>` | Always use plural wrapper |
| PPN = DPP × 12% | Use PPN = DPP × 11% (Nilai Lain 11/12) |
| PM allocated full-time | PM = 20% × project duration |
| Work=P1D in XML | Use PT8H0M0S format |
| Assignments inline in task | Use separate `<Assignments>` section |
| Units=100 in assignments | Use Units=1 |
