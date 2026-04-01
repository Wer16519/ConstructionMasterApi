from sqlalchemy.orm import Session
from models import MaterialIssue
from schemas import MaterialIssueCreate
from typing import List, Optional
from datetime import date
import random


def get_material_issue(db: Session, issue_id: int):
    return db.query(MaterialIssue).filter(MaterialIssue.issue_id == issue_id).first()


def get_material_issues(db: Session, skip: int = 0, limit: int = 100, requisition_id: Optional[int] = None):
    query = db.query(MaterialIssue)
    if requisition_id:
        query = query.filter(MaterialIssue.requisition_id == requisition_id)
    return query.order_by(MaterialIssue.issue_date.desc()).offset(skip).limit(limit).all()


def create_material_issue(db: Session, issue: MaterialIssueCreate):
    issue_number = f"ISS-{date.today().strftime('%Y%m%d')}-{random.randint(1, 9999):04d}"
    db_issue = MaterialIssue(
        **issue.model_dump(),
        issue_number=issue_number
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def process_material_return(db: Session, issue_id: int, return_quantity, return_reason):
    from sqlalchemy import text

    db.execute(
        text("CALL process_material_return(:p1, :p2, :p3)"),
        {"p1": issue_id, "p2": return_quantity, "p3": return_reason}
    )
    db.commit()
    return get_material_issue(db, issue_id)