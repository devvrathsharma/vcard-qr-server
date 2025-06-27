from flask import Flask, render_template, request, session, redirect, send_from_directory, url_for
from flask_session import Session
from flask_mail import Mail, Message
import os
import secrets

app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Email config (replace with real credentials)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',
    MAIL_PASSWORD='your_app_password'
)

mail = Mail(app)

# In-memory user store (for demo; use DB in production)
users = {}

@app.route("/")
def index():
    if not session.get("uid"):
        return redirect("/login")
    return render_template("index.html", qr_generated=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users.get(email)
        if user and user.get("password") == password:
            session["uid"] = email
            return redirect("/")
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        email = request.form["email"]
        token = secrets.token_urlsafe(32)
        users[email] = {"first": first, "last": last, "token": token}

        reset_link = url_for("set_password", token=token, _external=True)

        msg = Message(
            subject="Welcome to vCard QR App!",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
            body=f"""
Hi {first},

Thanks for signing up!

Your username is: {email}
Please click the link below to set your password:
{reset_link}

Regards,
vCard QR Team
            """
        )
        mail.send(msg)
        return "Signup successful. Please check your email to complete registration."
    return render_template("signup.html")

@app.route("/set-password", methods=["GET", "POST"])
def set_password():
    if request.method == "GET":
        return render_template("set_password.html", token=request.args.get("token"))
    token = request.form["token"]
    password = request.form["password"]
    for email, user in users.items():
        if user.get("token") == token:
            user["password"] = password
            return "Password set! <a href='/login'>Login</a>"
    return "Invalid token"

@app.route("/session-login", methods=["POST"])
def session_login():
    uid = request.json.get("uid")
    session["uid"] = uid
    return "Logged in"

@app.route("/logout")
def logout():
    session.pop("uid", None)
    return redirect("/login")

@app.route("/vcard.html")
def serve_vcard():
    return send_from_directory("static", "vcard.html")

@app.route("/login.html")
def serve_login_html():
    return send_from_directory("static", "login.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
