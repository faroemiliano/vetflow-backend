from sqlalchemy.orm import Session

from app.models.enums import EstadoPago
from app.models.pago import Pago


def get_pago(
    db: Session,
    pago_id: int,
    veterinaria_id: int,
) -> Pago | None:

    return (
        db.query(Pago)
        .filter(
            Pago.id == pago_id,
            Pago.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_pagos(
    db: Session,
    veterinaria_id: int,
) -> list[Pago]:

    return (
        db.query(Pago)
        .filter(
            Pago.veterinaria_id == veterinaria_id,
            Pago.estado == EstadoPago.ACTIVO,
        )
        .order_by(
            Pago.creado_en.desc(),
        )
        .all()
    )


def get_pagos_by_factura(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> list[Pago]:

    return (
        db.query(Pago)
        .filter(
            Pago.factura_id == factura_id,
            Pago.veterinaria_id == veterinaria_id,
            Pago.estado == EstadoPago.ACTIVO,
        )
        .order_by(
            Pago.creado_en.asc(),
        )
        .all()
    )


def create_pago(
    db: Session,
    pago: Pago,
) -> Pago:

    db.add(pago)

    db.commit()

    db.refresh(pago)

    return pago


def update_pago(
    db: Session,
    pago: Pago,
) -> Pago:

    db.commit()

    db.refresh(pago)

    return pago


def delete_pago(
    db: Session,
    pago: Pago,
) -> None:

    db.delete(pago)

    db.commit()