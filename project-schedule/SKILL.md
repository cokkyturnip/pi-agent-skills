---
name: project-schedule
description: Generate, update, and maintain MS Project XML schedules compatible with Microsoft Project and ProjectLibre. Use when the user wants to create a project timeline, add tasks, set dependencies, add holidays, or export schedule in MS Project XML format.
---

# Skill: Project Schedule

This skill generates and maintains MS Project XML schedules that are compatible with both Microsoft Project and ProjectLibre.

---

## Scope

Output is limited to **MS Project XML (.xml)** — a text-based XML format that is human-editable, compatible with ProjectLibre (File → Open), and MS Project.

---

## Python Generator (Recommended)

A Python script (`generate_schedule.py`) is provided at the skill's `scripts/` directory.

```python
from generate_schedule import ProjectSchedule
from datetime import date

sched = ProjectSchedule("My Project", start_date=date(2026, 9, 1),
                        root_task_name="My Project")  # opsional: task root level 1 = nama project (tampil di MS Project & ProjectLibre)

# Resources
sched.add_resource("Developer")
sched.add_resource("QA")

# Holidays (auto-skipped in date calculation)
sched.add_holiday("Hari Natal", "2026-12-25")

# Tasks with hierarchy
P1 = "Phase 1"
sched.add_task(P1, "P5D")   # summary (dates from children)

sched.add_task("Task A", "P2D", parent=P1)                                     # no resource
sched.add_task("Task B", "P3D", predecessor="Task A", resource="Developer", parent=P1)  # with resource

# Milestone
sched.add_task("Sign-off", predecessor="Task B")

# Long duration using months
sched.add_task("Maintenance", "P6M")

sched.save("schedule.xml")
```

**Duration formats:**
| Format | Meaning | Example |
|--------|---------|---------|
| `P{n}D` | n working days | `P5D` = 5 hari kerja |
| `PT{n}H` | n hours | `PT40H` = 40 jam (5 hari) |
| `P{n}M` | n months (22 hari/bulan) | `P6M` = 6 bulan |
| `P0D` | Milestone (0 hari) | `P0D` |

**Parameters for `add_task()`:**
| Param | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Task name (unique) |
| `duration` | ❌ | ISO 8601 duration (default `P1D`) |
| `predecessor` | ❌ | Task name that must finish before this starts |
| `resource` | ❌ | Resource name to assign |
| `parent` | ❌ | Parent task name (for hierarchy) |
| `start`/`finish` | ❌ | Fixed dates (ISO 8601 string) |

---

## Timeline Output — ASCII Preferred

Untuk menampilkan jadwal di dokumen (PRD, proposal, laporan), gunakan diagram **ASCII** — **bukan Mermaid** (preferensi user: lebih sederhana & mudah dimengerti). Pola yang dipakai:

```
Minggu        1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
Fase 1        ██████████
Fase 2           ██████████████████████████
Fase 3           ██████████████████████████████████████
Fase 4           ████████████████████████████████████
Fase 5                                       ██████████████████████
Fase 6                                                         ██████████
GO-LIVE                                                             ▲
```

Aturan:
- Panjang `█` proporsional dengan durasi kalender fase; `▲` = milestone (GO-LIVE, Design Freeze).
- Selalu sertakan **tabel milestone** (nama + tanggal) di bawah diagram.
- Tanggal diambil dari nilai Start/Finish nyata di XML hasil generate (bukan perkiraan).

---

## Resource & Capacity Planning

Analisis effort per resource/peran & kapasitas dari file XML hasil generate. Contoh nyata (Field Sales Canvassing): **39 assignment, 960 jam = 120 PD**, 6 peran:

| Peran | Jam | PD | Utilisasi¹ | Catatan |
|-------|-----|----|-----------|---------|
| Web Developer (Next.js) | 280 | 35.0 | 100% | Padat — menjadi critical path Web |
| Mobile Developer (Android) | 256 | 32.0 | 86% | |
| Backend Developer (Node.js/Express) | 208 | 26.0 | 43% | Longgar — punya headroom |
| QA Engineer | 128 | 16.0 | 100% | Padat (jendela QA sempit) |
| Business Analyst | 64 | 8.0 | 11% | Tersebar 3 bulan — bisa dirangkum |
| UI/UX Designer | 24 | 3.0 | 100% | |

¹ Utilisasi = work (jam) ÷ kapasitas hari kerja × 8 jam antara assignment start & finish.

Gunakan **`scripts/analyze_capacity.py`** (stdlib saja, tanpa dependency):

```bash
python scripts/analyze_capacity.py schedule.xml
```

Output: work per resource (jam + PD) + jumlah task + rentang tanggal + utilisasi, effort per fase (summary), dan deteksi overlap (resource di-assign ke 2+ task paralel).

**Tips capacity planning:**
- 1 PD = 8 jam; `Units=1` (= 100% alokasi).
- **Headcount:** total PD ÷ durasi kalender (hari kerja) → mis. 120 PD ÷ 72 hari ≈ 1,7 orang rata-rata; tim 2–3 orang cukup (lihat PRD §10.1).
- **Utilisasi tinggi (>90%) = bottleneck** → pertimbangkan tambah resource atau longgarkan predecessor (geser task yang tidak tergantung).
- **Utilisasi rendah (<30%)** → rangkum rentang (mulai belakangan / selesai lebih cepat) atau serap tugas dari resource padat.
- **Resource tanpa assignment** (PM, oversight) tidak muncul di XML — tambahkan alokasi manajemen terpisah ±10–15% di laporan.
- **Untuk proposal/biaya:** effort per peran (dari XML) × rate/hari → biaya per peran (lihat PRD §10.3).

---

## Critical MS Project XML Rules

### ❗ GUID + ID on Tasks and Resources (MUST)

MS Project **refuses to open** the file entirely ("Project cannot open the file") if Task/Resource elements lack `<GUID>` and `<ID>`. Always emit both, right after `<UID>`:

```xml
<Task>
  <UID>9</UID>
  <GUID>7BB39ADF-818F-F111-8579-940853B340AC</GUID>
  <ID>3</ID>
  <Name>1.1 Kickoff</Name>
  ...
```

- `<ID>` = sequential position (1..N), separate from UID
- `<GUID>` = uppercase UUID, unique per element
- Applies to Tasks **and** Resources (and Assignments benefit from GUID + `CreationDate`)

### ❗ Complete Assignment Fields (avoid "Name[0%]" in ProjectLibre)

A minimal `<Assignment>` with only `UID/TaskUID/ResourceUID/Units` makes ProjectLibre render the resource column as **`Name[0%]`** because assignment Work is read as null. Emit the full standard set — at minimum `Work`, `RegularWork`, `RemainingWork`, `Start`, `Finish`, `PercentWorkComplete` — matching the fixing file's structure. The generator does this automatically.

### ❗ PredecessorLink Fields

Include `CrossProject=0`, `LinkLag=0`, `LagFormat=7` alongside `PredecessorUID` and `Type`, or MS Project's importer may reject the file.

### ❗ Element Names (MUST be exact)

MS Project ignores wrong element names silently. This causes 0-duration or broken schedules.

| Correct | Wrong (ignored) |
|---------|-----------------|
| `<Summary>1</Summary>` | ❌ `<IsSummary>1</IsSummary>` |
| `<Active>1</Active>` | ❌ `<IsActive>1</IsActive>` |

Additional required elements per task:
- `<Manual>0</Manual>` (auto-scheduled)
- `<Estimated>0</Estimated>`
- `<ConstraintType>0</ConstraintType>` (ASAP)

### ❗ Task-Level Work MUST match Duration

For leaf tasks with resources: `Work` = `Duration` (same hours).  
For leaf tasks without resources: `Work` = `PT0H0M0S`.  
For summary tasks: `Work` = sum of all children's Work.

If Work is wrong (e.g., PT0H0M0S for all tasks), MS Project shows **"Start No Later Than"** constraint instead of "As Soon As Possible".

### ❗ SaveVersion Must Match MS Project Version

| MS Project Version | SaveVersion |
|-------------------|-------------|
| 2010 | `14` |
| 2013 | `15` |
| 2016+ | `16` |

Using the wrong version can cause constraint interpretation issues.

### ❗ Calendars Wrapper

Use `<Calendars>` (plural) wrapping `<Calendar>`, not bare `<Calendar>`:

```xml
<Calendars>
  <Calendar>
    <UID>1</UID>
    <Name>Standard</Name>
    <IsBaseCalendar>1</IsBaseCalendar>
    <IsBaselineCalendar>0</IsBaselineCalendar>
    <BaseCalendarUID>-1</BaseCalendarUID>
    ...
  </Calendar>
</Calendars>
```

### ❗ Separate Assignments Section

**Assignments MUST be in a separate `<Assignments>` section**, NOT inline inside `<Task>`.  
Inline assignments are NOT read by MS Project.

```xml
<Assignments>
  <Assignment>
    <UID>1</UID>
    <GUID>...</GUID>
    <TaskUID>12</TaskUID>
    <ResourceUID>2</ResourceUID>
    <PercentWorkComplete>0</PercentWorkComplete>
    <RegularWork>PT8H0M0S</RegularWork>
    <RemainingWork>PT8H0M0S</RemainingWork>
    <Start>...</Start>
    <Finish>...</Finish>
    <Units>1</Units>   <!-- 1 = 100% -->
    <Work>PT8H0M0S</Work>
    ...
  </Assignment>
</Assignments>
```

**(Diatas hanya ilustrasi penempatan — generator otomatis mengisi field lengkap; jangan tulis manual tanpa Work/Start/Finish.)**

**`<Units>`** format: `1` (not 100). In MS Project XML, `1` = 100% allocation. Verified behavior: `1` works correctly in **both** MS Project and ProjectLibre; `100` breaks ProjectLibre (renders 10000%). MS Project normalizes either value, so never write `100`.

### ❗ Project-Level Settings

Include these to match MS Project export:

```xml
<DefaultTaskType>0</DefaultTaskType>
<NewTasksAreManual>1</NewTasksAreManual>
<NewTasksEstimated>1</NewTasksEstimated>
<ScheduleFromStart>1</ScheduleFromStart>
<NewTaskStartDate>0</NewTaskStartDate>
<HonorConstraints>0</HonorConstraints>
```

### ❗ Root Task (opsional, via `root_task_name`) — Level 1, UID ≠ 0

Task root berisi nama project dan menjadi induk seluruh hierarki. Generator menghitung otomatis: Start/Finish = min/max seluruh task, Duration = jam kerja antara keduanya, Work = total effort fase.

```python
ProjectSchedule("Judul", start_date=..., root_task_name="Nama Project")
```

Aturan penting (terbukti lewat uji COM MS Project):
- Root ditaruh di **OutlineLevel 1** — MS Project **membuang task OutlineLevel 0** (file fixing pun: "Field_Sales_Canvassing" level 0 tidak tampil di MS Project).
- Root **UID ≠ 0** (pakai 64, seperti wrapper di file fixing) — MS Project menolak task ber-UID 0. `ID` boleh 1.
- Semua task lain bergeser +1 level (fase = 2, task = 3) dan `ID` bergeser +1.

---

## Common Pitfalls & Solutions

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| MS Project refuses to open file ("cannot open the file") | Missing `<GUID>`/`<ID>` on Tasks/Resources | Add GUID + ID after UID on every Task and Resource |
| Resource column shows `Name[0%]` | Assignment has no `Work` field (read as null) | Emit full assignment fields (Work, RegularWork, RemainingWork, Start, Finish) |
| Duration = 0 | Missing `<Work>` or wrong element names | Add `Work=Duration`, use `<Summary>` not `<IsSummary>` |
| Constraint = "Start No Later Than" | Wrong `Work` values (all PT0H0M0S) | Set `Work=Duration` for leaf tasks, sum for summaries |
| "edays" display | Wrong `DurationFormat` | Use 7=days, 21=elapsed, 11=months |
| Resource not assigned | Inline `<Assignment>` inside `<Task>` | Move to separate `<Assignments>` section |
| `Units=100` breaks ProjectLibre (10000%) | Wrong Units format | Use `1` (verified: `1` = 100% in MS Project XML; works in both tools) |

---

## Working Day Calculation

The generator skips weekends (Sat/Sun) and holidays when calculating finish dates. For example:
- `P5D` starting Mon → Fri (5 weekdays)
- `P6M` starting Sep 1 → ~Mar 9 (6 months, accounting for weekends)

---

## Encoding

All XML must be UTF-8. Special characters:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
