from __future__ import annotations

import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

from dashboard_panel import DashboardPanel
from calendar_panel import CalendarPanel
from kanban_panel import KanbanPanel
from gantt_panel import GanttPanel

from dialogs import TaskDialog

from task_manager import TaskManager

from excel_manager import ExcelManager
from metrics_manager import MetricsManager
from backup_manager import BackupManager
from report_manager import ReportManager


class MainWindow(tk.Tk):

    APP_NAME = "Task Planner Pro"

    VERSION = "3.0"

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self):

        super().__init__()

        self.title(

            f"{self.APP_NAME} {self.VERSION}"

        )

        self.geometry(

            "1700x950"

        )

        self.minsize(

            1400,

            800

        )

        self.protocol(

            "WM_DELETE_WINDOW",

            self.close

        )

        # ---------------------------------------------
        # Managers
        # ---------------------------------------------

        self.excel = ExcelManager()

        self.metrics = MetricsManager()

        self.backup = BackupManager()

        self.report = ReportManager()

        self.task_manager = TaskManager(

            excel_manager=self.excel,

            metrics_manager=self.metrics,

            backup_manager=self.backup,

            report_manager=self.report

        )

        self.task_manager.add_listener(

            self.on_manager_event

        )

        # ---------------------------------------------
        # Variables
        # ---------------------------------------------

        self.current_task = None

        self.current_project = None

        self.modified = False

        # ---------------------------------------------
        # UI
        # ---------------------------------------------

        self.create_style()

        self.create_layout()

        self.create_menu()

        self.create_toolbar()

        self.create_sidebar()

        self.create_notebook()

        self.create_statusbar()

        self.register_callbacks()

        self.load_data()

        self.after(

            300000,

            self.autosave

        )
        
    # =====================================================
    # ESTILOS
    # =====================================================

    def create_style(self):

        self.style = ttk.Style(self)

        try:

            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold")
        )

        self.style.configure(
            "Header.TLabel",
            font=("Segoe UI", 11, "bold")
        )

        self.style.configure(
            "Sidebar.TFrame",
            background="#F5F5F5"
        )

        self.style.configure(
            "Ribbon.TFrame",
            background="#ECECEC"
        )

        self.style.configure(
            "Status.TLabel",
            padding=4
        )

    # =====================================================
    # LAYOUT PRINCIPAL
    # =====================================================

    def create_layout(self):

        self.columnconfigure(1, weight=1)

        self.rowconfigure(2, weight=1)

    # =====================================================
    # MENÚ
    # =====================================================

    def create_menu(self):

        self.menu = tk.Menu(self)

        # ----------------------------------------
        # Archivo
        # ----------------------------------------

        archivo = tk.Menu(

            self.menu,

            tearoff=False

        )

        archivo.add_command(

            label="Nueva tarea",

            command=self.new_task

        )

        archivo.add_command(

            label="Abrir"

        )

        archivo.add_separator()

        archivo.add_command(

            label="Guardar",

            command=self.save

        )

        archivo.add_command(

            label="Guardar como..."

        )

        archivo.add_separator()

        archivo.add_command(

            label="Importar Excel",

            command=self.import_excel

        )

        archivo.add_command(

            label="Exportar Excel",

            command=self.export_excel

        )

        archivo.add_separator()

        archivo.add_command(

            label="Salir",

            command=self.close

        )

        self.menu.add_cascade(

            label="Archivo",

            menu=archivo

        )

        # ----------------------------------------
        # Editar
        # ----------------------------------------

        editar = tk.Menu(

            self.menu,

            tearoff=False

        )

        editar.add_command(

            label="Deshacer",

            command=self.undo

        )

        editar.add_command(

            label="Rehacer",

            command=self.redo

        )

        editar.add_separator()

        editar.add_command(

            label="Buscar",

            command=self.search

        )

        self.menu.add_cascade(

            label="Editar",

            menu=editar

        )

        # ----------------------------------------
        # Ver
        # ----------------------------------------

        ver = tk.Menu(

            self.menu,

            tearoff=False

        )

        ver.add_command(

            label="Dashboard",

            command=lambda:
            self.show_tab(0)

        )

        ver.add_command(

            label="Calendario",

            command=lambda:
            self.show_tab(1)

        )

        ver.add_command(

            label="Kanban",

            command=lambda:
            self.show_tab(2)

        )

        ver.add_command(

            label="Gantt",

            command=lambda:
            self.show_tab(3)

        )

        self.menu.add_cascade(

            label="Ver",

            menu=ver

        )

        # ----------------------------------------
        # Ayuda
        # ----------------------------------------

        ayuda = tk.Menu(

            self.menu,

            tearoff=False

        )

        ayuda.add_command(

            label="Acerca de...",

            command=self.about

        )

        self.menu.add_cascade(

            label="Ayuda",

            menu=ayuda

        )

        self.configure(

            menu=self.menu

        )

    # =====================================================
    # TOOLBAR
    # =====================================================

    def create_toolbar(self):

        self.toolbar = ttk.Frame(

            self,

            style="Ribbon.TFrame"

        )

        self.toolbar.grid(

            row=0,

            column=0,

            columnspan=2,

            sticky="ew"

        )

        ttk.Button(

            self.toolbar,

            text="Nueva",

            command=self.new_task

        ).pack(

            side="left",

            padx=4,

            pady=5

        )

        ttk.Button(

            self.toolbar,

            text="Editar",

            command=self.edit_task

        ).pack(

            side="left",

            padx=4

        )

        ttk.Button(

            self.toolbar,

            text="Eliminar",

            command=self.delete_task

        ).pack(

            side="left",

            padx=4

        )

        ttk.Separator(

            self.toolbar,

            orient="vertical"

        ).pack(

            side="left",

            fill="y",

            padx=8

        )

        ttk.Button(

            self.toolbar,

            text="Guardar",

            command=self.save

        ).pack(

            side="left",

            padx=4

        )

        ttk.Button(

            self.toolbar,

            text="Actualizar",

            command=self.refresh_all

        ).pack(

            side="left",

            padx=4

        )

        ttk.Separator(

            self.toolbar,

            orient="vertical"

        ).pack(

            side="left",

            fill="y",

            padx=8

        )

        ttk.Button(

            self.toolbar,

            text="Undo",

            command=self.undo

        ).pack(

            side="left",

            padx=4

        )

        ttk.Button(

            self.toolbar,

            text="Redo",

            command=self.redo

        ).pack(

            side="left",

            padx=4

        )

        ttk.Separator(

            self.toolbar,

            orient="vertical"

        ).pack(

            side="left",

            fill="y",

            padx=8

        )

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(

            self.toolbar,

            width=35,

            textvariable=self.search_var

        )

        self.search_entry.pack(

            side="right",

            padx=8

        )

        self.search_entry.bind(

            "<KeyRelease>",

            self.search_changed

        )

        ttk.Label(

            self.toolbar,

            text="Buscar:"

        ).pack(

            side="right"
        )
        
    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ttk.Frame(

            self,

            style="Sidebar.TFrame",

            width=220

        )

        self.sidebar.grid(

            row=1,

            column=0,

            rowspan=2,

            sticky="ns"

        )

        self.sidebar.grid_propagate(False)

        ttk.Label(

            self.sidebar,

            text="Navegación",

            style="Header.TLabel"

        ).pack(

            anchor="w",

            padx=10,

            pady=(10, 15)

        )

        self.btn_dashboard = ttk.Button(

            self.sidebar,

            text="📊 Dashboard",

            command=lambda:

                self.show_tab(0)

        )

        self.btn_dashboard.pack(

            fill="x",

            padx=10,

            pady=2

        )

        self.btn_calendar = ttk.Button(

            self.sidebar,

            text="📅 Calendario",

            command=lambda:

                self.show_tab(1)

        )

        self.btn_calendar.pack(

            fill="x",

            padx=10,

            pady=2

        )

        self.btn_kanban = ttk.Button(

            self.sidebar,

            text="📋 Kanban",

            command=lambda:

                self.show_tab(2)

        )

        self.btn_kanban.pack(

            fill="x",

            padx=10,

            pady=2

        )

        self.btn_gantt = ttk.Button(

            self.sidebar,

            text="📈 Gantt",

            command=lambda:

                self.show_tab(3)

        )

        self.btn_gantt.pack(

            fill="x",

            padx=10,

            pady=2

        )

        self.btn_reports = ttk.Button(

            self.sidebar,

            text="📄 Informes",

            command=lambda:

                self.show_tab(4)

        )

        self.btn_reports.pack(

            fill="x",

            padx=10,

            pady=2

        )

        self.btn_powerbi = ttk.Button(

            self.sidebar,

            text="📊 Power BI",

            command=lambda:

                self.show_tab(5)

        )

        self.btn_powerbi.pack(

            fill="x",

            padx=10,

            pady=2

        )

        ttk.Separator(

            self.sidebar,

            orient="horizontal"

        ).pack(

            fill="x",

            padx=10,

            pady=15

        )

        ttk.Label(

            self.sidebar,

            text="Acciones",

            style="Header.TLabel"

        ).pack(

            anchor="w",

            padx=10,

            pady=(0,10)

        )

        ttk.Button(

            self.sidebar,

            text="➕ Nueva tarea",

            command=self.new_task

        ).pack(

            fill="x",

            padx=10,

            pady=2

        )

        ttk.Button(

            self.sidebar,

            text="💾 Guardar",

            command=self.save

        ).pack(

            fill="x",

            padx=10,

            pady=2

        )

        ttk.Button(

            self.sidebar,

            text="🔄 Actualizar",

            command=self.refresh_all

        ).pack(

            fill="x",

            padx=10,

            pady=2

        )

        ttk.Button(

            self.sidebar,

            text="📦 Backup",

            command=self.create_backup

        ).pack(

            fill="x",

            padx=10,

            pady=2

        )

        ttk.Separator(

            self.sidebar,

            orient="horizontal"

        ).pack(

            fill="x",

            padx=10,

            pady=15

        )

        self.lbl_total_tasks = ttk.Label(

            self.sidebar,

            text="Tareas: 0"

        )

        self.lbl_total_tasks.pack(

            anchor="w",

            padx=10,

            pady=2

        )

        self.lbl_pending = ttk.Label(

            self.sidebar,

            text="Pendientes: 0"

        )

        self.lbl_pending.pack(

            anchor="w",

            padx=10,

            pady=2

        )

        self.lbl_progress = ttk.Label(

            self.sidebar,

            text="En curso: 0"

        )

        self.lbl_progress.pack(

            anchor="w",

            padx=10,

            pady=2

        )

        self.lbl_done = ttk.Label(

            self.sidebar,

            text="Finalizadas: 0"

        )

        self.lbl_done.pack(

            anchor="w",

            padx=10,

            pady=2

        )

        self.lbl_overdue = ttk.Label(

            self.sidebar,

            text="Retrasadas: 0"

        )

        self.lbl_overdue.pack(

            anchor="w",

            padx=10,

            pady=2

        )

    # =====================================================
    # NOTEBOOK
    # =====================================================

    def create_notebook(self):

        self.notebook = ttk.Notebook(

            self

        )

        self.notebook.grid(

            row=1,

            column=1,

            sticky="nsew"

        )

        self.dashboard_panel = DashboardPanel(

            self.notebook

        )

        self.calendar_panel = CalendarPanel(

            self.notebook

        )

        self.kanban_panel = KanbanPanel(

            self.notebook

        )

        self.gantt_panel = GanttPanel(

            self.notebook

        )

        self.reports_frame = ttk.Frame(

            self.notebook

        )

        self.powerbi_frame = ttk.Frame(

            self.notebook

        )

        self.notebook.add(

            self.dashboard_panel,

            text="Dashboard"

        )

        self.notebook.add(

            self.calendar_panel,

            text="Calendario"

        )

        self.notebook.add(

            self.kanban_panel,

            text="Kanban"

        )

        self.notebook.add(

            self.gantt_panel,

            text="Gantt"

        )

        self.notebook.add(

            self.reports_frame,

            text="Informes"

        )

        self.notebook.add(

            self.powerbi_frame,

            text="Power BI"

        )

        self.notebook.bind(

            "<<NotebookTabChanged>>",

            self.tab_changed

        )
        
        
    # =====================================================
    # STATUS BAR
    # =====================================================

    def create_statusbar(self):

        self.statusbar = ttk.Frame(self)

        self.statusbar.grid(

            row=2,

            column=1,

            sticky="ew"

        )

        self.status_message = tk.StringVar(

            value="Listo"

        )

        self.lbl_status = ttk.Label(

            self.statusbar,

            textvariable=self.status_message,

            style="Status.TLabel"

        )

        self.lbl_status.pack(

            side="left",

            padx=8

        )

        ttk.Separator(

            self.statusbar,

            orient="vertical"

        ).pack(

            side="left",

            fill="y",

            padx=8

        )

        self.lbl_tasks = ttk.Label(

            self.statusbar,

            text="0 tareas"

        )

        self.lbl_tasks.pack(

            side="left",

            padx=6

        )

        self.lbl_modified = ttk.Label(

            self.statusbar,

            text=""

        )

        self.lbl_modified.pack(

            side="left",

            padx=10

        )

        self.lbl_clock = ttk.Label(

            self.statusbar,

            text=""

        )

        self.lbl_clock.pack(

            side="right",

            padx=10

        )

        self.update_clock()

    # =====================================================
    # RELOJ
    # =====================================================

    def update_clock(self):

        self.lbl_clock.configure(

            text=datetime.now().strftime(

                "%d/%m/%Y %H:%M:%S"

            )

        )

        self.after(

            1000,

            self.update_clock

        )

    # =====================================================
    # CALLBACKS
    # =====================================================

    def register_callbacks(self):

        self.calendar_panel.set_task_open_callback(

            self.edit_task_by_id

        )

        self.kanban_panel.set_task_open_callback(

            self.edit_task_by_id

        )

        self.gantt_panel.set_task_open_callback(

            self.edit_task_by_id

        )

        self.calendar_panel.set_task_change_callback(

            self.task_changed

        )

        self.kanban_panel.set_task_change_callback(

            self.task_changed

        )

        self.gantt_panel.set_task_change_callback(

            self.task_changed

        )

    # =====================================================
    # EVENTOS DEL MANAGER
    # =====================================================

    def on_manager_event(

        self,

        event,

        task=None

    ):

        self.modified = self.task_manager.modified

        self.refresh_statistics()

        self.refresh_all()

        self.status_message.set(

            event.replace(

                "_",

                " "

            ).capitalize()

        )

        if self.modified:

            self.lbl_modified.configure(

                text="● Modificado"

            )

        else:

            self.lbl_modified.configure(

                text=""

            )

    # =====================================================
    # CARGA INICIAL
    # =====================================================

    def load_data(self):

        try:

            self.task_manager.import_excel()

        except Exception:

            pass

        self.refresh_all()

    # =====================================================
    # REFRESCAR TODO
    # =====================================================

    def refresh_all(self):

        tareas = self.task_manager.all_tasks()

        self.dashboard_panel.reload(

            tareas

        )

        self.calendar_panel.reload(

            tareas

        )

        self.kanban_panel.reload(

            tareas

        )

        self.gantt_panel.reload(

            tareas

        )

        self.refresh_statistics()

    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    def refresh_statistics(self):

        stats = self.task_manager.statistics()

        self.lbl_total_tasks.configure(

            text=f"Tareas: {stats['total']}"

        )

        self.lbl_pending.configure(

            text=f"Pendientes: {stats['pending']}"

        )

        self.lbl_progress.configure(

            text=f"En curso: {stats['progress']}"

        )

        self.lbl_done.configure(

            text=f"Finalizadas: {stats['completed']}"

        )

        self.lbl_overdue.configure(

            text=f"Retrasadas: {stats['overdue']}"

        )

        self.lbl_tasks.configure(

            text=f"{stats['total']} tareas"

        )

    # =====================================================
    # CAMBIO DE PESTAÑA
    # =====================================================

    def tab_changed(

        self,

        event=None

    ):

        indice = self.notebook.index(

            self.notebook.select()

        )

        nombres = [

            "Dashboard",

            "Calendario",

            "Kanban",

            "Gantt",

            "Informes",

            "Power BI"

        ]

        if indice < len(nombres):

            self.status_message.set(

                nombres[indice]

            )

    # =====================================================
    # MOSTRAR PESTAÑA
    # =====================================================

    def show_tab(

        self,

        index

    ):

        self.notebook.select(

            index

        )
        
        
    # =====================================================
    # NUEVA TAREA
    # =====================================================

    def new_task(self):

        dialog = TaskDialog(self)

        task = dialog.show()

        if task is None:

            return

        self.task_manager.add_task(

            task

        )

    # =====================================================
    # EDITAR TAREA
    # =====================================================

    def edit_task(self):

        if self.current_task is None:

            messagebox.showinfo(

                "Task Planner Pro",

                "Seleccione una tarea."

            )

            return

        self.edit_task_by_id(

            self.current_task.id

        )

    # =====================================================
    # EDITAR POR ID
    # =====================================================

    def edit_task_by_id(

        self,

        task_id

    ):

        task = self.task_manager.get(

            task_id

        )

        if task is None:

            return

        dialog = TaskDialog(

            self,

            task.clone()

        )

        resultado = dialog.show()

        if resultado is None:

            return

        self.task_manager.update_task(

            resultado

        )

    # =====================================================
    # ELIMINAR
    # =====================================================

    def delete_task(self):

        if self.current_task is None:

            return

        if not messagebox.askyesno(

            "Eliminar",

            f"¿Eliminar '{self.current_task.titulo}'?"

        ):

            return

        self.task_manager.delete_task(

            self.current_task.id

        )

        self.current_task = None

    # =====================================================
    # CAMBIO DESDE PANEL
    # =====================================================

    def task_changed(

        self,

        task

    ):

        self.task_manager.update_task(

            task

        )

    # =====================================================
    # GUARDAR
    # =====================================================

    def save(self):

        try:

            self.task_manager.save()

            self.status_message.set(

                "Proyecto guardado."

            )

        except Exception as ex:

            messagebox.showerror(

                "Guardar",

                str(ex)

            )

    # =====================================================
    # IMPORTAR EXCEL
    # =====================================================

    def import_excel(self):

        try:

            self.task_manager.import_excel()

            self.refresh_all()

        except Exception as ex:

            messagebox.showerror(

                "Importar",

                str(ex)

            )

    # =====================================================
    # EXPORTAR EXCEL
    # =====================================================

    def export_excel(self):

        try:

            self.task_manager.export_excel()

            self.status_message.set(

                "Exportación finalizada."

            )

        except Exception as ex:

            messagebox.showerror(

                "Exportar",

                str(ex)

            )

    # =====================================================
    # DESHACER
    # =====================================================

    def undo(self):

        if self.task_manager.undo():

            self.refresh_all()

    # =====================================================
    # REHACER
    # =====================================================

    def redo(self):

        if self.task_manager.redo():

            self.refresh_all()

    # =====================================================
    # BÚSQUEDA
    # =====================================================

    def search(self):

        self.search_entry.focus_set()

        self.search_entry.select_range(

            0,

            tk.END

        )

    # =====================================================
    # CAMBIO TEXTO BÚSQUEDA
    # =====================================================

    def search_changed(

        self,

        event=None

    ):

        texto = self.search_var.get().strip()

        if not texto:

            self.refresh_all()

            return

        tareas = self.task_manager.search(

            texto

        )

        self.dashboard_panel.reload(

            tareas

        )

        self.calendar_panel.reload(

            tareas

        )

        self.kanban_panel.reload(

            tareas

        )

        self.gantt_panel.reload(

            tareas

        )

    # =====================================================
    # AUTOGUARDADO
    # =====================================================

    def autosave(self):

        try:

            self.task_manager.autosave()

        finally:

            self.after(

                300000,

                self.autosave

            )

    # =====================================================
    # BACKUP
    # =====================================================

    def create_backup(self):

        try:

            self.task_manager.create_backup()

            self.status_message.set(

                "Backup creado."

            )

        except Exception as ex:

            messagebox.showerror(

                "Backup",

                str(ex)

            )
            
            
    # =====================================================
    # ACERCA DE
    # =====================================================

    def about(self):

        texto = (
            f"{self.APP_NAME} {self.VERSION}\n\n"
            "Gestión profesional de tareas y proyectos.\n\n"
            "Módulos:\n"
            "• Dashboard\n"
            "• Calendario\n"
            "• Kanban\n"
            "• Gantt\n"
            "• Informes\n"
            "• Power BI\n\n"
            "© Antonio García"
        )

        messagebox.showinfo(

            "Acerca de",

            texto

        )

    # =====================================================
    # ACTUALIZAR SELECCIÓN
    # =====================================================

    def set_current_task(

        self,

        task

    ):

        self.current_task = task

    # =====================================================
    # ACTUALIZAR PROYECTO
    # =====================================================

    def set_current_project(

        self,

        project

    ):

        self.current_project = project

    # =====================================================
    # CAMBIAR TEMA
    # =====================================================

    def set_theme(

        self,

        theme

    ):

        try:

            self.style.theme_use(

                theme

            )

        except Exception:

            pass

    # =====================================================
    # RECARGAR INTERFAZ
    # =====================================================

    def reload_ui(self):

        self.refresh_all()

        self.update()

    # =====================================================
    # RESTABLECER FILTROS
    # =====================================================

    def clear_filters(self):

        self.search_var.set("")

        self.refresh_all()

    # =====================================================
    # EXPORTAR INFORME
    # =====================================================

    def export_report(self):

        try:

            self.task_manager.generate_report(

                "general"

            )

            self.status_message.set(

                "Informe generado."

            )

        except Exception as ex:

            messagebox.showerror(

                "Informe",

                str(ex)

            )

    # =====================================================
    # REFRESCAR POWER BI
    # =====================================================

    def refresh_powerbi(self):

        try:

            self.task_manager.refresh_powerbi()

            self.status_message.set(

                "Power BI actualizado."

            )

        except Exception as ex:

            messagebox.showerror(

                "Power BI",

                str(ex)

            )

    # =====================================================
    # ATAJOS
    # =====================================================

    def register_shortcuts(self):

        self.bind(

            "<Control-n>",

            lambda e: self.new_task()

        )

        self.bind(

            "<Control-s>",

            lambda e: self.save()

        )

        self.bind(

            "<Control-f>",

            lambda e: self.search()

        )

        self.bind(

            "<F5>",

            lambda e: self.refresh_all()

        )

        self.bind(

            "<Control-z>",

            lambda e: self.undo()

        )

        self.bind(

            "<Control-y>",

            lambda e: self.redo()

        )

        self.bind(

            "<Delete>",

            lambda e: self.delete_task()

        )

    # =====================================================
    # CERRAR
    # =====================================================

    def close(self):

        if self.task_manager.modified:

            respuesta = messagebox.askyesnocancel(

                "Salir",

                "Hay cambios sin guardar.\n\n¿Desea guardar antes de salir?"

            )

            if respuesta is None:

                return

            if respuesta:

                self.save()

        try:

            self.task_manager.shutdown()

        except Exception:

            pass

        self.destroy()


# ==========================================================
# EJECUCIÓN
# ==========================================================

def main():

    app = MainWindow()

    app.register_shortcuts()

    app.mainloop()


if __name__ == "__main__":

    main()
        
        
        
        
        
        
        
        
        
        
        
        
        