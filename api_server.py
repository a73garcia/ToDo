from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse
import json

from src.api.routes import Routes


class TodoAPIHandler(BaseHTTPRequestHandler):
    """Manejador HTTP de la API REST ToDo 2.0."""

    routes = Routes()

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def _parts(self):
        return [unquote(part) for part in urlparse(self.path).path.split("/") if part]

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            parts = self._parts()
            query = parse_qs(parsed.query)
            value = lambda key, default=None: query.get(key, [default])[0]

            if parsed.path == "/api/health":
                return self._send_json({"ok": True, "service": "ToDo API", "version": "2.0"})

            if parsed.path == "/api/tasks":
                data, status = self.routes.get_tasks(
                    search=value("q", ""),
                    status=value("status"),
                    priority=value("priority"),
                    responsible=value("responsible"),
                    project=value("project"),
                    tag=value("tag"),
                    favorite=None,
                )
            elif len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                data, status = self.routes.get_task(int(parts[2]))
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "comments":
                data, status = self.routes.get_comments(int(parts[2]))
            elif parsed.path == "/api/dashboard":
                data, status = self.routes.get_dashboard()
            elif parsed.path == "/api/calendar":
                data, status = self.routes.get_calendar(value("year"), value("month"), value("day"))
            elif parsed.path == "/api/upcoming":
                data, status = self.routes.get_upcoming(int(value("days", 14)))
            elif parsed.path == "/api/overdue":
                data, status = self.routes.get_overdue()
            elif parsed.path == "/api/statistics/responsible":
                data, status = self.routes.get_statistics_by_responsible()
            elif parsed.path == "/api/history":
                data, status = self.routes.get_history(value("task_id"), value("limit"))
            else:
                return self._send_json({"error": "Ruta no encontrada."}, 404)

            return self._send_json(data, status)
        except Exception as exc:
            return self._send_json({"error": str(exc)}, 400)

    def do_POST(self):
        try:
            parsed = urlparse(self.path)
            parts = self._parts()
            data = self._read_json()

            if parsed.path == "/api/tasks":
                result, status = self.routes.create_task(data)
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "comments":
                result, status = self.routes.add_comment(int(parts[2]), data)
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "tags":
                result, status = self.routes.add_tag(int(parts[2]), data)
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "favorite":
                result, status = self.routes.toggle_favorite(int(parts[2]))
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "status":
                result, status = self.routes.change_status(int(parts[2]), data)
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "progress":
                result, status = self.routes.change_progress(int(parts[2]), data)
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "move":
                result, status = self.routes.move_task(int(parts[2]), data)
            elif parsed.path == "/api/backups":
                result, status = self.routes.create_backup()
            else:
                return self._send_json({"error": "Ruta no encontrada."}, 404)

            return self._send_json(result, status)
        except Exception as exc:
            return self._send_json({"error": str(exc)}, 400)

    def do_PATCH(self):
        try:
            parts = self._parts()
            if len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                result, status = self.routes.update_task(int(parts[2]), self._read_json())
                return self._send_json(result, status)
            return self._send_json({"error": "Ruta no encontrada."}, 404)
        except Exception as exc:
            return self._send_json({"error": str(exc)}, 400)

    def do_PUT(self):
        try:
            parts = self._parts()
            if len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                result, status = self.routes.replace_task(int(parts[2]), self._read_json())
                return self._send_json(result, status)
            return self._send_json({"error": "Ruta no encontrada."}, 404)
        except Exception as exc:
            return self._send_json({"error": str(exc)}, 400)

    def do_DELETE(self):
        try:
            parts = self._parts()
            if len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                result, status = self.routes.delete_task(int(parts[2]))
            elif len(parts) == 5 and parts[:2] == ["api", "tasks"] and parts[3] == "comments":
                result, status = self.routes.delete_comment(int(parts[2]), int(parts[4]))
            elif len(parts) == 5 and parts[:2] == ["api", "tasks"] and parts[3] == "tags":
                result, status = self.routes.remove_tag(int(parts[2]), parts[4])
            else:
                return self._send_json({"error": "Ruta no encontrada."}, 404)
            return self._send_json(result, status)
        except Exception as exc:
            return self._send_json({"error": str(exc)}, 400)


def run(host="127.0.0.1", port=8001):
    server = ThreadingHTTPServer((host, port), TodoAPIHandler)
    print(f"API ToDo disponible en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
