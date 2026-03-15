from app.services.gmail_service import connect_gmail, fetch_unread_emails
from app.database.db import SessionLocal, engine
import sqlite3
from app.database.models import Base
from app.schemas.email_schema import EmailCreate
from app.services.email_service import process_and_store_emails

# Ensure tables exist when running this script directly.
Base.metadata.create_all(bind=engine)

# Toggle this when you want a fresh DB run.
CLEAR_DB = False
if CLEAR_DB:
    con = sqlite3.connect("ai_workflow.db")
    cur = con.cursor()
    cur.execute("DELETE FROM tasks")
    cur.execute("DELETE FROM email_actions")
    cur.execute("DELETE FROM emails")
    con.commit()
    con.close()

mail = connect_gmail()
# Scan a larger window to find 10 work-relevant emails.
emails = fetch_unread_emails(limit=100, unseen_only=False)

db = SessionLocal()

saved = 0
for email in emails:

    email_schema = EmailCreate(
        from_email=email["from_email"],
        subject=email["subject"],
        body=email["body"],
        message_id=email.get("message_id")
    )

    result = process_and_store_emails(db, email_schema)
    if result is not None:
        saved += 1
        if saved >= 10:
            break

db.close()
