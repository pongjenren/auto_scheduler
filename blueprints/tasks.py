import uuid
from flask import Blueprint, jsonify, request, render_template

from storage.json_store import load_tasks, save_tasks

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/", methods=["GET"])
def task_list():
    """Task 頁面 HTML。可透過 query 參數 sort / filter。"""
    sort_key = request.args.get("sort", "title")
    status = request.args.get("status")  # optional filter

    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    tasks.sort(key=lambda x: x.get(sort_key, ""))

    return render_template("tasks.html", tasks=tasks, sort_key=sort_key, status=status)


@tasks_bp.route("/", methods=["POST"])
def add_task():
    """新增一筆 task（JSON API）。"""
    data = request.get_json()
    new_task = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "est_hours": float(data["est_hours"]),
        "due_date": data.get("due_date", ""),
        "color": data.get("color", "#2196f3"),  # 預設藍色
        "status": "todo",
    }
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify({"ok": True, "task": new_task}), 201


@tasks_bp.route("/<task_id>", methods=["PATCH"])
def update_task(task_id):
    """更新 task（例如變更 status）。"""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t.update(request.get_json())
            break
    save_tasks(tasks)
    return jsonify({"ok": True})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = [t for t in load_tasks() if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"ok": True})
