# app/services/action_service.py

def decide_action(urgency: str, tasks: list[str]) -> str:
    """
    Decide what action to take for an email.
    """

    if urgency == "high":
        return "escalate"

    if tasks:
        return "reminder"

    return "none"
