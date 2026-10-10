from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://interiox:interiox@localhost:5432/interiox"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "dev-secret-change-me"
    jwt_expire_minutes: int = 60
    otp_provider: str = "console"  # console | twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
