"""
app.py
Punto de entrada de la aplicación ToDo
Versión 0.1
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import webbrowser
import threading
import time

from config import (
    APP_NAME,
    APP_VERSION,
    HOST,
    PORT,
    TEMPLATE_DIR,
    STATIC_DIR,
    DATA_DIR,
    EXCEL_FILE,
    ensure_directories,
)


class TodoRequestHandler(SimpleHTTPRequestHandler):
    """Servidor HTTP sencillo."""

    def translate_path(self, path):
        if path in ("", "/"):
            path = "/index.html"

        if path.startswith("/css/"):
            return str(STATIC_DIR / "css" / path.replace("/css/", ""))

        if path.startswith("/js/"):
            return str(STATIC_DIR / "js" / path.replace("/js/", ""))

        return str(TEMPLATE_DIR / path.lstrip("/"))


def create_excel_placeholder():
    """
    Temporal.
    En versiones posteriores será sustituido por excel_manager.py
    """
    if not EXCEL_FILE.exists():
        EXCEL_FILE.touch()


def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://{HOST}:{PORT}")


def main():

    print("=" * 60)
    print(f"{APP_NAME} {APP_VERSION}")
    print("=" * 60)

    ensure_directories()
    create_excel_placeholder()

    os.chdir(Path(__file__).parent)

    threading.Thread(target=open_browser, daemon=True).start()

    server = HTTPServer((HOST, PORT), TodoRequestHandler)

    print(f"Servidor iniciado en http://{HOST}:{PORT}")
    print("Pulse Ctrl+C para finalizar.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
