#!/usr/bin/env python3
"""
MS Project XML generator — ProjectLibre & MS Project compatible.

Usage:
  python3 generate_schedule.py --name "My Project" --output schedule.xml

  # Or import as module:
  from generate_schedule import ProjectSchedule
  sched = ProjectSchedule("My Project")
  sched.add_task("Task 1", duration="P1D")
  sched.add_task("Task 2", duration="P2D", predecessor="Task 1")
  sched.save("schedule.xml")
"""
from __future__ import annotations

import argparse
import uuid
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from typing import Optional


class ProjectSchedule:
    """Generate MS Project XML schedules compatible with ProjectLibre & MS Project."""

    def __init__(self, name: str, start_date: Optional[date] = None,
                 root_task_name: Optional[str] = None):
        self.name = name
        self.start_date = start_date or date.today()
        # Nama task root level 0 (= nama project). None = tanpa root task.
        self.root_task_name = root_task_name
        self.tasks: list[dict] = []
        self.resources: list[dict] = []
        self.holidays: list[dict] = []
        self._next_uid = 1
        self._children_of: dict[int, list[int]] = {}
        self._date_cache: dict[int, tuple[str, str]] = {}

    def add_task(
        self,
        name: str,
        duration: Optional[str] = None,
        predecessor: Optional[str] = None,
        start: Optional[str] = None,
        finish: Optional[str] = None,
        resource: Optional[str] = None,
        parent: Optional[str] = None,
        is_summary: bool = False,
    ) -> int:
        """Add a task. Returns UID.

        duration: ISO 8601 duration (P1D, P2D, PT8H, etc.). Omit or None for
                  summary tasks (dates auto-calculated from children).
        predecessor: name of task that must finish before this one starts
        start/finish: ISO 8601 date string (overrides auto-calculation). Use
                      only for milestones or fixed-date tasks.
        resource: resource name to assign
        parent: name of parent summary task for hierarchy
        is_summary: True if this is a summary/phase task (no work assigned,
                    dates from children). Overrides duration.
        """
        uid = self._next_uid
        self._next_uid += 1

        task = {
            "uid": uid,
            "name": name,
            "duration": duration,
            "predecessor": predecessor,
            "start": start,
            "finish": finish,
            "resource": resource,
            "parent": parent,
            "is_summary": is_summary,
        }
        self.tasks.append(task)

        if resource and not any(r["name"] == resource for r in self.resources):
            res_uid = self._next_uid
            self._next_uid += 1
            self.resources.append({"name": resource, "uid": res_uid})

        if parent:
            parent_uid = self._lookup_uid(parent)
            if parent_uid not in self._children_of:
                self._children_of[parent_uid] = []
            self._children_of[parent_uid].append(uid)

        return uid

    def add_holiday(self, name: str, date_str: str):
        """Add a non-working day (holiday). date_str: YYYY-MM-DD"""
        self.holidays.append({"name": name, "date": date_str})

    def add_resource(self, name: str) -> int:
        """Add a human resource (role). Stores the UID in the dict."""
        uid = self._next_uid
        self._next_uid += 1
        self.resources.append({"name": name, "uid": uid})
        return uid

    def _lookup_uid(self, task_name: str) -> int:
        for t in self.tasks:
            if t["name"] == task_name:
                return t["uid"]
        raise ValueError(f"Task '{task_name}' not found")

    @staticmethod
    def _iso_dur_to_hours(duration: str) -> int:
        """Convert ISO 8601 duration to hours (8h per day, 22d per month)."""
        if not duration:
            return 0
        days = 0
        hours = 0
        months = 0
        if duration.startswith("P"):
            rest = duration[1:]
            if "M" in rest and "T" not in rest.split("M")[0]:
                # P{n}M = months (not minutes)
                m_part = rest.split("M")[0]
                if m_part and m_part.isdigit():
                    months = int(m_part)
            elif "D" in rest:
                parts = rest.split("D")
                if parts[0].isdigit():
                    days = int(parts[0])
            elif "T" in rest or rest.startswith("T"):
                pass
        if "PT" in duration and "H" in duration:
            hstr = duration.split("H")[0].split("PT")[-1]
            if hstr.isdigit():
                hours = int(hstr)
        return months * 176 + days * 8 + hours

    def _is_milestone(self, task: dict) -> bool:
        return task["duration"] in ("P0D", "PT0H", None, "") and not bool(self._children_of.get(task["uid"]))

    def _add_working_days(self, start: date, working_days: int) -> date:
        """Add working days (skip weekends & holidays)."""
        current = start
        added = 0
        holidays = {h["date"] for h in self.holidays}
        while added < working_days:
            current += timedelta(days=1)
            if current.weekday() >= 5:  # Sat/Sun
                continue
            if current.isoformat() in holidays:
                continue
            added += 1
        return current

    def _calc_dates(self, task_index: int, _depth: int = 0,
                     parent_base: Optional[date] = None) -> tuple[str, str]:
        """Calculate start/finish dates.

        parent_base: For summary tasks computing children, the summary's own
                     base date (from predecessor chain). Children without an
                     explicit predecessor inherit this as their start date.
        """
        task = self.tasks[task_index]
        uid = task["uid"]

        if uid in self._date_cache:
            return self._date_cache[uid]

        if _depth >= 500:
            base_str = f"{self.start_date.isoformat()}T00:00:00"
            return base_str, base_str

        if task["start"] and task["finish"]:
            self._date_cache[uid] = (task["start"], task["finish"])
            return task["start"], task["finish"]

        # Summary task: derive base from predecessor, then compute children
        if task["is_summary"] or bool(self._children_of.get(task["uid"])):
            base = self.start_date
            if task["predecessor"]:
                pred_uid = self._lookup_uid(task["predecessor"])
                for t in self.tasks:
                    if t["uid"] == pred_uid:
                        _, pred_finish = self._calc_dates(self.tasks.index(t), _depth + 1)
                        base = datetime.strptime(pred_finish, "%Y-%m-%dT%H:%M:%S").date()
                        if self._is_milestone(t):  # milestone -> successor: same day
                            pass
                        else:
                            base = self._add_working_days(base, 1)  # next working day
                        break

            # Collect children's dates, passing `base` as parent_base
            child_dates = []
            for t in self.tasks:
                if t.get("parent") and self._lookup_uid(t["parent"]) == uid:
                    ci = self.tasks.index(t)
                    cs, cf = self._calc_dates(ci, _depth + 1, parent_base=base)
                    child_dates.append((cs, cf))

            if child_dates:
                child_dates.sort(key=lambda x: x[0])
                earliest = child_dates[0][0]
                latest = max(cf for _, cf in child_dates)
                self._date_cache[uid] = (earliest, latest)
                return earliest, latest
            else:
                start_str = f"{base.isoformat()}T08:00:00"
                self._date_cache[uid] = (start_str, start_str)
                return start_str, start_str

        # Leaf task
        base = parent_base if parent_base is not None else self.start_date
        if task["predecessor"]:
            pred_uid = self._lookup_uid(task["predecessor"])
            for t in self.tasks:
                if t["uid"] == pred_uid:
                    _, pred_finish = self._calc_dates(self.tasks.index(t), _depth + 1)
                    base = datetime.strptime(pred_finish, "%Y-%m-%dT%H:%M:%S").date()
                    if self._is_milestone(t) or self._is_milestone(task):  # milestone link: same day
                        pass
                    else:
                        base = self._add_working_days(base, 1)  # next working day
                    break

        # Duration in working days
        dur = task["duration"] or "P1D"
        working_days = 1
        if dur.startswith("P") and "M" in dur and "T" not in dur.split("M")[0]:
            months = int(dur[1:].split("M")[0])
            working_days = months * 22
        elif dur.startswith("P") and "D" in dur:
            parts = dur[1:].split("D")
            working_days = int(parts[0]) if parts[0].isdigit() else 1
        elif dur.startswith("PT") and "H" in dur:
            hours = int(dur.replace("PT", "").replace("H", ""))
            working_days = max(1, round(hours / 8))

        # Use working day calculation for finish
        finish = self._add_working_days(base, working_days - 1) if working_days > 0 else base
        start_str = f"{base.isoformat()}T08:00:00"
        finish_str = f"{finish.isoformat()}T17:00:00"
        self._date_cache[uid] = (start_str, finish_str)
        return start_str, finish_str

    def _get_outline_level(self, task: dict) -> int:
        level = 1
        visited = set()
        current = task
        while current.get("parent"):
            if current["uid"] in visited:
                break
            visited.add(current["uid"])
            level += 1
            try:
                parent_uid = self._lookup_uid(current["parent"])
                for t in self.tasks:
                    if t["uid"] == parent_uid:
                        current = t
                        break
                else:
                    break
            except ValueError:
                break
        return level

    def _compute_summary_work(self) -> dict[int, int]:
        """Compute Work (in hours) for each summary task by summing children."""
        # Process in reverse order so children are computed before parents
        summary_work: dict[int, int] = {}
        for task in reversed(self.tasks):
            uid = task["uid"]
            children = self._children_of.get(uid, [])
            if not children:
                continue
            total = 0
            for child_uid in children:
                child_work = summary_work.get(child_uid)
                if child_work is not None:
                    total += child_work
                else:
                    # Leaf child: Work = duration hours if has resource else 0
                    for t in self.tasks:
                        if t["uid"] == child_uid:
                            if t.get("resource"):
                                total += self._iso_dur_to_hours(t.get("duration", "P1D"))
                            break
            summary_work[uid] = total
        return summary_work

    def _build_xml(self) -> ET.Element:
        self._date_cache = {}
        summary_work = self._compute_summary_work()

        root = ET.Element("Project")
        root.set("xmlns", "http://schemas.microsoft.com/project")

        ET.SubElement(root, "SaveVersion").text = "14"
        ET.SubElement(root, "Name").text = self.name
        ET.SubElement(root, "CalendarUID").text = "1"
        ET.SubElement(root, "DefaultStartTime").text = "08:00:00"
        ET.SubElement(root, "DefaultFinishTime").text = "17:00:00"
        ET.SubElement(root, "MinutesPerDay").text = "480"
        ET.SubElement(root, "MinutesPerWeek").text = "2400"
        ET.SubElement(root, "DaysPerMonth").text = "22"
        ET.SubElement(root, "StartDate").text = f"{self.start_date.isoformat()}T08:00:00"
        ET.SubElement(root, "DurationFormat").text = "7"
        ET.SubElement(root, "DefaultTaskType").text = "0"
        ET.SubElement(root, "NewTasksAreManual").text = "1"
        ET.SubElement(root, "NewTasksEstimated").text = "1"
        ET.SubElement(root, "ScheduleFromStart").text = "1"
        ET.SubElement(root, "NewTaskStartDate").text = "0"
        ET.SubElement(root, "HonorConstraints").text = "0"

        # Calendar (wrapped in Calendars plural, matching MS Project export)
        cals = ET.SubElement(root, "Calendars")
        cal = ET.SubElement(cals, "Calendar")
        ET.SubElement(cal, "UID").text = "1"
        ET.SubElement(cal, "Name").text = "Standard"
        ET.SubElement(cal, "IsBaseCalendar").text = "1"
        ET.SubElement(cal, "IsBaselineCalendar").text = "0"
        ET.SubElement(cal, "BaseCalendarUID").text = "-1"
        wd = ET.SubElement(cal, "WeekDays")
        for day_type in range(1, 8):
            item = ET.SubElement(wd, "WeekDay")
            ET.SubElement(item, "DayType").text = str(day_type)
            ET.SubElement(item, "DayWorking").text = "0" if day_type in (1, 7) else "1"
            if day_type not in (1, 7):
                wt = ET.SubElement(item, "WorkingTimes")
                period = ET.SubElement(wt, "WorkingTime")
                ET.SubElement(period, "FromTime").text = "08:00:00"
                ET.SubElement(period, "ToTime").text = "12:00:00"
                period2 = ET.SubElement(wt, "WorkingTime")
                ET.SubElement(period2, "FromTime").text = "13:00:00"
                ET.SubElement(period2, "ToTime").text = "17:00:00"

        if self.holidays:
            exceptions = ET.SubElement(cal, "Exceptions")
            for i, h in enumerate(self.holidays, 1):
                exc = ET.SubElement(exceptions, "Exception")
                ET.SubElement(exc, "UID").text = str(i)
                ET.SubElement(exc, "Name").text = h["name"]
                ET.SubElement(exc, "Type").text = "2"
                tp = ET.SubElement(exc, "TimePeriod")
                ET.SubElement(tp, "FromDate").text = h["date"]
                ET.SubElement(tp, "ToDate").text = h["date"]

        # Tasks
        # Precompute semua tanggal dulu (root butuh min/max seluruh task)
        for i in range(len(self.tasks)):
            self._calc_dates(i)

        tasks_elem = ET.SubElement(root, "Tasks")
        assign_uid_counter = 1

        # Task root = nama project (opsional via root_task_name), level 1.
        # MS Project membuang task OutlineLevel 0 (terbukti di file fixing),
        # jadi root ditaruh di level 1 agar tampil di MS Project & ProjectLibre.
        # Urutan dokumen + OutlineLevel menentukan hierarki: root(1) pertama,
        # lalu fase(2) & task(3) otomatis jadi anaknya di kedua tool.
        if self.root_task_name:
            all_dates = [self._date_cache[t["uid"]] for t in self.tasks if t["uid"] in self._date_cache]
            if all_dates:
                root_start = min(d[0] for d in all_dates)
                root_finish = max(d[1] for d in all_dates)
            else:
                root_start = f"{self.start_date.isoformat()}T08:00:00"
                root_finish = root_start
            # Durasi root = jam kerja antara start & finish
            hs = {h["date"] for h in self.holidays}
            sd = datetime.strptime(root_start[:10], "%Y-%m-%d").date()
            fd = datetime.strptime(root_finish[:10], "%Y-%m-%d").date()
            wd = 0
            d = sd
            while d <= fd:
                if d.weekday() < 5 and d.isoformat() not in hs:
                    wd += 1
                d += timedelta(days=1)
            root_hours = wd * 8
            # Work root = total effort seluruh fase (top-level summary)
            top_work = sum(summary_work.get(t["uid"], 0) for t in self.tasks
                           if t["is_summary"] and not t.get("parent"))
            rt = ET.SubElement(tasks_elem, "Task")
            ET.SubElement(rt, "UID").text = "64"  # UID=0 ditolak MS Project; 64 seperti wrapper di fixing
            ET.SubElement(rt, "GUID").text = str(uuid.uuid4()).upper()
            ET.SubElement(rt, "ID").text = "1"
            ET.SubElement(rt, "Name").text = self.root_task_name
            ET.SubElement(rt, "Active").text = "1"
            ET.SubElement(rt, "Manual").text = "0"
            ET.SubElement(rt, "Type").text = "1"
            ET.SubElement(rt, "IsNull").text = "0"
            ET.SubElement(rt, "Estimated").text = "0"
            ET.SubElement(rt, "ConstraintType").text = "0"
            ET.SubElement(rt, "CalendarUID").text = "-1"
            ET.SubElement(rt, "Summary").text = "1"
            ET.SubElement(rt, "Milestone").text = "0"
            ET.SubElement(rt, "Duration").text = f"PT{root_hours}H0M0S"
            ET.SubElement(rt, "RemainingDuration").text = f"PT{root_hours}H0M0S"
            ET.SubElement(rt, "Work").text = f"PT{top_work}H0M0S"
            ET.SubElement(rt, "RegularWork").text = f"PT{top_work}H0M0S"
            ET.SubElement(rt, "RemainingWork").text = f"PT{top_work}H0M0S"
            ET.SubElement(rt, "DurationFormat").text = "21"
            ET.SubElement(rt, "Start").text = root_start
            ET.SubElement(rt, "Finish").text = root_finish
            ET.SubElement(rt, "OutlineLevel").text = "1"

        for i, task in enumerate(self.tasks):
            start, finish = self._calc_dates(i)
            outline_level = self._get_outline_level(task) + 1

            t = ET.SubElement(tasks_elem, "Task")
            ET.SubElement(t, "UID").text = str(task["uid"])
            # GUID + ID wajib agar MS Project menerima file (tanpa ini:
            # "Project cannot open the file")
            ET.SubElement(t, "GUID").text = str(uuid.uuid4()).upper()
            ET.SubElement(t, "ID").text = str(i + 2)  # +1: root ambil ID 1 (MS Project drop ID 0)
            ET.SubElement(t, "Name").text = task["name"]
            ET.SubElement(t, "Active").text = "1"
            ET.SubElement(t, "Manual").text = "0"
            ET.SubElement(t, "Type").text = "0"   # 0=Fixed Units (matching fix file leaf tasks)
            ET.SubElement(t, "IsNull").text = "0"
            ET.SubElement(t, "Estimated").text = "0"
            ET.SubElement(t, "ConstraintType").text = "0"
            ET.SubElement(t, "CalendarUID").text = "-1"

            dur = task["duration"]
            is_milestone = dur in ("P0D", "PT0H", None, "") and not self._children_of.get(task["uid"])
            is_summary_actual = bool(self._children_of.get(task["uid"]))

            if is_summary_actual:
                ET.SubElement(t, "Summary").text = "1"
            else:
                ET.SubElement(t, "Summary").text = "0"
            if is_milestone:
                ET.SubElement(t, "Milestone").text = "1"
            else:
                ET.SubElement(t, "Milestone").text = "0"

            duration_hours = self._iso_dur_to_hours(dur)
            if is_summary_actual:
                # Summary duration = working days between child Start/Finish
                from datetime import datetime as _dt
                hs = set(h["date"] for h in self.holidays)
                s_d = _dt.strptime(start[:10], "%Y-%m-%d").date()
                f_d = _dt.strptime(finish[:10], "%Y-%m-%d").date()
                wd = 0
                d = s_d
                while d <= f_d:
                    if d.weekday() < 5 and d.isoformat() not in hs:
                        wd += 1
                    d += timedelta(days=1)
                duration_hours = wd * 8
            ET.SubElement(t, "Duration").text = f"PT{duration_hours}H0M0S"

            # Work = Duration_hours for leaf tasks with resources
            # Work = PT0H0M0S for leaf tasks without resources
            # Summary tasks: Work = sum children (calculated later)
            if is_summary_actual:
                sw = summary_work.get(task["uid"], 0)
                ET.SubElement(t, "Work").text = f"PT{sw}H0M0S"
                ET.SubElement(t, "RegularWork").text = f"PT{sw}H0M0S"
                ET.SubElement(t, "RemainingWork").text = f"PT{sw}H0M0S"
            elif task["resource"] and duration_hours > 0:
                ET.SubElement(t, "Work").text = f"PT{duration_hours}H0M0S"
                ET.SubElement(t, "RegularWork").text = f"PT{duration_hours}H0M0S"
                ET.SubElement(t, "RemainingWork").text = f"PT{duration_hours}H0M0S"
            else:
                ET.SubElement(t, "Work").text = "PT0H0M0S"
                ET.SubElement(t, "RegularWork").text = "PT0H0M0S"
                ET.SubElement(t, "RemainingWork").text = "PT0H0M0S"
            if duration_hours > 0:
                ET.SubElement(t, "RemainingDuration").text = f"PT{duration_hours}H0M0S"
            else:
                ET.SubElement(t, "RemainingDuration").text = "PT0H0M0S"

            # DurationFormat: 7=days, 21=elapsed_days, 11=months
            if duration_hours >= 960:
                df = "11"   # months for very long tasks
            elif duration_hours >= 80:
                df = "21"   # elapsed days for phase/sprint tasks
            else:
                df = "7"    # days for normal tasks
            ET.SubElement(t, "DurationFormat").text = df
            ET.SubElement(t, "Start").text = start
            ET.SubElement(t, "Finish").text = finish
            ET.SubElement(t, "OutlineLevel").text = str(outline_level)

            # PredecessorLink
            if task["predecessor"]:
                pred_uid = self._lookup_uid(task["predecessor"])
                link = ET.SubElement(t, "PredecessorLink")
                ET.SubElement(link, "PredecessorUID").text = str(pred_uid)
                ET.SubElement(link, "Type").text = "1"
                ET.SubElement(link, "CrossProject").text = "0"
                ET.SubElement(link, "LinkLag").text = "0"
                ET.SubElement(link, "LagFormat").text = "7"

        # Separate Assignments section (MS Project requires this, not inline)
        all_assignments: list[dict] = []
        for i, task in enumerate(self.tasks):
            if task["resource"]:
                for r in self.resources:
                    if r["name"] == task["resource"]:
                        ts, tf = self._calc_dates(i)
                        dur_h = self._iso_dur_to_hours(task["duration"])
                        all_assignments.append({
                            "uid": assign_uid_counter,
                            "resource_uid": r["uid"],
                            "task_uid": task["uid"],
                            "hours": dur_h,
                            "start": ts,
                            "finish": tf,
                        })
                        assign_uid_counter += 1
                        break

        # Resources
        if self.resources:
            res_elem = ET.SubElement(root, "Resources")
            for r in self.resources:
                res = ET.SubElement(res_elem, "Resource")
                ET.SubElement(res, "UID").text = str(r["uid"])
                ET.SubElement(res, "GUID").text = str(uuid.uuid4()).upper()
                ET.SubElement(res, "ID").text = str(r["uid"])
                ET.SubElement(res, "Name").text = r["name"]
                ET.SubElement(res, "Type").text = "1"
                ET.SubElement(res, "IsNull").text = "0"
                ET.SubElement(res, "MaxUnits").text = "100"

        # Separate Assignments section (MS Project reads this, not inline)
        if all_assignments:
            assns = ET.SubElement(root, "Assignments")
            for a in all_assignments:
                # Field set lengkap menyerupai export ProjectLibre — penting agar UI
                # membaca Work/Start/Finish assignment (tanpa ini Work terbaca null
                # dan kolom resource bisa tampil aneh seperti "Nama[0%]")
                w = f"PT{a['hours']}H0M0S"
                z = "PT0H0M0S"
                zz = "0.00"
                assn = ET.SubElement(assns, "Assignment")
                ET.SubElement(assn, "UID").text = str(a["uid"])
                ET.SubElement(assn, "GUID").text = str(uuid.uuid4()).upper()
                ET.SubElement(assn, "TaskUID").text = str(a["task_uid"])
                ET.SubElement(assn, "ResourceUID").text = str(a["resource_uid"])
                ET.SubElement(assn, "PercentWorkComplete").text = "0"
                ET.SubElement(assn, "ActualCost").text = "0"
                ET.SubElement(assn, "ActualOvertimeCost").text = "0"
                ET.SubElement(assn, "ActualOvertimeWork").text = z
                ET.SubElement(assn, "ActualWork").text = z
                ET.SubElement(assn, "ACWP").text = zz
                ET.SubElement(assn, "Confirmed").text = "0"
                ET.SubElement(assn, "Cost").text = "0"
                ET.SubElement(assn, "CostRateTable").text = "0"
                ET.SubElement(assn, "RateScale").text = "0"
                ET.SubElement(assn, "CostVariance").text = "0"
                ET.SubElement(assn, "CV").text = zz
                ET.SubElement(assn, "Delay").text = "0"
                ET.SubElement(assn, "Finish").text = a["finish"]
                ET.SubElement(assn, "FinishVariance").text = "0"
                ET.SubElement(assn, "WorkVariance").text = zz
                ET.SubElement(assn, "HasFixedRateUnits").text = "1"
                ET.SubElement(assn, "FixedMaterial").text = "0"
                ET.SubElement(assn, "LevelingDelay").text = "0"
                ET.SubElement(assn, "LevelingDelayFormat").text = "39"
                ET.SubElement(assn, "LinkedFields").text = "0"
                ET.SubElement(assn, "Milestone").text = "0"
                ET.SubElement(assn, "Overallocated").text = "0"
                ET.SubElement(assn, "OvertimeCost").text = "0"
                ET.SubElement(assn, "OvertimeWork").text = z
                ET.SubElement(assn, "RegularWork").text = w
                ET.SubElement(assn, "RemainingCost").text = "0"
                ET.SubElement(assn, "RemainingOvertimeCost").text = "0"
                ET.SubElement(assn, "RemainingOvertimeWork").text = z
                ET.SubElement(assn, "RemainingWork").text = w
                ET.SubElement(assn, "ResponsePending").text = "0"
                ET.SubElement(assn, "Start").text = a["start"]
                ET.SubElement(assn, "StartVariance").text = "0"
                ET.SubElement(assn, "Units").text = "1"
                ET.SubElement(assn, "UpdateNeeded").text = "0"
                ET.SubElement(assn, "VAC").text = zz
                ET.SubElement(assn, "Work").text = w
                ET.SubElement(assn, "WorkContour").text = "0"
                ET.SubElement(assn, "BCWS").text = zz
                ET.SubElement(assn, "BCWP").text = zz
                ET.SubElement(assn, "BookingType").text = "0"
                ET.SubElement(assn, "BudgetCost").text = "0"
                ET.SubElement(assn, "BudgetWork").text = z
                ET.SubElement(assn, "CreationDate").text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        return root

    def save(self, path: str):
        ET.register_namespace("", "http://schemas.microsoft.com/project")
        tree = ET.ElementTree(self._build_xml())
        tree.write(path, encoding="UTF-8", xml_declaration=True)

    def to_string(self) -> str:
        ET.register_namespace("", "http://schemas.microsoft.com/project")
        import io
        buf = io.StringIO()
        tree = ET.ElementTree(self._build_xml())
        tree.write(buf, encoding="unicode", xml_declaration=True)
        return buf.getvalue()


def main():
    parser = argparse.ArgumentParser(description="Generate MS Project XML schedule")
    parser.add_argument("--name", default="Project", help="Project name")
    parser.add_argument("--start", default=date.today().isoformat(), help="Start date YYYY-MM-DD")
    parser.add_argument("--output", "-o", default="schedule.xml", help="Output XML file")
    args = parser.parse_args()

    sched = ProjectSchedule(args.name, start_date=date.fromisoformat(args.start))
    sched.save(args.output)
    print(f"✓ {args.output}")


if __name__ == "__main__":
    main()
