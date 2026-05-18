from flask import Flask, render_template, jsonify
import psutil
import time
import socket
import platform



app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/system")
def system_page():
    return render_template("system.html")

def get_temperature():
    #placeholder while developing on mac mini
    # Rasberry Pi temperature will be added later
    return "N/A"

def get_uptime():
    boot_time = psutil.boot_time()
    current_time = time.time()

    uptime_seconds = int(current_time - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    if days > 0: 
        return f"{hours}d {hours}h {minutes}m"
    else:
        return f"{hours}h {minutes}m"
    
def get_ip_address():
    try:
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_connection.connect(("8.8.8.8", 80))

        ip_address = socket_connection.getsockname()[0]

        socket_connection.close()

        return ip_address

    except Exception:
        return "N/A"

@app.route('/api/system-usage', methods = ['GET'])
def system_usage():
     cpu_percent= psutil.cpu_percent(interval = None)
     ram_percent= psutil.virtual_memory().percent
     temp = get_temperature()
     disk_usage = psutil.disk_usage('/').percent
     uptime = get_uptime()
     process_count = len(psutil.pids())
     ip_address = get_ip_address()

     device_name = platform.node()
     system_name = platform.system()
     machine_type = platform.machine()


     return jsonify(
        cpu = cpu_percent,
        ram = ram_percent,
        temp = temp,
        disk = disk_usage,
        uptime = uptime, 
        processes = process_count, 
        ip=ip_address,
        device=device_name, 
        system=system_name, 
        machine=machine_type
        ) 



if __name__ == "__main__":
    psutil.cpu_percent(interval = None)
    app.run(debug = True)

