from sqlalchemy.orm import Session

from app.models.estudio_medico import Estudio
from app.repositories.estudio_medico_repository import (
    create_estudio,
    get_estudio,
    get_estudios,
    update_estudio,
    delete_estudio,
)

from app.repositories.historia_clinica_repository import (
    get_historia_clinica,
)

from app.schemas.estudio_medico_schemas import (
    EstudioCreate,
    EstudioUpdate,
)


def create_estudio_service(
    db: Session,
    estudio_data: EstudioCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Estudio:

    historia = get_historia_clinica(
        db,
        estudio_data.historia_clinica_id,
        veterinaria_id,
    )

    if historia is None:
        raise ValueError(
            "Historia clínica no encontrada."
        )

    return create_estudio(
        db,
        estudio_data,
        usuario_id,
        veterinaria_id,
    )


def get_estudio_service(
    db: Session,
    estudio_id: int,
    veterinaria_id: int,
) -> Estudio | None:

    return get_estudio(
        db,
        estudio_id,
        veterinaria_id,
    )


def get_estudios_service(
    db: Session,
    veterinaria_id: int,
) -> list[Estudio]:

    return get_estudios(
        db,
        veterinaria_id,
    )


def update_estudio_service(
    db: Session,
    estudio_id: int,
    estudio_data: EstudioUpdate,
    veterinaria_id: int,
) -> Estudio | None:

    return update_estudio(
        db,
        estudio_id,
        estudio_data,
        veterinaria_id,
    )


def delete_estudio_service(
    db: Session,
    estudio_id: int,
    veterinaria_id: int,
) -> bool:

    return delete_estudio(
        db,
        estudio_id,
        veterinaria_id,
    )