from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import (
    MaterialCreate, MaterialResponse,
    MaterialRequisitionCreate, MaterialRequisitionResponse,
    ApiResponse
)
import crud

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_model=List[MaterialResponse])
def get_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    low_stock: bool = False,
    db: Session = Depends(get_db)
):
    return crud.get_materials(db, skip=skip, limit=limit, low_stock=low_stock)

@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = crud.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.post("/", response_model=MaterialResponse, status_code=201)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)

@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(material_id: int, material_data: dict, db: Session = Depends(get_db)):
    material = crud.update_material(db, material_id, material_data)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.get("/requisitions/", response_model=List[MaterialRequisitionResponse])
def get_requisitions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    work_order_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_material_requisitions(db, skip=skip, limit=limit, work_order_id=work_order_id)

@router.post("/requisitions/", response_model=MaterialRequisitionResponse, status_code=201)
def create_requisition(requisition: MaterialRequisitionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_material_requisition(db, requisition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))