from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FacturaDetalleCreate(BaseModel):

    factura_id: int

    descripcion: str

    cantidad: int = Field(
        gt=0
    )

    precio_unitario: Decimal = Field(
        gt=0
    )


class FacturaDetalleUpdate(BaseModel):

    descripcion: str | None = None

    cantidad: int | None = Field(
        default=None,
        gt=0,
    )

    precio_unitario: Decimal | None = Field(
        default=None,
        gt=0,
    )


class FacturaDetalleResponse(BaseModel):

    id: int

    factura_id: int

    descripcion: str

    cantidad: int

    precio_unitario: Decimal

    subtotal: Decimal

    creado_en: datetime
    actualizado_en: datetime


    model_config = ConfigDict(
        from_attributes=True,
    )