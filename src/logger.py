"""
src/logger.py
Sistema de registro de eventos para ToDo.
"""

from pathlib import Path
from datetime import datetime
import logging

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "todo.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

_logger = logging.getLogger("ToDo")


def info(message: str):
    _logger.info(message)


def warning(message: str):
    _logger.warning(message)


def error(message: str):
    _logger.error(message)


def exception(message: str):
    _logger.exception(message)


def task_created(task_id: int, title: str):
    info(f"Tarea creada | ID={task_id} | {title}")


def task_updated(task_id: int, field: str):
    info(f"Tarea modificada | ID={task_id} | Campo={field}")


def task_deleted(task_id: int):
    warning(f"Tarea eliminada | ID={task_id}")


def backup_created(filename: str):
    info(f"Backup generado | {filename}")


if __name__ == "__main__":
    info("Inicio del sistema de logs")
    task_created(1, "Ejemplo")
    task_updated(1, "Estado")
    backup_created("tareas_20260716_120000.xlsx")
    error("Mensaje de prueba")
