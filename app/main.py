import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import FRONTEND_URL, logger
from .database import engine, Base
from .routes import auth, uploads, admin, contact, dependencies, services, gallery, blog
from .schemas import UserOut

# ==================== SETUP DATABASE ====================
Base.metadata.create_all(bind=engine)

# ==================== FASTAPI APP ====================
app = FastAPI(title="FastAPI Backend with Auth & Uploads")

# ==================== CORS CONFIG ====================
# FRONTEND_URL harus valid dari environment Railway
allowed_origins = [
    FRONTEND_URL,                # domain Vercel lu
    "http://localhost:5173",     # dev local
    "http://127.0.0.1:5173",
]

# Jika FRONTEND_URL kosong, Railway bakal error → perbaiki
allowed_origins = [o for o in allowed_origins if o is not None and o != ""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STATIC FILES (UPLOADS) ====================
# gunakan path absolut di server Railway
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount folder untuk akses file via: /uploads/<filename>
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ==================== ROUTES ====================
app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(admin.router)
app.include_router(contact.router)
app.include_router(services.router)
app.include_router(gallery.router)
app.include_router(blog.router)

# ==================== USER INFO CHECK ====================
@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user=Depends(dependencies.get_current_user)):
    logger.info(f"/users/me accessed user_id={current_user.id}")
    return current_user

# ==================== HEALTH CHECK ====================
@app.get("/")
def root():
    return {"msg": "FastAPI Backend up and running", "frontend": FRONTEND_URL}
