from flask import Flask, render_template, jsonify, request
import psutil
import time
from modules.system_info import get_system_stats, get_expanded_system_details



app = Flask(__name__)

app_settings = {
    "refresh_interval": 1000,
    "temperature_unit": "C"
}

app_logs = []

def add_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    app_logs.insert(0, {
        "timestamp": timestamp,
        "message": message
    })

    if len(app_logs) > 50:
        app_logs.pop()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/system")
def system_page():
    return render_template("system.html")

@app.route("/api/system-usage", methods=["GET"])
def system_usage():
    return jsonify(get_system_stats(app_settings["temperature_unit"]))

@app.route("/api/system-details", methods=["GET"])
def system_details():
    return jsonify(get_expanded_system_details())

@app.route("/settings")
def settings_page():
    return render_template("settings.html", settings=app_settings)


@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(app_settings)


@app.route("/api/settings", methods=["POST"])
def save_settings():
    data = request.get_json()

    refresh_interval = int(data.get("refresh_interval", 1000))
    temperature_unit = data.get("temperature_unit", "C")

    app_settings["refresh_interval"] = refresh_interval
    app_settings["temperature_unit"] = temperature_unit

    add_log(f"Settings updated: refresh interval {refresh_interval}ms, temperature unit {temperature_unit}")

    return jsonify({
        "success": True,
        "settings": app_settings
    })

@app.route("/logs")
def logs_page():
    return render_template("logs.html")


@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(app_logs)

@app.route("/api/logs", methods=["POST"])
def create_log():
    data = request.get_json()
    message = data.get("message", "Unknown event")

    add_log(message)

    return jsonify({
        "success": True
    })

if __name__ == "__main__":
    psutil.cpu_percent(interval=None)
    add_log("PiHub started")
    app.run(debug=True)

