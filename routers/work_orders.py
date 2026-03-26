from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import WorkOrderCreate, WorkOrderResponse, ApiResponse
import crud

router = APIRouter(prefix="/work-orders", tags=["work_orders"])


@router.get("/", response_model=List[WorkOrderResponse])
def get_work_orders(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=500),
        status: Optional[str] = None,
        object_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    return crud.get_work_orders(db, skip=skip, limit=limit, status=status, object_id=object_id)


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
def get_work_order(work_order_id: int, db: Session = Depends(get_db)):
    work_order = crud.get_work_order(db, work_order_id)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    return work_order


@router.post("/", response_model=WorkOrderResponse, status_code=201)
def create_work_order(work_order: WorkOrderCreate, db: Session = Depends(get_db)):
    return crud.create_work_order(db, work_order)


@router.put("/{work_order_id}", response_model=WorkOrderResponse)
def update_work_order(work_order_id: int, work_order_data: dict, db: Session = Depends(get_db)):
    work_order = crud.update_work_order(db, work_order_id, work_order_data)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    return work_order


@router.post("/{work_order_id}/complete", response_model=ApiResponse)
def complete_work_order(work_order_id: int, notes: Optional[str] = None, db: Session = Depends(get_db)):
    work_order = crud.get_work_order(db, work_order_id)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")

    crud.complete_work_order_proc(db, work_order_id, notes)
    return ApiResponse(success=True, message="Work order completed successfully")