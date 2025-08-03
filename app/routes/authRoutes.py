# routes/authRoutes.py

from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import Annotated
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.authentication.services import create_new_user, get_user_by_username_or_email, verify_the_account
from app.authentication.tokenManager import create_access_token, create_refresh_token
from app.background.celery_app import send_otp_email
from app.schemas.Otp import OtpLoginResponse, OtpRequest, OtpResponse
from app.schemas.Token import TokenResponse
from app.schemas.User import UserCreate, UserCreateResponse, UserLogin
from app.database import get_db
import logging
from background.OtpService import OtpService, get_otp_service

logger = logging.getLogger(__name__)
authRoute = APIRouter(prefix="/auth", tags=["auth"])

@authRoute.post("/login", response_model=OtpLoginResponse)
async def login(db: Annotated[AsyncSession, Depends(get_db)], request: Request):
    try:
        try:
            body = await request.json()
            user_data = UserLogin(**body)
        except Exception:
            form = await request.form()
            try:
                user_data = UserLogin(
                    username=form.get("username"),
                    password=form.get("password")
                )
            except ValidationError as e:
                logger.error(f"Error login route Validation of Request Body: {str(e)}")
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        existing_user = await get_user_by_username_or_email(db, user_data.username, user_data.username)
        if existing_user is None:
            logger.error("login route: User does not exists")
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid UserName or Password")

        if not existing_user.is_verified:
            try:
                await db.delete(existing_user)
                await db.commit()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account was not verified")
            except Exception as e:
                logger.error(f"Error deleting unverified account, login route: {str(e)}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unkown behaviour from the server in login route")
        if not existing_user.verify_password(user_data.password):
            logger.error("Invalid Password")
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid UserName or Password")
        task = send_otp_email.delay(existing_user.email)

        return OtpLoginResponse(taskID=task.id, message="Otp sent")
    except Exception as e:
        logger.error(f"Error login route: {str(e)}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Error in Login route")

@authRoute.post("/verify", response_model=TokenResponse)
async def login_otp_verification(
    db: Annotated[AsyncSession, Depends(get_db)],
    otp_service: Annotated[OtpService, Depends(get_otp_service)],
    payload: OtpRequest
):
    result = otp_service.verify_code(payload.email, payload.otp)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid otp")
    existing_user = await get_user_by_username_or_email(db, email=payload.email)
    if existing_user is None:
        logger.error("login route: User does not exists")
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid UserName")
    access_token = create_access_token(user_data=existing_user.to_jwt_payload())
    refresh_token = create_refresh_token(user_data=existing_user.to_jwt_payload())
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        type="Bearer"
    )

@authRoute.post("/register", response_model=UserCreateResponse)
async def register_new_user(db: Annotated[AsyncSession, Depends(get_db)], payload: UserCreate):
    try:
        return await create_new_user(db, payload)
    except Exception as e:
        logger.error(f"Error register route: {str(e)}")
        raise

@authRoute.post("/register-verify", response_model=OtpResponse)
async def verify_account_after_registration(
    db: Annotated[AsyncSession, Depends(get_db)],
    otp_service: Annotated[OtpService, Depends(get_otp_service)],
    payload: OtpRequest
):
    try:
        return await verify_the_account(db, otp_service, payload)
    except Exception as e:
        logger.error(f"Error verifying after register route: {str(e)}")
        raise
