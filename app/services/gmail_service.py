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

def fetch_unread_emails(limit: int = 10, unseen_only: bool = True):
    mail = connect_gmail()

    mail.select("inbox")

    criteria = "UNSEEN" if unseen_only else "ALL"
    status, messages = mail.search(None, criteria)

    email_ids = messages[0].split()

    emails = []

    for eid in email_ids[-limit:]:  # latest emails by ID
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
                            payload = part.get_payload(decode=True)
                            if payload is not None:
                                body = payload.decode(errors="replace")
                            break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload is not None:
                        body = payload.decode(errors="replace")

                emails.append({
                    "from_email": from_email,
                    "subject": subject,
                    "body": body
                })

    mail.logout()

    return emails
