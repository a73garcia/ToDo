"""
routes.py
Definición de rutas REST para la API de ToDo.
Versión inicial.
"""

from models import Task
from database import TaskRepository
from history_manager import HistoryManager


class Routes:

    def __init__(self):
        self.repo = TaskRepository()
        self.history = HistoryManager()

    def get_tasks(self):
        return [t.__dict__ for t in self.repo.get_all()]

    def get_task(self, task_id):
        task = self.repo.get_by_id(task_id)
        if task is None:
            return {"error": "Tarea no encontrada"}, 404
        return task.__dict__, 200

    def create_task(self, data):
        task = Task(
            titulo=data.get("titulo", ""),
            descripcion=data.get("descripcion", ""),
            responsable=data.get("responsable", ""),
            prioridad=data.get("prioridad", "Media"),
            estado=data.get("estado", "Pendiente"),
            fecha_prevista=data.get("fecha", ""),
            avance=int(data.get("avance", 0))
        )

        self.repo.add(task)
        self.history.add_entry(
            task_id=self.repo.count(),
            action="Creación",
            user="API",
            observations=task.titulo
        )

        return {"ok": True}, 201

    def update_task(self, task_id, data):
        # Implementación completa en una versión posterior.
        return {
            "warning": "Actualización pendiente de implementación",
            "task_id": task_id
        }, 501

    def delete_task(self, task_id):
        # Implementación completa en una versión posterior.
        return {
            "warning": "Eliminación pendiente de implementación",
            "task_id": task_id
        }, 501

    def get_history(self, task_id=None):
        return self.history.get_history(task_id), 200

    def get_dashboard(self):
        tasks = self.repo.get_all()

        dashboard = {
            "total": len(tasks),
            "pendientes": sum(t.estado == "Pendiente" for t in tasks),
            "en_curso": sum(t.estado == "En curso" for t in tasks),
            "bloqueadas": sum(t.estado == "Bloqueada" for t in tasks),
            "finalizadas": sum(t.estado == "Finalizada" for t in tasks),
            "canceladas": sum(t.estado == "Cancelada" for t in tasks),
        }

        return dashboard, 200


if __name__ == "__main__":
    api = Routes()
    print(api.get_dashboard())
