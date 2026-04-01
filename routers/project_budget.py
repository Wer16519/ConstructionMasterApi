from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import ProjectBudgetCreate, ProjectBudgetResponse, ApiResponse
import crud

router = APIRouter(prefix="/budget", tags=["project_budget"])


@router.get("/", response_model=List[ProjectBudgetResponse])
def get_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    object_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_project_budgets(db, skip=skip, limit=limit, object_id=object_id)


@router.get("/{budget_id}", response_model=ProjectBudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = crud.get_project_budget(db, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget record not found")
    return budget


@router.get("/object/{object_id}/summary")
def get_object_budget_summary(object_id: int, db: Session = Depends(get_db)):
    return crud.get_object_budget_summary(db, object_id)


@router.post("/", response_model=ProjectBudgetResponse, status_code=201)
def create_budget(budget: ProjectBudgetCreate, db: Session = Depends(get_db)):
    return crud.create_project_budget(db, budget)


@router.put("/{budget_id}", response_model=ProjectBudgetResponse)
def update_budget(budget_id: int, budget_data: dict, db: Session = Depends(get_db)):
    budget = crud.update_project_budget(db, budget_id, budget_data)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget record not found")
    return budget


@router.delete("/{budget_id}", response_model=ApiResponse)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    success = crud.delete_project_budget(db, budget_id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget record not found")
    return ApiResponse(success=True, message="Budget record deleted successfully")