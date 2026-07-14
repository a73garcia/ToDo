import sys
import traceback
from tkinter import messagebox

from ui import MainWindow


def global_exception_handler(exc_type, exc_value, exc_traceback):
    error = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )

    print(error)

    try:
        messagebox.showerror(
            "Task Planner Pro",
            error
        )
    except Exception:
        pass


sys.excepthook = global_exception_handler


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
