from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import WorkTypeCreate, WorkTypeResponse, ApiResponse
import crud

router = APIRouter(prefix="/work-types", tags=["work_types"])


@router.get("/", response_model=List[WorkTypeResponse])
def get_work_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_work_types(db, skip=skip, limit=limit, category_id=category_id)


@router.get("/{work_type_id}", response_model=WorkTypeResponse)
def get_work_type(work_type_id: int, db: Session = Depends(get_db)):
    work_type = crud.get_work_type(db, work_type_id)
    if not work_type:
        raise HTTPException(status_code=404, detail="Work type not found")
    return work_type


@router.post("/", response_model=WorkTypeResponse, status_code=201)
def create_work_type(work_type: WorkTypeCreate, db: Session = Depends(get_db)):
    return crud.create_work_type(db, work_type)


@router.put("/{work_type_id}", response_model=WorkTypeResponse)
def update_work_type(work_type_id: int, work_type_data: dict, db: Session = Depends(get_db)):
    work_type = crud.update_work_type(db, work_type_id, work_type_data)
    if not work_type:
        raise HTTPException(status_code=404, detail="Work type not found")
    return work_type


@router.delete("/{work_type_id}", response_model=ApiResponse)
def delete_work_type(work_type_id: int, db: Session = Depends(get_db)):
    success = crud.delete_work_type(db, work_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work type not found")
    return ApiResponse(success=True, message="Work type deleted successfully")