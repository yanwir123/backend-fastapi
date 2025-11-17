from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..routes.dependencies import require_admin
import shutil
import uuid
import os

router = APIRouter(prefix="/services", tags=["services"])

UPLOAD_FOLDER = "uploads/services"


@router.post("/", response_model=schemas.ServiceOut, dependencies=[Depends(require_admin)])
def create_service(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = schemas.ServiceCreate(title=title, description=description)

    return crud.create_service(db, data, image_url=file_path)


@router.get("/", response_model=list[schemas.ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return crud.get_all_services(db)


@router.patch("/{service_id}", response_model=schemas.ServiceOut, dependencies=[Depends(require_admin)])
def update_service(
    service_id: int,
    title: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None

    if file:
        # FIX: pastikan folder upload ada
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = file_path

    data = schemas.ServiceUpdate(title=title, description=description)

    updated = crud.update_service(db, service_id, data, image_url)

    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")

    return updated


@router.delete("/{service_id}", dependencies=[Depends(require_admin)])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_service(db, service_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")

    return {"message": "Service deleted successfully"}
