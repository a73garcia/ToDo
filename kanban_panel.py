"""
=========================================================
Task Planner Pro
kanban_panel.py
=========================================================
Panel Kanban
=========================================================
"""

from __future__ import annotations

import tkinter as tk

from tkinter import ttk

from datetime import datetime

from config import (
    STATUS_PENDING,
    STATUS_PROGRESS,
    STATUS_BLOCKED,
    STATUS_DONE
)


# ==========================================================
# TARJETA
# ==========================================================

class KanbanCard(ttk.Frame):

    CARD_WIDTH = 280

    def __init__(

        self,

        parent,

        task,

        click_callback=None,

        double_click_callback=None,

        drag_callback=None

    ):

        super().__init__(

            parent,

            relief="solid",

            borderwidth=1,

            padding=8

        )

        self.task = task

        self.click_callback = click_callback

        self.double_click_callback = double_click_callback

        self.drag_callback = drag_callback

        self.drag_start_y = 0

        self.configure(width=self.CARD_WIDTH)

        self.build_ui()

        self.bind_events()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.columnconfigure(0, weight=1)

        # -----------------------------
        # CABECERA
        # -----------------------------

        header = ttk.Frame(self)

        header.grid(

            row=0,

            column=0,

            sticky="ew"

        )

        self.lbl_title = ttk.Label(

            header,

            text=self.task.titulo,

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            wraplength=240,

            justify="left"

        )

        self.lbl_title.pack(

            anchor="w"

        )

        # -----------------------------
        # RESPONSABLE
        # -----------------------------

        self.lbl_owner = ttk.Label(

            self,

            text=f"👤 {self.task.responsable}",

            font=(

                "Segoe UI",

                9

            )

        )

        self.lbl_owner.grid(

            row=1,

            column=0,

            sticky="w",

            pady=(6, 0)

        )

        # -----------------------------
        # FECHA
        # -----------------------------

        fecha = self.task.fecha_prevista

        if not fecha:

            fecha = "-"

        self.lbl_date = ttk.Label(

            self,

            text=f"📅 {fecha}",

            font=(

                "Segoe UI",

                9

            )

        )

        self.lbl_date.grid(

            row=2,

            column=0,

            sticky="w"

        )

        # -----------------------------
        # PRIORIDAD
        # -----------------------------

        self.lbl_priority = ttk.Label(

            self,

            text=self.task.prioridad,

            foreground=self.priority_color()

        )

        self.lbl_priority.grid(

            row=3,

            column=0,

            sticky="w",

            pady=(4, 0)

        )

        # -----------------------------
        # PROGRESO
        # -----------------------------

        self.progress = ttk.Progressbar(

            self,

            maximum=100,

            value=self.task.avance

        )

        self.progress.grid(

            row=4,

            column=0,

            sticky="ew",

            pady=(8, 0)

        )

        # -----------------------------
        # PIE
        # -----------------------------

        footer = ttk.Frame(self)

        footer.grid(

            row=5,

            column=0,

            sticky="ew",

            pady=(8, 0)

        )

        self.lbl_progress = ttk.Label(

            footer,

            text=f"{self.task.avance}%"

        )

        self.lbl_progress.pack(

            side="left"

        )

        if self.task.overdue:

            ttk.Label(

                footer,

                text="⚠",

                foreground="red"

            ).pack(

                side="right"

            )

    # =====================================================
    # COLOR PRIORIDAD
    # =====================================================

    def priority_color(self):

        prioridad = self.task.prioridad.lower()

        if prioridad == "crítica":

            return "#D32F2F"

        if prioridad == "alta":

            return "#F57C00"

        if prioridad == "media":

            return "#1976D2"

        return "#388E3C"

    # =====================================================
    # EVENTOS
    # =====================================================

    def bind_events(self):

        widgets = [

            self,

            self.lbl_title,

            self.lbl_owner,

            self.lbl_date,

            self.lbl_priority,

            self.progress

        ]

        for widget in widgets:

            widget.bind(

                "<Button-1>",

                self.on_click

            )

            widget.bind(

                "<Double-Button-1>",

                self.on_double_click

            )

            widget.bind(

                "<ButtonPress-1>",

                self.start_drag

            )

            widget.bind(

                "<B1-Motion>",

                self.drag

            )

            widget.bind(

                "<ButtonRelease-1>",

                self.stop_drag

            )

    # =====================================================
    # CLICK
    # =====================================================

    def on_click(self, event):

        if self.click_callback:

            self.click_callback(

                self.task

            )

    # =====================================================
    # DOBLE CLICK
    # =====================================================

    def on_double_click(self, event):

        if self.double_click_callback:

            self.double_click_callback(

                self.task

            )

    # =====================================================
    # DRAG
    # =====================================================

    def start_drag(self, event):

        self.drag_start_y = event.y_root

    def drag(self, event):

        if self.drag_callback:

            self.drag_callback(

                "move",

                self,

                event

            )

    def stop_drag(self, event):

        if self.drag_callback:

            self.drag_callback(

                "drop",

                self,

                event

            )
            
# ==========================================================
# COLUMNA KANBAN
# ==========================================================

class KanbanColumn(ttk.Frame):

    def __init__(

        self,

        parent,

        title,

        status

    ):

        super().__init__(parent)

        self.status = status

        self.title = title

        self.cards = []

        self.card_click_callback = None

        self.card_double_click_callback = None

        self.card_drag_callback = None

        self.build_ui()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def build_ui(self):

        self.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1)

        # --------------------------------------
        # CABECERA
        # --------------------------------------

        header = ttk.Frame(self)

        header.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=5,

            pady=(5, 0)

        )

        self.lbl_title = ttk.Label(

            header,

            text=self.title,

            font=(

                "Segoe UI",

                11,

                "bold"

            )

        )

        self.lbl_title.pack(

            side="left"

        )

        self.lbl_counter = ttk.Label(

            header,

            text="0",

            width=4,

            anchor="center"

        )

        self.lbl_counter.pack(

            side="right"

        )

        # --------------------------------------
        # CANVAS
        # --------------------------------------

        self.canvas = tk.Canvas(

            self,

            highlightthickness=0,

            borderwidth=0

        )

        self.canvas.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        scrollbar = ttk.Scrollbar(

            self,

            orient="vertical",

            command=self.canvas.yview

        )

        scrollbar.grid(

            row=1,

            column=1,

            sticky="ns"

        )

        self.canvas.configure(

            yscrollcommand=scrollbar.set

        )

        self.container = ttk.Frame(

            self.canvas

        )

        self.window = self.canvas.create_window(

            (0, 0),

            window=self.container,

            anchor="nw"

        )

        self.container.bind(

            "<Configure>",

            self._on_configure

        )

        self.canvas.bind(

            "<Configure>",

            self._resize

        )

        self.canvas.bind_all(

            "<MouseWheel>",

            self._mousewheel

        )

    # =====================================================
    # EVENTOS
    # =====================================================

    def _on_configure(

        self,

        event

    ):

        self.canvas.configure(

            scrollregion=self.canvas.bbox("all")

        )

    def _resize(

        self,

        event

    ):

        self.canvas.itemconfigure(

            self.window,

            width=event.width

        )

    def _mousewheel(

        self,

        event

    ):

        self.canvas.yview_scroll(

            int(-1 * (event.delta / 120)),

            "units"

        )

    # =====================================================
    # CALLBACKS
    # =====================================================

    def set_callbacks(

        self,

        click=None,

        double_click=None,

        drag=None

    ):

        self.card_click_callback = click

        self.card_double_click_callback = double_click

        self.card_drag_callback = drag

    # =====================================================
    # LIMPIAR
    # =====================================================

    def clear(self):

        for card in self.cards:

            card.destroy()

        self.cards.clear()

        self.update_counter()

    # =====================================================
    # AÑADIR TARJETA
    # =====================================================

    def add_card(

        self,

        task

    ):

        card = KanbanCard(

            self.container,

            task,

            click_callback=self.card_click_callback,

            double_click_callback=self.card_double_click_callback,

            drag_callback=self.card_drag_callback

        )

        card.pack(

            fill="x",

            padx=6,

            pady=4

        )

        self.cards.append(card)

        self.update_counter()

    # =====================================================
    # ELIMINAR TARJETA
    # =====================================================

    def remove_card(

        self,

        task_id

    ):

        for card in self.cards[:]:

            if card.task.id == task_id:

                card.destroy()

                self.cards.remove(card)

                break

        self.update_counter()

    # =====================================================
    # BUSCAR TARJETA
    # =====================================================

    def find_card(

        self,

        task_id

    ):

        for card in self.cards:

            if card.task.id == task_id:

                return card

        return None

    # =====================================================
    # ACTUALIZAR TARJETA
    # =====================================================

    def update_card(

        self,

        task

    ):

        card = self.find_card(task.id)

        if card is None:

            return

        card.task = task

        card.lbl_title.config(

            text=task.titulo

        )

        card.lbl_owner.config(

            text=f"👤 {task.responsable}"

        )

        fecha = task.fecha_prevista or "-"

        card.lbl_date.config(

            text=f"📅 {fecha}"

        )

        card.lbl_priority.config(

            text=task.prioridad,

            foreground=card.priority_color()

        )

        card.progress.configure(

            value=task.avance

        )

        card.lbl_progress.config(

            text=f"{task.avance}%"

        )

    # =====================================================
    # CONTADOR
    # =====================================================

    def update_counter(self):

        self.lbl_counter.config(

            text=str(

                len(self.cards)

            )

        )

    # =====================================================
    # DEVOLVER TAREAS
    # =====================================================

    def get_tasks(self):

        return [

            card.task

            for card in self.cards

        ]

    # =====================================================
    # ORDENAR
    # =====================================================

    def sort_cards(

        self,

        key=None

    ):

        if key is None:

            key = lambda t: (

                t.prioridad,

                t.fecha_prevista,

                t.titulo.lower()

            )

        tareas = sorted(

            self.get_tasks(),

            key=key

        )

        self.clear()

        for tarea in tareas:

            self.add_card(tarea)
            
            
            
# ==========================================================
# PANEL KANBAN
# ==========================================================

class KanbanPanel(ttk.Frame):

    def __init__(

        self,

        parent

    ):

        super().__init__(parent)

        self.tasks = []

        self.columns = {}

        self.selected_task = None

        self.task_open_callback = None

        self.task_change_callback = None

        self.build_ui()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def build_ui(self):

        self.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1)

        self.create_toolbar()

        self.create_canvas()

        self.create_columns()

    # =====================================================
    # TOOLBAR
    # =====================================================

    def create_toolbar(self):

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

            text="Kanban",

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

            text="Actualizar",

            command=self.refresh

        ).pack(

            side="right",

            padx=2

        )

        ttk.Button(

            toolbar,

            text="Ordenar",

            command=self.sort_all

        ).pack(

            side="right",

            padx=2

        )

    # =====================================================
    # CANVAS
    # =====================================================

    def create_canvas(self):

        self.canvas = tk.Canvas(

            self,

            highlightthickness=0

        )

        self.canvas.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        hscroll = ttk.Scrollbar(

            self,

            orient="horizontal",

            command=self.canvas.xview

        )

        hscroll.grid(

            row=2,

            column=0,

            sticky="ew"

        )

        self.canvas.configure(

            xscrollcommand=hscroll.set

        )

        self.board = ttk.Frame(

            self.canvas

        )

        self.window = self.canvas.create_window(

            (0, 0),

            window=self.board,

            anchor="nw"

        )

        self.board.bind(

            "<Configure>",

            self._board_configure

        )

        self.canvas.bind(

            "<Configure>",

            self._canvas_resize

        )

    # =====================================================
    # EVENTOS
    # =====================================================

    def _board_configure(

        self,

        event

    ):

        self.canvas.configure(

            scrollregion=self.canvas.bbox("all")

        )

    def _canvas_resize(

        self,

        event

    ):

        self.canvas.itemconfigure(

            self.window,

            height=event.height

        )

    # =====================================================
    # COLUMNAS
    # =====================================================

    def create_columns(self):

        estados = [

            ("Pendientes", STATUS_PENDING),

            ("En curso", STATUS_PROGRESS),

            ("Bloqueadas", STATUS_BLOCKED),

            ("Finalizadas", STATUS_DONE)

        ]

        for columna, (titulo, estado) in enumerate(estados):

            panel = KanbanColumn(

                self.board,

                titulo,

                estado

            )

            panel.grid(

                row=0,

                column=columna,

                padx=8,

                pady=5,

                sticky="ns"

            )

            panel.set_callbacks(

                click=self.card_clicked,

                double_click=self.card_double_clicked,

                drag=self.card_drag

            )

            self.columns[estado] = panel

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

        self.refresh()

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        for column in self.columns.values():

            column.clear()

        for task in self.tasks:

            column = self.columns.get(

                task.estado

            )

            if column:

                column.add_card(task)

    # =====================================================
    # ORDENAR
    # =====================================================

    def sort_all(self):

        for column in self.columns.values():

            column.sort_cards()

    # =====================================================
    # CLICK
    # =====================================================

    def card_clicked(

        self,

        task

    ):

        self.selected_task = task

    # =====================================================
    # DOBLE CLICK
    # =====================================================

    def card_double_clicked(

        self,

        task

    ):

        self.selected_task = task

        if self.task_open_callback:

            self.task_open_callback(

                task.id

            )

    # =====================================================
    # DRAG
    # =====================================================

    def card_drag(

        self,

        action,

        card,

        event

    ):

        """
        Implementación completa de Drag & Drop
        en la siguiente parte.
        """

        pass
            
            
            
            
            
            
            
            
