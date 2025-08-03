# schemas/Otp.py

from pydantic import BaseModel

class OtpRequest(BaseModel):
    email: str
    otp: str

class OtpResponse(BaseModel):
    message: str

class OtpLoginResponse(BaseModel):
    taskID: str
    message: str

    class Config:
        from_attributes = True
