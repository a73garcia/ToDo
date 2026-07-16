"""
src/excel_manager.py
Gestión del archivo Excel de ToDo
"""

from pathlib import Path
from datetime import datetime

from openpyxl import Workbook, load_workbook

from config import EXCEL_FILE, EXCEL_COLUMNS


class ExcelManager:

    def __init__(self, excel_path: Path = EXCEL_FILE):
        self.excel_path = Path(excel_path)

    def create_if_not_exists(self):
        if self.excel_path.exists():
            return

        self.excel_path.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()

        ws = wb.active
        ws.title = "Tareas"

        for col, value in enumerate(EXCEL_COLUMNS, start=1):
            ws.cell(row=1, column=col).value = value

        historial = wb.create_sheet("Historial")
        historial.append([
            "Fecha",
            "ID",
            "Acción",
            "Usuario",
            "Observaciones"
        ])

        configuracion = wb.create_sheet("Configuración")
        configuracion["A1"] = "Creado"
        configuracion["B1"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        wb.save(self.excel_path)

    def workbook(self):
        self.create_if_not_exists()
        return load_workbook(self.excel_path)

    def save(self, workbook):
        workbook.save(self.excel_path)

    def next_id(self):
        wb = self.workbook()
        ws = wb["Tareas"]

        if ws.max_row <= 1:
            return 1

        ids = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is not None:
                ids.append(int(row[0]))

        return max(ids, default=0) + 1

    def add_task(self, data: dict):

        wb = self.workbook()
        ws = wb["Tareas"]

        row = [
            self.next_id(),
            data.get("Título", ""),
            data.get("Descripción", ""),
            data.get("Responsable", ""),
            data.get("Prioridad", "Media"),
            data.get("Estado", "Pendiente"),
            data.get("Fecha creación", datetime.now().strftime("%Y-%m-%d")),
            data.get("Fecha inicio", ""),
            data.get("Fecha prevista", ""),
            data.get("Fecha finalización", ""),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            data.get("Avance (%)", 0),
            data.get("Observaciones", "")
        ]

        ws.append(row)
        self.save(wb)
