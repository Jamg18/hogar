# Contrato inicial de API — `/api/v1`

La API usa JSON, autenticación por token y paginación. Los detalles concretos
del token se fijarán al crear el backend; para móvil se recomienda JWT con
rotación de refresh token.

## Recursos de finanzas

| Método y ruta | Acción |
| --- | --- |
| `GET /categories?type=expense` | Lista las categorías disponibles en el hogar. |
| `POST /categories` | Crea una categoría propia. |
| `PATCH /categories/{id}` | Edita o desactiva una categoría propia. |
| `GET /transactions?from=2026-09-01&to=2026-09-30` | Lista movimientos filtrados. |
| `POST /transactions` | Registra un movimiento manual. |
| `GET /transactions/{id}` | Consulta un movimiento. |
| `PATCH /transactions/{id}` | Modifica un movimiento manual. |
| `DELETE /transactions/{id}` | Lo elimina o archiva según sus vínculos. |
| `GET /finance/summary?month=2026-09` | Devuelve ingresos, gastos y balance mensuales. |

## Ejemplo: crear un gasto

```json
POST /api/v1/transactions
{
  "type": "expense",
  "amount": "48.35",
  "currency": "EUR",
  "category_id": "f41a0b2e-...",
  "effective_date": "2026-09-18",
  "note": "Compra semanal"
}
```

```json
201 Created
{
  "id": "b82c...",
  "type": "expense",
  "amount": "48.35",
  "currency": "EUR",
  "category": {"id": "f41a0b2e-...", "name": "Alimentación"},
  "effective_date": "2026-09-18",
  "source": "manual",
  "note": "Compra semanal"
}
```

## Respuestas de error

Se empleará el formato RFC 7807 o un equivalente uniforme: `code`, `detail` y
errores por campo. Nunca se expondrán trazas internas al cliente.
