"""
notifications.py
Sistema de notificaciones para ToDo.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    level: str
    title: str
    message: str
    created: str


class NotificationManager:

    def __init__(self):
        self.notifications = []

    def add(self, level, title, message):
        n = Notification(
            level=level,
            title=title,
            message=message,
            created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.notifications.append(n)
        return n

    def info(self, title, message):
        return self.add("INFO", title, message)

    def warning(self, title, message):
        return self.add("WARNING", title, message)

    def error(self, title, message):
        return self.add("ERROR", title, message)

    def success(self, title, message):
        return self.add("SUCCESS", title, message)

    def list_all(self):
        return [n.__dict__ for n in self.notifications]

    def clear(self):
        self.notifications.clear()

    def check_due_tasks(self, tasks):
        today = datetime.now().strftime("%Y-%m-%d")

        for task in tasks:
            fecha = getattr(task, "fecha_prevista", "")

            if not fecha:
                continue

            if (
                fecha < today and
                getattr(task, "estado", "") != "Finalizada"
            ):
                self.warning(
                    "Tarea atrasada",
                    f"{task.titulo} debía finalizar el {fecha}"
                )


if __name__ == "__main__":
    manager = NotificationManager()
    manager.info("Inicio", "Aplicación iniciada correctamente")
    print(manager.list_all())
