"""Analyze resource/capacity from an MS Project XML file.

Usage:
    python analyze_capacity.py <schedule.xml>

Prints:
  - Work per resource (hours + person-days) + assignment span + utilization
  - Effort per phase/summary task
  - Overlap detection (resource assigned to 2+ parallel tasks)

Uses only the standard library (ElementTree), consistent with
generate_schedule.py. Person-day (PD) = 8 hours. Capacity = working days
(Mon-Fri, no holiday calendar) x 8h between the resource's assignment
start and finish.
"""

import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta

NS = {"p": "http://schemas.microsoft.com/project"}


def iso_hours(s: str) -> int:
    """'PT40H0M0S' / 'PT40H' -> 40"""
    s = (s or "").replace("PT", "").replace("H0M0S", "").replace("H", "")
    return int(s) if s.strip().isdigit() else 0


def pd(hours: int) -> float:
    return round(hours / 8, 1)


def d(s: str) -> date:
    return date.fromisoformat(s[:10])


def working_days(start: date, finish: date) -> int:
    n, cur = 0, start
    while cur <= finish:
        if cur.weekday() < 5:
            n += 1
        cur += timedelta(days=1)
    return n


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    root = ET.parse(path).getroot()

    # Resources: UID -> name
    ress = {}
    for e in root.findall("p:Resources/p:Resource", NS):
        uid = (e.findtext("p:UID", default="", namespaces=NS) or "").strip()
        name = (e.findtext("p:Name", default="", namespaces=NS) or "").strip()
        ress[uid] = name

    # Assignments: aggregate per resource
    work: dict[str, dict] = {}
    intervals: dict[str, list] = {}
    total_hours = 0
    for a in root.findall("p:Assignments/p:Assignment", NS):
        ru = (a.findtext("p:ResourceUID", default="", namespaces=NS) or "").strip()
        tu = (a.findtext("p:TaskUID", default="", namespaces=NS) or "").strip()
        w = iso_hours(a.findtext("p:Work", default="", namespaces=NS))
        st = (a.findtext("p:Start", default="", namespaces=NS) or "")[:10]
        fi = (a.findtext("p:Finish", default="", namespaces=NS) or "")[:10]
        name = ress.get(ru, f"UID {ru}")
        total_hours += w
        rec = work.setdefault(name, {"hours": 0, "n": 0, "start": st, "finish": fi})
        rec["hours"] += w
        rec["n"] += 1
        rec["start"] = min(rec["start"], st)
        rec["finish"] = max(rec["finish"], fi)
        intervals.setdefault(name, []).append((st, fi, tu))

    print("=== Effort per Resource (dari assignment) ===")
    print(f"{'Resource':<38}{'Jam':>6}{'PD':>8}{'Task':>6}  {'Rentang assignment':<24}{'Utilisasi':>10}")
    for name, rec in sorted(work.items(), key=lambda kv: -kv[1]["hours"]):
        cap = working_days(d(rec["start"]), d(rec["finish"])) * 8
        util = f"{rec['hours'] / cap * 100:.0f}%" if cap else "-"
        print(f"{name:<38}{rec['hours']:>6}{pd(rec['hours']):>8}{rec['n']:>6}  "
              f"{rec['start']} -> {rec['finish']:<11}{util:>10}")
    print(f"{'TOTAL':<38}{total_hours:>6}{pd(total_hours):>8}{sum(r['n'] for r in work.values()):>6}")
    print()

    print("=== Effort per Fase (summary tasks) ===")
    print(f"{'Summary':<50}{'Start':<12}{'Finish':<12}{'PD':>6}{'Durasi':>9}")
    for t in root.findall("p:Tasks/p:Task", NS):
        if (t.findtext("p:Summary", default="0", namespaces=NS) or "").strip() == "1":
            name = (t.findtext("p:Name", default="", namespaces=NS) or "").strip()
            lvl = (t.findtext("p:OutlineLevel", default="", namespaces=NS) or "").strip()
            if lvl == "1":  # root task
                continue
            st = (t.findtext("p:Start", default="", namespaces=NS) or "")[:10]
            fi = (t.findtext("p:Finish", default="", namespaces=NS) or "")[:10]
            w = iso_hours(t.findtext("p:Work", default="", namespaces=NS))
            dur = iso_hours(t.findtext("p:Duration", default="", namespaces=NS))
            print(f"{name:<50}{st:<12}{fi:<12}{pd(w):>6}{dur/8:>7.1f}d")
    print()

    # Overlap detection: two intervals overlap if a.start <= b.finish and b.start <= a.finish
    print("=== Overlap Check (resource di-assign paralel) ===")
    found = False
    for name, iv in sorted(intervals.items()):
        ivs = sorted(iv)
        for i in range(len(ivs)):
            for j in range(i + 1, len(ivs)):
                a1, a2, ta = ivs[i]
                b1, b2, tb = ivs[j]
                if a1 <= b2 and b1 <= a2:
                    found = True
                    print(f"  {name}: task {ta} ({a1}..{a2}) tumpang tindih task {tb} ({b1}..{b2})")
    if not found:
        print("  Tidak ada overlap (semua resource bekerja serial).")


if __name__ == "__main__":
    main()
