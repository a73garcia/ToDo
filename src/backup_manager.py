"""
src/backup_manager.py
Gestión de copias de seguridad del archivo Excel.
"""

from pathlib import Path
from datetime import datetime
import shutil

from config import EXCEL_FILE, BACKUP_DIR


class BackupManager:

    def __init__(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def crear_backup(self):
        """Crea una copia del archivo Excel."""

        if not EXCEL_FILE.exists():
            return None

        nombre = datetime.now().strftime(
            "tareas_%Y%m%d_%H%M%S.xlsx"
        )

        destino = BACKUP_DIR / nombre

        shutil.copy2(EXCEL_FILE, destino)

        return destino

    def listar_backups(self):
        archivos = sorted(
            BACKUP_DIR.glob("*.xlsx"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        return archivos

    def eliminar_backup(self, archivo):
        archivo = Path(archivo)

        if archivo.exists():
            archivo.unlink()
            return True

        return False

    def limpiar_antiguos(self, conservar=20):
        backups = self.listar_backups()

        if len(backups) <= conservar:
            return 0

        eliminados = 0

        for fichero in backups[conservar:]:
            fichero.unlink()
            eliminados += 1

        return eliminados


if __name__ == "__main__":

    gestor = BackupManager()

    copia = gestor.crear_backup()

    if copia:
        print(f"Backup creado: {copia}")
    else:
        print("No existe todavía el archivo Excel.")
