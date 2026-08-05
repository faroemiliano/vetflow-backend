from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class GastoBase(BaseModel):

    categoria: str

    descripcion: str

    monto: Decimal = Field(
        gt=0,
    )

    observaciones: str | None = None


class GastoCreate(GastoBase):
    pass


class GastoUpdate(BaseModel):

    categoria: str | None = None

    descripcion: str | None = None

    monto: Decimal | None = Field(
        default=None,
        gt=0,
    )

    observaciones: str | None = None


class GastoResponse(BaseModel):

    id: int

    caja_id: int

    veterinaria_id: int

    usuario_id: int

    categoria: str

    descripcion: str

    monto: Decimal

    observaciones: str | None

    creado_en: datetime

    actualizado_en: datetime


    model_config = ConfigDict(
        from_attributes=True,
    )