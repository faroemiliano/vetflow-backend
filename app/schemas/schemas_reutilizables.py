from pydantic import BaseModel, ConfigDict

class UsuarioSimple(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class MascotaSimple(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class ClienteSimple(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class VeterinariaSimple(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)