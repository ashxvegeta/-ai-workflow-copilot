from fastapi import FastAPI
from app.routes.emails import router as emails_router
app = FastAPI(title="AI Workflow Co-Pilot")
app.include_router(emails_router, prefix="/emails")
@app.get("/")
def health_check():
    return {"status": "AI Workflow Co-Pilot is running!"}