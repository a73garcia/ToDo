import calendar
from datetime import datetime
import tkinter as tk
from tkinter import ttk


class CalendarPanel(ttk.Frame):

    def __init__(self, master, on_date_selected=None):
        super().__init__(master)
        self.on_date_selected = on_date_selected
        self.current = datetime.today()
        self.task_dates = {}
        self._build()

    def _build(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=10)

        ttk.Button(header, text="◀", command=lambda: self.change_month(-1)).pack(side="left")

        self.title = ttk.Label(header, font=("Segoe UI", 12, "bold"))
        self.title.pack(side="left", expand=True)

        ttk.Button(header, text="▶", command=lambda: self.change_month(1)).pack(side="right")

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.draw()

    def load_tasks(self, tasks):
        self.task_dates = {}
        for t in tasks:
            if getattr(t, "fecha_prevista", ""):
                self.task_dates.setdefault(t.fecha_prevista, []).append(t)
        self.draw()

    def change_month(self, delta):
        y = self.current.year
        m = self.current.month + delta
        if m < 1:
            m = 12
            y -= 1
        elif m > 12:
            m = 1
            y += 1
        self.current = self.current.replace(year=y, month=m, day=1)
        self.draw()

    def draw(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.title.config(text=self.current.strftime("%B %Y"))

        days = ["L","M","X","J","V","S","D"]
        for c,d in enumerate(days):
            ttk.Label(self.grid_frame, text=d).grid(row=0,column=c,padx=2,pady=2)

        cal = calendar.Calendar(firstweekday=0)
        row = 1
        for week in cal.monthdayscalendar(self.current.year, self.current.month):
            for col, day in enumerate(week):
                if day == 0:
                    ttk.Label(self.grid_frame, text="").grid(row=row,column=col)
                    continue

                date_str = f"{day:02d}/{self.current.month:02d}/{self.current.year}"
                has_tasks = date_str in self.task_dates

                btn = tk.Button(
                    self.grid_frame,
                    text=str(day),
                    width=4,
                    bg="#C8F7C5" if has_tasks else "white",
                    command=lambda d=date_str: self.select_date(d)
                )
                btn.grid(row=row,column=col,padx=1,pady=1)
            row += 1

    def select_date(self, date_string):
        if self.on_date_selected:
            self.on_date_selected(date_string)
