import math
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Designer, ReviewRequest, User
from ..schemas import DesignerOut, ReviewRequestIn, ReviewRequestOut
from ..security import current_user

router = APIRouter(prefix="/designers", tags=["designers"])


def _km(lat1, lon1, lat2, lon2) -> float:
    r = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


@router.get("", response_model=list[DesignerOut])
def nearby(city: Optional[str] = None, lat: Optional[float] = Query(None), lon: Optional[float] = Query(None),
           db: Session = Depends(get_db)):
    q = db.query(Designer)
    if city:
        q = q.filter(Designer.city.ilike(city))
    out = []
    for d in q.all():
        item = DesignerOut.model_validate(d)
        if lat is not None and lon is not None:
            item.distance_km = round(_km(lat, lon, d.latitude, d.longitude), 1)
        out.append(item)
    out.sort(key=lambda x: (x.distance_km if x.distance_km is not None else 1e9, -x.rating))
    return out


@router.post("/{designer_id}/review-requests", response_model=ReviewRequestOut, status_code=201)
def request_review(designer_id: str, body: ReviewRequestIn, user: User = Depends(current_user),
                   db: Session = Depends(get_db)):
    rr = ReviewRequest(user_id=user.id, designer_id=designer_id, project_id=body.project_id,
                       contact_name=body.contact_name, contact_phone=body.contact_phone,
                       message=body.message, photo_url=body.photo_url)
    db.add(rr); db.commit(); db.refresh(rr)
    # TODO: notify designer (email/WhatsApp/SMS) via a background task
    return rr


@router.get("/review-requests/mine", response_model=list[ReviewRequestOut])
def my_requests(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(ReviewRequest).filter_by(user_id=user.id).all()
