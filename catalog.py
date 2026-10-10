from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CatalogItem

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("")
def list_items(room: Optional[str] = None, category: Optional[str] = None, style: Optional[str] = None,
               db: Session = Depends(get_db)):
    q = db.query(CatalogItem)
    if room: q = q.filter_by(room=room)
    if category: q = q.filter_by(category=category)
    if style: q = q.filter(CatalogItem.style.in_([style, "any"]))
    return q.all()
