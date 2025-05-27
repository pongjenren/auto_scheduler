# scheduler/allocator.py
from datetime import datetime, timedelta, time
from collections import defaultdict



import os
import json

def load_available_slots():
    path = os.path.join(os.getcwd(), "data", "available_slots.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_tasks():
    path = os.path.join(os.getcwd(), "data", "tasks.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def allocate():
    avaliable_slots = load_available_slots()
    tasks = load_tasks()

    if not avaliable_slots or not tasks:
        return
    
    # 讀取tasks中的所有"due"並取出最晚的日期
    last_due = max((task["due_date"] for task in tasks), default=None)

    # 1. Prepare slots: sort by date and time
    # 依據 today ~ last_due 的日期範圍，展開所有可用 slots
    today = datetime.today().date()
    last_due_date = datetime.strptime(last_due, "%Y-%m-%d").date() if last_due else today
    slots = []
    for d in range((last_due_date - today).days + 1):
        cur_date = today + timedelta(days=d)
        weekday = cur_date.weekday()  # monday=0
        for slot in avaliable_slots:
            if slot["day"] == weekday:
                slots.append({
                    "date": cur_date.strftime("%Y-%m-%d"),
                    "hour": slot["hour"],
                })
    slots = sorted(slots, key=lambda s: (s["date"], s["hour"]))
    slot_usage = [False] * len(slots)

    # 2. Prepare tasks: sort by due date first
    tasks = sorted(tasks, key=lambda t: t["due_date"])

    # 3. Split tasks into subtasks
    subtasks = []
    for task in tasks:
        est = int(task["est_hours"])
        times = int(task["est_times"])  # 預估時間
        l = [int(est//times)] * times
        est -= sum(l)  # 剩餘時間
        for i in range(est):
            l[i] += 1
        # Find all slots that can fit this task
        # Split into est subtasks, each as close as possible to 1 hour

        for i in range(times):
            duration = l[i]
            subtasks.append({
                "task_id": task["id"],
                "subtask_id": os.urandom(8).hex(),
                "title": task["title"],
                "due_date": task["due_date"],
                "duration": duration,
                "subtask_index": i,
            })
    # 4. Allocate subtasks to slots
    schedule = []
    assigned_per_day = defaultdict(set)  # date -> set of task_ids

    ### start from here

    for subtask in subtasks:
        allocated = False
        for idx, slot in enumerate(slots):
            if slot_usage[idx]:
                continue
            slot_date = slot["date"]
            # Don't assign same task twice in one day
            if subtask["task_id"] in assigned_per_day[slot_date]:
                continue
            # Check if slot is long enough
            slot_start = _to_time(slot["start"])
            slot_end = _to_time(slot["end"])
            slot_minutes = (datetime.combine(datetime.today(), slot_end) -
                            datetime.combine(datetime.today(), slot_start)).seconds // 60
            if slot_minutes < subtask["duration"]:
                continue
            # Assign
            start_dt = datetime.strptime(f"{slot['date']} {slot['start']}", "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(minutes=subtask["duration"])
            schedule.append({
                "task_id": subtask["task_id"],
                "subtask_index": subtask["subtask_index"],
                "name": subtask["name"],
                "start": start_dt.strftime("%Y-%m-%d %H:%M"),
                "end": end_dt.strftime("%Y-%m-%d %H:%M"),
                "duration": subtask["duration"],
            })
            slot_usage[idx] = True
            assigned_per_day[slot_date].add(subtask["task_id"])
            allocated = True
            break
        if not allocated:
            # Could not allocate this subtask
            continue

    # 5. Save to schedule.json
    out_path = os.path.join(os.getcwd(), "data", "schedule.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

    print("finish allocate")




def _to_time(hhmm):
    h, m = map(int, hhmm.split(":"))
    return time(h, m)
