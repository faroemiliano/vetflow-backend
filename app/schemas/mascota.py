from pydantic import BaseModel, ConfigDict, Field


class MascotaCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100
    )

    especie: str = Field(
        min_length=2,
        max_length=50
    )

    raza: str | None = Field(
        default=None,
        max_length=100
    )

    edad: int | None = None

    cliente_id: int


class MascotaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    especie: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    raza: str | None = Field(
        default=None,
        max_length=100
    )

    edad: int | None = None


class MascotaResponse(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str | None
    edad: int | None
    cliente_id: int

    model_config = ConfigDict(from_attributes=True)