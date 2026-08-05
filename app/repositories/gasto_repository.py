from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Gasto


def get_gasto(
    db: Session,
    gasto_id: int,
    veterinaria_id: int,
) -> Gasto | None:

    return (
        db.query(Gasto)
        .filter(
            Gasto.id == gasto_id,
            Gasto.veterinaria_id == veterinaria_id,
        )
        .first()
    )


def get_gastos(
    db: Session,
    veterinaria_id: int,
) -> list[Gasto]:

    return (
        db.query(Gasto)
        .filter(
            Gasto.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(Gasto.creado_en),
        )
        .all()
    )


def get_gastos_by_caja(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> list[Gasto]:

    return (
        db.query(Gasto)
        .filter(
            Gasto.caja_id == caja_id,
            Gasto.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(Gasto.creado_en),
        )
        .all()
    )


def create_gasto(
    db: Session,
    gasto: Gasto,
) -> Gasto:

    db.add(gasto)

    db.commit()

    db.refresh(gasto)

    return gasto


def update_gasto(
    db: Session,
    gasto: Gasto,
) -> Gasto:

    db.commit()

    db.refresh(gasto)

    return gasto


def delete_gasto(
    db: Session,
    gasto: Gasto,
) -> None:

    db.delete(gasto)

    db.commit()