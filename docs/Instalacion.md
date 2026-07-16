# Instalación de ToDo

## Requisitos

-   Python 3.13 o superior
-   Git (opcional)
-   Navegador web moderno

## Estructura esperada

``` text
ToDo/
├── app.py
├── api_server.py
├── config.py
├── src/
├── services/
├── static/
├── templates/
├── data/
└── docs/
```

## Preparación

1.  Clona el repositorio o copia la carpeta del proyecto.
2.  Sitúate en la carpeta raíz:

``` bash
cd ToDo
```

3.  (Opcional) Crea un entorno virtual:

``` bash
python -m venv .venv
```

Actívalo:

-   Windows

``` bash
.venv\\Scripts\\activate
```

-   Linux/macOS

``` bash
source .venv/bin/activate
```

## Dependencias

Instala las dependencias del proyecto:

``` bash
pip install -r requirements.txt
```

## Primer inicio

Ejecuta:

``` bash
python app.py
```

En el primer arranque la aplicación:

-   crea `data/tareas.xlsx` si no existe;
-   crea las carpetas de copias de seguridad y registros;
-   prepara la estructura del libro Excel;
-   inicia la API REST y la interfaz web.

## Acceso

-   Aplicación: `http://127.0.0.1:8000`
-   API: `http://127.0.0.1:8000/api/health`

## Copias de seguridad

Las copias automáticas se almacenan en:

``` text
data/backups/
```

## Solución de problemas

### El puerto está ocupado

Modifica `HOST` o `PORT` en `config.py`.

### No se crea el Excel

Comprueba permisos de escritura sobre la carpeta `data`.

### Error al abrir el Excel

Restaura una copia desde `data/backups/`.

## Actualización

Para actualizar el proyecto:

1.  Haz una copia de seguridad.
2.  Sustituye los archivos del proyecto.
3.  Conserva la carpeta `data/`.
4.  Ejecuta de nuevo `python app.py`.
