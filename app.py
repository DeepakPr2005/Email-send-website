from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# 🔐 Use Gmail App Password
SENDER_EMAIL = "deepak2005prajapat@gmail.com"
APP_PASSWORD = "jrjtusjutjicelvn"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect("sent_mails.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            subject TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- SAVE MAIL ----------------
def save_mail(email, subject):
    conn = sqlite3.connect("sent_mails.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mails (email, subject) VALUES (?, ?)",
        (email, subject)
    )
    conn.commit()
    conn.close()

# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        hr_email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        file = request.files["resume"]

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = hr_email
        msg["Subject"] = subject
        msg.set_content(message)

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=filename
            )

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        save_mail(hr_email, subject)
        return redirect(url_for("success"))

    return render_template("index.html")

# ---------------- SUCCESS ----------------
@app.route("/success")
def success():
    return render_template("success.html")

# ---------------- SENT MAILS ----------------
@app.route("/mails")
def mails():
    conn = sqlite3.connect("sent_mails.db")
    cur = conn.cursor()
    cur.execute("SELECT email, subject FROM mails ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("mails.html", mails=data)

if __name__ == "__main__":
    app.run(debug=True)
