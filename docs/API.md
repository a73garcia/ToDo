# API de ToDo

## Información general

-   Base URL: `/api`
-   Formato: `application/json`
-   Codificación: UTF-8

------------------------------------------------------------------------

## Health

### GET `/api/health`

Comprueba que la API está disponible.

**Respuesta**

``` json
{
  "ok": true,
  "service": "ToDo API"
}
```

------------------------------------------------------------------------

## Tareas

### GET `/api/tasks`

Devuelve todas las tareas.

**Parámetros opcionales**

  Parámetro   Descripción
  ----------- ---------------------
  `q`         Texto para búsqueda

### GET `/api/tasks/{id}`

Obtiene una tarea concreta.

### POST `/api/tasks`

Crea una nueva tarea.

Campos principales:

-   titulo
-   descripcion
-   responsable
-   prioridad
-   estado
-   fecha_prevista
-   avance
-   observaciones

### PATCH `/api/tasks/{id}`

Actualiza únicamente los campos enviados.

### PUT `/api/tasks/{id}`

Sustituye completamente una tarea.

### DELETE `/api/tasks/{id}`

Elimina una tarea.

------------------------------------------------------------------------

## Dashboard

### GET `/api/dashboard`

Devuelve:

-   Total de tareas
-   Pendientes
-   En curso
-   Bloqueadas
-   Finalizadas
-   Canceladas
-   Retrasadas
-   Avance medio

------------------------------------------------------------------------

## Calendario

### GET `/api/calendar`

Parámetros opcionales:

-   `year`
-   `month`

------------------------------------------------------------------------

## Historial

### GET `/api/history`

Opcional:

-   `task_id`

------------------------------------------------------------------------

## Códigos HTTP

  Código   Significado
  -------- ---------------------
  200      Correcto
  201      Creado
  400      Petición incorrecta
  404      No encontrado
  500      Error interno

------------------------------------------------------------------------

## Ejemplo de creación

``` json
{
  "titulo":"Preparar informe",
  "descripcion":"Informe mensual",
  "responsable":"Antonio",
  "prioridad":"Alta",
  "estado":"Pendiente",
  "fecha_prevista":"2026-08-01",
  "avance":0
}
```
