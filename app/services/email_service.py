from app.services.ai_service import summarize_email

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
            "body": "Please review the updated work from home policy."
        }
    ]
    
    for email in emails:
        email["summary"] = summarize_email(email["body"])
    return emails
