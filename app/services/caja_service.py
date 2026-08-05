from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Caja
from app.models.enums import EstadoCaja, TipoMovimientoCaja

from app.repositories.caja_repository import (
    create_caja,
    get_caja,
    get_caja_abierta,
    get_cajas,
    update_caja,
)
from app.repositories.movimiento_caja_repository import get_cantidad_movimientos, get_total_egresos, get_total_ingresos, get_total_movimientos
from app.schemas.caja_schemas import CajaResumenResponse

def _calcular_saldo_final(
    db: Session,
    caja: Caja,
) -> Decimal:

    ingresos = get_total_movimientos(
        db,
        caja.id,
        TipoMovimientoCaja.INGRESO,
    )

    egresos = get_total_movimientos(
        db,
        caja.id,
        TipoMovimientoCaja.EGRESO,
    )

    return (
        caja.saldo_inicial
        + ingresos
        - egresos
    )

def abrir_caja_service(
    db: Session,
    saldo_inicial: Decimal,
    observaciones: str | None,
    usuario_id: int,
    veterinaria_id: int,
) -> Caja:

    caja_abierta = get_caja_abierta(
        db,
        veterinaria_id,
    )

    if caja_abierta is not None:
        raise ValueError(
            "Ya existe una caja abierta."
        )

    caja = Caja(
        veterinaria_id=veterinaria_id,
        usuario_apertura_id=usuario_id,
        saldo_inicial=saldo_inicial,
        estado=EstadoCaja.ABIERTA,
        observaciones=observaciones,
    )

    return create_caja(
        db,
        caja,
    )

def cerrar_caja_service(
    db: Session,
    caja_id: int,
    observaciones: str | None,
    usuario_id: int,
    veterinaria_id: int,
) -> Caja:

    caja = get_caja(
        db,
        caja_id,
        veterinaria_id,
    )

    if caja is None:
        raise ValueError(
            "Caja no encontrada."
        )

    if caja.estado == EstadoCaja.CERRADA:
        raise ValueError(
            "La caja ya está cerrada."
        )

    caja.saldo_final = _calcular_saldo_final(
        db,
        caja,
    )

    caja.usuario_cierre_id = usuario_id

    caja.fecha_cierre = datetime.now()

    caja.estado = EstadoCaja.CERRADA

    caja.observaciones = observaciones

    return update_caja(
        db,
        caja,
    )

def get_caja_service(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> Caja:

    caja = get_caja(
        db,
        caja_id,
        veterinaria_id,
    )

    if caja is None:
        raise ValueError(
            "Caja no encontrada."
        )

    return caja

def get_cajas_service(
    db: Session,
    veterinaria_id: int,
) -> list[Caja]:

    return get_cajas(
        db,
        veterinaria_id,
    )

def get_caja_abierta_service(
    db: Session,
    veterinaria_id: int,
) -> Caja | None:

    return get_caja_abierta(
        db,
        veterinaria_id,
    )

def get_resumen_caja_service(
    db: Session,
    veterinaria_id: int,
) -> CajaResumenResponse:

    caja = get_caja_abierta(
        db,
        veterinaria_id,
    )

    if caja is None:
        raise ValueError(
            "No hay una caja abierta."
        )

    ingresos = get_total_ingresos(
        db,
        caja.id,
    )

    egresos = get_total_egresos(
        db,
        caja.id,
    )

    cantidad_movimientos = get_cantidad_movimientos(
        db,
        caja.id,
    )

    saldo_actual = (
        caja.saldo_inicial
        + ingresos
        - egresos
    )

    return CajaResumenResponse(
        caja_id=caja.id,
        saldo_inicial=caja.saldo_inicial,
        ingresos=ingresos,
        egresos=egresos,
        cantidad_movimientos=cantidad_movimientos,
        fecha_apertura=caja.fecha_apertura,
        saldo_actual=saldo_actual,
    )