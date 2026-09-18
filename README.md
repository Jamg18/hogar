# Hogar

Aplicación móvil para administrar la economía cotidiana de un hogar: finanzas,
compras y movilidad. El primer objetivo es una herramienta privada, fiable y
útil; la publicación comercial queda fuera del MVP.

## Estado

Se ha definido la base funcional y técnica del proyecto. El primer entregable
de software será una API de finanzas en Django REST Framework, consumible desde
una aplicación Flutter.

## Arquitectura objetivo

```text
Flutter (Android/iOS)
        │ HTTPS / JSON
        ▼
Django + Django REST Framework
 ├── users       identidad y hogar
 ├── finance     historial financiero común
 ├── shopping    listas, precios y compras
 ├── mobility    vehículos, repostajes y rutas
 └── insights    análisis resumido futuro
        │
        ▼
PostgreSQL
```

Los módulos de compras y movilidad nunca duplican la contabilidad: cuando se
confirma una compra o un repostaje crean o enlazan un movimiento de `finance`.

## Documentación

- [MVP de finanzas](docs/mvp-finanzas.md)
- [Modelo de dominio](docs/modelo-dominio.md)
- [Contrato inicial de API](docs/api-v1.md)
- [Decisiones técnicas](docs/decisiones-tecnicas.md)

## Preparar el backend

Desde la carpeta del proyecto:

```bash
cd /home/gamma/hogar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El archivo de dependencias está en [`requirements.txt`](requirements.txt). El
entorno virtual se crea en `.venv/`, se ignora por Git y se activa cada vez que
se vaya a trabajar en el backend.

## Ejecutar la API localmente

```bash
cd /home/gamma/hogar/backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py createsuperuser
../.venv/bin/python manage.py runserver
```

Con el servidor activo, los accesos locales principales son:

- Administración: http://127.0.0.1:8000/admin/
- Documentación interactiva: http://127.0.0.1:8000/api/docs/
- Esquema OpenAPI: http://127.0.0.1:8000/api/schema/
- API: http://127.0.0.1:8000/api/v1/

La cuenta que se crea con `createsuperuser` usa el correo electrónico como
identificador y recibe automáticamente un hogar con las categorías iniciales.

## Siguiente hito

Crear el repositorio ejecutable del backend, con Django, PostgreSQL y la API
versionada de categorías y movimientos.
