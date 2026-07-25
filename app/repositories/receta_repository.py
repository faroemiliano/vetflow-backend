from sqlalchemy.orm import Session

from app.models.recetas import Receta
from app.schemas.receta_schemas import (
    RecetaCreate,
    RecetaUpdate,
)

def create_receta(
        db: Session,
        receta_data: RecetaCreate,
        usuario_id: int,
        veterinaria_id: int
)-> Receta:
    
    receta = Receta(
        historia_clinica_id= receta_data.historia_clinica_id,
        indicaciones_generales= receta_data.indicaciones_generales,
        usuario_id= usuario_id,
        veterinaria_id= veterinaria_id
    )

    db.add(receta)
    db.commit()
    db.refresh(receta)

    return receta


def get_receta(
        db:Session,
        receta_id: int,
        veterinar_id: int,

)-> Receta:
    
    return(
        db.query(Receta)
        .filter(
            Receta.id == receta_id,
            Receta.veterinaria_id == veterinar_id,
        )
        .first()
    )

def get_recetas(
        db: Session,
        veterinaria_id: int
) -> list[Receta]:
    
    return(
        db.query(Receta)
        .filter(
            Receta.veterinaria_id == veterinaria_id
        )
        .all()
    )

def get_recetas_by_historia(
    db: Session,
    historia_clinica_id: int,
    veterinaria_id: int,
) -> list[Receta]:

    return (
        db.query(Receta)
        .filter(
            Receta.historia_clinica_id == historia_clinica_id,
            Receta.veterinaria_id == veterinaria_id,
        )
        .all()
    )

def get_recetas_by_historia(
    db: Session,
    historia_clinica_id: int,
    veterinaria_id: int,
) -> list[Receta]:

    return (
        db.query(Receta)
        .filter(
            Receta.historia_clinica_id == historia_clinica_id,
            Receta.veterinaria_id == veterinaria_id,
        )
        .all()
    )

def update_receta(
    db: Session,
    receta_id: int,
    receta_data: RecetaUpdate,
    veterinaria_id: int,
) -> Receta | None:

    receta = get_receta(
        db,
        receta_id,
        veterinaria_id,
    )

    if receta is None:
        return None


    for key, value in receta_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            receta,
            key,
            value,
        )


    db.commit()
    db.refresh(receta)

    return receta

def delete_receta(
    db: Session,
    receta_id: int,
    veterinaria_id: int,
) -> bool:

    receta = get_receta(
        db,
        receta_id,
        veterinaria_id,
    )

    if receta is None:
        return False

    db.delete(receta)
    db.commit()

    return True