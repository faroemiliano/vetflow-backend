from sqlalchemy.orm import Session

from app.models import MovimientoCaja

from app.repositories.caja_repository import (
    get_caja,
)

from app.repositories.movimiento_caja_repository import (
    create_movimiento,
    get_movimiento,
    get_movimientos,
    get_movimientos_by_caja,
)

def get_movimiento_service(
    db: Session,
    movimiento_id: int,
    veterinaria_id: int,
) -> MovimientoCaja:

    movimiento = get_movimiento(
        db,
        movimiento_id,
        veterinaria_id,
    )

    if movimiento is None:
        raise ValueError(
            "Movimiento de caja no encontrado."
        )

    return movimiento

def get_movimientos_service(
    db: Session,
    veterinaria_id: int,
) -> list[MovimientoCaja]:

    return get_movimientos(
        db,
        veterinaria_id,
    )

def get_movimientos_by_caja_service(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> list[MovimientoCaja]:

    caja = get_caja(
        db,
        caja_id,
        veterinaria_id,
    )

    if caja is None:
        raise ValueError(
            "Caja no encontrada."
        )

    return get_movimientos_by_caja(
        db,
        caja_id,
        veterinaria_id,
    )

def create_movimiento_service(
    db: Session,
    movimiento: MovimientoCaja,
) -> MovimientoCaja:

    return create_movimiento(
        db,
        movimiento,
    )

