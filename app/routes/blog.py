from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..routes.dependencies import require_admin
import shutil, uuid, os

router = APIRouter(prefix="/blog", tags=["blog"])
UPLOAD_FOLDER = "uploads/blog"


@router.post("/", response_model=schemas.BlogOut, dependencies=[Depends(require_admin)])
def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = schemas.BlogCreate(title=title, content=content)

    return crud.create_blog(db, data, image_url=file_path)


@router.get("/", response_model=list[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db)):
    return crud.get_all_blogs(db)


@router.patch("/{blog_id}", response_model=schemas.BlogOut, dependencies=[Depends(require_admin)])
def update_blog(
    blog_id: int,
    title: str = Form(None),
    content: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None

    if file:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = file_path

    data = schemas.BlogUpdate(title=title, content=content)

    updated = crud.update_blog(db, blog_id, data, image_url)

    if not updated:
        raise HTTPException(status_code=404, detail="Blog not found")

    return updated


@router.delete("/{blog_id}", dependencies=[Depends(require_admin)])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_blog(db, blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"message": "Blog deleted successfully"}
