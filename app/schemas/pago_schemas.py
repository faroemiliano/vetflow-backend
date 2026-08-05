from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoPago
from app.models.pago import MetodoPago


class PagoBase(BaseModel):
    factura_id: int

    monto: Decimal = Field(
        gt=0,
    )

    metodo_pago: MetodoPago

    observaciones: str | None = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    observaciones: str | None = None


class PagoResponse(BaseModel):

    id:int
    factura_id:int
    usuario_id:int
    veterinaria_id:int

    monto:Decimal
    metodo_pago:MetodoPago
    estado:EstadoPago

    observaciones:str | None

    creado_en:datetime
    actualizado_en:datetime

    model_config = ConfigDict(
        from_attributes=True
    )