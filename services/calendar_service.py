"""
calendar_service.py
Servicio de calendario para el proyecto ToDo.
"""

from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Optional

from src.database import TaskRepository


class CalendarService:
    """Agrupa y consulta tareas por fechas y periodos."""

    def __init__(self, repository=None):
        self.repo = repository or TaskRepository()

    def get_tasks(self):
        return self.repo.get_all()

    @staticmethod
    def _parse_date(value):
        if not value:
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        return datetime.strptime(
            str(value),
            "%Y-%m-%d"
        ).date()

    @staticmethod
    def _task_to_dict(task):
        return task.to_dict()

    def tasks_for_day(self, target_date):
        target = self._parse_date(target_date)

        return [
            self._task_to_dict(task)
            for task in self.get_tasks()
            if self._parse_date(task.fecha_prevista) == target
        ]

    def tasks_for_month(self, year: int, month: int):
        result = defaultdict(list)

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if not due:
                continue

            if due.year == int(year) and due.month == int(month):
                result[due.isoformat()].append(
                    self._task_to_dict(task)
                )

        return dict(sorted(result.items()))

    def tasks_for_week(self, reference_date=None):
        reference = self._parse_date(
            reference_date or date.today()
        )

        monday = reference - timedelta(
            days=reference.weekday()
        )
        sunday = monday + timedelta(days=6)

        result = defaultdict(list)

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if due and monday <= due <= sunday:
                result[due.isoformat()].append(
                    self._task_to_dict(task)
                )

        return {
            "start": monday.isoformat(),
            "end": sunday.isoformat(),
            "days": dict(sorted(result.items())),
        }

    def upcoming(self, days=7, include_today=True):
        today = date.today()
        start = today if include_today else today + timedelta(days=1)
        end = today + timedelta(days=int(days))

        tasks = []

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if (
                due
                and start <= due <= end
                and task.estado not in ("Finalizada", "Cancelada")
            ):
                tasks.append(task)

        tasks.sort(
            key=lambda item: (
                item.fecha_prevista,
                item.prioridad,
                item.id or 0,
            )
        )

        return [
            self._task_to_dict(task)
            for task in tasks
        ]

    def overdue(self):
        today = date.today()
        tasks = []

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if (
                due
                and due < today
                and task.estado not in ("Finalizada", "Cancelada")
            ):
                tasks.append(task)

        tasks.sort(
            key=lambda item: (
                item.fecha_prevista,
                item.id or 0,
            )
        )

        return [
            self._task_to_dict(task)
            for task in tasks
        ]

    def without_due_date(self):
        return [
            self._task_to_dict(task)
            for task in self.get_tasks()
            if not task.fecha_prevista
        ]

    def month_summary(self, year: int, month: int):
        tasks = []

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if due and due.year == year and due.month == month:
                tasks.append(task)

        return {
            "year": year,
            "month": month,
            "total": len(tasks),
            "pendientes": sum(
                task.estado == "Pendiente"
                for task in tasks
            ),
            "en_curso": sum(
                task.estado == "En curso"
                for task in tasks
            ),
            "bloqueadas": sum(
                task.estado == "Bloqueada"
                for task in tasks
            ),
            "finalizadas": sum(
                task.estado == "Finalizada"
                for task in tasks
            ),
            "canceladas": sum(
                task.estado == "Cancelada"
                for task in tasks
            ),
        }

    def calendar_events(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None
    ):
        events = []

        for task in self.get_tasks():
            due = self._parse_date(task.fecha_prevista)

            if not due:
                continue

            if year is not None and due.year != int(year):
                continue

            if month is not None and due.month != int(month):
                continue

            events.append({
                "id": task.id,
                "title": task.titulo,
                "date": due.isoformat(),
                "status": task.estado,
                "priority": task.prioridad,
                "responsible": task.responsable,
                "progress": task.avance,
            })

        return sorted(
            events,
            key=lambda item: (
                item["date"],
                item["id"] or 0,
            )
        )


if __name__ == "__main__":
    service = CalendarService()
    print(service.tasks_for_week())
