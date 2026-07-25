from sqlalchemy.orm import Session

from app.models.receta_medicamento import RecetaMedicamento

from app.repositories.receta_medicamento_repository import (
    create_receta_medicamento,
    get_receta_medicamento,
    get_medicamentos_by_receta,
    update_receta_medicamento,
    delete_receta_medicamento,
)

from app.repositories.receta_repository import (
    get_receta,
)

from app.schemas.receta_medicamento_schemas import (
    RecetaMedicamentoCreate,
    RecetaMedicamentoUpdate,
)

def create_receta_medicamento_service(
    db: Session,
    medicamento_data: RecetaMedicamentoCreate,
    receta_id: int,
    veterinaria_id: int,
) -> RecetaMedicamento:


    receta = get_receta(
        db,
        receta_id,
        veterinaria_id,
    )


    if receta is None:
        raise ValueError(
            "La receta no existe o no pertenece a la veterinaria."
        )


    return create_receta_medicamento(
        db,
        medicamento_data,
        receta_id,
    )

def get_receta_medicamento_service(
    db: Session,
    medicamento_id: int,
) -> RecetaMedicamento | None:

    return get_receta_medicamento(
        db,
        medicamento_id,
    )

def get_medicamentos_by_receta_service(
    db: Session,
    receta_id: int,
    veterinaria_id: int,
) -> list[RecetaMedicamento]:


    receta = get_receta(
        db,
        receta_id,
        veterinaria_id,
    )


    if receta is None:
        raise ValueError(
            "La receta no existe."
        )


    return get_medicamentos_by_receta(
        db,
        receta_id,
    )

def update_receta_medicamento_service(
    db: Session,
    medicamento_id: int,
    medicamento_data: RecetaMedicamentoUpdate,
) -> RecetaMedicamento | None:


    return update_receta_medicamento(
        db,
        medicamento_id,
        medicamento_data,
    )

def delete_receta_medicamento_service(
    db: Session,
    medicamento_id: int,
) -> bool:


    return delete_receta_medicamento(
        db,
        medicamento_id,
    )