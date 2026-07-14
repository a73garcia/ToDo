"""
=========================================================
Task Planner Pro
gantt_panel.py
=========================================================
Diagrama de Gantt
=========================================================
"""

from __future__ import annotations

import tkinter as tk

from tkinter import ttk

from datetime import datetime
from datetime import timedelta

from config import (
    DATE_FORMAT,
    STATUS_PENDING,
    STATUS_PROGRESS,
    STATUS_BLOCKED,
    STATUS_DONE
)


class GanttPanel(ttk.Frame):

    """
    Panel Gantt.

    Responsabilidades:

        • Dibujar tareas
        • Mostrar calendario
        • Mostrar línea temporal
        • Scroll
        • Zoom

    No modifica datos.
    No calcula métricas.
    """

    DAY_WIDTH = 30
    ROW_HEIGHT = 34
    HEADER_HEIGHT = 40
    TASK_WIDTH = 260

    def __init__(

        self,

        parent

    ):

        super().__init__(parent)

        self.tasks = []

        self.zoom = 1

        self.start_date = None

        self.end_date = None

        self.task_open_callback = None

        self.task_change_callback = None

        self.selected_task = None

        self._build_ui()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def _build_ui(self):

        self.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1)

        self._create_toolbar()

        self._create_canvas()

    # =====================================================
    # TOOLBAR
    # =====================================================

    def _create_toolbar(self):

        toolbar = ttk.Frame(self)

        toolbar.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=8,

            pady=8

        )

        ttk.Label(

            toolbar,

            text="Diagrama de Gantt",

            font=(

                "Segoe UI",

                18,

                "bold"

            )

        ).pack(

            side="left"

        )

        ttk.Button(

            toolbar,

            text="+",

            width=3,

            command=self.zoom_in

        ).pack(

            side="right",

            padx=2

        )

        ttk.Button(

            toolbar,

            text="-",

            width=3,

            command=self.zoom_out

        ).pack(

            side="right",

            padx=2

        )

        ttk.Button(

            toolbar,

            text="Hoy",

            command=self.goto_today

        ).pack(

            side="right",

            padx=2

        )

        ttk.Button(

            toolbar,

            text="Actualizar",

            command=self.refresh

        ).pack(

            side="right",

            padx=2

        )

    # =====================================================
    # CANVAS
    # =====================================================

    def _create_canvas(self):

        frame = ttk.Frame(self)

        frame.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        frame.columnconfigure(0, weight=1)

        frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(

            frame,

            background="white",

            highlightthickness=0

        )

        self.canvas.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        vscroll = ttk.Scrollbar(

            frame,

            orient="vertical",

            command=self.canvas.yview

        )

        vscroll.grid(

            row=0,

            column=1,

            sticky="ns"

        )

        hscroll = ttk.Scrollbar(

            frame,

            orient="horizontal",

            command=self.canvas.xview

        )

        hscroll.grid(

            row=1,

            column=0,

            sticky="ew"

        )

        self.canvas.configure(

            xscrollcommand=hscroll.set,

            yscrollcommand=vscroll.set

        )

        self.canvas.bind(

            "<Double-Button-1>",

            self._double_click

        )

        self.canvas.bind(

            "<Button-1>",

            self._click

        )

    # =====================================================
    # CALLBACKS
    # =====================================================

    def set_task_open_callback(

        self,

        callback

    ):

        self.task_open_callback = callback

    def set_task_change_callback(

        self,

        callback

    ):

        self.task_change_callback = callback

    # =====================================================
    # CARGAR
    # =====================================================

    def load_tasks(

        self,

        tasks

    ):

        self.tasks = list(tasks)

        self._calculate_range()

        self.refresh()

    # =====================================================
    # CALCULAR RANGO
    # =====================================================

    def _calculate_range(self):

        fechas = []

        for task in self.tasks:

            try:

                if task.fecha_inicio:

                    fechas.append(

                        datetime.strptime(

                            task.fecha_inicio,

                            DATE_FORMAT

                        )

                    )

            except Exception:

                pass

            try:

                if task.fecha_prevista:

                    fechas.append(

                        datetime.strptime(

                            task.fecha_prevista,

                            DATE_FORMAT

                        )

                    )

            except Exception:

                pass

        if not fechas:

            hoy = datetime.today()

            self.start_date = hoy

            self.end_date = hoy + timedelta(days=30)

            return

        self.start_date = min(fechas)

        self.end_date = max(fechas) + timedelta(days=15)

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        self.canvas.delete("all")

        self._draw_header()

        self._draw_today()

        self._draw_tasks()

    # =====================================================
    # ZOOM
    # =====================================================

    def zoom_in(self):

        self.zoom = min(

            self.zoom + 1,

            4

        )

        self.refresh()

    def zoom_out(self):

        self.zoom = max(

            self.zoom - 1,

            1

        )

        self.refresh()

    # =====================================================
    # IR A HOY
    # =====================================================

    def goto_today(self):

        self.refresh()

    # =====================================================
    # CLICK
    # =====================================================

    def _click(

        self,

        event

    ):

        pass

    # =====================================================
    # DOBLE CLICK
    # =====================================================

    def _double_click(

        self,

        event

    ):

        if self.selected_task and self.task_open_callback:

            self.task_open_callback(

                self.selected_task.id

            )
            
    # =====================================================
    # DIBUJAR CABECERA
    # =====================================================

    def _draw_header(self):

        dias = (self.end_date - self.start_date).days + 1

        ancho_dia = self.DAY_WIDTH * self.zoom

        self.canvas.create_rectangle(
            0,
            0,
            self.TASK_WIDTH,
            self.HEADER_HEIGHT,
            fill="#ECEFF1",
            outline="#B0BEC5"
        )

        self.canvas.create_text(
            10,
            self.HEADER_HEIGHT / 2,
            anchor="w",
            text="Tarea",
            font=("Segoe UI", 10, "bold")
        )

        fecha = self.start_date

        x = self.TASK_WIDTH

        for _ in range(dias):

            self.canvas.create_rectangle(
                x,
                0,
                x + ancho_dia,
                self.HEADER_HEIGHT,
                fill="#ECEFF1",
                outline="#CFD8DC"
            )

            self.canvas.create_text(
                x + ancho_dia / 2,
                14,
                text=fecha.strftime("%d"),
                font=("Segoe UI", 8)
            )

            self.canvas.create_text(
                x + ancho_dia / 2,
                30,
                text=fecha.strftime("%b"),
                font=("Segoe UI", 7)
            )

            fecha += timedelta(days=1)

            x += ancho_dia

    # =====================================================
    # DIBUJAR LÍNEA DE HOY
    # =====================================================

    def _draw_today(self):

        hoy = datetime.today()

        if hoy < self.start_date:

            return

        if hoy > self.end_date:

            return

        ancho_dia = self.DAY_WIDTH * self.zoom

        dias = (hoy - self.start_date).days

        x = self.TASK_WIDTH + dias * ancho_dia

        self.canvas.create_line(

            x,

            0,

            x,

            5000,

            fill="#E53935",

            width=2,

            dash=(5, 3)

        )

    # =====================================================
    # DIBUJAR TAREAS
    # =====================================================

    def _draw_tasks(self):

        ancho_dia = self.DAY_WIDTH * self.zoom

        y = self.HEADER_HEIGHT

        for task in self.tasks:

            self._draw_task_row(

                task,

                y,

                ancho_dia

            )

            y += self.ROW_HEIGHT

        self.canvas.configure(

            scrollregion=self.canvas.bbox("all")

        )

    # =====================================================
    # DIBUJAR FILA
    # =====================================================

    def _draw_task_row(

        self,

        task,

        y,

        ancho_dia

    ):

        self.canvas.create_rectangle(

            0,

            y,

            self.TASK_WIDTH,

            y + self.ROW_HEIGHT,

            fill="white",

            outline="#E0E0E0"

        )

        self.canvas.create_text(

            8,

            y + self.ROW_HEIGHT / 2,

            anchor="w",

            text=task.titulo,

            font=("Segoe UI", 9)

        )

        if not task.fecha_inicio:

            return

        if not task.fecha_prevista:

            return

        try:

            inicio = datetime.strptime(

                task.fecha_inicio,

                DATE_FORMAT

            )

            fin = datetime.strptime(

                task.fecha_prevista,

                DATE_FORMAT

            )

        except Exception:

            return

        x1 = self.TASK_WIDTH + (

            (inicio - self.start_date).days

            * ancho_dia

        )

        x2 = self.TASK_WIDTH + (

            (fin - self.start_date).days + 1

        ) * ancho_dia

        color = self._status_color(

            task.estado

        )

        barra = self.canvas.create_rectangle(

            x1,

            y + 6,

            x2,

            y + self.ROW_HEIGHT - 6,

            fill=color,

            outline="#455A64",

            width=1,

            tags=(

                "task",

                str(task.id)

            )

        )

        self.canvas.create_text(

            (x1 + x2) / 2,

            y + self.ROW_HEIGHT / 2,

            text=f"{task.avance}%",

            fill="white",

            font=("Segoe UI", 8, "bold"),

            tags=(

                "task",

                str(task.id)

            )

        )

    # =====================================================
    # COLOR DEL ESTADO
    # =====================================================

    def _status_color(

        self,

        estado

    ):

        if estado == STATUS_PENDING:

            return "#F9A825"

        if estado == STATUS_PROGRESS:

            return "#1E88E5"

        if estado == STATUS_BLOCKED:

            return "#E53935"

        if estado == STATUS_DONE:

            return "#43A047"

        return "#90A4AE"
        
        
    # =====================================================
    # SELECCIÓN DE TAREA
    # =====================================================

    def _click(self, event):

        item = self.canvas.find_closest(

            self.canvas.canvasx(event.x),

            self.canvas.canvasy(event.y)

        )

        if not item:

            self.selected_task = None

            return

        tags = self.canvas.gettags(item)

        if len(tags) < 2:

            self.selected_task = None

            return

        if tags[0] != "task":

            self.selected_task = None

            return

        try:

            task_id = int(tags[1])

        except Exception:

            return

        self.selected_task = self.find_task(task_id)

        self._highlight_selected(task_id)

    # =====================================================
    # RESALTAR SELECCIÓN
    # =====================================================

    def _highlight_selected(self, task_id):

        self.canvas.itemconfigure(

            "selected",

            width=1

        )

        self.canvas.dtag(

            "selected",

            "selected"

        )

        for item in self.canvas.find_withtag(str(task_id)):

            self.canvas.addtag_withtag(

                "selected",

                item

            )

        self.canvas.itemconfigure(

            "selected",

            width=3,

            outline="#000000"

        )

    # =====================================================
    # BUSCAR TAREA
    # =====================================================

    def find_task(self, task_id):

        for task in self.tasks:

            if task.id == task_id:

                return task

        return None

    # =====================================================
    # ACTUALIZAR TAREA
    # =====================================================

    def update_task(self, task):

        actual = self.find_task(task.id)

        if actual is None:

            return

        actual.__dict__.update(task.__dict__)

        self.refresh()

    # =====================================================
    # AÑADIR TAREA
    # =====================================================

    def add_task(self, task):

        self.tasks.append(task)

        self._calculate_range()

        self.refresh()

    # =====================================================
    # ELIMINAR TAREA
    # =====================================================

    def remove_task(self, task_id):

        self.tasks = [

            t

            for t in self.tasks

            if t.id != task_id

        ]

        self.selected_task = None

        self._calculate_range()

        self.refresh()

    # =====================================================
    # MOVER FECHAS
    # =====================================================

    def move_task(

        self,

        task_id,

        start_date,

        end_date

    ):

        task = self.find_task(task_id)

        if task is None:

            return

        task.fecha_inicio = start_date

        task.fecha_prevista = end_date

        if self.task_change_callback:

            self.task_change_callback(task)

        self.refresh()

    # =====================================================
    # FILTRO
    # =====================================================

    def filter_tasks(self, predicate):

        originales = self.tasks

        self.tasks = list(

            filter(

                predicate,

                originales

            )

        )

        self._calculate_range()

        self.refresh()

        self.tasks = originales

    # =====================================================
    # LIMPIAR FILTRO
    # =====================================================

    def clear_filter(self):

        self._calculate_range()

        self.refresh()

    # =====================================================
    # EXPORTAR
    # =====================================================

    def export_image(self, filename):

        try:

            self.canvas.postscript(

                file=filename,

                colormode="color"

            )

        except Exception:

            pass

    # =====================================================
    # CENTRAR EN HOY
    # =====================================================

    def center_today(self):

        hoy = datetime.today()

        dias = (

            hoy - self.start_date

        ).days

        ancho = self.DAY_WIDTH * self.zoom

        x = (

            self.TASK_WIDTH +

            dias * ancho

        )

        region = self.canvas.bbox("all")

        if region:

            total = region[2]

            if total > 0:

                self.canvas.xview_moveto(

                    max(

                        0,

                        x / total

                    )

                )

    # =====================================================
    # AUTOREFRESH
    # =====================================================

    def start_autorefresh(

        self,

        interval=60000

    ):

        self.refresh()

        self.after(

            interval,

            lambda: self.start_autorefresh(

                interval

            )

        )

    # =====================================================
    # LIMPIAR
    # =====================================================

    def clear(self):

        self.selected_task = None

        self.tasks.clear()

        self.canvas.delete("all")

    # =====================================================
    # DESTRUCTOR
    # =====================================================

    def destroy(self):

        self.clear()

        super().destroy()
        
        
    # =====================================================
    # DRAG & DROP DE BARRAS
    # =====================================================

    def enable_drag(self):

        self.drag_item = None

        self.drag_task = None

        self.drag_start_x = 0

        self.drag_original_start = None

        self.drag_original_end = None

        self.canvas.tag_bind(

            "task",

            "<ButtonPress-1>",

            self._drag_begin

        )

        self.canvas.tag_bind(

            "task",

            "<B1-Motion>",

            self._drag_motion

        )

        self.canvas.tag_bind(

            "task",

            "<ButtonRelease-1>",

            self._drag_end

        )

    # =====================================================
    # COMIENZO DRAG
    # =====================================================

    def _drag_begin(self, event):

        item = self.canvas.find_withtag("current")

        if not item:

            return

        tags = self.canvas.gettags(item)

        if len(tags) < 2:

            return

        try:

            task_id = int(tags[1])

        except Exception:

            return

        self.drag_task = self.find_task(task_id)

        if self.drag_task is None:

            return

        self.drag_item = item[0]

        self.drag_start_x = event.x

        self.drag_original_start = self.drag_task.fecha_inicio

        self.drag_original_end = self.drag_task.fecha_prevista

    # =====================================================
    # MOVIMIENTO
    # =====================================================

    def _drag_motion(self, event):

        if self.drag_item is None:

            return

        dx = event.x - self.drag_start_x

        self.canvas.move(

            self.drag_item,

            dx,

            0

        )

        self.drag_start_x = event.x

    # =====================================================
    # FINAL DRAG
    # =====================================================

    def _drag_end(self, event):

        if self.drag_task is None:

            return

        ancho_dia = self.DAY_WIDTH * self.zoom

        desplazamiento = self.canvas.coords(

            self.drag_item

        )[0]

        dias = round(

            (

                desplazamiento -

                self.TASK_WIDTH

            ) / ancho_dia

        )

        try:

            inicio = datetime.strptime(

                self.drag_original_start,

                DATE_FORMAT

            )

            fin = datetime.strptime(

                self.drag_original_end,

                DATE_FORMAT

            )

        except Exception:

            self.refresh()

            return

        nuevo_inicio = inicio + timedelta(days=dias)

        nuevo_fin = fin + timedelta(days=dias)

        self.drag_task.fecha_inicio = nuevo_inicio.strftime(

            DATE_FORMAT

        )

        self.drag_task.fecha_prevista = nuevo_fin.strftime(

            DATE_FORMAT

        )

        if self.task_change_callback:

            self.task_change_callback(

                self.drag_task

            )

        self.drag_item = None

        self.drag_task = None

        self.refresh()

    # =====================================================
    # ESCALA TEMPORAL
    # =====================================================

    def set_scale(

        self,

        scale

    ):

        scales = {

            "day": 30,

            "week": 10,

            "month": 4

        }

        self.DAY_WIDTH = scales.get(

            scale,

            30

        )

        self.refresh()

    # =====================================================
    # DEPENDENCIAS
    # =====================================================

    def draw_dependencies(self):

        for task in self.tasks:

            if not hasattr(

                task,

                "depends_on"

            ):

                continue

            for dependency in task.depends_on:

                origen = self.find_task(

                    dependency

                )

                if origen is None:

                    continue

                self._draw_dependency(

                    origen,

                    task

                )

    # =====================================================
    # FLECHA
    # =====================================================

    def _draw_dependency(

        self,

        task_from,

        task_to

    ):

        """
        Dibuja una flecha entre dos tareas.
        Se ejecutará después de dibujar las barras.
        """

        pass

    # =====================================================
    # REAJUSTAR RANGO
    # =====================================================

    def fit_to_tasks(self):

        self._calculate_range()

        self.center_today()

        self.refresh()

    # =====================================================
    # TAREA SIGUIENTE
    # =====================================================

    def next_task(self):

        if not self.tasks:

            return

        if self.selected_task is None:

            self.selected_task = self.tasks[0]

            return

        indice = self.tasks.index(

            self.selected_task

        )

        indice = min(

            indice + 1,

            len(self.tasks) - 1

        )

        self.selected_task = self.tasks[indice]

    # =====================================================
    # TAREA ANTERIOR
    # =====================================================

    def previous_task(self):

        if not self.tasks:

            return

        if self.selected_task is None:

            self.selected_task = self.tasks[0]

            return

        indice = self.tasks.index(

            self.selected_task

        )

        indice = max(

            indice - 1,

            0

        )

        self.selected_task = self.tasks[indice]
            
            
    # =====================================================
    # VISTA
    # =====================================================

    def set_view_mode(
        self,
        mode
    ):
        """
        Cambia la escala temporal.

        day
        week
        month
        quarter
        """

        self.view_mode = mode

        if mode == "day":
            self.DAY_WIDTH = 30

        elif mode == "week":
            self.DAY_WIDTH = 12

        elif mode == "month":
            self.DAY_WIDTH = 5

        elif mode == "quarter":
            self.DAY_WIDTH = 2

        self.refresh()

    # =====================================================
    # MOSTRAR SOLO ACTIVAS
    # =====================================================

    def show_active_only(self):

        self.filter_tasks(

            lambda t: t.estado != STATUS_DONE

        )

    # =====================================================
    # MOSTRAR TODAS
    # =====================================================

    def show_all(self):

        self.clear_filter()

    # =====================================================
    # TAREAS RETRASADAS
    # =====================================================

    def show_overdue(self):

        self.filter_tasks(

            lambda t: t.overdue

        )

    # =====================================================
    # BUSCAR
    # =====================================================

    def search(

        self,

        text

    ):

        texto = text.lower().strip()

        if not texto:

            self.clear_filter()

            return

        self.filter_tasks(

            lambda t:

            texto in t.titulo.lower()

            or texto in t.responsable.lower()

            or texto in t.proyecto.lower()

        )

    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    def statistics(self):

        total = len(self.tasks)

        done = len(

            [

                t

                for t in self.tasks

                if t.estado == STATUS_DONE

            ]

        )

        progress = len(

            [

                t

                for t in self.tasks

                if t.estado == STATUS_PROGRESS

            ]

        )

        blocked = len(

            [

                t

                for t in self.tasks

                if t.estado == STATUS_BLOCKED

            ]

        )

        pending = len(

            [

                t

                for t in self.tasks

                if t.estado == STATUS_PENDING

            ]

        )

        overdue = len(

            [

                t

                for t in self.tasks

                if t.overdue

            ]

        )

        return {

            "total": total,

            "done": done,

            "progress": progress,

            "blocked": blocked,

            "pending": pending,

            "overdue": overdue

        }

    # =====================================================
    # EXPORTAR PNG
    # =====================================================

    def save_png(

        self,

        filename

    ):

        self.canvas.postscript(

            file=filename.replace(

                ".png",

                ".ps"

            ),

            colormode="color"

        )

    # =====================================================
    # RECARGAR
    # =====================================================

    def reload(

        self,

        tasks

    ):

        self.tasks = list(tasks)

        self._calculate_range()

        self.refresh()

    # =====================================================
    # TAREAS DEL RESPONSABLE
    # =====================================================

    def tasks_by_owner(

        self,

        owner

    ):

        return [

            t

            for t in self.tasks

            if t.responsable == owner

        ]

    # =====================================================
    # TAREAS DEL PROYECTO
    # =====================================================

    def tasks_by_project(

        self,

        project

    ):

        return [

            t

            for t in self.tasks

            if t.proyecto == project

        ]

    # =====================================================
    # ZOOM AL 100 %
    # =====================================================

    def reset_zoom(self):

        self.zoom = 1

        self.refresh()

    # =====================================================
    # AJUSTAR AL PANEL
    # =====================================================

    def fit_view(self):

        self._calculate_range()

        self.reset_zoom()

        self.center_today()

    # =====================================================
    # CALLBACK EXPORTACIÓN
    # =====================================================

    def set_export_callback(

        self,

        callback

    ):

        self.export_callback = callback

    # =====================================================
    # EXPORTAR EXCEL
    # =====================================================

    def export_excel(self):

        if hasattr(

            self,

            "export_callback"

        ):

            self.export_callback(

                self.tasks

            )

    # =====================================================
    # ATAJOS DE TECLADO
    # =====================================================

    def register_shortcuts(self):

        self.bind(

            "<F5>",

            lambda e: self.refresh()

        )

        self.bind(

            "<Control-0>",

            lambda e: self.reset_zoom()

        )

        self.bind(

            "<Control-plus>",

            lambda e: self.zoom_in()

        )

        self.bind(

            "<Control-minus>",

            lambda e: self.zoom_out()

        )

        self.bind(

            "<Home>",

            lambda e: self.center_today()

        )

    # =====================================================
    # ENFOQUE
    # =====================================================

    def focus_panel(self):

        self.canvas.focus_set()

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    @property
    def total_tasks(self):

        return len(self.tasks)

    @property
    def visible_tasks(self):

        return len(self.tasks)
            
            
            
            
