from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.movimiento_caja_schemas import (
    MovimientoCajaResponse,
)

from app.services.movimiento_caja_service import (
    get_movimiento_service,
    get_movimientos_service,
    get_movimientos_by_caja_service,
)


router = APIRouter(
    prefix="/movimientos-caja",
    tags=["Movimientos Caja"],
)


@router.get(
    "/",
    response_model=list[MovimientoCajaResponse],
)
def get_movimientos(
    db: Session = Depends(get_db),
):

    try:
        return get_movimientos_service(
            db,
            veterinaria_id=1,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{movimiento_id}",
    response_model=MovimientoCajaResponse,
)
def get_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db),
):

    try:
        return get_movimiento_service(
            db,
            movimiento_id,
            veterinaria_id=1,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/caja/{caja_id}",
    response_model=list[MovimientoCajaResponse],
)
def get_movimientos_by_caja(
    caja_id: int,
    db: Session = Depends(get_db),
):

    try:
        return get_movimientos_by_caja_service(
            db,
            caja_id,
            veterinaria_id=1,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )