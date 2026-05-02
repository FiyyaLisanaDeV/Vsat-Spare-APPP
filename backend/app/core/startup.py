import subprocess
from app.utils.logger import logger


def verify_pg_tools():
    """Verifikasi ketersediaan pg_dump dan psql saat startup."""
    tools = ["pg_dump", "psql"]
    for tool in tools:
        result = subprocess.run(
            [tool, "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.critical(
                f"{tool} tidak tersedia. Periksa instalasi postgresql-client."
            )
            raise RuntimeError(
                f"{tool} tidak tersedia. Periksa instalasi postgresql-client."
            )
        logger.info(f"{tool} tersedia: {result.stdout.strip()}")
