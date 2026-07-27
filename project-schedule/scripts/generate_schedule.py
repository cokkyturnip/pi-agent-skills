#!/usr/bin/env python3
"""
MS Project XML generator — ProjectLibre compatible.

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
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from typing import Optional


class ProjectSchedule:
    """Generate MS Project XML schedules compatible with ProjectLibre."""

    def __init__(self, name: str, start_date: Optional[date] = None):
        self.name = name
        self.start_date = start_date or date.today()
        self.tasks: list[dict] = []
        self.resources: list[dict] = []
        self.holidays: list[dict] = []
        self._next_uid = 1

    def add_task(
        self,
        name: str,
        duration: str = "P1D",
        predecessor: Optional[str] = None,
        start: Optional[str] = None,
        finish: Optional[str] = None,
        resource: Optional[str] = None,
    ) -> int:
        """Add a task. Returns UID.

        duration: ISO 8601 duration (P1D, P2D, PT8H, etc.)
        predecessor: name of task that must finish before this one starts
        start/finish: ISO 8601 date string (overrides auto-calculation)
        resource: resource name to assign
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
        }
        self.tasks.append(task)

        # Auto-register resource
        if resource and not any(r["name"] == resource for r in self.resources):
            self.resources.append({"name": resource})

        return uid

    def add_holiday(self, name: str, date_str: str):
        """Add a non-working day (holiday). date_str: YYYY-MM-DD"""
        self.holidays.append({"name": name, "date": date_str})

    def add_resource(self, name: str) -> int:
        uid = self._next_uid
        self._next_uid += 1
        self.resources.append({"name": name})
        return uid

    def _lookup_uid(self, task_name: str) -> int:
        for t in self.tasks:
            if t["name"] == task_name:
                return t["uid"]
        raise ValueError(f"Task '{task_name}' not found")

    def _calc_dates(self, task_index: int) -> tuple[str, str]:
        task = self.tasks[task_index]
        if task["start"] and task["finish"]:
            return task["start"], task["finish"]

        base = self.start_date
        if task["predecessor"]:
            pred_uid = self._lookup_uid(task["predecessor"])
            for t in self.tasks:
                if t["uid"] == pred_uid:
                    _, pred_finish = self._calc_dates(self.tasks.index(t))
                    base = datetime.strptime(pred_finish, "%Y-%m-%dT%H:%M:%S").date()
                    base += timedelta(days=1)
                    break

        dur = task["duration"]
        days = 1
        if dur.startswith("P") and "D" in dur:
            days = int(dur.replace("P", "").replace("D", ""))
        elif dur.startswith("PT") and "H" in dur:
            hours = int(dur.replace("PT", "").replace("H", ""))
            days = max(1, round(hours / 8))

        start_str = f"{base.isoformat()}T00:00:00"
        finish = base + timedelta(days=days)
        finish_str = f"{finish.isoformat()}T00:00:00"
        return start_str, finish_str

    def _build_xml(self) -> ET.Element:
        root = ET.Element("Project")
        root.set("xmlns", "http://schemas.microsoft.com/project")

        ET.SubElement(root, "SaveVersion").text = "16.0"
        ET.SubElement(root, "Name").text = self.name

        cal = ET.SubElement(root, "Calendar")
        ET.SubElement(cal, "UID").text = "1"
        ET.SubElement(cal, "Name").text = "Standard"
        wd = ET.SubElement(cal, "WeekDays")
        for day_type in range(1, 8):
            item = ET.SubElement(wd, "WeekDay")
            ET.SubElement(item, "DayType").text = str(day_type)
            ET.SubElement(item, "DayWorking").text = "0" if day_type in (1, 7) else "1"

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

        tasks_elem = ET.SubElement(root, "Tasks")
        for i, task in enumerate(self.tasks):
            start, finish = self._calc_dates(i)
            t = ET.SubElement(tasks_elem, "Task")
            ET.SubElement(t, "UID").text = str(task["uid"])
            ET.SubElement(t, "Name").text = task["name"]
            ET.SubElement(t, "Duration").text = task["duration"]
            ET.SubElement(t, "Start").text = start
            ET.SubElement(t, "Finish").text = finish

            pred_uid = self._lookup_uid(task["predecessor"]) if task["predecessor"] else 0
            link = ET.SubElement(t, "PredecessorLink")
            ET.SubElement(link, "PredecessorUID").text = str(pred_uid)
            ET.SubElement(link, "Type").text = "1"

            if task["resource"]:
                for r in self.resources:
                    if r["name"] == task["resource"]:
                        assn = ET.SubElement(t, "Assignment")
                        ET.SubElement(assn, "ResourceUID").text = str(r.get("uid", 1))
                        ET.SubElement(assn, "TaskUID").text = str(task["uid"])
                        ET.SubElement(assn, "Units").text = "100"
                        break

        if self.resources:
            res_elem = ET.SubElement(root, "Resources")
            for r in self.resources:
                res = ET.SubElement(res_elem, "Resource")
                res_uid = r.get("uid", 1)
                ET.SubElement(res, "UID").text = str(res_uid)
                ET.SubElement(res, "Name").text = r["name"]

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