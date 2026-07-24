from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AplicacionVacunaCreate(BaseModel):
    vacuna_id: int

    fecha_aplicacion: date

    fecha_proxima: date | None = None

    observaciones: str | None = Field(
        default=None,
        max_length=500,
    )


class AplicacionVacunaUpdate(BaseModel):
    fecha_aplicacion: date | None = None

    fecha_proxima: date | None = None

    observaciones: str | None = Field(
        default=None,
        max_length=500,
    )


class AplicacionVacunaResponse(BaseModel):
    id: int

    mascota_id: int
    vacuna_id: int

    fecha_aplicacion: date
    fecha_proxima: date | None

    observaciones: str | None

    veterinaria_id: int

    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)