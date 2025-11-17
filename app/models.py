# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # ✅ ubah dari hashed_password ke password_hash
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String(6), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    uploads = relationship("Upload", back_populates="owner", cascade="all, delete-orphan")


class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    filename = Column(String(255))
    file_url = Column(Text)
    status = Column(String(20), default="pending")  # pending, acc, rejected
    created_at = Column(TIMESTAMP, server_default=func.now())

    owner = relationship("User", back_populates="uploads")


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150))
    message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy.sql import func

class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    image_url = Column(String)

    # Perbaikan timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
