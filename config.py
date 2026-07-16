"""
config.py
Configuración general de ToDo - Versión 2.0.
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
LOG_DIR = DATA_DIR / "logs"

STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
SRC_DIR = BASE_DIR / "src"

EXCEL_FILE = DATA_DIR / "tareas.xlsx"

APP_NAME = "ToDo"
APP_VERSION = "2.0.0"

HOST = "127.0.0.1"
PORT = 8000

TASK_STATES = [
    "Pendiente",
    "En curso",
    "Bloqueada",
    "Finalizada",
    "Cancelada",
]

DEFAULT_STATE = "Pendiente"

TASK_PRIORITIES = [
    "Baja",
    "Media",
    "Alta",
    "Crítica",
]

DEFAULT_PRIORITY = "Media"

EXCEL_COLUMNS = [
    "ID",
    "Título",
    "Descripción",
    "Responsable",
    "Prioridad",
    "Estado",
    "Fecha creación",
    "Fecha inicio",
    "Fecha prevista",
    "Fecha finalización",
    "Última actualización",
    "Avance (%)",
    "Observaciones",
    "Etiquetas",
    "Comentarios",
    "Favorito",
    "Recordatorio",
    "Proyecto",
    "Tiempo estimado",
    "Tiempo empleado",
    "Versión",
]


def ensure_directories():
    for folder in (
        DATA_DIR,
        BACKUP_DIR,
        LOG_DIR,
        STATIC_DIR,
        STATIC_DIR / "css",
        STATIC_DIR / "js",
        STATIC_DIR / "assets",
        TEMPLATE_DIR,
        SRC_DIR,
    ):
        folder.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_directories()
    print(f"{APP_NAME} {APP_VERSION}")
    print("Estructura preparada.")
