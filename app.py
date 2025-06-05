from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if not session.get("uid"):
        return redirect("/login")
    return render_template("index.html", qr_generated=False)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/session-login", methods=["POST"])
def session_login():
    uid = request.json.get("uid")
    session["uid"] = uid
    return "Logged in"

@app.route("/logout")
def logout():
    session.pop("uid", None)
    return redirect("/login")

# 🔽 THIS IS WHERE YOU HAD THE ERROR
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
