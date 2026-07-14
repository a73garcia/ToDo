import csv
import json
from pathlib import Path
from datetime import datetime

from openpyxl import Workbook

from config import EXPORT_DIR


class PowerBIManager:

    def __init__(self, excel_manager, metrics_manager):

        self.excel = excel_manager

        self.metrics = metrics_manager

        self.export_folder = EXPORT_DIR

        self.export_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # RUTAS
    # =====================================================

    @property
    def csv_file(self):

        return self.export_folder / "powerbi_dataset.csv"

    @property
    def excel_file(self):

        return self.export_folder / "powerbi_dataset.xlsx"

    @property
    def json_file(self):

        return self.export_folder / "powerbi_dataset.json"

    # =====================================================
    # DATASET
    # =====================================================

    def dataset(self):

        return self.metrics.powerbi_dataset()

    # =====================================================
    # EXPORTAR CSV
    # =====================================================

    def export_csv(self):

        datos = self.dataset()

        if not datos:

            return self.csv_file

        with open(

            self.csv_file,

            "w",

            newline="",

            encoding="utf-8-sig"

        ) as fichero:

            writer = csv.DictWriter(

                fichero,

                fieldnames=datos[0].keys()

            )

            writer.writeheader()

            writer.writerows(datos)

        return self.csv_file

    # =====================================================
    # EXPORTAR JSON
    # =====================================================

    def export_json(self):

        with open(

            self.json_file,

            "w",

            encoding="utf-8"

        ) as fichero:

            json.dump(

                self.dataset(),

                fichero,

                indent=4,

                ensure_ascii=False

            )

        return self.json_file

    # =====================================================
    # EXPORTAR EXCEL
    # =====================================================

    def export_excel(self):

        wb = Workbook()

        ws = wb.active

        ws.title = "PowerBI"

        datos = self.dataset()

        if datos:

            ws.append(

                list(datos[0].keys())

            )

            for fila in datos:

                ws.append(

                    list(fila.values())

                )

        wb.save(

            self.excel_file

        )

        return self.excel_file

    # =====================================================
    # KPI
    # =====================================================

    def export_kpi(self):

        return self.metrics.kpi()

    # =====================================================
    # REFRESCO COMPLETO
    # =====================================================

    def refresh_all(self):

        """
        Actualiza todas las métricas y exporta todos los
        datasets para Power BI.
        """

        self.excel.refresh()

        self.export_csv()

        self.export_excel()

        self.export_json()

        return True

    # =====================================================
    # SNAPSHOT
    # =====================================================

    def snapshot(self):

        return {

            "fecha": datetime.now(),

            "dataset": len(self.dataset()),

            "csv": str(self.csv_file),

            "excel": str(self.excel_file),

            "json": str(self.json_file),

            "kpi": self.metrics.kpi()

        }

    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(self):

        return self.metrics.dashboard_data()

    # =====================================================
    # INFORME EJECUTIVO
    # =====================================================

    def executive_report(self):

        return self.metrics.executive_summary()

    # =====================================================
    # EXPORTAR DASHBOARD
    # =====================================================

    def export_dashboard(self):

        datos = self.dashboard()

        fichero = self.export_folder / "dashboard.json"

        with open(

            fichero,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                datos,

                f,

                indent=4,

                ensure_ascii=False

            )

        return fichero

    # =====================================================
    # EXPORTAR RESUMEN EJECUTIVO
    # =====================================================

    def export_summary(self):

        fichero = self.export_folder / "summary.json"

        with open(

            fichero,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.executive_report(),

                f,

                indent=4,

                ensure_ascii=False,

                default=str

            )

        return fichero

    # =====================================================
    # EXPORTAR TODO
    # =====================================================

    def export_all(self):

        return {

            "csv": self.export_csv(),

            "excel": self.export_excel(),

            "json": self.export_json(),

            "dashboard": self.export_dashboard(),

            "summary": self.export_summary()

        }

    # =====================================================
    # ÚLTIMA EXPORTACIÓN
    # =====================================================

    def last_export(self):

        if not self.csv_file.exists():

            return None

        return datetime.fromtimestamp(

            self.csv_file.stat().st_mtime

        )

    # =====================================================
    # ESTADO
    # =====================================================

    def status(self):

        return {

            "dataset": len(

                self.dataset()

            ),

            "ultima_exportacion":

                self.last_export(),

            "carpeta":

                str(self.export_folder),

            "csv":

                self.csv_file.exists(),

            "excel":

                self.excel_file.exists(),

            "json":

                self.json_file.exists()

        }

    # =====================================================
    # VALIDACIÓN
    # =====================================================

    def validate(self):

        datos = self.dataset()

        if not datos:

            return False

        campos = {

            "id",

            "titulo",

            "estado",

            "prioridad",

            "responsable",

            "categoria",

            "avance"

        }

        return campos.issubset(

            datos[0].keys()

        )

    # =====================================================
    # LIMPIAR EXPORTACIONES
    # =====================================================

    def clean(self):

        for fichero in (

            self.csv_file,

            self.excel_file,

            self.json_file,

            self.export_folder / "dashboard.json",

            self.export_folder / "summary.json"

        ):

            if fichero.exists():

                fichero.unlink()

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def info(self):

        return {

            "manager": "PowerBIManager",

            "version": "2.0",

            "dataset": len(

                self.dataset()

            ),

            "estado": self.status()

        }


