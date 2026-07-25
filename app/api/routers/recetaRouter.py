from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.usuario import Usuario, RolUsuario

from app.schemas.receta_schemas import (
    RecetaCreate,
    RecetaUpdate,
    RecetaResponse,
)

from app.services.receta_service import (
    create_receta_service,
    get_receta_service,
    get_recetas_service,
    get_recetas_by_historia_service,
    update_receta_service,
    delete_receta_service,
)

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)

router = APIRouter(
    prefix="/recetas",
    tags=["Recetas"]
)

@router.post(
    "",
    response_model=RecetaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_roles(
                RolUsuario.ADMIN,
                RolUsuario.VETERINARIO,
            )
        )
    ],
)
def create_receta(
    receta_data: RecetaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return create_receta_service(
        db,
        receta_data,
        current_user.id,
        current_user.veterinaria_id,
    )

@router.get(
    "/{receta_id}",
    response_model=RecetaResponse,
)
def get_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    receta = get_receta_service(
        db,
        receta_id,
        current_user.veterinaria_id,
    )

    if receta is None:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada",
        )

    return receta

@router.get(
    "",
    response_model=list[RecetaResponse],
)
def get_recetas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_recetas_service(
        db,
        current_user.veterinaria_id,
    )

@router.get(
    "/historia/{historia_clinica_id}",
    response_model=list[RecetaResponse],
)
def get_recetas_by_historia(
    historia_clinica_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_recetas_by_historia_service(
        db,
        historia_clinica_id,
        current_user.veterinaria_id,
    )

@router.put(
    "/{receta_id}",
    response_model=RecetaResponse,
)
def update_receta(
    receta_id: int,
    receta_data: RecetaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    receta = update_receta_service(
        db,
        receta_id,
        receta_data,
        current_user.veterinaria_id,
    )

    if receta is None:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada",
        )

    return receta

@router.delete(
    "/{receta_id}",
)
def delete_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    eliminado = delete_receta_service(
        db,
        receta_id,
        current_user.veterinaria_id,
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada",
        )

    return {
        "message": "Receta eliminada correctamente"
    }