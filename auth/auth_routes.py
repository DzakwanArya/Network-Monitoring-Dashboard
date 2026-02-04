from flask import Blueprint, render_template, request, redirect, session
from auth.auth_repository import find_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = find_user(
            request.form["username"],
            request.form["password"]
        )

        if user:
            session["user"] = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            return redirect("/")
        return render_template("login.html", error="Login gagal")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
