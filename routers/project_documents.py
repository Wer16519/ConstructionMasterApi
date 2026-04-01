from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import ProjectDocumentCreate, ProjectDocumentResponse, ApiResponse
import crud

router = APIRouter(prefix="/documents", tags=["project_documents"])


@router.get("/", response_model=List[ProjectDocumentResponse])
def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    object_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_project_documents(db, skip=skip, limit=limit, object_id=object_id)


@router.get("/{document_id}", response_model=ProjectDocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = crud.get_project_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/", response_model=ProjectDocumentResponse, status_code=201)
def create_document(document: ProjectDocumentCreate, db: Session = Depends(get_db)):
    return crud.create_project_document(db, document)


@router.put("/{document_id}", response_model=ProjectDocumentResponse)
def update_document(document_id: int, document_data: dict, db: Session = Depends(get_db)):
    doc = crud.update_project_document(db, document_id, document_data)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/{document_id}/approve", response_model=ApiResponse)
def approve_document(document_id: int, approved_by: str, db: Session = Depends(get_db)):
    doc = crud.approve_document(db, document_id, approved_by)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(success=True, message="Document approved successfully")


@router.delete("/{document_id}", response_model=ApiResponse)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    success = crud.delete_project_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(success=True, message="Document deleted successfully")