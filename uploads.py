"""Local-disk photo uploads for design-review requests.

Swap the save location for S3 / Cloud Storage in production — this keeps the
starter kit runnable with zero extra infra.
"""
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from ..models import User
from ..security import current_user

router = APIRouter(prefix="/uploads", tags=["uploads"])
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 5 * 1024 * 1024


@router.post("/photo")
async def upload_photo(file: UploadFile = File(...), user: User = Depends(current_user)):
    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Only JPEG, PNG or WEBP images are accepted")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image must be under 5MB")
    ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[file.content_type]
    name = f"{uuid.uuid4()}.{ext}"
    (UPLOAD_DIR / name).write_bytes(data)
    # In production this returns a public CDN URL; here it's a relative API path.
    return {"photo_url": f"/uploads/{name}"}
