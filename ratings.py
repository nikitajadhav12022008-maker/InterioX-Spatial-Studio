from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Rating, User
from ..schemas import RatingIn, RatingSummary
from ..security import current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("", status_code=201)
def submit_rating(body: RatingIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    r = Rating(user_id=user.id, value=body.value, comment=body.comment)
    db.add(r); db.commit()
    return {"detail": "Thanks for the feedback!"}


@router.get("/summary", response_model=RatingSummary)
def rating_summary(db: Session = Depends(get_db)):
    avg, count = db.query(func.avg(Rating.value), func.count(Rating.id)).first()
    return RatingSummary(average=round(avg or 0, 2), count=count or 0)
