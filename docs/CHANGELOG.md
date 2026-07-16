# CHANGELOG

Todos los cambios importantes del proyecto **ToDo** se registran en este
documento.

El formato está inspirado en *Keep a Changelog* y versionado semántico.

------------------------------------------------------------------------

# \[1.0.0\] - En desarrollo

## Añadido

### Arquitectura

-   Organización del proyecto por módulos.
-   Separación entre frontend, API, servicios y persistencia.
-   Estructura preparada para crecimiento.

### Backend

-   API REST.
-   Gestión de tareas (CRUD).
-   Validación centralizada.
-   Gestión del historial.
-   Gestión de copias de seguridad.
-   Persistencia mediante Excel.

### Servicios

-   DashboardService.
-   CalendarService.
-   SearchService.
-   StatisticsService.

### Frontend

-   Dashboard.
-   Tabla de tareas.
-   Calendario.
-   Búsqueda.
-   Filtros.
-   Exportación CSV.
-   Notificaciones.

### Documentación

-   API.md
-   Arquitectura.md
-   Instalacion.md
-   CHANGELOG.md

------------------------------------------------------------------------

## Mejorado

-   Organización del código.
-   Gestión de errores.
-   Validaciones.
-   Rendimiento del acceso al Excel.
-   Compatibilidad con futuras bases de datos.

------------------------------------------------------------------------

## Pendiente para la versión 1.1

-   Autenticación completa.
-   Gestión de usuarios y permisos.
-   Informes PDF.
-   Gráficos avanzados.
-   Sincronización multiusuario.
-   Notificaciones por correo y Teams.
-   Importación y exportación Excel avanzadas.
-   Tema oscuro.
-   Internacionalización.

------------------------------------------------------------------------

## Compatibilidad

  Componente      Estado
  --------------- ------------
  Python 3.13     Compatible
  Windows         Compatible
  Linux           Compatible
  Excel (.xlsx)   Compatible
  API REST        Compatible
  HTML/CSS/JS     Compatible

------------------------------------------------------------------------

## Notas

Durante el desarrollo se han reorganizado los módulos para mejorar la
mantenibilidad y facilitar futuras ampliaciones sin afectar a la
interfaz de usuario.
