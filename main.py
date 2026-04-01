from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    contractors_router,
    sites_router,
    objects_router,
    work_orders_router,
    materials_router,
    reports_router,
    dashboard_router
)
app = FastAPI(
    title="Construction Accounting API",
    description="API для учета строительства",
    version="1.0.0"
)

# CORS middleware для Android приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(contractors_router)
app.include_router(sites_router)
app.include_router(objects_router)
app.include_router(work_orders_router)
app.include_router(materials_router)
app.include_router(reports_router)
app.include_router(dashboard_router)
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
            "dashboard": "/dashboard"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)