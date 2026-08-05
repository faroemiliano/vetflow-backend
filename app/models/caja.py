from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
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
from app.models.enums import EstadoCaja

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria
    from app.models.movimiento_caja import MovimientoCaja


class Caja(Base):
    __tablename__ = "cajas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )

    usuario_apertura_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    usuario_cierre_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True,
    )

    saldo_inicial: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    saldo_final: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    fecha_apertura: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    fecha_cierre: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    estado: Mapped[EstadoCaja] = mapped_column(
        Enum(EstadoCaja),
        nullable=False,
        default=EstadoCaja.ABIERTA,
    )

    observaciones: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="cajas",
    )

    usuario_apertura: Mapped["Usuario"] = relationship(
        foreign_keys=[usuario_apertura_id],
    )

    usuario_cierre: Mapped["Usuario | None"] = relationship(
        foreign_keys=[usuario_cierre_id],
    )

    movimientos: Mapped[list["MovimientoCaja"]] = relationship(
        back_populates="caja",
        cascade="all, delete-orphan",
    )

    gastos: Mapped[list["Gasto"]] = relationship(
        back_populates="caja",
    )