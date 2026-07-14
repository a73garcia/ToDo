"""
Task Planner Pro
dashboard_panel.py
Panel de indicadores
"""

import tkinter as tk
from tkinter import ttk


class DashboardPanel(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.cards = {}
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        for title in (
            "Pendientes",
            "En curso",
            "Bloqueadas",
            "Finalizadas",
            "Retrasadas",
            "Total"
        ):
            frame = ttk.LabelFrame(top, text=title)
            frame.pack(side="left", fill="both", expand=True, padx=4)

            lbl = ttk.Label(frame, text="0", font=("Segoe UI",18,"bold"))
            lbl.pack(pady=15)

            self.cards[title] = lbl

        prog = ttk.LabelFrame(self, text="Avance global")
        prog.pack(fill="x", padx=10, pady=10)

        self.progress = ttk.Progressbar(prog, maximum=100)
        self.progress.pack(fill="x", padx=10, pady=10)

        self.progress_text = ttk.Label(prog, text="0 %")
        self.progress_text.pack(pady=(0,10))

    def update_metrics(self, metrics):
        mapping = {
            "Pendientes":"pendientes",
            "En curso":"en_curso",
            "Bloqueadas":"bloqueadas",
            "Finalizadas":"finalizadas",
            "Retrasadas":"retrasadas",
            "Total":"total"
        }

        for title,key in mapping.items():
            self.cards[title].config(text=str(metrics.get(key,0)))

        value = metrics.get("avance_global",0)
        self.progress["value"] = value
        self.progress_text.config(text=f"{value}%")

    def clear(self):
        self.update_metrics({})
