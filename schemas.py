from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal


# Contractor schemas
class ContractorBase(BaseModel):
    name: str
    inn: str
    kpp: Optional[str] = None
    ogrn: Optional[str] = None
    legal_address: str
    actual_address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    bank_name: Optional[str] = None
    bank_bik: Optional[str] = None
    bank_account: Optional[str] = None
    is_active: Optional[bool] = True


class ContractorCreate(ContractorBase):
    pass


class ContractorResponse(ContractorBase):
    contractor_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Construction Site schemas
class ConstructionSiteBase(BaseModel):
    name: str
    address: str
    cadastral_number: Optional[str] = None
    area: Optional[Decimal] = None
    start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    site_status: Optional[str] = 'planning'
    contractor_id: Optional[int] = None


class ConstructionSiteCreate(ConstructionSiteBase):
    pass


class ConstructionSiteResponse(ConstructionSiteBase):
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Building Object schemas
class BuildingObjectBase(BaseModel):
    site_id: int
    object_code: str
    name: str
    object_type: str
    floors: Optional[int] = None
    total_area: Optional[Decimal] = None
    construction_volume: Optional[Decimal] = None
    object_status: Optional[str] = 'design'


class BuildingObjectCreate(BuildingObjectBase):
    pass


class BuildingObjectResponse(BuildingObjectBase):
    object_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Work Order schemas
class WorkOrderBase(BaseModel):
    object_id: int
    contractor_id: int
    work_type_id: int
    quantity: Decimal
    unit_price: Optional[Decimal] = None
    order_date: date
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    order_status: Optional[str] = 'draft'
    supervisor_name: Optional[str] = None
    notes: Optional[str] = None


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderResponse(WorkOrderBase):
    work_order_id: int
    order_number: str
    total_amount: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Material schemas
class MaterialBase(BaseModel):
    code: str
    name: str
    unit_of_measure: Optional[str] = None
    current_price: Optional[Decimal] = None
    stock_quantity: Optional[Decimal] = 0
    minimum_stock: Optional[Decimal] = 0
    supplier_id: Optional[int] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    material_id: int

    model_config = ConfigDict(from_attributes=True)


# Material Requisition schemas
class MaterialRequisitionBase(BaseModel):
    work_order_id: int
    material_id: int
    required_quantity: Decimal
    requisition_date: date
    required_date: Optional[date] = None


class MaterialRequisitionCreate(MaterialRequisitionBase):
    pass


class MaterialRequisitionResponse(MaterialRequisitionBase):
    requisition_id: int
    requisition_number: str
    issued_quantity: Decimal
    requisition_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Work Acceptance schemas
class WorkAcceptanceBase(BaseModel):
    work_order_id: int
    acceptance_date: date
    actual_quantity: Decimal
    accepted_quantity: Decimal
    rejection_quantity: Optional[Decimal] = 0
    rejection_reason: Optional[str] = None
    quality_score: Optional[int] = Field(None, ge=1, le=5)
    accepted_by: Optional[str] = None


class WorkAcceptanceCreate(WorkAcceptanceBase):
    pass


class WorkAcceptanceResponse(WorkAcceptanceBase):
    acceptance_id: int
    acceptance_number: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Payment Request schemas
class PaymentRequestBase(BaseModel):
    work_order_id: int
    contractor_id: int
    amount: Decimal
    request_date: date
    notes: Optional[str] = None


class PaymentRequestCreate(PaymentRequestBase):
    pass


class PaymentRequestResponse(PaymentRequestBase):
    payment_request_id: int
    request_number: str
    payment_status: str
    paid_amount: Decimal
    payment_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Daily Report schemas
class DailyReportBase(BaseModel):
    report_date: date
    object_id: int
    weather_conditions: Optional[str] = None
    temperature: Optional[Decimal] = None
    workers_count: Optional[int] = None
    equipment_count: Optional[int] = None
    work_performed: Optional[str] = None
    issues_encountered: Optional[str] = None
    materials_used: Optional[str] = None
    created_by: Optional[str] = None


class DailyReportCreate(DailyReportBase):
    pass


class DailyReportResponse(DailyReportBase):
    daily_report_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Dashboard schemas
class DashboardStats(BaseModel):
    total_contractors: int
    total_sites: int
    total_objects: int
    active_work_orders: int
    completed_work_orders: int
    total_materials_value: Decimal
    pending_payments: Decimal
    total_paid: Decimal


class ProjectProgress(BaseModel):
    object_name: str
    total_planned_quantity: Decimal
    total_completed_quantity: Decimal
    completion_percentage: Decimal
    total_budget: Decimal
    actual_cost: Decimal
    budget_variance: Decimal


class SiteStats(BaseModel):
    site_name: str
    objects_count: int
    orders_count: int
    total_cost: Decimal
    avg_quality: Optional[float]


# Common response
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None