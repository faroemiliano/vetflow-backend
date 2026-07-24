from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.usuario_repository import get_usuario_by_email
from app.schemas.usuario_schemas import (
    GoogleTokenRequest,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
    TokenResponse,
)
from app.services.usuario_service import (
    create_usuario_service,
    delete_usuario_service,
    get_usuario_service,
    get_usuarios_service,
    login_con_google_service,
    update_usuario_service,
)

from app.core.security import create_access_token
from app.api.dependencies.auth import get_current_user, require_roles
from app.models.usuario import RolUsuario, Usuario



router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

# Temporalmente se usa una veterinaria fija hasta implementar autenticación.


@router.post("/google", response_model=TokenResponse)
def iniciar_sesion_con_google(
    credenciales: GoogleTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        usuario = login_con_google_service(
            db,
            credenciales.id_token,
            credenciales.veterinaria_slug,
        )

        access_token = create_access_token(
            {"sub": str(usuario.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": usuario,
        }
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except ValueError as error:
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe" in str(error)
            else status.HTTP_401_UNAUTHORIZED
        )
        raise HTTPException(status_code=status_code, detail=str(error)) from error


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    
)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(RolUsuario.ADMIN)
    ),
    
):
    try:
        return create_usuario_service(db, usuario, current_user.veterinaria_id,)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_usuarios_service(
        db,
        current_user.veterinaria_id,
    )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_usuario_service(
            db,
            usuario_id,
            current_user.veterinaria_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    
)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(RolUsuario.ADMIN)
),
):
    try:
        return update_usuario_service(
            db,
            usuario_id,
            usuario,
            current_user.veterinaria_id,
        )
    except ValueError as error:
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "Ya existe" in str(error)
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(error),
        ) from error


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    
    
)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
    require_roles(RolUsuario.ADMIN)
),
):
    try:
        delete_usuario_service(db, usuario_id,  current_user.veterinaria_id,)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post("/test-login")
def test_login(
    db: Session = Depends(get_db),
):

    usuario = get_usuario_by_email(
        db,
        "admin@example.com",
        1
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario de prueba no encontrado"
        )

    access_token = create_access_token(
        {"sub": str(usuario.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario,
    }