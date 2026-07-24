from sqlalchemy.orm import Session

from app.models.mascota import Mascota
from app.schemas.mascota_schemas import MascotaCreate, MascotaUpdate

def create_mascota(
        db: Session,
        mascota_data: MascotaCreate,
        veterinaria_id: int
) -> Mascota:
    """
    Crea una nueva mascota en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        mascota_data (MascotaCreate): Los datos de la mascota a crear.

    Returns:
        Mascota: La mascota creada.
    """
    nueva_mascota = Mascota(
        nombre=mascota_data.nombre,
        especie=mascota_data.especie,
        raza=mascota_data.raza,
        edad=mascota_data.edad,
        cliente_id=mascota_data.cliente_id,
        veterinaria_id=veterinaria_id
    )
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

def get_mascota(
        db: Session,
        mascota_id: int,
        veterinaria_id: int
) -> Mascota | None:
    """
    Obtiene una mascota específica de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        mascota_id (int): El ID de la mascota a obtener.

    Returns:
        Mascota | None: La mascota encontrada o None si no se encuentra.
    """
    return db.query(Mascota).filter(
        Mascota.id == mascota_id,
        Mascota.veterinaria_id == veterinaria_id
    ).first()

def get_mascotas(
    db: Session,
    veterinaria_id: int
) -> list[Mascota]:
    """
    Obtiene todas las mascotas de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        veterinaria_id (int): El ID de la veterinaria.

    Returns:
        List[Mascota]: La lista de mascotas encontradas.
    """
    return db.query(Mascota).filter(Mascota.veterinaria_id == veterinaria_id).order_by(Mascota.nombre).all()

def update_mascota(
        db: Session,
        mascota_id: int,
        mascota_data: MascotaUpdate,
        veterinaria_id: int
) -> Mascota | None:
    """
    Actualiza una mascota específica en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        mascota_id (int): El ID de la mascota a actualizar.
        mascota_data (MascotaUpdate): Los datos de la mascota a actualizar.

    Returns:
        Mascota | None: La mascota actualizada o None si no se encuentra.
    """
    mascota = db.query(Mascota).filter(
        Mascota.id == mascota_id,
        Mascota.veterinaria_id == veterinaria_id
    ).first()

    if not mascota:
        return None

    for key, value in mascota_data.model_dump(exclude_unset=True).items():
        setattr(mascota, key, value)

    db.commit()
    db.refresh(mascota)
    return mascota  

def get_mascotas_by_cliente(
        db: Session,
        cliente_id: int,
        veterinaria_id: int
)-> list[Mascota]:
    """
    Obtiene todas las mascotas asociadas a un cliente específico.

    Args:
        db (Session): La sesión de la base de datos.
        cliente_id (int): El ID del cliente.

    Returns:
        List[Mascota]: La lista de mascotas encontradas.
    """
    return db.query(Mascota).filter(
        Mascota.cliente_id == cliente_id,
        Mascota.veterinaria_id == veterinaria_id
    ).all()

def delete_mascota(
        db: Session,
        mascota_id: int,
        veterinaria_id: int
) -> bool:
    """
    Elimina una mascota específica de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        mascota_id (int): El ID de la mascota a eliminar.

    Returns:
        bool: True si la mascota fue eliminada, False si no se encuentra.
    """
    mascota = db.query(Mascota).filter(
        Mascota.id == mascota_id,
        Mascota.veterinaria_id == veterinaria_id
    ).first()

    if not mascota:
        return False

    db.delete(mascota)
    db.commit()
    return True 