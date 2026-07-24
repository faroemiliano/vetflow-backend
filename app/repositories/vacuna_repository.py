from sqlalchemy.orm import Session

from app.models.vacuna import Vacuna
from app.schemas.vacuna_schemas import (
    VacunaCreate,
    VacunaUpdate,
)


def create_vacuna(
    db: Session,
    vacuna_data: VacunaCreate,
    veterinaria_id: int,
) -> Vacuna:

    vacuna = Vacuna(
        nombre=vacuna_data.nombre,
        descripcion=vacuna_data.descripcion,
        activo=vacuna_data.activo,
        veterinaria_id=veterinaria_id,
    )

    db.add(vacuna)
    db.commit()
    db.refresh(vacuna)

    return vacuna

def get_vacuna(
    db: Session,
    vacuna_id: int,
    veterinaria_id: int,
) -> Vacuna | None:

    return (
        db.query(Vacuna)
        .filter(
            Vacuna.id == vacuna_id,
            Vacuna.veterinaria_id == veterinaria_id,
        )
        .first()
    )

def get_vacunas(
    db: Session,
    veterinaria_id: int,
) -> list[Vacuna]:

    return (
        db.query(Vacuna)
        .filter(
            Vacuna.veterinaria_id == veterinaria_id,
        )
        .order_by(
            Vacuna.nombre.asc()
        )
        .all()
    )

def update_vacuna(
    db: Session,
    vacuna_id: int,
    vacuna_data: VacunaUpdate,
    veterinaria_id: int,
) -> Vacuna | None:

    vacuna = get_vacuna(
        db,
        vacuna_id,
        veterinaria_id,
    )

    if vacuna is None:
        return None

    for key, value in vacuna_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            vacuna,
            key,
            value,
        )

    db.commit()
    db.refresh(vacuna)

    return vacuna

def delete_vacuna(
    db: Session,
    vacuna_id: int,
    veterinaria_id: int,
) -> bool:

    vacuna = get_vacuna(
        db,
        vacuna_id,
        veterinaria_id,
    )

    if vacuna is None:
        return False

    db.delete(vacuna)
    db.commit()

    return True

