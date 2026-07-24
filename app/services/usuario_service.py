import bcrypt
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.usuario import Usuario
from app.repositories.usuario_repository import (
    create_usuario,
    create_usuario_google,
    delete_usuario,
    get_usuario,
    get_usuario_by_email,
    get_usuario_by_google_id,
    get_usuarios,
    update_usuario,
    
)
from app.schemas.usuario_schemas import UsuarioCreate, UsuarioUpdate
from app.repositories.veterinaria_repository import (
    get_veterinaria_by_slug,
)


def _hash_password(password: str | None) -> str | None:
    if password is None:
        return None

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def create_usuario_service(
    db: Session,
    usuario_data: UsuarioCreate,
    veterinaria_id: int,
) -> Usuario:
    usuario_existente = get_usuario_by_email(
        db,
        usuario_data.email,
        veterinaria_id,
    )
    if usuario_existente:
        raise ValueError("Ya existe un usuario con ese email.")

    return create_usuario(
        db,
        usuario_data,
        veterinaria_id,
        _hash_password(usuario_data.password),
    )


def get_usuario_service(
    db: Session,
    usuario_id: int,
    veterinaria_id: int,
) -> Usuario:
    usuario = get_usuario(db, usuario_id, veterinaria_id)
    if usuario is None:
        raise ValueError("Usuario no encontrado.")
    return usuario


def get_usuarios_service(
    db: Session,
    veterinaria_id: int,
) -> list[Usuario]:
    return get_usuarios(db, veterinaria_id)


def login_con_google_service(
    db: Session,
    token: str,
    veterinaria_slug: str,
) -> Usuario:
    if not settings.GOOGLE_CLIENT_ID:
        raise RuntimeError("Google Sign-In no está configurado.")

    try:
        datos_google = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except (GoogleAuthError, ValueError) as error:
        raise ValueError("El token de Google no es válido o expiró.") from error

    google_id = datos_google.get("sub")
    email = datos_google.get("email")
    if not google_id or not email or not datos_google.get("email_verified"):
        raise ValueError("La cuenta de Google no tiene un email verificado.")

    usuario = get_usuario_by_google_id(db, google_id)
    if usuario:
        if not usuario.activo:
            raise ValueError("El usuario se encuentra desactivado.")
        return usuario
    
    veterinaria = get_veterinaria_by_slug(
        db,
        veterinaria_slug,
    )

    if veterinaria is None:
        raise ValueError(
            "La veterinaria no existe."
        )

    veterinaria_id = veterinaria.id

    usuario_con_email = get_usuario_by_email(db, email, veterinaria_id)
    if usuario_con_email:
        raise ValueError(
            "Ya existe un usuario con ese email. Iniciá sesión con el método original "
            "para vincular Google de forma segura."
        )

    nombre = datos_google.get("given_name") or datos_google.get("name") or email.split("@", 1)[0]
    apellido = datos_google.get("family_name") or "Sin apellido"
    return create_usuario_google(
        db,
        nombre=nombre,
        apellido=apellido,
        email=email,
        foto_url=datos_google.get("picture"),
        google_id=google_id,
        veterinaria_id=veterinaria_id,
    )


def update_usuario_service(
    db: Session,
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    veterinaria_id: int,
) -> Usuario:
    usuario = get_usuario(db, usuario_id, veterinaria_id)
    if usuario is None:
        raise ValueError("Usuario no encontrado.")

    if usuario_data.email and usuario_data.email != usuario.email:
        usuario_existente = get_usuario_by_email(
            db,
            usuario_data.email,
            veterinaria_id,
        )
        if usuario_existente:
            raise ValueError("Ya existe un usuario con ese email.")

    return update_usuario(
        db,
        usuario_id,
        usuario_data,
        veterinaria_id,
        _hash_password(usuario_data.password)
        if usuario_data.password is not None
        else None,
    )


def delete_usuario_service(
    db: Session,
    usuario_id: int,
    veterinaria_id: int,
) -> bool:
    if get_usuario(db, usuario_id, veterinaria_id) is None:
        raise ValueError("Usuario no encontrado.")

    return delete_usuario(db, usuario_id, veterinaria_id)
