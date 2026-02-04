from core.interface_detector import detect_network
from core.ip_range_generator import generate_ip_range
from core.ping_scanner import scan_ip_range


def monitoring_job():
    interfaces = detect_network()

    for iface in interfaces:
        subnet = f"{iface['subnet']}/{iface['cidr']}"
        print(f"[SCAN] {iface['interface']} {subnet}")

        ip_range = generate_ip_range(subnet)

        # 🔥 INI SAJA
        scan_ip_range(ip_range, iface["interface"])

        print("🔥 MONITORING JOB RUNNING 🔥")

    print("[✓] Monitoring cycle complete")
