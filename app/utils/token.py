# app/utils/token.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from .security import verify_password
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from ..schemas import TokenPayload
import logging



logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(sub=payload.get("sub"), exp=payload.get("exp"), role=payload.get("role"))
        return token_data
    except JWTError as e:
        logger.debug(f"Token decode error: {e}")
        raise