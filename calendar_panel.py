"""
=========================================================
Task Planner Pro
calendar_panel.py
=========================================================
Panel Calendario
=========================================================
"""

from __future__ import annotations

import calendar
import tkinter as tk

from datetime import datetime
from tkinter import ttk

from tkcalendar import Calendar

from config import (
    DATE_FORMAT,
    STATUS_PENDING,
    STATUS_PROGRESS,
    STATUS_BLOCKED,
    STATUS_DONE
)


class CalendarPanel(ttk.Frame):
    """
    Panel de calendario.

    Responsabilidades:

        • Mostrar calendario mensual.
        • Mostrar tareas del día seleccionado.
        • Permitir abrir una tarea.
        • Marcar visualmente días con tareas.

    NO realiza cálculos.
    NO accede a Excel.
    NO modifica datos.
    """

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self, parent):

        super().__init__(parent)

        self.tasks = []

        self.selected_date = None

        self.task_open_callback = None

        self.task_change_callback = None

        self.month_changed_callback = None

        self._build_ui()

    # =====================================================
    # UI
    # =====================================================

    def _build_ui(self):

        self.columnconfigure(0, weight=3)

        self.columnconfigure(1, weight=2)

        self.rowconfigure(1, weight=1)

        self._create_toolbar()

        self._create_calendar()

        self._create_task_panel()

    # =====================================================
    # TOOLBAR
    # =====================================================

    def _create_toolbar(self):

        toolbar = ttk.Frame(self)

        toolbar.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            toolbar,
            text="Calendario",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        ttk.Button(
            toolbar,
            text="Hoy",
            command=self.goto_today
        ).pack(side="right", padx=2)

        ttk.Button(
            toolbar,
            text="Actualizar",
            command=self.refresh
        ).pack(side="right", padx=2)

    # =====================================================
    # CALENDARIO
    # =====================================================

    def _create_calendar(self):

        frame = ttk.Frame(self)

        frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=(0, 10)
        )

        self.calendar = Calendar(
            frame,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
            firstweekday="monday"
        )

        self.calendar.pack(
            fill="both",
            expand=True
        )

        self.calendar.bind(
            "<<CalendarSelected>>",
            self._day_selected
        )

        self.calendar.bind(
            "<<CalendarMonthChanged>>",
            self._month_changed
        )

    # =====================================================
    # PANEL DERECHO
    # =====================================================

    def _create_task_panel(self):

        panel = ttk.LabelFrame(
            self,
            text="Tareas del día",
            padding=8
        )

        panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=(0, 10)
        )

        panel.columnconfigure(0, weight=1)

        panel.rowconfigure(0, weight=1)

        self.task_list = ttk.Treeview(
            panel,
            columns=(
                "Estado",
                "Prioridad",
                "Título"
            ),
            show="headings",
            height=18
        )

        self.task_list.heading(
            "Estado",
            text="Estado"
        )

        self.task_list.heading(
            "Prioridad",
            text="Prioridad"
        )

        self.task_list.heading(
            "Título",
            text="Título"
        )

        self.task_list.column(
            "Estado",
            width=90,
            anchor="center"
        )

        self.task_list.column(
            "Prioridad",
            width=80,
            anchor="center"
        )

        self.task_list.column(
            "Título",
            width=260
        )

        scrollbar = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.task_list.yview
        )

        self.task_list.configure(
            yscrollcommand=scrollbar.set
        )

        self.task_list.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.task_list.tag_configure(
            STATUS_PENDING,
            background="#FFF8CC"
        )

        self.task_list.tag_configure(
            STATUS_PROGRESS,
            background="#DDEEFF"
        )

        self.task_list.tag_configure(
            STATUS_BLOCKED,
            background="#FFD8D8"
        )

        self.task_list.tag_configure(
            STATUS_DONE,
            background="#DFF6DF"
        )

        self.task_list.bind(
            "<Double-1>",
            self._open_task
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

    def set_month_changed_callback(
        self,
        callback
    ):

        self.month_changed_callback = callback

    # =====================================================
    # CARGA
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

        self._mark_calendar_days()

        self._refresh_day_tasks()

    # =====================================================
    # IR A HOY
    # =====================================================

    def goto_today(self):

        self.calendar.selection_set(
            datetime.today()
        )

        self._day_selected()

    # =====================================================
    # DÍA SELECCIONADO
    # =====================================================

    def _day_selected(
        self,
        event=None
    ):

        self.selected_date = self.calendar.get_date()

        self._refresh_day_tasks()

    # =====================================================
    # CAMBIO DE MES
    # =====================================================

    def _month_changed(
        self,
        event=None
    ):

        if self.month_changed_callback:

            self.month_changed_callback(
                self.calendar.get_displayed_month()
            )

        self._mark_calendar_days()
        
    # =====================================================
    # ACTUALIZAR TAREAS DEL DÍA
    # =====================================================

    def _refresh_day_tasks(self):

        self.task_list.delete(*self.task_list.get_children())

        if not self.selected_date:

            self.selected_date = self.calendar.get_date()

        tareas = []

        for task in self.tasks:

            if task.fecha_prevista == self.selected_date:

                tareas.append(task)

        tareas.sort(
            key=lambda x: (
                x.prioridad,
                x.titulo.lower()
            )
        )

        for task in tareas:

            self.task_list.insert(
                "",
                "end",
                iid=str(task.id),
                values=(
                    task.estado,
                    task.prioridad,
                    task.titulo
                ),
                tags=(task.estado,)
            )

    # =====================================================
    # MARCAR DÍAS CON TAREAS
    # =====================================================

    def _mark_calendar_days(self):

        try:

            self.calendar.calevent_remove("all")

        except Exception:

            pass

        for task in self.tasks:

            if not task.fecha_prevista:

                continue

            tag = self._calendar_tag(task)

            self.calendar.calevent_create(

                task.fecha_prevista,

                task.titulo,

                tag

            )

        self._configure_calendar_tags()

    # =====================================================
    # CONFIGURAR TAGS
    # =====================================================

    def _configure_calendar_tags(self):

        try:

            self.calendar.tag_config(
                "pending",
                background="#FFE082"
            )

            self.calendar.tag_config(
                "progress",
                background="#90CAF9"
            )

            self.calendar.tag_config(
                "blocked",
                background="#EF9A9A"
            )

            self.calendar.tag_config(
                "done",
                background="#A5D6A7"
            )

            self.calendar.tag_config(
                "overdue",
                background="#FF7043"
            )

        except Exception:

            pass

    # =====================================================
    # OBTENER TAG
    # =====================================================

    def _calendar_tag(self, task):

        if task.overdue:

            return "overdue"

        if task.estado == STATUS_PENDING:

            return "pending"

        if task.estado == STATUS_PROGRESS:

            return "progress"

        if task.estado == STATUS_BLOCKED:

            return "blocked"

        if task.estado == STATUS_DONE:

            return "done"

        return "pending"

    # =====================================================
    # ABRIR TAREA
    # =====================================================

    def _open_task(self, event=None):

        seleccion = self.task_list.selection()

        if not seleccion:

            return

        task_id = int(seleccion[0])

        if self.task_open_callback:

            self.task_open_callback(task_id)

    # =====================================================
    # OBTENER TAREA SELECCIONADA
    # =====================================================

    def get_selected_task_id(self):

        seleccion = self.task_list.selection()

        if not seleccion:

            return None

        return int(seleccion[0])

    # =====================================================
    # LIMPIAR PANEL
    # =====================================================

    def clear(self):

        self.tasks.clear()

        self.task_list.delete(

            *self.task_list.get_children()

        )

        try:

            self.calendar.calevent_remove("all")

        except Exception:

            pass

    # =====================================================
    # RESUMEN MENSUAL
    # =====================================================

    def month_summary(self):

        mes = self.calendar.get_displayed_month()

        total = 0

        pendientes = 0

        curso = 0

        bloqueadas = 0

        finalizadas = 0

        for task in self.tasks:

            if not task.fecha_prevista:

                continue

            try:

                fecha = datetime.strptime(
                    task.fecha_prevista,
                    DATE_FORMAT
                )

            except Exception:

                continue

            if (
                fecha.month != mes[0]
                or fecha.year != mes[1]
            ):

                continue

            total += 1

            if task.estado == STATUS_PENDING:

                pendientes += 1

            elif task.estado == STATUS_PROGRESS:

                curso += 1

            elif task.estado == STATUS_BLOCKED:

                bloqueadas += 1

            elif task.estado == STATUS_DONE:

                finalizadas += 1

        return {

            "total": total,

            "pending": pendientes,

            "progress": curso,

            "blocked": bloqueadas,

            "done": finalizadas

        }

    # =====================================================
    # IR A UNA FECHA
    # =====================================================

    def goto_date(self, date_string):

        try:

            fecha = datetime.strptime(
                date_string,
                DATE_FORMAT
            )

            self.calendar.selection_set(fecha)

            self.selected_date = date_string

            self._refresh_day_tasks()

        except Exception:

            pass

    # =====================================================
    # APLICAR FILTRO
    # =====================================================

    def filter_tasks(self, predicate):

        self.task_list.delete(
            *self.task_list.get_children()
        )

        for task in filter(predicate, self.tasks):

            self.task_list.insert(
                "",
                "end",
                iid=str(task.id),
                values=(
                    task.estado,
                    task.prioridad,
                    task.titulo
                ),
                tags=(task.estado,)
            )
            
    # =====================================================
    # CONTADORES
    # =====================================================

    def total_tasks(self):

        return len(self.tasks)

    def tasks_for_today(self):

        fecha = datetime.today().strftime(DATE_FORMAT)

        return [

            t

            for t in self.tasks

            if t.fecha_prevista == fecha

        ]

    def overdue_tasks(self):

        return [

            t

            for t in self.tasks

            if t.overdue

        ]

    # =====================================================
    # BUSCAR
    # =====================================================

    def find_task(self, task_id):

        for task in self.tasks:

            if task.id == task_id:

                return task

        return None

    # =====================================================
    # RECARGAR
    # =====================================================

    def reload(self, tasks):

        self.tasks = list(tasks)

        self.refresh()

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def change_status(

        self,

        task_id,

        status

    ):

        task = self.find_task(task_id)

        if task is None:

            return

        task.estado = status

        if self.task_change_callback:

            self.task_change_callback(task)

        self.refresh()

    # =====================================================
    # CAMBIAR FECHA
    # =====================================================

    def change_due_date(

        self,

        task_id,

        new_date

    ):

        task = self.find_task(task_id)

        if task is None:

            return

        task.fecha_prevista = new_date

        if self.task_change_callback:

            self.task_change_callback(task)

        self.refresh()

    # =====================================================
    # SIGUIENTE TAREA
    # =====================================================

    def next_task(self):

        items = self.task_list.get_children()

        if not items:

            return

        current = self.task_list.selection()

        if not current:

            self.task_list.selection_set(items[0])

            return

        index = items.index(current[0])

        if index < len(items) - 1:

            self.task_list.selection_set(

                items[index + 1]

            )

            self.task_list.focus(

                items[index + 1]

            )

            self.task_list.see(

                items[index + 1]

            )

    # =====================================================
    # TAREA ANTERIOR
    # =====================================================

    def previous_task(self):

        items = self.task_list.get_children()

        if not items:

            return

        current = self.task_list.selection()

        if not current:

            self.task_list.selection_set(items[0])

            return

        index = items.index(current[0])

        if index > 0:

            self.task_list.selection_set(

                items[index - 1]

            )

            self.task_list.focus(

                items[index - 1]

            )

            self.task_list.see(

                items[index - 1]

            )

    # =====================================================
    # EXPANDIR DÍA
    # =====================================================

    def show_day_summary(self):

        resumen = self.month_summary()

        texto = (
            f"Tareas del mes\n\n"
            f"Total: {resumen['total']}\n"
            f"Pendientes: {resumen['pending']}\n"
            f"En curso: {resumen['progress']}\n"
            f"Bloqueadas: {resumen['blocked']}\n"
            f"Finalizadas: {resumen['done']}"
        )

        from tkinter import messagebox

        messagebox.showinfo(

            "Resumen",

            texto

        )

    # =====================================================
    # EXPORTAR MES
    # =====================================================

    def export_month(self):

        if not hasattr(self, "export_callback"):

            return

        mes = self.calendar.get_displayed_month()

        self.export_callback(

            mes[0],

            mes[1]

        )

    # =====================================================
    # CALLBACK EXPORT
    # =====================================================

    def set_export_callback(

        self,

        callback

    ):

        self.export_callback = callback

    # =====================================================
    # REFRESCO AUTOMÁTICO
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
    # REDIMENSIONADO
    # =====================================================

    def on_resize(

        self,

        event=None

    ):

        self.update_idletasks()

    # =====================================================
    # DESTRUCTOR
    # =====================================================

    def destroy(self):

        try:

            self.calendar.calevent_remove("all")

        except Exception:

            pass

        self.tasks.clear()

        super().destroy()
            

        
        
        
        
        
        
    
