"""
src/settings.py
Configuración global editable de la aplicación ToDo.
"""

from dataclasses import dataclass, field
from pathlib import Path
import json

CONFIG_FILE = Path("data") / "settings.json"


@dataclass
class Settings:
    idioma: str = "es"
    tema: str = "claro"
    puerto: int = 8000

    backups_maximos: int = 20
    crear_backup_al_iniciar: bool = True
    crear_backup_al_salir: bool = True

    vista_inicial: str = "dashboard"
    mostrar_calendario: bool = True
    mostrar_estadisticas: bool = True

    prioridad_colores: dict = field(default_factory=lambda: {
        "Baja": "#28a745",
        "Media": "#007bff",
        "Alta": "#fd7e14",
        "Crítica": "#dc3545"
    })

    estado_colores: dict = field(default_factory=lambda: {
        "Pendiente": "#6c757d",
        "En curso": "#0d6efd",
        "Bloqueada": "#ffc107",
        "Finalizada": "#198754",
        "Cancelada": "#dc3545"
    })

    def save(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls):
        if not CONFIG_FILE.exists():
            s = cls()
            s.save()
            return s

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)


if __name__ == "__main__":
    settings = Settings.load()
    print(settings)
