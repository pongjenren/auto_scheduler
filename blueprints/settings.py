from flask import Blueprint, render_template, request, jsonify
from storage.json_store import load_settings, save_settings

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/", methods=["GET"])
def settings_view():
    """顯示工作時段設定頁。"""
    return render_template("settings.html", settings=load_settings())


@settings_bp.route("/", methods=["PUT"])
def update_settings():
    """更新可用時間段（整筆覆寫）。"""
    data = request.get_json()
    # 預期格式: { "work_slots": [ { "weekday": 0, "start": "09:00", "end": "12:00" }, ... ] }
    save_settings(data)
    return jsonify({"ok": True})
