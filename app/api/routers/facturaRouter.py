from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)
from app.models.enums import RolUsuario
from app.models.usuario import Usuario
from app.schemas.factura_schemas import (
    FacturaCreate,
    FacturaResponse,
    FacturaUpdate,
)
from app.services.factura_service import (
    create_factura_service,
    delete_factura_service,
    get_factura_service,
    get_facturas_service,
    update_factura_service,
)

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"],
)


@router.get(
    "/",
    response_model=list[FacturaResponse],
)
def get_facturas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_facturas_service(
        db,
        current_user.veterinaria_id,
    )

@router.get(
    "/{factura_id}",
    response_model=FacturaResponse,
)
def get_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_factura_service(
            db,
            factura_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.post(
    "/",
    response_model=FacturaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_factura(
    factura_data: FacturaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    return create_factura_service(
        db,
        factura_data,
        current_user.id,
        current_user.veterinaria_id,
    )   

@router.put(
    "/{factura_id}",
    response_model=FacturaResponse,
)
def update_factura(
    factura_id: int,
    factura_data: FacturaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.RECEPCIONISTA,
        )
    ),
):

    try:

        return update_factura_service(
            db,
            factura_id,
            factura_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{factura_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
        )
    ),
):

    try:

        delete_factura_service(
            db,
            factura_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )