from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.mascota_schemas import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse,
)

from app.api.dependencies.auth import admin_or_recepcionista
from app.models.usuario import Usuario

from app.services.mascota_service import (
    create_mascota_service,
    get_mascota_service,
    get_mascotas_service,
    update_mascota_service,
    delete_mascota_service,
    get_mascotas_by_cliente_service,)

router = APIRouter(
    prefix=("/mascotas"),
    tags=["Mascotas"],
)



@router.post("/", response_model=MascotaResponse)
def create_mascota(
    mascota: MascotaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,):
    try:
        return create_mascota_service(db, mascota, current_user.veterinaria_id,)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.get("/", response_model=list[MascotaResponse])
def get_mascotas(
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,
    ):

    return get_mascotas_service(db, current_user.veterinaria_id)

    
@router.get("/{mascota_id}", response_model=MascotaResponse)
def get_mascota(
    mascota_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,):

    try:
        return get_mascota_service(db, mascota_id, current_user.veterinaria_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.put("/{mascota_id}", response_model=MascotaResponse)
def update_mascota(
    mascota_id: int, 
    mascota: MascotaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,):

    try:
        return update_mascota_service(db, mascota_id, mascota, current_user.veterinaria_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{mascota_id}")
def delete_mascota(
    mascota_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,):

    try:
        delete_mascota_service(db, mascota_id, current_user.veterinaria_id)
        return {"message": "Mascota eliminada exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/cliente/{cliente_id}", response_model=list[MascotaResponse])
def get_mascotas_by_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = admin_or_recepcionista,):

    try:
        return get_mascotas_by_cliente_service(db, cliente_id, current_user.veterinaria_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    