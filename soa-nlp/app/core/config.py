from pydantic import BaseSettings


class Settings(BaseSettings):
    ALLOWED_HOST: list
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_CONTACT: dict
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
