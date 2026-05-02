import threading
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.services import backup_service
from app.core.dependencies import require_admin
from app.core.config import settings
from app.utils.logger import logger
from app.utils import errors as E

router = APIRouter(prefix="/api/backup", tags=["Backup & Restore"])

# Flag untuk menandai status restore berjalan
_restore_in_progress = False
_restore_lock = threading.Lock()

BACKUP_DIR = Path("/backups")


def check_restore_lock():
    """Middleware-like check untuk blokir request saat restore berjalan."""
    if _restore_in_progress:
        raise HTTPException(
            status_code=503,
            detail=E.MAINTENANCE_MODE,
        )


@router.get("/list")
def list_backups(
    admin: User = Depends(require_admin),
):
    """Daftar semua file backup yang tersedia."""
    check_restore_lock()
    backups = backup_service.list_backups()
    return {"success": True, "message": "Berhasil", "data": backups}


@router.post("/create")
def create_backup(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Backup manual database sekarang."""
    check_restore_lock()
    try:
        result = backup_service.create_backup(prefix="backup")
        logger.info(f"Backup manual selesai | user_id={admin.id} file={result['filename']}")
        return {"success": True, "message": "Backup berhasil dibuat", "data": result}
    except Exception as e:
        logger.error(f"Backup manual gagal | user_id={admin.id} reason={str(e)}")
        raise HTTPException(status_code=500, detail=E.BACKUP_FAILED)


@router.get("/download/{filename}")
def download_backup(
    filename: str,
    admin: User = Depends(require_admin),
):
    """Download file backup."""
    # Sanitasi nama file
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Nama file tidak valid.")

    filepath = BACKUP_DIR / filename
    if not filepath.exists() or not filepath.is_file():
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/octet-stream",
    )


@router.post("/restore/upload")
async def restore_from_upload(
    file: UploadFile = File(...),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Restore database dari file SQL yang diupload."""
    global _restore_in_progress

    # Validasi ekstensi
    if not file.filename or not file.filename.endswith(".sql"):
        raise HTTPException(status_code=400, detail=E.RESTORE_INVALID_FORMAT)

    # Validasi ukuran (baca sebagian dulu)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=E.RESTORE_FILE_TOO_LARGE)

    # Simpan file sementara
    temp_path = BACKUP_DIR / f"upload_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(content)

    return await _do_restore(temp_path, admin.id, db)


@router.post("/restore/{filename}")
async def restore_from_existing(
    filename: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Restore database dari file backup yang sudah ada."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Nama file tidak valid.")

    if not filename.endswith(".sql"):
        raise HTTPException(status_code=400, detail=E.RESTORE_INVALID_FORMAT)

    filepath = BACKUP_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    return await _do_restore(filepath, admin.id, db)


async def _do_restore(filepath: Path, user_id: int, db: Session):
    """Eksekusi restore database."""
    global _restore_in_progress

    with _restore_lock:
        if _restore_in_progress:
            raise HTTPException(status_code=503, detail=E.MAINTENANCE_MODE)
        _restore_in_progress = True

    try:
        # Revoke semua session aktif
        from app.services.auth_service import revoke_all_user_tokens
        from app.models.user import User as UserModel
        users = db.query(UserModel).all()
        for user in users:
            revoke_all_user_tokens(db, user.id)

        backup_service.restore_backup(filepath, user_id)

        logger.info(f"Restore selesai | file={filepath.name} user_id={user_id}")
        return {
            "success": True,
            "message": "Restore berhasil. Semua session telah direset. Silakan login kembali.",
            "data": None,
        }
    except Exception as e:
        logger.error(f"Restore gagal | file={filepath.name} reason={str(e)}")
        raise HTTPException(status_code=500, detail=E.RESTORE_FAILED)
    finally:
        _restore_in_progress = False
        # Hapus file upload sementara jika ada
        if filepath.name.startswith("upload_"):
            try:
                filepath.unlink()
            except Exception:
                pass
