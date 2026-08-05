from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria
    from app.models.caja import Caja


class Gasto(Base):
    __tablename__ = "gastos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    caja_id: Mapped[int] = mapped_column(
        ForeignKey("cajas.id"),
        nullable=False,
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    monto: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    observaciones: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    caja: Mapped["Caja"] = relationship(
        back_populates="gastos",
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="gastos",
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="gastos",
    )