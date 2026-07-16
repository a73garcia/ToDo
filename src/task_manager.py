"""
src/task_manager.py
Lógica de negocio para la gestión de tareas.
"""

from datetime import datetime
from excel_manager import ExcelManager


class TaskManager:

    def __init__(self):
        self.db = ExcelManager()
        self.db.create_if_not_exists()

    def crear_tarea(
        self,
        titulo,
        descripcion="",
        responsable="",
        prioridad="Media",
        fecha_prevista="",
        observaciones=""
    ):

        datos = {
            "Título": titulo,
            "Descripción": descripcion,
            "Responsable": responsable,
            "Prioridad": prioridad,
            "Estado": "Pendiente",
            "Fecha creación": datetime.now().strftime("%Y-%m-%d"),
            "Fecha prevista": fecha_prevista,
            "Avance (%)": 0,
            "Observaciones": observaciones,
        }

        self.db.add_task(datos)

    def listar_tareas(self):
        wb = self.db.workbook()
        ws = wb["Tareas"]

        tareas = []

        for fila in ws.iter_rows(min_row=2, values_only=True):
            if fila[0] is None:
                continue

            tareas.append({
                "id": fila[0],
                "titulo": fila[1],
                "descripcion": fila[2],
                "responsable": fila[3],
                "prioridad": fila[4],
                "estado": fila[5],
                "fecha_creacion": fila[6],
                "fecha_inicio": fila[7],
                "fecha_prevista": fila[8],
                "fecha_fin": fila[9],
                "ultima_actualizacion": fila[10],
                "avance": fila[11],
                "observaciones": fila[12],
            })

        return tareas

    def buscar_por_id(self, tarea_id):
        for tarea in self.listar_tareas():
            if tarea["id"] == tarea_id:
                return tarea
        return None

    def estadisticas(self):
        tareas = self.listar_tareas()

        resumen = {
            "total": len(tareas),
            "pendientes": 0,
            "en_curso": 0,
            "bloqueadas": 0,
            "finalizadas": 0,
            "canceladas": 0,
        }

        for t in tareas:
            estado = t["estado"]

            if estado == "Pendiente":
                resumen["pendientes"] += 1
            elif estado == "En curso":
                resumen["en_curso"] += 1
            elif estado == "Bloqueada":
                resumen["bloqueadas"] += 1
            elif estado == "Finalizada":
                resumen["finalizadas"] += 1
            elif estado == "Cancelada":
                resumen["canceladas"] += 1

        return resumen


if __name__ == "__main__":
    gestor = TaskManager()
    print(gestor.estadisticas())
