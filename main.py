from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
from .tasks import celery_app

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Issue Tracker API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    created = crud.create_user(db, user)
    return created

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token({"sub": user.username}, expires_delta=timedelta(hours=4))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/projects", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, current_user = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    created = crud.create_project(db, project, owner_id=current_user.id)
    return created

@app.get("/projects", response_model=list[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    return crud.list_projects(db)

@app.post("/projects/{project_id}/issues", response_model=schemas.IssueOut)
def create_issue(project_id: int, issue: schemas.IssueCreate, current_user = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    created = crud.create_issue(db, project_id, issue, reporter_id=current_user.id)
    # enqueue background notification
    celery_app.send_task("send_issue_notification", args=[created.id, created.title])
    return created

@app.get("/projects/{project_id}/issues", response_model=list[schemas.IssueOut])
def list_issues(project_id: int, db: Session = Depends(get_db)):
    return crud.list_issues_for_project(db)
