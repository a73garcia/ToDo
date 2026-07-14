from collections import Counter
from datetime import datetime

from config import (
    STATUS_PENDING,
    STATUS_PROGRESS,
    STATUS_BLOCKED,
    STATUS_DONE,
)


class MetricsManager:

    def __init__(self, excel_manager):

        self.excel = excel_manager

    # =====================================================
    # TAREAS
    # =====================================================

    @property
    def tasks(self):

        return self.excel.load_tasks()

    # =====================================================
    # TOTAL
    # =====================================================

    def total_tasks(self):

        return len(self.tasks)

    # =====================================================
    # POR ESTADO
    # =====================================================

    def tasks_by_status(self):

        contador = Counter()

        for tarea in self.tasks:

            contador[tarea.estado] += 1

        return contador

    # =====================================================
    # POR PRIORIDAD
    # =====================================================

    def tasks_by_priority(self):

        contador = Counter()

        for tarea in self.tasks:

            contador[tarea.prioridad] += 1

        return contador

    # =====================================================
    # POR CATEGORÍA
    # =====================================================

    def tasks_by_category(self):

        contador = Counter()

        for tarea in self.tasks:

            if tarea.categoria:

                contador[tarea.categoria] += 1

        return contador

    # =====================================================
    # POR RESPONSABLE
    # =====================================================

    def tasks_by_owner(self):

        contador = Counter()

        for tarea in self.tasks:

            if tarea.responsable:

                contador[tarea.responsable] += 1

        return contador

    # =====================================================
    # RETRASADAS
    # =====================================================

    def delayed_tasks(self):

        return sum(

            1

            for tarea in self.tasks

            if tarea.esta_retrasada()

        )

    # =====================================================
    # FINALIZADAS
    # =====================================================

    def completed_tasks(self):

        return self.tasks_by_status().get(

            STATUS_DONE,

            0

        )

    # =====================================================
    # EN CURSO
    # =====================================================

    def active_tasks(self):

        datos = self.tasks_by_status()

        return (

            datos.get(STATUS_PENDING, 0)

            + datos.get(STATUS_PROGRESS, 0)

            + datos.get(STATUS_BLOCKED, 0)

        )

    # =====================================================
    # AVANCE GLOBAL
    # =====================================================

    def global_progress(self):

        tareas = self.tasks

        if not tareas:

            return 0

        return round(

            sum(

                t.avance

                for t in tareas

            )

            / len(tareas),

            1

        )

    # =====================================================
    # KPI
    # =====================================================

    def kpi(self):

        estados = self.tasks_by_status()

        return {

            "fecha": datetime.now(),

            "total": self.total_tasks(),

            "pendientes": estados.get(

                STATUS_PENDING,

                0

            ),

            "en_curso": estados.get(

                STATUS_PROGRESS,

                0

            ),

            "bloqueadas": estados.get(

                STATUS_BLOCKED,

                0

            ),

            "finalizadas": estados.get(

                STATUS_DONE,

                0

            ),

            "retrasadas": self.delayed_tasks(),

            "avance": self.global_progress()

        }
        
    # =====================================================
    # PRODUCTIVIDAD POR RESPONSABLE
    # =====================================================

    def owner_productivity(self):

        datos = {}

        for tarea in self.tasks:

            responsable = tarea.responsable or "Sin asignar"

            if responsable not in datos:

                datos[responsable] = {

                    "total": 0,

                    "finalizadas": 0,

                    "avance": 0

                }

            datos[responsable]["total"] += 1

            datos[responsable]["avance"] += tarea.avance

            if tarea.estado == STATUS_DONE:

                datos[responsable]["finalizadas"] += 1

        for responsable in datos:

            total = datos[responsable]["total"]

            if total:

                datos[responsable]["avance"] = round(

                    datos[responsable]["avance"] / total,

                    1

                )

        return datos

    # =====================================================
    # PRODUCTIVIDAD POR CATEGORÍA
    # =====================================================

    def category_productivity(self):

        datos = {}

        for tarea in self.tasks:

            categoria = tarea.categoria or "Sin categoría"

            if categoria not in datos:

                datos[categoria] = {

                    "total": 0,

                    "avance": 0

                }

            datos[categoria]["total"] += 1

            datos[categoria]["avance"] += tarea.avance

        for categoria in datos:

            total = datos[categoria]["total"]

            if total:

                datos[categoria]["avance"] = round(
                    datos[categoria]["avance"] / total,
                    1
                )

        return datos

    # =====================================================
    # RESUMEN PARA DASHBOARD
    # =====================================================

    def dashboard_data(self):

        return {

            "kpi": self.kpi(),

            "estado": dict(self.tasks_by_status()),

            "prioridad": dict(self.tasks_by_priority()),

            "categoria": dict(self.tasks_by_category()),

            "responsable": dict(self.tasks_by_owner()),

            "productividad": self.owner_productivity()

        }

    # =====================================================
    # DATOS PARA POWER BI
    # =====================================================

    def powerbi_dataset(self):

        filas = []

        for tarea in self.tasks:

            filas.append({

                "id": tarea.id,

                "titulo": tarea.titulo,

                "estado": tarea.estado,

                "prioridad": tarea.prioridad,

                "responsable": tarea.responsable,

                "categoria": tarea.categoria,

                "avance": tarea.avance,

                "fecha_inicio": tarea.fecha_inicio,

                "fecha_prevista": tarea.fecha_prevista,

                "retrasada": tarea.esta_retrasada()

            })

        return filas

    # =====================================================
    # RESUMEN EJECUTIVO
    # =====================================================

    def executive_summary(self):

        return {

            "fecha": datetime.now(),

            "total_tareas": self.total_tasks(),

            "tareas_activas": self.active_tasks(),

            "tareas_finalizadas": self.completed_tasks(),

            "tareas_retrasadas": self.delayed_tasks(),

            "avance_global": self.global_progress(),

            "responsables": len(self.tasks_by_owner()),

            "categorias": len(self.tasks_by_category())

        }

    # =====================================================
    # MÉTRICAS COMPLETAS
    # =====================================================

    def full_report(self):

        return {

            "kpi": self.kpi(),

            "dashboard": self.dashboard_data(),

            "powerbi": self.powerbi_dataset(),

            "owners": self.owner_productivity(),

            "categories": self.category_productivity(),

            "summary": self.executive_summary()

        }
        
        
        
