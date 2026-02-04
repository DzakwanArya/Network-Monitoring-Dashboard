from flask import Flask, jsonify
from flask_cors import CORS

from database.device_repository import get_all_devices, get_device_stats
from database.db_connection import get_connection

from api.alert_api import alert_api
# from api.device_api import device_api  # kalau nanti dipisah

app = Flask(__name__)
CORS(app)

# ==========================
# REGISTER BLUEPRINT
# ==========================
app.register_blueprint(alert_api)
# app.register_blueprint(device_api)

# ==========================
# DEVICES (STATUS TERAKHIR)
# ==========================
@app.route("/api/devices")
def devices():
    print('[API] GET /api/devices')
    data = get_all_devices()

    # optional limit param to reduce payload for UI
    from flask import request
    limit = request.args.get('limit')
    try:
        if limit:
            limit = int(limit)
            data = data[:limit]
    except Exception:
        pass

    print(f"[API] /api/devices -> {len(data)} rows (limit={limit})")
    return jsonify(data)

# ==========================
# STATS (UP / DOWN)
# ==========================
@app.route("/api/stats")
def stats():
    return jsonify(get_device_stats())

# ==========================
# DEVICE HISTORY
# ==========================
@app.route("/api/history")
def device_history():
    print('[API] GET /api/history')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ip_address, status, latency_ms, checked_at
        FROM device_history
        ORDER BY checked_at DESC
        LIMIT 100
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"[API] /api/history -> {len(data)} rows")
    return jsonify(data)


# ==========================
# HEALTH
# ==========================
@app.route("/api/health")
def health():
    print('[API] GET /api/health')
    return jsonify({"status":"ok"})

# ==========================
# LATENCY HISTORY
# ==========================
@app.route("/api/latency/<ip>")
def latency_history(ip):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT latency_ms, checked_at
        FROM device_history
        WHERE ip_address = %s AND latency_ms IS NOT NULL
        ORDER BY checked_at DESC
        LIMIT 50
    """, (ip,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)

# ==========================
# RUN SERVER
# ==========================
if __name__ == "__main__":
    app.run(port=5001, debug=True)
