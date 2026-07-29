import os
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.adjunto import Adjunto
from app.schemas.adjunto_schemas import (
    AdjuntoCreate,
    AdjuntoUpdate,
)

from app.repositories.adjuntos_repository import (
    create_adjunto,
    get_adjunto,
    get_adjuntos,
    update_adjunto,
    delete_adjunto,
)

from app.repositories.historia_clinica_repository import (
    get_historia_clinica,
)

from app.repositories.estudio_medico_repository import (
    get_estudio,
)

UPLOAD_DIR = Path("uploads")

def create_adjunto_service(
    db: Session,
    adjunto_data: AdjuntoCreate,
    archivo: UploadFile,
    usuario_id: int,
    veterinaria_id: int,
) -> Adjunto:


    historia = get_historia_clinica(
        db,
        adjunto_data.historia_clinica_id,
        veterinaria_id,
    )


    if historia is None:
        raise ValueError(
            "Historia clínica no encontrada."
        )


    if adjunto_data.estudio_id:

        estudio = get_estudio(
            db,
            adjunto_data.estudio_id,
            veterinaria_id,
        )

        if estudio is None:
            raise ValueError(
                "Estudio no encontrado."
            )


    nombre, ruta, tamaño = guardar_archivo(
        archivo,
        veterinaria_id,
        adjunto_data.historia_clinica_id
    )


    return create_adjunto(
        db,
        adjunto_data,
        usuario_id,
        veterinaria_id,
        nombre,
        ruta,
        archivo.content_type,
        tamaño,
    )

def guardar_archivo(
    archivo: UploadFile,
    veterinaria_id: int,
    historia_clinica_id: int,
) -> tuple[str, str, int]:

    carpeta = (
        UPLOAD_DIR
        / f"veterinaria_{veterinaria_id}"
        / "historias"
        / str(historia_clinica_id)
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = Path(archivo.filename).suffix

    nombre_unico = f"{uuid4()}{extension}"

    ruta = carpeta / nombre_unico

    with ruta.open("wb") as buffer:
        shutil.copyfileobj(
            archivo.file,
            buffer,
        )

    tamano = ruta.stat().st_size

    return (
        archivo.filename,
        str(ruta),
        tamano,
    )

def get_adjuntos_service(
    db: Session,
    veterinaria_id: int,
):

    return get_adjuntos(
        db,
        veterinaria_id,
    )

def get_adjunto_service(
    db: Session,
    adjunto_id: int,
    veterinaria_id: int,
):

    return get_adjunto(
        db,
        adjunto_id,
        veterinaria_id,
    )

def update_adjunto_service(
    db: Session,
    adjunto_id: int,
    adjunto_data: AdjuntoUpdate,
    veterinaria_id: int,
):

    return update_adjunto(
        db,
        adjunto_id,
        adjunto_data,
        veterinaria_id,
    )

def delete_adjunto_service(
    db: Session,
    adjunto_id: int,
    veterinaria_id: int,
):

    return delete_adjunto(
        db,
        adjunto_id,
        veterinaria_id,
    )