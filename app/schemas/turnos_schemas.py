from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.turno import EstadoTurno


class UsuarioTurno(BaseModel):
    id: int
    nombre: str
    apellido: str
    rol: str

    model_config = ConfigDict(from_attributes=True)


class MascotaTurno(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str | None

    model_config = ConfigDict(from_attributes=True)


class TurnoCreate(BaseModel):
    usuario_id: int
    mascota_id: int
    fecha_hora: datetime

    motivo: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    observaciones: str | None = Field(
        default=None,
        max_length=1000,
    )


class TurnoUpdate(BaseModel):
    fecha_hora: datetime | None = None

    motivo: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    observaciones: str | None = Field(
        default=None,
        max_length=1000,
    )

    estado: EstadoTurno | None = None

    usuario_id: int | None = None


class TurnoResponse(BaseModel):
    id: int

    fecha_hora: datetime

    motivo: str | None

    estado: EstadoTurno

    observaciones: str | None

    creado_en: datetime

    actualizado_en: datetime

    usuario: UsuarioTurno

    mascota: MascotaTurno

    model_config = ConfigDict(from_attributes=True)