from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecetaSimple(BaseModel):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class RecetaBase(BaseModel):
    indicaciones_generales: str | None = Field(
        default=None,
        max_length=1000,
    )


class RecetaCreate(RecetaBase):
    historia_clinica_id: int


class RecetaUpdate(BaseModel):
    indicaciones_generales: str | None = Field(
        default=None,
        max_length=1000,
    )


class RecetaResponse(RecetaBase):
    id: int

    historia_clinica_id: int
    usuario_id: int
    veterinaria_id: int

    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(
        from_attributes=True
    )