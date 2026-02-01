from sqlalchemy import Column, Integer, String,Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    from_email = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    summary = Column(Text)
    urgency = Column(String)
    # One email has many tasks
    tasks = relationship("Task", back_populates="email",cascade="all, delete")

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    task_text = Column(Text)
    is_completed = Column(Integer, default=0)
    # Each task belongs to one email
    email = relationship("Email", back_populates="tasks")

     
    