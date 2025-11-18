import os
import logging
from dotenv import load_dotenv

# ==================== LOAD .ENV ====================
# Hanya load .env saat di local
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
if ENVIRONMENT == "local":
    load_dotenv()

# ==================== LOGGER SETUP ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")


# ==================== DATABASE ====================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if ENVIRONMENT == "local":
        # fallback untuk local development
        DATABASE_URL = "postgresql://postgres:server123@localhost:5432/postgres"
        logger.warning("DATABASE_URL tidak ditemukan, menggunakan default LOCAL.")
    else:
        # fallback untuk VPS (PostgreSQL default)
        DATABASE_URL = "postgresql://postgres:server123@localhost:5432/postgres"
        logger.warning("DATABASE_URL tidak ditemukan, menggunakan default VPS LOCAL DB.")

logger.info(f"DATABASE_URL digunakan: {DATABASE_URL}")


# ==================== JWT & AUTH ====================
SECRET_KEY = os.getenv("SECRET_KEY", "THIS_IS_DEFAULT_SECRET_KEY_CHANGE_IT_IN_ENV")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# ==================== FRONTEND CORS ====================
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    FRONTEND_URL = "http://localhost:5173" if ENVIRONMENT == "local" else "*"

logger.info(f"FRONTEND_URL: {FRONTEND_URL}")


# ==================== SMTP ====================
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

