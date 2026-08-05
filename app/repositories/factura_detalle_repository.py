from sqlalchemy.orm import Session

from app.models.factura_detalle import FacturaDetalle



def get_detalle(
    db: Session,
    detalle_id: int,
    veterinaria_id: int,
) -> FacturaDetalle | None:

    return (
        db.query(FacturaDetalle)
        .filter(
            FacturaDetalle.id == detalle_id,
            FacturaDetalle.factura.has(
                veterinaria_id=veterinaria_id
            ),
        )
        .first()
    )



def get_detalles_by_factura(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> list[FacturaDetalle]:

    return (
        db.query(FacturaDetalle)
        .filter(
            FacturaDetalle.factura_id == factura_id,
            FacturaDetalle.factura.has(
                veterinaria_id=veterinaria_id
            ),
        )
        .all()
    )



def create_detalle(
    db: Session,
    detalle: FacturaDetalle,
) -> FacturaDetalle:

    db.add(detalle)

    db.commit()

    db.refresh(detalle)

    return detalle



def update_detalle(
    db: Session,
    detalle: FacturaDetalle,
) -> FacturaDetalle:

    db.commit()

    db.refresh(detalle)

    return detalle



def delete_detalle(
    db: Session,
    detalle: FacturaDetalle,
) -> None:

    db.delete(detalle)

    db.commit()