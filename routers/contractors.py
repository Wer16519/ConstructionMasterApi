from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import ContractorCreate, ContractorResponse, ApiResponse
import crud

router = APIRouter(prefix="/contractors", tags=["contractors"])

@router.get("/", response_model=List[ContractorResponse])
def get_contractors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    return crud.get_contractors(db, skip=skip, limit=limit, active_only=active_only)

@router.get("/{contractor_id}", response_model=ContractorResponse)
def get_contractor(contractor_id: int, db: Session = Depends(get_db)):
    contractor = crud.get_contractor(db, contractor_id)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor

@router.post("/", response_model=ContractorResponse, status_code=201)
def create_contractor(contractor: ContractorCreate, db: Session = Depends(get_db)):
    return crud.create_contractor(db, contractor)

@router.put("/{contractor_id}", response_model=ContractorResponse)
def update_contractor(contractor_id: int, contractor_data: dict, db: Session = Depends(get_db)):
    contractor = crud.update_contractor(db, contractor_id, contractor_data)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor

@router.delete("/{contractor_id}", response_model=ApiResponse)
def delete_contractor(contractor_id: int, db: Session = Depends(get_db)):
    success = crud.delete_contractor(db, contractor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return ApiResponse(success=True, message="Contractor deleted successfully")