import json
import os
from flask import Blueprint, render_template, request, jsonify
from storage.json_store import load_settings, save_settings

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/", methods=["GET"])
def settings_view():
    """顯示工作時段設定頁，並讀取顏色列表。"""
    settings_data = load_settings()
    json_path = os.path.join(os.getcwd(), "data", "color.json")
    colors = []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            colors = json.load(f)
    except Exception as e:
        print("Error loading color.json:", e)
    return render_template("settings.html", settings=settings_data, colors=colors)


@settings_bp.route("/", methods=["PUT"])
def update_settings():
    """
    更新工作時段及忙碌時段設定（整筆覆寫）。
    預期格式:
    {
      "work_slots": [ { "weekday": 0, "start": "09:00", "end": "12:00" }, ... ],
      "busy_slot": [ { "day": 1, "hour": 9 }, ... ]
    }
    """
    data = request.get_json()
    # 假設 data/settings.json 結構中有 "work_slots" 與 "busy_slot"
    save_settings(data)  # 請確保 save_settings 可處理 "busy_slot"
    return jsonify({"ok": True})


@settings_bp.route("/colors", methods=["POST"])
def save_colors():
    """儲存顏色列表到 JSON 檔案。"""
    try:
        data = request.get_json()
        print("Received color data:", data)  # Debug 輸出
        colors = data.get("colors", [])
        json_path = os.path.join(os.getcwd(), "data", "color.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(colors, f, ensure_ascii=False, indent=2)
        print("Successfully saved colors to:", json_path)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error saving colors:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
