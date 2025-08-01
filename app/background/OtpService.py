import random
import smtplib
from redis import Redis
from email.message import EmailMessage
import logging
from infrastructure.redis_client import redis_client
from config import config

logger = logging.getLogger(__name__)

class OtpSendError(Exception): pass

class OtpService:
    def __init__(self, redis: Redis, email:str, password:str) -> None:
        self.__email = email
        self.__password = password
        self.__redis = redis

    def __generate_code(self)->str:
        return str(random.randint(100000, 999999))

    def __store_email_and_code(self, to_email:str, otp:str):
        self.__redis.set(to_email, otp, ex=300)

    def __delete_the_code(self, to_email:str):
        self.__redis.delete(to_email)

    def __send_email(self, to_email:str, otp:str):
        msg = EmailMessage()
        msg["Subject"] = "Verification CODE"
        msg["from"] = self.__email
        msg["to"] = to_email
        msg.set_content(f"Your OTP is {otp}\n\nThis code will expire in 5 minutes.")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.__email, self.__password)
                smtp.send_message(msg)
        except Exception as e:
            logger.error(f"SMTP error: {str(e)}")
            raise OtpSendError("Failed to send email")

    def verify_code(self, to_email:str, verification_code:str)->bool:
        # print(f"Redis Type = {type(self.__redis)}")
        otp = self.__redis.get(to_email)
        if otp and otp.decode("utf-8") == verification_code:
            self.__delete_the_code(to_email)
            return True
        return False

    def send_otp(self, to_email:str):
        otp = self.__generate_code()
        self.__store_email_and_code(to_email, otp)
        try:
            self.__send_email(to_email, otp)
            return {"status":"SUCCESS", "otp":otp}
        except Exception as e:
            self.__delete_the_code(to_email)
            logger.error(f"Error sending OTP: {str(e)}")
            raise OtpSendError("Failed to send email OTP")

_otp_instance = None

def get_otp_service():
    global _otp_instance
    if _otp_instance is None:
        _otp_instance = OtpService(redis=redis_client, email=config.MAIL_ACCOUNT, password=config.MAIL_PASSWORD)
    return _otp_instance
