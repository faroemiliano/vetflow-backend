from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Factura
from app.repositories.factura_repository import (
    create_factura,
    delete_factura,
    get_factura,
    get_facturas,
    get_ultima_factura,
    update_factura,
)
from app.schemas.factura_schemas import (
    FacturaCreate,
    FacturaUpdate,
)

def _generar_numero_factura(
    db: Session,
    veterinaria_id: int,
) -> tuple[int, str]:

    ultima = get_ultima_factura(
        db,
        veterinaria_id,
    )

    if ultima is None:
        numero = 1
    else:
        numero = ultima.numero + 1

    codigo = f"FAC-{numero:06d}"

    return numero, codigo

def create_factura_service(
    db: Session,
    factura_data: FacturaCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Factura:

    numero, codigo = _generar_numero_factura(
        db,
        veterinaria_id,
    )

    subtotal = Decimal("0.00")

    total = subtotal - factura_data.descuento

    total_pagado = Decimal("0.00")

    saldo_pendiente = total

    factura = Factura(
        cliente_id=factura_data.cliente_id,
        usuario_id=usuario_id,
        veterinaria_id=veterinaria_id,
        numero=numero,
        codigo_factura=codigo,
        subtotal=subtotal,
        descuento=factura_data.descuento,
        total=total,
        total_pagado=total_pagado,
        saldo_pendiente=saldo_pendiente,
        observaciones=factura_data.observaciones,
    )

    return create_factura(
        db,
        factura,
    )

def get_factura_service(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> Factura:

    factura = get_factura(
        db,
        factura_id,
        veterinaria_id,
    )

    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )

    return factura

def get_facturas_service(
    db: Session,
    veterinaria_id: int,
) -> list[Factura]:

    return get_facturas(
        db,
        veterinaria_id,
    )

def update_factura_service(
    db: Session,
    factura_id: int,
    factura_data: FacturaUpdate,
    veterinaria_id: int,
) -> Factura:

    factura = get_factura(
        db,
        factura_id,
        veterinaria_id,
    )

    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )

    for key, value in factura_data.model_dump(
        exclude_unset=True,
    ).items():

        setattr(
            factura,
            key,
            value,
        )

    return update_factura(
        db,
        factura,
    )

def delete_factura_service(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> None:

    factura = get_factura(
        db,
        factura_id,
        veterinaria_id,
    )

    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )

    delete_factura(
        db,
        factura,
    )