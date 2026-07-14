"""
Task Planner Pro
excel_manager.py
Parte 4 de 4
Sincronización y utilidades finales
"""

    # =====================================================
    # ACTUALIZAR RESPONSABLES
    # =====================================================

    def update_owners(self):

        wb = self.workbook()
        ws = wb["Responsables"]

        while ws.max_row > 1:
            ws.delete_rows(2)

        responsables = sorted({
            t.responsable.strip()
            for t in self.load_tasks()
            if t.responsable.strip()
        })

        for r in responsables:
            ws.append([r, "", ""])

        self.save(wb)

    # =====================================================
    # ACTUALIZAR CATEGORÍAS
    # =====================================================

    def update_categories(self):

        wb = self.workbook()
        ws = wb["Categorias"]

        while ws.max_row > 1:
            ws.delete_rows(2)

        categorias = sorted({
            t.categoria.strip()
            for t in self.load_tasks()
            if t.categoria.strip()
        })

        for c in categorias:
            ws.append([c, "#5B9BD5"])

        self.save(wb)

    # =====================================================
    # SINCRONIZAR TODO
    # =====================================================

    def synchronize(self):

        self.update_owners()
        self.update_categories()
        self.update_metrics()

    # =====================================================
    # VALIDAR BASE DE DATOS
    # =====================================================

    def validate_database(self):

        wb = self.workbook()

        required = [
            SHEET_TASKS,
            SHEET_HISTORY,
            "Metricas",
            "Categorias",
            "Responsables",
            "Calendario",
            "Configuracion"
        ]

        for sheet in required:
            if sheet not in wb.sheetnames:
                raise ValueError(f"Falta la hoja: {sheet}")

        return True

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def database_info(self):

        tareas = len(self.load_tasks())

        return {
            "archivo": str(self.file),
            "tareas": tareas,
            "hojas": self.workbook().sheetnames
        }

    # =====================================================
    # MANTENIMIENTO
    # =====================================================

    def maintenance(self):

        self.validate_database()
        self.synchronize()
        self.backup()
