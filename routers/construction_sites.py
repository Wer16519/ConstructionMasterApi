from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import ConstructionSiteCreate, ConstructionSiteResponse, ApiResponse
import crud

router = APIRouter(prefix="/sites", tags=["construction_sites"])

@router.get("/", response_model=List[ConstructionSiteResponse])
def get_sites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_sites(db, skip=skip, limit=limit, status=status)

@router.get("/{site_id}", response_model=ConstructionSiteResponse)
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = crud.get_site(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.get("/{site_id}/details")
def get_site_details(site_id: int, db: Session = Depends(get_db)):
    site_data = crud.get_site_with_objects(db, site_id)
    if not site_data:
        raise HTTPException(status_code=404, detail="Site not found")
    return site_data

@router.post("/", response_model=ConstructionSiteResponse, status_code=201)
def create_site(site: ConstructionSiteCreate, db: Session = Depends(get_db)):
    return crud.create_site(db, site)

@router.put("/{site_id}", response_model=ConstructionSiteResponse)
def update_site(site_id: int, site_data: dict, db: Session = Depends(get_db)):
    site = crud.update_site(db, site_id, site_data)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.delete("/{site_id}", response_model=ApiResponse)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    success = crud.delete_site(db, site_id)
    if not success:
        raise HTTPException(status_code=404, detail="Site not found")
    return ApiResponse(success=True, message="Site deleted successfully")