# Session = database transaction context
# Passed from get_db() (dependency injection)
from  sqlalchemy.orm import Session
#ORM models: Email → parent table, Task → child table
from app.database.models import Email, Task
from app.routes import emails
from app.services.ai_service import (summarize_email,extract_tasks,detect_urgency)


def process_and_store_emails(db: Session):
    emails = [
        {
            "from": "manager@company.com",
            "subject": "Project deadline",
            "body": "Please complete the dashboard by Friday and send a status update by Thursday evening."
        },
        {
            "from": "hr@company.com",
            "subject": "Policy Update",
            "body": "Hi team,Hope you're doing well.As discussed in yesterday’s meeting, please complete the dashboard by Friday.Let me know if you face blockers.Thanks,Manager"
        }
    ]

    saved_emails = []

    for email in emails:
        summary = summarize_email(email["body"])
        tasks = extract_tasks(email["body"])
        urgency = detect_urgency(email["body"])

        email_obj = Email(
            from_email=email["from"],
            subject=email["subject"],
            body=email["body"],
            summary=summary,
            urgency=urgency
        )

        db.add(email_obj)
        db.commit()
        db.refresh(email_obj)

        for task_text in tasks:
            task_obj = Task(
                email_id=email_obj.id,
                task_text=task_text
            )
            db.add(task_obj)

        db.commit()
        saved_emails.append(email_obj)

    # ✅ return AFTER loop finishes
    return saved_emails
    # return saved_emails # ❌ incorrect placement before now fix
     
def get_stored_emails(db: Session):
    return db.query(Email).all()
