from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import (
    TipoMovimientoCaja,
    OrigenMovimientoCaja,
)


class MovimientoCajaCreate(BaseModel):

    caja_id: int

    tipo: TipoMovimientoCaja

    origen: OrigenMovimientoCaja

    descripcion: str

    monto: Decimal

class MovimientoCajaResponse(BaseModel):

    id: int

    caja_id: int
    veterinaria_id: int
    usuario_id: int

    factura_id: int | None
    pago_id: int | None

    tipo: TipoMovimientoCaja
    origen: OrigenMovimientoCaja

    descripcion: str

    monto: Decimal

    creado_en: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )