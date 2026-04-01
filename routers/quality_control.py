from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import QualityControlCreate, QualityControlResponse, ApiResponse
import crud

router = APIRouter(prefix="/quality-control", tags=["quality_control"])


@router.get("/", response_model=List[QualityControlResponse])
def get_quality_controls(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    object_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_quality_controls(db, skip=skip, limit=limit, object_id=object_id)


@router.get("/{qc_id}", response_model=QualityControlResponse)
def get_quality_control(qc_id: int, db: Session = Depends(get_db)):
    qc = crud.get_quality_control(db, qc_id)
    if not qc:
        raise HTTPException(status_code=404, detail="Quality control record not found")
    return qc


@router.post("/", response_model=QualityControlResponse, status_code=201)
def create_quality_control(qc: QualityControlCreate, db: Session = Depends(get_db)):
    return crud.create_quality_control(db, qc)


@router.put("/{qc_id}", response_model=QualityControlResponse)
def update_quality_control(qc_id: int, qc_data: dict, db: Session = Depends(get_db)):
    qc = crud.update_quality_control(db, qc_id, qc_data)
    if not qc:
        raise HTTPException(status_code=404, detail="Quality control record not found")
    return qc


@router.delete("/{qc_id}", response_model=ApiResponse)
def delete_quality_control(qc_id: int, db: Session = Depends(get_db)):
    success = crud.delete_quality_control(db, qc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quality control record not found")
    return ApiResponse(success=True, message="Quality control record deleted successfully")