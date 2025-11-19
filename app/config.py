import os
import logging
from dotenv import load_dotenv

# ==================== KONFIGURASI UMUM ====================

# Tentukan ENVIRONMENT (akan mencoba membaca dari OS, default ke 'local')
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Load file .env jika ENVIRONMENT adalah 'local'
# File .env seharusnya berada di root directory proyek Anda.
if ENVIRONMENT == "local":
    load_dotenv()

# ==================== LOGGER SETUP ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")
logger.info(f"Aplikasi berjalan di environment: {ENVIRONMENT}")


# ==================== KONFIGURASI DATABASE ====================

# Baca URL database dari ENVIRONMENT (ini adalah cara terbaik)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # --- FALLBACK JIKA DATABASE_URL TIDAK DITEMUKAN ---
    
    # Ganti 'KATA_SANDI_DB_ANDA' dengan kata sandi yang BENAR di server PostgreSQL Anda
    # Ini adalah bagian yang harus Anda perbaiki agar sesuai dengan server DB Anda.
    # Contoh default yang SANGAT TIDAK AMAN jika menggunakan kata sandi 'server123'
    DEFAULT_PASSWORD = "server123" 
    
    if ENVIRONMENT == "local":
        # Fallback untuk local development
        DATABASE_URL = f"postgresql://postgres:{DEFAULT_PASSWORD}@localhost:5432/postgres"
        logger.warning("DATABASE_URL tidak ditemukan, menggunakan default LOCAL.")
    else:
        # Fallback untuk environment selain local (misalnya VPS/Production)
        DATABASE_URL = f"postgresql://postgres:{DEFAULT_PASSWORD}@127.0.0.1:5432/postgres"
        logger.warning("DATABASE_URL tidak ditemukan, menggunakan default VPS LOCAL DB.")

logger.info(f"Database HOST digunakan: {DATABASE_URL.split('@')[1]}")
# PENTING: Jangan log DATABASE_URL secara keseluruhan di production karena mengandung password!


# ==================== JWT & AUTH ====================
SECRET_KEY = os.getenv("SECRET_KEY", "THIS_IS_DEFAULT_SECRET_KEY_CHANGE_IT_IN_ENV")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# ==================== FRONTEND CORS ====================
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    # Set default berdasarkan environment
    FRONTEND_URL = "http://localhost:5173" if ENVIRONMENT == "local" else "*"

logger.info(f"FRONTEND_URL: {FRONTEND_URL}")

# CORS list (memungkinkan lebih dari satu domain)
CORS_ORIGINS = [
    FRONTEND_URL,
    "http://127.0.0.1:8000",  # FastAPI default local host
    "http://localhost:8000",
]
if ENVIRONMENT != "local":
    CORS_ORIGINS.append(os.getenv("PRODUCTION_FRONTEND_URL", "*"))


# ==================== SMTP (Email) ====================
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")