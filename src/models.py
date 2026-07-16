"""
src/models.py
Modelos de datos del proyecto ToDo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


DATE_FMT = "%Y-%m-%d"
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Task:
    id: Optional[int] = None
    titulo: str = ""
    descripcion: str = ""
    responsable: str = ""
    prioridad: str = "Media"
    estado: str = "Pendiente"

    fecha_creacion: str = field(default_factory=lambda: datetime.now().strftime(DATE_FMT))
    fecha_inicio: str = ""
    fecha_prevista: str = ""
    fecha_finalizacion: str = ""
    ultima_actualizacion: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FMT))

    avance: int = 0
    observaciones: str = ""

    def validate(self):
        if not self.titulo.strip():
            raise ValueError("El título es obligatorio.")

        if self.avance < 0 or self.avance > 100:
            raise ValueError("El avance debe estar entre 0 y 100.")

    def to_excel_row(self):
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
        ]

    @classmethod
    def from_excel_row(cls, row):
        return cls(
            id=row[0],
            titulo=row[1] or "",
            descripcion=row[2] or "",
            responsable=row[3] or "",
            prioridad=row[4] or "Media",
            estado=row[5] or "Pendiente",
            fecha_creacion=row[6] or "",
            fecha_inicio=row[7] or "",
            fecha_prevista=row[8] or "",
            fecha_finalizacion=row[9] or "",
            ultima_actualizacion=row[10] or "",
            avance=row[11] or 0,
            observaciones=row[12] or "",
        )


@dataclass
class HistoryEntry:
    fecha: str
    tarea_id: int
    accion: str
    usuario: str
    observaciones: str = ""

    @classmethod
    def create(cls, tarea_id, accion, usuario="Sistema", observaciones=""):
        return cls(
            fecha=datetime.now().strftime(DATETIME_FMT),
            tarea_id=tarea_id,
            accion=accion,
            usuario=usuario,
            observaciones=observaciones,
        )

    def to_excel_row(self):
        return [
            self.fecha,
            self.tarea_id,
            self.accion,
            self.usuario,
            self.observaciones,
        ]
