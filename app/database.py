from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL, logger

# ===================== DATABASE CONNECTION =====================
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency untuk mendapatkan sesi database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
