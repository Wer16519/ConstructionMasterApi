from sqlalchemy.orm import Session
from models import WorkCategory
from schemas import WorkCategoryCreate
from typing import List, Optional


def get_work_category(db: Session, category_id: int):
    return db.query(WorkCategory).filter(WorkCategory.category_id == category_id).first()


def get_work_categories(db: Session, skip: int = 0, limit: int = 100, parent_id: Optional[int] = None):
    query = db.query(WorkCategory)
    if parent_id is not None:
        query = query.filter(WorkCategory.parent_category_id == parent_id)
    return query.offset(skip).limit(limit).all()


def create_work_category(db: Session, category: WorkCategoryCreate):
    db_category = WorkCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_work_category(db: Session, category_id: int, category_data: dict):
    db_category = get_work_category(db, category_id)
    if db_category:
        for key, value in category_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_work_category(db: Session, category_id: int):
    db_category = get_work_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False