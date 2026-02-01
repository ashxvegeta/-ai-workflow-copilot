# Connects Python to the DB
from sqlalchemy import create_engine
# sessionmaker → factory to create DB sessions
# declarative_base → base class for all ORM models
from sqlalchemy.orm import sessionmaker, declarative_base
# Session → used for type hinting
from sqlalchemy.orm import Session
# Generator → used because get_db() uses yield
from typing import Generator


# | Part               | Meaning    |
# | ------------------ | ---------- |
# | `sqlite`           | DB type    |
# | `///`              | local file |
# | `./ai_workflow.db` | file name  |

DATABASE_URL = "sqlite:///./ai_workflow.db"

# Create the Engine (DB connection)
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


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


