"""
Task Planner Pro
excel_manager.py
Parte 3 de 4
Historial, eliminación, métricas y backups
"""

from datetime import datetime
import shutil

    # =====================================================
    # ELIMINAR TAREA
    # =====================================================

    def delete_task(self, task_id):

        wb = self.workbook()
        ws = wb[SHEET_TASKS]

        for row in range(2, ws.max_row + 1):
            if ws.cell(row, 1).value == task_id:
                ws.delete_rows(row)
                break

        self.save(wb)

    # =====================================================
    # AÑADIR HISTORIAL
    # =====================================================

    def add_history(self, task_id, usuario, avance, comentario):

        wb = self.workbook()
        ws = wb[SHEET_HISTORY]

        ws.append([
            task_id,
            datetime.now().strftime(DATETIME_FORMAT),
            usuario,
            avance,
            comentario
        ])

        self.save(wb)

    # =====================================================
    # BACKUP
    # =====================================================

    def backup(self):

        if not AUTO_BACKUP:
            return

        destino = BACKUP_DIR / (
            "Backup_" +
            datetime.now().strftime("%Y%m%d_%H%M%S") +
            ".xlsx"
        )

        shutil.copy2(self.file, destino)

    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    def statistics(self):

        tareas = self.load_tasks()

        datos = {
            "Pendiente": 0,
            "En curso": 0,
            "Bloqueada": 0,
            "Finalizada": 0,
            "Total": len(tareas)
        }

        for t in tareas:
            if t.estado in datos:
                datos[t.estado] += 1

        return datos

    # =====================================================
    # ACTUALIZAR MÉTRICAS POWER BI
    # =====================================================

    def update_metrics(self):

        wb = self.workbook()
        ws = wb["Metricas"]

        datos = self.statistics()

        total = datos["Total"]

        avance = 0

        if total:
            suma = sum(t.avance for t in self.load_tasks())
            avance = round(suma / total)

        ws.append([
            datetime.now().strftime(DATE_FORMAT),
            datos["Pendiente"],
            datos["En curso"],
            datos["Bloqueada"],
            datos["Finalizada"],
            0,
            total,
            avance
        ])

        self.save(wb)

    # =====================================================
    # REFRESCO COMPLETO
    # =====================================================

    def refresh(self):

        self.update_metrics()

        self.backup()
