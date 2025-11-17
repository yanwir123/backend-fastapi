from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..routes.dependencies import require_admin
import shutil, uuid, os

router = APIRouter(prefix="/gallery", tags=["gallery"])
UPLOAD_FOLDER = "uploads/gallery"


@router.post("/", response_model=schemas.GalleryOut, dependencies=[Depends(require_admin)])
def create_gallery(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = schemas.GalleryCreate(title=title)

    return crud.create_gallery(db, data, image_url=file_path)


@router.get("/", response_model=list[schemas.GalleryOut])
def get_gallery(db: Session = Depends(get_db)):
    return crud.get_all_gallery(db)


@router.delete("/{gallery_id}", dependencies=[Depends(require_admin)])
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_gallery(db, gallery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    return {"message": "Gallery deleted successfully"}
