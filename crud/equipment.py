from sqlalchemy.orm import Session
from models import Equipment, EquipmentAssignment
from schemas import EquipmentCreate, EquipmentAssignmentCreate
from typing import List, Optional
from datetime import date


def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()


def get_equipment_list(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(Equipment)
    if status:
        query = query.filter(Equipment.status == status)
    return query.offset(skip).limit(limit).all()


def create_equipment(db: Session, equipment: EquipmentCreate):
    db_equipment = Equipment(**equipment.model_dump())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def update_equipment(db: Session, equipment_id: int, equipment_data: dict):
    db_equipment = get_equipment(db, equipment_id)
    if db_equipment:
        for key, value in equipment_data.items():
            setattr(db_equipment, key, value)
        db.commit()
        db.refresh(db_equipment)
    return db_equipment


def delete_equipment(db: Session, equipment_id: int):
    db_equipment = get_equipment(db, equipment_id)
    if db_equipment:
        db.delete(db_equipment)
        db.commit()
        return True
    return False


def get_equipment_assignments(db: Session, skip: int = 0, limit: int = 100, equipment_id: Optional[int] = None):
    query = db.query(EquipmentAssignment)
    if equipment_id:
        query = query.filter(EquipmentAssignment.equipment_id == equipment_id)
    return query.offset(skip).limit(limit).all()


def create_equipment_assignment(db: Session, assignment: EquipmentAssignmentCreate):
    db_assignment = EquipmentAssignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    # Update equipment status
    equipment = get_equipment(db, assignment.equipment_id)
    if equipment:
        equipment.status = 'in_use'
        db.commit()

    return db_assignment


def return_equipment(db: Session, assignment_id: int, return_date: date):
    db_assignment = db.query(EquipmentAssignment).filter(
        EquipmentAssignment.assignment_id == assignment_id
    ).first()

    if db_assignment:
        db_assignment.actual_return_date = return_date
        db.commit()
        db.refresh(db_assignment)

        # Check if equipment has other active assignments
        equipment = get_equipment(db, db_assignment.equipment_id)
        if equipment:
            active_assignments = db.query(EquipmentAssignment).filter(
                EquipmentAssignment.equipment_id == equipment.equipment_id,
                EquipmentAssignment.actual_return_date.is_(None)
            ).count()

            if active_assignments == 0:
                equipment.status = 'available'
                db.commit()

        return db_assignment
    return None