"""
src/database.py
Capa de acceso a datos para ToDo.
"""

from models import Task
from excel_manager import ExcelManager


class TaskRepository:
    """Repositorio de tareas basado en Excel."""

    def __init__(self):
        self.excel = ExcelManager()
        self.excel.create_if_not_exists()

    def get_all(self):
        wb = self.excel.workbook()
        ws = wb["Tareas"]

        tasks = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:
                continue
            tasks.append(Task.from_excel_row(row))
        return tasks

    def get_by_id(self, task_id):
        for task in self.get_all():
            if task.id == task_id:
                return task
        return None

    def add(self, task: Task):
        self.excel.add_task({
            "Título": task.titulo,
            "Descripción": task.descripcion,
            "Responsable": task.responsable,
            "Prioridad": task.prioridad,
            "Estado": task.estado,
            "Fecha creación": task.fecha_creacion,
            "Fecha inicio": task.fecha_inicio,
            "Fecha prevista": task.fecha_prevista,
            "Fecha finalización": task.fecha_finalizacion,
            "Avance (%)": task.avance,
            "Observaciones": task.observaciones,
        })

    def exists(self, task_id):
        return self.get_by_id(task_id) is not None

    def count(self):
        return len(self.get_all())

    def search(self, text):
        text = text.lower()
        return [
            t for t in self.get_all()
            if text in t.titulo.lower()
            or text in t.descripcion.lower()
            or text in t.responsable.lower()
        ]


if __name__ == "__main__":
    repo = TaskRepository()
    print(f"Tareas almacenadas: {repo.count()}")
