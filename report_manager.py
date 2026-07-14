"""
Task Planner Pro
report_manager.py
Generación de informes y exportaciones
"""

import csv
from datetime import datetime
from openpyxl import Workbook


class ReportManager:

    def __init__(self, excel_manager):
        self.excel = excel_manager

    def export_csv(self, filename):
        tareas = self.excel.load_tasks()

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([
                "ID","Título","Responsable","Estado",
                "Prioridad","Avance","Creación","Prevista"
            ])

            for t in tareas:
                w.writerow([
                    t.id,
                    t.titulo,
                    t.responsable,
                    t.estado,
                    t.prioridad,
                    t.avance,
                    t.fecha_creacion,
                    t.fecha_prevista
                ])

    def export_excel(self, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Informe"

        ws.append([
            "ID","Título","Responsable","Estado",
            "Prioridad","Avance","Creación","Prevista"
        ])

        for t in self.excel.load_tasks():
            ws.append([
                t.id,
                t.titulo,
                t.responsable,
                t.estado,
                t.prioridad,
                t.avance,
                t.fecha_creacion,
                t.fecha_prevista
            ])

        wb.save(filename)

    def executive_summary(self):
        tareas = self.excel.load_tasks()
        total = len(tareas)
        fin = sum(1 for t in tareas if t.estado == "Finalizada")
        progreso = round(sum(t.avance for t in tareas) / total) if total else 0

        return {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "total_tareas": total,
            "finalizadas": fin,
            "avance_global": progreso
        }
