from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
    )

    apellido: str = Field(
        min_length=2,
        max_length=100,
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    email: EmailStr

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
    )

    rol: RolUsuario = RolUsuario.RECEPCIONISTA


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    apellido: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
    )

    activo: bool | None = None

    rol: RolUsuario | None = None

    foto_url: str | None = None


class GoogleTokenRequest(BaseModel):
    id_token: str = Field(min_length=1)

    veterinaria_slug: str = Field(
        min_length=2,
        max_length=100,
    )


class UsuarioResponse(BaseModel):
    id: int

    nombre: str

    apellido: str

    telefono: str | None

    email: EmailStr

    activo: bool

    rol: RolUsuario

    foto_url: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str

    token_type: str = "bearer"

    usuario: UsuarioResponse

