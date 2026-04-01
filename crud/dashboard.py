# crud/dashboard.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (
    Contractor, ConstructionSite, BuildingObject,
    WorkOrder, Material, PaymentRequest
)


def get_contractor_count(db: Session):
    return db.query(func.count(Contractor.contractor_id)).scalar()


def get_site_count(db: Session):
    return db.query(func.count(ConstructionSite.site_id)).scalar()


def get_object_count(db: Session):
    return db.query(func.count(BuildingObject.object_id)).scalar()


def get_active_work_orders_count(db: Session):
    return db.query(func.count(WorkOrder.work_order_id)).filter(
        WorkOrder.order_status.in_(['approved', 'in_progress'])
    ).scalar()


def get_completed_work_orders_count(db: Session):
    return db.query(func.count(WorkOrder.work_order_id)).filter(
        WorkOrder.order_status == 'completed'
    ).scalar()


def get_total_materials_value(db: Session):
    result = db.query(func.sum(Material.current_price * Material.stock_quantity)).scalar()
    return result or 0


def get_pending_payments_total(db: Session):
    result = db.query(func.sum(PaymentRequest.amount - PaymentRequest.paid_amount)).filter(
        PaymentRequest.payment_status.in_(['pending', 'approved', 'partially_paid'])
    ).scalar()
    return result or 0


def get_total_paid(db: Session):
    result = db.query(func.sum(PaymentRequest.paid_amount)).filter(
        PaymentRequest.payment_status == 'paid'
    ).scalar()
    return result or 0