from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import WorkOrder, WorkAcceptance
from schemas import WorkOrderCreate
from typing import List, Optional
from datetime import date

def get_work_order(db: Session, work_order_id: int):
    return db.query(WorkOrder).filter(WorkOrder.work_order_id == work_order_id).first()

def get_work_orders(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None, object_id: Optional[int] = None):
    query = db.query(WorkOrder)
    if status:
        query = query.filter(WorkOrder.order_status == status)
    if object_id:
        query = query.filter(WorkOrder.object_id == object_id)
    return query.order_by(WorkOrder.order_date.desc()).offset(skip).limit(limit).all()

def create_work_order(db: Session, work_order: WorkOrderCreate):
    db_work_order = WorkOrder(**work_order.model_dump())
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

def update_work_order(db: Session, work_order_id: int, work_order_data: dict):
    db_work_order = get_work_order(db, work_order_id)
    if db_work_order:
        for key, value in work_order_data.items():
            setattr(db_work_order, key, value)
        db.commit()
        db.refresh(db_work_order)
    return db_work_order

def complete_work_order_proc(db: Session, work_order_id: int, notes: str = None):
    from sqlalchemy import text
    db.execute(text("CALL complete_work_order(:p1, :p2)"), {"p1": work_order_id, "p2": notes})
    db.commit()
    return get_work_order(db, work_order_id)

def get_active_work_orders_count(db: Session):
    return db.query(func.count(WorkOrder.work_order_id)).filter(
        WorkOrder.order_status.in_(['approved', 'in_progress'])
    ).scalar()

def get_completed_work_orders_count(db: Session):
    return db.query(func.count(WorkOrder.work_order_id)).filter(
        WorkOrder.order_status == 'completed'
    ).scalar()