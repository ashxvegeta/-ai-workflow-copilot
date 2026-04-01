from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes.emails import router as emails_router
from app.database.db import engine
from app.database.models import Base
from app.services.scheduler_service import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Workflow Co-Pilot")
app.include_router(emails_router, prefix="/emails")

# Serve static UI
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Start background scheduler when the API starts.
start_scheduler()

@app.get("/")
def ui():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health_check():
    return {"status": "AI Workflow Co-Pilot is running!"}
