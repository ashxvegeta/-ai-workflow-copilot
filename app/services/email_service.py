# Session = database transaction context
# Passed from get_db() (dependency injection)
from  sqlalchemy.orm import Session
#ORM models: Email → parent table, Task → child table
from app.database.models import Email, Task
# from app.routes import emails
from app.schemas.email_schema import EmailCreate
from app.services.ai_service import (summarize_email,extract_tasks,detect_urgency,classify_email_type)
from app.services.action_service import decide_action
from app.database.models import EmailAction
from app.services.action_service import decide_action
from app.services.workflow_service import execute_action


def process_and_store_emails(db: Session, email: EmailCreate):

    # 1️⃣ AI processing
    summary = summarize_email(email.body)

    sender = email.from_email.lower()
    if "google.com" in sender or "googleplay" in sender or "no-reply" in sender:
        print("SKIPPED SYSTEM EMAIL")
        return None

    email_type = classify_email_type(email.body)

    if email_type != "work":
        print("SKIPPED NON-WORK EMAIL")
        return None

    tasks = extract_tasks(email.body)

    urgency = detect_urgency(email.body)

    action_type = decide_action(urgency, tasks)

    print("EMAIL TYPE:", email_type)
    print("DECIDED ACTION:", action_type)

    # 2️⃣ Save Email
    email_obj = Email(
        from_email=email.from_email,
        subject=email.subject,
        body=email.body,
        summary=summary,
        urgency=urgency,
        email_type=email_type
    )

    db.add(email_obj)
    db.commit()
    db.refresh(email_obj)

    # 3️⃣ Save Action
    if action_type != "none":
        action_obj = EmailAction(
            email_id=email_obj.id,
            action_type=action_type
        )
        db.add(action_obj)

    # 4️⃣ Save Tasks
    for task_text in tasks:
        task_obj = Task(
            email_id=email_obj.id,
            task_text=task_text
        )
        db.add(task_obj)

    db.commit()

    # 5️⃣ Execute action
    execute_action(action_type, email_obj)

    return email_obj
     
def get_stored_emails(db: Session):
    emails = (
        db.query(Email)
        .filter(Email.email_type == "work")
        .order_by(Email.created_at.desc())
        .limit(10)
        .all()
    )
    for email in emails:
        # Fetch the latest action from the related table
        action_record = db.query(EmailAction).filter(EmailAction.email_id == email.id).first()
        email.action = action_record.action_type if action_record else "none"
    return emails
