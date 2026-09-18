# Modelo de dominio

## Principios

- Todos los importes se guardan como `Decimal`, nunca `float`.
- Las fechas de negocio se guardan como fecha local (`effective_date`); las
  auditorías como fecha/hora UTC (`created_at`, `updated_at`).
- El historial financiero es la fuente de verdad del dinero gastado o ingresado.
- Una entidad de otro módulo puede vincularse a un movimiento, pero no lo crea
  de forma silenciosa ni permite que dos entidades sean su origen.

## Entidades iniciales

| Entidad | Campos relevantes | Propósito |
| --- | --- | --- |
| `User` | email, nombre, contraseña | Identidad; se usará el usuario propio de Django desde el inicio. |
| `Household` | nombre, moneda, zona horaria | Espacio de datos privado del hogar. |
| `Membership` | hogar, usuario, rol | Permite futuro uso compartido. |
| `Category` | hogar opcional, nombre, tipo, color, activa | Clasifica movimientos; las globales son plantillas. |
| `Transaction` | hogar, tipo, importe, categoría, fecha, nota, origen | Entrada del historial. |

`Transaction.type` será `income` o `expense`. El importe siempre será positivo;
el signo se interpreta por el tipo. Esto evita importes negativos ambiguos.

`Transaction.source` inicia como `manual` y más adelante podrá ser `shopping`
o `fuel`. Las entidades futuras guardarán una relación uno-a-uno con su
movimiento financiero:

```text
ShoppingPurchase  1 ─── 1 Transaction
FuelFillUp        1 ─── 1 Transaction
```

## Extensiones ya previstas

| Dominio | Entidades futuras | Relación con finanzas |
| --- | --- | --- |
| Compras | ShoppingList, Item, Store, ProductPrice, Purchase | Una compra confirmada enlaza un gasto. |
| Movilidad | Vehicle, FuelStationSnapshot, FuelFillUp, RouteEstimate | Un repostaje enlaza un gasto. |
| Análisis | MonthlyAggregate, Insight | Solo lee datos agregados; no modifica transacciones. |

## Categorías iniciales sugeridas

Gastos: alimentación, vivienda, suministros, transporte, combustible, salud,
ocio, suscripciones, educación, mascotas, otros.

Ingresos: salario, extra, reembolso, venta, otros.
