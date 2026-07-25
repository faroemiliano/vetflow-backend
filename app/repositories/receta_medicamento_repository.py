from sqlalchemy.orm import Session

from app.models.receta_medicamento import RecetaMedicamento

from app.schemas.receta_medicamento_schemas import (
    RecetaMedicamentoCreate,
    RecetaMedicamentoUpdate,
)

def create_receta_medicamento(
    db: Session,
    medicamento_data: RecetaMedicamentoCreate,
    receta_id: int,
) -> RecetaMedicamento:

    medicamento = RecetaMedicamento(
        receta_id=receta_id,
        nombre=medicamento_data.nombre,
        presentacion=medicamento_data.presentacion,
        dosis=medicamento_data.dosis,
        frecuencia=medicamento_data.frecuencia,
        duracion=medicamento_data.duracion,
        via_administracion=medicamento_data.via_administracion,
        observaciones=medicamento_data.observaciones,
    )

    db.add(medicamento)
    db.commit()
    db.refresh(medicamento)

    return medicamento

def get_receta_medicamento(
    db: Session,
    medicamento_id: int,
) -> RecetaMedicamento | None:

    return (
        db.query(RecetaMedicamento)
        .filter(
            RecetaMedicamento.id == medicamento_id
        )
        .first()
    )

def get_medicamentos_by_receta(
    db: Session,
    receta_id: int,
) -> list[RecetaMedicamento]:

    return (
        db.query(RecetaMedicamento)
        .filter(
            RecetaMedicamento.receta_id == receta_id
        )
        .all()
    )

def update_receta_medicamento(
    db: Session,
    medicamento_id: int,
    medicamento_data: RecetaMedicamentoUpdate,
) -> RecetaMedicamento | None:

    medicamento = get_receta_medicamento(
        db,
        medicamento_id,
    )

    if medicamento is None:
        return None


    for key, value in medicamento_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            medicamento,
            key,
            value,
        )


    db.commit()
    db.refresh(medicamento)

    return medicamento

def delete_receta_medicamento(
    db: Session,
    medicamento_id: int,
) -> bool:

    medicamento = get_receta_medicamento(
        db,
        medicamento_id,
    )

    if medicamento is None:
        return False


    db.delete(medicamento)
    db.commit()

    return True