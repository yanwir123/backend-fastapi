from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..config import logger
from ..routes.dependencies import require_admin

# ====================== ADMIN UPLOAD ROUTER ======================
router = APIRouter(
    prefix="/admin/uploads",
    tags=["Admin Uploads"]
)

# ====================== GET SEMUA UPLOADS (ADMIN) ======================
@router.get("/", response_model=list[schemas.UploadOut])
def get_all_uploads(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(require_admin)
):
    """
    👮 Hanya admin yang bisa melihat semua data upload.
    """
    uploads = crud.get_uploads(db)
    if not uploads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tidak ada data upload ditemukan"
        )
    logger.info(f"Admin {current_user.username} melihat seluruh uploads")
    return uploads


# ====================== PATCH STATUS UPLOAD ======================
@router.patch("/{upload_id}", response_model=schemas.UploadOut)
def change_status(
    upload_id: int,
    payload: schemas.UploadStatusUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(require_admin)
):
    """
    👮 Admin dapat mengubah status upload menjadi 'acc' atau 'rejected'.
    """
    if payload.status not in ("acc", "rejected"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status harus 'acc' atau 'rejected'"
        )

    upload = crud.update_upload_status(db, upload_id=upload_id, status=payload.status)
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload tidak ditemukan"
        )

    logger.info(
        f"Admin {current_user.username} memperbarui status upload id={upload.id} menjadi {upload.status}"
    )
    return upload


# ====================== STATISTIK UPLOAD ======================
@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(require_admin)
):
    """
    📊 Statistik jumlah upload berdasarkan status.
    """
    s = crud.get_upload_stats(db)
    logger.info(f"Admin {current_user.username} melihat statistik upload")
    return s


# ====================== APPROVED UPLOADS (PUBLIC) ======================
@router.get("/approved", response_model=list[schemas.UploadOut])
def approved_public(db: Session = Depends(get_db)):
    """
    🌍 Endpoint publik untuk melihat upload yang sudah disetujui (acc).
    """
    uploads = crud.get_approved_uploads(db)
    if not uploads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Belum ada upload yang disetujui"
        )
    return uploads
