from datetime import datetime

from sqlalchemy.orm import Session,  joinedload

from app.models.turno import Turno
from app.schemas.turnos_schemas import TurnoCreate, TurnoUpdate


def create_turno(
        db:Session,
        turno_data: TurnoCreate,
        veterinaria_id: int
)-> Turno:
    nuevo_turno = Turno(
        usuario_id= turno_data.usuario_id,
        mascota_id= turno_data.mascota_id,
        fecha_hora= turno_data.fecha_hora,
        motivo= turno_data.motivo,
        observaciones= turno_data.observaciones,
        veterinaria_id=veterinaria_id,
    )

    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)

    return nuevo_turno

def get_turno(
    db: Session,
    turno_id: int,
    veterinaria_id: int,
) -> Turno | None:

    return (
        db.query(Turno)
        .filter(
            Turno.id == turno_id,
            Turno.veterinaria_id == veterinaria_id,
        )
        .options(
            joinedload(Turno.usuario),
            joinedload(Turno.mascota),
        )
        .first()
    )

def get_turnos(
    db: Session,
    veterinaria_id: int,
) -> list[Turno]:

    return (
        db.query(Turno)
        .options(
            joinedload(Turno.usuario),
            joinedload(Turno.mascota),
        )
        .filter(
            Turno.veterinaria_id == veterinaria_id
        )
        .all()
    )

def update_turno(
        db:Session,
        turno_id: int,
        turno_data: TurnoUpdate,
        veterinaria_id: int
)-> Turno | None:
    
    turno= (
        db.query(Turno)
        .filter(
            Turno.id == turno_id,
            Turno.veterinaria_id == veterinaria_id
        ).first()
    )

    if not turno:
        return None
    
    for key, value in turno_data.model_dump(exclude_unset=True).items():
        setattr(turno, key, value)

    db.commit()
    db.refresh(turno)

    return turno

def delete_turno(
        db: Session,
        turno_id: int,
        veterinaria_id: int
) -> bool:
    
    turno= (
        db.query(Turno)
        .filter(
            Turno.id == turno_id,
            Turno.veterinaria_id == veterinaria_id
        ).first()
    )

    if not turno:
        return False
    
    db.delete(turno)
    db.commit()

    return True

def get_turnos_by_mascota(
        db:Session,
        mascota_id: int,
        veterinaria_id: int,
) -> list[Turno]:
    
    return (
        db.query(Turno)
        .filter(Turno.mascota_id == mascota_id,
                Turno.veterinaria_id == veterinaria_id,
                )
                .all()
    )

def get_turnos_by_usuario(
    db: Session,
    usuario_id: int,
    veterinaria_id: int,
) -> list[Turno]:

    return (
        db.query(Turno)
        .filter(
            Turno.usuario_id == usuario_id,
            Turno.veterinaria_id == veterinaria_id,
        )
        .all()
    )

def get_turno_by_fecha_usuario(
    db: Session,
    usuario_id: int,
    fecha_hora: datetime,
    veterinaria_id: int,
) -> Turno | None:

    return (
        db.query(Turno)
        .filter(
            Turno.usuario_id == usuario_id,
            Turno.fecha_hora == fecha_hora,
            Turno.veterinaria_id == veterinaria_id,
        )
        .first()
    )