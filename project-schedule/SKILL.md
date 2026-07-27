---
name: project-schedule
description: Generate, update, and maintain MS Project XML schedules compatible with ProjectLibre. Use when the user wants to create a project timeline, add tasks, set dependencies, add holidays, or export schedule in MS Project XML format.
---

# Project Schedule Skill

## Kapan Menggunakan Skill Ini

- User ingin membuat **project schedule** baru dalam format **MS Project XML (.xml)**
- User ingin **menambahkan/mengupdate task, milestone, dependency, durasi**
- User ingin **menambahkan hari libur nasional/cuti bersama** ke kalender
- User ingin **menambahkan kolom/hari kerja** (misal sabtu jadi kerja)
- User ingin mengubah **base calendar, working hours, atau hari non-kerja**

## Format Output

Hanya **MS Project XML (.xml)** — format teks berbasis XML, bisa diedit manual, kompatibel dengan ProjectLibre (File → Open) dan MS Project.

> ⚠️ ProjectLibre juga punya format native `.pod` (binary Java serialization), tapi **tidak bisa dibaca/diedit oleh AI**. Hanya bisa dibuka via ProjectLibre langsung.

## Template XML Lengkap (Validator)

Gunakan template ini sebagai dasar (tidak perlu rewrite dari awal — cukup pakai `edit` untuk perubahan):

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Project xmlns="http://schemas.microsoft.com/project">
    <SaveVersion>14</SaveVersion>
    <Name>{NAMA_PROJECT}</Name>
    <Title>{NAMA_PROJECT}</Title>
    <ScheduleFromStart>1</ScheduleFromStart>
    <StartDate>{START_DATE}T08:00:00</StartDate>
    <FinishDate>{FINISH_DATE}T17:00:00</FinishDate>
    <MinutesPerDay>480</MinutesPerDay>
    <MinutesPerWeek>2400</MinutesPerWeek>
    <DaysPerMonth>20</DaysPerMonth>
    <DefaultTaskType>0</DefaultTaskType>
    <DurationFormat>7</DurationFormat>
    <CalendarUID>1</CalendarUID>
    <DefaultStartTime>15:00:00</DefaultStartTime>
    <DefaultFinishTime>00:00:00</DefaultFinishTime>
    <Calendars>
        <Calendar>
            <UID>1</UID>
            <Name>Standard</Name>
            <IsBaseCalendar>1</IsBaseCalendar>
            <WeekDays>
                <WeekDay><DayType>1</DayType><DayWorking>0</DayWorking></WeekDay>
                <WeekDay><DayType>2</DayType><DayWorking>1</DayWorking><WorkingTimes>
                    <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>
                    <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>
                </WorkingTimes></WeekDay>
                <WeekDay><DayType>3</DayType><DayWorking>1</DayWorking><WorkingTimes>
                    <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>
                    <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>
                </WorkingTimes></WeekDay>
                <WeekDay><DayType>4</DayType><DayWorking>1</DayWorking><WorkingTimes>
                    <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>
                    <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>
                </WorkingTimes></WeekDay>
                <WeekDay><DayType>5</DayType><DayWorking>1</DayWorking><WorkingTimes>
                    <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>
                    <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>
                </WorkingTimes></WeekDay>
                <WeekDay><DayType>6</DayType><DayWorking>1</DayWorking><WorkingTimes>
                    <WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime>
                    <WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime>
                </WorkingTimes></WeekDay>
                <WeekDay><DayType>7</DayType><DayWorking>0</DayWorking></WeekDay>
            </WeekDays>
            <Exceptions>
                <!-- HARI LIBUR NASIONAL & CUTI BERSAMA:
                <Exception>
                    <EnteredByOccurrences>0</EnteredByOccurrences>
                    <TimePeriod>
                        <FromDate>2026-01-01T00:00:00</FromDate>
                        <ToDate>2026-01-01T23:59:00</ToDate>
                    </TimePeriod>
                    <Occurrences>1</Occurrences>
                    <Type>1</Type>
                    <DayWorking>0</DayWorking>
                </Exception>
                -->
            </Exceptions>
        </Calendar>
    </Calendars>
    <Tasks>
        <!-- Task template -->
    </Tasks>
</Project>
```

## Aturan Format XML (ProjectLibre-Compatible)

### Header
- **Namespace** harus `xmlns="http://schemas.microsoft.com/project"` — **tanpa** `/2003` di path
- `CalendarUID` di header harus cocok dengan UID base calendar (biasanya `1`)
- `MinutesPerDay` = 480 (8 jam), `DaysPerMonth` = 20
- `DefaultStartTime` dan `DefaultFinishTime`: nilai default ProjectLibre adalah `15:00:00` dan `00:00:00` — **jangan diubah** ke `08:00:00`/`17:00:00` karena itu adalah internal offset MS Project, bukan jam kerja aktual

### Calendar
- Setiap **Calendar** punya `UID, Name, IsBaseCalendar, BaseCalendarUID, WeekDays`
- Base calendar: `IsBaseCalendar=1`, `BaseCalendarUID=-1`
- **DayType**: 1=Minggu, 2=Senin, 3=Selasa, 4=Rabu, 5=Kamis, 6=Jumat, 7=Sabtu
- Jika ProjectLibre **menolak file**, kosongkan `<Calendars/>` dulu — pengguna bisa menambahkan calendar manual dari ProjectLibre UI

#### Format Exception yang BENAR (ProjectLibre native)
Jangan pakai format:
```xml
<Exception><UID>1</UID><Name>Libur</Name><Date>2026-08-17T00:00:00</Date><Type>1</Type><DayWorking>0</DayWorking></Exception>
```

Yang benar — ProjectLibre pakai **TimePeriod** dengan FromDate/ToDate, **bukan** elemen `<Date>`:
```xml
<Exception>
    <EnteredByOccurrences>0</EnteredByOccurrences>
    <TimePeriod>
        <FromDate>2026-08-17T00:00:00</FromDate>
        <ToDate>2026-08-17T23:59:00</ToDate>
    </TimePeriod>
    <Occurrences>1</Occurrences>
    <Type>1</Type>
    <DayWorking>0</DayWorking>
</Exception>
```

⚠️ **PENTING**: Format `<Date>` di Exception adalah format MS Project asli dan TIDAK kompatibel dengan ProjectLibre. ProjectLibre hanya membaca format `TimePeriod` dengan `FromDate`/`ToDate`.

### Task
Setiap Task harus punya:

| Field | Wajib? | Nilai |
|-------|--------|-------|
| `UID` | ✅ | Unique integer |
| `ID` | ✅ | Sama dengan UID |
| `Name` | ✅ | Nama task |
| `Type` | ✅ | `0` (fixed duration — **gunakan 0**, bukan 1) |
| `IsNull` | ✅ | `0` |
| `CreateDate` | ✅ | ISO date |
| `WBS` | ✅ | **Harus kosong** `<WBS></WBS>` — jangan diisi string hierarchy. ProjectLibre otomatis generate WBS sendiri dari OutlineNumber. Kalau diisi nilai, parser gagal. |
| `OutlineNumber` | ✅ | Hierarchy string (`1`, `1.1`, `1.1.1`) |
| `OutlineLevel` | ✅ | 1=root, 2=phase, 3=group, 4=task |
| `Start` | ✅ | `{YYYY-MM-DD}T08:00:00` |
| `Finish` | ✅ | `{YYYY-MM-DD}T17:00:00` |
| `Duration` | ✅ | Format ISO 8601: `PT{N}H0M0S` |
| `DurationFormat` | ✅ | `7` |
| `Resume` | ✅ | Sama dengan Start date |
| `ResumeValid` | ✅ | `0` |
| `EffortDriven` | ✅ | `1` |
| `Recurring` | ✅ | `0` |
| `OverAllocated` | ✅ | `0` |
| `Estimated` | ✅ | `0` |
| `Milestone` | ✅ | `1` untuk milestone, `0` untuk task biasa |
| `Summary` | ✅ | `1` untuk group/summary, `0` untuk task leaf |
| `Critical` | ✅ | `1`/`0` |
| `IsSubproject` | ✅ | `0` |
| `IsSubprojectReadOnly` | ✅ | `0` |
| `ExternalTask` | ✅ | `0` |
| `FixedCostAccrual` | ✅ | `2` |
| `PercentComplete` | ✅ | `0` |
| `PercentWorkComplete` | ✅ | `0` |
| `RemainingDuration` | ✅ | Sama dengan Duration (karena 0% complete) |
| `ConstraintType` | ✅ | `0` (as soon as possible) |
| `CalendarUID` | ✅ | `-1` (inherit dari base calendar) |
| `ConstraintDate` | ✅ | `1970-01-01T00:00:00` |
| `LevelAssignments` | ✅ | `0` |
| `LevelingCanSplit` | ✅ | `0` |
| `LevelingDelay` | ✅ | `0` |
| `LevelingDelayFormat` | ✅ | `7` |
| `IgnoreResourceCalendar` | ✅ | `0` |
| `HideBar` | ✅ | `0` |
| `Rollup` | ✅ | `0` |
| `EarnedValueMethod` | ✅ | `0` |
| `Active` | ✅ | `1` |
| `Manual` | ✅ | `0` |
| `PredecessorLink` | ⚠️ | **Langsung di dalam Task** (tanpa wrapper PredecessorLinks) |
| `Priority` | ⚠️ | `500` default |

⚠️ **Semua field di atas WAJIB ada di setiap Task**, meskipun nilai default.

### Self-Closing Tags

ProjectLibre sensitif terhadap self-closing tags (`<Manager/>` vs `<Manager></Manager>`). Selalu gunakan **paired tags** untuk elemen yang mungkin kosong:
- ✅ `<WBS></WBS>` (bukan `<WBS/>`)
- ✅ `<Group></Group>` (bukan `<Group/>`)
- ✅ `<Manager></Manager>` (bukan `<Manager/>`)
 Kalau ada field yang hilang, ProjectLibre bisa menolak file tanpa pesan error yang jelas.

### Strategi Generate File Besar (Template-copy approach)

Untuk file 45+ tasks, **jangan generate dari nol** — terlalu besar untuk output model. Gunakan pendekatan:

1. **Baca Template.xml** sebagai string
2. **Regex replace sections**: header, resources, tasks, assignments
3. **Generate task XML string** via Python (loop) — kode ringkas, data di tuple
4. **Write then execute**: tulis script ke `/tmp/gen_.py`, execute dengan `bash`

### XML Declaration

Template.xml pakai:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
```

Proyek baru harus **sama persis** — termasuk `standalone="yes"`. Kalau hasil DOM parsing kehilangan `standalone`, ProjectLibre bisa tolak file.

### PredecessorLink (dependency)

⚠️ **KRUSIAL — Pastikan format ini EXACT**: `PredecessorLink` ditempatkan **LANGSUNG** di dalam `<Task>`, **TANPA** wrapper `<PredecessorLinks>`. Menggunakan wrapper `<PredecessorLinks>` menyebabkan ProjectLibre tidak membaca predecessor (kolom kosong).

✅ **BENAR** (sama persis Template.xml):
```xml
<Task>
    ...
    <PredecessorLink>
        <PredecessorUID>3</PredecessorUID>
        <Type>1</Type>
        <CrossProject>0</CrossProject>
    </PredecessorLink>
    <Active>1</Active>
    <Manual>0</Manual>
</Task>
```

❌ **SALAH** (ProjectLibre abaikan predecessor):
```xml
<PredecessorLinks>
    <PredecessorLink>
        <PredecessorUID>3</PredecessorUID>
        ...
    </PredecessorLink>
</PredecessorLinks>
```

- `Type`: `1` = FS (Finish-to-Start)
- `CrossProject`: `0`
- `LinkLag` dan `LagFormat`: **TIDAK PERLU** ditambahkan — Template.xml tidak memakai-nya, dan ProjectLibre lebih toleran tanpa-nya

### Durasi
- 1 hari = 8 jam (Senin-Jumat = 8 jam, Sabtu = 8 jam)
- `PT80H0M0S` = 80 jam = 10 hari kerja (Senin-Jumat) atau ~8 hari (Senin-Sabtu)
- `PT0H0M0S` = milestone

## Workflow

### 1. Membuat Schedule Baru (XML)
1. Tanya user: nama project, start date, berapa phase, task-list
2. Generate file XML dengan template di atas
3. Cari tahu **hari libur nasional** yang relevan (filter hanya yang jatuh di hari kerja dalam rentang project)
4. Tambahkan `Exceptions` untuk setiap hari libur
5. Tulis file ke path yang diminta user

### 2. Menambahkan Hari Libur ke Schedule Existing (XML)
1. Baca file XML yang sudah ada
2. Cari `<Calendar>` → cek apakah sudah ada `<Exceptions>` block
3. Jika belum ada, tambahkan `<Exceptions></Exceptions>` setelah `</WeekDays>`
4. Tambahkan `<Exception>` untuk setiap hari libur
5. Pastikan `UID` di Exception unik & sequential

### 3. Menambahkan/Update Task (XML)
1. Baca file XML
2. Cari `<Tasks>` section
3. Tambahkan `<Task>` baru dengan format di atas
4. Update `FinishDate` di header jika perlu
5. Update `Duration` pada summary task

### 4. Mengubah Kalender (hari kerja/libur)
1. Baca file XML
2. Cari `<Calendar>` dengan nama yang sesuai
3. Ubah `<DayWorking>` pada `<WeekDay>` yang sesuai
4. Contoh: ubah Sabtu jadi kerja → `DayType=6`, `DayWorking=1`

## Contoh Penggunaan

### Generate Schedule Baru (XML)
```
User: "Buat schedule project IADAM selama 6 bulan mulai 28 Juli 2026"
→ Generate file XML dengan template
→ Cari hari libur nasional Indonesia 2026
→ Tambahkan Exceptions
→ Tulis file
```

### Tambah Libur Nasional
```
User: "Tambahin hari libur nasional 2026 ke schedule"
→ Baca XML
→ Tambah Exceptions
→ Tulis ulang
```

### Tambah Task Baru
```
User: "Tambah task 'Sprint Planning' 2 hari setelah Kick-off"
→ Baca XML
→ Cari task Kick-off
→ Hitung start date (hari setelah Kick-off)
→ Tambah task baru dengan PredecessorLink ke Kick-off
→ Tulis ulang
```

## Tips
- Untuk **project besar**, generate semua task dulu baru tambah exceptions
- Cek hari libur: jika libur jatuh di **Sabtu/Minggu** (sudah non-working day), tidak perlu ditambahkan sebagai exception
- Hari libur nasional Indonesia: gunakan web search untuk lookup SKB 3 Menteri terbaru
- Untuk **cuti bersama**: filter hanya yang jatuh di hari kerja (Senin-Jumat atau Sabtu-jika-kerja)
- Gunakan `var date = new Date('YYYY-MM-DD')` untuk cek hari dalam bahasa js

## Strategi Output Token Limit untuk File Besar

Jika file XML schedule (45+ tasks / >30KB) tidak bisa dikirim dalam satu heredoc karena **output token limit** model:

### Masalah
- XML schedule dengan 45 task × ~43 tag = ~134KB file
- Model LLM punya batas output (~8K-32K tokens = ~32K-128K chars)
- Heredoc inline (`python3 << 'EOF'`) gagal karena teks terpotong sebelum lengkap terkirim

### Solusi: Write-then-Execute
1. **Tulis script Python** ke file `/tmp/gen_sched.py` pakai tool `write` (backend-to-backend, tanpa limitasi output model)
2. **Isi script**: baca template XML, proses header/resources/tasks/assignments, tulis output
3. **Execute** dengan `bash`: `cd /tmp && python3 gen_sched.py`
4. **Jika script masih terlalu besar**: pakai `>>` append bertahap:
   - `echo 'baris 1' > gen.py`
   - `cat >> gen.py << 'PART1'` → tulis bagian pertama
   - `cat >> gen.py << 'PART2'` → tulis bagian kedua
   - `python3 gen.py` → execute

### Alternatif: Template-first
- Generate dengan baca template XML → replace sections (Tasks, Resources, Assignments) → write output
- Lebih ringkas daripada build-from-scratch (template sudah punya calendars, header, struktur yang proven working)
- Simpan template sebagai base64 agar muat dalam satu perintah bash pendek

### Catatan
- Output token limit **bukan error** — bedakan dari timeout/crash
- Tanda: heredoc terpotong di tengah, script tidak lengkap saat dieksekusi
- Gunakan `wc -l` dan `wc -c` untuk cek apakah file output masuk akal