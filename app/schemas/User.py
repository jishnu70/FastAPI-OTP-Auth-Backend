# schemas/User.py

from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, confirm_password:str, info: ValidationInfo):
        password = info.data.get("password")
        if password and confirm_password != password:
            raise ValueError("Passwords do not match")
        return confirm_password

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreateResponse(BaseModel):
    taskID: str
    userID: str
    message: str
