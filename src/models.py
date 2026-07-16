"""
src/models.py
Modelos de datos de ToDo - Versión 2.0 corregida.

Esta versión sustituye al archivo models.py anterior.
Corrige la serialización y reconstrucción de comentarios
para conservar autor, fecha y texto.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Optional


DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COMMENT_SEPARATOR = "\n---COMMENT---\n"

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


def today_string() -> str:
    return date.today().strftime(DATE_FORMAT)


def now_string() -> str:
    return datetime.now().strftime(DATETIME_FORMAT)


def normalize_date(value: Any) -> str:
    if value in (None, ""):
        return ""

    if isinstance(value, datetime):
        return value.strftime(DATE_FORMAT)

    if isinstance(value, date):
        return value.strftime(DATE_FORMAT)

    text = str(value).strip()

    for fmt in (
        DATE_FORMAT,
        "%d/%m/%Y",
        DATETIME_FORMAT,
        "%d/%m/%Y %H:%M:%S",
    ):
        try:
            return datetime.strptime(text, fmt).strftime(DATE_FORMAT)
        except ValueError:
            continue

    raise ValueError(
        f"Fecha no válida: {value}. Use el formato YYYY-MM-DD."
    )


def normalize_datetime(value: Any) -> str:
    if value in (None, ""):
        return now_string()

    if isinstance(value, datetime):
        return value.strftime(DATETIME_FORMAT)

    if isinstance(value, date):
        return datetime.combine(
            value,
            datetime.min.time()
        ).strftime(DATETIME_FORMAT)

    text = str(value).strip()

    for fmt in (
        DATETIME_FORMAT,
        DATE_FORMAT,
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ):
        try:
            return datetime.strptime(text, fmt).strftime(
                DATETIME_FORMAT
            )
        except ValueError:
            continue

    raise ValueError(
        f"Fecha y hora no válidas: {value}."
    )


def normalize_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []

    if isinstance(value, (list, tuple, set)):
        items = value
    else:
        items = str(value).split(",")

    result = []

    for item in items:
        text = str(item).strip()

        if text and text not in result:
            result.append(text)

    return result


@dataclass
class Comment:
    author: str = "Usuario"
    text: str = ""
    created_at: str = field(default_factory=now_string)

    def __post_init__(self):
        self.author = str(
            self.author or "Usuario"
        ).strip() or "Usuario"

        self.text = str(
            self.text or ""
        ).strip()

        self.created_at = normalize_datetime(
            self.created_at
        )

        if not self.text:
            raise ValueError(
                "El texto del comentario es obligatorio."
            )

    def to_dict(self) -> dict:
        return {
            "author": self.author,
            "text": self.text,
            "created_at": self.created_at,
        }

    def to_storage_text(self) -> str:
        """
        Convierte el comentario al formato persistido en Excel.

        Formato:
        fecha
        autor

        texto
        """

        return (
            f"{self.created_at}\n"
            f"{self.author}\n\n"
            f"{self.text}"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Comment":
        return cls(
            author=data.get("author", "Usuario"),
            text=data.get("text", ""),
            created_at=data.get(
                "created_at",
                now_string()
            ),
        )

    @classmethod
    def from_storage_text(cls, raw: Any) -> "Comment":
        """
        Reconstruye un comentario almacenado en Excel.

        Conserva fecha, autor y texto. También admite bloques antiguos
        sin una estructura completa.
        """

        text = str(raw or "").strip()

        if not text:
            raise ValueError(
                "El bloque de comentario está vacío."
            )

        lines = text.splitlines()

        created_at = now_string()
        author = "Histórico"
        body_start = 0

        if lines:
            first = lines[0].strip()

            try:
                created_at = normalize_datetime(first)
                body_start = 1
            except ValueError:
                created_at = now_string()

        if len(lines) > body_start:
            possible_author = lines[body_start].strip()

            if possible_author:
                author = possible_author
                body_start += 1

        while (
            body_start < len(lines)
            and not lines[body_start].strip()
        ):
            body_start += 1

        body = "\n".join(
            lines[body_start:]
        ).strip()

        if not body:
            body = text

        return cls(
            author=author,
            text=body,
            created_at=created_at,
        )


@dataclass
class Task:
    id: Optional[int] = None
    titulo: str = ""
    descripcion: str = ""
    responsable: str = ""
    prioridad: str = "Media"
    estado: str = "Pendiente"

    fecha_creacion: str = field(
        default_factory=today_string
    )
    fecha_inicio: str = ""
    fecha_prevista: str = ""
    fecha_finalizacion: str = ""
    ultima_actualizacion: str = field(
        default_factory=now_string
    )

    avance: int = 0
    observaciones: str = ""

    etiquetas: list[str] = field(
        default_factory=list
    )
    comentarios: list[Comment] = field(
        default_factory=list
    )
    favorito: bool = False
    recordatorio: str = ""
    proyecto: str = ""
    tiempo_estimado: float = 0.0
    tiempo_empleado: float = 0.0

    def __post_init__(self):
        self.id = self._normalize_id(self.id)

        self.titulo = str(
            self.titulo or ""
        ).strip()

        self.descripcion = str(
            self.descripcion or ""
        ).strip()

        self.responsable = str(
            self.responsable or ""
        ).strip()

        self.prioridad = str(
            self.prioridad or "Media"
        ).strip()

        self.estado = str(
            self.estado or "Pendiente"
        ).strip()

        self.fecha_creacion = normalize_date(
            self.fecha_creacion or today_string()
        )

        self.fecha_inicio = normalize_date(
            self.fecha_inicio
        )

        self.fecha_prevista = normalize_date(
            self.fecha_prevista
        )

        self.fecha_finalizacion = normalize_date(
            self.fecha_finalizacion
        )

        self.ultima_actualizacion = normalize_datetime(
            self.ultima_actualizacion
        )

        self.avance = self._normalize_progress(
            self.avance
        )

        self.observaciones = str(
            self.observaciones or ""
        ).strip()

        self.etiquetas = normalize_list(
            self.etiquetas
        )

        self.comentarios = self._normalize_comments(
            self.comentarios
        )

        self.favorito = self._normalize_boolean(
            self.favorito
        )

        self.recordatorio = normalize_date(
            self.recordatorio
        )

        self.proyecto = str(
            self.proyecto or ""
        ).strip()

        self.tiempo_estimado = self._normalize_hours(
            self.tiempo_estimado
        )

        self.tiempo_empleado = self._normalize_hours(
            self.tiempo_empleado
        )

        self.apply_business_rules()

    @staticmethod
    def _normalize_id(value: Any) -> Optional[int]:
        if value in (None, ""):
            return None

        return int(value)

    @staticmethod
    def _normalize_progress(value: Any) -> int:
        try:
            progress = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "El avance debe ser un número entero."
            ) from exc

        if not 0 <= progress <= 100:
            raise ValueError(
                "El avance debe estar entre 0 y 100."
            )

        return progress

    @staticmethod
    def _normalize_hours(value: Any) -> float:
        if value in (None, ""):
            return 0.0

        try:
            hours = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Las horas deben ser un número."
            ) from exc

        if hours < 0:
            raise ValueError(
                "Las horas no pueden ser negativas."
            )

        return round(hours, 2)

    @staticmethod
    def _normalize_boolean(value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if value in (
            1,
            "1",
            "true",
            "True",
            "sí",
            "si",
            "Sí",
        ):
            return True

        return False

    @staticmethod
    def _normalize_comments(
        comments: Any
    ) -> list[Comment]:
        if not comments:
            return []

        if isinstance(comments, str):
            raw_items = comments.split(
                COMMENT_SEPARATOR
            )

            return [
                Comment.from_storage_text(item)
                for item in raw_items
                if str(item).strip()
            ]

        result = []

        for item in comments:
            if isinstance(item, Comment):
                result.append(item)
            elif isinstance(item, dict):
                result.append(
                    Comment.from_dict(item)
                )
            elif str(item).strip():
                result.append(
                    Comment.from_storage_text(item)
                )

        return result

    def apply_business_rules(self):
        if self.estado == "Finalizada":
            self.avance = 100

            if not self.fecha_finalizacion:
                self.fecha_finalizacion = today_string()

        elif self.avance == 100:
            self.estado = "Finalizada"

            if not self.fecha_finalizacion:
                self.fecha_finalizacion = today_string()

        elif (
            self.estado == "Pendiente"
            and self.avance > 0
        ):
            self.estado = "En curso"

        if (
            self.estado not in (
                "Finalizada",
                "Cancelada"
            )
            and self.fecha_finalizacion
        ):
            self.fecha_finalizacion = ""

    def validate(self) -> bool:
        if not self.titulo:
            raise ValueError(
                "El título es obligatorio."
            )

        if len(self.titulo) > 200:
            raise ValueError(
                "El título no puede superar "
                "los 200 caracteres."
            )

        if len(self.descripcion) > 5000:
            raise ValueError(
                "La descripción no puede superar "
                "los 5000 caracteres."
            )

        if len(self.responsable) > 100:
            raise ValueError(
                "El responsable no puede superar "
                "los 100 caracteres."
            )

        if self.prioridad not in VALID_PRIORITIES:
            raise ValueError(
                f"Prioridad no válida: {self.prioridad}"
            )

        if self.estado not in VALID_STATES:
            raise ValueError(
                f"Estado no válido: {self.estado}"
            )

        if (
            self.fecha_inicio
            and self.fecha_finalizacion
            and self.fecha_finalizacion
            < self.fecha_inicio
        ):
            raise ValueError(
                "La fecha de finalización no puede ser "
                "anterior a la fecha de inicio."
            )

        return True

    def touch(self):
        self.ultima_actualizacion = now_string()

    def add_comment(
        self,
        text: str,
        author: str = "Usuario"
    ) -> Comment:
        comment = Comment(
            author=author,
            text=text
        )

        self.comentarios.append(comment)
        self.touch()

        return comment

    def remove_comment(
        self,
        index: int
    ) -> bool:
        if (
            index < 0
            or index >= len(self.comentarios)
        ):
            return False

        self.comentarios.pop(index)
        self.touch()

        return True

    def add_tag(self, tag: str) -> bool:
        tag = str(
            tag or ""
        ).strip()

        if (
            not tag
            or tag in self.etiquetas
        ):
            return False

        self.etiquetas.append(tag)
        self.touch()

        return True

    def remove_tag(self, tag: str) -> bool:
        tag = str(
            tag or ""
        ).strip()

        if tag not in self.etiquetas:
            return False

        self.etiquetas.remove(tag)
        self.touch()

        return True

    def comments_to_storage(self) -> str:
        return COMMENT_SEPARATOR.join(
            comment.to_storage_text()
            for comment in self.comentarios
        )

    def to_excel_row(self) -> list:
        self.validate()

        return [
            self.id,
            self.titulo,
            self.descripcion,
            self.responsable,
            self.prioridad,
            self.estado,
            self.fecha_creacion,
            self.fecha_inicio,
            self.fecha_prevista,
            self.fecha_finalizacion,
            self.ultima_actualizacion,
            self.avance,
            self.observaciones,
            ", ".join(self.etiquetas),
            self.comments_to_storage(),
            self.favorito,
            self.recordatorio,
            self.proyecto,
            self.tiempo_estimado,
            self.tiempo_empleado,
            2,
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "responsable": self.responsable,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_prevista": self.fecha_prevista,
            "fecha": self.fecha_prevista,
            "fecha_finalizacion": self.fecha_finalizacion,
            "ultima_actualizacion": self.ultima_actualizacion,
            "avance": self.avance,
            "observaciones": self.observaciones,
            "etiquetas": list(self.etiquetas),
            "comentarios": [
                comment.to_dict()
                for comment in self.comentarios
            ],
            "favorito": self.favorito,
            "recordatorio": self.recordatorio,
            "proyecto": self.proyecto,
            "tiempo_estimado": self.tiempo_estimado,
            "tiempo_empleado": self.tiempo_empleado,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        data = dict(data or {})

        return cls(
            id=data.get("id"),
            titulo=data.get("titulo", ""),
            descripcion=data.get("descripcion", ""),
            responsable=data.get("responsable", ""),
            prioridad=data.get("prioridad", "Media"),
            estado=data.get("estado", "Pendiente"),
            fecha_creacion=data.get(
                "fecha_creacion",
                today_string()
            ),
            fecha_inicio=data.get(
                "fecha_inicio",
                ""
            ),
            fecha_prevista=data.get(
                "fecha_prevista",
                data.get("fecha", "")
            ),
            fecha_finalizacion=data.get(
                "fecha_finalizacion",
                ""
            ),
            ultima_actualizacion=data.get(
                "ultima_actualizacion",
                now_string()
            ),
            avance=data.get("avance", 0),
            observaciones=data.get(
                "observaciones",
                ""
            ),
            etiquetas=data.get(
                "etiquetas",
                []
            ),
            comentarios=data.get(
                "comentarios",
                []
            ),
            favorito=data.get(
                "favorito",
                False
            ),
            recordatorio=data.get(
                "recordatorio",
                ""
            ),
            proyecto=data.get(
                "proyecto",
                ""
            ),
            tiempo_estimado=data.get(
                "tiempo_estimado",
                0
            ),
            tiempo_empleado=data.get(
                "tiempo_empleado",
                0
            ),
        )

    @classmethod
    def from_excel_row(cls, row) -> "Task":
        values = list(row)

        if len(values) < 21:
            values.extend(
                [None] * (
                    21 - len(values)
                )
            )

        return cls(
            id=values[0],
            titulo=values[1] or "",
            descripcion=values[2] or "",
            responsable=values[3] or "",
            prioridad=values[4] or "Media",
            estado=values[5] or "Pendiente",
            fecha_creacion=(
                values[6]
                or today_string()
            ),
            fecha_inicio=values[7] or "",
            fecha_prevista=values[8] or "",
            fecha_finalizacion=values[9] or "",
            ultima_actualizacion=(
                values[10]
                or now_string()
            ),
            avance=values[11] or 0,
            observaciones=values[12] or "",
            etiquetas=values[13] or "",
            comentarios=values[14] or "",
            favorito=values[15] or False,
            recordatorio=values[16] or "",
            proyecto=values[17] or "",
            tiempo_estimado=values[18] or 0,
            tiempo_empleado=values[19] or 0,
        )


@dataclass
class HistoryEntry:
    fecha: str
    tarea_id: int
    accion: str
    usuario: str = "Sistema"
    observaciones: str = ""

    def __post_init__(self):
        self.fecha = normalize_datetime(
            self.fecha
        )

        self.tarea_id = int(
            self.tarea_id
        )

        self.accion = str(
            self.accion or ""
        ).strip()

        self.usuario = str(
            self.usuario or "Sistema"
        ).strip() or "Sistema"

        self.observaciones = str(
            self.observaciones or ""
        ).strip()

        if not self.accion:
            raise ValueError(
                "La acción es obligatoria."
            )

    @classmethod
    def create(
        cls,
        tarea_id,
        accion,
        usuario="Sistema",
        observaciones=""
    ) -> "HistoryEntry":
        return cls(
            fecha=now_string(),
            tarea_id=tarea_id,
            accion=accion,
            usuario=usuario,
            observaciones=observaciones,
        )

    def to_excel_row(self) -> list:
        return [
            self.fecha,
            self.tarea_id,
            self.accion,
            self.usuario,
            self.observaciones,
        ]

    def to_dict(self) -> dict:
        return {
            "fecha": self.fecha,
            "task_id": self.tarea_id,
            "accion": self.accion,
            "usuario": self.usuario,
            "observaciones": self.observaciones,
        }


if __name__ == "__main__":
    example = Task(
        titulo="Comprobar comentarios",
        proyecto="ToDo",
        etiquetas=["Frontend", "API"],
    )

    original = example.add_comment(
        "El autor, la fecha y el texto deben conservarse.",
        "Administrador"
    )

    row = example.to_excel_row()
    restored = Task.from_excel_row(row)
    recovered = restored.comentarios[0]

    assert recovered.author == original.author
    assert recovered.created_at == original.created_at
    assert recovered.text == original.text

    print(restored.to_dict())
