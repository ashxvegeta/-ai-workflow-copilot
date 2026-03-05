from services.gmail_service import connect_gmail, fetch_unread_emails

mail = connect_gmail()
emails = fetch_unread_emails()
for email in emails:
    print(email)