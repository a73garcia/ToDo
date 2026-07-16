"""
dashboard_service.py
Servicio del Dashboard - Parte 1
"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta

from src.database import TaskRepository


class DashboardService:
    def __init__(self):
        self.repo = TaskRepository()

    def get_tasks(self):
        return self.repo.get_all()

    def total_tasks(self):
        return len(self.get_tasks())

    def count_by_status(self):
        c = Counter()
        for t in self.get_tasks():
            c[t.estado] += 1
        return dict(c)

    def count_by_priority(self):
        c = Counter()
        for t in self.get_tasks():
            c[t.prioridad] += 1
        return dict(c)

    def average_progress(self):
        tasks = self.get_tasks()
        if not tasks:
            return 0
        return round(sum(t.avance for t in tasks) / len(tasks), 2)

    def completed_percentage(self):
        total = self.total_tasks()
        if total == 0:
            return 0
        return round(
            self.count_by_status().get("Finalizada", 0) * 100 / total,
            2,
        )

    def overdue_tasks(self):
        today = datetime.today().strftime("%Y-%m-%d")
        result = []
        for t in self.get_tasks():
            if (
                t.fecha_prevista
                and t.fecha_prevista < today
                and t.estado not in ("Finalizada", "Cancelada")
            ):
                result.append(t)
        return result

    def upcoming_tasks(self, days=7):
        today = datetime.today()
        limit = today + timedelta(days=days)
        result = []
        for t in self.get_tasks():
            if not t.fecha_prevista:
                continue
            try:
                due = datetime.strptime(t.fecha_prevista, "%Y-%m-%d")
            except Exception:
                continue
            if today <= due <= limit:
                result.append(t)
        return sorted(result, key=lambda x: x.fecha_prevista)

    def tasks_by_user(self):
        users = defaultdict(int)
        for t in self.get_tasks():
            if t.responsable:
                users[t.responsable] += 1
        return dict(users)

    def workload(self):
        total = max(self.total_tasks(), 1)
        return {
            user: {
                "total": qty,
                "percentage": round(qty * 100 / total, 2),
            }
            for user, qty in self.tasks_by_user().items()
        }


if __name__ == "__main__":
    service = DashboardService()
    print(service.total_tasks())
