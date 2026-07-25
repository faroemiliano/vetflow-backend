from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.estudio_medico_schemas import (
    EstudioCreate,
    EstudioUpdate,
    EstudioResponse,
)

from app.services.estudio_medico_service import (
    create_estudio_service,
    get_estudio_service,
    get_estudios_service,
    update_estudio_service,
    delete_estudio_service,
)

from app.api.dependencies.auth import (
    get_current_user,
)

from app.models.usuario import Usuario


router = APIRouter(
    prefix="/estudios",
    tags=["Estudios"],
)

@router.post(
    "/",
    response_model=EstudioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_estudio(
    estudio_data: EstudioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return create_estudio_service(
            db,
            estudio_data,
            current_user.id,
            current_user.veterinaria_id,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
    
@router.get(
    "/{estudio_id}",
    response_model=EstudioResponse,
)
def get_estudio(
    estudio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    estudio = get_estudio_service(
        db,
        estudio_id,
        current_user.veterinaria_id,
    )


    if estudio is None:
        raise HTTPException(
            status_code=404,
            detail="Estudio no encontrado.",
        )


    return estudio

@router.get(
    "/",
    response_model=list[EstudioResponse],
)
def get_estudios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_estudios_service(
        db,
        current_user.veterinaria_id,
    )

@router.put(
    "/{estudio_id}",
    response_model=EstudioResponse,
)
def update_estudio(
    estudio_id: int,
    estudio_data: EstudioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    estudio = update_estudio_service(
        db,
        estudio_id,
        estudio_data,
        current_user.veterinaria_id,
    )


    if estudio is None:
        raise HTTPException(
            status_code=404,
            detail="Estudio no encontrado.",
        )


    return estudio

@router.delete(
    "/{estudio_id}",
)
def delete_estudio(
    estudio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    eliminado = delete_estudio_service(
        db,
        estudio_id,
        current_user.veterinaria_id,
    )


    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Estudio no encontrado.",
        )


    return {
        "message": "Estudio eliminado correctamente."
    }