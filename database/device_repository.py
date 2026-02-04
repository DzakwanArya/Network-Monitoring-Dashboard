from database.db_connection import get_connection
from datetime import datetime


# ==========================
# SIMPAN STATUS TERAKHIR
# ==========================
def save_device(ip, interface_name, status, latency_ms):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO network_devices
        (ip_address, interface_name, status, latency_ms, last_seen)
        VALUES (%s, %s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            interface_name = VALUES(interface_name),
            status = VALUES(status),
            latency_ms = VALUES(latency_ms),
            last_seen = NOW()
    """, (ip, interface_name, status, latency_ms))

    conn.commit()
    cursor.close()
    conn.close()



# ==========================
# SIMPAN HISTORY (TIMELINE)
# ==========================
def save_device_history(ip, interface_name, status, latency_ms=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO device_history
            (ip_address, interface_name, status, latency_ms, checked_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (ip, interface_name, status, latency_ms))

    conn.commit()
    cursor.close()
    conn.close()



# ==========================
# AMBIL SEMUA DEVICE
# ==========================
def get_all_devices():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ip_address, interface_name, status, latency_ms, last_seen
        FROM network_devices
        ORDER BY last_seen DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data



# ==========================
# AMBIL DEVICE BY IP
# ==========================
def get_device_by_ip(ip):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM network_devices
        WHERE ip_address = %s
    """, (ip,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result


# ==========================
# STATISTIK UP / DOWN
# ==========================
def get_device_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM network_devices
        GROUP BY status
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    stats = {"UP": 0, "DOWN": 0}
    for status, count in rows:
        stats[status] = count

    return stats


# ==========================
# HISTORY (API)
# ==========================
def get_device_history(limit=100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ip_address, interface_name, status, latency_ms, checked_at
        FROM device_history
        ORDER BY checked_at DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return data

