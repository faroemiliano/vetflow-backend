from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)

from app.models.enums import RolUsuario
from app.models.usuario import Usuario

from app.schemas.vacuna_schemas import (
    VacunaCreate,
    VacunaResponse,
    VacunaUpdate,
)

from app.schemas.aplicacion_vacuna_schemas import (
    AplicacionVacunaCreate,
    AplicacionVacunaResponse,
    AplicacionVacunaUpdate,
)

from app.services.vacuna_service import (
    create_vacuna_service,
    delete_vacuna_service,
    get_vacuna_service,
    get_vacunas_service,
    update_vacuna_service,
)

from app.services.aplicacion_vacuna_service import (
    create_aplicacion_vacuna_service,
    delete_aplicacion_vacuna_service,
    get_aplicacion_vacuna_service,
    get_aplicaciones_by_mascota_service,
    update_aplicacion_vacuna_service,
)

router = APIRouter(
    prefix="/vacunas",
    tags=["Vacunas"],
)

@router.post(
    "",
    response_model=VacunaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vacuna(
    vacuna_data: VacunaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:

        return create_vacuna_service(
            db,
            vacuna_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get(
    "",
    response_model=list[VacunaResponse],
)
def get_vacunas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_vacunas_service(
        db,
        current_user.veterinaria_id,
    )

@router.get(
    "/{vacuna_id}",
    response_model=VacunaResponse,
)
def get_vacuna(
    vacuna_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_vacuna_service(
            db,
            vacuna_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.put(
    "/{vacuna_id}",
    response_model=VacunaResponse,
)
def update_vacuna(
    vacuna_id: int,
    vacuna_data: VacunaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:

        return update_vacuna_service(
            db,
            vacuna_id,
            vacuna_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.delete(
    "/{vacuna_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vacuna(
    vacuna_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
        )
    ),
):

    try:

        delete_vacuna_service(
            db,
            vacuna_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.post(
    "/mascotas/{mascota_id}",
    response_model=AplicacionVacunaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_aplicacion(
    mascota_id: int,
    aplicacion_data: AplicacionVacunaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:

        return create_aplicacion_vacuna_service(
            db,
            mascota_id,
            aplicacion_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get(
    "/mascotas/{mascota_id}",
    response_model=list[AplicacionVacunaResponse],
)
def get_historial_vacunas(
    mascota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_aplicaciones_by_mascota_service(
            db,
            mascota_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.get(
    "/aplicaciones/{aplicacion_id}",
    response_model=AplicacionVacunaResponse,
)
def get_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_aplicacion_vacuna_service(
            db,
            aplicacion_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.put(
    "/aplicaciones/{aplicacion_id}",
    response_model=AplicacionVacunaResponse,
)
def update_aplicacion(
    aplicacion_id: int,
    aplicacion_data: AplicacionVacunaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:

        return update_aplicacion_vacuna_service(
            db,
            aplicacion_id,
            aplicacion_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
@router.delete(
    "/aplicaciones/{aplicacion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
        )
    ),
):

    try:

        delete_aplicacion_vacuna_service(
            db,
            aplicacion_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )