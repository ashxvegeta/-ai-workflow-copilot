import email
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.email_schema import EmailCreate
from app.services.email_service import (process_and_store_emails,get_stored_emails)
from app.schemas.email import EmailResponse
from typing import List
from fastapi import HTTPException, status

router = APIRouter()

@router.post("/process")
def process_email(
    email: EmailCreate,
    db: Session = Depends(get_db)
):
    if email.body.strip() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email body cannot be empty."
        )
    
    return process_and_store_emails(db, email)
    


@router.get("/", response_model=List[EmailResponse])
def fetch_emails(db: Session = Depends(get_db)):
    emails = get_stored_emails(db)
    return emails