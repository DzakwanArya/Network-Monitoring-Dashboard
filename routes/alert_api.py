from flask import Blueprint, jsonify
from database.db_connection import get_connection

alert_api = Blueprint("alert_api", __name__)

@alert_api.route("/api/alerts")
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM alert_logs
        ORDER BY created_at DESC
        LIMIT 10
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)


@alert_api.route("/api/alerts/unread-count")
def unread_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM alert_logs WHERE is_read = FALSE
    """)

    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return jsonify({"count": count})
