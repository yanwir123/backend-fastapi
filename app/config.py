import os
import logging
from dotenv import load_dotenv

# ==================== LOAD .ENV ====================
# Hanya untuk local testing, Railway tidak memerlukan ini
if os.getenv("ENVIRONMENT", "local") == "local":
    load_dotenv()

# ==================== ENV ====================
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")  # local / production

# DATABASE
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if ENVIRONMENT == "local":
        # fallback untuk local development
        DATABASE_URL = "postgresql://postgres:server123@localhost:5432/postgres"
        logger = logging.getLogger("app")
        logger.warning("DATABASE_URL tidak ditemukan di env, menggunakan default local.")
    else:
        raise ValueError("DATABASE_URL tidak ditemukan!")

# JWT & Auth
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY tidak boleh kosong!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# FRONTEND URL untuk CORS
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    FRONTEND_URL = "http://localhost:5173" if ENVIRONMENT == "local" else ""

# ==================== SMTP ====================
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# ==================== LOGGER ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")

logger.info(f"ENVIRONMENT: {ENVIRONMENT}")
logger.info(f"DATABASE_URL: {DATABASE_URL}")
logger.info(f"FRONTEND_URL: {FRONTEND_URL}")
