from pydantic_settings import BaseSettings

class AppSetting(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY : str = ""

    MAIL_ACCOUNT: str = ""
    MAIL_PASSWORD: str = ""

    class Config:
        env_file=".env"

config = AppSetting()
