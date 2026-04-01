from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database import get_db
from schemas import SafetyReportCreate, SafetyReportResponse, ApiResponse
import crud

router = APIRouter(prefix="/safety-reports", tags=["safety_reports"])


@router.get("/", response_model=List[SafetyReportResponse])
def get_safety_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    site_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_safety_reports(db, skip=skip, limit=limit, site_id=site_id)


@router.get("/{report_id}", response_model=SafetyReportResponse)
def get_safety_report(report_id: int, db: Session = Depends(get_db)):
    report = crud.get_safety_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    return report


@router.post("/", response_model=SafetyReportResponse, status_code=201)
def create_safety_report(report: SafetyReportCreate, db: Session = Depends(get_db)):
    return crud.create_safety_report(db, report)


@router.put("/{report_id}", response_model=SafetyReportResponse)
def update_safety_report(report_id: int, report_data: dict, db: Session = Depends(get_db)):
    report = crud.update_safety_report(db, report_id, report_data)
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    return report


@router.post("/{report_id}/close", response_model=ApiResponse)
def close_safety_report(report_id: int, db: Session = Depends(get_db)):
    report = crud.close_safety_report(db, report_id, date.today())
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    return ApiResponse(success=True, message="Safety report closed successfully")


@router.delete("/{report_id}", response_model=ApiResponse)
def delete_safety_report(report_id: int, db: Session = Depends(get_db)):
    success = crud.delete_safety_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Safety report not found")
    return ApiResponse(success=True, message="Safety report deleted successfully")