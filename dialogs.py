"""
Task Planner Pro
dialogs.py
Diálogo de creación y edición de tareas
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TaskDialog(tk.Toplevel):

    def __init__(self, master, task=None):
        super().__init__(master)

        self.title("Tarea")
        self.resizable(False, False)
        self.result = None

        self.vars = {
            "titulo": tk.StringVar(value=getattr(task, "titulo", "")),
            "responsable": tk.StringVar(value=getattr(task, "responsable", "")),
            "estado": tk.StringVar(value=getattr(task, "estado", "Pendiente")),
            "prioridad": tk.StringVar(value=getattr(task, "prioridad", "Media")),
            "categoria": tk.StringVar(value=getattr(task, "categoria", "")),
            "inicio": tk.StringVar(value=getattr(task, "fecha_inicio", "")),
            "prevista": tk.StringVar(value=getattr(task, "fecha_prevista", "")),
            "avance": tk.IntVar(value=getattr(task, "avance", 0)),
        }

        self._build(task)

        self.grab_set()
        self.transient(master)

    def _build(self, task):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        fields = [
            ("Título", "titulo"),
            ("Responsable", "responsable"),
            ("Categoría", "categoria"),
            ("Inicio", "inicio"),
            ("Vencimiento", "prevista"),
        ]

        row = 0
        for text, key in fields:
            ttk.Label(frm, text=text).grid(row=row, column=0, sticky="w", pady=4)
            ttk.Entry(frm, textvariable=self.vars[key], width=40).grid(row=row, column=1, pady=4)
            row += 1

        ttk.Label(frm, text="Estado").grid(row=row, column=0, sticky="w")
        ttk.Combobox(
            frm,
            textvariable=self.vars["estado"],
            values=["Pendiente", "En curso", "Bloqueada", "Finalizada"],
            state="readonly"
        ).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(frm, text="Prioridad").grid(row=row, column=0, sticky="w")
        ttk.Combobox(
            frm,
            textvariable=self.vars["prioridad"],
            values=["Baja", "Media", "Alta", "Crítica"],
            state="readonly"
        ).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(frm, text="Avance").grid(row=row, column=0, sticky="w")
        ttk.Scale(frm, from_=0, to=100, variable=self.vars["avance"], orient="horizontal").grid(
            row=row, column=1, sticky="ew", pady=4
        )
        row += 1

        ttk.Label(frm, text="Descripción").grid(row=row, column=0, sticky="nw")
        self.txt_desc = tk.Text(frm, width=40, height=5)
        self.txt_desc.grid(row=row, column=1, pady=4)
        if task and getattr(task, "descripcion", ""):
            self.txt_desc.insert("1.0", task.descripcion)
        row += 1

        buttons = ttk.Frame(frm)
        buttons.grid(row=row, column=0, columnspan=2, pady=10)

        ttk.Button(buttons, text="Aceptar", command=self.accept).pack(side="left", padx=5)
        ttk.Button(buttons, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

    def accept(self):
        if not self.vars["titulo"].get().strip():
            messagebox.showwarning("Validación", "El título es obligatorio.")
            return

        self.result = {
            "titulo": self.vars["titulo"].get().strip(),
            "descripcion": self.txt_desc.get("1.0", "end").strip(),
            "responsable": self.vars["responsable"].get().strip(),
            "estado": self.vars["estado"].get(),
            "prioridad": self.vars["prioridad"].get(),
            "categoria": self.vars["categoria"].get().strip(),
            "fecha_inicio": self.vars["inicio"].get().strip(),
            "fecha_prevista": self.vars["prevista"].get().strip(),
            "avance": int(self.vars["avance"].get()),
        }
        self.destroy()
