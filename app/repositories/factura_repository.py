from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Factura


def get_factura(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> Factura | None:

    return (
        db.query(Factura)
        .filter(
            Factura.id == factura_id,
            Factura.veterinaria_id == veterinaria_id,
        )
        .first()
    )

def get_facturas(
    db: Session,
    veterinaria_id: int,
) -> list[Factura]:

    return (
        db.query(Factura)
        .filter(
            Factura.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(Factura.numero),
        )
        .all()
    )

def get_ultima_factura(
    db: Session,
    veterinaria_id: int,
) -> Factura | None:

    return (
        db.query(Factura)
        .filter(
            Factura.veterinaria_id == veterinaria_id,
        )
        .order_by(
            desc(Factura.numero),
        )
        .first()
    )

def create_factura(
    db: Session,
    factura: Factura,
) -> Factura:

    db.add(factura)

    db.commit()

    db.refresh(factura)

    return factura

def update_factura(
    db: Session,
    factura: Factura,
) -> Factura:

    db.commit()

    db.refresh(factura)

    return factura

def delete_factura(
    db: Session,
    factura: Factura,
) -> None:

    db.delete(factura)

    db.commit()