from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AdjuntoBase(BaseModel):

    historia_clinica_id: int

    estudio_id: int | None = None

    descripcion: str | None = None


class AdjuntoCreate(AdjuntoBase):
    pass


class AdjuntoUpdate(BaseModel):

    descripcion: str | None = None


class AdjuntoResponse(AdjuntoBase):

    id: int

    nombre_archivo: str

    ruta_archivo: str

    tipo_archivo: str

    tamano: int | None

    usuario_id: int

    veterinaria_id: int

    creado_en: datetime


    model_config = ConfigDict(
        from_attributes=True
    )