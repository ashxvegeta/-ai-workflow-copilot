from pydantic import BaseModel

class Email(BaseModel):
    from_email: str
    subject: str
    body: str
