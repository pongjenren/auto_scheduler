from flask import Flask
from flask_cors import CORS

# 載入 Blueprints
from blueprints.schedule import schedule_bp
from blueprints.tasks import tasks_bp
from blueprints.settings import settings_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["JSON_AS_ASCII"] = False  # 確保傳回中文不亂碼
    CORS(app)

    # 註冊藍圖
    app.register_blueprint(schedule_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(settings_bp)

    @app.route("/")
    def index():
        from flask import redirect
        return redirect("/schedule/")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
