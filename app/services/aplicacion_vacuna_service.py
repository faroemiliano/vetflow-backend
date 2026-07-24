from sqlalchemy.orm import Session

from app.models.aplicacion_vacuna import AplicacionVacuna

from app.repositories.aplicacion_vacuna_repository import (
    create_aplicacion_vacuna,
    delete_aplicacion_vacuna,
    get_aplicacion_vacuna,
    get_aplicaciones_by_mascota,
    update_aplicacion_vacuna,
)

from app.repositories.mascota_repository import (
    get_mascota,
)

from app.repositories.vacuna_repository import (
    get_vacuna,
)

from app.schemas.aplicacion_vacuna_schemas import (
    AplicacionVacunaCreate,
    AplicacionVacunaUpdate,
)

def create_aplicacion_vacuna_service(
    db: Session,
    mascota_id: int,
    aplicacion_data: AplicacionVacunaCreate,
    veterinaria_id: int,
) -> AplicacionVacuna:

    mascota = get_mascota(
        db,
        mascota_id,
        veterinaria_id,
    )

    if mascota is None:
        raise ValueError(
            "Mascota no encontrada."
        )

    vacuna = get_vacuna(
        db,
        aplicacion_data.vacuna_id,
        veterinaria_id,
    )

    if vacuna is None:
        raise ValueError(
            "Vacuna no encontrada."
        )

    return create_aplicacion_vacuna(
        db,
        aplicacion_data,
        mascota_id,
        veterinaria_id,
    )

def get_aplicacion_vacuna_service(
    db: Session,
    aplicacion_id: int,
    veterinaria_id: int,
) -> AplicacionVacuna:

    aplicacion = get_aplicacion_vacuna(
        db,
        aplicacion_id,
        veterinaria_id,
    )

    if aplicacion is None:
        raise ValueError(
            "Aplicación de vacuna no encontrada."
        )

    return aplicacion

def get_aplicaciones_by_mascota_service(
    db: Session,
    mascota_id: int,
    veterinaria_id: int,
) -> list[AplicacionVacuna]:

    mascota = get_mascota(
        db,
        mascota_id,
        veterinaria_id,
    )

    if mascota is None:
        raise ValueError(
            "Mascota no encontrada."
        )

    return get_aplicaciones_by_mascota(
        db,
        mascota_id,
        veterinaria_id,
    )

def update_aplicacion_vacuna_service(
    db: Session,
    aplicacion_id: int,
    aplicacion_data: AplicacionVacunaUpdate,
    veterinaria_id: int,
) -> AplicacionVacuna:

    aplicacion = get_aplicacion_vacuna(
        db,
        aplicacion_id,
        veterinaria_id,
    )

    if aplicacion is None:
        raise ValueError(
            "Aplicación de vacuna no encontrada."
        )

    return update_aplicacion_vacuna(
        db,
        aplicacion_id,
        aplicacion_data,
        veterinaria_id,
    )

def delete_aplicacion_vacuna_service(
    db: Session,
    aplicacion_id: int,
    veterinaria_id: int,
) -> None:

    deleted = delete_aplicacion_vacuna(
        db,
        aplicacion_id,
        veterinaria_id,
    )

    if not deleted:
        raise ValueError(
            "Aplicación de vacuna no encontrada."
        )