from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import DashboardStats, ApiResponse
import crud

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return DashboardStats(
        total_contractors=crud.get_contractor_count(db),
        total_sites=crud.get_site_count(db),
        total_objects=crud.get_object_count(db),
        active_work_orders=crud.get_active_work_orders_count(db),
        completed_work_orders=crud.get_completed_work_orders_count(db),
        total_materials_value=crud.get_total_materials_value(db),
        pending_payments=crud.get_pending_payments_total(db),
        total_paid=crud.get_total_paid(db)
    )