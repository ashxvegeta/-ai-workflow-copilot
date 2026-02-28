# Session = database transaction context
# Passed from get_db() (dependency injection)
from  sqlalchemy.orm import Session
#ORM models: Email → parent table, Task → child table
from app.database.models import Email, Task
from app.routes import emails
from app.schemas.email_schema import EmailCreate
from app.services.ai_service import (summarize_email,extract_tasks,detect_urgency)
from app.services.action_service import decide_action
from app.database.models import EmailAction
from app.services.action_service import decide_action
from app.services.workflow_service import execute_action


def process_and_store_emails(db: Session, email: EmailCreate):

    # 1️⃣ AI processing
    summary = summarize_email(email.body)
    tasks = extract_tasks(email.body)
    urgency = detect_urgency(email.body)
    action_type = decide_action(urgency, tasks)

    print("DECIDED ACTION:", action_type)

    # 2️⃣ Save Email
    email_obj = Email(
        from_email=email.from_email,
        subject=email.subject,
        body=email.body,
        summary=summary,
        urgency=urgency
    )

    db.add(email_obj)
    db.commit()
    db.refresh(email_obj)

    print("EMAIL STORED WITH ID:", email_obj.id)

    # 3️⃣ Save Tasks
    for task_text in tasks:
        task_obj = Task(
            email_id=email_obj.id,
            task_text=task_text
        )
        db.add(task_obj)

    db.commit()

    # 4️⃣ Execute Action (SIMPLE)
    execute_action(action_type, email_obj)

    return email_obj


def get_stored_emails(db: Session):
    emails = db.query(Email).all()
    for email in emails:
        # Fetch the latest action from the related table
        action_record = db.query(EmailAction).filter(EmailAction.email_id == email.id).first()
        email.action = action_record.action_type if action_record else "none"
    return emails
