# app/routes/upload.py
import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from ..database import get_db
from .. import crud, schemas, models
from ..config import logger
from fastapi import Request
from ..routes.dependencies import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {
    # basic allowed extensions; can be expanded
    "png", "jpg", "jpeg", "gif", "bmp", "pdf", "doc", "docx", "xls", "xlsx", "txt"
}

def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@router.post("/", response_model=schemas.UploadOut)
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # only 'user' or admin can upload — current_user already authenticated
    logger.info(f"Upload attempt by user_id={current_user.id} filename={file.filename}")

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    # generate unique filename
    orig_ext = file.filename.rsplit(".", 1)[1]
    unique_name = f"{uuid4().hex}.{orig_ext}"
    dest_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.exception("Failed to store uploaded file")
        raise HTTPException(status_code=500, detail="Failed to store file")

    # file_url - serve via static files mount; construct accessible URL path
    file_url = f"/uploads/{unique_name}"
    upload = crud.create_upload(db, user_id=current_user.id, filename=file.filename, file_url=file_url)
    logger.info(f"File uploaded id={upload.id} user_id={upload.user_id} stored_as={unique_name}")
    return upload

@router.get("/me", response_model=list[schemas.UploadOut])
def my_uploads(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    uploads = db.query(models.Upload).filter(models.Upload.user_id == current_user.id).order_by(models.Upload.created_at.desc()).all()
    return uploads
