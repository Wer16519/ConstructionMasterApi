from sqlalchemy.orm import Session
from models import QualityControl
from schemas import QualityControlCreate
from typing import List, Optional


def get_quality_control(db: Session, qc_id: int):
    return db.query(QualityControl).filter(QualityControl.qc_id == qc_id).first()


def get_quality_controls(db: Session, skip: int = 0, limit: int = 100, object_id: Optional[int] = None):
    query = db.query(QualityControl)
    if object_id:
        query = query.filter(QualityControl.object_id == object_id)
    return query.order_by(QualityControl.inspection_date.desc()).offset(skip).limit(limit).all()


def create_quality_control(db: Session, qc: QualityControlCreate):
    db_qc = QualityControl(**qc.model_dump())
    db.add(db_qc)
    db.commit()
    db.refresh(db_qc)
    return db_qc


def update_quality_control(db: Session, qc_id: int, qc_data: dict):
    db_qc = get_quality_control(db, qc_id)
    if db_qc:
        for key, value in qc_data.items():
            setattr(db_qc, key, value)
        db.commit()
        db.refresh(db_qc)
    return db_qc


def delete_quality_control(db: Session, qc_id: int):
    db_qc = get_quality_control(db, qc_id)
    if db_qc:
        db.delete(db_qc)
        db.commit()
        return True
    return False