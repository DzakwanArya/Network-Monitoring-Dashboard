from database.db_connection import get_connection

LATENCY_THRESHOLD = 200  # ms


# ==========================
# CREATE LATENCY ALERT
# ==========================
def create_latency_alert(ip, latency):
    if latency is None or latency < LATENCY_THRESHOLD:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            ip_address,
            alert_type,
            latency_ms,
            message,
            is_read
        )
        VALUES (%s, 'LATENCY', %s, %s, 0)
    """, (
        ip,
        latency,
        f"High latency detected: {latency} ms"
    ))

    conn.commit()
    cursor.close()
    conn.close()


# ==========================
# CREATE STATUS ALERT
# ==========================
def create_status_alert(ip, old_status, new_status):
    if old_status == new_status:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            ip_address,
            alert_type,
            old_status,
            status,
            message,
            is_read
        )
        VALUES (%s, 'STATUS', %s, %s, %s, 0)
    """, (
        ip,
        old_status,
        new_status,
        f"Status changed {old_status} → {new_status}"
    ))

    conn.commit()
    cursor.close()
    conn.close()


# ==========================
# GET LATEST ALERTS
# ==========================
def get_latest_alerts(limit=50):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            ip_address,
            alert_type,
            old_status,
            status,
            latency_ms,
            message,
            created_at,
            is_read
        FROM alerts
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # 🔑 KONVERSI PENTING UNTUK FRONTEND
    for r in rows:
        r["read"] = bool(r["is_read"])
        del r["is_read"]

    return rows


# ==========================
# UNREAD COUNT
# ==========================
def get_unread_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE is_read = 0
    """)

    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


# ==========================
# MARK ALERT AS READ
# ==========================
def mark_alert_as_read(alert_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alerts
        SET is_read = 1
        WHERE id = %s
    """, (alert_id,))

    conn.commit()
    cursor.close()
    conn.close()


# ==========================
# MARK ALL ALERTS AS READ
# ==========================
def mark_all_as_read():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alerts
        SET is_read = 1
        WHERE is_read = 0
    """)

    conn.commit()
    cursor.close()
    conn.close()
