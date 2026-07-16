"""
search_service.py
Servicio de búsqueda avanzada para ToDo.
"""

from src.database import TaskRepository


class SearchService:

    def __init__(self, repository=None):
        self.repo = repository or TaskRepository()

    def all(self):
        return self.repo.get_all()

    @staticmethod
    def _contains(value, text):
        return text in str(value or "").lower()

    def search(self, text):
        text = str(text or "").strip().lower()
        if not text:
            return [t.to_dict() for t in self.all()]

        result = []

        for task in self.all():
            if any([
                self._contains(task.titulo, text),
                self._contains(task.descripcion, text),
                self._contains(task.responsable, text),
                self._contains(task.estado, text),
                self._contains(task.prioridad, text),
                self._contains(task.observaciones, text),
                self._contains(task.fecha_prevista, text),
            ]):
                result.append(task.to_dict())

        return result

    def filter(
        self,
        status=None,
        priority=None,
        responsible=None,
        progress_min=None,
        progress_max=None,
    ):
        tasks = self.all()

        if status:
            tasks = [t for t in tasks if t.estado == status]

        if priority:
            tasks = [t for t in tasks if t.prioridad == priority]

        if responsible:
            responsible = responsible.lower()
            tasks = [
                t for t in tasks
                if t.responsable.lower() == responsible
            ]

        if progress_min is not None:
            tasks = [
                t for t in tasks
                if t.avance >= int(progress_min)
            ]

        if progress_max is not None:
            tasks = [
                t for t in tasks
                if t.avance <= int(progress_max)
            ]

        return [t.to_dict() for t in tasks]

    def sort(self, field="id", reverse=False):
        tasks = self.all()

        mapping = {
            "id": lambda t: t.id or 0,
            "titulo": lambda t: t.titulo.lower(),
            "responsable": lambda t: t.responsable.lower(),
            "estado": lambda t: t.estado,
            "prioridad": lambda t: t.prioridad,
            "fecha": lambda t: t.fecha_prevista or "9999-12-31",
            "avance": lambda t: t.avance,
        }

        key = mapping.get(field, mapping["id"])

        return [
            t.to_dict()
            for t in sorted(tasks, key=key, reverse=reverse)
        ]

    def statistics(self):
        tasks = self.all()

        return {
            "total": len(tasks),
            "con_fecha": sum(bool(t.fecha_prevista) for t in tasks),
            "sin_fecha": sum(not t.fecha_prevista for t in tasks),
            "responsables": len(
                {t.responsable for t in tasks if t.responsable}
            ),
            "estados": sorted({t.estado for t in tasks}),
            "prioridades": sorted({t.prioridad for t in tasks}),
        }


if __name__ == "__main__":
    service = SearchService()
    print(service.statistics())
