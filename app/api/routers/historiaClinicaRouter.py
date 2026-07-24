from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)
from app.database.session import get_db
from app.models.usuario import RolUsuario, Usuario
from app.schemas.historia_clinica_schemas import (
    HistoriaClinicaCreate,
    HistoriaClinicaResponse,
    HistoriaClinicaUpdate,
)
from app.services.historia_clinica_service import (
    create_historia_clinica_service,
    delete_historia_clinica_service,
    get_historia_clinica_service,
    get_historia_clinica_by_mascota,
    get_historias_clinicas_service,
    update_historia_clinica_service,
)

router = APIRouter(
    prefix="/historias-clinicas",
    tags=["Historias Clínicas"],
)

@router.post(
    "/",
    response_model=HistoriaClinicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_historia_clinica(
    historia_data: HistoriaClinicaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario= Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO
        )
    ),
):
    try:
        return create_historia_clinica_service(
            db,
            historia_data,
            current_user.id,
            current_user.veterinaria_id
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get(
    "/",
    response_model=list[HistoriaClinicaResponse],
)
def get_historias_clinicas(
    db: Session=Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_historias_clinicas_service(
        db,
        current_user.veterinaria_id
    )


    
@router.get(
    "/{historia_id}", 
    response_model=HistoriaClinicaResponse,
)

def get_historia_clinica(
    historia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    
):
    
    try:
        return get_historia_clinica_service(
            db,
            historia_id,
            current_user.veterinaria_id,
        )



    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.get(
    "/mascota/{mascota_id}",
    response_model=list[HistoriaClinicaResponse],
)
def get_historial_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:
        return get_historia_clinica_by_mascota(
            db,
            mascota_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )    
    
@router.put(
    "/{historia_id}",
    response_model=HistoriaClinicaResponse,
)
def update_historia_clinica(
    historia_id: int,
    historia_data: HistoriaClinicaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:
        return update_historia_clinica_service(
            db,
            historia_id,
            historia_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )    
    

@router.delete(
    "/{historia_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_historia_clinica(
    historia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
        )
    ),
):

    try:

        delete_historia_clinica_service(
            db,
            historia_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )