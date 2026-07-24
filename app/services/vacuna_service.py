from sqlalchemy.orm import Session

from app.models.vacuna import Vacuna
from app.repositories.vacuna_repository import (
    create_vacuna,
    delete_vacuna,
    get_vacuna,
    get_vacunas,
    update_vacuna,
)
from app.schemas.vacuna_schemas import (
    VacunaCreate,
    VacunaUpdate,
)

def create_vacuna_service(
    db: Session,
    vacuna_data: VacunaCreate,
    veterinaria_id: int,
) -> Vacuna:

    return create_vacuna(
        db,
        vacuna_data,
        veterinaria_id,
    )

def get_vacuna_service(
    db: Session,
    vacuna_id: int,
    veterinaria_id: int,
) -> Vacuna:

    vacuna = get_vacuna(
        db,
        vacuna_id,
        veterinaria_id,
    )

    if vacuna is None:
        raise ValueError(
            "Vacuna no encontrada."
        )

    return vacuna

def get_vacunas_service(
    db: Session,
    veterinaria_id: int,
) -> list[Vacuna]:

    return get_vacunas(
        db,
        veterinaria_id,
    )

def update_vacuna_service(
    db: Session,
    vacuna_id: int,
    vacuna_data: VacunaUpdate,
    veterinaria_id: int,
) -> Vacuna:

    vacuna = update_vacuna(
        db,
        vacuna_id,
        vacuna_data,
        veterinaria_id,
    )

    if vacuna is None:
        raise ValueError(
            "Vacuna no encontrada."
        )

    return vacuna

def delete_vacuna_service(
    db: Session,
    vacuna_id: int,
    veterinaria_id: int,
) -> None:

    deleted = delete_vacuna(
        db,
        vacuna_id,
        veterinaria_id,
    )

    if not deleted:
        raise ValueError(
            "Vacuna no encontrada."
        )
    
    