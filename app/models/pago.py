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
from app.models.enums import EstadoPago, MetodoPago


if TYPE_CHECKING:
    from app.models.factura import Factura
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria
    from app.models.movimiento_caja import MovimientoCaja


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    factura_id: Mapped[int] = mapped_column(
        ForeignKey("facturas.id"),
        nullable=False,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    veterinaria_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarias.id"),
        nullable=False,
    )

    monto: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    metodo_pago: Mapped[MetodoPago] = mapped_column(
        Enum(MetodoPago),
        nullable=False,
    )

    estado: Mapped[EstadoPago] = mapped_column(
        Enum(EstadoPago),
        nullable=False,
        default=EstadoPago.ACTIVO,
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

    factura: Mapped["Factura"] = relationship(
        back_populates="pagos",
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="pagos",
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="pagos",
    )

    movimientos_caja: Mapped[list["MovimientoCaja"]] = relationship()