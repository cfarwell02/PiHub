from flask import Flask, render_template, jsonify
import psutil
from modules.system_info import get_system_stats



app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/system")
def system_page():
    return render_template("system.html")

@app.route('/api/system-usage', methods = ['GET'])
def system_usage():
     return jsonify(get_system_stats()) 


if __name__ == "__main__":
    psutil.cpu_percent(interval = None)
    app.run(debug = True)

