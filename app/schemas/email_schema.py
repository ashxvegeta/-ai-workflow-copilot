from pydantic import BaseModel

class EmailCreate(BaseModel):
    from_email: str
    subject: str
    body: str
    message_id: str | None = None
