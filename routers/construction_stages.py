from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import ConstructionStageCreate, ConstructionStageResponse, ApiResponse
import crud

router = APIRouter(prefix="/construction-stages", tags=["construction_stages"])


@router.get("/", response_model=List[ConstructionStageResponse])
def get_stages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    object_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_construction_stages(db, skip=skip, limit=limit, object_id=object_id)


@router.get("/{stage_id}", response_model=ConstructionStageResponse)
def get_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.get_construction_stage(db, stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Construction stage not found")
    return stage


@router.post("/", response_model=ConstructionStageResponse, status_code=201)
def create_stage(stage: ConstructionStageCreate, db: Session = Depends(get_db)):
    return crud.create_construction_stage(db, stage)


@router.put("/{stage_id}", response_model=ConstructionStageResponse)
def update_stage(stage_id: int, stage_data: dict, db: Session = Depends(get_db)):
    stage = crud.update_construction_stage(db, stage_id, stage_data)
    if not stage:
        raise HTTPException(status_code=404, detail="Construction stage not found")
    return stage


@router.post("/{stage_id}/start", response_model=ApiResponse)
def start_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.start_stage(db, stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found or cannot be started")
    return ApiResponse(success=True, message="Stage started successfully")


@router.post("/{stage_id}/complete", response_model=ApiResponse)
def complete_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.complete_stage(db, stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found or cannot be completed")
    return ApiResponse(success=True, message="Stage completed successfully")


@router.delete("/{stage_id}", response_model=ApiResponse)
def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    success = crud.delete_construction_stage(db, stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Construction stage not found")
    return ApiResponse(success=True, message="Construction stage deleted successfully")