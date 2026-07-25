from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.usuario import Usuario, RolUsuario

from app.schemas.receta_medicamento_schemas import (
    RecetaMedicamentoCreate,
    RecetaMedicamentoUpdate,
    RecetaMedicamentoResponse,
)

from app.services.receta_medicamento_service import (
    create_receta_medicamento_service,
    get_medicamentos_by_receta_service,
    get_receta_medicamento_service,
    update_receta_medicamento_service,
    delete_receta_medicamento_service,
)

from app.api.dependencies.auth import (
    get_current_user,
    require_roles,
)

router = APIRouter(
    prefix="/recetas",
    tags=["Receta Medicamentos"],
)

@router.post(
    "/{receta_id}/medicamentos",
    response_model=RecetaMedicamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_medicamento(
    receta_id: int,
    medicamento_data: RecetaMedicamentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    try:

        return create_receta_medicamento_service(
            db,
            medicamento_data,
            receta_id,
            current_user.veterinaria_id,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
    
@router.get(
    "/{receta_id}/medicamentos",
    response_model=list[RecetaMedicamentoResponse],
)
def get_medicamentos(
    receta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_medicamentos_by_receta_service(
            db,
            receta_id,
            current_user.veterinaria_id,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )   
    
@router.put(
    "/medicamentos/{medicamento_id}",
    response_model=RecetaMedicamentoResponse,
)
def update_medicamento(
    medicamento_id: int,
    medicamento_data: RecetaMedicamentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    medicamento = update_receta_medicamento_service(
        db,
        medicamento_id,
        medicamento_data,
    )

    if medicamento is None:
        raise HTTPException(
            status_code=404,
            detail="Medicamento no encontrado",
        )

    return medicamento

@router.delete(
    "/medicamentos/{medicamento_id}",
)
def delete_medicamento(
    medicamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.VETERINARIO,
        )
    ),
):

    eliminado = delete_receta_medicamento_service(
        db,
        medicamento_id,
    )


    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Medicamento no encontrado",
        )


    return {
        "message": "Medicamento eliminado correctamente"
    }