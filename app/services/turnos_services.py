from sqlalchemy.orm import Session

from app.models.turno import Turno
from app.models.usuario import RolUsuario
from app.repositories.mascota_repository import get_mascota
from app.repositories.turno_repository import (
    create_turno,
    delete_turno,
    get_turno,
    get_turno_by_fecha_usuario,
    get_turnos,
    update_turno,
)
from app.repositories.usuario_repository import get_usuario
from app.schemas.turnos_schemas import (
    TurnoCreate,
    TurnoUpdate,
)

def create_turno_service(
        db:Session,
        turno_data: TurnoCreate,
        veterinaria_id: int
) -> Turno:
    
    mascota = get_mascota(
        db,
        turno_data.mascota_id,
        veterinaria_id,
    )

    if mascota is None:
        raise ValueError(
            "Mascota no encontrada"
        )
    
    usuario = get_usuario(
        db,
        turno_data.usuario_id,
        veterinaria_id
    )

    if usuario is None:
        raise ValueError(
            "Usuario no encontrado"
        )
    
    if usuario.rol != RolUsuario.VETERINARIO:
        raise ValueError(
            "El usuario seleccionado no es un veterinario"
        )
    
    turno_existente = get_turno_by_fecha_usuario(
        db,
        turno_data.usuario_id,
        turno_data.fecha_hora,
        veterinaria_id
    ) 

    if turno_existente:
        raise ValueError(
            "Veterinario ya tiene turno asignado para ese horario"
        )
    
    return create_turno(
        db,
        turno_data,
        veterinaria_id
    )

def get_turno_service(
        db: Session,
        turno_id: int,
        veterinaria_id: int,
) -> Turno:
    
    turno = get_turno(
        db,
        turno_id,
        veterinaria_id
    )

    if turno is None:
        raise ValueError(
            "Turno no encontrado"
        )
    
    return turno

def get_turnos_service(
        db: Session,
        veterinaria_id: int,
)-> list[Turno]:
    return get_turnos(
        db,
        veterinaria_id
    )

def update_turnos_service(
        db: Session,
        turno_id: int,
        turno_data: TurnoUpdate,
        veterinaria_id: int
)-> Turno:
    
    turno = get_turno(
        db,
        turno_id,
        veterinaria_id
    )

    if turno is None:
        raise ValueError(
            "Turno no encontrado"
        )
    
    if turno_data.usuario_id is not None:

        usuario = get_usuario(
            db,
            turno_data.usuario_id,
            veterinaria_id
        )
        if usuario is None:
            raise ValueError(
                "Usuario no encontrado"
            )
    
        if usuario.rol != RolUsuario.VETERINARIO:
            raise ValueError(
                "El usuario seleccionado no es veterinario"
            )
    
    usuario_id = (
        turno_data.usuario_id
        if turno_data.usuario_id is not None
        else turno.usuario_id
    )

    fecha_hora = (
        turno_data.fecha_hora
        if turno_data.fecha_hora is not None
        else turno.fecha_hora
    )

    turno_existente = get_turno_by_fecha_usuario(
        db,
        usuario_id,
        fecha_hora,
        veterinaria_id
    )

    if turno_existente and turno_existente.id != turno.id:
        raise ValueError(
            "El veterinario ya tiene un turno en ese horario."
        )
    
    return update_turno(
        db,
        turno_id,
        turno_data,
        veterinaria_id
    )
        

def delete_turno_service(
    db: Session,
    turno_id: int,
    veterinaria_id: int,
) -> bool:

    turno = get_turno(
        db,
        turno_id,
        veterinaria_id,
    )

    if turno is None:
        raise ValueError(
            "Turno no encontrado."
        )

    return delete_turno(
        db,
        turno_id,
        veterinaria_id,
    )    