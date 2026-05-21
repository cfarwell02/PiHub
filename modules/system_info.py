import psutil
import time
import socket
import platform


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
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_connection:
            socket_connection.connect(("8.8.8.8", 80))
            return socket_connection.getsockname()[0]

    except Exception:
        return "N/A"

def get_system_stats():
     cpu_percent= psutil.cpu_percent(interval = None)
     ram_percent= psutil.virtual_memory().percent
     disk_percent = psutil.disk_usage('/').percent
     process_count = len(psutil.pids())


     return {
        "cpu": cpu_percent,
        "ram": ram_percent,
        "temp": get_temperature(),
        "disk": disk_percent,
        "uptime": get_uptime(), 
        "processes": process_count, 
        "ip": get_ip_address(),
        "device": platform.node(), 
        "system": platform.system(), 
        "machine": platform.machine()
     }
