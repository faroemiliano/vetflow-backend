from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.factura import Factura

class FacturaDetalle(Base):
    __tablename__ = "factura_detalles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    factura_id: Mapped[int] = mapped_column(
        ForeignKey("facturas.id"),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
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
        back_populates="detalles",
    )

   