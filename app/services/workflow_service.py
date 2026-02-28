from app.services.notification_service import send_email_notification


def execute_action(action_type: str, email):

    if action_type == "escalate":

        print(f"[ESCALATION] Email {email.id} escalated!")

        subject = f"🚨 Escalation Alert - Email {email.id}"

        body = f"""
High urgency email detected.

From: {email.from_email}
Subject: {email.subject}
Summary: {email.summary}
        """

        send_email_notification(subject, body)

    elif action_type == "reminder":
        print(f"[REMINDER] Reminder created for Email {email.id}")

    else:
        print(f"[NO ACTION] Email {email.id}")