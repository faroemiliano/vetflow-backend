from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.gasto_schemas import (
    GastoCreate,
    GastoUpdate,
    GastoResponse,
)

from app.services.gasto_service import (
    create_gasto_service,
    delete_gasto_service,
    get_gasto_service,
    get_gastos_service,
    update_gasto_service,
)

from app.api.dependencies.auth import (
    get_current_user,
)

from app.models.usuario import Usuario


router = APIRouter(
    prefix="/gastos",
    tags=["Gastos"],
)


@router.get(
    "/",
    response_model=list[GastoResponse],
)
def get_gastos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    return get_gastos_service(
        db,
        current_user.veterinaria_id,
    )



@router.post(
    "/",
    response_model=GastoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_gasto(
    gasto_data: GastoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return create_gasto_service(
            db,
            gasto_data,
            current_user.id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



@router.get(
    "/{gasto_id}",
    response_model=GastoResponse,
)
def get_gasto(
    gasto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return get_gasto_service(
            db,
            gasto_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )



@router.patch(
    "/{gasto_id}",
    response_model=GastoResponse,
)
def update_gasto(
    gasto_id: int,
    gasto_data: GastoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        return update_gasto_service(
            db,
            gasto_id,
            gasto_data,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )



@router.delete(
    "/{gasto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_gasto(
    gasto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):

    try:

        delete_gasto_service(
            db,
            gasto_id,
            current_user.veterinaria_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e))