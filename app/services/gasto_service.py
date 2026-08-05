from sqlalchemy.orm import Session

from app.models import Gasto, MovimientoCaja

from app.models.enums import (
    TipoMovimientoCaja,
    OrigenMovimientoCaja,
)

from app.repositories.caja_repository import (
    get_caja_abierta,
)

from app.repositories.gasto_repository import (
    create_gasto,
    delete_gasto,
    get_gasto,
    get_gastos,
    get_gastos_by_caja,
    update_gasto,
)

from app.repositories.movimiento_caja_repository import (
    create_movimiento,
)

from app.schemas.gasto_schemas import (
    GastoCreate,
    GastoUpdate,
)


def create_gasto_service(
    db: Session,
    gasto_data: GastoCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Gasto:


    caja = get_caja_abierta(
        db,
        veterinaria_id,
    )


    if caja is None:
        raise ValueError(
            "No hay una caja abierta."
        )


    gasto = Gasto(
        caja_id=caja.id,
        veterinaria_id=veterinaria_id,
        usuario_id=usuario_id,
        categoria=gasto_data.categoria,
        descripcion=gasto_data.descripcion,
        monto=gasto_data.monto,
        observaciones=gasto_data.observaciones,
    )


    gasto = create_gasto(
        db,
        gasto,
    )


    movimiento = MovimientoCaja(
        caja_id=caja.id,
        veterinaria_id=veterinaria_id,
        usuario_id=usuario_id,
        tipo=TipoMovimientoCaja.EGRESO,
        origen=OrigenMovimientoCaja.GASTO,
        descripcion=f"Gasto: {gasto.descripcion}",
        monto=gasto.monto,
    )


    create_movimiento(
        db,
        movimiento,
    )


    return gasto



def get_gasto_service(
    db: Session,
    gasto_id: int,
    veterinaria_id: int,
) -> Gasto:


    gasto = get_gasto(
        db,
        gasto_id,
        veterinaria_id,
    )


    if gasto is None:
        raise ValueError(
            "Gasto no encontrado."
        )


    return gasto



def get_gastos_service(
    db: Session,
    veterinaria_id: int,
) -> list[Gasto]:

    return get_gastos(
        db,
        veterinaria_id,
    )



def get_gastos_by_caja_service(
    db: Session,
    caja_id: int,
    veterinaria_id: int,
) -> list[Gasto]:


    return get_gastos_by_caja(
        db,
        caja_id,
        veterinaria_id,
    )



def update_gasto_service(
    db: Session,
    gasto_id: int,
    gasto_data: GastoUpdate,
    veterinaria_id: int,
) -> Gasto:


    gasto = get_gasto(
        db,
        gasto_id,
        veterinaria_id,
    )


    if gasto is None:
        raise ValueError(
            "Gasto no encontrado."
        )


    for key, value in gasto_data.model_dump(
        exclude_unset=True,
    ).items():

        setattr(
            gasto,
            key,
            value,
        )


    return update_gasto(
        db,
        gasto,
    )



def delete_gasto_service(
    db: Session,
    gasto_id: int,
    veterinaria_id: int,
) -> None:


    gasto = get_gasto(
        db,
        gasto_id,
        veterinaria_id,
    )


    if gasto is None:
        raise ValueError(
            "Gasto no encontrado."
        )


    delete_gasto(
        db,
        gasto,
    )