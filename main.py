from api.app import app
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import monitoring_job

# ==========================
# INIT SCHEDULER (NON-BLOCKING)
# ==========================
scheduler = BackgroundScheduler(
    daemon=True   # penting agar mati saat Flask mati
)

scheduler.add_job(
    monitoring_job,
    "interval",
    minutes=1,        # scan tiap 1 menit
    max_instances=1,  # cegah job numpuk
    coalesce=True     # gabung job yang tertinggal
)

scheduler.start()
print("📡 Network Monitoring Scheduler started...")

# ==========================
# RUN FLASK
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
        use_reloader=False  # ⚠️ WAJIB (hindari scheduler double)
    )
