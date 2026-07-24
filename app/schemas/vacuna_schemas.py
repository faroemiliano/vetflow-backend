from pydantic import BaseModel, ConfigDict, Field


class VacunaSimple(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class VacunaBase(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
    )

    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )

    activo: bool = True


class VacunaCreate(VacunaBase):
    pass


class VacunaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )

    activo: bool | None = None


class VacunaResponse(VacunaBase):
    id: int
    veterinaria_id: int

    model_config = ConfigDict(from_attributes=True)