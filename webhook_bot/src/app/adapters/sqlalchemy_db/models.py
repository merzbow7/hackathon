import uuid

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.application.models.telegram_user import User

# Определяем соглашение об именованиях
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)
mapper_registry = registry()


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    keycloak_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    verification_code: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=True)


mapper_registry.map_imperatively(User, TelegramUser.__table__)
