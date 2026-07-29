from sqlalchemy.orm import Session

from app.models.adjunto import Adjunto
from app.schemas.adjunto_schemas import AdjuntoCreate, AdjuntoUpdate

def create_adjunto(
    db: Session,
    adjunto_data: AdjuntoCreate,
    usuario_id: int,
    veterinaria_id: int,
    nombre_archivo: str,
    ruta_archivo: str,
    tipo_archivo: str,
    tamano: int | None,
) -> Adjunto:

    adjunto = Adjunto(
        historia_clinica_id=adjunto_data.historia_clinica_id,
        estudio_id=adjunto_data.estudio_id,
        descripcion=adjunto_data.descripcion,
        usuario_id=usuario_id,
        veterinaria_id=veterinaria_id,
        nombre_archivo=nombre_archivo,
        ruta_archivo=ruta_archivo,
        tipo_archivo=tipo_archivo,
        tamano=tamano,
    )

    db.add(adjunto)
    db.commit()
    db.refresh(adjunto)

    return adjunto

def get_adjunto(
    db: Session,
    adjunto_id: int,
    veterinaria_id: int,
) -> Adjunto | None:

    return (
        db.query(Adjunto)
        .filter(
            Adjunto.id == adjunto_id,
            Adjunto.veterinaria_id == veterinaria_id,
        )
        .first()
    )

def get_adjuntos(
    db: Session,
    veterinaria_id: int,
) -> list[Adjunto]:

    return (
        db.query(Adjunto)
        .filter(
            Adjunto.veterinaria_id == veterinaria_id
        )
        .all()
    )

def update_adjunto(
    db: Session,
    adjunto_id: int,
    adjunto_data: AdjuntoUpdate,
    veterinaria_id: int,
) -> Adjunto | None:

    adjunto = get_adjunto(
        db,
        adjunto_id,
        veterinaria_id,
    )

    if adjunto is None:
        return None


    for key, value in adjunto_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            adjunto,
            key,
            value,
        )


    db.commit()
    db.refresh(adjunto)

    return adjunto

def delete_adjunto(
    db: Session,
    adjunto_id: int,
    veterinaria_id: int,
) -> bool:

    adjunto = get_adjunto(
        db,
        adjunto_id,
        veterinaria_id,
    )

    if adjunto is None:
        return False


    db.delete(adjunto)
    db.commit()

    return True