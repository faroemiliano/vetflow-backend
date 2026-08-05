from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.factura_detalle import FacturaDetalle

from app.repositories.factura_detalle_repository import (
    create_detalle,
    delete_detalle,
    get_detalle,
    get_detalles_by_factura,
    update_detalle,
)

from app.repositories.factura_repository import (
    get_factura,
    update_factura,
)

from app.schemas.factura_detalle_schemas import (
    FacturaDetalleCreate,
    FacturaDetalleUpdate,
)


def _actualizar_totales_factura(
    db: Session,
    factura,
):

    detalles = get_detalles_by_factura(
        db,
        factura.id,
        factura.veterinaria_id,
    )


    subtotal = sum(
        (
            detalle.subtotal
            for detalle in detalles
        ),
        Decimal("0.00"),
    )


    factura.subtotal = subtotal

    factura.total = (
        subtotal - factura.descuento
    )

    factura.saldo_pendiente = (
        factura.total - factura.total_pagado
    )


    update_factura(
        db,
        factura,
    )


def create_factura_detalle_service(
    db: Session,
    detalle_data: FacturaDetalleCreate,
    veterinaria_id: int,
) -> FacturaDetalle:


    factura = get_factura(
        db,
        detalle_data.factura_id,
        veterinaria_id,
    )


    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )


    subtotal = (
        detalle_data.cantidad
        *
        detalle_data.precio_unitario
    )


    detalle = FacturaDetalle(

        factura_id=factura.id,

        descripcion=detalle_data.descripcion,

        cantidad=detalle_data.cantidad,

        precio_unitario=detalle_data.precio_unitario,

        subtotal=subtotal,
    )


    detalle = create_detalle(
        db,
        detalle,
    )


    _actualizar_totales_factura(
        db,
        factura,
    )


    return detalle



def get_detalle_service(
    db: Session,
    detalle_id: int,
    veterinaria_id: int,
):

    detalle = get_detalle(
        db,
        detalle_id,
        veterinaria_id,
    )


    if detalle is None:
        raise ValueError(
            "Detalle no encontrado."
        )


    return detalle



def get_detalles_factura_service(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
):

    return get_detalles_by_factura(
        db,
        factura_id,
        veterinaria_id,
    )



def update_factura_detalle_service(
    db: Session,
    detalle_id: int,
    detalle_data: FacturaDetalleUpdate,
    veterinaria_id: int,
):

    detalle = get_detalle(
        db,
        detalle_id,
        veterinaria_id,
    )


    if detalle is None:
        raise ValueError(
            "Detalle no encontrado."
        )


    for key, value in detalle_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            detalle,
            key,
            value,
        )


    detalle.subtotal = (
        detalle.cantidad
        *
        detalle.precio_unitario
    )


    detalle = update_detalle(
        db,
        detalle,
    )


    _actualizar_totales_factura(
        db,
        detalle.factura,
    )


    return detalle



def delete_factura_detalle_service(
    db: Session,
    detalle_id: int,
    veterinaria_id: int,
):

    detalle = get_detalle(
        db,
        detalle_id,
        veterinaria_id,
    )


    if detalle is None:
        raise ValueError(
            "Detalle no encontrado."
        )


    factura = detalle.factura


    delete_detalle(
        db,
        detalle,
    )


    _actualizar_totales_factura(
        db,
        factura,
    )