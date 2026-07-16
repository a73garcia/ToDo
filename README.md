# ToDo

Aplicación local para gestionar tareas mediante una interfaz web y almacenar los datos en un archivo Excel `.xlsx`.

## Funciones disponibles

- Alta, edición y eliminación de tareas.
- Estados: Pendiente, En curso, Bloqueada, Finalizada y Cancelada.
- Responsable, prioridad, fechas, observaciones y porcentaje de avance.
- Dashboard y calendario.
- Búsqueda y filtros desde la interfaz.
- Historial de cambios dentro del libro Excel.
- Copias de seguridad antes de cada modificación.
- API REST integrada en el mismo servidor de la aplicación.

## Requisitos

- Python 3.13.3.
- Navegador web moderno.
- Paquete Python `openpyxl`, indicado en `requirements.txt`.

## Preparación

Desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

La aplicación abrirá automáticamente el navegador en:

```text
http://127.0.0.1:8000
```

Para cerrarla, vuelve a la ventana de comandos y pulsa `Ctrl+C`.

## Almacenamiento

Al iniciar la aplicación, si no existe, se crea un libro válido en:

```text
data/tareas.xlsx
```

El libro contiene estas hojas:

- `Tareas`: información principal.
- `Historial`: registro de creaciones, actualizaciones y eliminaciones.
- `Configuración`: versión, estados y prioridades disponibles.

Antes de modificar el libro se crea una copia en `backups/`.

## Estructura principal

```text
ToDo/
├── app.py
├── config.py
├── requirements.txt
├── data/
│   └── tareas.xlsx
├── backups/
├── static/
│   ├── css/
│   │   └── estilos.css
│   └── js/
│       └── app.js
└── templates/
    └── index.html
```

## API

El servidor integrado proporciona:

- `GET /api/health`
- `GET /api/tasks`
- `GET /api/tasks/{id}`
- `POST /api/tasks`
- `PATCH /api/tasks/{id}`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
- `GET /api/dashboard`
- `GET /api/calendar`
- `GET /api/history`

## Rama actual

El proyecto se encuentra actualmente en `main`. Cuando se cree una rama `develop`, las nuevas funciones podrán desarrollarse allí y reservar `main` para versiones estables.
