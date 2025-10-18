from sqlalchemy.orm import Session
from . import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate, role: str = "developer"):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    db_proj = models.Project(title=project.title, description=project.description, owner_id=owner_id)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj

def list_projects(db: Session, skip=0, limit=100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_issue(db: Session, project_id: int, issue: schemas.IssueCreate, reporter_id: int):
    db_issue = models.Issue(title=issue.title, description=issue.description, priority=issue.priority, project_id=project_id, reporter_id=reporter_id, assignee_id=issue.assignee_id)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

def list_issues_for_project(db: Session, project_id: int):
    return db.query(models.Issue).filter(models.Issue.project_id == project_id).all()
