from src.excel_manager import ExcelManager
from src.models import Task
from src.validators import validate_identifier, validate_task, validate_task_payload


class TaskRepository:
    """Repositorio CRUD basado en el libro Excel."""

    def __init__(self, excel_manager=None):
        self.excel = excel_manager or ExcelManager()
        self.excel.create_if_not_exists()
        self.excel.ensure_structure()

    def get_all(self):
        workbook = self.excel.workbook(read_only=True, data_only=True)
        worksheet = workbook[self.excel.TASKS_SHEET]
        tasks = []
        for row in worksheet.iter_rows(
            min_row=2,
            max_col=len(self.excel.TASK_COLUMNS),
            values_only=True,
        ):
            if row[0] in (None, ""):
                continue
            tasks.append(Task.from_excel_row(row))
        workbook.close()
        return tasks

    def get_by_id(self, task_id):
        task_id = validate_identifier(task_id)
        return next((task for task in self.get_all() if task.id == task_id), None)

    def add(self, task):
        if not isinstance(task, Task):
            task = Task.from_dict(task)
        validate_task(task)

        workbook = self.excel.workbook()
        worksheet = workbook[self.excel.TASKS_SHEET]
        task.id = self.excel.next_id(worksheet)
        task.touch()
        worksheet.append(task.to_excel_row())
        self.excel.save(workbook)
        workbook.close()
        return task

    def update(self, task_id, data):
        task_id = validate_identifier(task_id)
        payload = validate_task_payload(data, partial=True)

        workbook = self.excel.workbook()
        worksheet = workbook[self.excel.TASKS_SHEET]

        for row_number in range(2, worksheet.max_row + 1):
            if worksheet.cell(row_number, 1).value != task_id:
                continue

            current = Task.from_excel_row([
                worksheet.cell(row_number, column).value
                for column in range(1, 22)
            ])

            for key, value in payload.items():
                setattr(current, "fecha_prevista" if key == "fecha" else key, value)

            current.__post_init__()
            current.touch()
            validate_task(current)

            for column, value in enumerate(current.to_excel_row(), 1):
                worksheet.cell(row_number, column, value)

            self.excel.save(workbook)
            workbook.close()
            return current

        workbook.close()
        return None

    def replace(self, task_id, data):
        existing = self.get_by_id(task_id)
        if existing is None:
            return None
        task = data if isinstance(data, Task) else Task.from_dict(data)
        task.id = int(task_id)
        if not task.fecha_creacion:
            task.fecha_creacion = existing.fecha_creacion
        return self.update(task_id, task.to_dict())

    def delete(self, task_id):
        task_id = validate_identifier(task_id)
        workbook = self.excel.workbook()
        worksheet = workbook[self.excel.TASKS_SHEET]
        for row_number in range(2, worksheet.max_row + 1):
            if worksheet.cell(row_number, 1).value == task_id:
                worksheet.delete_rows(row_number)
                self.excel.save(workbook)
                workbook.close()
                return True
        workbook.close()
        return False

    def search(self, text):
        query = str(text or "").lower()
        result = []
        for task in self.get_all():
            searchable = " ".join([
                task.titulo,
                task.descripcion,
                task.responsable,
                task.estado,
                task.prioridad,
                task.proyecto,
                " ".join(task.etiquetas),
                " ".join(comment.text for comment in task.comentarios),
            ]).lower()
            if query in searchable:
                result.append(task)
        return result

    def filter(self, status=None, priority=None, responsible=None, project=None, tag=None, favorite=None):
        tasks = self.get_all()
        filters = {
            "estado": status,
            "prioridad": priority,
            "responsable": responsible,
            "proyecto": project,
            "favorito": favorite,
        }
        for attribute, value in filters.items():
            if value not in (None, ""):
                tasks = [task for task in tasks if getattr(task, attribute) == value]
        if tag:
            tasks = [task for task in tasks if tag in task.etiquetas]
        return tasks

    def get_by_date(self, iso_date):
        return [task for task in self.get_all() if task.fecha_prevista == iso_date]

    def get_by_month(self, year, month):
        prefix = f"{int(year):04d}-{int(month):02d}"
        return [task for task in self.get_all() if task.fecha_prevista.startswith(prefix)]

    def count(self):
        return len(self.get_all())
