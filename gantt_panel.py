"""
Task Planner Pro
gantt_panel.py
Panel Gantt
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk


class GanttPanel(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.tasks = []

        self.canvas = tk.Canvas(self, background="white")
        self.hbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(
            xscrollcommand=self.hbar.set,
            yscrollcommand=self.vbar.set
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def load_tasks(self, tasks):
        self.tasks = tasks
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        if not self.tasks:
            self.canvas.create_text(
                20, 20,
                anchor="nw",
                text="No hay tareas para mostrar."
            )
            return

        y = 40

        for task in self.tasks:

            try:
                inicio = datetime.strptime(task.fecha_inicio, "%d/%m/%Y")
                fin = datetime.strptime(task.fecha_prevista, "%d/%m/%Y")
                dias = max((fin - inicio).days, 1)
            except Exception:
                dias = 1

            color = {
                "Pendiente": "#FFD966",
                "En curso": "#5B9BD5",
                "Bloqueada": "#E06666",
                "Finalizada": "#70AD47"
            }.get(getattr(task, "estado", ""), "#A5A5A5")

            self.canvas.create_text(
                10,
                y + 10,
                anchor="w",
                text=f"[{task.id}] {task.titulo}"
            )

            x = 250
            ancho = dias * 12

            self.canvas.create_rectangle(
                x,
                y,
                x + ancho,
                y + 20,
                fill=color,
                outline="black"
            )

            progreso = getattr(task, "avance", 0)

            self.canvas.create_rectangle(
                x,
                y,
                x + (ancho * progreso / 100),
                y + 20,
                fill="#00B050",
                outline=""
            )

            self.canvas.create_text(
                x + ancho + 10,
                y + 10,
                anchor="w",
                text=f"{progreso}%"
            )

            y += 35

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom(self, factor):
        self.canvas.scale("all", 0, 0, factor, 1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
