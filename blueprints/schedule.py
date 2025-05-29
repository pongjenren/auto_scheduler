from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request
import os
import time

from storage.json_store import load_tasks, load_settings, save_tasks
from scheduler.allocator import allocate

schedule_bp = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule_bp.route("/", methods=["GET"])
def schedule_view():
    """顯示未來四天排程（HTML），所有日期運算於後端完成。"""
    from datetime import timedelta
    import json
    today = datetime.today().date()
    # 產生未來四天的日期字串與標題
    date_list = []
    for i in range(4):
        d = today + timedelta(days=i)
        date_list.append({
            'date': d.strftime('%Y-%m-%d'),
            'label': d.strftime('%m/%d (%a)')
        })
    
    # 讀取 schedule.json
    schedule_path = os.path.join(os.getcwd(), "data", "schedule.json")
    schedule_data = []
    if os.path.exists(schedule_path):
        with open(schedule_path, "r", encoding="utf-8") as f:
            schedule_data = json.load(f)
    
    # 讀取 tasks.json 以取得顏色
    tasks_path = os.path.join(os.getcwd(), "data", "tasks.json")
    task_colors = {}
    if os.path.exists(tasks_path):
        with open(tasks_path, "r", encoding="utf-8") as f:
            for t in json.load(f):
                task_colors[t["id"]] = t.get("color", "#2196f3")
    
    # 讀取 available_slots.json，建立未來四天的不可用 slots list
    available_slots_path = os.path.join(os.getcwd(), "data", "available_slots.json")
    unavailable_slots = {d['date']: [] for d in date_list}
    if os.path.exists(available_slots_path):
        with open(available_slots_path, "r", encoding="utf-8") as f:
            slots_data = json.load(f)

        for i in range(today.weekday(), today.weekday() + 4):
            for hr in range(8, 24):
                if not any(slot['day'] == i and slot['hour'] == hr for slot in slots_data):
                    # 如果沒有對應的可用時段，則加入不可用時段
                    unavailable_slots[(today + timedelta(days=i - today.weekday())).strftime('%Y-%m-%d')].append(hr)

        # 將 unavailable_slots 轉為 JSON 並儲存到 data/unavailable_slots.json
        output_path = os.path.join(os.getcwd(), "data", "unavailable_slots.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(unavailable_slots, f, ensure_ascii=False, indent=2)

    return render_template("schedule.html", schedule_data=schedule_data, task_colors=task_colors, date_list=date_list, unavailable_slots=unavailable_slots)


@schedule_bp.route("/refresh", methods=["GET"])
def schedule_json():
    """重新排程並回傳 JSON（前端 AJAX 用），同時回傳 HTML 片段。"""
    allocate()
    # 直接渲染 schedule.html 的內容片段
    today = datetime.today().date()
    # 只渲染內容部分
    from flask import render_template_string
    from jinja2 import Template
    import json
    # 取得 schedule.html 的內容
    with open(os.path.join(os.path.dirname(__file__), '../templates/schedule.html'), encoding='utf-8') as f:
        tpl = f.read()
    # 只渲染 row 內容
    # 這裡直接回傳 JSON，前端 reload 整頁即可

    return 0
