# ToDo

Aplicación local para gestionar tareas, responsables, fechas, estados y avances diarios, utilizando:

- HTML, CSS y JavaScript para la interfaz.
- Python 3.13 como servidor local.
- Excel `.xlsx` como almacenamiento.
- Sin necesidad de instalar software adicional en el equipo.

## Objetivo

La aplicación permitirá:

- Crear tareas.
- Editar tareas existentes.
- Cambiar su estado.
- Registrar avances diarios.
- Asignar responsables.
- Definir fechas de creación y finalización.
- Consultar tareas pendientes, en curso y finalizadas.
- Visualizar un calendario de tareas.
- Guardar toda la información en un archivo Excel.
- Crear copias de seguridad.

## Estados previstos

- Pendiente
- En curso
- Bloqueada
- Finalizada
- Cancelada

## Estructura inicial

```text
ToDo/
├── app.py
├── README.md
├── config.py
├── data/
│   └── tareas.xlsx
├── static/
│   ├── css/
│   │   └── estilos.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── src/
│   ├── __init__.py
│   ├── excel_manager.py
│   ├── task_manager.py
│   └── backup_manager.py
└── backups/
```

## Fases del proyecto

### Versión 0.1

- Servidor Python local.
- Interfaz HTML inicial.
- Creación automática del Excel.
- Alta de tareas.
- Listado de tareas.
- Cambio de estado.

### Versión 0.2

- Edición de tareas.
- Historial diario de avances.
- Filtros y búsquedas.
- Calendario mensual.

### Versión 0.3

- Panel de indicadores.
- Copias de seguridad.
- Exportaciones.
- Mejoras de interfaz.

### Versión 1.0

- Aplicación estable.
- Validaciones completas.
- Documentación de uso.
- Preparación para publicación en GitHub.

## Ejecución prevista

Desde la carpeta del proyecto:

```bash
python app.py
```

Después se abrirá la aplicación en el navegador mediante una dirección local similar a:

```text
http://127.0.0.1:8000
```

## Requisitos

- Python 3.13.3
- Navegador web moderno
- No se utilizarán librerías externas salvo que sean estrictamente necesarias y se acuerde previamente.

## Rama de desarrollo

El desarrollo se realizará inicialmente sobre la rama:

```text
develop
```

La rama `main` se reservará para versiones estables.
