from src.excel_manager import ExcelManager
from src.models import HistoryEntry


class HistoryManager:
    """Registra y consulta el historial almacenado en Excel."""

    def __init__(self, excel_manager=None):
        self.excel = excel_manager or ExcelManager()
        self.excel.create_if_not_exists()

    def add_entry(self, task_id, action, user="Sistema", observations=""):
        entry = HistoryEntry.create(task_id, action, user, observations)
        self.excel.append_history_row(entry.to_excel_row())
        return entry.to_dict()

    def get_history(self, task_id=None, limit=None):
        workbook = self.excel.workbook(read_only=True, data_only=True)
        worksheet = workbook[self.excel.HISTORY_SHEET]
        result = []

        for row in worksheet.iter_rows(min_row=2, max_col=5, values_only=True):
            if not row[0]:
                continue
            item = {
                "fecha": str(row[0]),
                "task_id": row[1],
                "accion": row[2] or "",
                "usuario": row[3] or "",
                "observaciones": row[4] or "",
            }
            if task_id is not None and int(item["task_id"]) != int(task_id):
                continue
            result.append(item)

        workbook.close()
        result.sort(key=lambda item: item["fecha"], reverse=True)

        if limit not in (None, ""):
            result = result[: int(limit)]
        return result
