from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import FRONTEND_URL, logger

# ===================== INIT APP =====================
app = FastAPI(title="FastAPI Backend - Railway")

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS diizinkan untuk: {FRONTEND_URL}")

# ===================== ROUTES =====================
@app.get("/ping")
def ping():
    """Test endpoint untuk cek backend"""
    return {"message": "Backend is live!"}

# ===================== ROUTE CONTOH =====================
# nanti tambahkan routers di sini
# from .routers import auth, users
# app.include_router(auth.router, prefix="/auth")
# app.include_router(users.router, prefix="/users")
