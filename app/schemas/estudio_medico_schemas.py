from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EstudioBase(BaseModel):

    tipo: str = Field(
        min_length=2,
        max_length=100,
    )

    nombre: str = Field(
        min_length=2,
        max_length=150,
    )

    resultado: str | None = None

    observaciones: str | None = None

    fecha_realizacion: datetime

class EstudioCreate(EstudioBase):

    historia_clinica_id: int

class EstudioUpdate(BaseModel):

    tipo: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    resultado: str | None = None

    observaciones: str | None = None

    fecha_realizacion: datetime | None = None

class EstudioResponse(EstudioBase):

    id: int

    historia_clinica_id: int

    usuario_id: int

    veterinaria_id: int


    model_config = ConfigDict(
        from_attributes=True
    )