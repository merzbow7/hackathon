import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from keycloak import KeycloakAdmin
from pydantic import BaseModel, Field, TypeAdapter, ConfigDict, model_validator
from pydantic_core.core_schema import ValidationInfo
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

from app.adapters.sqlalchemy_db.institution.repository import get_institution_repo, InstitutionRepository
from app.adapters.sqlalchemy_db.users.repository import UserRepository, get_user_repo
from app.main.keycloak import get_keycloak_admin_provider

admin_router = APIRouter(prefix="/admin")


class InstitutionModel(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserModel(BaseModel):
    id: int
    telegram_id: int
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    keycloak_id: uuid.UUID
    verification_code: uuid.UUID
    institution: InstitutionModel | None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    @classmethod
    def remove_stopwords(cls, data: "UserModel", info: ValidationInfo):
        context = info.context
        if not context:
            return data
        kc_user = context.get(str(data.keycloak_id))
        if kc_user:
            data.first_name = kc_user.get("firstName")
            data.last_name = kc_user.get("lastName")
        return data


@admin_router.get("/users", tags=["user-management"])
async def get_users(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
) -> list[UserModel]:
    kc_users = await keycloak_admin.a_get_users()
    context = {user.get("id"): user for user in kc_users}
    users = await user_repo.get_all()
    ta = TypeAdapter(List[UserModel])
    return ta.validate_python(users, context=context)


@admin_router.get("/user/{user_id}", tags=["user-management"])
async def get_user(
    user_id: int,
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin_provider)],
) -> UserModel:
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    kc_user = await keycloak_admin.a_get_user(str(user.keycloak_id))
    return UserModel.model_validate(user, context={str(user.keycloak_id): kc_user})


class UserInstitution(BaseModel):
    institution_id: int | None


@admin_router.put("/user/{user_id}", tags=["user-management"])
async def set_user_institution(
    user_id: int,
    user_institution: UserInstitution,
    user_repo: Annotated[UserRepository, Depends(get_user_repo)]
):
    updated = await user_repo.set_institution(user_id, user_institution.institution_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return Response(status_code=204)


@admin_router.get("/groups", tags=["user-management"])
async def get_groups(
    institution_repo: Annotated[InstitutionRepository, Depends(get_institution_repo)],
) -> list[InstitutionModel]:
    institutions = await institution_repo.get_all()
    ta = TypeAdapter(List[InstitutionModel])
    return ta.validate_python(institutions)


@admin_router.get("/group/{group_id}", tags=["user-management"])
async def get_group(
    institution_id: int,
    institution_repo: Annotated[InstitutionRepository, Depends(get_institution_repo)],
) -> InstitutionModel:
    institution = await institution_repo.get(institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Not found")
    return InstitutionModel.model_validate(institution)


@admin_router.post("/add_group", tags=["user-management"])
async def add_group(
    group_name: str,
    institution_repo: Annotated[InstitutionRepository, Depends(get_institution_repo)],
):
    try:
        await institution_repo.add(group_name)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="already exists")
    else:
        return Response(status_code=204)
