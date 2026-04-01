from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database import get_db
from schemas import (
    EquipmentCreate, EquipmentResponse,
    EquipmentAssignmentCreate, EquipmentAssignmentResponse,
    ApiResponse
)
import crud

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/", response_model=List[EquipmentResponse])
def get_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_equipment_list(db, skip=skip, limit=limit, status=status)


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_item(equipment_id: int, db: Session = Depends(get_db)):
    equipment = crud.get_equipment(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    return crud.create_equipment(db, equipment)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(equipment_id: int, equipment_data: dict, db: Session = Depends(get_db)):
    equipment = crud.update_equipment(db, equipment_id, equipment_data)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.delete("/{equipment_id}", response_model=ApiResponse)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    success = crud.delete_equipment(db, equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return ApiResponse(success=True, message="Equipment deleted successfully")


@router.get("/assignments/", response_model=List[EquipmentAssignmentResponse])
def get_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    equipment_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_equipment_assignments(db, skip=skip, limit=limit, equipment_id=equipment_id)


@router.post("/assignments/", response_model=EquipmentAssignmentResponse, status_code=201)
def create_assignment(assignment: EquipmentAssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_equipment_assignment(db, assignment)


@router.post("/assignments/{assignment_id}/return", response_model=ApiResponse)
def return_equipment_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = crud.return_equipment(db, assignment_id, date.today())
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return ApiResponse(success=True, message="Equipment returned successfully")