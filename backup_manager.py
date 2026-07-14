"""
Task Planner Pro
backup_manager.py
Gestión de copias de seguridad
"""

from pathlib import Path
from datetime import datetime
import shutil


class BackupManager:

    def __init__(self, excel_manager, backup_dir):
        self.excel = excel_manager
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self):
        source = Path(self.excel.file)
        if not source.exists():
            raise FileNotFoundError(f"No existe: {source}")

        name = "Backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"
        destination = self.backup_dir / name

        shutil.copy2(source, destination)

        return destination

    def list_backups(self):
        return sorted(
            self.backup_dir.glob("Backup_*.xlsx"),
            reverse=True
        )

    def restore_backup(self, backup_file):
        backup = Path(backup_file)

        if not backup.exists():
            raise FileNotFoundError(backup)

        shutil.copy2(backup, self.excel.file)

    def cleanup(self, keep_last=10):
        backups = self.list_backups()

        for old in backups[keep_last:]:
            try:
                old.unlink()
            except Exception:
                pass

    def info(self):
        backups = self.list_backups()

        return {
            "total_backups": len(backups),
            "latest": str(backups[0]) if backups else None
        }
