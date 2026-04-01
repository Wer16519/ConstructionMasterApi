from sqlalchemy.orm import Session
from models import SafetyReport
from schemas import SafetyReportCreate
from typing import List, Optional
from datetime import date


def get_safety_report(db: Session, report_id: int):
    return db.query(SafetyReport).filter(SafetyReport.report_id == report_id).first()


def get_safety_reports(db: Session, skip: int = 0, limit: int = 100, site_id: Optional[int] = None):
    query = db.query(SafetyReport)
    if site_id:
        query = query.filter(SafetyReport.site_id == site_id)
    return query.order_by(SafetyReport.report_date.desc()).offset(skip).limit(limit).all()


def create_safety_report(db: Session, report: SafetyReportCreate):
    db_report = SafetyReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_safety_report(db: Session, report_id: int, report_data: dict):
    db_report = get_safety_report(db, report_id)
    if db_report:
        for key, value in report_data.items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_safety_report(db: Session, report_id: int):
    db_report = get_safety_report(db, report_id)
    if db_report:
        db.delete(db_report)
        db.commit()
        return True
    return False


def close_safety_report(db: Session, report_id: int, closed_date: date):
    db_report = get_safety_report(db, report_id)
    if db_report:
        db_report.closed_date = closed_date
        db.commit()
        db.refresh(db_report)
        return db_report
    return None