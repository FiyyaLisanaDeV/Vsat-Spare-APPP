import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from app.core.config import settings
from app.utils.logger import logger
from app.utils import errors as E

BACKUP_DIR = Path("/backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def get_db_connection_params() -> Dict[str, str]:
    """Parse DATABASE_URL untuk mendapatkan parameter koneksi PostgreSQL."""
    url = settings.DATABASE_URL
    # postgresql://user:password@host:port/dbname
    parts = url.replace("postgresql://", "").split("@")
    credentials = parts[0].split(":")
    host_db = parts[1].split("/")
    host_port = host_db[0].split(":")

    return {
        "PGUSER": credentials[0],
        "PGPASSWORD": credentials[1],
        "PGHOST": host_port[0],
        "PGPORT": host_port[1] if len(host_port) > 1 else "5432",
        "PGDATABASE": host_db[1],
    }


def list_backups() -> List[Dict[str, Any]]:
    """Daftar semua file backup yang tersedia."""
    backups = []
    for f in sorted(BACKUP_DIR.glob("*.sql"), reverse=True):
        stat = f.stat()
        size_bytes = stat.st_size
        size_str = _format_size(size_bytes)
        mtime = datetime.fromtimestamp(stat.st_mtime)
        backups.append({
            "filename": f.name,
            "size": size_str,
            "size_bytes": size_bytes,
            "created_at": mtime.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return backups


def create_backup(prefix: str = "backup") -> Dict[str, Any]:
    """Buat backup database menggunakan pg_dump."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{prefix}_{timestamp}.sql"
    filepath = BACKUP_DIR / filename

    env = os.environ.copy()
    env.update(get_db_connection_params())

    logger.info(f"Memulai backup: {filename}")
    start_time = datetime.now()

    try:
        result = subprocess.run(
            ["pg_dump", "-Fp", "-f", str(filepath)],
            env=env,
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode != 0:
            logger.error(
                f"pg_dump error | returncode={result.returncode} | "
                f"stderr={result.stderr}"
            )
            if filepath.exists():
                filepath.unlink()
            raise RuntimeError(f"pg_dump gagal: {result.stderr}")

        duration = (datetime.now() - start_time).total_seconds()
        size_str = _format_size(filepath.stat().st_size)
        logger.info(
            f"Backup selesai | file={filename} size={size_str} duration={duration:.1f}s"
        )

        # Bersihkan backup lama
        _cleanup_old_backups()

        return {
            "filename": filename,
            "size": size_str,
            "duration": f"{duration:.1f}s",
        }

    except subprocess.TimeoutExpired:
        if filepath.exists():
            filepath.unlink()
        logger.error("Backup timeout setelah 600 detik")
        raise RuntimeError("Backup timeout")

    except Exception as e:
        if filepath.exists():
            filepath.unlink()
        raise


def restore_backup(filepath: Path, user_id: int) -> bool:
    """Restore database dari file SQL."""
    env = os.environ.copy()
    env.update(get_db_connection_params())
    db_name = env.get("PGDATABASE", settings.POSTGRES_DB)

    logger.info(f"Memulai restore | file={filepath.name} user_id={user_id}")

    # Step 1: Auto backup sebelum restore
    pre_restore_filename = None
    try:
        result = create_backup(prefix="pre_restore")
        pre_restore_filename = result["filename"]
        logger.info(f"Pre-restore backup dibuat: {pre_restore_filename}")
    except Exception as e:
        logger.error(f"Pre-restore backup gagal: {str(e)}")
        raise RuntimeError(f"Gagal membuat backup sebelum restore: {str(e)}")

    # Step 2: Jalankan restore
    try:
        # Terminasi koneksi aktif
        subprocess.run(
            [
                "psql",
                "-c",
                f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{db_name}' AND pid <> pg_backend_pid();",
            ],
            env=env,
            capture_output=True,
        )

        # Drop & recreate database tidak dipraktikkan di sini karena terhubung
        # Gunakan psql dengan --single-transaction
        result = subprocess.run(
            ["psql", "-f", str(filepath)],
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,
        )

        if result.returncode != 0:
            logger.error(
                f"Restore gagal | returncode={result.returncode} | "
                f"stderr={result.stderr} | file={filepath.name}"
            )
            raise RuntimeError(result.stderr)

        logger.info(f"Restore selesai | file={filepath.name} user_id={user_id}")
        return True

    except subprocess.TimeoutExpired:
        logger.error(f"Restore timeout | file={filepath.name}")
        raise RuntimeError("Restore timeout setelah 30 menit")


def _cleanup_old_backups():
    """Hapus backup lama, pertahankan hanya N file terbaru (sesuai BACKUP_RETENTION)."""
    backups = sorted(BACKUP_DIR.glob("backup_*.sql"), reverse=True)
    retention = settings.BACKUP_RETENTION

    if len(backups) > retention:
        for old_backup in backups[retention:]:
            old_backup.unlink()
            logger.info(f"Backup lama dihapus: {old_backup.name}")


def _format_size(size_bytes: int) -> str:
    """Format ukuran file ke string yang mudah dibaca."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def check_disk_usage():
    """Periksa penggunaan disk. Log warning jika > 80%."""
    stat = shutil.disk_usage(str(BACKUP_DIR))
    percent = (stat.used / stat.total) * 100
    if percent > 80:
        logger.warning(f"Disk usage tinggi | used={percent:.1f}%")
    return percent
