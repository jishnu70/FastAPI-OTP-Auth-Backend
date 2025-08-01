# dependencies/User.py

from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from app.authentication.tokenManager import decode_token
from app.database import get_db
import logging
from app.models import User

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if not user_id:
            logger.error(f"User does not exist: {credentials_exception}")
            raise credentials_exception
    except InvalidTokenError:
        logger.error(f"Error fetching user by userID: {InvalidTokenError}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error fetching current user: {e}")
        raise credentials_exception

    user = await db.execute(select(User).filter_by(id = user_id))
    if user is None:
        logger.error("get_currect_user: User fetched is None")
        raise credentials_exception
    return user
