from pydantic_settings import BaseSettings

class AppSetting(BaseSettings):
    # DATABASE_URl: str = ""
    # SECRET_KEY : str = ""

    GMAIL_ACCOUNT: str = ""
    GMAIL_PASSWORD: str = ""

    class Config:
        env_file=".env"

config = AppSetting()
