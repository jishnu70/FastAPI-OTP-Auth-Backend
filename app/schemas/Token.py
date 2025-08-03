# schemas/Token.py

from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
