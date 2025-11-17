# app/routes/dependencies.py
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import crud, models
from ..utils import token as token_utils
from ..schemas import TokenPayload
from ..config import logger

def get_authorization_credentials(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    return parts[1]

def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_authorization_credentials)) -> models.User:
    try:
        payload: TokenPayload = token_utils.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    if payload.sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(models.User).filter(models.User.id == int(payload.sub)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Unauthorized admin access attempt user_id={current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
