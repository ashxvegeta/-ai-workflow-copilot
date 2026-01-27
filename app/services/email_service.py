from app.services.ai_service import (
    summarize_email,
    extract_tasks,
    detect_urgency
)


def get_sample_emails():
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
    
    for email in emails:
        email["summary"] = summarize_email(email["body"])
        email["tasks"] = extract_tasks(email["body"])
        email["urgency"] = detect_urgency(email["body"])
    return emails
