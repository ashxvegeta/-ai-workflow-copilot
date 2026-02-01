from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.email_service import (process_and_store_emails,get_stored_emails)
from app.schemas.email import EmailResponse
from typing import List

router = APIRouter()

@router.post("/process")
def process_emails(db: Session = Depends(get_db)):
    return process_and_store_emails(db)


@router.get("/", response_model=List[EmailResponse])
def fetch_emails(db: Session = Depends(get_db)):
    emails = get_stored_emails(db)
    return emails