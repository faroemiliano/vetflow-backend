from sqlalchemy.orm import Session

from app.models.usuario import RolUsuario, Usuario
from app.schemas.usuario_schemas import UsuarioCreate, UsuarioUpdate


def create_usuario(
    db: Session,
    usuario_data: UsuarioCreate,
    veterinaria_id: int,
    password_hash: str | None,
) -> Usuario:
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        telefono=usuario_data.telefono,
        email=usuario_data.email,
        password_hash=password_hash,
        rol=usuario_data.rol,
        veterinaria_id=veterinaria_id,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def get_usuario(
    db: Session,
    usuario_id: int,
    veterinaria_id: int,
) -> Usuario | None:
    return (
        db.query(Usuario)
        .filter(
            Usuario.id == usuario_id,
            Usuario.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_usuarios(db: Session, veterinaria_id: int) -> list[Usuario]:
    return (
        db.query(Usuario)
        .filter(Usuario.veterinaria_id == veterinaria_id)
        .all()
    )


def get_usuario_by_email(
    db: Session,
    email: str,
    veterinaria_id: int,
) -> Usuario | None:
    return (
        db.query(Usuario)
        .filter(
            Usuario.email == email,
            Usuario.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_usuario_by_google_id(db: Session, google_id: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.google_id == google_id).first()


def create_usuario_google(
    db: Session,
    *,
    nombre: str,
    apellido: str,
    email: str,
    foto_url: str | None,
    google_id: str,
    veterinaria_id: int,
) -> Usuario:
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        foto_url=foto_url,
        google_id=google_id,
        rol=RolUsuario.RECEPCIONISTA,
        veterinaria_id=veterinaria_id,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def update_usuario(
    db: Session,
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    veterinaria_id: int,
    password_hash: str | None = None,
) -> Usuario | None:
    usuario = get_usuario(db, usuario_id, veterinaria_id)

    if usuario is None:
        return None

    datos_actualizacion = usuario_data.model_dump(
        exclude_unset=True,
        exclude={"password"},
    )
    for key, value in datos_actualizacion.items():
        setattr(usuario, key, value)

    if password_hash is not None:
        usuario.password_hash = password_hash

    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(
    db: Session,
    usuario_id: int,
    veterinaria_id: int,
) -> bool:
    usuario = get_usuario(db, usuario_id, veterinaria_id)

    if usuario is None:
        return False

    usuario.activo = False
    db.commit()
    return True
