from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import EstadoFactura, EstadoPago
from app.models import Pago

from app.models import MovimientoCaja

from app.models.enums import (
    TipoMovimientoCaja,
    OrigenMovimientoCaja,
)

from app.repositories.caja_repository import (
    get_caja_abierta,
)

from app.repositories.movimiento_caja_repository import (
    create_movimiento,
)

from app.repositories.factura_repository import (
    get_factura,
    update_factura,
)

from app.repositories.pago_repository import (
    create_pago,
    delete_pago,
    get_pago,
    get_pagos,
    get_pagos_by_factura,
    update_pago,
)

from app.schemas.pago_schemas import (
    PagoCreate,
    PagoUpdate,
)


def _recalcular_factura(
    db: Session,
    factura,
    veterinaria_id
) -> None:

    pagos = get_pagos_by_factura(
        db,
        factura.id,
        veterinaria_id,
    )

    total_pagado = sum(
        (
            pago.monto
            for pago in pagos
        ),
        Decimal("0.00"),
    )

    factura.total_pagado = total_pagado

    saldo = factura.total - total_pagado

    if saldo < Decimal("0.00"):
        saldo = Decimal("0.00")

    factura.saldo_pendiente = saldo

    if factura.estado != EstadoFactura.ANULADA:

        if total_pagado == Decimal("0.00"):
            factura.estado = EstadoFactura.PENDIENTE

        elif saldo == Decimal("0.00"):
            factura.estado = EstadoFactura.PAGADA

        else:
            factura.estado = EstadoFactura.PARCIAL

    update_factura(
        db,
        factura,
        
    )


def create_pago_service(
    db: Session,
    pago_data: PagoCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Pago:

    factura = get_factura(
        db,
        pago_data.factura_id,
        veterinaria_id,
    )

    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )

    if factura.estado == EstadoFactura.ANULADA:
        raise ValueError(
            "La factura está anulada."
        )

    if pago_data.monto <= Decimal("0.00"):
        raise ValueError(
            "El monto debe ser mayor que cero."
        )

    if pago_data.monto > factura.saldo_pendiente:
        raise ValueError(
            "El pago supera el saldo pendiente."
        )

    pago = Pago(
        factura_id=factura.id,
        usuario_id=usuario_id,
        veterinaria_id=veterinaria_id,
        monto=pago_data.monto,
        metodo_pago=pago_data.metodo_pago,
        observaciones=pago_data.observaciones,
    )

    pago = create_pago(
        db,
        pago,
        
        
    )

    caja = get_caja_abierta(
    db,
    veterinaria_id,
)

    if caja is not None:

        movimiento = MovimientoCaja(
            caja_id=caja.id,
            veterinaria_id=veterinaria_id,
            usuario_id=usuario_id,
            factura_id=factura.id,
            pago_id=pago.id,
            tipo=TipoMovimientoCaja.INGRESO,
            origen=OrigenMovimientoCaja.PAGO,
            descripcion=f"Pago factura {factura.codigo_factura}",
            monto=pago.monto,
        )

        create_movimiento(
            db,
            movimiento,
        )

    _recalcular_factura(
        db,
        factura,
        veterinaria_id
        
    )

    return pago


def get_pago_service(
    db: Session,
    pago_id: int,
    veterinaria_id: int,
) -> Pago:

    pago = get_pago(
        db,
        pago_id,
        veterinaria_id,
    )

    if pago is None:
        raise ValueError(
            "Pago no encontrado."
        )

    return pago

def get_pagos_service(
    db: Session,
    veterinaria_id: int,
) -> list[Pago]:

    return get_pagos(
        db,
        veterinaria_id,
    )

def get_pagos_factura_service(
    db: Session,
    factura_id: int,
    veterinaria_id: int,
) -> list[Pago]:

    factura = get_factura(
        db,
        factura_id,
        veterinaria_id,
    )

    if factura is None:
        raise ValueError(
            "Factura no encontrada."
        )

    return get_pagos_by_factura(
        db,
        factura.id,
        veterinaria_id
    )


def update_pago_service(
    db: Session,
    pago_id: int,
    pago_data: PagoUpdate,
    veterinaria_id: int,
) -> Pago:

    pago = get_pago(
        db,
        pago_id,
        
    )

    if pago is None:
        raise ValueError(
            "Pago no encontrado."
        )

    factura = pago.factura

    for key, value in pago_data.model_dump(
        exclude_unset=True,
    ).items():

        setattr(
            pago,
            key,
            value,
        )

    pagos = get_pagos_by_factura(
        db,
        factura.id,
    )

    otros_pagos = sum(
        (
            p.monto
            for p in pagos
            if p.id != pago.id
        ),
        Decimal("0.00"),
    )

    if otros_pagos + pago.monto > factura.total:
        raise ValueError(
            "El total de pagos supera el total de la factura."
        )

    pago = update_pago(
        db,
        pago,
        
    )

    _recalcular_factura(
        db,
        factura,
        veterinaria_id,
    )

    return pago


def delete_pago_service(
    db: Session,
    pago_id: int,
    veterinaria_id: int,
) -> None:

    pago = get_pago(
        db,
        pago_id,
        veterinaria_id,
    )

    if pago is None:
        raise ValueError(
            "Pago no encontrado."
        )

    factura = pago.factura

    delete_pago(
        db,
        pago,
        veterinaria_id
    )

    _recalcular_factura(
        db,
        factura,
        veterinaria_id
    )


def anular_pago_service(
    db: Session,
    pago_id: int,
    veterinaria_id: int,
) -> Pago:

    pago = get_pago(
        db,
        pago_id,
        veterinaria_id,
    )

    if pago is None:
        raise ValueError(
            "Pago no encontrado."
        )

    if pago.estado == EstadoPago.ANULADO:
        raise ValueError(
            "El pago ya está anulado."
        )

    pago.estado = EstadoPago.ANULADO

    update_pago(
        db,
        pago,
    )

    caja = get_caja_abierta(
    db,
    veterinaria_id,
)

    if caja is not None:

        movimiento = MovimientoCaja(
            caja_id=caja.id,
            veterinaria_id=veterinaria_id,
            usuario_id=pago.usuario_id,
            factura_id=pago.factura_id,
            pago_id=pago.id,
            tipo=TipoMovimientoCaja.EGRESO,
            origen=OrigenMovimientoCaja.AJUSTE,
            descripcion=f"Anulación pago factura {pago.factura.codigo_factura}",
            monto=pago.monto,
        )

        create_movimiento(
            db,
            movimiento,
        )

    _recalcular_factura(
        db,
        pago.factura,
        veterinaria_id,
    )

    return pago