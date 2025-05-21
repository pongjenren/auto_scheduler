# scheduler/allocator.py
from datetime import datetime, timedelta, time
from collections import defaultdict

def allocate(tasks, settings, horizon_days=4):
    """極簡：將 TODO task FIFO 填入 work_slots，跨日不拆段。"""
    tasks = [t for t in tasks if t["status"] != "done"]
    plan = defaultdict(list)
    today = datetime.today().date()

    # 預先根據設定產生所有 slots
    slots = []
    for i in range(horizon_days):
        cur = today + timedelta(days=i)
        weekday = cur.weekday()  # Mon=0
        for slot in settings["work_slots"]:
            if slot["weekday"] == weekday:
                start_t = datetime.combine(cur, _to_time(slot["start"]))
                end_t = datetime.combine(cur, _to_time(slot["end"]))
                slots.append({"date": cur, "start": start_t, "end": end_t})

    # FIFO 填入
    for task in tasks:
        need = task["est_hours"]
        for slot in slots:
            avail_hours = (slot["end"] - slot["start"]).seconds / 3600
            if avail_hours >= need and "task" not in slot:
                slot["task"] = task
                plan[slot["date"].isoformat()].append({
                    "start": slot["start"].strftime("%H:%M"),
                    "end": slot["end"].strftime("%H:%M"),
                    "task": task,
                })
                break
    # 依時間排序
    for day in plan:
        plan[day].sort(key=lambda x: x["start"])
    return plan

def _to_time(hhmm):
    h, m = map(int, hhmm.split(":"))
    return time(h, m)
