from sqlalchemy.orm import Session

from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate

from app.repositories.mascota_repository import (
    create_mascota,
    get_mascota,
    get_mascotas,
    update_mascota,
    delete_mascota, 
    get_mascotas_by_cliente)

from app.repositories.cliente_repository import get_cliente

def create_mascota_service(
    db: Session,
    mascota_data: MascotaCreate,
    veterinaria_id: int
) -> Mascota:
    """
    Crea una nueva mascota validando que el cliente exista
    dentro de la misma veterinaria.
    """

    cliente = get_cliente(db, mascota_data.cliente_id, veterinaria_id)

    if cliente is None:
        raise ValueError("Cliente no encontrado.")

    return create_mascota(db, mascota_data, veterinaria_id)

def get_mascota_service(
    db: Session,
    mascota_id: int,
    veterinaria_id: int
) -> Mascota | None:
    """
    Obtiene una mascota específica de la base de datos.
    """

    mascota = get_mascota(db, mascota_id, veterinaria_id)
    if mascota is None:
        raise ValueError("Mascota no fue encontrada.")
    
    return get_mascota(db, mascota_id, veterinaria_id)

def get_mascotas_service(
    db: Session,
    veterinaria_id: int
) -> list[Mascota]:
    """
    Obtiene todas las mascotas de la base de datos.
    """
    return get_mascotas(db, veterinaria_id) 

def update_mascota_service(
    db: Session,
    mascota_id: int,
    mascota_data: MascotaUpdate,
    veterinaria_id: int
) -> Mascota | None:
    """
    Actualiza una mascota específica de la base de datos.
    """
    mascota = get_mascota(db, mascota_id, veterinaria_id)

    if mascota is None:
        raise ValueError("Mascota no fue encontrada.")

    return update_mascota(db, mascota_id, mascota_data, veterinaria_id) 

def delete_mascota_service(
    db: Session,
    mascota_id: int,
    veterinaria_id: int
) -> bool:
    """
    Elimina una mascota específica de la base de datos.
    """

    mascota = get_mascota(db, mascota_id, veterinaria_id)
    if mascota is None:
        raise ValueError("Mascota no fue encontrada.")
    return delete_mascota(db, mascota_id, veterinaria_id)   

def get_mascotas_by_cliente_service(
    db: Session,
    cliente_id: int,
    veterinaria_id: int
) -> list[Mascota]:
    """
    Obtiene todas las mascotas de un cliente específico de la base de datos.
    """
    return get_mascotas_by_cliente(db, cliente_id, veterinaria_id)