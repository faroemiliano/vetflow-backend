from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)

from app.models.usuario import Usuario
from app.models.enums import RolUsuario

from app.schemas.factura_detalle_schemas import (
    FacturaDetalleCreate,
    FacturaDetalleResponse,
    FacturaDetalleUpdate,
)

from app.services.factura_detalle_service import (
    create_factura_detalle_service,
    delete_factura_detalle_service,
    get_detalle_service,
    get_detalles_factura_service,
    update_factura_detalle_service,
)

router = APIRouter(
    prefix="/factura-detalles",
    tags=["Factura Detalles"],
)

@router.get(
    "/{detalle_id}",
    response_model=FacturaDetalleResponse,
)
def get_detalle(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_detalle_service(
            db,
            detalle_id,
            current_user.veterinaria_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.get(
    "/factura/{factura_id}",
    response_model=list[FacturaDetalleResponse],
)
def get_detalles_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_detalles_factura_service(
        db,
        factura_id,
        current_user.veterinaria_id
    )

@router.post(
    "/",
    response_model=FacturaDetalleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_detalle(
    detalle_data: FacturaDetalleCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    try:

        return create_factura_detalle_service(
            db,
            detalle_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.put(
    "/{detalle_id}",
    response_model=FacturaDetalleResponse,
)
def update_detalle(
    detalle_id: int,
    detalle_data: FacturaDetalleUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    try:

        return update_factura_detalle_service(
            db,
            detalle_id,
            detalle_data,
            current_user.veterinaria_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.delete(
    "/{detalle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_detalle(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
        )
    ),
):

    try:

        delete_factura_detalle_service(
            db,
            detalle_id,
            current_user.veterinaria_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )