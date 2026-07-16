"""
src/validators.py
Funciones de validación para el proyecto ToDo.
"""

from datetime import datetime

VALID_STATES = (
    "Pendiente",
    "En curso",
    "Bloqueada",
    "Finalizada",
    "Cancelada",
)

VALID_PRIORITIES = (
    "Baja",
    "Media",
    "Alta",
    "Crítica",
)


def validate_required(value, field_name):
    if value is None or str(value).strip() == "":
        raise ValueError(f'El campo "{field_name}" es obligatorio.')
    return True


def validate_date(value, field_name="Fecha", fmt="%Y-%m-%d"):
    if value in ("", None):
        return True
    try:
        datetime.strptime(str(value), fmt)
    except ValueError as exc:
        raise ValueError(
            f'{field_name} debe tener el formato {fmt}.'
        ) from exc
    return True


def validate_state(state):
    if state not in VALID_STATES:
        raise ValueError(
            f"Estado no válido: {state}"
        )
    return True


def validate_priority(priority):
    if priority not in VALID_PRIORITIES:
        raise ValueError(
            f"Prioridad no válida: {priority}"
        )
    return True


def validate_progress(progress):
    try:
        progress = int(progress)
    except Exception as exc:
        raise ValueError("El avance debe ser un número entero.") from exc

    if not 0 <= progress <= 100:
        raise ValueError("El avance debe estar entre 0 y 100.")

    return True


def validate_responsable(nombre):
    if nombre is None:
        return True

    nombre = str(nombre).strip()

    if len(nombre) > 100:
        raise ValueError(
            "El nombre del responsable supera los 100 caracteres."
        )

    return True


def validate_task(task):
    validate_required(task.titulo, "Título")
    validate_priority(task.prioridad)
    validate_state(task.estado)
    validate_progress(task.avance)
    validate_responsable(task.responsable)
    validate_date(task.fecha_creacion, "Fecha creación")
    validate_date(task.fecha_inicio, "Fecha inicio")
    validate_date(task.fecha_prevista, "Fecha prevista")
    validate_date(task.fecha_finalizacion, "Fecha finalización")
    return True
