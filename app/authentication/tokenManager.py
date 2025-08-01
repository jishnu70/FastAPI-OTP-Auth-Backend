# authentication/tokenManager.py

from datetime import datetime, timedelta, timezone
from enum import Enum
from fastapi import HTTPException, status
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from config import config

SECRET_KEY = config.SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM

class TokenExpire(Enum):
    access_token_expire = 30    # minutes
    refresh_token_expire = 7    # days

def create_access_token(user_data: dict):
    expires_delta: timedelta = timedelta(minutes=TokenExpire.access_token_expire.value)
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": str(user_data.get("id")),
        "type": "access"
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_data: dict):
    expires_delta: timedelta = timedelta(days=TokenExpire.refresh_token_expire.value)
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": str(user_data.get("id")),
        "type": "refresh"
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def generate_new_access_token(refresh_token: str)->str:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type for refresh")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found in token")

    new_access_token = create_access_token({"id": user_id})
    return new_access_token
