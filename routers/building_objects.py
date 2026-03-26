from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import BuildingObjectCreate, BuildingObjectResponse, ApiResponse
import crud

router = APIRouter(prefix="/objects", tags=["building_objects"])

@router.get("/", response_model=List[BuildingObjectResponse])
def get_objects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    site_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_objects(db, skip=skip, limit=limit, site_id=site_id)

@router.get("/{object_id}", response_model=BuildingObjectResponse)
def get_object(object_id: int, db: Session = Depends(get_db)):
    obj = crud.get_object(db, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj

@router.get("/{object_id}/details")
def get_object_details(object_id: int, db: Session = Depends(get_db)):
    obj_data = crud.get_object_with_orders(db, object_id)
    if not obj_data:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj_data

@router.post("/", response_model=BuildingObjectResponse, status_code=201)
def create_object(obj: BuildingObjectCreate, db: Session = Depends(get_db)):
    return crud.create_object(db, obj)

@router.put("/{object_id}", response_model=BuildingObjectResponse)
def update_object(object_id: int, object_data: dict, db: Session = Depends(get_db)):
    obj = crud.update_object(db, object_id, object_data)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj

@router.delete("/{object_id}", response_model=ApiResponse)
def delete_object(object_id: int, db: Session = Depends(get_db)):
    success = crud.delete_object(db, object_id)
    if not success:
        raise HTTPException(status_code=404, detail="Object not found")
    return ApiResponse(success=True, message="Object deleted successfully")