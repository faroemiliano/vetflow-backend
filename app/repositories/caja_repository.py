from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Caja
from app.models.enums import EstadoCaja


def get_caja(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> Caja | None:

    return (
        db.query(Caja)
        .filter(
            Caja.id == caja_id,
            Caja.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_cajas(
    db: Session,
    veterinaria_id: int,
) -> list[Caja]:

    return (
        db.query(Caja)
        .filter(
            Caja.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(Caja.fecha_apertura),
        )
        .all()
    )


def get_caja_abierta(
    db: Session,
    veterinaria_id: int,
) -> Caja | None:

    return (
        db.query(Caja)
        .filter(
            Caja.veterinaria_id == veterinaria_id,
            Caja.estado == EstadoCaja.ABIERTA,
        )
        .first()
    )


def create_caja(
    db: Session,
    caja: Caja,
) -> Caja:

    db.add(caja)

    db.commit()

    db.refresh(caja)

    return caja


def update_caja(
    db: Session,
    caja: Caja,
) -> Caja:

    db.commit()

    db.refresh(caja)

    return caja

