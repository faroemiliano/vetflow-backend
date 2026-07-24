from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


from app.schemas.schemas_reutilizables import UsuarioSimple, MascotaSimple


class HistoriaClinicaCreate(BaseModel):

    mascota_id: int

    diagnostico: str = Field(
        min_length=3,
    )

    tratamiento: str | None = Field(
        default=None
    )

    observaciones: str | None = Field(
        default=None
    )


class HistoriaClinicaUpdate(BaseModel):

    diagnostico: str | None = Field(
        default=None,
        min_length=3,
    )

    tratamiento: str | None = None

    observaciones: str | None = None    


class HistoriaClinicaResponse(BaseModel):

    id: int

    mascota: MascotaSimple
    usuario: UsuarioSimple

    veterinaria_id: int

    diagnostico: str

    tratamiento: str | None

    observaciones: str | None

    creado_en: datetime


    model_config = ConfigDict(
        from_attributes=True
    )

