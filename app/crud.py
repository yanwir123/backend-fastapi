# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from .utils.security import hash_password, verify_password
from datetime import datetime
from typing import Optional
from datetime import datetime, timedelta
import random, string
from . import models

# ---------------- USERS ----------------
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str, role: str = "user") -> models.User:
    user = models.User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

# ---------------- UPLOADS ----------------
def create_upload(db: Session, user_id: int, filename: str, file_url: str) -> models.Upload:
    upload = models.Upload(user_id=user_id, filename=filename, file_url=file_url, status="pending")
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

def get_uploads(db: Session, skip: int =0, limit: int =100):
    return db.query(models.Upload).order_by(models.Upload.created_at.desc()).offset(skip).limit(limit).all()

def get_upload_by_id(db: Session, upload_id: int):
    return db.query(models.Upload).filter(models.Upload.id == upload_id).first()

def update_upload_status(db: Session, upload_id: int, status: str):
    upload = get_upload_by_id(db, upload_id)
    if not upload:
        return None
    upload.status = status
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

def get_approved_uploads(db: Session, skip: int =0, limit: int =100):
    return db.query(models.Upload).filter(models.Upload.status == "acc").order_by(models.Upload.created_at.desc()).offset(skip).limit(limit).all()

def get_upload_stats(db: Session):
    total = db.query(models.Upload).count()
    pending = db.query(models.Upload).filter(models.Upload.status == "pending").count()
    approved = db.query(models.Upload).filter(models.Upload.status == "acc").count()
    rejected = db.query(models.Upload).filter(models.Upload.status == "rejected").count()
    return {"total": total, "pending": pending, "approved": approved, "rejected": rejected}

# ---------------- CONTACT ----------------
def create_contact(db: Session, name: str, email: str, message: str):
    entry = models.Contact(name=name, email=email, message=message)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def set_otp_for_user(db, user: models.User):
    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    db.refresh(user)
    return otp

def verify_otp(db, email: str, otp: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if user.otp_code == otp and user.otp_expiry > datetime.utcnow():
        user.is_verified = True
        user.otp_code = None
        user.otp_expiry = None
        db.commit()
        db.refresh(user)
        return user
    return None


# ---------------- SERVICES ----------------
def create_service(db: Session, data: schemas.ServiceCreate, image_url: str):
    service = models.Service(
        title=data.title,
        description=data.description,
        image_url=image_url
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_all_services(db: Session):
    return db.query(models.Service).order_by(models.Service.created_at.desc()).all()


def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def update_service(db: Session, service_id: int, data: schemas.ServiceUpdate, image_url: str = None):
    service = get_service_by_id(db, service_id)
    if not service:
        return None

    if data.title is not None:
        service.title = data.title
    if data.description is not None:
        service.description = data.description
    if image_url is not None:
        service.image_url = image_url

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int):
    service = get_service_by_id(db, service_id)
    if not service:
        return None

    db.delete(service)
    db.commit()
    return True

# ---------------- GALLERY ----------------
def create_gallery(db: Session, data: schemas.GalleryCreate, image_url: str):
    gallery = models.Gallery(
        title=data.title,
        image_url=image_url
    )
    db.add(gallery)
    db.commit()
    db.refresh(gallery)
    return gallery


def get_all_gallery(db: Session):
    return db.query(models.Gallery).order_by(models.Gallery.created_at.desc()).all()


def get_gallery_by_id(db: Session, gallery_id: int):
    return db.query(models.Gallery).filter(models.Gallery.id == gallery_id).first()


def delete_gallery(db: Session, gallery_id: int):
    gallery = get_gallery_by_id(db, gallery_id)
    if not gallery:
        return None

    db.delete(gallery)
    db.commit()
    return True

# ---------------- BLOG ----------------
def create_blog(db: Session, data: schemas.BlogCreate, image_url: str):
    blog = models.Blog(
        title=data.title,
        content=data.content,
        image_url=image_url
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def get_all_blogs(db: Session):
    return db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()


def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def update_blog(db: Session, blog_id: int, data: schemas.BlogUpdate, image_url: str = None):
    blog = get_blog_by_id(db, blog_id)
    if not blog:
        return None

    if data.title is not None:
        blog.title = data.title
    if data.content is not None:
        blog.content = data.content
    if image_url is not None:
        blog.image_url = image_url

    db.commit()
    db.refresh(blog)
    return blog


def delete_blog(db: Session, blog_id: int):
    blog = get_blog_by_id(db, blog_id)
    if not blog:
        return None

    db.delete(blog)
    db.commit()
    return True
