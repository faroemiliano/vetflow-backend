from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.database.session import get_db
from app.models.usuario import Usuario

from app.schemas.pago_schemas import (
    PagoCreate,
    PagoResponse,
)

from app.services.pago_service import (
    anular_pago_service,
    create_pago_service,
    get_pago_service,
    get_pagos_factura_service,
    get_pagos_service,
)

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
)


@router.post(
    "/",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pago(
    pago_data: PagoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return create_pago_service(
            db=db,
            pago_data=pago_data,
            usuario_id=current_user.id,
            veterinaria_id=current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{pago_id}",
    response_model=PagoResponse,
)
def get_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_pago_service(
            db=db,
            pago_id=pago_id,
            veterinaria_id=current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/factura/{factura_id}",
    response_model=list[PagoResponse],
)
def get_pagos_factura(
    factura_id: int,
    db: Session =Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_pagos_factura_service(
        db=db,
        factura_id=factura_id,
        veterinaria_id=current_user.veterinaria_id,
    )

@router.patch(
    "/{pago_id}/anular",
    response_model=PagoResponse,
)
def anular_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return anular_pago_service(
        db,
        pago_id,
        current_user.veterinaria_id,
    )

@router.get(
    "/",
    response_model=list[PagoResponse],
)
def get_pagos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return get_pagos_service(
        db,
        current_user.veterinaria_id,
    )