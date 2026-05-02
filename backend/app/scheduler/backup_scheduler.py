from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from app.services.backup_service import create_backup, check_disk_usage
from app.utils.logger import logger

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Jakarta"))


def run_daily_backup():
    """Job backup harian — dijalankan setiap pukul 01:00 WIB."""
    logger.info("Auto backup harian dimulai...")
    try:
        check_disk_usage()
        result = create_backup(prefix="backup")
        logger.info(
            f"Auto backup selesai | file={result['filename']} "
            f"size={result['size']} duration={result['duration']}"
        )
    except Exception as e:
        logger.error(
            f"Auto backup gagal | reason={str(e)} | timestamp={__import__('datetime').datetime.now()}"
        )
        # Jangan raise — jadwal tetap berjalan besok


def start_scheduler():
    """Mulai APScheduler dengan job backup harian."""
    scheduler.add_job(
        run_daily_backup,
        trigger=CronTrigger(hour=1, minute=0, timezone=pytz.timezone("Asia/Jakarta")),
        id="daily_backup",
        name="Daily Backup",
        replace_existing=True,
        misfire_grace_time=3600,  # Toleransi 1 jam jika server restart
    )
    scheduler.start()
    logger.info("Scheduler backup harian aktif — setiap pukul 01:00 WIB")


def stop_scheduler():
    """Hentikan scheduler saat aplikasi shutdown."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler dihentikan.")
