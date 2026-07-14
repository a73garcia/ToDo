import shutil
import zipfile

from pathlib import Path
from datetime import datetime

from config import (
    BACKUP_DIR,
    EXCEL_FILE
)


class BackupManager:

    def __init__(self, excel_manager):

        self.excel = excel_manager

        self.folder = BACKUP_DIR

        self.folder.mkdir(

            parents=True,

            exist_ok=True

        )

    # =====================================================
    # FECHA
    # =====================================================

    def timestamp(self):

        return datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

    # =====================================================
    # BACKUP XLSX
    # =====================================================

    def create_backup(self):

        destino = self.folder / (

            f"Backup_{self.timestamp()}.xlsx"

        )

        shutil.copy2(

            EXCEL_FILE,

            destino

        )

        return destino

    # =====================================================
    # BACKUP ZIP
    # =====================================================

    def create_zip_backup(self):

        xlsx = self.create_backup()

        zip_name = self.folder / (

            xlsx.stem + ".zip"

        )

        with zipfile.ZipFile(

            zip_name,

            "w",

            zipfile.ZIP_DEFLATED

        ) as zipf:

            zipf.write(

                xlsx,

                arcname=xlsx.name

            )

        xlsx.unlink()

        return zip_name

    # =====================================================
    # LISTADO
    # =====================================================

    def backups(self):

        return sorted(

            self.folder.glob("*"),

            reverse=True

        )

    # =====================================================
    # ÚLTIMO BACKUP
    # =====================================================

    def latest_backup(self):

        datos = self.backups()

        if not datos:

            return None

        return datos[0]

    # =====================================================
    # RESTAURAR
    # =====================================================

    def restore(self, backup_file):

        backup = Path(backup_file)

        if not backup.exists():

            raise FileNotFoundError(

                backup

            )

        if backup.suffix.lower() == ".zip":

            with zipfile.ZipFile(

                backup

            ) as zipf:

                zipf.extractall(

                    self.folder

                )

                archivo = self.folder / (

                    zipf.namelist()[0]

                )

                shutil.copy2(

                    archivo,

                    EXCEL_FILE

                )

                archivo.unlink()

        else:

            shutil.copy2(

                backup,

                EXCEL_FILE

            )


    # =====================================================
    # ELIMINAR BACKUP
    # =====================================================

    def delete_backup(self, backup_file):

        backup = Path(backup_file)

        if backup.exists():

            backup.unlink()

            return True

        return False

    # =====================================================
    # ROTACIÓN AUTOMÁTICA
    # =====================================================

    def rotate_backups(self, keep=30):

        backups = self.backups()

        if len(backups) <= keep:

            return

        for fichero in backups[keep:]:

            try:

                fichero.unlink()

            except Exception:

                pass

    # =====================================================
    # LIMPIAR ANTIGUOS
    # =====================================================

    def cleanup_days(self, days=90):

        limite = datetime.now().timestamp() - (days * 86400)

        eliminados = 0

        for fichero in self.backups():

            if fichero.stat().st_mtime < limite:

                try:

                    fichero.unlink()

                    eliminados += 1

                except Exception:

                    pass

        return eliminados

    # =====================================================
    # TAMAÑO TOTAL
    # =====================================================

    def total_size(self):

        total = 0

        for fichero in self.backups():

            total += fichero.stat().st_size

        return total

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def backup_info(self):

        ultimo = self.latest_backup()

        return {

            "carpeta": str(self.folder),

            "numero_backups": len(self.backups()),

            "ultimo_backup": str(ultimo) if ultimo else None,

            "tamano_bytes": self.total_size()

        }

    # =====================================================
    # VERIFICAR INTEGRIDAD
    # =====================================================

    def verify_backup(self, backup_file):

        backup = Path(backup_file)

        if not backup.exists():

            return False

        try:

            if backup.suffix.lower() == ".zip":

                with zipfile.ZipFile(backup) as zf:

                    return zf.testzip() is None

            return backup.stat().st_size > 0

        except Exception:

            return False

    # =====================================================
    # VERIFICAR TODOS
    # =====================================================

    def verify_all(self):

        resultado = {}

        for fichero in self.backups():

            resultado[fichero.name] = self.verify_backup(fichero)

        return resultado

    # =====================================================
    # MANTENIMIENTO
    # =====================================================

    def maintenance(self):

        self.rotate_backups()

        self.cleanup_days()

    # =====================================================
    # EXPORTAR HISTORIAL
    # =====================================================

    def history(self):

        historial = []

        for fichero in self.backups():

            historial.append({

                "nombre": fichero.name,

                "fecha":

                    datetime.fromtimestamp(

                        fichero.stat().st_mtime

                    ),

                "tamano":

                    fichero.stat().st_size,

                "valido":

                    self.verify_backup(

                        fichero

                    )

            })

        return historial

    # =====================================================
    # ESTADO
    # =====================================================

    def status(self):

        return {

            "backups":

                len(self.backups()),

            "tamano":

                self.total_size(),

            "ultimo":

                self.latest_backup(),

            "integridad":

                self.verify_all()

        }


