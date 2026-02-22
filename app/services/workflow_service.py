def execute_action(action_type: str, email):
    if action_type == "escalate":
        print(f"[ESCALATION] Email {email.id} escalated!")

    elif action_type == "reminder":
        print(f"[REMINDER] Reminder created for Email {email.id}")

    else:
        print(f"[NO ACTION] Email {email.id}")