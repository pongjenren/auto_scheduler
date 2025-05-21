# storage/json_store.py
import json, os, pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"
BASE_DIR.mkdir(exist_ok=True)

def _read(path, default):
    if not path.exists():
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2))
    return json.loads(path.read_text())

def _write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2))

def load_tasks():
    return _read(BASE_DIR / "tasks.json", [])

def save_tasks(tasks):
    _write(BASE_DIR / "tasks.json", tasks)

def load_settings():
    return _read(BASE_DIR / "settings.json", { "work_slots": [] })

def save_settings(settings):
    _write(BASE_DIR / "settings.json", settings)
