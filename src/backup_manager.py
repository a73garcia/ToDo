from datetime import datetime
import shutil

from config import EXCEL_FILE, BACKUP_DIR


class BackupManager:
    """Gestiona las copias de seguridad del libro Excel."""

    def __init__(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def create_backup(self):
        if not EXCEL_FILE.exists():
            return None

        destination = BACKUP_DIR / f"tareas_{datetime.now():%Y%m%d_%H%M%S_%f}.xlsx"
        shutil.copy2(EXCEL_FILE, destination)
        return destination

    crear_backup = create_backup

    def list_backups(self):
        return sorted(
            BACKUP_DIR.glob("*.xlsx"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

    listar_backups = list_backups
