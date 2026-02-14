# Session = database transaction context
# Passed from get_db() (dependency injection)
from  sqlalchemy.orm import Session
#ORM models: Email → parent table, Task → child table
from app.database.models import Email, Task
from app.routes import emails
from app.schemas.email_schema import EmailCreate
from app.services.ai_service import (summarize_email,extract_tasks,detect_urgency)


def process_and_store_emails(db: Session, email: EmailCreate):

        # 1️⃣ AI processing
        summary = summarize_email(email.body)
        tasks = extract_tasks(email.body)
        urgency = detect_urgency(email.body)
  

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

        # 3️⃣ Save Tasks
        for task_text in tasks:
            task_obj = Task(
                email_id=email_obj.id,
                task_text=task_text
            )
            db.add(task_obj)

        db.commit()
        return email_obj
     
def get_stored_emails(db: Session):
    return db.query(Email).all()
