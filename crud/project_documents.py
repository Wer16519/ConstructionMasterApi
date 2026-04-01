from sqlalchemy.orm import Session
from models import ProjectDocument
from schemas import ProjectDocumentCreate
from typing import List, Optional
from datetime import date


def get_project_document(db: Session, document_id: int):
    return db.query(ProjectDocument).filter(ProjectDocument.document_id == document_id).first()


def get_project_documents(db: Session, skip: int = 0, limit: int = 100, object_id: Optional[int] = None):
    query = db.query(ProjectDocument)
    if object_id:
        query = query.filter(ProjectDocument.object_id == object_id)
    return query.order_by(ProjectDocument.document_date.desc()).offset(skip).limit(limit).all()


def create_project_document(db: Session, document: ProjectDocumentCreate):
    db_document = ProjectDocument(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_project_document(db: Session, document_id: int, document_data: dict):
    db_document = get_project_document(db, document_id)
    if db_document:
        for key, value in document_data.items():
            setattr(db_document, key, value)
        db.commit()
        db.refresh(db_document)
    return db_document


def delete_project_document(db: Session, document_id: int):
    db_document = get_project_document(db, document_id)
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False


def approve_document(db: Session, document_id: int, approved_by: str):
    from sqlalchemy import func
    db_document = get_project_document(db, document_id)
    if db_document:
        db_document.approved = True
        db_document.approved_by = approved_by
        db_document.approval_date = date.today()
        db.commit()
        db.refresh(db_document)
        return db_document
    return None