from sqlalchemy.orm import Session
from sqlalchemy import func
from models import ConstructionSite, BuildingObject
from schemas import ConstructionSiteCreate
from typing import List, Optional

def get_site(db: Session, site_id: int):
    return db.query(ConstructionSite).filter(ConstructionSite.site_id == site_id).first()

def get_sites(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(ConstructionSite)
    if status:
        query = query.filter(ConstructionSite.site_status == status)
    return query.offset(skip).limit(limit).all()

def create_site(db: Session, site: ConstructionSiteCreate):
    db_site = ConstructionSite(**site.model_dump())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def update_site(db: Session, site_id: int, site_data: dict):
    db_site = get_site(db, site_id)
    if db_site:
        for key, value in site_data.items():
            setattr(db_site, key, value)
        db.commit()
        db.refresh(db_site)
    return db_site

def delete_site(db: Session, site_id: int):
    db_site = get_site(db, site_id)
    if db_site:
        db.delete(db_site)
        db.commit()
        return True
    return False

def get_site_with_objects(db: Session, site_id: int):
    site = get_site(db, site_id)
    if site:
        objects = db.query(BuildingObject).filter(BuildingObject.site_id == site_id).all()
        return {"site": site, "objects": objects}
    return None

def get_site_count(db: Session):
    return db.query(func.count(ConstructionSite.site_id)).scalar()