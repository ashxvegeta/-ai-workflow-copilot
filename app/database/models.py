from sqlalchemy import Column, Integer, String,Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .db import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    from_email = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    summary = Column(Text)
    urgency = Column(String)
    email_type = Column(String) # work | personal | spam
    # One email has many tasks
    status = Column(String,default="open") # open | in_progress | resolved | escalated
    assigned_to = Column(String, nullable=True)
    sla_deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    tasks = relationship("Task", back_populates="email",cascade="all, delete")

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    task_text = Column(Text)
    is_completed = Column(Integer, default=0)
    # Each task belongs to one email
    email = relationship("Email", back_populates="tasks")


class EmailAction(Base):
    __tablename__ = "email_actions"

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    action_type = Column(String(20), nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())




     
    