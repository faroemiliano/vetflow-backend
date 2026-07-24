from sqlalchemy.orm import Session

from app.models.aplicacion_vacuna import AplicacionVacuna
from app.schemas.aplicacion_vacuna_schemas import (
    AplicacionVacunaCreate,
    AplicacionVacunaUpdate,
)

def create_aplicacion_vacuna(
    db: Session,
    aplicacion_data: AplicacionVacunaCreate,
    mascota_id: int,
    veterinaria_id: int,
) -> AplicacionVacuna:

    aplicacion = AplicacionVacuna(
        mascota_id=mascota_id,
        vacuna_id=aplicacion_data.vacuna_id,
        fecha_aplicacion=aplicacion_data.fecha_aplicacion,
        fecha_proxima=aplicacion_data.fecha_proxima,
        observaciones=aplicacion_data.observaciones,
        veterinaria_id=veterinaria_id,
    )

    db.add(aplicacion)
    db.commit()
    db.refresh(aplicacion)

    return aplicacion

def get_aplicacion_vacuna(
    db: Session,
    aplicacion_id: int,
    veterinaria_id: int,
) -> AplicacionVacuna | None:

    return (
        db.query(AplicacionVacuna)
        .filter(
            AplicacionVacuna.id == aplicacion_id,
            AplicacionVacuna.veterinaria_id == veterinaria_id,
        )
        .first()
    )

def get_aplicaciones_by_mascota(
    db: Session,
    mascota_id: int,
    veterinaria_id: int,
) -> list[AplicacionVacuna]:

    return (
        db.query(AplicacionVacuna)
        .filter(
            AplicacionVacuna.mascota_id == mascota_id,
            AplicacionVacuna.veterinaria_id == veterinaria_id,
        )
        .order_by(
            AplicacionVacuna.fecha_aplicacion.desc()
        )
        .all()
    )

def update_aplicacion_vacuna(
    db: Session,
    aplicacion_id: int,
    aplicacion_data: AplicacionVacunaUpdate,
    veterinaria_id: int,
) -> AplicacionVacuna | None:

    aplicacion = get_aplicacion_vacuna(
        db,
        aplicacion_id,
        veterinaria_id,
    )

    if aplicacion is None:
        return None

    for key, value in aplicacion_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            aplicacion,
            key,
            value,
        )

    db.commit()
    db.refresh(aplicacion)

    return aplicacion

def delete_aplicacion_vacuna(
    db: Session,
    aplicacion_id: int,
    veterinaria_id: int,
) -> bool:

    aplicacion = get_aplicacion_vacuna(
        db,
        aplicacion_id,
        veterinaria_id,
    )

    if aplicacion is None:
        return False

    db.delete(aplicacion)
    db.commit()

    return True