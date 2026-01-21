from typing import Any, Generator

from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db() -> Generator[Session, Any, None]:
    """

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

