import smtplib
from email.message import EmailMessage
import os


def send_email_notification(subject: str, body: str):

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    receiver_email = os.getenv("ALERT_RECEIVER")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "workflow@app.com"
    msg["To"] = receiver_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email sending failed:", str(e))