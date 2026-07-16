"""
api_server.py
Servidor REST básico para ToDo.
Versión inicial.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from database import TaskRepository
from models import Task


class TodoAPIHandler(BaseHTTPRequestHandler):

    repo = TaskRepository()

    def _send(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/tasks":
            tasks = [t.__dict__ for t in self.repo.get_all()]
            return self._send(tasks)

        return self._send({"error": "No encontrado"}, 404)

    def do_POST(self):
        if self.path != "/api/tasks":
            return self._send({"error": "No encontrado"}, 404)

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8")
        data = json.loads(payload)

        task = Task(
            titulo=data.get("titulo", ""),
            descripcion=data.get("descripcion", ""),
            responsable=data.get("responsable", ""),
            prioridad=data.get("prioridad", "Media"),
            estado=data.get("estado", "Pendiente"),
            fecha_prevista=data.get("fecha", ""),
            avance=int(data.get("avance", 0)),
        )

        self.repo.add(task)

        return self._send({"ok": True}, 201)

    def do_DELETE(self):
        # Se implementará completamente en la siguiente versión
        return self._send({
            "warning": "DELETE pendiente de implementación."
        }, 501)


def run(host="127.0.0.1", port=8001):
    server = HTTPServer((host, port), TodoAPIHandler)
    print(f"API disponible en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
