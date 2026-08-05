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
from app.models.enums import (
    TipoMovimientoCaja,
    OrigenMovimientoCaja,
)

if TYPE_CHECKING:
    from app.models.caja import Caja
    from app.models.factura import Factura
    from app.models.pago import Pago
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria


class MovimientoCaja(Base):
    __tablename__ = "movimientos_caja"

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

    factura_id: Mapped[int | None] = mapped_column(
        ForeignKey("facturas.id"),
        nullable=True,
    )

    pago_id: Mapped[int | None] = mapped_column(
        ForeignKey("pagos.id"),
        nullable=True,
    )

    tipo: Mapped[TipoMovimientoCaja] = mapped_column(
        Enum(TipoMovimientoCaja),
        nullable=False,
    )

    origen: Mapped[OrigenMovimientoCaja] = mapped_column(
        Enum(OrigenMovimientoCaja),
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

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    caja: Mapped["Caja"] = relationship(
        back_populates="movimientos",
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="movimientos_caja",
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="movimientos_caja",
    )

    factura: Mapped["Factura | None"] = relationship(
        back_populates="movimientos_caja",
    )

    pago: Mapped["Pago | None"] = relationship(
        back_populates="movimientos_caja",
    )