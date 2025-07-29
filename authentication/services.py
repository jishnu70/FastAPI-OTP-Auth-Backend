# authentication/services.py

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from background.OtpService import OtpService
from models.User import User
from schemas.User import UserCreate, UserCreateResponse
from schemas.Otp import OtpRequest, OtpResponse
from background.celery_app import send_otp_email
import logging

logger = logging.getLogger(__name__)

async def get_user_by_username_or_email(db: AsyncSession ,name:str|None=None, email:str|None=None) -> User | None:
    if name is None and email is None:
        return None

    result = await db.execute(
        select(User)
        .where(
            or_(
                User.username==name, User.email==email
            )
        )
    )
    return result.scalars().first()

async def create_new_user(db: AsyncSession, user: UserCreate)->UserCreateResponse:
    try:
        existing_user = await get_user_by_username_or_email(db, user.username, user.email)
        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Username already exists"
                )
            elif existing_user.email == user.email:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Email already exists"
                )
        new_user = User(
            username=user.username,
            email = user.email,
            password = User.hash_password(user.password),
            is_verified = False
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        task = send_otp_email.delay(user.email)

        return UserCreateResponse(
            taskID=task.id,
            userID=new_user.id,
            message="User created, please check your email for otp verification."
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Error: create_new_user path -> {str(e)}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Error creating new user")

async def verify_the_account(db: AsyncSession, otp_service: OtpService, otp_payload: OtpRequest)->OtpResponse:
    try:
        result = otp_service.verify_code(otp_payload.email, otp_payload.otp)
        if result:
            user = await get_user_by_username_or_email(db, email=otp_payload.email)
            if not user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email")

            user.is_verified = True

            await db.commit()
            await db.refresh(user)

            return OtpResponse(
                message="account verified"
            )
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Invalid OTP")
    except Exception as e:
        logger.error(f"Error: verify_the_account path -> {str(e)}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Error verifying the OTP")
