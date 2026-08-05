from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoCaja

from app.schemas.movimiento_caja_schemas import (
    MovimientoCajaResponse,
)




class CajaBase(BaseModel):

    observaciones: str | None = None

class CajaCreate(CajaBase):

    saldo_inicial: Decimal = Field(
        ge=0,
    )

class CajaCerrar(CajaBase):
    pass

class CajaResponse(BaseModel):

    id: int

    veterinaria_id: int

    usuario_apertura_id: int
    usuario_cierre_id: int | None

    saldo_inicial: Decimal
    saldo_final: Decimal | None

    fecha_apertura: datetime
    fecha_cierre: datetime | None

    estado: EstadoCaja

    observaciones: str | None

    movimientos: list[MovimientoCajaResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )

class CajaResumenResponse(BaseModel):

    saldo_inicial: Decimal
    ingresos: Decimal
    egresos: Decimal
    saldo_actual: Decimal
    fecha_apertura: datetime
    cantidad_movimientos: int

    model_config = ConfigDict(
        from_attributes=True,
    )

