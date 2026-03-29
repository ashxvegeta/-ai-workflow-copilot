# AI Email Workflow Copilot

## What This Project Does
This project turns raw Gmail emails into structured, actionable work items.

**Pipeline:**
Gmail → Fetch → AI Understand → Extract Tasks → Decide Action → Store → Execute → API

## End-to-End Flow (File-by-File)

1. **Fetch Emails**
   - File: `app/services/gmail_service.py`
   - Connects to Gmail via IMAP
   - Pulls latest emails (configurable limit / UNSEEN vs ALL)
   - Extracts `from`, `subject`, `body`, `message_id`

2. **AI Processing + Filtering**
   - File: `app/services/email_service.py`
   - Summarize email
   - Skip system senders (e.g., `no-reply`, Google)
   - Classify email type (work/personal/newsletter/promotion/spam)
   - Skip non-work emails
   - Extract tasks
   - Detect urgency
   - Decide action (reminder/escalate/none)
   - Dedupe by `message_id`
   - Save to DB
   - Execute action

3. **AI Helpers**
   - File: `app/services/ai_service.py`
   - `summarize_email`, `extract_tasks`, `detect_urgency`, `classify_email_type`

4. **Database Models**
   - File: `app/database/models.py`
   - Tables: `Email`, `Task`, `EmailAction`
   - `Email.message_id` prevents duplicates

5. **API Retrieval**
   - File: `app/routes/emails.py`
   - `GET /emails/` returns latest work emails

## Quick Run (Local)
```powershell
& .\venv\Scripts\python.exe .\test_pipeline.py
uvicorn app.main:app --reload
```

Then open:
`http://127.0.0.1:8000/emails/`

