import time
from threading import Lock
from database.alert_repository import (
    create_status_alert,
    create_latency_alert
)

LATENCY_THRESHOLD = 150
LATENCY_COOLDOWN = 120

_last_latency_alert = {}
_latency_lock = Lock()

def check_status_change(old_status, new_status, ip):
    if old_status != new_status:
        try:
            create_status_alert(ip, old_status, new_status)
        except Exception as e:
            print(f"[STATUS ALERT ERROR] {ip}: {e}")

def check_latency(ip, latency):
    if latency is None or latency < LATENCY_THRESHOLD:
        return

    try:
        with _latency_lock:
            now = time.time()
            last_time = _last_latency_alert.get(ip, 0)

            if now - last_time < LATENCY_COOLDOWN:
                return

            create_latency_alert(ip, latency)
            _last_latency_alert[ip] = now
    except Exception as e:
        print(f"[LATENCY ALERT ERROR] {ip}: {e}")
