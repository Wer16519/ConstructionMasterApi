from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Material, MaterialRequisition, MaterialRequisition
from schemas import MaterialCreate, MaterialRequisitionCreate
from typing import List, Optional


def get_material(db: Session, material_id: int):
    return db.query(Material).filter(Material.material_id == material_id).first()


def get_materials(db: Session, skip: int = 0, limit: int = 100, low_stock: bool = False):
    query = db.query(Material)
    if low_stock:
        query = query.filter(Material.stock_quantity < Material.minimum_stock)
    return query.offset(skip).limit(limit).all()


def create_material(db: Session, material: MaterialCreate):
    db_material = Material(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def update_material(db: Session, material_id: int, material_data: dict):
    db_material = get_material(db, material_id)
    if db_material:
        for key, value in material_data.items():
            setattr(db_material, key, value)
        db.commit()
        db.refresh(db_material)
    return db_material


def get_material_requisition(db: Session, requisition_id: int):
    return db.query(MaterialRequisition).filter(MaterialRequisition.requisition_id == requisition_id).first()


def get_material_requisitions(db: Session, skip: int = 0, limit: int = 100, work_order_id: Optional[int] = None):
    query = db.query(MaterialRequisition)
    if work_order_id:
        query = query.filter(MaterialRequisition.work_order_id == work_order_id)
    return query.order_by(MaterialRequisition.requisition_date.desc()).offset(skip).limit(limit).all()


def create_material_requisition(db: Session, requisition: MaterialRequisitionCreate):
    from datetime import date
    import random

    req_number = f"REQ-{date.today().strftime('%Y%m%d')}-{random.randint(1, 9999):04d}"
    db_requisition = MaterialRequisition(
        **requisition.model_dump(),
        requisition_number=req_number
    )
    db.add(db_requisition)
    db.commit()
    db.refresh(db_requisition)
    return db_requisition


def get_total_materials_value(db: Session):
    result = db.query(func.sum(Material.current_price * Material.stock_quantity)).scalar()
    return result or 0