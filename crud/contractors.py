from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Contractor
from schemas import ContractorCreate
from typing import List, Optional

def get_contractor(db: Session, contractor_id: int):
    return db.query(Contractor).filter(Contractor.contractor_id == contractor_id).first()

def get_contractors(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False):
    query = db.query(Contractor)
    if active_only:
        query = query.filter(Contractor.is_active == True)
    return query.offset(skip).limit(limit).all()

def create_contractor(db: Session, contractor: ContractorCreate):
    db_contractor = Contractor(**contractor.model_dump())
    db.add(db_contractor)
    db.commit()
    db.refresh(db_contractor)
    return db_contractor

def update_contractor(db: Session, contractor_id: int, contractor_data: dict):
    db_contractor = get_contractor(db, contractor_id)
    if db_contractor:
        for key, value in contractor_data.items():
            setattr(db_contractor, key, value)
        db.commit()
        db.refresh(db_contractor)
    return db_contractor

def delete_contractor(db: Session, contractor_id: int):
    db_contractor = get_contractor(db, contractor_id)
    if db_contractor:
        db.delete(db_contractor)
        db.commit()
        return True
    return False

def get_contractor_count(db: Session):
    return db.query(func.count(Contractor.contractor_id)).scalar()