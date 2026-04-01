from sqlalchemy.orm import Session
from sqlalchemy import func
from models import ConstructionStage
from schemas import ConstructionStageCreate
from typing import List, Optional
from datetime import date


def get_construction_stage(db: Session, stage_id: int):
    return db.query(ConstructionStage).filter(ConstructionStage.stage_id == stage_id).first()


def get_construction_stages(db: Session, skip: int = 0, limit: int = 100, object_id: Optional[int] = None):
    query = db.query(ConstructionStage)
    if object_id:
        query = query.filter(ConstructionStage.object_id == object_id)
    return query.order_by(ConstructionStage.stage_order).offset(skip).limit(limit).all()


def create_construction_stage(db: Session, stage: ConstructionStageCreate):
    db_stage = ConstructionStage(**stage.model_dump())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


def update_construction_stage(db: Session, stage_id: int, stage_data: dict):
    db_stage = get_construction_stage(db, stage_id)
    if db_stage:
        for key, value in stage_data.items():
            setattr(db_stage, key, value)
        db.commit()
        db.refresh(db_stage)
    return db_stage


def delete_construction_stage(db: Session, stage_id: int):
    db_stage = get_construction_stage(db, stage_id)
    if db_stage:
        db.delete(db_stage)
        db.commit()
        return True
    return False


def start_stage(db: Session, stage_id: int):
    db_stage = get_construction_stage(db, stage_id)
    if db_stage and db_stage.stage_status == 'planned':
        db_stage.actual_start_date = date.today()
        db_stage.stage_status = 'in_progress'
        db.commit()
        db.refresh(db_stage)
        return db_stage
    return None


def complete_stage(db: Session, stage_id: int):
    db_stage = get_construction_stage(db, stage_id)
    if db_stage and db_stage.stage_status == 'in_progress':
        db_stage.actual_end_date = date.today()
        db_stage.stage_status = 'completed'
        db.commit()
        db.refresh(db_stage)
        return db_stage
    return None