from __future__ import annotations

import copy

from dataclasses import dataclass, field, asdict

from datetime import datetime

from pathlib import Path

from typing import List, Optional

from config import (
    DATE_FORMAT,
    DATETIME_FORMAT,

    STATUS_PENDING,
    STATUS_PROGRESS,
    STATUS_BLOCKED,
    STATUS_DONE,

    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_HIGH,
    PRIORITY_CRITICAL
)


# ==========================================================
# HISTORIAL
# ==========================================================

@dataclass(slots=True)
class HistoryEntry:

    fecha: str = ""

    usuario: str = ""

    avance: int = 0

    comentario: str = ""

    def to_dict(self):

        return asdict(self)

    @classmethod
    def from_dict(cls, data):

        return cls(**data)


# ==========================================================
# ADJUNTO
# ==========================================================

@dataclass(slots=True)
class Attachment:

    nombre: str = ""

    ruta: str = ""

    tamano: int = 0

    def exists(self):

        return Path(self.ruta).exists()

    @property
    def filename(self):

        return Path(self.ruta).name

    @property
    def extension(self):

        return Path(self.ruta).suffix.lower()

    def to_dict(self):

        return asdict(self)

    @classmethod
    def from_dict(cls, data):

        return cls(**data)


# ==========================================================
# RESPONSABLE
# ==========================================================

@dataclass(slots=True)
class Owner:

    nombre: str = ""

    departamento: str = ""

    email: str = ""

    telefono: str = ""

    activo: bool = True

    def to_dict(self):

        return asdict(self)


# ==========================================================
# CATEGORÍA
# ==========================================================

@dataclass(slots=True)
class Category:

    nombre: str = ""

    color: str = "#2F80ED"

    icono: str = ""

    def to_dict(self):

        return asdict(self)


# ==========================================================
# ETIQUETA
# ==========================================================

@dataclass(slots=True)
class Tag:

    nombre: str = ""

    color: str = "#2196F3"

    def to_dict(self):

        return asdict(self)


# ==========================================================
# TAREA
# ==========================================================

@dataclass(slots=True)
class Task:

    # ----------------------------------------------
    # Identificación
    # ----------------------------------------------

    id: int = 0

    uuid: str = ""

    version: int = 1

    # ----------------------------------------------
    # Información
    # ----------------------------------------------

    titulo: str = ""

    descripcion: str = ""

    proyecto: str = ""

    categoria: str = ""

    responsable: str = ""

    etiquetas: str = ""

    estado: str = STATUS_PENDING

    prioridad: str = PRIORITY_MEDIUM

    riesgo: str = "Bajo"

    color: str = "#2F80ED"

    favorita: bool = False

    archivada: bool = False

    orden: int = 0

    # ----------------------------------------------
    # Fechas
    # ----------------------------------------------

    fecha_creacion: str = ""

    fecha_inicio: str = ""

    fecha_prevista: str = ""

    fecha_finalizacion: str = ""

    fecha_modificacion: str = ""

    ultima_visualizacion: str = ""

    # ----------------------------------------------
    # Usuarios
    # ----------------------------------------------

    creado_por: str = ""

    modificado_por: str = ""

    # ----------------------------------------------
    # Progreso
    # ----------------------------------------------

    avance: int = 0

    porcentaje_planificado: int = 0

    porcentaje_real: int = 0

    porcentaje_desviacion: float = 0.0

    # ----------------------------------------------
    # Costes
    # ----------------------------------------------

    horas_estimadas: float = 0.0

    horas_reales: float = 0.0

    coste_estimado: float = 0.0

    coste_real: float = 0.0

    # ----------------------------------------------
    # Relaciones
    # ----------------------------------------------

    dependencias: List[int] = field(default_factory=list)

    bloqueantes: List[int] = field(default_factory=list)

    historial: List[HistoryEntry] = field(default_factory=list)

    adjuntos: List[Attachment] = field(default_factory=list)

    comentarios: str = ""
    
    # ======================================================
    # FINALIZAR TAREA
    # ======================================================

    def finalizar(self):

        self.estado = STATUS_DONE

        self.avance = 100

        self.porcentaje_real = 100

        self.fecha_finalizacion = datetime.now().strftime(
            DATE_FORMAT
        )

        self.fecha_modificacion = datetime.now().strftime(
            DATETIME_FORMAT
        )

    # ======================================================
    # COMPLETADA
    # ======================================================

    @property
    def completed(self):

        return self.estado == STATUS_DONE

    # ======================================================
    # ACTIVA
    # ======================================================

    @property
    def active(self):

        return self.estado in (

            STATUS_PENDING,

            STATUS_PROGRESS,

            STATUS_BLOCKED

        )

    # ======================================================
    # RETRASADA
    # ======================================================

    @property
    def overdue(self):

        if self.completed:

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

    @property
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
    # DÍAS RETRASO
    # ======================================================

    @property
    def days_overdue(self):

        dias = self.days_remaining

        if dias is None:

            return None

        return abs(dias) if dias < 0 else 0

    # ======================================================
    # PROGRESO RESTANTE
    # ======================================================

    @property
    def remaining_progress(self):

        return max(

            0,

            100 - self.avance

        )

    # ======================================================
    # COLOR PROGRESO
    # ======================================================

    @property
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
    # DESVIACIÓN
    # ======================================================

    @property
    def progress_deviation(self):

        return (

            self.porcentaje_real

            - self.porcentaje_planificado

        )

    # ======================================================
    # MODIFICADA
    # ======================================================

    def touch(self):

        self.fecha_modificacion = datetime.now().strftime(

            DATETIME_FORMAT

        )
        
        
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

        self.touch()

    # ======================================================
    # ADJUNTOS
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

        self.touch()

    def remove_attachment(

        self,

        nombre

    ):

        self.adjuntos = [

            a

            for a

            in self.adjuntos

            if a.nombre != nombre

        ]

        self.touch()

    # ======================================================
    # DEPENDENCIAS
    # ======================================================

    def add_dependency(

        self,

        task_id

    ):

        if task_id not in self.dependencias:

            self.dependencias.append(task_id)

    def remove_dependency(

        self,

        task_id

    ):

        if task_id in self.dependencias:

            self.dependencias.remove(task_id)

    # ======================================================
    # BLOQUEANTES
    # ======================================================

    def add_blocker(

        self,

        task_id

    ):

        if task_id not in self.bloqueantes:

            self.bloqueantes.append(task_id)

    def remove_blocker(

        self,

        task_id

    ):

        if task_id in self.bloqueantes:

            self.bloqueantes.remove(task_id)
            
            
            
    # ======================================================
    # VALIDACIÓN
    # ======================================================

    def validate(self):

        errores = []

        if not self.titulo.strip():

            errores.append(
                "El título es obligatorio."
            )

        if not self.responsable.strip():

            errores.append(
                "Debe indicar un responsable."
            )

        if self.estado not in (

            STATUS_PENDING,

            STATUS_PROGRESS,

            STATUS_BLOCKED,

            STATUS_DONE

        ):

            errores.append(
                "Estado incorrecto."
            )

        if self.prioridad not in (

            PRIORITY_LOW,

            PRIORITY_MEDIUM,

            PRIORITY_HIGH,

            PRIORITY_CRITICAL

        ):

            errores.append(
                "Prioridad incorrecta."
            )

        if self.avance < 0 or self.avance > 100:

            errores.append(
                "El avance debe estar entre 0 y 100."
            )

        if self.porcentaje_planificado < 0 or self.porcentaje_planificado > 100:

            errores.append(
                "Porcentaje planificado incorrecto."
            )

        if self.porcentaje_real < 0 or self.porcentaje_real > 100:

            errores.append(
                "Porcentaje real incorrecto."
            )

        if self.horas_estimadas < 0:

            errores.append(
                "Las horas estimadas no pueden ser negativas."
            )

        if self.horas_reales < 0:

            errores.append(
                "Las horas reales no pueden ser negativas."
            )

        if self.coste_estimado < 0:

            errores.append(
                "El coste estimado no puede ser negativo."
            )

        if self.coste_real < 0:

            errores.append(
                "El coste real no puede ser negativo."
            )

        if self.fecha_inicio and self.fecha_prevista:

            try:

                inicio = datetime.strptime(
                    self.fecha_inicio,
                    DATE_FORMAT
                )

                prevista = datetime.strptime(
                    self.fecha_prevista,
                    DATE_FORMAT
                )

                if prevista < inicio:

                    errores.append(
                        "La fecha prevista es anterior a la fecha de inicio."
                    )

            except Exception:

                errores.append(
                    "Formato de fecha incorrecto."
                )

        return errores

    # ======================================================
    # SERIALIZAR
    # ======================================================

    def to_dict(self):

        datos = asdict(self)

        datos["historial"] = [

            h.to_dict()

            for h in self.historial

        ]

        datos["adjuntos"] = [

            a.to_dict()

            for a in self.adjuntos

        ]

        return datos

    # ======================================================
    # DESERIALIZAR
    # ======================================================

    @classmethod
    def from_dict(cls, data):

        task = cls()

        for campo, valor in data.items():

            if campo == "historial":

                task.historial = [

                    HistoryEntry.from_dict(h)

                    for h in valor

                ]

            elif campo == "adjuntos":

                task.adjuntos = [

                    Attachment.from_dict(a)

                    for a in valor

                ]

            elif hasattr(task, campo):

                setattr(task, campo, valor)

        return task

    # ======================================================
    # CLONAR
    # ======================================================

    def clone(self):

        return copy.deepcopy(self)

    # ======================================================
    # COPIA PARA EXPORTACIÓN
    # ======================================================

    def export_dict(self):

        datos = self.to_dict()

        datos.pop("historial", None)

        datos.pop("adjuntos", None)

        return datos

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================

    def __str__(self):

        return (

            f"[{self.id}] "

            f"{self.titulo} "

            f"({self.estado})"

        )

    def __repr__(self):

        return self.__str__()

    # ======================================================
    # COMPARACIÓN
    # ======================================================

    def __lt__(self, other):

        return self.fecha_prevista < other.fecha_prevista

    def __eq__(self, other):

        return self.id == other.id
        
        
# ==========================================================
# PROYECTO
# ==========================================================

@dataclass(slots=True)
class Project:

    id: int = 0

    nombre: str = ""

    descripcion: str = ""

    responsable: str = ""

    cliente: str = ""

    color: str = "#2F80ED"

    fecha_inicio: str = ""

    fecha_fin: str = ""

    presupuesto: float = 0.0

    coste_real: float = 0.0

    activo: bool = True

    tareas: List[int] = field(default_factory=list)

    # ------------------------------------------------------

    def add_task(self, task_id):

        if task_id not in self.tareas:

            self.tareas.append(task_id)

    # ------------------------------------------------------

    def remove_task(self, task_id):

        if task_id in self.tareas:

            self.tareas.remove(task_id)

    # ------------------------------------------------------

    @property
    def total_tasks(self):

        return len(self.tareas)

    # ------------------------------------------------------

    def progress(self, tasks):

        proyecto = [

            t

            for t in tasks

            if t.id in self.tareas

        ]

        if not proyecto:

            return 0

        return round(

            sum(t.avance for t in proyecto)

            / len(proyecto),

            1

        )

    # ------------------------------------------------------

    def to_dict(self):

        return asdict(self)

    @classmethod
    def from_dict(cls, data):

        return cls(**data)


# ==========================================================
# NOTIFICACIÓN
# ==========================================================

@dataclass(slots=True)
class Notification:

    tipo: str = "INFO"

    prioridad: str = "NORMAL"

    titulo: str = ""

    mensaje: str = ""

    responsable: str = ""

    fecha: str = ""

    fecha_lectura: str = ""

    leida: bool = False

    # ------------------------------------------------------

    def mark_as_read(self):

        self.leida = True

        self.fecha_lectura = datetime.now().strftime(

            DATETIME_FORMAT

        )

    # ------------------------------------------------------

    def mark_as_unread(self):

        self.leida = False

        self.fecha_lectura = ""

    # ------------------------------------------------------

    def to_dict(self):

        return asdict(self)

    @classmethod
    def from_dict(cls, data):

        return cls(**data)


# ==========================================================
# WIDGET DASHBOARD
# ==========================================================

@dataclass(slots=True)
class DashboardWidget:

    nombre: str = ""

    visible: bool = True

    posicion: int = 0

    alto: int = 250

    ancho: int = 350

    color: str = "#2F80ED"

    configuracion: dict = field(default_factory=dict)

    def to_dict(self):

        return asdict(self)


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

@dataclass(slots=True)
class AppSettings:

    usuario: str = ""

    idioma: str = "es"

    tema: str = "Claro"

    color_principal: str = "#2F80ED"

    zoom: int = 100

    autosave: bool = True

    backup_on_exit: bool = True

    auto_powerbi: bool = False

    dias_aviso: int = 3

    ultima_apertura: str = ""

    ultimo_proyecto: str = ""

    ultimo_filtro: str = ""

    ultima_pestana: int = 0

    sidebar_width: int = 280

    max_backups: int = 30

    mostrar_dashboard: bool = True

    mostrar_calendario: bool = True

    mostrar_kanban: bool = True

    mostrar_gantt: bool = True

    mostrar_tabla: bool = True

    widgets: List[DashboardWidget] = field(default_factory=list)

    # ------------------------------------------------------

    def to_dict(self):

        datos = asdict(self)

        datos["widgets"] = [

            w.to_dict()

            for w in self.widgets

        ]

        return datos

    @classmethod
    def from_dict(cls, data):

        cfg = cls()

        for k, v in data.items():

            if k == "widgets":

                cfg.widgets = [

                    DashboardWidget(**x)

                    for x in v

                ]

            elif hasattr(cfg, k):

                setattr(cfg, k, v)

        return cfg
        
        
        
# ==========================================================
# ENUMERACIONES
# ==========================================================

TASK_STATUS = (

    STATUS_PENDING,

    STATUS_PROGRESS,

    STATUS_BLOCKED,

    STATUS_DONE

)

TASK_PRIORITY = (

    PRIORITY_LOW,

    PRIORITY_MEDIUM,

    PRIORITY_HIGH,

    PRIORITY_CRITICAL

)

TASK_RISK = (

    "Bajo",

    "Normal",

    "Alto",

    "Crítico"

)


# ==========================================================
# UTILIDADES
# ==========================================================

def now():

    """
    Fecha y hora actual.
    """

    return datetime.now().strftime(

        DATETIME_FORMAT

    )


def today():

    """
    Fecha actual.
    """

    return datetime.now().strftime(

        DATE_FORMAT

    )


def parse_date(value):

    """
    Convierte una cadena DD/MM/YYYY en datetime.
    """

    if not value:

        return None

    try:

        return datetime.strptime(

            value,

            DATE_FORMAT

        )

    except Exception:

        return None


# ==========================================================
# FACTORY TASK
# ==========================================================

def create_task():

    """
    Crea una nueva tarea con valores por defecto.
    """

    task = Task()

    task.fecha_creacion = today()

    task.fecha_modificacion = now()

    task.estado = STATUS_PENDING

    task.prioridad = PRIORITY_MEDIUM

    task.avance = 0

    task.version = 1

    return task


# ==========================================================
# FACTORY PROJECT
# ==========================================================

def create_project():

    proyecto = Project()

    proyecto.fecha_inicio = today()

    return proyecto


# ==========================================================
# VALIDADORES
# ==========================================================

def validate_task(task: Task):

    return task.validate()


def validate_project(project: Project):

    errores = []

    if not project.nombre.strip():

        errores.append(

            "Debe indicar un nombre."

        )

    if project.presupuesto < 0:

        errores.append(

            "El presupuesto no puede ser negativo."

        )

    if project.coste_real < 0:

        errores.append(

            "El coste real no puede ser negativo."

        )

    return errores


# ==========================================================
# EXPORTACIÓN
# ==========================================================

def task_to_excel(task: Task):

    """
    Devuelve un diccionario preparado para Excel.
    """

    return task.export_dict()


def task_to_json(task: Task):

    return task.to_dict()


# ==========================================================
# IMPORTACIÓN
# ==========================================================

def task_from_json(data):

    return Task.from_dict(data)


# ==========================================================
# VERSIÓN DEL MODELO
# ==========================================================

MODEL_VERSION = "2.0.0"


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "HistoryEntry",

    "Attachment",

    "Owner",

    "Category",

    "Tag",

    "Task",

    "Project",

    "Notification",

    "DashboardWidget",

    "AppSettings",

    "TASK_STATUS",

    "TASK_PRIORITY",

    "TASK_RISK",

    "MODEL_VERSION",

    "today",

    "now",

    "parse_date",

    "create_task",

    "create_project",

    "validate_task",

    "validate_project",

    "task_to_excel",

    "task_to_json",

    "task_from_json"

]
    
    
    
    
    
    
    
    
    
    
    
    
