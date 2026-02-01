# Connects Python to the DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./ai_workflow.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# Creates DB sessions (transactions)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# Parent class for all DB models
Base = declarative_base()
