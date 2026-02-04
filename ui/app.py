from flask import Flask, render_template, redirect, session
from functools import wraps
from auth.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_TO_RANDOM_SECRET"

app.register_blueprint(auth_bp)


def login_required(role=None):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if "user" not in session:
                return redirect("/login")

            if role and session["user"]["role"] != role:
                return "Forbidden", 403

            return func(*args, **kwargs)
        return decorated
    return wrapper


@app.route("/")
@login_required()
def dashboard():
    return render_template("index.html", user=session["user"])


@app.route("/notifications")
@login_required(role="ADMIN")
def notifications():
    return render_template("notifications.html")


def run_ui():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,        # ⛔ WAJIB FALSE
        use_reloader=False # ⛔ WAJIB FALSE
    )


if __name__ == "__main__":
    run_ui()
