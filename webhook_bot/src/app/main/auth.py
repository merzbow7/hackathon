import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from keycloak import KeycloakOpenID  # pip require python-keycloak
from pydantic import BaseModel

from app.config.settings import get_settings


class KcUser(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    realm_roles: list[str]


settings = get_settings()

keycloak_openid = KeycloakOpenID(
    server_url=settings.keycloak_server_url,  # https://sso.example.com/auth/
    client_id=settings.keycloak_client_id,  # backend-client-id
    realm_name=settings.keycloak_realm,  # example-realm
    client_secret_key=settings.keycloak_client_secret,  # your backend client secret
)
oauth2_scheme = HTTPBearer()


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


# Get the payload/token from keycloak
async def get_payload(token: Annotated[HTTPAuthorizationCredentials, Security(oauth2_scheme)]) -> dict:
    try:
        return keycloak_openid.decode_token(
            token.credentials,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Get user infos from the payload
async def get_user_info(payload: Annotated[dict, Depends(get_payload)]) -> KcUser:
    try:
        user = KcUser(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return user


async def admin_required(user: Annotated[KcUser, Depends(get_user_info)]) -> KcUser:
    settings = get_settings()
    if settings.vite_kk_admin_role not in user.realm_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return user
