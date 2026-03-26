from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import (
    DailyReportCreate, DailyReportResponse,
    PaymentRequestCreate, PaymentRequestResponse,
    WorkAcceptanceCreate, WorkAcceptanceResponse,
    ProjectProgress, ApiResponse
)
from datetime import date
import crud

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/daily", response_model=List[DailyReportResponse])
def get_daily_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    object_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_daily_reports(db, skip=skip, limit=limit, object_id=object_id)

@router.post("/daily", response_model=DailyReportResponse, status_code=201)
def create_daily_report(report: DailyReportCreate, db: Session = Depends(get_db)):
    return crud.create_daily_report(db, report)

@router.get("/payments", response_model=List[PaymentRequestResponse])
def get_payment_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_payment_requests(db, skip=skip, limit=limit, status=status)

@router.post("/payments", response_model=PaymentRequestResponse, status_code=201)
def create_payment_request(payment: PaymentRequestCreate, db: Session = Depends(get_db)):
    return crud.create_payment_request(db, payment.model_dump())

@router.get("/acceptances", response_model=List[WorkAcceptanceResponse])
def get_acceptances(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    work_order_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_work_acceptances(db, skip=skip, limit=limit, work_order_id=work_order_id)

@router.post("/acceptances", response_model=WorkAcceptanceResponse, status_code=201)
def create_acceptance(acceptance: WorkAcceptanceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_work_acceptance(db, acceptance.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/project-progress/{object_id}", response_model=ProjectProgress)
def get_project_progress(object_id: int, db: Session = Depends(get_db)):
    progress = crud.get_project_progress_func(db, object_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Object not found")
    return progress