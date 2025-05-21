from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request

from storage.json_store import load_tasks, load_settings, save_tasks
from scheduler.allocator import allocate

schedule_bp = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule_bp.route("/", methods=["GET"])
def schedule_view():
    """顯示未來四天排程（HTML）。"""
    tasks = load_tasks()
    settings = load_settings()
    plan = allocate(tasks, settings)
    today = datetime.today().date()
    return render_template("schedule.html", plan=plan, today=today, timedelta=timedelta)


@schedule_bp.route("/refresh", methods=["GET"])
def schedule_json():
    """重新排程並回傳 JSON（前端 AJAX 用）。"""
    tasks = load_tasks()
    settings = load_settings()
    new_plan = allocate(tasks, settings)
    return jsonify(new_plan)
