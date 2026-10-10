import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    mobile: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    projects = relationship("Project", back_populates="owner")


class Project(Base):
    """A saved design. scope='house' holds every room in the building, scope='room' holds one."""
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    building_type: Mapped[str] = mapped_column(String, default="house")  # house|office|hospital|cafe
    scope: Mapped[str] = mapped_column(String, default="house")
    # {"rooms": {"living": {"width":450,"depth":380,"maxBudget":..,"items":[...]}, ...}}
    layout: Mapped[dict] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="projects")


class CatalogItem(Base):
    __tablename__ = "catalog_items"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    room: Mapped[str] = mapped_column(String, index=True)
    category: Mapped[str] = mapped_column(String, index=True)
    style: Mapped[str] = mapped_column(String, default="any")
    price: Mapped[float] = mapped_column(Float)
    width_cm: Mapped[float] = mapped_column(Float)
    depth_cm: Mapped[float] = mapped_column(Float)
    height_cm: Mapped[float] = mapped_column(Float)
    lumens: Mapped[int] = mapped_column(Integer, default=0)
    obstacle: Mapped[bool] = mapped_column(Boolean, default=True)
    glb_url: Mapped[str] = mapped_column(String, default="")


class Designer(Base):
    __tablename__ = "designers"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String, index=True)
    specialty: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float, default=0)
    reviews: Mapped[int] = mapped_column(Integer, default=0)
    latitude: Mapped[float] = mapped_column(Float, default=0)
    longitude: Mapped[float] = mapped_column(Float, default=0)


class ReviewRequest(Base):
    __tablename__ = "review_requests"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    designer_id: Mapped[str] = mapped_column(ForeignKey("designers.id"), index=True)
    project_id: Mapped[str] = mapped_column(String, default="")
    contact_name: Mapped[str] = mapped_column(String)
    contact_phone: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String, default="")
    photo_url: Mapped[str] = mapped_column(String, default="")  # uploaded via /uploads, see routers/uploads.py
    status: Mapped[str] = mapped_column(String, default="pending")  # pending|accepted|declined|completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Rating(Base):
    __tablename__ = "ratings"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    value: Mapped[int] = mapped_column(Integer)  # 1-5
    comment: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
