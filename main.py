from typing import Annotated
from fastapi import FastAPI, status, Response, Depends
import uvicorn
from pydantic import BaseModel
from background.OtpService import OtpService, get_otp_service
from background.celery_app import send_otp_email

app = FastAPI()

class EmailRequest(BaseModel):
    email: str

@app.get("/")
def root():
    return {"message": "backend is online"}

@app.post("/")
async def login(payload: EmailRequest):
    task = send_otp_email.delay(payload.email)
    return {"taskID": task.id, "message": "OTP sent"}

@app.post("/verify-otp")
def verify_the_otp(payload:OtpRequest, otp_service: OtpService = Depends(get_otp_service)):
    result = otp_service.verify_code(payload.email, payload.otp)
    if result:
        return {"message": "otp verified"}
    return Response(status_code=status.HTTP_400_BAD_REQUEST, content={"message":"wrong otp"})

def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
