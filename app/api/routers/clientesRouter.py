from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_roles
from app.database.session import get_db

from app.models.usuario import RolUsuario, Usuario
from app.schemas.cliente_schemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
)

from app.services.cliente_services import (
    create_cliente_service,
    get_cliente_service,
    get_clientes_service,
    update_cliente_service,
    delete_cliente_service,
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)

  # ID de la veterinaria para la que se están gestionando los clientes    

@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
    require_roles(
        RolUsuario.ADMIN,
        RolUsuario.RECEPCIONISTA,
    )
),
):
    try:
        return create_cliente_service(
            db,
            cliente,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.get(
    "/",
    response_model=list[ClienteResponse],
)
def listar_clientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_clientes_service(
        db,
        current_user.veterinaria_id,
    )

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_cliente_service(
            db,
            cliente_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
)
def actualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
    require_roles(
        RolUsuario.ADMIN,
        RolUsuario.RECEPCIONISTA,
    )
),
):
    try:
        return update_cliente_service(
            db,
            cliente_id,
            cliente,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.delete(
    "/{cliente_id}",
    status_code=204,
)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
    require_roles(RolUsuario.ADMIN)
),
):

    try:
        delete_cliente_service(
            db,
            cliente_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )  