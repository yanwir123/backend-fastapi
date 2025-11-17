# app/schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# ======================================
#               AUTH / USER
# ======================================
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    role: Optional[str] = None


# ======================================
#               UPLOAD
# ======================================
class UploadCreate(BaseModel):
    # metadata only (file uploaded via multipart)
    pass


class UploadOut(BaseModel):
    id: int
    user_id: int
    filename: Optional[str]
    file_url: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class UploadStatusUpdate(BaseModel):
    status: str   # "acc" or "rejected"


# ======================================
#               CONTACT
# ======================================
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str


class ContactOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    message: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# ======================================
#               VERIFY OTP
# ======================================
class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


# ============================================================
# ======================= SERVICES ============================
# ============================================================

class ServiceBase(BaseModel):
    title: str
    description: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ServiceOut(ServiceBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


# ============================================================
# ======================== GALLERY ============================
# ============================================================

class GalleryCreate(BaseModel):
    title: str

class GalleryOut(BaseModel):
    id: int
    title: str
    image_url: str

    class Config:
        orm_mode = True


# ============================================================
# ========================== BLOG =============================
# ============================================================

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogOut(BlogBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True