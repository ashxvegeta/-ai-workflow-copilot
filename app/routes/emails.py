from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.email_service import process_and_store_emails

router = APIRouter()

@router.post("/process")
def process_emails(db: Session = Depends(get_db)):
    return process_and_store_emails(db)
