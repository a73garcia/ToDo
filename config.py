"""
config.py
Configuración general del proyecto ToDo
"""

from pathlib import Path

# -------------------------
# Rutas
# -------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = BASE_DIR / "backups"
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
SRC_DIR = BASE_DIR / "src"

EXCEL_FILE = DATA_DIR / "tareas.xlsx"

# -------------------------
# Aplicación
# -------------------------

APP_NAME = "ToDo"
APP_VERSION = "0.1.0"

HOST = "127.0.0.1"
PORT = 8000

# -------------------------
# Estados
# -------------------------

TASK_STATES = [
    "Pendiente",
    "En curso",
    "Bloqueada",
    "Finalizada",
    "Cancelada",
]

DEFAULT_STATE = TASK_STATES[0]

# -------------------------
# Prioridades
# -------------------------

TASK_PRIORITIES = [
    "Baja",
    "Media",
    "Alta",
    "Crítica",
]

DEFAULT_PRIORITY = "Media"

# -------------------------
# Columnas del Excel
# -------------------------

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
]

# -------------------------
# Crear carpetas necesarias
# -------------------------

def ensure_directories():
    for folder in (
        DATA_DIR,
        BACKUP_DIR,
        STATIC_DIR,
        TEMPLATE_DIR,
        SRC_DIR,
    ):
        folder.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_directories()
    print(f"{APP_NAME} {APP_VERSION}")
    print("Estructura inicial preparada.")
