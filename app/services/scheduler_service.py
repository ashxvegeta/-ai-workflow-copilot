from apscheduler.schedulers.background import BackgroundScheduler
from app.services.gmail_service import fetch_unread_emails
from app.services.email_service import process_and_store_emails
from app.schemas.email_schema import EmailCreate
from app.database.db import SessionLocal


def process_gmail_inbox():
    print("Checking Gmail for new emails...")

    emails = fetch_unread_emails()

    db = SessionLocal()

    for email_data in emails:

        email_schema = EmailCreate(
            from_email=email_data["from_email"],
            subject=email_data["subject"],
            body=email_data["body"]
        )

        process_and_store_emails(db, email_schema)

    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        process_gmail_inbox,
        "interval",
        minutes=5
    )

    scheduler.start()

    print("Scheduler started. Checking Gmail every 5 minutes...")