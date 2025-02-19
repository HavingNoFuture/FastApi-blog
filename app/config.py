from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8")

    DATABASE_URL: str
    SECRET_KEY: str
    TOKEN_LIFETIME: int = 3600  # seconds


settings = Settings()
