from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.usuario import Usuario

from app.schemas.adjunto_schemas import (
    AdjuntoResponse,
    AdjuntoUpdate,
)

from app.services.adjunto_service import (
    create_adjunto_service,
    get_adjunto_service,
    get_adjuntos_service,
    update_adjunto_service,
    delete_adjunto_service,
)

from app.api.dependencies.auth import (
    get_current_user,
)

router = APIRouter(
    prefix="/adjunto",
    tags=["Adjunto"],
)

@router.post(
    "/",
    response_model=AdjuntoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_adjunto(
    historia_clinica_id: int = Form(...),
    estudio_id: int | None = Form(None),
    descripcion: str | None = Form(None),

    archivo: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: Usuario = Depends(
        get_current_user
    ),
):

    try:

        from app.schemas.adjunto_schemas import AdjuntoCreate

        adjunto_data = AdjuntoCreate(
            historia_clinica_id=historia_clinica_id,
            estudio_id=estudio_id if estudio_id != 0 else None,
            descripcion=descripcion,
        )


        return create_adjunto_service(
            db,
            adjunto_data,
            archivo,
            current_user.id,
            current_user.veterinaria_id,
        )


    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
    
@router.get(
    "/",
    response_model=list[AdjuntoResponse],
)
def get_adjuntos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_adjuntos_service(
        db,
        current_user.veterinaria_id,
    )


@router.get(
    "/{adjunto_id}",
    response_model=AdjuntoResponse,
)
def get_adjunto(
    adjunto_id: int,

    db: Session = Depends(get_db),

    current_user: Usuario = Depends(
        get_current_user
    ),
):

    adjunto = get_adjunto_service(
        db,
        adjunto_id,
        current_user.veterinaria_id,
    )


    if adjunto is None:
        raise HTTPException(
            status_code=404,
            detail="Adjunto no encontrado",
        )

    return adjunto

@router.patch(
    "/{adjunto_id}",
    response_model=AdjuntoResponse,
)
def update_adjunto(
    adjunto_id: int,

    datos: AdjuntoUpdate,

    db: Session = Depends(get_db),

    current_user: Usuario = Depends(
        get_current_user
    ),
):

    adjunto = update_adjunto_service(
        db,
        adjunto_id,
        datos,
        current_user.veterinaria_id,
    )


    if adjunto is None:
        raise HTTPException(
            status_code=404,
            detail="Adjunto no encontrado",
        )


    return adjunto

@router.delete(
    "/{adjunto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_adjunto(
    adjunto_id: int,

    db: Session = Depends(get_db),

    current_user: Usuario = Depends(
        get_current_user
    ),
):

    eliminado = delete_adjunto_service(
        db,
        adjunto_id,
        current_user.veterinaria_id,
    )


    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Adjunto no encontrado",
        )