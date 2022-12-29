from typing import Dict

from pydantic import BaseSettings

from .config_client import get_soa_configs


def config_server_source(settings: BaseSettings) -> Dict[str, any]:
    """
    A simple settings source that loads variables from config server

    """
    return get_soa_configs()


class Settings(BaseSettings):
    LDAP_HOST: str
    LDAP_DOMAIN: str
    LDAP_HOST_DOMAIN: str
    ALLOWED_HOST: list
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_CONTACT: dict
    SECRET_KEY: str
    AD_GROUP: str
    ACCESS_TOKEN_EXP_TIME: int
    REFRESH_TOKEN_EXP_TIME: int
    LDAP_USERNAME: str
    LDAP_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DEBUG: bool
    CRYPTOGRAPHY: str
    PROTEGRITY_USERNAME: str
    PROTEGRITY_PASSWORD: str
    BASE_CERTIFICATE: str
    DEFAULT_TIMEOUT: int
    AUDIO_DNS: str
    TOKENIZE_URL_JSON: str
    DETOKENIZE_URL_JSON: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                config_server_source,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
