# Arquitectura del Proyecto ToDo

## Visión general

La aplicación sigue una arquitectura por capas para separar la interfaz,
la lógica de negocio y la persistencia.

``` text
Frontend (HTML/CSS/JS)
        │
        ▼
 API REST (api_server.py + routes.py)
        │
        ▼
 Servicios (services/)
        │
        ▼
Repositorio (database.py)
        │
        ▼
ExcelManager
        │
        ▼
tareas.xlsx
```

## Estructura

### Raíz

-   `app.py`: inicia la aplicación.
-   `api_server.py`: servidor REST.
-   `config.py`: configuración general.

### src/

Contiene los componentes internos:

-   `models.py`
-   `database.py`
-   `excel_manager.py`
-   `history_manager.py`
-   `backup_manager.py`
-   `validators.py`

Submódulos:

-   `api/`
-   `auth/`
-   `reports/`

### services/

Centraliza la lógica de negocio:

-   `dashboard_service.py`
-   `calendar_service.py`
-   `search_service.py`
-   `statistics_service.py`

### static/

Recursos web:

-   `css/`
-   `js/`
-   `assets/`

### templates/

Plantillas HTML.

### data/

Datos persistentes:

-   `tareas.xlsx`
-   `backups/`
-   `logs/`

### tests/

Pruebas unitarias e integración.

## Flujo de una petición

1.  El navegador envía una petición HTTP.
2.  `api_server.py` la recibe.
3.  `routes.py` valida y enruta.
4.  El servicio correspondiente aplica la lógica.
5.  `TaskRepository` accede a los datos.
6.  `ExcelManager` lee o escribe el archivo Excel.
7.  La respuesta JSON vuelve al cliente.

## Principios de diseño

-   Separación de responsabilidades.
-   Validación centralizada.
-   Persistencia mediante Excel.
-   API REST desacoplada del frontend.
-   Servicios reutilizables.
-   Copias de seguridad automáticas.
-   Historial de cambios.
-   Código preparado para crecer hacia una base de datos SQL sin
    modificar el frontend.

## Evolución prevista

-   Autenticación por tokens.
-   Informes PDF.
-   Notificaciones por correo o Teams.
-   Base de datos SQL opcional.
-   Sincronización multiusuario.
-   Paneles gráficos avanzados.
