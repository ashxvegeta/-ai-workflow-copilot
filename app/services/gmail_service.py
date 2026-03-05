import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def connect_gmail():
    """
    Connect to Gmail using IMAP.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        print("✅ Connected to Gmail successfully")
        return mail
    except Exception as e:
        print("❌ Gmail connection failed:", e)
        return None