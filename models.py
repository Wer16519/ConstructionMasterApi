from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Contractor(Base):
    __tablename__ = "contractors"

    contractor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    inn = Column(String(12), unique=True, nullable=False)
    kpp = Column(String(9))
    ogrn = Column(String(15))
    legal_address = Column(Text, nullable=False)
    actual_address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    bank_name = Column(String(200))
    bank_bik = Column(String(9))
    bank_account = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class ConstructionSite(Base):
    __tablename__ = "construction_sites"

    site_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    cadastral_number = Column(String(50))
    area = Column(Numeric(12, 2))
    start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_end_date = Column(Date)
    site_status = Column(String(20), default='planning')
    contractor_id = Column(Integer, ForeignKey("contractors.contractor_id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class BuildingObject(Base):
    __tablename__ = "building_objects"

    object_id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("construction_sites.site_id", ondelete="CASCADE"))
    object_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    object_type = Column(String(50), nullable=False)
    floors = Column(Integer)
    total_area = Column(Numeric(12, 2))
    construction_volume = Column(Numeric(12, 2))
    object_status = Column(String(20), default='design')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class WorkOrder(Base):
    __tablename__ = "work_orders"

    work_order_id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    object_id = Column(Integer, ForeignKey("building_objects.object_id"))
    contractor_id = Column(Integer, ForeignKey("contractors.contractor_id"))
    work_type_id = Column(Integer, ForeignKey("work_types.work_type_id"))
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_price = Column(Numeric(12, 2))
    total_amount = Column(Numeric(12, 2))
    order_date = Column(Date, nullable=False)
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    order_status = Column(String(20), default='draft')
    supervisor_name = Column(String(100))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Material(Base):
    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    unit_of_measure = Column(String(20))
    current_price = Column(Numeric(12, 2))
    stock_quantity = Column(Numeric(12, 2), default=0)
    minimum_stock = Column(Numeric(12, 2), default=0)
    supplier_id = Column(Integer, ForeignKey("contractors.contractor_id"))


class MaterialRequisition(Base):
    __tablename__ = "material_requisitions"

    requisition_id = Column(Integer, primary_key=True, index=True)
    requisition_number = Column(String(50), unique=True, nullable=False)
    work_order_id = Column(Integer, ForeignKey("work_orders.work_order_id"))
    material_id = Column(Integer, ForeignKey("materials.material_id"))
    required_quantity = Column(Numeric(12, 2), nullable=False)
    issued_quantity = Column(Numeric(12, 2), default=0)
    requisition_date = Column(Date, nullable=False)
    required_date = Column(Date)
    requisition_status = Column(String(20), default='pending')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class WorkAcceptance(Base):
    __tablename__ = "work_acceptance"

    acceptance_id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.work_order_id"))
    acceptance_number = Column(String(50), unique=True, nullable=False)
    acceptance_date = Column(Date, nullable=False)
    actual_quantity = Column(Numeric(12, 2), nullable=False)
    accepted_quantity = Column(Numeric(12, 2), nullable=False)
    rejection_quantity = Column(Numeric(12, 2), default=0)
    rejection_reason = Column(Text)
    quality_score = Column(Integer)
    accepted_by = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())


class PaymentRequest(Base):
    __tablename__ = "payment_requests"

    payment_request_id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(50), unique=True, nullable=False)
    work_order_id = Column(Integer, ForeignKey("work_orders.work_order_id"))
    contractor_id = Column(Integer, ForeignKey("contractors.contractor_id"))
    amount = Column(Numeric(12, 2), nullable=False)
    request_date = Column(Date, nullable=False)
    payment_status = Column(String(20), default='pending')
    paid_amount = Column(Numeric(12, 2), default=0)
    payment_date = Column(Date)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class DailyReport(Base):
    __tablename__ = "construction_daily_reports"

    daily_report_id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, nullable=False)
    object_id = Column(Integer, ForeignKey("building_objects.object_id"))
    weather_conditions = Column(String(100))
    temperature = Column(Numeric(5, 2))
    workers_count = Column(Integer)
    equipment_count = Column(Integer)
    work_performed = Column(Text)
    issues_encountered = Column(Text)
    materials_used = Column(Text)
    created_by = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())