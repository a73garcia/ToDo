"""
Task Planner Pro
kanban_panel.py
Tablero Kanban
"""

import tkinter as tk
from tkinter import ttk


class KanbanPanel(ttk.Frame):

    COLUMNS = (
        "Pendiente",
        "En curso",
        "Bloqueada",
        "Finalizada",
    )

    def __init__(self, master, on_task_selected=None):
        super().__init__(master)
        self.on_task_selected = on_task_selected
        self.lists = {}
        self.tasks = []
        self._build()

    def _build(self):
        for idx, title in enumerate(self.COLUMNS):
            frame = ttk.LabelFrame(self, text=title)
            frame.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)

            lb = tk.Listbox(frame, activestyle="none")
            lb.pack(fill="both", expand=True, padx=5, pady=5)
            lb.bind("<<ListboxSelect>>",
                    lambda e, s=title: self._select(s))

            self.lists[title] = lb
            self.columnconfigure(idx, weight=1)

        self.rowconfigure(0, weight=1)

    def load_tasks(self, tasks):
        self.tasks = tasks

        for lb in self.lists.values():
            lb.delete(0, "end")

        for task in tasks:
            estado = getattr(task, "estado", "Pendiente")
            if estado not in self.lists:
                estado = "Pendiente"

            texto = f"[{task.id}] {task.titulo}"
            self.lists[estado].insert("end", texto)

    def _select(self, estado):
        lb = self.lists[estado]

        if not lb.curselection():
            return

        texto = lb.get(lb.curselection()[0])

        try:
            task_id = int(texto.split("]")[0][1:])
        except Exception:
            return

        tarea = next(
            (t for t in self.tasks if t.id == task_id),
            None
        )

        if self.on_task_selected and tarea:
            self.on_task_selected(tarea)

    def move_task(self, task_id, new_status):
        for t in self.tasks:
            if t.id == task_id:
                t.estado = new_status
                break

        self.load_tasks(self.tasks)
