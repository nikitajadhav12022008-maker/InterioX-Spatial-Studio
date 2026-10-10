from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..otp import check_otp, issue_otp
from ..schemas import OtpRequest, OtpVerify, TokenOut
from ..security import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/request", status_code=202)
def request_otp(body: OtpRequest):
    try:
        issue_otp(body.mobile)
    except ValueError as e:
        raise HTTPException(429, str(e))
    return {"detail": "Verification code sent"}


@router.post("/otp/verify", response_model=TokenOut)
def verify_otp(body: OtpVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile=body.mobile).first()
    if not check_otp(body.mobile, body.code):
        raise HTTPException(400, "Incorrect or expired code")
    if not user:
        if not body.name:
            raise HTTPException(422, "name is required for first sign-in")
        user = User(mobile=body.mobile, name=body.name)
        db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_token(user.id), name=user.name)
