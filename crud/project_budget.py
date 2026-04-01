from sqlalchemy.orm import Session
from sqlalchemy import func
from models import ProjectBudget
from schemas import ProjectBudgetCreate
from typing import List, Optional


def get_project_budget(db: Session, budget_id: int):
    return db.query(ProjectBudget).filter(ProjectBudget.budget_id == budget_id).first()


def get_project_budgets(db: Session, skip: int = 0, limit: int = 100, object_id: Optional[int] = None):
    query = db.query(ProjectBudget)
    if object_id:
        query = query.filter(ProjectBudget.object_id == object_id)
    return query.offset(skip).limit(limit).all()


def create_project_budget(db: Session, budget: ProjectBudgetCreate):
    db_budget = ProjectBudget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def update_project_budget(db: Session, budget_id: int, budget_data: dict):
    db_budget = get_project_budget(db, budget_id)
    if db_budget:
        for key, value in budget_data.items():
            setattr(db_budget, key, value)
        db.commit()
        db.refresh(db_budget)
    return db_budget


def delete_project_budget(db: Session, budget_id: int):
    db_budget = get_project_budget(db, budget_id)
    if db_budget:
        db.delete(db_budget)
        db.commit()
        return True
    return False


def get_object_budget_summary(db: Session, object_id: int):
    result = db.query(
        func.sum(ProjectBudget.planned_amount).label('total_planned'),
        func.sum(ProjectBudget.actual_amount).label('total_actual')
    ).filter(ProjectBudget.object_id == object_id).first()

    return {
        'total_planned': result[0] or 0,
        'total_actual': result[1] or 0,
        'variance': (result[0] or 0) - (result[1] or 0)
    }