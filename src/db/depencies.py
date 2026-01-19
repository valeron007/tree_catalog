from typing import Any, Generator

import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.src.auth.auth_bearer import JWTBearer
from .database import SessionLocal
from ..models.models import User


def get_db() -> Generator[Session, Any, None]:
    """

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(JWTBearer())) -> HTTPException | Any:
    """

    Parameters
    ----------
    token :

    Returns
    -------

    """
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        user_id = payload.get('sub')
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.expunge(user)
        return user
    except(jwt.PyJWTError, AttributeError):
        return HTTPException(status_code="Invalid token")
