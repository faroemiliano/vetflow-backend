from decimal import Decimal

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models import MovimientoCaja
from app.models.enums import TipoMovimientoCaja


def get_movimiento(
    db: Session,
    movimiento_id: int,
    veterinaria_id: int,
) -> MovimientoCaja | None:

    return (
        db.query(MovimientoCaja)
        .filter(
            MovimientoCaja.id == movimiento_id,
            MovimientoCaja.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_movimientos(
    db: Session,
    veterinaria_id: int,
) -> list[MovimientoCaja]:

    return (
        db.query(MovimientoCaja)
        .filter(
            MovimientoCaja.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(MovimientoCaja.creado_en),
        )
        .all()
    )


def get_movimientos_by_caja(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> list[MovimientoCaja]:

    return (
        db.query(MovimientoCaja)
        .filter(
            MovimientoCaja.caja_id == caja_id,
            MovimientoCaja.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(MovimientoCaja.creado_en),
        )
        .all()
    )


def create_movimiento(
    db: Session,
    movimiento: MovimientoCaja,
) -> MovimientoCaja:

    db.add(movimiento)

    db.commit()

    db.refresh(movimiento)

    return movimiento

def get_total_movimientos(
    db: Session,
    caja_id: int,
    tipo: TipoMovimientoCaja,
) -> Decimal:

    total = (
        db.query(
            func.sum(
                MovimientoCaja.monto
            )
        )
        .filter(
            MovimientoCaja.caja_id == caja_id,
            MovimientoCaja.tipo == tipo,
        )
        .scalar()
    )

    return total or Decimal("0.00")

def get_total_ingresos(
    db: Session,
    caja_id: int,
) -> Decimal:

    return get_total_movimientos(
        db,
        caja_id,
        TipoMovimientoCaja.INGRESO,
    )


def get_total_egresos(
    db: Session,
    caja_id: int,
) -> Decimal:

    return get_total_movimientos(
        db,
        caja_id,
        TipoMovimientoCaja.EGRESO,
    )

def get_cantidad_movimientos(
    db: Session,
    caja_id: int,
) -> int:

    return (
        db.query(
            func.count(
                MovimientoCaja.id,
            )
        )
        .filter(
            MovimientoCaja.caja_id == caja_id,
        )
        .scalar()
        or 0
    )