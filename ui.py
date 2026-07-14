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

    # ======================================================
    # TABLA DE TAREAS
    # ======================================================

    def create_task_table(self):

        columns = (

            "ID",

            "Título",

            "Responsable",

            "Estado",

            "Prioridad",

            "Categoría",

            "Inicio",

            "Vencimiento",

            "Avance"

        )

        self.tree = ttk.Treeview(

            self.table_frame,

            columns=columns,

            show="headings",

            selectmode="browse"

        )

        self.tree.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        scrollbar_y = ttk.Scrollbar(

            self.table_frame,

            orient="vertical",

            command=self.tree.yview

        )

        scrollbar_y.pack(

            side="right",

            fill="y"

        )

        scrollbar_x = ttk.Scrollbar(

            self.table_frame,

            orient="horizontal",

            command=self.tree.xview

        )

        scrollbar_x.pack(

            side="bottom",

            fill="x"

        )

        self.tree.configure(

            yscrollcommand=scrollbar_y.set,

            xscrollcommand=scrollbar_x.set

        )

        widths = {

            "ID":70,

            "Título":350,

            "Responsable":170,

            "Estado":120,

            "Prioridad":120,

            "Categoría":150,

            "Inicio":110,

            "Vencimiento":110,

            "Avance":90

        }

        for columna in columns:

            self.tree.heading(

                columna,

                text=columna,

                command=lambda c=columna:

                    self.sort_table(c)

            )

            self.tree.column(

                columna,

                width=widths[columna],

                anchor="center"

            )

        self.tree.column(

            "Título",

            anchor="w"

        )

        self.tree.tag_configure(

            "Pendiente",

            background="#FFF6CC"

        )

        self.tree.tag_configure(

            "En curso",

            background="#DCEEFF"

        )

        self.tree.tag_configure(

            "Bloqueada",

            background="#FFD9D9"

        )

        self.tree.tag_configure(

            "Finalizada",

            background="#DFF5DF"

        )

        self.tree.bind(

            "<<TreeviewSelect>>",

            self.on_select_task

        )

        self.tree.bind(

            "<Double-1>",

            lambda e:self.edit_task()

        )

        self.tree.bind(

            "<Button-3>",

            self.popup_menu

        )

    # ======================================================
    # RECARGAR TABLA
    # ======================================================

    def refresh_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        for tarea in self.tasks:

            self.tree.insert(

                "",

                "end",

                iid=str(tarea.id),

                values=(

                    tarea.id,

                    tarea.titulo,

                    tarea.responsable,

                    tarea.estado,

                    tarea.prioridad,

                    tarea.categoria,

                    tarea.fecha_inicio,

                    tarea.fecha_prevista,

                    f"{tarea.avance}%"

                ),

                tags=(

                    tarea.estado,

                )

            )

    # ======================================================
    # SELECCIÓN
    # ======================================================

    def on_select_task(

        self,

        event=None

    ):

        seleccion = self.tree.selection()

        if not seleccion:

            self.selected_task = None

            return

        task_id = int(

            seleccion[0]

        )

        self.selected_task = self.excel.get_task(

            task_id

        )

        if self.selected_task:

            self.status.set(

                f"Tarea seleccionada: "

                f"{self.selected_task.titulo}"

            )

    # ======================================================
    # ORDENAR
    # ======================================================

    def sort_table(

        self,

        column

    ):

        filas = [

            (

                self.tree.set(

                    item,

                    column

                ),

                item

            )

            for item

            in self.tree.get_children()

        ]

        filas.sort()

        for indice, (_, item) in enumerate(filas):

            self.tree.move(

                item,

                "",

                indice

            )

    # ======================================================
    # MENÚ CONTEXTUAL
    # ======================================================

    def popup_menu(

        self,

        event

    ):

        menu = tk.Menu(

            self,

            tearoff=False

        )

        menu.add_command(

            label="Editar",

            command=self.edit_task

        )

        menu.add_command(

            label="Duplicar",

            command=self.duplicate_task

        )

        menu.add_command(

            label="Eliminar",

            command=self.delete_task

        )

        menu.tk_popup(

            event.x_root,

            event.y_root

        )

    # ======================================================
    # NUEVA TAREA
    # ======================================================

    def new_task(self):

        dialog = TaskDialog(

            self,

            title="Nueva tarea"

        )

        if not dialog.result:

            return

        task = dialog.result

        self.excel.add_task(task)

        self.excel.refresh()

        self.refresh()

        self.status.set(

            "Nueva tarea creada"

        )

    # ======================================================
    # EDITAR TAREA
    # ======================================================

    def edit_task(self):

        if self.selected_task is None:

            messagebox.showwarning(

                APP_NAME,

                "Seleccione una tarea."

            )

            return

        dialog = TaskDialog(

            self,

            task=self.selected_task,

            title="Editar tarea"

        )

        if not dialog.result:

            return

        self.excel.update_task(

            dialog.result

        )

        self.excel.add_history(

            dialog.result.id,

            "Usuario",

            dialog.result.avance,

            "Tarea modificada"

        )

        self.excel.refresh()

        self.refresh()

        self.status.set(

            "Tarea actualizada"

        )

    # ======================================================
    # ELIMINAR TAREA
    # ======================================================

    def delete_task(self):

        if self.selected_task is None:

            return

        respuesta = messagebox.askyesno(

            APP_NAME,

            "¿Desea eliminar la tarea?"

        )

        if not respuesta:

            return

        self.excel.delete_task(

            self.selected_task.id

        )

        self.refresh()

        self.status.set(

            "Tarea eliminada"

        )

    # ======================================================
    # DUPLICAR TAREA
    # ======================================================

    def duplicate_task(self):

        if self.selected_task is None:

            return

        tarea = self.selected_task

        nueva = type(tarea)()

        nueva.titulo = tarea.titulo

        nueva.descripcion = tarea.descripcion

        nueva.responsable = tarea.responsable

        nueva.estado = tarea.estado

        nueva.prioridad = tarea.prioridad

        nueva.categoria = tarea.categoria

        nueva.etiquetas = tarea.etiquetas

        nueva.fecha_inicio = tarea.fecha_inicio

        nueva.fecha_prevista = tarea.fecha_prevista

        nueva.fecha_creacion = datetime.now().strftime(

            DATE_FORMAT

        )

        nueva.avance = 0

        nueva.comentarios = ""

        self.excel.add_task(

            nueva

        )

        self.refresh()

    # ======================================================
    # BUSCADOR
    # ======================================================

    def search_tasks(self):

        texto = self.search_text.get().strip()

        if texto == "":

            self.load_tasks()

        else:

            self.tasks = self.excel.search_tasks(

                texto

            )

        self.refresh_table()

    # ======================================================
    # FILTRO POR ESTADO
    # ======================================================

    def filter_status(

        self,

        estado

    ):

        self.tasks = self.excel.tasks_by_status(

            estado

        )

        self.refresh_table()

        self.status.set(

            f"{len(self.tasks)} tareas"

        )

    # ======================================================
    # FILTRO RESPONSABLE
    # ======================================================

    def filter_owner(

        self,

        responsable

    ):

        self.tasks = self.excel.tasks_by_owner(

            responsable

        )

        self.refresh_table()

    # ======================================================
    # FILTRO CATEGORÍA
    # ======================================================

    def filter_category(

        self,

        categoria

    ):

        self.tasks = self.excel.tasks_by_category(

            categoria

        )

        self.refresh_table()

    # ======================================================
    # RESETEAR FILTROS
    # ======================================================

    def clear_filters(self):

        self.search_text.set("")

        self.load_tasks()

        self.refresh_table()

        self.status.set(

            "Filtros eliminados"

        )

    # ======================================================
    # ACTUALIZAR PANEL DE NOTIFICACIONES
    # ======================================================

    def show_notifications(self):

        self.notification_list.delete(

            0,

            tk.END

        )

        for mensaje in self.notifications.ui_messages():

            self.notification_list.insert(

                tk.END,

                mensaje

            )
        
        
    # ======================================================
    # REFRESCAR DASHBOARD
    # ======================================================

    def refresh_dashboard(self):

        try:

            datos = self.metrics.dashboard_data()

            if hasattr(self.dashboard, "update_data"):

                self.dashboard.update_data(datos)

        except Exception as ex:

            print("Dashboard:", ex)

    # ======================================================
    # REFRESCAR CALENDARIO
    # ======================================================

    def refresh_calendar(self):

        try:

            if hasattr(self.calendar, "load_tasks"):

                self.calendar.load_tasks(self.tasks)

        except Exception as ex:

            print("Calendar:", ex)

    # ======================================================
    # REFRESCAR KANBAN
    # ======================================================

    def refresh_kanban(self):

        try:

            if hasattr(self.kanban, "load_tasks"):

                self.kanban.load_tasks(self.tasks)

        except Exception as ex:

            print("Kanban:", ex)

    # ======================================================
    # REFRESCAR GANTT
    # ======================================================

    def refresh_gantt(self):

        try:

            if hasattr(self.gantt, "load_tasks"):

                self.gantt.load_tasks(self.tasks)

        except Exception as ex:

            print("Gantt:", ex)

    # ======================================================
    # EXPORTAR EXCEL
    # ======================================================

    def export_excel(self):

        fichero = self.report.export_excel()

        messagebox.showinfo(

            APP_NAME,

            f"Informe generado\n\n{fichero}"

        )

    # ======================================================
    # EXPORTAR CSV
    # ======================================================

    def export_csv(self):

        fichero = self.report.export_csv()

        messagebox.showinfo(

            APP_NAME,

            f"Informe generado\n\n{fichero}"

        )

    # ======================================================
    # EXPORTAR PDF
    # ======================================================

    def export_pdf(self):

        fichero = self.report.export_pdf()

        messagebox.showinfo(

            APP_NAME,

            f"Informe generado\n\n{fichero}"

        )

    # ======================================================
    # EXPORTAR TODO
    # ======================================================

    def export_all_reports(self):

        self.report.export_all()

        messagebox.showinfo(

            APP_NAME,

            "Todos los informes han sido exportados."

        )

    # ======================================================
    # BACKUP
    # ======================================================

    def create_backup(self):

        fichero = self.backup.create_zip_backup()

        messagebox.showinfo(

            APP_NAME,

            f"Backup creado\n\n{fichero}"

        )

    # ======================================================
    # RESTAURAR BACKUP
    # ======================================================

    def restore_backup(self):

        fichero = filedialog.askopenfilename(

            title="Seleccionar Backup",

            filetypes=[

                ("Backups", "*.zip *.xlsx")

            ]

        )

        if not fichero:

            return

        self.backup.restore(fichero)

        self.refresh()

        messagebox.showinfo(

            APP_NAME,

            "Backup restaurado correctamente."

        )

    # ======================================================
    # REFRESCAR POWER BI
    # ======================================================

    def refresh_powerbi(self):

        self.powerbi.refresh_all()

        messagebox.showinfo(

            APP_NAME,

            "Dataset actualizado."

        )

    # ======================================================
    # ACTUALIZACIÓN COMPLETA
    # ======================================================

    def full_refresh(self):

        self.excel.refresh()

        self.load_tasks()

        self.refresh_dashboard()

        self.refresh_calendar()

        self.refresh_kanban()

        self.refresh_gantt()

        self.refresh_table()

        self.show_notifications()

        self.status.set(

            "Aplicación sincronizada"

        )

    # ======================================================
    # INFORMACIÓN DEL PROYECTO
    # ======================================================

    def project_info(self):

        datos = self.metrics.executive_summary()

        texto = f"""

Task Planner Pro

Versión: {APP_VERSION}

Total tareas: {datos['total_tareas']}

Tareas activas: {datos['tareas_activas']}

Finalizadas: {datos['tareas_finalizadas']}

Retrasadas: {datos['tareas_retrasadas']}

Avance global: {datos['avance_global']}%

"""

        messagebox.showinfo(

            "Información",

            texto

        )
        
    # ======================================================
    # ATAJOS DE TECLADO
    # ======================================================

    def register_shortcuts(self):

        self.bind("<Control-n>", lambda e: self.new_task())

        self.bind("<Control-e>", lambda e: self.edit_task())

        self.bind("<Delete>", lambda e: self.delete_task())

        self.bind("<F5>", lambda e: self.full_refresh())

        self.bind("<Control-f>", lambda e: self.focus_search())

        self.bind("<Escape>", lambda e: self.clear_filters())

    # ======================================================
    # BUSCADOR
    # ======================================================

    def focus_search(self):

        self.search_entry.focus_set()

        self.search_entry.select_range(0, tk.END)

    # ======================================================
    # FAVORITOS
    # ======================================================

    def add_favorite(self):

        if self.selected_task is None:

            return

        self.selected_task.favorita = True

        self.excel.update_task(

            self.selected_task

        )

        self.refresh()

    def remove_favorite(self):

        if self.selected_task is None:

            return

        self.selected_task.favorita = False

        self.excel.update_task(

            self.selected_task

        )

        self.refresh()

    def show_favorites(self):

        self.tasks = [

            t

            for t in self.excel.load_tasks()

            if getattr(

                t,

                "favorita",

                False

            )

        ]

        self.refresh_table()

    # ======================================================
    # ETIQUETAS
    # ======================================================

    def filter_tag(

        self,

        tag

    ):

        self.tasks = [

            t

            for t in self.excel.load_tasks()

            if tag.lower()

            in t.etiquetas.lower()

        ]

        self.refresh_table()

    # ======================================================
    # ESTADÍSTICAS
    # ======================================================

    def update_status_statistics(self):

        datos = self.metrics.kpi()

        self.status.set(

            f"Tareas: {datos['total']}   "

            f"Pendientes: {datos['pendientes']}   "

            f"Curso: {datos['en_curso']}   "

            f"Finalizadas: {datos['finalizadas']}"

        )

    # ======================================================
    # SINCRONIZACIÓN
    # ======================================================

    def synchronize_panels(self):

        self.refresh_dashboard()

        self.refresh_calendar()

        self.refresh_kanban()

        self.refresh_gantt()

        self.refresh_table()

        self.show_notifications()

        self.update_status_statistics()

    # ======================================================
    # CAMBIO DE PESTAÑA
    # ======================================================

    def on_tab_changed(

        self,

        event=None

    ):

        indice = self.notebook.index(

            self.notebook.select()

        )

        if indice == 0:

            self.refresh_dashboard()

        elif indice == 1:

            self.refresh_calendar()

        elif indice == 2:

            self.refresh_kanban()

        elif indice == 3:

            self.refresh_gantt()

        elif indice == 4:

            self.refresh_table()

    # ======================================================
    # CERRAR
    # ======================================================

    def on_close(self):

        try:

            self.backup.maintenance()

        except Exception:

            pass

        self.destroy()

    # ======================================================
    # INICIALIZACIÓN FINAL
    # ======================================================

    def initialize(self):

        self.register_shortcuts()

        self.notebook.bind(

            "<<NotebookTabChanged>>",

            self.on_tab_changed

        )

        self.protocol(

            "WM_DELETE_WINDOW",

            self.on_close

        )

        self.full_refresh()
        
        

        
        
        
        
        








