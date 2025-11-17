# app/config.py
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app")

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")  # Gmail kamu
SMTP_PASS = os.getenv("SMTP_PASS")  # App password Gmail kamu

# Contoh tambahan yang sudah ada
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "secretjwtkey"
ALGORITHM = "HS256"