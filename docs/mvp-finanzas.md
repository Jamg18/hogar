# MVP 1 — Finanzas del hogar

## Objetivo

Permitir a una persona registrar y consultar ingresos y gastos de su hogar de
forma rápida, con categorías y totales correctos por periodo.

## Incluido

- Registro y acceso de usuario.
- Un hogar inicial asociado a su creador. La estructura permite añadir miembros
  posteriormente sin rediseñar los datos.
- Categorías de ingreso y gasto, incluidas categorías predefinidas editables.
- Creación, edición, borrado y consulta paginada de movimientos.
- Filtros por fecha, tipo y categoría.
- Resumen mensual: ingresos, gastos y balance.
- Moneda del hogar (EUR por defecto), importes con dos decimales y zona horaria.

## Fuera del MVP

- Presupuestos, cuentas bancarias y sincronización bancaria.
- Recurrentes, adjuntos, OCR de tickets y exportación.
- Listas de compra, precios, vehículos, rutas, IA y publicación en tiendas.

## Criterios de aceptación

1. Un usuario puede crear un ingreso o gasto con importe, categoría y fecha.
2. Un movimiento no puede tener importe cero ni una categoría de tipo contrario.
3. El resumen de septiembre, por ejemplo, suma exclusivamente movimientos cuya
   fecha efectiva esté en septiembre, sin depender de cuándo se crearon.
4. Solo los miembros del hogar pueden leer o modificar sus datos.
5. Borrar un movimiento conserva trazabilidad mediante borrado lógico si en el
   futuro estuviera vinculado a una compra o repostaje.

## Flujo principal

```text
Usuario → elige ingreso/gasto → categoría + importe + fecha → guarda
        → movimiento financiero → historial y resumen mensual actualizados
```
