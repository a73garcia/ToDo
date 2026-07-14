import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from config import (
    APP_NAME,
    APP_VERSION
)

from excel_manager import ExcelManager
from metrics_manager import MetricsManager
from powerbi_manager import PowerBIManager
from backup_manager import BackupManager
from report_manager import ReportManager
from notification_manager import NotificationManager

from dashboard_panel import DashboardPanel
from calendar_panel import CalendarPanel
from kanban_panel import KanbanPanel
from gantt_panel import GanttPanel

from dialogs import TaskDialog


class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        # ==================================================
        # VENTANA
        # ==================================================

        self.title(

            f"{APP_NAME} {APP_VERSION}"

        )

        self.geometry(

            "1700x950"

        )

        self.minsize(

            1400,

            850

        )

        # ==================================================
        # GESTORES
        # ==================================================

        self.excel = ExcelManager()

        self.metrics = MetricsManager(

            self.excel

        )

        self.powerbi = PowerBIManager(

            self.excel,

            self.metrics

        )

        self.backup = BackupManager(

            self.excel

        )

        self.report = ReportManager(

            self.excel,

            self.metrics

        )

        self.notifications = NotificationManager(

            self.excel

        )

        # ==================================================
        # DATOS
        # ==================================================

        self.tasks = []

        self.selected_task = None

        # ==================================================
        # VARIABLES
        # ==================================================

        self.status = tk.StringVar()

        self.status.set(

            "Inicializando..."

        )

        self.search_text = tk.StringVar()

        # ==================================================
        # CONSTRUCCIÓN
        # ==================================================

        self.create_menu()

        self.create_toolbar()

        self.create_statusbar()

        self.create_main_layout()

        self.load_tasks()

        self.refresh_dashboard()

        self.show_notifications()

    # ======================================================
    # CARGAR
    # ======================================================

    def load_tasks(self):

        self.tasks = self.excel.load_tasks()

    # ======================================================
    # ACTUALIZAR
    # ======================================================

    def refresh(self):

        self.load_tasks()

        self.refresh_dashboard()

        self.refresh_calendar()

        self.refresh_kanban()

        self.refresh_gantt()

        self.refresh_table()

        self.status.set(

            f"{len(self.tasks)} tareas cargadas"

        )

    # ======================================================
    # MENÚ
    # ======================================================

    def create_menu(self):

        self.menu = tk.Menu(

            self

        )

        self.config(

            menu=self.menu

        )

        self.file_menu = tk.Menu(

            self.menu,

            tearoff=False

        )

        self.menu.add_cascade(

            label="Archivo",

            menu=self.file_menu

        )

        self.file_menu.add_command(

            label="Nueva tarea",

            command=self.new_task

        )

        self.file_menu.add_separator()

        self.file_menu.add_command(

            label="Actualizar",

            command=self.refresh

        )

        self.file_menu.add_separator()

        self.file_menu.add_command(

            label="Salir",

            command=self.destroy

        )

        # ==============================================

        self.report_menu = tk.Menu(

            self.menu,

            tearoff=False

        )

        self.menu.add_cascade(

            label="Informes",

            menu=self.report_menu

        )

        self.report_menu.add_command(

            label="Excel",

            command=self.report.export_excel

        )

        self.report_menu.add_command(

            label="CSV",

            command=self.report.export_csv

        )

        self.report_menu.add_command(

            label="PDF",

            command=self.report.export_pdf

        )

        # ==============================================

        self.tools_menu = tk.Menu(

            self.menu,

            tearoff=False

        )

        self.menu.add_cascade(

            label="Herramientas",

            menu=self.tools_menu

        )

        self.tools_menu.add_command(

            label="Actualizar Power BI",

            command=self.powerbi.refresh_all

        )

        self.tools_menu.add_command(

            label="Crear Backup",

            command=self.backup.create_backup

        )
