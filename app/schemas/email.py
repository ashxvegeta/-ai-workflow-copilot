from pydantic import BaseModel
from typing import List
from app.schemas.task import TaskResponse

class EmailResponse(BaseModel):
    id: int
    from_email: str
    subject: str
    body: str
    summary: str
    urgency: str
    tasks: List[TaskResponse]

    class Config:
        from_attributes = True
