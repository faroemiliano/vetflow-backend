from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)

from app.models.enums import RolUsuario

from app.models.usuario import Usuario

from app.schemas.caja_schemas import (
    CajaCreate,
    CajaCerrar,
    CajaResponse,
    CajaResumenResponse,
)

from app.services.caja_service import (
    abrir_caja_service,
    cerrar_caja_service,
    get_caja_abierta_service,
    get_caja_service,
    get_cajas_service,
    get_resumen_caja_service,
)

router = APIRouter(
    prefix="/cajas",
    tags=["Cajas"],
)

@router.post(
    "/",
    response_model=CajaResponse,
    status_code=status.HTTP_201_CREATED,
)
def abrir_caja(
    caja_data: CajaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    try:
        return abrir_caja_service(
            db=db,
            saldo_inicial=caja_data.saldo_inicial,
            observaciones=caja_data.observaciones,
            usuario_id=current_user.id,
            veterinaria_id=current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.get(
    "/",
    response_model=list[CajaResponse],
)
def get_cajas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_cajas_service(
        db,
        current_user.veterinaria_id,
    )

@router.get(
    "/abierta",
    response_model=CajaResponse,
)
def get_caja_abierta(
    db: Session =Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    caja = get_caja_abierta_service(
        db,
        current_user.veterinaria_id,
    )

    if caja is None:
        raise HTTPException(
            status_code=404,
            detail="No hay una caja abierta.",
        )

    return caja

@router.get(
    "/resumen",
    response_model=CajaResumenResponse,
)
def get_resumen_caja(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_resumen_caja_service(
            db,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.get(
    "/{caja_id}",
    response_model=CajaResponse,
)
def get_caja(
    caja_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_caja_service(
            db,
            caja_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.patch(
    "/{caja_id}/cerrar",
    response_model=CajaResponse,
)
def cerrar_caja(
    caja_id: int,
    caja_data: CajaCerrar,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    try:

        return cerrar_caja_service(
            db=db,
            caja_id=caja_id,
            observaciones=caja_data.observaciones,
            usuario_id=current_user.id,
            veterinaria_id=current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
