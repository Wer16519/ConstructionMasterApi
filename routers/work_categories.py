from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import WorkCategoryCreate, WorkCategoryResponse, ApiResponse
import crud

router = APIRouter(prefix="/work-categories", tags=["work_categories"])


@router.get("/", response_model=List[WorkCategoryResponse])
def get_work_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_work_categories(db, skip=skip, limit=limit, parent_id=parent_id)


@router.get("/{category_id}", response_model=WorkCategoryResponse)
def get_work_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_work_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Work category not found")
    return category


@router.post("/", response_model=WorkCategoryResponse, status_code=201)
def create_work_category(category: WorkCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_work_category(db, category)


@router.put("/{category_id}", response_model=WorkCategoryResponse)
def update_work_category(category_id: int, category_data: dict, db: Session = Depends(get_db)):
    category = crud.update_work_category(db, category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Work category not found")
    return category


@router.delete("/{category_id}", response_model=ApiResponse)
def delete_work_category(category_id: int, db: Session = Depends(get_db)):
    success = crud.delete_work_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work category not found")
    return ApiResponse(success=True, message="Work category deleted successfully")