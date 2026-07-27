---
name: project-schedule
description: Generate, update, and maintain MS Project XML schedules compatible with ProjectLibre. Use when the user wants to create a project timeline, add tasks, set dependencies, add holidays, or export schedule in MS Project XML format.
---

# Skill: Project Schedule

This skill generates and maintains MS Project XML schedules that are compatible with both Microsoft Project and ProjectLibre.

---

## Scope

Output is limited to **MS Project XML (.xml)** — a text-based XML format that is human-editable, compatible with ProjectLibre (File → Open), and MS Project.

---

## MS Project XML Structure Overview

Use the template below as a base. Do not rewrite from scratch for every edit; prefer `edit` for incremental updates.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project xmlns="http://schemas.microsoft.com/project">
  <SaveVersion>16.0</SaveVersion>
  <Name>Project Name</Name>
  <Calendar>
    <UID>1</UID>
    <Name>Standard</Name>
    <WeekDays>
      <WeekDay>
        <DayType>1</DayType>
        <DayWorking>1</DayWorking>
      </WeekDay>
    </WeekDays>
  </Calendar>
  <Tasks>
    <Task>
      <UID>1</UID>
      <Name>Task Name</Name>
      <Duration>PT8H0M0S</Duration>
      <Start>2025-01-01T00:00:00</Start>
      <Finish>2025-01-02T00:00:00</Finish>
      <PredecessorLink>
        <PredecessorUID>0</PredecessorUID>
        <Type>1</Type>
      </PredecessorLink>
    </Task>
  </Tasks>
  <Resources>
    <Resource>
      <UID>1</UID>
      <Name>Resource Name</Name>
    </Resource>
  </Resources>
</Project>
```

---

## Critical MS Project XML Rules

1. **CalendarUID consistency**: The `CalendarUID` in the header must match the UID of the base calendar (usually `1`).
2. **Default time fields**: `DefaultStartTime` and `DefaultFinishTime` in ProjectLibre default to `15:00:00` and `00:00:00` — **do NOT change** these to `08:00:00`/`17:00:00`. Those values are internal MS Project offsets, not actual working hours.
3. **ProjectLibre exception format**: ProjectLibre **rejects files** using the MS Project `<Date>` exception format. Use `TimePeriod` with `FromDate`/`ToDate` instead.
   - **Correct example** — ProjectLibre native `TimePeriod` format:
     ```xml
     <Exception>
       <Name>New Year's Day</Name>
       <Type>2</Type>
       <TimePeriod>
         <FromDate>2025-01-01</FromDate>
         <ToDate>2025-01-01</ToDate>
       </TimePeriod>
     </Exception>
     ```
   - **Incorrect** — MS Project original `<Date>` format is **NOT** compatible with ProjectLibre:
     ```xml
     <Exception>
       <Name>New Year's Day</Name>
       <Type>2</Type>
       <Date>2025-01-01</Date>
     </Exception>
     ```
   - ⚠️ **WARNING**: The `<Date>` element is MS Project native and **incompatible** with ProjectLibre. ProjectLibre only reads `TimePeriod` elements using `FromDate`/`ToDate`.

---

## Validation Matrix

| Field | ProjectLibre | MS Project | Notes |
|:---|:---:|:---:|:---|
| `<WBS>` | ✅ | ✅ | Matches UID |
| `<Start>` | ✅ | ✅ | Standard ISO 8601 |
| `<Finish>` | ✅ | ✅ | Standard ISO 8601 |
| `<Duration>` | ✅ | ✅ | ISO 8601 duration |
| `<PredecessorLink>` | ✅ | ✅ | Required dependency |
| `<CalendarUID>` | ✅ | ✅ | Must match base calendar |
| `<TimePeriod>` | ✅ | ❌ | ProjectLibre native only |
| `<Date>` | ❌ | ✅ | **Do not use for ProjectLibre** |

---

## ProjectLibre Exception Format Guide

### Correct ProjectLibre Format
ProjectLibre uses **`TimePeriod`** with `FromDate`/`ToDate`, **NOT** the `<Date>` element:

| Element | Required | Description |
|:---|:---:|:---|
| `<Name>` | Yes | Holiday/exception name |
| `<Type>` | Yes | `2` = holiday, `1` = working day |
| `<FromDate>` | Yes | Start of period |
| `<ToDate>` | Yes | End of period |
| `<TimePeriod>` | Yes | Container for dates |

**Correct structure**:
```xml
<Exception>
  <Name>Christmas</Name>
  <Type>2</Type>
  <FromDate>2025-12-25</FromDate>
  <ToDate>2025-12-25</ToDate>
</Exception>
```

### Invalid Format (MS Project Original)
⚠️ **WARNING**: The `<Date>` element is MS Project native and **incompatible** with ProjectLibre:

```xml
<!-- DO NOT USE THIS FOR PROJECTLIBRE -->
<Exception>
  <Name>Christmas</Name>
  <Type>2</Type>
  <Date>2025-12-25</Date>
</Exception>
```

---

## Field Reference

| ID | Required | Description |
|:---|:---:|:---|
| `<UID>` | ✅ | Unique identifier |
| `<Name>` | ✅ | Task/resource name |
| `<Start>` | ✅ | ISO 8601 start date |
| `<Finish>` | ✅ | ISO 8601 finish date |
| `<Duration>` | ✅ | ISO 8601 duration |
| `<WBS>` | ❌ | Must remain **empty** `<WBS></WBS>` — ProjectLibre auto-generates WBS from OutlineNumber. If populated, the parser fails. |
| `<CalendarUID>` | ✅ | Must match base calendar UID (usually `1`) |

---

## Recurring Tasks

Recurring tasks must use the correct recurrence type and pattern. Supported types:

| Type | Description |
|:---|:---|
| `1` | Daily |
| `2` | Weekly |
| `3` | Monthly |
| `4` | Yearly |

**Correct weekly pattern example**:
```xml
<RecurrenceData>
  <RecurrenceType>2</RecurrenceType>
  <WeekFrequency>1</WeekFrequency>
  <DaysOfWeek>2</DaysOfWeek>
  <DayPicker>0</DayPicker>
</RecurrenceData>
```

---

## Assignment Rules

Resources must be assigned using the `<Assignment>` element within the task:

```xml
<Assignment>
  <ResourceUID>1</ResourceUID>
  <TaskUID>1</TaskUID>
  <Units>100</Units>
</Assignment>
```

---

## Constraints

Tasks can have constraints:

```xml
<Constraint>
  <Type>2</Type> <!-- Must Start On -->
  <Date>2025-01-01T00:00:00</Date>
</Constraint>
```

---

## Encoding Rules

All XML files must be UTF-8 encoded. Special characters must be escaped:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&apos;`

---

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|:---|:---|:---|
| "File cannot be opened" | Invalid XML structure | Validate XML structure |
| "WBS duplicate" | WBS field populated | Remove `<WBS>` value |
| "Date format error" | Wrong date format | Use ISO 8601 format |
| "Calendar not found" | Invalid CalendarUID | Verify calendar UID |

---

## Python Utility

A Python script (`generate_schedule.py`) is provided at `~/.claude/skills/project-schedule/scripts/generate_schedule.py` for generating valid MS Project XML programmatically:

```python
# Usage: cd ~/.claude/skills/project-schedule/scripts
# Then run python3 generate_schedule.py or import:
from generate_schedule import ProjectSchedule

schedule = ProjectSchedule("My Project")
schedule.add_task("Task 1", duration="P1D")
schedule.add_task("Task 2", duration="P2D", predecessor="Task 1")
schedule.add_holiday("New Year", "2026-01-01")
schedule.save("schedule.xml")
```

**Run directly:**
```bash
cd ~/.claude/skills/project-schedule/scripts && python3 generate_schedule.py --name "My Project" --output schedule.xml
```

---

## Notes

- Always validate the generated XML against MS Project XML schema before distributing.
- Test files in ProjectLibre to ensure compatibility.
- Use `TimePeriod` with `FromDate`/`ToDate` for all holiday/exception entries in ProjectLibre files.
- Avoid the MS Project native `<Date>` element — ProjectLibre will reject the file.
