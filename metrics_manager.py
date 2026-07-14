"""
Task Planner Pro
metrics_manager.py
Gestión de métricas para Power BI
"""

from datetime import datetime
from collections import Counter


class MetricsManager:
    def __init__(self, excel_manager):
        self.excel = excel_manager

    def task_metrics(self):
        tareas = self.excel.load_tasks()

        estados = Counter(t.estado for t in tareas)

        total = len(tareas)
        avance = round(sum(t.avance for t in tareas) / total) if total else 0

        retrasadas = sum(
            1 for t in tareas
            if hasattr(t, "esta_retrasada") and t.esta_retrasada()
        )

        return {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "total": total,
            "pendientes": estados.get("Pendiente", 0),
            "en_curso": estados.get("En curso", 0),
            "bloqueadas": estados.get("Bloqueada", 0),
            "finalizadas": estados.get("Finalizada", 0),
            "retrasadas": retrasadas,
            "avance_global": avance,
        }

    def owners_metrics(self):
        tareas = self.excel.load_tasks()
        datos = {}

        for t in tareas:
            nombre = t.responsable or "Sin responsable"
            datos.setdefault(nombre, {"total": 0, "finalizadas": 0})
            datos[nombre]["total"] += 1
            if t.estado == "Finalizada":
                datos[nombre]["finalizadas"] += 1

        return datos

    def categories_metrics(self):
        tareas = self.excel.load_tasks()
        resultado = Counter(
            (t.categoria or "Sin categoría") for t in tareas
        )
        return dict(resultado)

    def build_snapshot(self):
        return {
            "general": self.task_metrics(),
            "responsables": self.owners_metrics(),
            "categorias": self.categories_metrics(),
        }
