from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import MaterialIssueCreate, MaterialIssueResponse, ApiResponse
import crud

router = APIRouter(prefix="/material-issues", tags=["material_issues"])


@router.get("/", response_model=List[MaterialIssueResponse])
def get_material_issues(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    requisition_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_material_issues(db, skip=skip, limit=limit, requisition_id=requisition_id)


@router.get("/{issue_id}", response_model=MaterialIssueResponse)
def get_material_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = crud.get_material_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Material issue not found")
    return issue


@router.post("/", response_model=MaterialIssueResponse, status_code=201)
def create_material_issue(issue: MaterialIssueCreate, db: Session = Depends(get_db)):
    return crud.create_material_issue(db, issue)


@router.post("/{issue_id}/return", response_model=ApiResponse)
def return_material(
    issue_id: int,
    return_quantity: float,
    return_reason: str,
    db: Session = Depends(get_db)
):
    issue = crud.process_material_return(db, issue_id, return_quantity, return_reason)
    if not issue:
        raise HTTPException(status_code=404, detail="Material issue not found")
    return ApiResponse(success=True, message="Material returned successfully")