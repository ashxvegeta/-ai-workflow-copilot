from app.services.gmail_service import connect_gmail, fetch_unread_emails
from app.database.db import SessionLocal, engine
from app.database.models import Base
from app.schemas.email_schema import EmailCreate
from app.services.email_service import process_and_store_emails

# Ensure tables exist when running this script directly.
Base.metadata.create_all(bind=engine)

mail = connect_gmail()
emails = fetch_unread_emails()

db = SessionLocal()

for email in emails:

    email_schema = EmailCreate(
        from_email=email["from_email"],
        subject=email["subject"],
        body=email["body"]
    )

    process_and_store_emails(db, email_schema)

db.close()
