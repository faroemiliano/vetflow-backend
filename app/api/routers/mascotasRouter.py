from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.mascota import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse,
)

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

VETERINARIA_ID = 2

@router.post("/", response_model=MascotaResponse)
def create_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    try:
        return create_mascota_service(db, mascota, VETERINARIA_ID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.get("/", response_model=list[MascotaResponse])
def get_mascotas(db: Session = Depends(get_db)):
    return get_mascotas_service(db, VETERINARIA_ID)

    
@router.get("/{mascota_id}", response_model=MascotaResponse)
def get_mascota(mascota_id: int, db: Session = Depends(get_db)):
    try:
        return get_mascota_service(db, mascota_id, VETERINARIA_ID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.put("/{mascota_id}", response_model=MascotaResponse)
def update_mascota(mascota_id: int, mascota: MascotaUpdate, db: Session = Depends(get_db)):
    try:
        return update_mascota_service(db, mascota_id, mascota, VETERINARIA_ID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{mascota_id}")
def delete_mascota(mascota_id: int, db: Session = Depends(get_db)):
    try:
        delete_mascota_service(db, mascota_id, VETERINARIA_ID)
        return {"message": "Mascota eliminada exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/cliente/{cliente_id}", response_model=list[MascotaResponse])
def get_mascotas_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        return get_mascotas_by_cliente_service(db, cliente_id, VETERINARIA_ID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    