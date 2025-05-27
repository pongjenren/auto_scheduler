from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request

from storage.json_store import load_tasks, load_settings, save_tasks
from scheduler.allocator import allocate

schedule_bp = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule_bp.route("/", methods=["GET"])
def schedule_view():
    """顯示未來四天排程（HTML）。不自動 allocate，僅顯示目前 plan。"""
    # 只顯示目前的 plan，不呼叫 allocate
    # 直接讀取 /schedule/refresh 的結果
    today = datetime.today().date()
    plan = {}
    try:
        # 嘗試讀取上次排程結果（如果有的話）
        # 這裡直接呼叫 allocate 但你可以改為讀取快取檔案
        # 但為了簡單，這裡先不顯示任何內容，直到按下 Scheduling Now
        pass
    except Exception:
        pass
    return render_template("schedule.html", plan=plan, today=today, timedelta=timedelta)


@schedule_bp.route("/refresh", methods=["GET"])
def schedule_json():
    """重新排程並回傳 JSON（前端 AJAX 用），同時回傳 HTML 片段。"""
    new_plan = allocate()
    # 直接渲染 schedule.html 的內容片段
    today = datetime.today().date()
    # 只渲染內容部分
    from flask import render_template_string
    from jinja2 import Template
    # 取得 schedule.html 的內容
    with open(os.path.join(os.path.dirname(__file__), '../templates/schedule.html'), encoding='utf-8') as f:
        tpl = f.read()
    # 只渲染 row 內容
    # 這裡直接回傳 JSON，前端 reload 整頁即可
    return jsonify(new_plan)
