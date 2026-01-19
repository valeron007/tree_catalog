from typing import Any, Generator

import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from .database import SessionLocal

def get_db() -> Generator[Session, Any, None]:
    """

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

