import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, MetaData, BigInteger, Identity
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

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

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="institution")
    turnovers: Mapped[list["Turnover"]] = relationship(back_populates="institution")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="institution")


class User(Base):
    __tablename__ = "telegram_user"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
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
    enabled: Mapped[bool] = mapped_column(default=True)

    institution: Mapped["Institution"] = relationship(back_populates="users", foreign_keys=[institution_id])


class Dict(Base):
    __tablename__ = "dict"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    ste_name: Mapped[str] = mapped_column(nullable=True)
    characteristics_name: Mapped[str] = mapped_column(nullable=True)
    reference_price: Mapped[float] = mapped_column(nullable=True)
    final_category_directory: Mapped[str] = mapped_column(nullable=True)
    kpgz_code: Mapped[str] = mapped_column(nullable=True)
    kpgz: Mapped[str] = mapped_column(nullable=True)
    spgz_code: Mapped[float] = mapped_column(nullable=True)
    spgz: Mapped[str] = mapped_column(nullable=True)
    registry_number_rk: Mapped[int] = mapped_column(BigInteger, nullable=True)


class Turnover(Base):
    __tablename__ = "turnover"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    product: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(nullable=True)
    unit_of_measurement: Mapped[str] = mapped_column(nullable=True)
    quantity_start_debit: Mapped[float] = mapped_column(nullable=True)
    balance_start_debit: Mapped[float] = mapped_column(nullable=True)
    quantity_turnover_debit: Mapped[float] = mapped_column(nullable=True)
    turnover_debit: Mapped[float] = mapped_column(nullable=True)
    quantity_turnover_credit: Mapped[float] = mapped_column(nullable=True)
    turnover_credit: Mapped[float] = mapped_column(nullable=True)
    quantity_end_debit: Mapped[float] = mapped_column(nullable=True)
    balance_end_debit: Mapped[float] = mapped_column(nullable=True)
    account_number: Mapped[int] = mapped_column(nullable=True)
    quarter_number: Mapped[int] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)

    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institution.id", ondelete="cascade"),
        nullable=True
    )
    institution: Mapped["Institution"] = relationship(back_populates="turnovers", foreign_keys=[institution_id])


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    id_spgz: Mapped[float] = mapped_column(nullable=True)
    name_spgz: Mapped[str] = mapped_column(nullable=True)
    registry_number_rk: Mapped[str] = mapped_column(nullable=True)
    lot_number_procurement: Mapped[float] = mapped_column(nullable=True)
    ikz: Mapped[str] = mapped_column(nullable=True)
    customer: Mapped[str] = mapped_column(nullable=True)
    subject_gk_name: Mapped[str] = mapped_column(nullable=True)
    supplier_selection_method: Mapped[str] = mapped_column(nullable=True)
    contract_basis_single_supplier: Mapped[str] = mapped_column(nullable=True)
    contract_status: Mapped[str] = mapped_column(nullable=True)
    version_number: Mapped[float] = mapped_column(nullable=True)
    gk_price_rub: Mapped[float] = mapped_column(nullable=True)
    gk_price_at_signing_rub: Mapped[float] = mapped_column(nullable=True)
    paid_rub: Mapped[float] = mapped_column(nullable=True)
    paid_percent: Mapped[float] = mapped_column(nullable=True)
    final_kpgz_code: Mapped[str] = mapped_column(nullable=True)
    final_kpgz_name: Mapped[str] = mapped_column(nullable=True)
    contract_date: Mapped[datetime] = mapped_column(nullable=True)
    registration_date: Mapped[datetime] = mapped_column(nullable=True)
    last_change_date: Mapped[datetime] = mapped_column(nullable=True)
    execution_start_date: Mapped[datetime] = mapped_column(nullable=True)
    execution_end_date: Mapped[datetime] = mapped_column(nullable=True)
    contract_end_date: Mapped[datetime] = mapped_column(nullable=True)
    supplier_sme_status_at_contract_signing: Mapped[str] = mapped_column(nullable=True)
    supplier_region_name: Mapped[str] = mapped_column(nullable=True)
    law_basis_44_223: Mapped[float] = mapped_column(nullable=True)
    electronic_execution: Mapped[str] = mapped_column(nullable=True)
    fulfilled_by_supplier: Mapped[float] = mapped_column(nullable=True)

    institution_id: Mapped[int] = mapped_column(
        ForeignKey("institution.id", ondelete="cascade"),
        nullable=True
    )
    institution: Mapped["Institution"] = relationship(back_populates="contracts", foreign_keys=[institution_id])
