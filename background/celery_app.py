# background/celery_app.py

from celery import Celery
from background.OtpService import OtpSendError, get_otp_service

celery_app = Celery(
    "background_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(name="otp.send_email")
def send_otp_email(to_email:str):
    otp_service = get_otp_service()
    try:
        otp_service.send_otp(to_email)
        return {"status": "success"}
    except OtpSendError as e:
        return {"status": "failed", "error": str(e)}
