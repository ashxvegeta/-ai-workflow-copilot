from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    task_text: str
    is_completed: int

    class Config:
        from_attributes = True