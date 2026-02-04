import subprocess
import platform
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from database.device_repository import (
    save_device,
    save_device_history,
    get_device_by_ip
)
from scheduler.alert import check_status_change, check_latency


# ==========================
# PING 1 IP + LATENCY
# ==========================
def ping_ip(ip: str):
    is_windows = platform.system().lower() == "windows"
    param = "-n" if is_windows else "-c"
    command = ["ping", param, "1", ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=3
        )
    except Exception:
        return False, None

    if result.returncode != 0:
        return False, None

    latency = None

    if is_windows:
        match = re.search(r"time[=<]\s*(\d+)\s*ms", result.stdout)
    else:
        match = re.search(r"time=\s*(\d+\.?\d*)\s*ms", result.stdout)

    if match:
        latency = int(float(match.group(1)))

    return True, latency


# ==========================
# SCAN IP LIST (MULTITHREAD)
# ==========================
def scan_ips(ip_list, interface_name="Wi-Fi", max_threads=50):
    active_ips = []

    def scan_single_ip(ip):
        try:
            old = get_device_by_ip(ip)

            is_up, latency = ping_ip(ip)
            status = "UP" if is_up else "DOWN"

            # Simpan status & history
            save_device(ip, interface_name, status, latency)
            save_device_history(ip, interface_name, status, latency)

            # 🔔 ALERT STATUS (UP/DOWN)
            if old:
                check_status_change(old["status"], status, ip)

            # 🔔 ALERT LATENCY (HANYA JIKA UP & ADA LATENCY)
            if is_up and latency is not None:
                check_latency(ip, latency)

            return ip if is_up else None

        except Exception as e:
            print(f"[ERROR] {ip}: {e}")
            return None

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_single_ip, ip) for ip in ip_list]

        for future in as_completed(futures):
            result = future.result()
            if result:
                active_ips.append(result)

    return active_ips


# ==========================
# ALIAS UNTUK SCHEDULER
# ==========================
def scan_ip_range(ip_range, interface_name="Wi-Fi"):
    return scan_ips(ip_range, interface_name)


# ==========================
# TEST MANUAL
# ==========================
if __name__ == "__main__":
    from core.ip_range_generator import generate_ip_range

    subnet = "192.168.101.0/24"
    ip_range = generate_ip_range(subnet)

    print(f"🔍 Scanning {len(ip_range)} IPs...")
    active_ips = scan_ip_range(ip_range)

    print("✅ IP AKTIF:")
    for ip in active_ips:
        print(ip)
