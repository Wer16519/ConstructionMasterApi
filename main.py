from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    contractors_router,
    sites_router,
    objects_router,
    work_orders_router,
    materials_router,
    reports_router,
    dashboard_router,
    work_categories_router,
    work_types_router,
    equipment_router,
    quality_control_router,
    safety_reports_router,
    project_documents_router,
    project_budget_router,
    construction_stages_router,
    material_issues_router
)

app = FastAPI(
    title="Construction Accounting API",
    description="API для учета строительства",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение всех роутеров
app.include_router(contractors_router)
app.include_router(sites_router)
app.include_router(objects_router)
app.include_router(work_orders_router)
app.include_router(materials_router)
app.include_router(reports_router)
app.include_router(dashboard_router)
app.include_router(work_categories_router)
app.include_router(work_types_router)
app.include_router(equipment_router)
app.include_router(quality_control_router)
app.include_router(safety_reports_router)
app.include_router(project_documents_router)
app.include_router(project_budget_router)
app.include_router(construction_stages_router)
app.include_router(material_issues_router)


@app.get("/")
def root():
    return {
        "message": "Construction Accounting API",
        "version": "1.0.0",
        "endpoints": {
            "contractors": "/contractors",
            "sites": "/sites",
            "objects": "/objects",
            "work_orders": "/work-orders",
            "materials": "/materials",
            "reports": "/reports",
            "dashboard": "/dashboard",
            "work_categories": "/work-categories",
            "work_types": "/work-types",
            "equipment": "/equipment",
            "quality_control": "/quality-control",
            "safety_reports": "/safety-reports",
            "documents": "/documents",
            "budget": "/budget",
            "construction_stages": "/construction-stages",
            "material_issues": "/material-issues"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")