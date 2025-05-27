import json
import os
from flask import Blueprint, render_template, request, jsonify
import pathlib
from storage.json_store import load_settings, save_settings

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/", methods=["GET"])
def settings_view():
    """顯示可用時段設定頁，並讀取顏色列表與可用時段。"""
    # 顏色
    color_path = os.path.join(os.getcwd(), "data", "color.json")
    colors = []
    try:
        with open(color_path, "r", encoding="utf-8") as f:
            colors = json.load(f)
    except Exception as e:
        print("Error loading color.json:", e)
    # 可用時段
    available_path = os.path.join(os.getcwd(), "data", "available_slots.json")
    available_slots = []
    if os.path.exists(available_path):
        try:
            with open(available_path, "r", encoding="utf-8") as f:
                available_slots = json.load(f)
        except Exception as e:
            print("Error loading available_slots.json:", e)
    return render_template("settings.html", colors=colors, available_slots=available_slots)



# 新增：儲存可用時段
@settings_bp.route("/available_slots", methods=["POST"])
def save_available_slots():
    """儲存可用時段到 available_slots.json"""
    data = request.get_json()
    slots = data.get("available_slots", [])
    available_path = os.path.join(os.getcwd(), "data", "available_slots.json")
    try:
        with open(available_path, "w", encoding="utf-8") as f:
            json.dump(slots, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error saving available_slots.json:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


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
