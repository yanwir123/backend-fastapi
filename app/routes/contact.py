from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..config import logger
from ..utils.email_utils import send_contact_email  # ⬅️ tambahkan ini

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("/", response_model=schemas.ContactOut)
def submit_contact(
    payload: schemas.ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    📩 Simpan pesan contact ke DB dan kirimkan ke email admin
    """
    try:
        # 1️⃣ Simpan ke database
        entry = crud.create_contact(db, name=payload.name, email=payload.email, message=payload.message)
        logger.info(f"Contact form submitted id={entry.id} name={entry.name}")

        # 2️⃣ Kirim email ke admin (di background)
        background_tasks.add_task(send_contact_email, payload.name, payload.email, payload.message)

        return entry
    except Exception as e:
        logger.error(f"Gagal memproses contact: {e}")
        raise HTTPException(status_code=500, detail="Gagal mengirim pesan")
