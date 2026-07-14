from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config import *


class DashboardPanel(ttk.Frame):
    """
    Dashboard principal de la aplicación.

    Este panel NO realiza cálculos.
    Todos los datos proceden de MetricsManager.
    """

    def __init__(self, parent, metrics_manager):

        super().__init__(parent)

        self.metrics = metrics_manager

        self.cards = {}

        self._create_layout()

        self.refresh()

    # =====================================================
    # LAYOUT
    # =====================================================

    def _create_layout(self):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._create_toolbar()

        self._create_cards()

        self._create_body()

    # =====================================================
    # TOOLBAR
    # =====================================================

    def _create_toolbar(self):

        toolbar = ttk.Frame(self)

        toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10,5)
        )

        ttk.Label(
            toolbar,
            text="Dashboard",
            font=("Segoe UI",18,"bold")
        ).pack(side="left")

        ttk.Button(
            toolbar,
            text="Actualizar",
            command=self.refresh
        ).pack(side="right")

    # =====================================================
    # KPI CARDS
    # =====================================================

    def _create_cards(self):

        frame = ttk.Frame(self)

        frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        frame.columnconfigure((0,1,2,3,4,5),weight=1)

        tarjetas = [

            ("Total","0"),

            ("Pendientes","0"),

            ("En curso","0"),

            ("Bloqueadas","0"),

            ("Finalizadas","0"),

            ("Avance","0 %")

        ]

        for columna,(titulo,valor) in enumerate(tarjetas):

            card = ttk.LabelFrame(
                frame,
                text=titulo,
                padding=10
            )

            card.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=4
            )

            label = ttk.Label(
                card,
                text=valor,
                font=("Segoe UI",20,"bold")
            )

            label.pack()

            self.cards[titulo]=label

    # =====================================================
    # BODY
    # =====================================================

    def _create_body(self):

        body = ttk.PanedWindow(
            self,
            orient=tk.HORIZONTAL
        )

        body.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.left = ttk.Frame(body)

        self.right = ttk.Frame(body)

        body.add(self.left,weight=3)

        body.add(self.right,weight=1)

        self._create_charts()

        self._create_lists()
        
    # =====================================================
    # CHARTS
    # =====================================================

    def _create_charts(self):

        charts = ttk.Frame(self.left)

        charts.pack(
            fill="both",
            expand=True
        )

        charts.columnconfigure(0, weight=1)
        charts.columnconfigure(1, weight=1)

        # -------------------------------
        # Estados
        # -------------------------------

        frame1 = ttk.LabelFrame(
            charts,
            text="Estado de tareas",
            padding=5
        )

        frame1.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,5)
        )

        self.figure_status = Figure(
            figsize=(4,3),
            dpi=100
        )

        self.ax_status = self.figure_status.add_subplot(111)

        self.canvas_status = FigureCanvasTkAgg(
            self.figure_status,
            frame1
        )

        self.canvas_status.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # -------------------------------
        # Prioridades
        # -------------------------------

        frame2 = ttk.LabelFrame(
            charts,
            text="Prioridades",
            padding=5
        )

        frame2.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,0)
        )

        self.figure_priority = Figure(
            figsize=(4,3),
            dpi=100
        )

        self.ax_priority = self.figure_priority.add_subplot(111)

        self.canvas_priority = FigureCanvasTkAgg(
            self.figure_priority,
            frame2
        )

        self.canvas_priority.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # PANEL DERECHO
    # =====================================================

    def _create_lists(self):

        self._create_deadlines()

        self._create_risks()

        self._create_activity()

    # =====================================================
    # VENCIMIENTOS
    # =====================================================

    def _create_deadlines(self):

        frame = ttk.LabelFrame(
            self.right,
            text="Próximos vencimientos",
            padding=5
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=(0,10)
        )

        self.deadlines = tk.Listbox(
            frame,
            height=8
        )

        self.deadlines.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # RIESGOS
    # =====================================================

    def _create_risks(self):

        frame = ttk.LabelFrame(
            self.right,
            text="Tareas críticas",
            padding=5
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=(0,10)
        )

        self.risks = tk.Listbox(
            frame,
            height=8
        )

        self.risks.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # ACTIVIDAD
    # =====================================================

    def _create_activity(self):

        frame = ttk.LabelFrame(
            self.right,
            text="Actividad reciente",
            padding=5
        )

        frame.pack(
            fill="both",
            expand=True
        )

        self.activity = tk.Listbox(
            frame,
            height=10
        )

        self.activity.pack(
            fill="both",
            expand=True
        )
        
    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        datos = self.metrics.dashboard()

        self._update_cards(datos)

        self._update_charts(datos)

        self._update_lists(datos)

    # =====================================================
    # KPI CARDS
    # =====================================================

    def _update_cards(self, datos):

        self.cards["Total"].config(
            text=datos["total"]
        )

        self.cards["Pendientes"].config(
            text=datos["pending"]
        )

        self.cards["En curso"].config(
            text=datos["progress"]
        )

        self.cards["Bloqueadas"].config(
            text=datos["blocked"]
        )

        self.cards["Finalizadas"].config(
            text=datos["done"]
        )

        self.cards["Avance"].config(
            text=f'{datos["progress_percent"]:.1f}%'
        )
        
    # =====================================================
    # ACTUALIZAR GRÁFICOS
    # =====================================================

    def _update_charts(self, datos):

        # -----------------------------
        # Estados
        # -----------------------------

        self.ax_status.clear()

        estados = datos["charts"]["status"]

        self.ax_status.pie(

            estados["values"],

            labels=estados["labels"],

            autopct="%1.1f%%",

            startangle=90

        )

        self.ax_status.set_title(

            "Estado"

        )

        self.canvas_status.draw()

        # -----------------------------
        # Prioridades
        # -----------------------------

        self.ax_priority.clear()

        prioridades = datos["charts"]["priority"]

        self.ax_priority.bar(

            prioridades["labels"],

            prioridades["values"]

        )

        self.ax_priority.set_title(

            "Prioridades"

        )

        self.canvas_priority.draw()

    # =====================================================
    # ACTUALIZAR LISTAS
    # =====================================================

    def _update_lists(self, datos):

        self.deadlines.delete(0, tk.END)

        self.risks.delete(0, tk.END)

        self.activity.delete(0, tk.END)

        # -----------------------------
        # Próximos vencimientos
        # -----------------------------

        for item in datos["deadlines"]:

            self.deadlines.insert(

                tk.END,

                item

            )

        # -----------------------------
        # Riesgos
        # -----------------------------

        for item in datos["risks"]:

            self.risks.insert(

                tk.END,

                item

            )

        # -----------------------------
        # Actividad
        # -----------------------------

        for item in datos["activity"]:

            self.activity.insert(

                tk.END,

                item

            )

    # =====================================================
    # LIMPIAR DASHBOARD
    # =====================================================

    def clear(self):

        for card in self.cards.values():

            card.config(text="0")

        self.deadlines.delete(0, tk.END)

        self.risks.delete(0, tk.END)

        self.activity.delete(0, tk.END)

        self.ax_status.clear()

        self.ax_priority.clear()

        self.canvas_status.draw()

        self.canvas_priority.draw()

    # =====================================================
    # CAMBIAR METRICS MANAGER
    # =====================================================

    def set_metrics_manager(self, manager):

        self.metrics = manager

        self.refresh()

    # =====================================================
    # REDIMENSIONADO
    # =====================================================

    def on_resize(self, event=None):

        self.canvas_status.draw_idle()

        self.canvas_priority.draw_idle()

    # =====================================================
    # EXPORTAR IMAGEN
    # =====================================================

    def export_dashboard(self, filename):

        self.figure_status.savefig(

            filename.replace(".png", "_estado.png"),

            dpi=150,

            bbox_inches="tight"

        )

        self.figure_priority.savefig(

            filename.replace(".png", "_prioridad.png"),

            dpi=150,

            bbox_inches="tight"

        )

    # =====================================================
    # AUTOREFRESH
    # =====================================================

    def start_autorefresh(self, interval=60000):

        self.refresh()

        self.after(

            interval,

            lambda: self.start_autorefresh(interval)

        )

    # =====================================================
    # DESTRUCTOR
    # =====================================================

    def destroy(self):

        try:

            self.figure_status.clear()

            self.figure_priority.clear()

        except Exception:

            pass

        super().destroy()
        
        
        
        
        
        
        
        
        
