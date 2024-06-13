import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from keycloak import KeycloakAdmin, KeycloakDeleteError, KeycloakPutError
from pydantic import BaseModel, Field, TypeAdapter
from starlette.responses import Response

from app.main.keycloak import get_keycloak_admin_provider

admin_router = APIRouter(prefix="/admin")


class KeyCloakUser(BaseModel):
    telegram_id: uuid.UUID = Field(alias="id")
    username: str
    email: str | None
    first_name: str | None = Field(alias="firstName")
    last_name: str | None = Field(alias="lastName")


class KeyCloakGroups(BaseModel):
    group_id: uuid.UUID = Field(alias="id")
    name: str
    path: str


class KeyCloakGroupsWithUser(BaseModel):
    group_id: uuid.UUID = Field(alias="id")
    name: str
    path: str
    users: list[KeyCloakUser]


class KeyCloakUserWithGroup(BaseModel):
    telegram_id: uuid.UUID = Field(alias="id")
    username: str
    email: str | None
    first_name: str | None = Field(alias="firstName")
    last_name: str | None = Field(alias="lastName")
    groups: list[KeyCloakGroups]


@admin_router.get("/users", tags=["user-management"])
async def get_users(
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    users = await keycloak_admin.a_get_users({"enabled": True, 'emailVerified': True})
    ta = TypeAdapter(List[KeyCloakUser])
    return ta.validate_python(users)


@admin_router.get("/user", tags=["user-management"])
async def get_user(
    user_id: uuid.UUID,
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    user_uuid = str(user_id)
    user = await keycloak_admin.a_get_user(user_uuid)
    user_groups = await keycloak_admin.a_get_user_groups(user_uuid)
    user["groups"] = user_groups
    return KeyCloakUserWithGroup.model_validate(user)


@admin_router.get("/groups", tags=["user-management"])
async def get_groups(
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    groups = await keycloak_admin.a_get_groups({"enabled": True})
    ta = TypeAdapter(List[KeyCloakGroups])
    return ta.validate_python(groups)


@admin_router.get("/group", tags=["user-management"])
async def get_group(
    group_id: uuid.UUID,
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    group_uuid = str(group_id)
    group = await keycloak_admin.a_get_group(group_uuid)
    users = await keycloak_admin.a_get_group_members(group_uuid)
    group["users"] = users
    return KeyCloakGroupsWithUser.model_validate(group)


@admin_router.put("/add_group", tags=["user-management"])
async def add_group(
    user_id: uuid.UUID,
    group_id: uuid.UUID,
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    group_uuid = str(group_id)
    user_uuid = str(user_id)
    try:
        await keycloak_admin.a_group_user_add(user_uuid, group_uuid)
    except KeycloakPutError as exc:
        Response(status_code=exc.response_code, content=exc.error_message)
    else:
        return Response(status_code=204)


@admin_router.put("/remove_group", tags=["user-management"])
async def remove_group(
    user_id: uuid.UUID,
    group_id: uuid.UUID,
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
):
    group_uuid = str(group_id)
    user_uuid = str(user_id)
    try:
        await keycloak_admin.a_group_user_remove(user_uuid, group_uuid)
    except KeycloakDeleteError as exc:
        Response(status_code=exc.response_code, content=exc.error_message)
    else:
        return Response(status_code=204)
