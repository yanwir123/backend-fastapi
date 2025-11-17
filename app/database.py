from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL, logger

# ===================== DATABASE CONNECTION =====================
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database engine dibuat sukses")
except Exception as e:
    logger.error(f"Gagal membuat engine database: {e}")
    raise e

# Dependency FastAPI
def get_db():
    """Dependency untuk mendapatkan session database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
