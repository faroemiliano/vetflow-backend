from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum

from app.models.enums import EstadoFactura
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.factura_detalle import FacturaDetalle
    from app.models.usuario import Usuario
    from app.models.veterinaria import Veterinaria
    from app.models.pago import Pago
    from app.models.movimiento_caja import MovimientoCaja


class Factura(Base):
    __tablename__ = "facturas"

    __table_args__ = (
        UniqueConstraint(
            "veterinaria_id",
            "numero",
            name="uq_factura_numero_veterinaria",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
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

    numero: Mapped[int] = mapped_column(
        nullable=False,
    )

    codigo_factura: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    descuento: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    total_pagado: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    saldo_pendiente: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    estado: Mapped[EstadoFactura] = mapped_column(
        Enum(EstadoFactura),
        default=EstadoFactura.PENDIENTE,
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

    cliente: Mapped["Cliente"] = relationship(
        back_populates="facturas",
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="facturas",
    )

    veterinaria: Mapped["Veterinaria"] = relationship(
        back_populates="facturas",
    )

    detalles: Mapped[list["FacturaDetalle"]] = relationship(
        back_populates="factura",
        cascade="all, delete-orphan",
    )

    detalles: Mapped[list["FacturaDetalle"]] = relationship(
        back_populates="factura",
        cascade="all, delete-orphan",
    )

    pagos: Mapped[list["Pago"]] = relationship(
        "Pago",
        back_populates="factura",
    )

    movimientos_caja: Mapped[list["MovimientoCaja"]] = relationship()