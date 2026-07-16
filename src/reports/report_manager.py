"""
report_manager.py
Generación de informes para ToDo.
"""

from datetime import datetime
import csv
from openpyxl import Workbook


class ReportManager:

    def export_csv(self, tasks, filename):
        headers = [
            "ID", "Título", "Responsable", "Prioridad",
            "Estado", "Fecha prevista", "Avance"
        ]

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for t in tasks:
                writer.writerow([
                    getattr(t, "id", ""),
                    getattr(t, "titulo", ""),
                    getattr(t, "responsable", ""),
                    getattr(t, "prioridad", ""),
                    getattr(t, "estado", ""),
                    getattr(t, "fecha_prevista", ""),
                    getattr(t, "avance", 0)
                ])

        return filename

    def export_excel(self, tasks, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Tareas"

        ws.append([
            "ID", "Título", "Responsable",
            "Prioridad", "Estado",
            "Fecha prevista", "Avance"
        ])

        for t in tasks:
            ws.append([
                getattr(t, "id", ""),
                getattr(t, "titulo", ""),
                getattr(t, "responsable", ""),
                getattr(t, "prioridad", ""),
                getattr(t, "estado", ""),
                getattr(t, "fecha_prevista", ""),
                getattr(t, "avance", 0)
            ])

        wb.save(filename)
        return filename

    def summary(self, tasks):
        total = len(tasks)

        return {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "pendientes": sum(getattr(t, "estado", "") == "Pendiente" for t in tasks),
            "en_curso": sum(getattr(t, "estado", "") == "En curso" for t in tasks),
            "bloqueadas": sum(getattr(t, "estado", "") == "Bloqueada" for t in tasks),
            "finalizadas": sum(getattr(t, "estado", "") == "Finalizada" for t in tasks),
            "canceladas": sum(getattr(t, "estado", "") == "Cancelada" for t in tasks),
            "avance_medio": round(
                sum(getattr(t, "avance", 0) for t in tasks) / total, 2
            ) if total else 0
        }


if __name__ == "__main__":
    print("ReportManager listo.")
