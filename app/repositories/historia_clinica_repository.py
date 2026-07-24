from sqlalchemy.orm import Session

from app.models.historia_clinica import HistoriaClinica
from app.schemas.historia_clinica_schemas import (
    HistoriaClinicaCreate,
    HistoriaClinicaUpdate,
)


def create_historia_clinica(
    db: Session,
    historia_data: HistoriaClinicaCreate,
    usuario_id: int,
    veterinaria_id: int
) -> HistoriaClinica:
    
    nueva_historia = HistoriaClinica(
        mascota_id= historia_data.mascota_id,
        usuario_id= usuario_id,
        veterinaria_id = veterinaria_id,
        diagnostico= historia_data.diagnostico,
        tratamiento=historia_data.tratamiento,
        observaciones= historia_data.observaciones
    )
    db.add(nueva_historia)
    db.commit()
    db.refresh(nueva_historia)

    return nueva_historia


def get_historia_clinica(
        db: Session,
        historia_id: int,
        veterinaria_id: int,
)-> HistoriaClinica | None:
    
    return(
        db.query(HistoriaClinica)
        .filter(
            HistoriaClinica.id == historia_id,
            HistoriaClinica.veterinaria_id ==   veterinaria_id
        )
        .first()
    )


def get_historias_clinicas(
        db: Session,
        veterinaria_id: int,
)-> list[HistoriaClinica]:
    
    return(
        db.query(HistoriaClinica)
        .filter(
            HistoriaClinica.veterinaria_id ==veterinaria_id
        )
        .all()
    )

def update_historia_clinica(
    db: Session,
    historia_id: int,
    historia_data: HistoriaClinicaUpdate,
    veterinaria_id: int,
) -> HistoriaClinica | None:

    historia = (
        db.query(HistoriaClinica)
        .filter(
            HistoriaClinica.id == historia_id,
            HistoriaClinica.veterinaria_id == veterinaria_id,
        )
        .first()
    )

    if not historia:
        return None


    for key, value in historia_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            historia,
            key,
            value,
        )


    db.commit()
    db.refresh(historia)

    return historia

def delete_historia_clinica(
    db: Session,
    historia_id: int,
    veterinaria_id: int,
) -> bool:

    historia = (
        db.query(HistoriaClinica)
        .filter(
            HistoriaClinica.id == historia_id,
            HistoriaClinica.veterinaria_id == veterinaria_id,
        )
        .first()
    )


    if not historia:
        return False


    db.delete(historia)
    db.commit()

    return True

def get_historial_by_mascota(
    db: Session,
    mascota_id: int,
    veterinaria_id: int,
) -> list[HistoriaClinica]:

    return (
        db.query(HistoriaClinica)
        .filter(
            HistoriaClinica.mascota_id == mascota_id,
            HistoriaClinica.veterinaria_id == veterinaria_id,
        )
        .order_by(
            HistoriaClinica.creado_en.desc()
        )
        .all()
    )