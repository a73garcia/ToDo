from datetime import date, datetime, timedelta

from src.backup_manager import BackupManager
from src.database import TaskRepository
from src.history_manager import HistoryManager
from src.models import Task
from src.validators import validate_comment_payload, validate_task_payload


class TaskManager:
    """Lógica de negocio de la aplicación."""

    def __init__(self, repository=None, history_manager=None, backup_manager=None):
        self.repo = repository or TaskRepository()
        self.history = history_manager or HistoryManager()
        self.backups = backup_manager or BackupManager()

    def list_tasks(self, search="", **filters):
        tasks = self.repo.search(search) if search else self.repo.filter(**filters)
        return [task.to_dict() for task in tasks]

    def get_task(self, task_id):
        task = self.repo.get_by_id(task_id)
        return task.to_dict() if task else None

    def create_task(self, data, user="API"):
        task = self.repo.add(Task.from_dict(validate_task_payload(data, partial=False)))
        self.history.add_entry(task.id, "Creación", user, task.titulo)
        return task.to_dict()

    def update_task(self, task_id, data, user="API", reason=""):
        task = self.repo.update(task_id, validate_task_payload(data, partial=True))
        if task:
            self.history.add_entry(task.id, "Actualización", user, reason or task.titulo)
        return task.to_dict() if task else None

    def replace_task(self, task_id, data, user="API"):
        task = self.repo.replace(task_id, validate_task_payload(data, partial=False))
        if task:
            self.history.add_entry(task.id, "Sustitución", user, task.titulo)
        return task.to_dict() if task else None

    def delete_task(self, task_id, user="API", create_backup=True):
        current = self.repo.get_by_id(task_id)
        if current is None:
            return False

        if create_backup:
            try:
                self.backups.create_backup()
            except Exception:
                pass

        deleted = self.repo.delete(task_id)
        if deleted:
            self.history.add_entry(task_id, "Eliminación", user, current.titulo)
        return deleted

    def list_comments(self, task_id):
        task = self.repo.get_by_id(task_id)
        return [comment.to_dict() for comment in task.comentarios] if task else None

    def add_comment(self, task_id, data, user="API"):
        payload = validate_comment_payload(data)
        task = self.repo.get_by_id(task_id)
        if task is None:
            return None

        comment = task.add_comment(payload["text"], payload["author"])
        self.repo.update(task_id, {
            "comentarios": [item.to_dict() for item in task.comentarios]
        })
        self.history.add_entry(task_id, "Comentario añadido", user, payload["text"][:250])
        return comment.to_dict()

    def delete_comment(self, task_id, index, user="API"):
        task = self.repo.get_by_id(task_id)
        if task is None or not task.remove_comment(int(index)):
            return False

        self.repo.update(task_id, {
            "comentarios": [item.to_dict() for item in task.comentarios]
        })
        self.history.add_entry(task_id, "Comentario eliminado", user, str(index))
        return True

    def add_tag(self, task_id, tag, user="API"):
        task = self.repo.get_by_id(task_id)
        if task is None or not task.add_tag(tag):
            return False
        self.repo.update(task_id, {"etiquetas": task.etiquetas})
        self.history.add_entry(task_id, "Etiqueta añadida", user, tag)
        return True

    def remove_tag(self, task_id, tag, user="API"):
        task = self.repo.get_by_id(task_id)
        if task is None or not task.remove_tag(tag):
            return False
        self.repo.update(task_id, {"etiquetas": task.etiquetas})
        self.history.add_entry(task_id, "Etiqueta eliminada", user, tag)
        return True

    def toggle_favorite(self, task_id, user="API"):
        task = self.repo.get_by_id(task_id)
        return self.update_task(task_id, {"favorito": not task.favorito}, user) if task else None

    def change_status(self, task_id, status, user="API"):
        return self.update_task(task_id, {"estado": status}, user, f"Estado: {status}")

    def change_progress(self, task_id, progress, user="API"):
        return self.update_task(task_id, {"avance": progress}, user, f"Avance: {progress}%")

    def move_task_to_date(self, task_id, target_date, user="API"):
        return self.update_task(task_id, {"fecha_prevista": target_date}, user, f"Fecha: {target_date}")

    def tasks_for_day(self, iso_date):
        return [task.to_dict() for task in self.repo.get_by_date(iso_date)]

    def tasks_for_month(self, year, month):
        return [task.to_dict() for task in self.repo.get_by_month(year, month)]

    def overdue_tasks(self):
        today = date.today().isoformat()
        return [
            task.to_dict()
            for task in self.repo.get_all()
            if task.fecha_prevista
            and task.fecha_prevista < today
            and task.estado not in ("Finalizada", "Cancelada")
        ]

    def upcoming_tasks(self, days=14):
        start = date.today()
        end = start + timedelta(days=int(days))
        result = []
        for task in self.repo.get_all():
            if not task.fecha_prevista or task.estado in ("Finalizada", "Cancelada"):
                continue
            due = datetime.strptime(task.fecha_prevista, "%Y-%m-%d").date()
            if start <= due <= end:
                result.append(task.to_dict())
        return sorted(result, key=lambda item: item["fecha_prevista"])

    def dashboard(self):
        tasks = self.repo.get_all()
        total = len(tasks)
        count = lambda state: sum(task.estado == state for task in tasks)
        return {
            "total": total,
            "pendientes": count("Pendiente"),
            "en_curso": count("En curso"),
            "bloqueadas": count("Bloqueada"),
            "finalizadas": count("Finalizada"),
            "canceladas": count("Cancelada"),
            "retrasadas": len(self.overdue_tasks()),
            "avance_medio": round(sum(task.avance for task in tasks) / total, 2) if total else 0,
        }

    def statistics_by_responsible(self):
        result = {}
        for task in self.repo.get_all():
            key = task.responsable or "Sin responsable"
            bucket = result.setdefault(key, {"total": 0, "finalizadas": 0, "avance_total": 0})
            bucket["total"] += 1
            bucket["finalizadas"] += task.estado == "Finalizada"
            bucket["avance_total"] += task.avance

        for bucket in result.values():
            bucket["avance_medio"] = round(bucket.pop("avance_total") / bucket["total"], 2)
        return result

    def get_history(self, task_id=None, limit=None):
        return self.history.get_history(task_id, limit)

    def create_backup(self):
        path = self.backups.create_backup()
        return str(path) if path else None
