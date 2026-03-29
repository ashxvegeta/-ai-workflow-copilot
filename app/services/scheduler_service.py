import os
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from app.services.gmail_service import fetch_unread_emails
from app.services.email_service import process_and_store_emails
from app.schemas.email_schema import EmailCreate
from app.database.db import SessionLocal

load_dotenv()


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


def start_scheduler(run_immediately: bool = True):
    scheduler = BackgroundScheduler()

    interval_minutes = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "5"))

    if run_immediately:
        process_gmail_inbox()

    scheduler.add_job(
        process_gmail_inbox,
        "interval",
        minutes=interval_minutes
    )

    scheduler.start()

    print(f"Scheduler started. Checking Gmail every {interval_minutes} minutes...")
