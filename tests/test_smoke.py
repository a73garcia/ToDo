from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.database import TaskRepository
from src.excel_manager import ExcelManager
from src.history_manager import HistoryManager
from src.task_manager import TaskManager


class TodoSmokeTest(unittest.TestCase):
    def test_complete_task_flow(self):
        with TemporaryDirectory() as directory:
            excel = ExcelManager(Path(directory) / "tareas.xlsx")
            repository = TaskRepository(excel)
            history = HistoryManager(excel)
            manager = TaskManager(repository, history)

            created = manager.create_task({
                "titulo": "Prueba automática",
                "prioridad": "Alta",
                "fecha_prevista": "2026-07-20",
                "etiquetas": ["test"],
            })

            self.assertEqual(created["id"], 1)

            comment = manager.add_comment(1, {
                "author": "Test",
                "text": "Comentario de prueba",
            })
            self.assertEqual(comment["author"], "Test")

            updated = manager.update_task(1, {"avance": 50})
            self.assertEqual(updated["avance"], 50)
            self.assertEqual(updated["estado"], "En curso")
            self.assertEqual(manager.dashboard()["total"], 1)

            self.assertTrue(
                manager.delete_task(1, create_backup=False)
            )
            self.assertEqual(manager.list_tasks(), [])


if __name__ == "__main__":
    unittest.main()
