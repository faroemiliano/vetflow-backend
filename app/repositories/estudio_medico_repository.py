from sqlalchemy.orm import Session

from app.models.estudio_medico import Estudio
from app.schemas.estudio_medico_schemas import (
    EstudioCreate,
    EstudioUpdate,
)


def create_estudio(
    db: Session,
    estudio_data: EstudioCreate,
    usuario_id: int,
    veterinaria_id: int,
) -> Estudio:

    nuevo_estudio = Estudio(
        **estudio_data.model_dump(),
        usuario_id=usuario_id,
        veterinaria_id=veterinaria_id,
    )

    db.add(nuevo_estudio)
    db.commit()
    db.refresh(nuevo_estudio)

    return nuevo_estudio

def get_estudio(
    db: Session,
    estudio_id: int,
    veterinaria_id: int,
) -> Estudio | None:

    return (
        db.query(Estudio)
        .filter(
            Estudio.id == estudio_id,
            Estudio.veterinaria_id == veterinaria_id,
        )
        .first()
    )

def get_estudios(
    db: Session,
    veterinaria_id: int,
) -> list[Estudio]:

    return (
        db.query(Estudio)
        .filter(
            Estudio.veterinaria_id == veterinaria_id
        )
        .all()
    )

def update_estudio(
    db: Session,
    estudio_id: int,
    estudio_data: EstudioUpdate,
    veterinaria_id: int,
) -> Estudio | None:

    estudio = get_estudio(
        db,
        estudio_id,
        veterinaria_id,
    )

    if estudio is None:
        return None


    for key, value in estudio_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            estudio,
            key,
            value,
        )


    db.commit()
    db.refresh(estudio)

    return estudio

def delete_estudio(
    db: Session,
    estudio_id: int,
    veterinaria_id: int,
) -> bool:

    estudio = get_estudio(
        db,
        estudio_id,
        veterinaria_id,
    )

    if estudio is None:
        return False


    db.delete(estudio)
    db.commit()

    return True