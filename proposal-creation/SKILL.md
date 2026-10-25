---
name: proposal-creation
description: Use when drafting, reviewing, or refining IT procurement proposals from RKS, RFI, RFP, tender specifications, or pengadaan documents, including project context, benefits, scope of work, out-of-scope, pricing, schedules, or compliance.
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

Save extracted text for reference. Keep original formatting where possible. Record source filenames and page/sheet/row references for proposal claims. Follow the language required by the RFQ; if it is unspecified, ask the user which language the client-facing proposal should use instead of inferring it from the conversation.

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

```text
1.  Ringkasan Eksekutif
2.  Profil Perusahaan
3.  Kondisi Saat Ini
4.  Manfaat yang Didapatkan
5.  Ruang Lingkup Pekerjaan (Scope of Work)
6.  Di Luar Ruang Lingkup (Out of Scope)
7.  Pemahaman Kebutuhan Proyek
8.  Pendekatan dan Metodologi
9.  Fitur Aplikasi
10. Requirements Compliance Matrix
11. Timeline Proyek
12. Kebutuhan Resources / Man Power
13. Teknologi dan Infrastruktur
14. Rincian Biaya
15. Penawaran Harga
16. Maintenance & SLA
17. Jaminan dan Garansi
18. Kepatuhan Regulasi dan Keamanan
19. Join Development dan Knowledge Transfer
20. Penutup
```

### Required Content for the Four Project Chapters

#### Kondisi Saat Ini

Describe the as-is environment using evidence from the procurement documents and discovery inputs. Cover relevant business processes, systems and integrations, user groups, channels, indicative workload or transaction volumes, pain points, constraints, and known data gaps. Cite the source filename plus page, worksheet, or requirement ID. If the source does not provide a fact, mark it as **Perlu konfirmasi** or **Asumsi**, not as an established condition.

#### Manfaat yang Didapatkan

Connect each stated problem to a proposed capability and an expected outcome. Use a table such as:

| Kondisi / Pain Point | Capability / Perubahan | Manfaat | KPI, Baseline, Target, dan Cara Ukur |
|---|---|---|---|

Use client-provided baselines and targets when available. Label forecasts and proposed targets as indicative, state their assumptions, and do not claim quantified ROI without supporting data.

#### Ruang Lingkup Pekerjaan (Scope of Work)

Organize the work into these four phases. For every phase, state activities, deliverables, dependencies or client inputs, indicative duration, and objective acceptance criteria. A phase is incomplete if it lists activities without the outputs the client will receive.

| Fase | Aktivitas Utama | Deliverables Utama | Kriteria Penerimaan | Durasi Indikatif |
|---|---|---|---|---|
| Kick-off Meeting | Confirm objectives, stakeholders, governance, RACI, communication and escalation paths, scope boundaries, success measures, schedule, risks, assumptions, access, and required client inputs. | Kick-off minutes/deck; project charter or initiation brief; RACI and communication/escalation matrix; baseline schedule and milestones; RAID log; initial assumptions, dependencies, and access/input register. | Pemilik proyek menyetujui baseline tujuan, tata kelola, jadwal, scope, dan daftar risiko/asumsi; catat keputusan dan isu terbuka. | `[x] hari kerja`, sesuai rencana mobilisasi dan ketersediaan stakeholder. |
| Analisa dan Perancangan | Run discovery and workshops; document as-is and to-be processes; analyze requirements, integrations, data, security, architecture, constraints, and acceptance needs; validate assumptions and indicative sizing. | Requirements catalogue and traceability matrix; as-is/to-be business-process flows; solution architecture and design; integration/data specifications; prototypes where needed; non-functional targets and sizing assumptions; approved design baseline. | Business owner dan IT meninjau serta menyetujui requirement, flow, desain, dan asumsi sizing; catat pengecualian atau keputusan yang masih terbuka. | `[x] minggu`, sesuai jumlah proses, integrasi, dan siklus review. |
| Implementasi dan Pengembangan | Configure or develop the approved features and functions; implement business-process flows, rules, roles, interfaces, and integrations; prepare environments and data activities that fall within scope; trace implementation to approved functional and non-functional requirements. | Configured/developed features; documented business-process flows and rules; integration and deployment artifacts; data-migration outputs only when included; configuration/source artifacts and technical documentation as contracted; requirement traceability and implementation evidence. | Build tersedia di environment yang disepakati; fitur dapat ditelusuri ke desain/requirement yang disetujui; bukti konfigurasi, integrasi, dan artefak serah-terima tercatat. | `[x] minggu`, berdasarkan backlog, kompleksitas, dan dependency yang disepakati. |
| Pengujian dan Quality Assurance | Prepare and execute test cycles; manage defects and retesting; support client UAT and release readiness. Include unit, integration/SIT, regression, performance, security, or other tests only when assigned in the agreed scope. | Test strategy and cases; requirements-to-test traceability; execution evidence and results; defect log and closure status; QA summary; UAT sign-off or documented outstanding issues; release/acceptance checklist. | Kriteria exit mengikuti kontrak dan test plan; hasil dan defect tercatat; defect kritis ditutup atau mendapat waiver tertulis; UAT disetujui atau isu tersisa diterima secara tertulis. | `[x] minggu`, termasuk retest dan waktu review/UAT dari client. |

For **Implementasi dan Pengembangan**, make the proposal specific enough to estimate and accept:

- List each feature/function, its user or actor, behavior, channel, integration, and linked requirement ID.
- Describe the business-process flow, business rules, exception paths, roles, and approval points. Add a diagram or a numbered flow when it improves clarity.
- Map functional requirements to non-functional requirements and acceptance evidence. Cover applicable security, performance, availability, capacity, recovery, usability, and data-retention targets.
- Provide an **indicative sizing and volume table** for relevant dimensions: users/seats, concurrent sessions, transactions or tickets per day/month, peak load, storage and retention, integrations/API throughput, growth, and infrastructure/resources. Cite the source for each input. Mark vendor estimates as **indikatif**, state assumptions and calculation basis, and identify when discovery or performance testing must validate them. Do not present unvalidated estimates as committed capacity.

#### Di Luar Ruang Lingkup (Out of Scope)

List exclusions in a boundary table and cross-check them against the Scope of Work, compliance matrix, schedule, and price:

| Item yang Tidak Termasuk | Batasan / Alasan | Status Sumber: Tertulis atau Usulan Vendor | Dampak / Dependency |
|---|---|---|---|

Quote and cite exclusions that the procurement source states explicitly. Label any additional boundary as **Usulan batasan vendor / perlu persetujuan**; do not present an inferred exclusion as a contractual fact. State ownership or dependencies for adjacent items such as third-party licenses, client-side infrastructure, integrations, data cleansing/migration, custom features, training, travel, and post-go-live support when relevant.

### Ringkasan Eksekutif Format

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

### Pricing Strategy

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

### MS Project XML Schedule

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

### Graphify — Knowledge Graph (Optional)

If a Graphify knowledge graph exists for the project (`graphify_status` confirms), use it to:
- **Query** project structure, dependencies, and context before writing (`graphify_query`)
- **Explain** specific files, functions, or concepts (`graphify_explain`)
- **Check blast radius** of changes (`graphify_affected`)
- **Build/update** the graph after significant changes (`graphify_build --update`)

Use the graph for discovery, then verify scope, deliverable boundaries, durations, acceptance criteria, and schedule dates against the authoritative procurement and proposal documents. Graph edges help navigation; they do not replace source evidence.

### Notion Publication

Use dual-path approach:
1. **Primary:** Notion MCP tool (`notion_create_pages`, `notion-update-page`)
2. **Fallback:** Python REST API with `NOTION_TOKEN` if OAuth callback fails

**Key Notion formatting rules:**
- Use `<table>`, `<tr>`, `<td>` for tables
- Use plain text in table cells (no `<strong>` or `**` — they render as literal text in Notion)
- For large content, split into batch uploads
- Use `update_content` (replace_by_match) for targeted edits
- For complete section replacements, use `replace_content` for the whole page

### Resource-Costing Integration

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
| Scope lists activities but no client outputs | Add phase-based deliverables and measurable acceptance criteria |
| Benefits claim unsupported ROI | Trace benefit to evidence and label targets/forecasts as assumptions |
| Indicative sizing appears guaranteed | State source, assumptions, calculation basis, and validation method |
| Inferred exclusions appear contractual | Cite explicit source exclusions; label proposed boundaries for approval |
