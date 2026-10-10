from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class OtpRequest(BaseModel):
    mobile: str = Field(pattern=r"^\+\d{8,15}$", description="E.164 format, e.g. +919876543210")


class OtpVerify(BaseModel):
    mobile: str = Field(pattern=r"^\+\d{8,15}$")
    code: str = Field(min_length=6, max_length=6)
    name: Optional[str] = None  # required only on first sign-in


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str


class ProjectIn(BaseModel):
    name: str
    building_type: str = "house"
    scope: str = "house"
    layout: dict[str, Any]


class ProjectOut(ProjectIn):
    id: str
    updated_at: datetime

    class Config:
        from_attributes = True


class DesignerOut(BaseModel):
    id: str
    name: str
    city: str
    specialty: str
    rating: float
    reviews: int
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True


class ReviewRequestIn(BaseModel):
    project_id: str = ""
    contact_name: str
    contact_phone: str
    message: str = ""
    photo_url: str = ""  # returned by POST /uploads/photo


class ReviewRequestOut(BaseModel):
    id: str
    designer_id: str
    status: str
    photo_url: str = ""
    created_at: datetime

    class Config:
        from_attributes = True


class RatingIn(BaseModel):
    value: int = Field(ge=1, le=5)
    comment: str = ""


class RatingSummary(BaseModel):
    average: float
    count: int
