from sqlalchemy.orm import Session

from app.models.historia_clinica import HistoriaClinica
from app.repositories.historia_clinica_repository import (
    create_historia_clinica,
    delete_historia_clinica,
    get_historia_clinica,
    get_historial_by_mascota,
    get_historias_clinicas,
    update_historia_clinica,
)
from app.repositories.mascota_repository import get_mascota
from app.schemas.historia_clinica_schemas import (
    HistoriaClinicaCreate,
    HistoriaClinicaUpdate,
)

def create_historia_clinica_service(
        db:Session,
        historia_data: HistoriaClinicaCreate,
        usuario_id: int,
        veterinaria_id: int,
) -> HistoriaClinica:
    
    mascota = get_mascota(
        db,
        historia_data.mascota_id,
        veterinaria_id
    )

    if mascota is None:
        raise ValueError(
            "No se encontro una mascota"
        )
    
    return create_historia_clinica(
        db,
        historia_data,
        usuario_id,
        veterinaria_id
    )

def get_historia_clinica_service(
        db: Session,
        historia_id: int,
        veterinaria_id: int,
)-> HistoriaClinica:
    
    historia = get_historia_clinica(
        db,
        historia_id,
        veterinaria_id
    )

    if historia is None:
        raise ValueError(
            "No se encontro una historia clinica"
        )
    return historia

def get_historias_clinicas_service(
        db: Session,
        veterinaria_id: int
)-> list[HistoriaClinica]:
    
    return get_historias_clinicas(
        db,
        veterinaria_id
    )

def get_historia_clinica_by_mascota(
        db: Session,
        mascota_id: int,
        veterinaria_id: int,
)-> list[HistoriaClinica]:
    
    mascota = get_mascota(
        db,
        mascota_id,
        veterinaria_id
    )

    if mascota is None:

        raise ValueError(
            "Esta mascota no tiene Historial"
        )
    
    return get_historial_by_mascota(
        db,
        mascota_id,
        veterinaria_id
    )
    

def update_historia_clinica_service(
        db: Session,
        historia_id: int,
        historia_data: HistoriaClinicaUpdate,
        veterinaria_id: int,
    )-> HistoriaClinica:

    historia = get_historia_clinica(
        db,
        historia_id,
        veterinaria_id
    )

    if historia is None:
        raise ValueError (
            "Historia clinica no encontrada"
        )
    
    return update_historia_clinica(
        db,
        historia_id,
        historia_data,
        veterinaria_id
    )

def delete_historia_clinica_service(
        db: Session,
        historia_id: int,
        veterinaria_id: int,
)->bool:
    
    historia = get_historia_clinica(
        db,
        historia_id,
        veterinaria_id
    )

    if historia is None:
        raise ValueError(
            "Historia clinica no encotrada"
        )
    
    return delete_historia_clinica(
        db,
        historia_id,
        veterinaria_id
    )
    