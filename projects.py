from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..schemas import ProjectIn, ProjectOut
from ..security import current_user
from ..spatial import audit_house, find_collisions

router = APIRouter(prefix="/projects", tags=["projects"])


def _own(db: Session, project_id: str, user: User) -> Project:
    p = db.get(Project, project_id)
    if not p or p.owner_id != user.id:
        raise HTTPException(404, "Project not found")
    return p


@router.get("", response_model=list[ProjectOut])
def list_projects(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Project).filter_by(owner_id=user.id).order_by(Project.updated_at.desc()).all()


@router.post("", response_model=ProjectOut, status_code=201)
def create_project(body: ProjectIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    p = Project(owner_id=user.id, name=body.name, scope=body.scope, layout=body.layout)
    db.add(p); db.commit(); db.refresh(p)
    return p


@router.put("/{project_id}", response_model=ProjectOut)
def save_project(project_id: str, body: ProjectIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    p = _own(db, project_id, user)
    p.name, p.scope, p.layout, p.updated_at = body.name, body.scope, body.layout, datetime.utcnow()
    db.commit(); db.refresh(p)
    return p


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    db.delete(_own(db, project_id, user)); db.commit()


@router.post("/{project_id}/audit")
def audit(project_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    """Authoritative server-side ergonomic audit + collision check."""
    p = _own(db, project_id, user)
    return {"collisions": find_collisions(p.layout), "audit": audit_house(p.layout)}
