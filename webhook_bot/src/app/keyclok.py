import asyncio
import uuid
from pprint import pprint

from keycloak import KeycloakOpenID, KeycloakAdmin
from pydantic import BaseModel, Field, TypeAdapter

from app.config.settings import get_settings

keycloak_url = "http://127.0.0.1:8080"


# Configure client


class KeyCloakUser(BaseModel):
    telegram_id: uuid.UUID = Field(alias="id")
    username: str
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")


class KeyCloakUserWithGroups(BaseModel):
    telegram_id: uuid.UUID = Field(alias="id")
    username: str
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    groups: list[str]


async def main():
    settings = get_settings()
    # keycloak_openid = KeycloakOpenID(
    #     server_url="http://127.0.0.1:8080",
    #     realm_name=settings.keycloak_realm,
    #     client_id=settings.keycloak_client_id,
    #     client_secret_key=settings.keycloak_client_secret,
    # )
    # token = await keycloak_openid.a_token(
    #     username="check_user",
    #     password="4hakat0n",
    #     grant_type="client_credentials"
    # )

    keycloak_admin = KeycloakAdmin(
        server_url=keycloak_url,
        client_id=settings.keycloak_client_id,
        client_secret_key=settings.keycloak_client_secret,
        realm_name="Steel",
        verify=True,
    )
    users = await keycloak_admin.a_get_users({"enabled": False})
    pprint(users)


if __name__ == '__main__':
    asyncio.run(main())
