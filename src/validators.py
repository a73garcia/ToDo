from typing import Any

from src.models import Task, VALID_PRIORITIES, VALID_STATES, normalize_date


def validate_identifier(value: Any) -> int:
    try:
        identifier = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("ID no válido.") from exc
    if identifier <= 0:
        raise ValueError("ID no válido.")
    return identifier


def validate_task(task: Task) -> bool:
    task.validate()
    return True


def validate_task_payload(data: dict, partial: bool = False) -> dict:
    if not isinstance(data, dict):
        raise ValueError("El cuerpo debe ser un objeto JSON.")

    allowed = {
        "titulo", "descripcion", "responsable", "prioridad", "estado",
        "fecha_creacion", "fecha_inicio", "fecha_prevista", "fecha",
        "fecha_finalizacion", "avance", "observaciones", "etiquetas",
        "comentarios", "favorito", "recordatorio", "proyecto",
        "tiempo_estimado", "tiempo_empleado",
    }
    result = {key: value for key, value in data.items() if key in allowed}

    if not partial and not str(result.get("titulo", "")).strip():
        raise ValueError("El título es obligatorio.")

    if "prioridad" in result and result["prioridad"] not in VALID_PRIORITIES:
        raise ValueError("Prioridad no válida.")

    if "estado" in result and result["estado"] not in VALID_STATES:
        raise ValueError("Estado no válido.")

    if "avance" in result:
        result["avance"] = int(result["avance"])
        if not 0 <= result["avance"] <= 100:
            raise ValueError("El avance debe estar entre 0 y 100.")

    for key in (
        "fecha_creacion", "fecha_inicio", "fecha_prevista", "fecha",
        "fecha_finalizacion", "recordatorio",
    ):
        if key in result:
            result[key] = normalize_date(result[key])

    return result


def validate_comment_payload(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Comentario no válido.")

    text = str(data.get("text", "")).strip()
    author = str(data.get("author", "Usuario")).strip() or "Usuario"

    if not text:
        raise ValueError("El comentario es obligatorio.")

    return {
        "author": author[:100],
        "text": text[:5000],
    }
