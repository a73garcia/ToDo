from __future__ import annotations

import copy

from datetime import datetime

from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from models import Task
from models import Project
from models import Category
from models import Owner


class TaskManager:
    """
    Gestor principal de tareas.

    Responsabilidades

        • CRUD de tareas
        • CRUD de proyectos
        • Historial
        • Undo / Redo
        • Notificaciones
        • Sincronización
        • Eventos
    """

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(

        self,

        excel_manager=None,

        metrics_manager=None,

        backup_manager=None,

        report_manager=None,

        powerbi_manager=None

    ):

        self.excel = excel_manager

        self.metrics = metrics_manager

        self.backup = backup_manager

        self.report = report_manager

        self.powerbi = powerbi_manager

        self.tasks: List[Task] = []

        self.projects: Dict[str, Project] = {}

        self.categories: Dict[str, Category] = {}

        self.owners: Dict[str, Owner] = {}

        self.modified = False

        self.undo_stack = []

        self.redo_stack = []

        self.listeners: List[Callable] = []

    # =====================================================
    # OBSERVADORES
    # =====================================================

    def add_listener(

        self,

        callback

    ):

        if callback not in self.listeners:

            self.listeners.append(

                callback

            )

    def remove_listener(

        self,

        callback

    ):

        if callback in self.listeners:

            self.listeners.remove(

                callback

            )

    def notify(

        self,

        event,

        task=None

    ):

        for callback in self.listeners:

            try:

                callback(

                    event,

                    task

                )

            except Exception:

                pass

    # =====================================================
    # CARGA
    # =====================================================

    def load(

        self,

        tasks

    ):

        self.tasks = list(tasks)

        self.modified = False

        self.notify(

            "loaded"

        )

    # =====================================================
    # LISTADO
    # =====================================================

    def all_tasks(self):

        return self.tasks

    def count(self):

        return len(

            self.tasks

        )

    # =====================================================
    # BUSCAR
    # =====================================================

    def get(

        self,

        task_id

    ) -> Optional[Task]:

        for task in self.tasks:

            if task.id == task_id:

                return task

        return None

    # =====================================================
    # EXISTE
    # =====================================================

    def exists(

        self,

        task_id

    ):

        return self.get(

            task_id

        ) is not None

    # =====================================================
    # NUEVO ID
    # =====================================================

    def next_id(self):

        if not self.tasks:

            return 1

        return max(

            t.id

            for t in self.tasks

        ) + 1

    # =====================================================
    # SNAPSHOT
    # =====================================================

    def save_state(self):

        self.undo_stack.append(

            copy.deepcopy(

                self.tasks

            )

        )

        self.redo_stack.clear()

    # =====================================================
    # MODIFICADO
    # =====================================================

    def touch(self):

        self.modified = True

        self.notify(

            "modified"

        )

    # =====================================================
    # NUEVA TAREA
    # =====================================================

    def add_task(

        self,

        task

    ):

        self.save_state()

        if task.id == 0:

            task.id = self.next_id()

        task.fecha_creacion = datetime.now().strftime(

            "%d/%m/%Y"

        )

        self.tasks.append(

            task

        )

        self.touch()

        self.notify(

            "task_added",

            task

        )

        return task

    # =====================================================
    # ELIMINAR
    # =====================================================

    def delete_task(

        self,

        task_id

    ):

        tarea = self.get(

            task_id

        )

        if tarea is None:

            return False

        self.save_state()

        self.tasks.remove(

            tarea

        )

        self.touch()

        self.notify(

            "task_deleted",

            tarea

        )

        return True

    # =====================================================
    # ACTUALIZAR
    # =====================================================

    def update_task(

        self,

        task

    ):

        actual = self.get(

            task.id

        )

        if actual is None:

            return False

        self.save_state()

        actual.__dict__.update(

            task.__dict__

        )

        actual.fecha_modificacion = datetime.now().strftime(

            "%d/%m/%Y %H:%M"

        )

        self.touch()

        self.notify(

            "task_updated",

            actual

        )

        return True
        
    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def change_status(

        self,

        task_id,

        new_status,

        user="Sistema"

    ):

        task = self.get(task_id)

        if task is None:

            return False

        if task.estado == new_status:

            return True

        self.save_state()

        old_status = task.estado

        task.estado = new_status

        if new_status == "Finalizada":

            task.finalizar()

        task.add_history(

            user,

            task.avance,

            f"Estado: {old_status} → {new_status}"

        )

        self.touch()

        self.notify(

            "task_status_changed",

            task

        )

        return True

    # =====================================================
    # CAMBIAR AVANCE
    # =====================================================

    def change_progress(

        self,

        task_id,

        progress,

        user="Sistema"

    ):

        task = self.get(task_id)

        if task is None:

            return False

        progress = max(

            0,

            min(

                100,

                int(progress)

            )

        )

        if progress == task.avance:

            return True

        self.save_state()

        task.avance = progress

        if progress == 100:

            task.estado = "Finalizada"

            task.fecha_finalizacion = datetime.now().strftime(

                "%d/%m/%Y"

            )

        elif progress > 0 and task.estado == "Pendiente":

            task.estado = "En curso"

        task.add_history(

            user,

            progress,

            f"Avance actualizado al {progress}%"

        )

        self.touch()

        self.notify(

            "task_progress_changed",

            task

        )

        return True

    # =====================================================
    # CAMBIAR RESPONSABLE
    # =====================================================

    def assign_owner(

        self,

        task_id,

        owner,

        user="Sistema"

    ):

        task = self.get(task_id)

        if task is None:

            return False

        self.save_state()

        anterior = task.responsable

        task.responsable = owner

        task.add_history(

            user,

            task.avance,

            f"Responsable: {anterior} → {owner}"

        )

        self.touch()

        self.notify(

            "task_owner_changed",

            task

        )

        return True

    # =====================================================
    # CAMBIAR FECHAS
    # =====================================================

    def update_dates(

        self,

        task_id,

        start_date=None,

        due_date=None,

        finish_date=None,

        user="Sistema"

    ):

        task = self.get(task_id)

        if task is None:

            return False

        self.save_state()

        if start_date is not None:

            task.fecha_inicio = start_date

        if due_date is not None:

            task.fecha_prevista = due_date
        if finish_date is not None:

            task.fecha_finalizacion = finish_date

        task.add_history(

            user,

            task.avance,

            "Fechas modificadas"

        )

        self.touch()

        self.notify(

            "task_dates_changed",

            task

        )

        return True

    # =====================================================
    # DUPLICAR
    # =====================================================

    def duplicate_task(

        self,

        task_id

    ):

        original = self.get(task_id)

        if original is None:

            return None

        self.save_state()

        nueva = original.clone()

        nueva.id = self.next_id()

        nueva.titulo = f"{nueva.titulo} (Copia)"

        nueva.fecha_creacion = datetime.now().strftime(

            "%d/%m/%Y"

        )

        nueva.fecha_modificacion = ""

        nueva.fecha_finalizacion = ""

        nueva.historial = []

        self.tasks.append(

            nueva

        )

        self.touch()

        self.notify(

            "task_duplicated",

            nueva

        )

        return nueva

    # =====================================================
    # FAVORITA
    # =====================================================

    def set_favorite(

        self,

        task_id,

        favorite=True

    ):

        task = self.get(task_id)

        if task is None:

            return False

        task.favorita = favorite

        self.touch()

        self.notify(

            "task_favorite",

            task

        )

        return True

    # =====================================================
    # MOVER ENTRE PROYECTOS
    # =====================================================

    def move_project(

        self,

        task_id,

        project

    ):

        task = self.get(task_id)

        if task is None:

            return False

        self.save_state()

        task.proyecto = project

        self.touch()

        self.notify(

            "task_project_changed",

            task

        )

        return True
        
        
    # =====================================================
    # AÑADIR HISTORIAL
    # =====================================================

    def add_history(

        self,

        task_id,

        comentario,

        usuario="Sistema",

        avance=None

    ):

        task = self.get(task_id)

        if task is None:

            return False

        if avance is None:

            avance = task.avance

        self.save_state()

        task.add_history(

            usuario,

            avance,

            comentario

        )

        self.touch()

        self.notify(

            "task_history_added",

            task

        )

        return True

    # =====================================================
    # AÑADIR ADJUNTO
    # =====================================================

    def add_attachment(

        self,

        task_id,

        nombre,

        ruta,

        tamano=0

    ):

        task = self.get(task_id)

        if task is None:

            return False

        self.save_state()

        task.add_attachment(

            nombre,

            ruta,

            tamano

        )

        self.touch()

        self.notify(

            "task_attachment_added",

            task

        )

        return True

    # =====================================================
    # ELIMINAR ADJUNTO
    # =====================================================

    def remove_attachment(

        self,

        task_id,

        nombre

    ):

        task = self.get(task_id)

        if task is None:

            return False

        self.save_state()

        task.remove_attachment(

            nombre

        )

        self.touch()

        self.notify(

            "task_attachment_removed",

            task

        )

        return True

    # =====================================================
    # BUSCAR POR TEXTO
    # =====================================================

    def search(

        self,

        text

    ):

        texto = text.lower().strip()

        if not texto:

            return self.tasks

        return [

            t

            for t in self.tasks

            if (

                texto in t.titulo.lower()

                or texto in t.descripcion.lower()

                or texto in t.responsable.lower()

                or texto in t.proyecto.lower()

                or texto in t.categoria.lower()

                or texto in t.etiquetas.lower()

            )

        ]

    # =====================================================
    # FILTRAR POR ESTADO
    # =====================================================

    def filter_status(

        self,

        estado

    ):

        return [

            t

            for t in self.tasks

            if t.estado == estado

        ]

    # =====================================================
    # FILTRAR POR PRIORIDAD
    # =====================================================

    def filter_priority(

        self,

        prioridad

    ):

        return [

            t

            for t in self.tasks

            if t.prioridad == prioridad

        ]

    # =====================================================
    # FILTRAR POR RESPONSABLE
    # =====================================================

    def filter_owner(

        self,

        owner

    ):

        return [

            t

            for t in self.tasks

            if t.responsable == owner

        ]

    # =====================================================
    # FILTRAR POR PROYECTO
    # =====================================================

    def filter_project(

        self,

        project

    ):

        return [

            t

            for t in self.tasks

            if t.proyecto == project

        ]

    # =====================================================
    # FILTRAR FAVORITAS
    # =====================================================

    def favorites(self):

        return [

            t

            for t in self.tasks

            if t.favorita

        ]

    # =====================================================
    # TAREAS RETRASADAS
    # =====================================================

    def overdue_tasks(self):

        return [

            t

            for t in self.tasks

            if t.esta_retrasada()

        ]

    # =====================================================
    # TAREAS FINALIZADAS
    # =====================================================

    def completed_tasks(self):

        return [

            t

            for t in self.tasks

            if t.is_completed()

        ]

    # =====================================================
    # TAREAS ACTIVAS
    # =====================================================

    def active_tasks(self):

        return [

            t

            for t in self.tasks

            if t.is_active()

        ]

    # =====================================================
    # ORDENAR
    # =====================================================

    def sort_by_title(self):

        self.tasks.sort(

            key=lambda t: t.titulo.lower()

        )

        self.notify(

            "tasks_sorted"

        )

    def sort_by_due_date(self):

        self.tasks.sort(

            key=lambda t: (

                t.fecha_prevista or "99/99/9999"

            )

        )

        self.notify(

            "tasks_sorted"

        )

    def sort_by_priority(self):

        orden = {

            "Crítica": 0,

            "Alta": 1,

            "Media": 2,

            "Baja": 3

        }

        self.tasks.sort(

            key=lambda t: orden.get(

                t.prioridad,

                99

            )

        )

        self.notify(

            "tasks_sorted"

        )
        
    # =====================================================
    # PROYECTOS
    # =====================================================

    def add_project(

        self,

        project: Project

    ):

        self.projects[

            project.nombre

        ] = project

        self.touch()

        self.notify(

            "project_added",

            project

        )

    def get_project(

        self,

        name

    ):

        return self.projects.get(

            name

        )

    def remove_project(

        self,

        name

    ):

        if name not in self.projects:

            return False

        del self.projects[name]

        self.touch()

        self.notify(

            "project_removed",

            name

        )

        return True

    def all_projects(self):

        return list(

            self.projects.values()

        )

    # =====================================================
    # CATEGORÍAS
    # =====================================================

    def add_category(

        self,

        category: Category

    ):

        self.categories[

            category.nombre

        ] = category

        self.touch()

        self.notify(

            "category_added",

            category

        )

    def get_category(

        self,

        name

    ):

        return self.categories.get(

            name

        )

    def remove_category(

        self,

        name

    ):

        if name not in self.categories:

            return False

        del self.categories[name]

        self.touch()

        self.notify(

            "category_removed",

            name

        )

        return True

    def all_categories(self):

        return list(

            self.categories.values()

        )

    # =====================================================
    # RESPONSABLES
    # =====================================================

    def add_owner(

        self,

        owner: Owner

    ):

        self.owners[

            owner.nombre

        ] = owner

        self.touch()

        self.notify(

            "owner_added",

            owner

        )

    def get_owner(

        self,

        name

    ):

        return self.owners.get(

            name

        )

    def remove_owner(

        self,

        name

    ):

        if name not in self.owners:

            return False

        del self.owners[name]

        self.touch()

        self.notify(

            "owner_removed",

            name

        )

        return True

    def all_owners(self):

        return list(

            self.owners.values()

        )

    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    def statistics(self):

        return {

            "total": len(

                self.tasks

            ),

            "pending": len(

                self.filter_status(

                    "Pendiente"

                )

            ),

            "progress": len(

                self.filter_status(

                    "En curso"

                )

            ),

            "blocked": len(

                self.filter_status(

                    "Bloqueada"

                )

            ),

            "completed": len(

                self.completed_tasks()

            ),

            "favorites": len(

                self.favorites()

            ),

            "overdue": len(

                self.overdue_tasks()

            )

        }

    # =====================================================
    # PORCENTAJE COMPLETADO
    # =====================================================

    def completion_percentage(self):

        total = len(

            self.tasks

        )

        if total == 0:

            return 0

        return round(

            (

                len(

                    self.completed_tasks()

                )

                / total

            ) * 100,

            2

        )

    # =====================================================
    # HORAS
    # =====================================================

    def total_estimated_hours(self):

        return sum(

            t.horas_estimadas

            for t in self.tasks

        )

    def total_real_hours(self):

        return sum(

            t.horas_reales

            for t in self.tasks

        )

    # =====================================================
    # COSTES
    # =====================================================

    def total_estimated_cost(self):

        return sum(

            t.coste_estimado

            for t in self.tasks

        )

    def total_real_cost(self):

        return sum(

            t.coste_real

            for t in self.tasks

        )

    # =====================================================
    # EXPORTACIÓN
    # =====================================================

    def export_excel(self):

        if self.excel is None:

            return

        self.excel.save_tasks(

            self.tasks

        )

    def import_excel(self):

        if self.excel is None:

            return

        self.tasks = self.excel.load_tasks()

        self.notify(

            "tasks_loaded"

        )

    # =====================================================
    # BACKUP
    # =====================================================

    def create_backup(self):

        if self.backup:

            self.backup.create(

                self.tasks

            )

    def restore_backup(self):

        if self.backup:

            self.tasks = self.backup.restore()

            self.notify(

                "backup_restored"

            )
            
    # =====================================================
    # UNDO
    # =====================================================

    def undo(self):

        if not self.undo_stack:

            return False

        self.redo_stack.append(

            copy.deepcopy(

                self.tasks

            )

        )

        self.tasks = self.undo_stack.pop()

        self.modified = True

        self.notify(

            "undo"

        )

        return True

    # =====================================================
    # REDO
    # =====================================================

    def redo(self):

        if not self.redo_stack:

            return False

        self.undo_stack.append(

            copy.deepcopy(

                self.tasks

            )

        )

        self.tasks = self.redo_stack.pop()

        self.modified = True

        self.notify(

            "redo"

        )

        return True

    # =====================================================
    # GUARDAR
    # =====================================================

    def save(self):

        if self.excel:

            self.excel.save_tasks(

                self.tasks

            )

        self.modified = False

        self.notify(

            "saved"

        )

    # =====================================================
    # AUTOGUARDADO
    # =====================================================

    def autosave(self):

        if not self.modified:

            return

        self.save()

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def update_metrics(self):

        if self.metrics is None:

            return

        self.metrics.update(

            self.tasks

        )

        self.notify(

            "metrics_updated"

        )

    # =====================================================
    # POWER BI
    # =====================================================

    def refresh_powerbi(self):

        if self.powerbi is None:

            return

        self.powerbi.refresh(

            self.tasks

        )

        self.notify(

            "powerbi_updated"

        )

    # =====================================================
    # INFORMES
    # =====================================================

    def generate_report(

        self,

        report_name,

        **kwargs

    ):

        if self.report is None:

            return None

        return self.report.generate(

            report_name,

            self.tasks,

            **kwargs

        )

    # =====================================================
    # LIMPIAR
    # =====================================================

    def clear(self):

        self.save_state()

        self.tasks.clear()

        self.projects.clear()

        self.categories.clear()

        self.owners.clear()

        self.modified = True

        self.notify(

            "cleared"

        )

    # =====================================================
    # RECARGAR
    # =====================================================

    def reload(

        self,

        tasks

    ):

        self.tasks = list(

            tasks

        )

        self.modified = False

        self.notify(

            "reloaded"

        )

    # =====================================================
    # VALIDAR
    # =====================================================

    def validate(self):

        errores = []

        ids = set()

        for task in self.tasks:

            errores.extend(

                task.validate()

            )

            if task.id in ids:

                errores.append(

                    f"ID duplicado: {task.id}"

                )

            ids.add(

                task.id

            )

        return errores

    # =====================================================
    # COMPACTAR IDS
    # =====================================================

    def normalize_ids(self):

        self.save_state()

        for indice, tarea in enumerate(

            self.tasks,

            start=1

        ):

            tarea.id = indice

        self.touch()

        self.notify(

            "ids_normalized"

        )

    # =====================================================
    # TAREAS DE HOY
    # =====================================================

    def tasks_today(self):

        hoy = datetime.now().strftime(

            "%d/%m/%Y"

        )

        return [

            t

            for t in self.tasks

            if t.fecha_prevista == hoy

        ]

    # =====================================================
    # TAREAS DE ESTA SEMANA
    # =====================================================

    def tasks_this_week(self):

        hoy = datetime.now()

        resultado = []

        for tarea in self.tasks:

            try:

                fecha = datetime.strptime(

                    tarea.fecha_prevista,

                    "%d/%m/%Y"

                )

            except Exception:

                continue

            if abs(

                (

                    fecha -

                    hoy

                ).days

            ) <= 7:

                resultado.append(

                    tarea

                )

        return resultado

    # =====================================================
    # TAREAS DE ESTE MES
    # =====================================================

    def tasks_this_month(self):

        hoy = datetime.now()

        return [

            t

            for t in self.tasks

            if t.fecha_prevista

            and datetime.strptime(

                t.fecha_prevista,

                "%d/%m/%Y"

            ).month == hoy.month

            and datetime.strptime(

                t.fecha_prevista,

                "%d/%m/%Y"

            ).year == hoy.year

        ]

    # =====================================================
    # CERRAR
    # =====================================================

    def shutdown(self):

        if self.modified:

            self.save()

        self.notify(

            "shutdown"

        )
        

        
        
        
        
        
        
        
