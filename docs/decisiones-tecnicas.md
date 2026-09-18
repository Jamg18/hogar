# Decisiones técnicas iniciales

## Elegidas

- **Backend:** Python + Django + Django REST Framework.
- **Base de datos:** PostgreSQL en todos los entornos relevantes; SQLite solo
  podría usarse para pruebas rápidas locales.
- **Cliente:** Flutter, con una capa de datos separada de la interfaz.
- **API:** REST bajo `/api/v1/`; documentada con OpenAPI desde el inicio.
- **Identificadores:** UUID públicos para no exponer secuencias internas.
- **Configuración:** variables de entorno, sin secretos en Git.

## Estructura prevista

```text
hogar/
├── backend/
│   ├── config/       # ajustes y rutas globales
│   └── apps/
│       ├── users/
│       ├── households/
│       ├── finance/
│       ├── shopping/ # fase posterior
│       └── mobility/ # fase posterior
├── mobile/           # Flutter
└── docs/
```

## Decisiones diferidas intencionadamente

- Proveedor de hosting y copias de seguridad.
- Sistema concreto de autenticación social.
- Fuente y licencia de precios de supermercados.
- Proveedor de rutas/mapas y sus costes.
- Diseño visual, nombre e identidad de marca.

Se aplazan porque no bloquean validar el módulo de finanzas y elegirlas ahora
generaría trabajo prematuro.
