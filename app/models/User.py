# models/User.py

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Boolean
from uuid import uuid4
from passlib.context import CryptContext
from app.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False, default=lambda: str(uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def verify_password(self, plain_password:str)->bool:
        return pwd_context.verify(plain_password, self.password)

    def to_jwt_payload(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
        }

    @staticmethod
    def hash_password(password:str)->str:
        return pwd_context.hash(password)
