from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    # REDIS  👇 ADD THESE
    REDIS_HOST: str
    REDIS_PORT: int

    FRONTEND_RESET_URL: str
    FRONTEND_MENTOR_URL: str
    FRONTEND_GUEST_URL: str
    FRONTEND_URL: str = "http://localhost:5173" # Default for local dev

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
