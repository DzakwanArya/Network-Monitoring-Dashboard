from flask import Blueprint, jsonify
from database.alert_repository import (
    get_latest_alerts,
    get_unread_count,
    mark_alert_as_read
)

alert_api = Blueprint(
    "alert_api",
    __name__,
    url_prefix="/api/alerts"
)

# ==========================
# GET ALL ALERTS
# ==========================
@alert_api.route("/", methods=["GET"])
def list_alerts():
    print('[API] GET /api/alerts')
    data = get_latest_alerts()
    print(f"[API] /api/alerts -> {len(data)} alerts")
    return jsonify(data)


@alert_api.route("/<int:alert_id>/read", methods=["POST"])
def read_alert(alert_id):
    print(f"[API] POST /api/alerts/{alert_id}/read")
    mark_alert_as_read(alert_id)
    return jsonify({"status":"ok"})


@alert_api.route("/unread-count", methods=["GET"])
def unread_count():
    print('[API] GET /api/alerts/unread-count')
    count = get_unread_count()
    print(f"[API] /api/alerts/unread-count -> {count}")
    return jsonify({
        "unread": count
    })


@alert_api.route("/read-all", methods=["POST"])
def read_all():
    print('[API] POST /api/alerts/read-all')
    from database.alert_repository import mark_all_as_read
    mark_all_as_read()
    return jsonify({"status":"ok"})



