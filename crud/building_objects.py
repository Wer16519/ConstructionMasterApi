from sqlalchemy.orm import Session
from sqlalchemy import func
from models import BuildingObject, WorkOrder
from schemas import BuildingObjectCreate
from typing import List, Optional

def get_object(db: Session, object_id: int):
    return db.query(BuildingObject).filter(BuildingObject.object_id == object_id).first()

def get_objects(db: Session, skip: int = 0, limit: int = 100, site_id: Optional[int] = None):
    query = db.query(BuildingObject)
    if site_id:
        query = query.filter(BuildingObject.site_id == site_id)
    return query.offset(skip).limit(limit).all()

def create_object(db: Session, obj: BuildingObjectCreate):
    db_object = BuildingObject(**obj.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def update_object(db: Session, object_id: int, object_data: dict):
    db_object = get_object(db, object_id)
    if db_object:
        for key, value in object_data.items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
    return db_object

def delete_object(db: Session, object_id: int):
    db_object = get_object(db, object_id)
    if db_object:
        db.delete(db_object)
        db.commit()
        return True
    return False

def get_object_with_orders(db: Session, object_id: int):
    obj = get_object(db, object_id)
    if obj:
        orders = db.query(WorkOrder).filter(WorkOrder.object_id == object_id).all()
        return {"object": obj, "orders": orders}
    return None

def get_object_count(db: Session):
    return db.query(func.count(BuildingObject.object_id)).scalar()