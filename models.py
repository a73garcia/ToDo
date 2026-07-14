from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from config import (
    DATE_FORMAT,
    DATETIME_FORMAT,
    STATUS_PENDING,
    PRIORITY_MEDIUM
)


# ==========================================================
# HISTORIAL
# ==========================================================

@dataclass
class HistoryEntry:

    fecha: str
    usuario: str
    avance: int
    comentario: str

    def to_dict(self):

        return {

            "fecha": self.fecha,

            "usuario": self.usuario,

            "avance": self.avance,

            "comentario": self.comentario

        }


# ==========================================================
# ADJUNTO
# ==========================================================

@dataclass
class Attachment:

    nombre: str
    ruta: str
    tamano: int = 0

    def exists(self):

        from pathlib import Path

        return Path(self.ruta).exists()


# ==========================================================
# RESPONSABLE
# ==========================================================

@dataclass
class Owner:

    nombre: str = ""
    departamento: str = ""
    email: str = ""

    def to_dict(self):

        return self.__dict__.copy()


# ==========================================================
# CATEGORÍA
# ==========================================================

@dataclass
class Category:

    nombre: str = ""
    color: str = "#2F80ED"

    def to_dict(self):

        return self.__dict__.copy()


# ==========================================================
# TAREA
# ==========================================================

@dataclass
class Task:

    id: int = 0

    titulo: str = ""

    descripcion: str = ""

    responsable: str = ""

    estado: str = STATUS_PENDING

    prioridad: str = PRIORITY_MEDIUM

    categoria: str = ""

    etiquetas: str = ""

    proyecto: str = ""

    fecha_creacion: str = ""

    fecha_inicio: str = ""

    fecha_prevista: str = ""

    fecha_finalizacion: str = ""

    fecha_modificacion: str = ""

    creado_por: str = ""

    modificado_por: str = ""

    avance: int = 0

    favorita: bool = False

    color: str = "#2F80ED"

    riesgo: str = "Normal"

    horas_estimadas: float = 0.0

    horas_reales: float = 0.0

    coste_estimado: float = 0.0

    coste_real: float = 0.0

    porcentaje_planificado: int = 0

    porcentaje_desviacion: float = 0.0

    comentarios: str = ""

    historial: List[HistoryEntry] = field(default_factory=list)

    adjuntos: List[Attachment] = field(default_factory=list)

    # ======================================================
    # FINALIZAR
    # ======================================================

    def finalizar(self):

        self.estado = "Finalizada"

        self.avance = 100

        self.fecha_finalizacion = datetime.now().strftime(

            DATE_FORMAT

        )

    # ======================================================
    # RETRASADA
    # ======================================================

    def esta_retrasada(self):

        if self.estado == "Finalizada":

            return False

        if not self.fecha_prevista:

            return False

        try:

            fecha = datetime.strptime(

                self.fecha_prevista,

                DATE_FORMAT

            )

            return fecha.date() < datetime.today().date()

        except Exception:

            return False
            
    # ======================================================
    # DÍAS RESTANTES
    # ======================================================

    def days_remaining(self):

        if not self.fecha_prevista:

            return None

        try:

            fecha = datetime.strptime(
                self.fecha_prevista,
                DATE_FORMAT
            )

            return (
                fecha.date()
                - datetime.today().date()
            ).days

        except Exception:

            return None

    # ======================================================
    # DÍAS DE RETRASO
    # ======================================================

    def days_overdue(self):

        dias = self.days_remaining()

        if dias is None:

            return None

        return abs(dias) if dias < 0 else 0

    # ======================================================
    # PORCENTAJE RESTANTE
    # ======================================================

    def remaining_progress(self):

        return max(0, 100 - self.avance)

    # ======================================================
    # COMPLETADA
    # ======================================================

    def is_completed(self):

        return self.estado == "Finalizada"

    # ======================================================
    # EN CURSO
    # ======================================================

    def is_active(self):

        return self.estado in (

            "Pendiente",

            "En curso",

            "Bloqueada"

        )

    # ======================================================
    # COLOR DEL PROGRESO
    # ======================================================

    def progress_color(self):

        if self.avance >= 100:

            return "#4CAF50"

        elif self.avance >= 75:

            return "#8BC34A"

        elif self.avance >= 50:

            return "#FFC107"

        elif self.avance >= 25:

            return "#FF9800"

        return "#F44336"

    # ======================================================
    # AÑADIR HISTORIAL
    # ======================================================

    def add_history(

        self,

        usuario,

        avance,

        comentario

    ):

        self.historial.append(

            HistoryEntry(

                fecha=datetime.now().strftime(
                    DATETIME_FORMAT
                ),

                usuario=usuario,

                avance=avance,

                comentario=comentario

            )

        )

    # ======================================================
    # AÑADIR ADJUNTO
    # ======================================================

    def add_attachment(

        self,

        nombre,

        ruta,

        tamano=0

    ):

        self.adjuntos.append(

            Attachment(

                nombre,

                ruta,

                tamano

            )

        )

    # ======================================================
    # ELIMINAR ADJUNTO
    # ======================================================

    def remove_attachment(

        self,

        nombre

    ):

        self.adjuntos = [

            a

            for a in self.adjuntos

            if a.nombre != nombre

        ]

    # ======================================================
    # SERIALIZAR
    # ======================================================

    def to_dict(self):

        return {

            "id": self.id,

            "titulo": self.titulo,

            "descripcion": self.descripcion,

            "responsable": self.responsable,

            "estado": self.estado,

            "prioridad": self.prioridad,

            "categoria": self.categoria,

            "etiquetas": self.etiquetas,

            "proyecto": self.proyecto,

            "fecha_creacion": self.fecha_creacion,

            "fecha_inicio": self.fecha_inicio,

            "fecha_prevista": self.fecha_prevista,

            "fecha_finalizacion": self.fecha_finalizacion,

            "fecha_modificacion": self.fecha_modificacion,

            "creado_por": self.creado_por,

            "modificado_por": self.modificado_por,

            "avance": self.avance,

            "favorita": self.favorita,

            "color": self.color,

            "riesgo": self.riesgo,

            "horas_estimadas": self.horas_estimadas,

            "horas_reales": self.horas_reales,

            "coste_estimado": self.coste_estimado,

            "coste_real": self.coste_real,

            "porcentaje_planificado": self.porcentaje_planificado,

            "porcentaje_desviacion": self.porcentaje_desviacion,

            "comentarios": self.comentarios,

            "historial": [

                h.to_dict()

                for h in self.historial

            ],

            "adjuntos": [

                {

                    "nombre": a.nombre,

                    "ruta": a.ruta,

                    "tamano": a.tamano

                }

                for a in self.adjuntos

            ]

        }

    # ======================================================
    # CLONAR
    # ======================================================

    def clone(self):

        import copy

        return copy.deepcopy(self)
        
# ==========================================================
# DESERIALIZAR
# ==========================================================

    @classmethod
    def from_dict(cls, data):

        task = cls()

        for key, value in data.items():

            if key == "historial":

                task.historial = [

                    HistoryEntry(**h)

                    for h in value

                ]

            elif key == "adjuntos":

                task.adjuntos = [

                    Attachment(**a)

                    for a in value

                ]

            elif hasattr(task, key):

                setattr(task, key, value)

        return task

    # ======================================================
    # VALIDACIÓN
    # ======================================================

    def validate(self):

        errores = []

        if not self.titulo.strip():

            errores.append("El título es obligatorio.")

        if self.avance < 0 or self.avance > 100:

            errores.append("El avance debe estar entre 0 y 100.")

        if self.horas_estimadas < 0:

            errores.append("Las horas estimadas no pueden ser negativas.")

        if self.horas_reales < 0:

            errores.append("Las horas reales no pueden ser negativas.")

        if self.coste_estimado < 0:

            errores.append("El coste estimado no puede ser negativo.")

        if self.coste_real < 0:

            errores.append("El coste real no puede ser negativo.")

        return errores

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================

    def __str__(self):

        return f"[{self.id}] {self.titulo}"

    def __repr__(self):

        return self.__str__()


# ==========================================================
# PROYECTO
# ==========================================================

@dataclass
class Project:

    nombre: str = ""

    descripcion: str = ""

    responsable: str = ""

    fecha_inicio: str = ""

    fecha_fin: str = ""

    color: str = "#2F80ED"

    tareas: List[int] = field(default_factory=list)

    def add_task(self, task_id):

        if task_id not in self.tareas:

            self.tareas.append(task_id)

    def remove_task(self, task_id):

        if task_id in self.tareas:

            self.tareas.remove(task_id)

    @property
    def total_tasks(self):

        return len(self.tareas)


# ==========================================================
# NOTIFICACIÓN
# ==========================================================

@dataclass
class Notification:

    tipo: str = "INFO"

    titulo: str = ""

    mensaje: str = ""

    fecha: str = ""

    leida: bool = False

    responsable: str = ""

    def mark_as_read(self):

        self.leida = True

    def to_dict(self):

        return self.__dict__.copy()


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

@dataclass
class AppSettings:

    tema: str = "Claro"

    idioma: str = "es"

    autosave: bool = True

    backup_on_exit: bool = True

    powerbi_auto_refresh: bool = False

    dias_aviso: int = 3

    mostrar_finalizadas: bool = True

    color_principal: str = "#2F80ED"

    ultima_apertura: str = ""

    usuario: str = ""

    def to_dict(self):

        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):

        cfg = cls()

        for key, value in data.items():

            if hasattr(cfg, key):

                setattr(cfg, key, value)

        return cfg


# ==========================================================
# ENUMERACIONES
# ==========================================================

TASK_STATUS = [

    "Pendiente",

    "En curso",

    "Bloqueada",

    "Finalizada"

]

TASK_PRIORITY = [

    "Baja",

    "Media",

    "Alta",

    "Crítica"

]

TASK_RISK = [

    "Bajo",

    "Normal",

    "Alto",

    "Crítico"

]
