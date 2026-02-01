from fastapi import FastAPI
from app.routes.emails import router as emails_router
from app.database.db import engine
from app.database.models import Base
Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Workflow Co-Pilot")
app.include_router(emails_router, prefix="/emails")
@app.get("/")
def health_check():
    return {"status": "AI Workflow Co-Pilot is running!"}