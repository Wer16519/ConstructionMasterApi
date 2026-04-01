# routers/__init__.py
from .contractors import router as contractors_router
from .construction_sites import router as sites_router
from .building_objects import router as objects_router
from .work_orders import router as work_orders_router
from .materials import router as materials_router
from .reports import router as reports_router
from .dashboard import router as dashboard_router
from .work_categories import router as work_categories_router
from .work_types import router as work_types_router
from .equipment import router as equipment_router
from .quality_control import router as quality_control_router
from .safety_reports import router as safety_reports_router
from .project_documents import router as project_documents_router
from .project_budget import router as project_budget_router
from .construction_stages import router as construction_stages_router
from .material_issues import router as material_issues_router

__all__ = [
    'contractors_router',
    'sites_router',
    'objects_router',
    'work_orders_router',
    'materials_router',
    'reports_router',
    'dashboard_router',
    'work_categories_router',
    'work_types_router',
    'equipment_router',
    'quality_control_router',
    'safety_reports_router',
    'project_documents_router',
    'project_budget_router',
    'construction_stages_router',
    'material_issues_router'
]