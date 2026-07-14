from __future__ import annotations

import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from tkcalendar import DateEntry

from config import *

from models import Task


# ==========================================================
# DIÁLOGO BASE
# ==========================================================

class BaseDialog(tk.Toplevel):

    def __init__(

        self,

        parent,

        title=""

    ):

        super().__init__(parent)

        self.parent = parent

        self.result = None

        self.transient(parent)

        self.title(title)

        self.resizable(True, True)

        self.protocol(

            "WM_DELETE_WINDOW",

            self.cancel

        )

        self.bind(

            "<Escape>",

            lambda e: self.cancel()

        )

        self.bind(

            "<Return>",

            lambda e: self.accept()

        )

        self.grab_set()

    # =====================================================
    # BOTONES
    # =====================================================

    def create_buttons(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(

            fill="x",

            pady=10

        )

        ttk.Button(

            frame,

            text="Aceptar",

            command=self.accept

        ).pack(

            side="right",

            padx=5

        )

        ttk.Button(

            frame,

            text="Cancelar",

            command=self.cancel

        ).pack(

            side="right"

        )

    # =====================================================
    # ACEPTAR
    # =====================================================

    def accept(self):

        self.destroy()

    # =====================================================
    # CANCELAR
    # =====================================================

    def cancel(self):

        self.result = None

        self.destroy()


# ==========================================================
# DIÁLOGO DE TAREA
# ==========================================================

class TaskDialog(BaseDialog):

    def __init__(

        self,

        parent,

        task=None

    ):

        self.task = task or Task()

        super().__init__(

            parent,

            "Editar tarea"

        )

        self.build_ui()

        self.load_task()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def build_ui(self):

        container = ttk.Frame(

            self,

            padding=10

        )

        container.pack(

            fill="both",

            expand=True

        )

        self.notebook = ttk.Notebook(

            container

        )

        self.notebook.pack(

            fill="both",

            expand=True

        )

        self.general_page = ttk.Frame(

            self.notebook

        )

        self.detail_page = ttk.Frame(

            self.notebook

        )

        self.note_page = ttk.Frame(

            self.notebook

        )

        self.attach_page = ttk.Frame(

            self.notebook

        )

        self.notebook.add(

            self.general_page,

            text="General"

        )

        self.notebook.add(

            self.detail_page,

            text="Planificación"

        )

        self.notebook.add(

            self.note_page,

            text="Notas"

        )

        self.notebook.add(

            self.attach_page,

            text="Adjuntos"

        )

        self.create_general_page()

        self.create_detail_page()

        self.create_notes_page()

        self.create_attachment_page()

        self.create_buttons(

            container

        )
        
        
    # =====================================================
    # PÁGINA GENERAL
    # =====================================================

    def create_general_page(self):

        frame = ttk.Frame(
            self.general_page,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )

        for i in range(8):
            frame.rowconfigure(i, pad=8)

        frame.columnconfigure(1, weight=1)

        # ---------------------------------------------
        # TÍTULO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Título:"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.var_title = tk.StringVar()

        self.ent_title = ttk.Entry(
            frame,
            textvariable=self.var_title
        )

        self.ent_title.grid(
            row=0,
            column=1,
            columnspan=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # RESPONSABLE
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Responsable:"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.var_owner = tk.StringVar()

        self.cmb_owner = ttk.Combobox(
            frame,
            textvariable=self.var_owner
        )

        self.cmb_owner.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # PROYECTO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Proyecto:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(15,0)
        )

        self.var_project = tk.StringVar()

        self.cmb_project = ttk.Combobox(
            frame,
            textvariable=self.var_project
        )

        self.cmb_project.grid(
            row=1,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # ESTADO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Estado:"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.var_status = tk.StringVar()

        self.cmb_status = ttk.Combobox(
            frame,
            textvariable=self.var_status,
            values=TASK_STATUS,
            state="readonly"
        )

        self.cmb_status.grid(
            row=2,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # PRIORIDAD
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Prioridad:"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(15,0)
        )

        self.var_priority = tk.StringVar()

        self.cmb_priority = ttk.Combobox(
            frame,
            textvariable=self.var_priority,
            values=TASK_PRIORITY,
            state="readonly"
        )

        self.cmb_priority.grid(
            row=2,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # CATEGORÍA
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Categoría:"
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        self.var_category = tk.StringVar()

        self.ent_category = ttk.Entry(
            frame,
            textvariable=self.var_category
        )

        self.ent_category.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # RIESGO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Riesgo:"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=(15,0)
        )

        self.var_risk = tk.StringVar()

        self.cmb_risk = ttk.Combobox(
            frame,
            textvariable=self.var_risk,
            values=TASK_RISK,
            state="readonly"
        )

        self.cmb_risk.grid(
            row=3,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # ETIQUETAS
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Etiquetas:"
        ).grid(
            row=4,
            column=0,
            sticky="nw"
        )

        self.txt_tags = tk.Text(
            frame,
            height=3,
            wrap="word"
        )

        self.txt_tags.grid(
            row=4,
            column=1,
            columnspan=3,
            sticky="nsew"
        )

        # ---------------------------------------------
        # DESCRIPCIÓN
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Descripción:"
        ).grid(
            row=5,
            column=0,
            sticky="nw"
        )

        self.txt_description = tk.Text(
            frame,
            height=8,
            wrap="word"
        )

        self.txt_description.grid(
            row=5,
            column=1,
            columnspan=3,
            sticky="nsew"
        )

        # ---------------------------------------------
        # AVANCE
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Avance:"
        ).grid(
            row=6,
            column=0,
            sticky="w"
        )

        self.var_progress = tk.IntVar()

        self.scale_progress = ttk.Scale(
            frame,
            from_=0,
            to=100,
            variable=self.var_progress,
            orient="horizontal",
            command=self._progress_changed
        )

        self.scale_progress.grid(
            row=6,
            column=1,
            columnspan=2,
            sticky="ew"
        )

        self.lbl_progress = ttk.Label(
            frame,
            text="0%"
        )

        self.lbl_progress.grid(
            row=6,
            column=3,
            sticky="e"
        )

        # ---------------------------------------------
        # FAVORITA
        # ---------------------------------------------

        self.var_favorite = tk.BooleanVar()

        ttk.Checkbutton(
            frame,
            text="Marcar como favorita",
            variable=self.var_favorite
        ).grid(
            row=7,
            column=1,
            sticky="w"
        )

    # =====================================================
    # CAMBIO DE PROGRESO
    # =====================================================

    def _progress_changed(self, value):

        porcentaje = int(float(value))

        self.lbl_progress.configure(
            text=f"{porcentaje}%"
        )

        if porcentaje >= 100:
            self.var_status.set(STATUS_DONE)

        elif porcentaje > 0 and self.var_status.get() == STATUS_PENDING:
            self.var_status.set(STATUS_PROGRESS)
            
            
    # =====================================================
    # PÁGINA PLANIFICACIÓN
    # =====================================================

    def create_detail_page(self):

        frame = ttk.Frame(
            self.detail_page,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        # ---------------------------------------------
        # FECHA CREACIÓN
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Fecha creación:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.date_created = DateEntry(
            frame,
            date_pattern="dd/mm/yyyy"
        )

        self.date_created.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # FECHA INICIO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Fecha inicio:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.date_start = DateEntry(
            frame,
            date_pattern="dd/mm/yyyy"
        )

        self.date_start.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # FECHA PREVISTA
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Fecha prevista:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.date_due = DateEntry(
            frame,
            date_pattern="dd/mm/yyyy"
        )

        self.date_due.grid(
            row=2,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # FECHA FINALIZACIÓN
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Fecha finalización:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.date_finished = DateEntry(
            frame,
            date_pattern="dd/mm/yyyy"
        )

        self.date_finished.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # HORAS ESTIMADAS
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Horas estimadas:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(20, 0)
        )

        self.var_estimated = tk.DoubleVar()

        ttk.Entry(
            frame,
            textvariable=self.var_estimated
        ).grid(
            row=0,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # HORAS REALES
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Horas reales:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(20, 0)
        )

        self.var_real = tk.DoubleVar()

        ttk.Entry(
            frame,
            textvariable=self.var_real
        ).grid(
            row=1,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # COSTE ESTIMADO
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Coste estimado:"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(20, 0)
        )

        self.var_cost_estimated = tk.DoubleVar()

        ttk.Entry(
            frame,
            textvariable=self.var_cost_estimated
        ).grid(
            row=2,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # COSTE REAL
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Coste real:"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=(20, 0)
        )

        self.var_cost_real = tk.DoubleVar()

        ttk.Entry(
            frame,
            textvariable=self.var_cost_real
        ).grid(
            row=3,
            column=3,
            sticky="ew"
        )

        # ---------------------------------------------
        # DESVIACIÓN
        # ---------------------------------------------

        ttk.Label(
            frame,
            text="Desviación:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(15, 5)
        )

        self.var_deviation = tk.DoubleVar()

        self.ent_deviation = ttk.Entry(
            frame,
            textvariable=self.var_deviation,
            state="readonly"
        )

        self.ent_deviation.grid(
            row=4,
            column=1,
            sticky="ew"
        )

        # ---------------------------------------------
        # BOTÓN RECALCULAR
        # ---------------------------------------------

        ttk.Button(
            frame,
            text="Recalcular",
            command=self.calculate_deviation
        ).grid(
            row=4,
            column=3,
            sticky="e"
        )

    # =====================================================
    # CALCULAR DESVIACIÓN
    # =====================================================

    def calculate_deviation(self):

        try:

            estimadas = self.var_estimated.get()

            reales = self.var_real.get()

            if estimadas <= 0:

                self.var_deviation.set(0)

                return

            porcentaje = (
                (reales - estimadas)
                / estimadas
            ) * 100

            self.var_deviation.set(
                round(
                    porcentaje,
                    2
                )
            )

        except Exception:

            self.var_deviation.set(0)
            
    # =====================================================
    # PÁGINA NOTAS
    # =====================================================

    def create_notes_page(self):

        frame = ttk.Frame(
            self.note_page,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Comentarios de la tarea",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.txt_comments = tk.Text(
            frame,
            wrap="word",
            undo=True
        )

        self.txt_comments.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.txt_comments.yview
        )

        scrollbar.grid(
            row=1,
            column=1,
            sticky="ns"
        )

        self.txt_comments.configure(
            yscrollcommand=scrollbar.set
        )

    # =====================================================
    # PÁGINA ADJUNTOS
    # =====================================================

    def create_attachment_page(self):

        frame = ttk.Frame(
            self.attach_page,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.attachment_list = ttk.Treeview(
            frame,
            columns=(
                "Nombre",
                "Ruta",
                "Tamaño"
            ),
            show="headings",
            height=10
        )

        self.attachment_list.heading(
            "Nombre",
            text="Nombre"
        )

        self.attachment_list.heading(
            "Ruta",
            text="Ruta"
        )

        self.attachment_list.heading(
            "Tamaño",
            text="Tamaño"
        )

        self.attachment_list.column(
            "Nombre",
            width=220
        )

        self.attachment_list.column(
            "Ruta",
            width=420
        )

        self.attachment_list.column(
            "Tamaño",
            width=90,
            anchor="e"
        )

        self.attachment_list.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.attachment_list.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.attachment_list.configure(
            yscrollcommand=scrollbar.set
        )

        buttons = ttk.Frame(frame)

        buttons.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(10, 0)
        )

        ttk.Button(
            buttons,
            text="Añadir",
            command=self.add_attachment
        ).pack(
            side="left"
        )

        ttk.Button(
            buttons,
            text="Eliminar",
            command=self.remove_attachment
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons,
            text="Abrir",
            command=self.open_attachment
        ).pack(
            side="left"
        )

    # =====================================================
    # AÑADIR ADJUNTO
    # =====================================================

    def add_attachment(self):

        fichero = filedialog.askopenfilename()

        if not fichero:
            return

        from pathlib import Path

        nombre = Path(fichero).name

        try:
            tamano = Path(fichero).stat().st_size
        except Exception:
            tamano = 0

        self.attachment_list.insert(
            "",
            "end",
            values=(
                nombre,
                fichero,
                tamano
            )
        )

    # =====================================================
    # ELIMINAR ADJUNTO
    # =====================================================

    def remove_attachment(self):

        seleccion = self.attachment_list.selection()

        if not seleccion:
            return

        self.attachment_list.delete(
            seleccion[0]
        )

    # =====================================================
    # ABRIR ADJUNTO
    # =====================================================

    def open_attachment(self):

        seleccion = self.attachment_list.selection()

        if not seleccion:
            return

        ruta = self.attachment_list.item(
            seleccion[0],
            "values"
        )[1]

        try:

            import os

            os.startfile(ruta)

        except Exception as ex:

            messagebox.showerror(
                "Adjunto",
                str(ex)
            )
            
            
    # =====================================================
    # CARGAR TAREA
    # =====================================================

    def load_task(self):

        task = self.task

        self.var_title.set(task.titulo)

        self.var_owner.set(task.responsable)

        self.var_project.set(task.proyecto)

        self.var_status.set(task.estado)

        self.var_priority.set(task.prioridad)

        self.var_category.set(task.categoria)

        self.var_risk.set(task.riesgo)

        self.var_progress.set(task.avance)

        self.var_favorite.set(task.favorita)

        self.var_estimated.set(task.horas_estimadas)

        self.var_real.set(task.horas_reales)

        self.var_cost_estimated.set(task.coste_estimado)

        self.var_cost_real.set(task.coste_real)

        self.var_deviation.set(task.porcentaje_desviacion)

        self.lbl_progress.configure(
            text=f"{task.avance}%"
        )

        self.txt_description.delete(
            "1.0",
            tk.END
        )

        self.txt_description.insert(
            "1.0",
            task.descripcion
        )

        self.txt_tags.delete(
            "1.0",
            tk.END
        )

        self.txt_tags.insert(
            "1.0",
            task.etiquetas
        )

        self.txt_comments.delete(
            "1.0",
            tk.END
        )

        self.txt_comments.insert(
            "1.0",
            task.comentarios
        )

        self._load_dates()

        self._load_attachments()

    # =====================================================
    # CARGAR FECHAS
    # =====================================================

    def _load_dates(self):

        try:

            if self.task.fecha_creacion:

                self.date_created.set_date(
                    datetime.strptime(
                        self.task.fecha_creacion,
                        DATE_FORMAT
                    )
                )

        except Exception:

            pass

        try:

            if self.task.fecha_inicio:

                self.date_start.set_date(
                    datetime.strptime(
                        self.task.fecha_inicio,
                        DATE_FORMAT
                    )
                )

        except Exception:

            pass

        try:

            if self.task.fecha_prevista:

                self.date_due.set_date(
                    datetime.strptime(
                        self.task.fecha_prevista,
                        DATE_FORMAT
                    )
                )

        except Exception:

            pass

        try:

            if self.task.fecha_finalizacion:

                self.date_finished.set_date(
                    datetime.strptime(
                        self.task.fecha_finalizacion,
                        DATE_FORMAT
                    )
                )

        except Exception:

            pass

    # =====================================================
    # CARGAR ADJUNTOS
    # =====================================================

    def _load_attachments(self):

        self.attachment_list.delete(
            *self.attachment_list.get_children()
        )

        for adjunto in self.task.adjuntos:

            self.attachment_list.insert(
                "",
                "end",
                values=(
                    adjunto.nombre,
                    adjunto.ruta,
                    adjunto.tamano
                )
            )

    # =====================================================
    # VALIDAR
    # =====================================================

    def validate(self):

        if not self.var_title.get().strip():

            messagebox.showwarning(
                "Validación",
                "Debe indicar un título."
            )

            self.notebook.select(
                self.general_page
            )

            self.ent_title.focus_set()

            return False

        if self.var_progress.get() < 0:

            return False

        if self.var_progress.get() > 100:

            return False

        return True

    # =====================================================
    # GUARDAR
    # =====================================================

    def save_task(self):

        self.task.titulo = self.var_title.get().strip()

        self.task.descripcion = self.txt_description.get(
            "1.0",
            tk.END
        ).strip()

        self.task.responsable = self.var_owner.get()

        self.task.estado = self.var_status.get()

        self.task.prioridad = self.var_priority.get()

        self.task.categoria = self.var_category.get()

        self.task.proyecto = self.var_project.get()

        self.task.etiquetas = self.txt_tags.get(
            "1.0",
            tk.END
        ).strip()

        self.task.riesgo = self.var_risk.get()

        self.task.avance = int(
            self.var_progress.get()
        )

        self.task.favorita = self.var_favorite.get()

        self.task.horas_estimadas = self.var_estimated.get()

        self.task.horas_reales = self.var_real.get()

        self.task.coste_estimado = self.var_cost_estimated.get()

        self.task.coste_real = self.var_cost_real.get()

        self.task.porcentaje_desviacion = self.var_deviation.get()

        self.task.comentarios = self.txt_comments.get(
            "1.0",
            tk.END
        ).strip()

        self.task.fecha_creacion = self.date_created.get()

        self.task.fecha_inicio = self.date_start.get()

        self.task.fecha_prevista = self.date_due.get()

        self.task.fecha_finalizacion = self.date_finished.get()

        self.task.fecha_modificacion = datetime.now().strftime(
            DATETIME_FORMAT
        )

        self.task.adjuntos.clear()

        for item in self.attachment_list.get_children():

            valores = self.attachment_list.item(
                item,
                "values"
            )

            self.task.add_attachment(

                valores[0],

                valores[1],

                int(valores[2])

            )

    # =====================================================
    # ACEPTAR
    # =====================================================

    def accept(self):

        if not self.validate():

            return

        self.save_task()

        self.result = self.task

        super().accept()
            
            
# ==========================================================
# HISTORIAL
# ==========================================================

    def refresh_history(self):

        if not hasattr(self, "history_tree"):

            return

        self.history_tree.delete(

            *self.history_tree.get_children()

        )

        for item in self.task.historial:

            self.history_tree.insert(

                "",

                "end",

                values=(

                    item.fecha,

                    item.usuario,

                    item.avance,

                    item.comentario

                )

            )

    # =====================================================
    # AÑADIR ENTRADA AL HISTORIAL
    # =====================================================

    def add_history_entry(

        self,

        usuario,

        comentario,

        avance=None

    ):

        if avance is None:

            avance = self.var_progress.get()

        self.task.add_history(

            usuario,

            avance,

            comentario

        )

        self.refresh_history()

    # =====================================================
    # LIMPIAR HISTORIAL
    # =====================================================

    def clear_history(self):

        if not messagebox.askyesno(

            "Historial",

            "¿Eliminar todo el historial?"

        ):

            return

        self.task.historial.clear()

        self.refresh_history()

    # =====================================================
    # RESTABLECER
    # =====================================================

    def reset_fields(self):

        self.var_title.set("")

        self.var_owner.set("")

        self.var_project.set("")

        self.var_status.set(STATUS_PENDING)

        self.var_priority.set(PRIORITY_MEDIUM)

        self.var_category.set("")

        self.var_risk.set("Normal")

        self.var_progress.set(0)

        self.var_favorite.set(False)

        self.var_estimated.set(0)

        self.var_real.set(0)

        self.var_cost_estimated.set(0)

        self.var_cost_real.set(0)

        self.var_deviation.set(0)

        self.lbl_progress.configure(

            text="0%"

        )

        self.txt_description.delete(

            "1.0",

            tk.END

        )

        self.txt_tags.delete(

            "1.0",

            tk.END

        )

        self.txt_comments.delete(

            "1.0",

            tk.END

        )

        self.attachment_list.delete(

            *self.attachment_list.get_children()

        )

        if hasattr(self, "history_tree"):

            self.history_tree.delete(

                *self.history_tree.get_children()

            )

    # =====================================================
    # DUPLICAR TAREA
    # =====================================================

    def duplicate(self):

        nueva = self.task.clone()

        nueva.id = 0

        nueva.titulo = f"{nueva.titulo} (Copia)"

        nueva.fecha_creacion = datetime.now().strftime(

            DATE_FORMAT

        )

        nueva.fecha_modificacion = ""

        nueva.fecha_finalizacion = ""

        self.result = nueva

        self.destroy()

    # =====================================================
    # SOLO LECTURA
    # =====================================================

    def set_readonly(

        self,

        readonly=True

    ):

        estado = "disabled" if readonly else "normal"

        readonly_state = "readonly" if readonly else "normal"

        self.ent_title.configure(state=estado)

        self.cmb_owner.configure(state=readonly_state)

        self.cmb_project.configure(state=readonly_state)

        self.cmb_status.configure(state=readonly_state)

        self.cmb_priority.configure(state=readonly_state)

        self.cmb_risk.configure(state=readonly_state)

        self.ent_category.configure(state=estado)

        self.scale_progress.configure(state=estado)

        self.txt_description.configure(state=estado)

        self.txt_tags.configure(state=estado)

        self.txt_comments.configure(state=estado)

    # =====================================================
    # CENTRAR DIÁLOGO
    # =====================================================

    def center(self):

        self.update_idletasks()

        w = self.winfo_width()

        h = self.winfo_height()

        sw = self.winfo_screenwidth()

        sh = self.winfo_screenheight()

        x = (sw - w) // 2

        y = (sh - h) // 2

        self.geometry(

            f"{w}x{h}+{x}+{y}"

        )

    # =====================================================
    # MOSTRAR
    # =====================================================

    def show(self):

        self.center()

        self.wait_window()

        return self.result
        
        
        
        
