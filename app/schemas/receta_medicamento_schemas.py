from pydantic import BaseModel, ConfigDict

from app.models.enums import ViaAdministracion


class RecetaMedicamentoBase(BaseModel):

    nombre: str

    presentacion: str | None = None

    dosis: str

    frecuencia: str

    duracion: str

    via_administracion: ViaAdministracion

    observaciones: str | None = None

class RecetaMedicamentoCreate(
    RecetaMedicamentoBase
):
    pass

class RecetaMedicamentoUpdate(BaseModel):

    nombre: str | None = None

    presentacion: str | None = None

    dosis: str | None = None

    frecuencia: str | None = None

    duracion: str | None = None

    via_administracion: ViaAdministracion | None = None

    observaciones: str | None = None
    

class RecetaMedicamentoResponse(
    RecetaMedicamentoBase
):

    id: int

    receta_id: int


    model_config = ConfigDict(
        from_attributes=True
    )