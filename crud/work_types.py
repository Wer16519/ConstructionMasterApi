from sqlalchemy.orm import Session
from models import WorkType
from schemas import WorkTypeCreate
from typing import List, Optional


def get_work_type(db: Session, work_type_id: int):
    return db.query(WorkType).filter(WorkType.work_type_id == work_type_id).first()


def get_work_types(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None):
    query = db.query(WorkType)
    if category_id:
        query = query.filter(WorkType.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def create_work_type(db: Session, work_type: WorkTypeCreate):
    db_work_type = WorkType(**work_type.model_dump())
    db.add(db_work_type)
    db.commit()
    db.refresh(db_work_type)
    return db_work_type


def update_work_type(db: Session, work_type_id: int, work_type_data: dict):
    db_work_type = get_work_type(db, work_type_id)
    if db_work_type:
        for key, value in work_type_data.items():
            setattr(db_work_type, key, value)
        db.commit()
        db.refresh(db_work_type)
    return db_work_type


def delete_work_type(db: Session, work_type_id: int):
    db_work_type = get_work_type(db, work_type_id)
    if db_work_type:
        db.delete(db_work_type)
        db.commit()
        return True
    return False