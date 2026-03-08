import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def connect_gmail():

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail

def fetch_unread_emails():
    mail = connect_gmail()

    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")

    email_ids = messages[0].split()

    emails = []

    for eid in email_ids[:5]:  # limit 5 emails
        status, msg_data = mail.fetch(eid, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject = msg["subject"]
                from_email = msg["from"]

                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()

                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                emails.append({
                    "from_email": from_email,
                    "subject": subject,
                    "body": body
                })

    mail.logout()

    return emails
