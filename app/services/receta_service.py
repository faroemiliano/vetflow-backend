from sqlalchemy.orm import Session

from app.models.recetas import Receta

from app.repositories.receta_repository import (
    create_receta,
    get_receta,
    get_recetas,
    get_recetas_by_historia,
    update_receta,
    delete_receta,
)

from app.schemas.receta_schemas import (
    RecetaCreate,
    RecetaUpdate,
)

def create_receta_service(
    db: Session,
    receta_data: RecetaCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Receta:


    return create_receta(
        db,
        receta_data,
        usuario_id,
        veterinaria_id,
    )

def get_receta_service(
    db: Session,
    receta_id: int,
    veterinaria_id: int,
) -> Receta | None:

    return get_receta(
        db,
        receta_id,
        veterinaria_id,
    )

def get_recetas_service(
    db: Session,
    veterinaria_id: int,
) -> list[Receta]:

    return get_recetas(
        db,
        veterinaria_id,
    )

def get_recetas_by_historia_service(
    db: Session,
    historia_clinica_id: int,
    veterinaria_id: int,
) -> list[Receta]:

    return get_recetas_by_historia(
        db,
        historia_clinica_id,
        veterinaria_id,
    )

def update_receta_service(
    db: Session,
    receta_id: int,
    receta_data: RecetaUpdate,
    veterinaria_id: int,
) -> Receta | None:

    return update_receta(
        db,
        receta_id,
        receta_data,
        veterinaria_id,
    )

def delete_receta_service(
    db: Session,
    receta_id: int,
    veterinaria_id: int,
) -> bool:

    return delete_receta(
        db,
        receta_id,
        veterinaria_id,
    )