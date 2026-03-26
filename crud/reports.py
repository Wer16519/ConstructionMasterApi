from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import (
    WorkOrder, WorkAcceptance, PaymentRequest,
    BuildingObject, ConstructionSite, DailyReport
)
from schemas import DailyReportCreate, ProjectProgress
from typing import List, Optional
from datetime import date


def get_daily_reports(db: Session, skip: int = 0, limit: int = 100, object_id: Optional[int] = None):
    query = db.query(DailyReport)
    if object_id:
        query = query.filter(DailyReport.object_id == object_id)
    return query.order_by(DailyReport.report_date.desc()).offset(skip).limit(limit).all()


def create_daily_report(db: Session, report: DailyReportCreate):
    db_report = DailyReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_payment_requests(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(PaymentRequest)
    if status:
        query = query.filter(PaymentRequest.payment_status == status)
    return query.order_by(PaymentRequest.request_date.desc()).offset(skip).limit(limit).all()


def create_payment_request(db: Session, payment_data: dict):
    from datetime import date
    import random

    req_number = f"PAY-{date.today().strftime('%Y%m%d')}-{random.randint(1, 9999):04d}"
    db_payment = PaymentRequest(
        **payment_data,
        request_number=req_number
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_work_acceptances(db: Session, skip: int = 0, limit: int = 100, work_order_id: Optional[int] = None):
    query = db.query(WorkAcceptance)
    if work_order_id:
        query = query.filter(WorkAcceptance.work_order_id == work_order_id)
    return query.order_by(WorkAcceptance.acceptance_date.desc()).offset(skip).limit(limit).all()


def create_work_acceptance(db: Session, acceptance_data: dict):
    from datetime import date
    import random

    acc_number = f"ACC-{date.today().strftime('%Y%m%d')}-{random.randint(1, 9999):04d}"
    db_acceptance = WorkAcceptance(
        **acceptance_data,
        acceptance_number=acc_number
    )
    db.add(db_acceptance)
    db.commit()
    db.refresh(db_acceptance)
    return db_acceptance


def get_project_progress_func(db: Session, object_id: int):
    from sqlalchemy import text
    result = db.execute(
        text("SELECT * FROM get_project_progress(:p1)"),
        {"p1": object_id}
    ).fetchone()

    if result:
        return ProjectProgress(
            object_name=result[0],
            total_planned_quantity=result[1],
            total_completed_quantity=result[2],
            completion_percentage=result[3],
            total_budget=result[4],
            actual_cost=result[5],
            budget_variance=result[6]
        )
    return None


def get_pending_payments_total(db: Session):
    result = db.query(func.sum(PaymentRequest.amount - PaymentRequest.paid_amount)).filter(
        PaymentRequest.payment_status.in_(['pending', 'approved', 'partially_paid'])
    ).scalar()
    return result or 0


def get_total_paid(db: Session):
    result = db.query(func.sum(PaymentRequest.paid_amount)).filter(
        PaymentRequest.payment_status == 'paid'
    ).scalar()
    return result or 0