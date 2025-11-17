import random, string
from datetime import datetime, timedelta
from app.models import User
from app.config import logger

def generate_otp(length: int = 6) -> str:
    """Generate kode OTP acak 6 digit."""
    return ''.join(random.choices(string.digits, k=length))

def save_otp_to_user(db, user: User, otp_code: str, expire_minutes: int = 10):
    """Simpan OTP dan waktu kedaluwarsa ke user."""
    user.otp_code = otp_code
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    db.commit()
    db.refresh(user)
    logger.debug(f"OTP saved for user={user.email}, expires_at={user.otp_expires_at}")
