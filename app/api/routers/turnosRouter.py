from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_roles
from app.database.session import get_db
from app.models.usuario import RolUsuario, Usuario
from app.schemas.turnos_schemas import (
    TurnoCreate,
    TurnoUpdate,
    TurnoResponse,
)
from app.services.turnos_services import (
    create_turno_service,
    get_turno_service,
    get_turnos_service,
    update_turnos_service,
    delete_turno_service,
)

router = APIRouter(
    prefix="/turnos",
    tags=["Turnos"],
)

@router.post(
    "/",
    response_model = TurnoResponse,
    status_code=status.HTTP_201_CREATED,
)

def crear_turno(
    turno: TurnoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA
        )
    ),
):
    try:
        return create_turno_service(
            db,
            turno,
            current_user.veterinaria_id
        )
    
    except ValueError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    

@router.get(
    "/",
    response_model=list[TurnoResponse],
)
def listar_turnos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_turnos_service(
        db,
        current_user.veterinaria_id,
    )



@router.get(
    "/{turno_id}",
    response_model=TurnoResponse,
)
def obtener_turno(
    turno_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_turno_service(
            db,
            turno_id,
            current_user.veterinaria_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    
@router.put(
    "/{turno_id}",
    response_model=TurnoResponse,
)
def actualizar_turno(
    turno_id: int,
    turno: TurnoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):
    try:
        return update_turnos_service(
            db,
            turno_id,
            turno,
            current_user.veterinaria_id,
        )

    except ValueError as error:

        status_code = (
            status.HTTP_400_BAD_REQUEST
            if (
                "veterinario" in str(error)
                or "horario" in str(error)
            )
            else status.HTTP_404_NOT_FOUND
        )

        raise HTTPException(
            status_code=status_code,
            detail=str(error),
        ) from error    
    
@router.delete(
    "/{turno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_turno(
    turno_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):
    try:
        delete_turno_service(
            db,
            turno_id,
            current_user.veterinaria_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error    