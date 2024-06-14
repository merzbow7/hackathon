import uuid

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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


class Institution(Base):
    __tablename__ = "institution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="institution")


class User(Base):
    __tablename__ = "telegram_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    keycloak_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, unique=True,
    )
    verification_code: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, default=uuid.uuid4,
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institution.id", ondelete="cascade"),
        nullable=True
    )

    institution: Mapped["Institution"] = relationship(back_populates="users", foreign_keys=[institution_id])
