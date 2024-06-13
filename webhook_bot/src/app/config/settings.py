from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    webhook_part: str
    base_url: str

    keycloak_server_url: str
    keycloak_client_id: str
    keycloak_client_secret: str
    keycloak_admin_client_secret: str
    keycloak_realm: str

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_uri: PostgresDsn

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8'
    )

    @model_validator(mode='before')  # noqa
    @classmethod
    def build_db_uri(cls, data: dict) -> dict:
        if not data.get("db_uri"):
            data["db_uri"] = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=data.get("postgres_host"),
                port=int(data.get("postgres_port")),
                username=data.get("postgres_user"),
                password=data.get("postgres_password"),
                path=data.get("postgres_db"),
            )
        return data


@lru_cache
def get_settings() -> Settings:
    return Settings()


AppSettings = Annotated[Settings, Depends(get_settings)]

if __name__ == '__main__':
    print(Settings().model_dump())
