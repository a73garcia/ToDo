from src.task_manager import TaskManager


class Routes:
    """Adaptador entre el servidor HTTP y la lógica de negocio."""

    def __init__(self, task_manager=None):
        self.tasks = task_manager or TaskManager()

    def get_tasks(self, **query):
        return self.tasks.list_tasks(search=query.pop("search", ""), **query), 200

    def get_task(self, task_id):
        task = self.tasks.get_task(task_id)
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def create_task(self, data):
        return self.tasks.create_task(data), 201

    def update_task(self, task_id, data):
        task = self.tasks.update_task(task_id, data)
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def replace_task(self, task_id, data):
        task = self.tasks.replace_task(task_id, data)
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def delete_task(self, task_id):
        return ({"ok": True}, 200) if self.tasks.delete_task(task_id) else ({"error": "Tarea no encontrada."}, 404)

    def get_comments(self, task_id):
        comments = self.tasks.list_comments(task_id)
        return (comments, 200) if comments is not None else ({"error": "Tarea no encontrada."}, 404)

    def add_comment(self, task_id, data):
        comment = self.tasks.add_comment(task_id, data)
        return (comment, 201) if comment else ({"error": "Tarea no encontrada."}, 404)

    def delete_comment(self, task_id, index):
        return ({"ok": True}, 200) if self.tasks.delete_comment(task_id, index) else ({"error": "Comentario no encontrado."}, 404)

    def add_tag(self, task_id, data):
        tag = str(data.get("tag", "")).strip()
        if tag and self.tasks.add_tag(task_id, tag):
            return {"ok": True, "tag": tag}, 201
        return {"error": "No se pudo añadir la etiqueta."}, 400

    def remove_tag(self, task_id, tag):
        return ({"ok": True}, 200) if self.tasks.remove_tag(task_id, tag) else ({"error": "Etiqueta no encontrada."}, 404)

    def toggle_favorite(self, task_id):
        task = self.tasks.toggle_favorite(task_id)
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def change_status(self, task_id, data):
        task = self.tasks.change_status(task_id, data.get("estado"))
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def change_progress(self, task_id, data):
        task = self.tasks.change_progress(task_id, int(data.get("avance", 0)))
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def move_task(self, task_id, data):
        task = self.tasks.move_task_to_date(task_id, data.get("fecha_prevista", ""))
        return (task, 200) if task else ({"error": "Tarea no encontrada."}, 404)

    def get_dashboard(self):
        return self.tasks.dashboard(), 200

    def get_calendar(self, year=None, month=None, day=None):
        if day:
            return self.tasks.tasks_for_day(day), 200
        if year and month:
            return self.tasks.tasks_for_month(year, month), 200
        return self.tasks.list_tasks(), 200

    def get_upcoming(self, days=14):
        return self.tasks.upcoming_tasks(days), 200

    def get_overdue(self):
        return self.tasks.overdue_tasks(), 200

    def get_statistics_by_responsible(self):
        return self.tasks.statistics_by_responsible(), 200

    def get_history(self, task_id=None, limit=None):
        return self.tasks.get_history(task_id, limit), 200

    def create_backup(self):
        path = self.tasks.create_backup()
        return ({"ok": True, "backup": path}, 201) if path else ({"error": "No se pudo crear la copia."}, 500)
