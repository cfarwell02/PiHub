import psutil
import time
import socket
import platform
import os
import subprocess

boot_time = time.time() - psutil.boot_time()

def get_temperature():
    
    try: 
        temps = psutil.sensors_temperatures()

        if temps: 
            for sensor_name in temps:
                if temps[sensor_name]:
                    temp = temps[sensor_name][0].current
                    return round(temp, 1)
    except:
        pass


    try:
        result = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        temp = result.replace("temp=", "").replace("'C", "").strip()
        return round(float(temp), 1)
    
    except:
        pass

    return "Unavailable"

def get_uptime():
    seconds = int(time.time() - psutil.boot_time())

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0: 
        return f"{days}d {hours}h {minutes}m"
    else:
        return f"{hours}h {minutes}m"
    
def get_ip_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_connection:
            socket_connection.connect(("8.8.8.8", 80))
            return socket_connection.getsockname()[0]

    except Exception:
        return "N/A"
    
def format_temperature(temp_celsius, temp_unit="C"):
    if temp_celsius == "Unavailable":
        return "Unavailable"

    if temp_unit == "F":
        temp_fahrenheit = (temp_celsius * 9 / 5) + 32
        return f"{round(temp_fahrenheit, 1)}°F"

    return f"{temp_celsius}°C"

def get_system_stats(temp_unit="C"):
     cpu_percent= psutil.cpu_percent(interval = None)
     ram_percent= psutil.virtual_memory().percent
     disk_percent = psutil.disk_usage('/').percent
     process_count = len(psutil.pids())


     return {
        "cpu": cpu_percent,
        "ram": ram_percent,
        "temp": format_temperature(get_temperature(), temp_unit),
        "disk": disk_percent,
        "uptime": get_uptime(), 
        "processes": process_count, 
        "ip": get_ip_address(),
        "device": platform.node(), 
        "system": platform.system(), 
        "machine": platform.machine()
     }
def get_expanded_system_details():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Unavailable",
        "python_version": platform.python_version(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "total_ram_gb": round(memory.total / (1024 ** 3), 2),
        "available_ram_gb": round(memory.available / (1024 ** 3), 2),
        "total_disk_gb": round(disk.total / (1024 ** 3), 2),
        "free_disk_gb": round(disk.free / (1024 ** 3), 2),
        "boot_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time())),
        "current_user": os.environ.get("USER") or os.environ.get("USERNAME") or "Unavailable"
    }
