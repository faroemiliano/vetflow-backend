from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    nombre: str
    telefono: str | None = None
    email: str | None = None

class ClienteCreate(ClienteBase):
    pass 

class ClienteUpdate(ClienteBase):
    nombre: str | None = None
    telefono: str | None = None
    email: str | None = None

class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)