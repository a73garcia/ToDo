"""
statistics_service.py
Servicio de estadísticas para ToDo.
"""

from collections import Counter, defaultdict
from datetime import datetime

from src.database import TaskRepository


class StatisticsService:

    def __init__(self, repository=None):
        self.repo = repository or TaskRepository()

    def tasks(self):
        return self.repo.get_all()

    def by_status(self):
        c = Counter(t.estado for t in self.tasks())
        return dict(c)

    def by_priority(self):
        c = Counter(t.prioridad for t in self.tasks())
        return dict(c)

    def by_responsible(self):
        c = Counter(
            t.responsable for t in self.tasks() if t.responsable
        )
        return dict(c)

    def monthly_creation(self):
        months = defaultdict(int)

        for task in self.tasks():
            if not task.fecha_creacion:
                continue
            try:
                month = datetime.strptime(
                    task.fecha_creacion,
                    "%Y-%m-%d"
                ).strftime("%Y-%m")
                months[month] += 1
            except Exception:
                pass

        return dict(sorted(months.items()))

    def monthly_completion(self):
        months = defaultdict(int)

        for task in self.tasks():
            if not task.fecha_finalizacion:
                continue
            try:
                month = datetime.strptime(
                    task.fecha_finalizacion,
                    "%Y-%m-%d"
                ).strftime("%Y-%m")
                months[month] += 1
            except Exception:
                pass

        return dict(sorted(months.items()))

    def progress_distribution(self):
        ranges = {
            "0-25": 0,
            "26-50": 0,
            "51-75": 0,
            "76-99": 0,
            "100": 0,
        }

        for task in self.tasks():
            p = int(task.avance)

            if p == 100:
                ranges["100"] += 1
            elif p >= 76:
                ranges["76-99"] += 1
            elif p >= 51:
                ranges["51-75"] += 1
            elif p >= 26:
                ranges["26-50"] += 1
            else:
                ranges["0-25"] += 1

        return ranges

    def productivity(self):
        tasks = self.tasks()

        total = len(tasks)
        finished = sum(
            t.estado == "Finalizada"
            for t in tasks
        )

        avg = (
            round(
                sum(t.avance for t in tasks) / total,
                2
            )
            if total else 0
        )

        return {
            "total": total,
            "finalizadas": finished,
            "pendientes": total - finished,
            "avance_medio": avg,
            "porcentaje_finalizadas": round(
                finished * 100 / total,
                2
            ) if total else 0,
        }

    def dashboard_dataset(self):
        return {
            "status": self.by_status(),
            "priority": self.by_priority(),
            "responsible": self.by_responsible(),
            "created": self.monthly_creation(),
            "completed": self.monthly_completion(),
            "progress": self.progress_distribution(),
            "productivity": self.productivity(),
        }


if __name__ == "__main__":
    service = StatisticsService()
    print(service.dashboard_dataset())
