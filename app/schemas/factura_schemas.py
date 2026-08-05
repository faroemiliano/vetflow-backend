from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoFactura, EstadoPago, MetodoPago


class PagoFacturaResponse(BaseModel):

    id: int
    monto: Decimal
    metodo_pago: MetodoPago
    estado: EstadoPago
    observaciones: str | None
    creado_en: datetime
    actualizado_en: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class FacturaBase(BaseModel):
    cliente_id: int
    descuento: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )
    observaciones: str | None = None


class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(BaseModel):
    descuento: Decimal | None = Field(
        default=None,
        ge=0
    )
    observaciones: str | None = None
    

class FacturaResponse(BaseModel):

    id: int

    cliente_id: int
    usuario_id: int
    veterinaria_id: int

    numero: int
    codigo_factura: str


    subtotal: Decimal
    descuento: Decimal
    total: Decimal


    total_pagado: Decimal
    saldo_pendiente: Decimal

    estado: EstadoFactura


    observaciones: str | None


    pagos: list[PagoFacturaResponse]


    creado_en: datetime
    actualizado_en: datetime


    model_config = ConfigDict(
        from_attributes=True
    )