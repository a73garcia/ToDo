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

    # ======================================================
    # BARRA DE HERRAMIENTAS
    # ======================================================

    def create_toolbar(self):

        self.toolbar = ttk.Frame(
            self,
            padding=5
        )

        self.toolbar.pack(
            fill="x",
            side="top"
        )

        ttk.Button(
            self.toolbar,
            text="➕ Nueva",
            command=self.new_task,
            width=12
        ).pack(side="left", padx=2)

        ttk.Button(
            self.toolbar,
            text="✏ Editar",
            command=self.edit_task,
            width=12
        ).pack(side="left", padx=2)

        ttk.Button(
            self.toolbar,
            text="🗑 Eliminar",
            command=self.delete_task,
            width=12
        ).pack(side="left", padx=2)

        ttk.Separator(
            self.toolbar,
            orient="vertical"
        ).pack(side="left", fill="y", padx=8)

        ttk.Label(
            self.toolbar,
            text="Buscar:"
        ).pack(side="left")

        self.search_entry = ttk.Entry(
            self.toolbar,
            textvariable=self.search_text,
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_tasks()
        )

        ttk.Separator(
            self.toolbar,
            orient="vertical"
        ).pack(side="left", fill="y", padx=8)

        ttk.Button(
            self.toolbar,
            text="🔄 Actualizar",
            command=self.refresh
        ).pack(side="left", padx=2)

        ttk.Button(
            self.toolbar,
            text="📊 Power BI",
            command=self.powerbi.refresh_all
        ).pack(side="left", padx=2)

        ttk.Button(
            self.toolbar,
            text="💾 Backup",
            command=self.backup.create_backup
        ).pack(side="left", padx=2)

    # ======================================================
    # BARRA DE ESTADO
    # ======================================================

    def create_statusbar(self):

        self.statusbar = ttk.Label(
            self,
            textvariable=self.status,
            anchor="w",
            relief="sunken"
        )

        self.statusbar.pack(
            side="bottom",
            fill="x"
        )

    # ======================================================
    # LAYOUT PRINCIPAL
    # ======================================================

    def create_main_layout(self):

        self.main = ttk.PanedWindow(
            self,
            orient="horizontal"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------

        self.left_panel = ttk.Frame(
            self.main,
            width=300
        )

        self.right_panel = ttk.Frame(
            self.main
        )

        self.main.add(
            self.left_panel,
            weight=1
        )

        self.main.add(
            self.right_panel,
            weight=5
        )

        self.create_left_panel()

        self.create_notebook()

    # ======================================================
    # PANEL IZQUIERDO
    # ======================================================

    def create_left_panel(self):

        ttk.Label(
            self.left_panel,
            text="Filtros",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10,5)
        )

        ttk.Button(
            self.left_panel,
            text="Todas",
            command=self.refresh
        ).pack(fill="x", padx=10, pady=2)

        ttk.Button(
            self.left_panel,
            text="Pendientes",
            command=lambda: self.filter_status("Pendiente")
        ).pack(fill="x", padx=10, pady=2)

        ttk.Button(
            self.left_panel,
            text="En curso",
            command=lambda: self.filter_status("En curso")
        ).pack(fill="x", padx=10, pady=2)

        ttk.Button(
            self.left_panel,
            text="Bloqueadas",
            command=lambda: self.filter_status("Bloqueada")
        ).pack(fill="x", padx=10, pady=2)

        ttk.Button(
            self.left_panel,
            text="Finalizadas",
            command=lambda: self.filter_status("Finalizada")
        ).pack(fill="x", padx=10, pady=2)

        ttk.Separator(
            self.left_panel
        ).pack(fill="x", padx=10, pady=10)

        ttk.Label(
            self.left_panel,
            text="Notificaciones",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=10
        )

        self.notification_list = tk.Listbox(
            self.left_panel,
            height=12
        )

        self.notification_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ======================================================
    # NOTEBOOK
    # ======================================================

    def create_notebook(self):

        self.notebook = ttk.Notebook(
            self.right_panel
        )

        self.notebook.pack(
            fill="both",
            expand=True
        )

        self.dashboard = DashboardPanel(
            self.notebook
        )

        self.calendar = CalendarPanel(
            self.notebook
        )

        self.kanban = KanbanPanel(
            self.notebook
        )

        self.gantt = GanttPanel(
            self.notebook
        )

        self.table_frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.dashboard,
            text="📊 Dashboard"
        )

        self.notebook.add(
            self.calendar,
            text="📅 Calendario"
        )

        self.notebook.add(
            self.kanban,
            text="📋 Kanban"
        )

        self.notebook.add(
            self.gantt,
            text="📈 Gantt"
        )

        self.notebook.add(
            self.table_frame,
            text="📄 Tareas"
        )

        self.create_task_table()










