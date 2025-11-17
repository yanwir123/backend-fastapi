# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..utils.token import create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, logger
from datetime import timedelta
from ..utils.email_utils import send_otp_email
from datetime import timedelta
from ..crud import set_otp_for_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(
    user_in: schemas.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    ✅ Registrasi user baru:
    - Cek duplikasi username/email
    - Simpan user baru
    - Generate OTP
    - Kirim email OTP di background
    """
    logger.info(f"📝 Register attempt: username={user_in.username}, email={user_in.email}")

    # 1️⃣ Cek apakah username/email sudah digunakan
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2️⃣ Buat user baru di database
    user = crud.create_user(
        db,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        role=user_in.role,
    )

    # 3️⃣ Generate OTP dan simpan ke user
    otp_code = set_otp_for_user(db, user)
    logger.debug(f"Generated OTP {otp_code} for user {user.email}")

    # 4️⃣ Kirim OTP via email di background
    background_tasks.add_task(send_otp_email, user.email, otp_code)

    logger.info(f"✅ Registration successful for {user.email}. OTP sent.")
    return {
        "success": True,
        "email": user.email,
        "message": "Registration successful. Please check your email for OTP verification."
    }

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password required")

    user = crud.authenticate_user(db, username=username, password=password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in."
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = create_access_token(subject=str(user.id), role=user.role, expires_delta=access_token_expires)
    logger.info(f"User login successful id={user.id} username={user.username}")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/verify-otp")
def verify_otp_route(payload: schemas.VerifyOtpRequest, db: Session = Depends(get_db)):
    email = payload.email
    otp = payload.otp

    user = crud.verify_otp(db, email, otp)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    logger.info(f"User verified email={email}")
    return {"message": "Email verified successfully, you can now login."}