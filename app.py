from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote
import mimetypes
import threading
import time
import webbrowser

from api_server import TodoAPIHandler
from config import APP_NAME, APP_VERSION, HOST, PORT, STATIC_DIR, TEMPLATE_DIR, ensure_directories
from src.excel_manager import ExcelManager


class TodoApplicationHandler(TodoAPIHandler):
    """Servidor integrado para frontend y API REST."""

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            return super().do_GET()
        return self._serve_file(parsed.path)

    def _serve_file(self, request_path: str):
        request_path = unquote(request_path or "/")

        if request_path in ("", "/", "/index.html"):
            file_path = TEMPLATE_DIR / "index.html"
            allowed_root = TEMPLATE_DIR
        elif request_path.startswith("/css/"):
            file_path = STATIC_DIR / "css" / request_path.removeprefix("/css/")
            allowed_root = STATIC_DIR
        elif request_path.startswith("/js/"):
            file_path = STATIC_DIR / "js" / request_path.removeprefix("/js/")
            allowed_root = STATIC_DIR
        elif request_path.startswith("/assets/"):
            file_path = STATIC_DIR / "assets" / request_path.removeprefix("/assets/")
            allowed_root = STATIC_DIR
        else:
            return self._send_json({"error": "Archivo no encontrado."}, 404)

        file_path = file_path.resolve()
        allowed_root = allowed_root.resolve()
        try:
            file_path.relative_to(allowed_root)
        except ValueError:
            return self._send_json({"error": "Acceso no permitido."}, 403)

        if not file_path.exists() or not file_path.is_file():
            return self._send_json({"error": "Archivo no encontrado."}, 404)

        content = file_path.read_bytes()
        mime_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        if mime_type.startswith("text/"):
            mime_type += "; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


def main():
    ensure_directories()
    ExcelManager().create_if_not_exists()

    server = ThreadingHTTPServer((HOST, PORT), TodoApplicationHandler)
    threading.Thread(
        target=lambda: (time.sleep(1), webbrowser.open(f"http://{HOST}:{PORT}")),
        daemon=True,
    ).start()

    print(f"{APP_NAME} {APP_VERSION} disponible en http://{HOST}:{PORT}")
    print("Pulse Ctrl+C para finalizar.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
