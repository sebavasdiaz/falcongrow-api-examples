# FalconGrow API v2 — ejemplos / examples

[Español](#español) · [English](#english)

Ejemplos de uso de la **API v2 de FalconGrow**, el panel SMM chileno para Chile y LATAM.
Documentación oficial: <https://www.falcongrow.com/api-docs> · Presentación: <https://www.falcongrow.com/api-smm>

---

## Español

### Qué es la API v2

FalconGrow es un panel SMM chileno para Chile y LATAM: seguidores, me gusta, vistas y reproducciones
para Instagram, TikTok, YouTube, Spotify, Facebook, Twitch y Kick. Sin suscripción: se paga por pedido
y, si una orden no se completa, lo no entregado vuelve automáticamente al saldo.

La API v2 sigue el formato estándar de los paneles SMM (mismos parámetros `key`, `action`, `service`,
`link`, `quantity` y mismas respuestas). Un panel hijo estándar (tipo Perfect Panel) puede agregar
FalconGrow como proveedor solo con la URL y la API key.

| | |
|---|---|
| Endpoint | `https://www.falcongrow.com/api/v2` |
| Método | `POST` (`GET` solo para `action=services`) |
| Formato | JSON o `application/x-www-form-urlencoded` |
| Autenticación | parámetro `key` con tu API key |
| Límite | 120 solicitudes por minuto por API key (HTTP 429 con `Retry-After` si se excede) |
| Moneda | USD; la API cobra de tu saldo prepago, el mismo del panel web |

**Cómo obtener la API key:** crea tu cuenta en <https://www.falcongrow.com>, entra a
*Perfil → pestaña API* y copia la clave. No hay proceso de aprobación ni costo adicional.
Nunca publiques tu clave; si se compromete, regenérala desde el panel.

### Acciones

| `action` | Parámetros | Respuesta (ejemplo) |
|---|---|---|
| `services` | — | `[{"service":42,"name":"…","type":"Default","category":"…","rate":"1.20","min":100,"max":50000,"dripfeed":false,"refill":true,"cancel":false}]` |
| `add` | `service`, `link`, `quantity` (opcionales `runs`, `interval` para dripfeed) | `{"order":7391}` |
| `status` | `order` o `orders=1,2,3` (máx. 100) | `{"charge":"1.200000","start_count":4820,"status":"In progress","remains":643,"currency":"USD"}` |
| `balance` | — | `{"balance":"48.530000","currency":"USD"}` |
| `refill` | `order` o `orders=1,2` (máx. 100) | `{"refill":"9910"}` |
| `cancel` | `orders=1,2` (máx. 100) | `[{"order":7391,"cancel":1}]` |
| `refill_status` | — | siempre `{"error":"Refill status is not supported"}` |

- `rate` es tu precio por 1.000 unidades en USD.
- Estados de pedido: `Pending`, `In progress`, `Completed`, `Partial`, `Canceled`, `Failed`.
- `refill` solo aplica si el servicio tiene `refill: true` y su período de reposición sigue vigente
  (una solicitud cada 24 h por pedido).
- `cancel` solo aplica a pedidos que aún no empezaron, de servicios con `cancel: true` y sin dripfeed.
  Cuando el pedido pasa a `Canceled`, el cargo vuelve a tu saldo.
- Si falta saldo o la cantidad está fuera de rango, no se crea el pedido ni se cobra nada.

### Errores

Como en los paneles estándar, los errores responden **HTTP 200** con un campo `error` (mensajes en inglés):

```json
{ "error": "Invalid API key" }
{ "error": "Incorrect request" }
{ "error": "Incorrect order ID" }
{ "error": "Not enough funds on balance" }
```

Excepciones: `429` (límite excedido; espera lo que indique `Retry-After`) y `500` (error interno; reintenta más tarde).

### Ejemplos

- [curl](examples/curl/ejemplos.sh)
- [Python](examples/python/falcongrow_api.py) (solo biblioteca estándar)
- [JavaScript / Node.js 18+](examples/javascript/falcongrow-api.mjs) (`fetch` nativo)

```bash
curl -X POST https://www.falcongrow.com/api/v2 \
  -d key=YOUR_API_KEY \
  -d action=balance
```

Recomendación: cachea la respuesta de `services`; el catálogo y los precios cambian unas pocas veces al día.

### Enlaces

- Documentación completa: <https://www.falcongrow.com/api-docs>
- API SMM en español: <https://www.falcongrow.com/api-smm>
- Precios: <https://www.falcongrow.com/precios>
- Tiempos de entrega medidos: <https://www.falcongrow.com/tiempos-de-entrega>
- Garantía y reembolsos: <https://www.falcongrow.com/garantia-y-reembolsos>
- Qué es FalconGrow: <https://www.falcongrow.com/sobre-falcongrow>
- Contacto: soporte@falcongrow.com

---

## English

### What the API v2 is

FalconGrow is a Chilean SMM panel for Chile and Latin America: followers, likes, views and plays for
Instagram, TikTok, YouTube, Spotify, Facebook, Twitch and Kick. No subscription: you pay per order, and
if an order is not completed, the undelivered part is refunded to your balance automatically.

The API v2 follows the standard SMM panel format (same `key`, `action`, `service`, `link`, `quantity`
parameters and the same responses). A standard child panel (e.g. Perfect Panel) can add FalconGrow as a
provider with just the URL and an API key.

| | |
|---|---|
| Endpoint | `https://www.falcongrow.com/api/v2` |
| Method | `POST` (`GET` only for `action=services`) |
| Format | JSON or `application/x-www-form-urlencoded` |
| Auth | `key` parameter with your API key |
| Rate limit | 120 requests per minute per API key (HTTP 429 with `Retry-After` when exceeded) |
| Currency | USD; the API charges your prepaid balance, the same one used by the web panel |

**Getting an API key:** create an account at <https://www.falcongrow.com>, open
*Profile → API tab* and copy the key. No approval process, no extra cost.
Never publish your key; if it leaks, regenerate it from the dashboard.

### Actions

| `action` | Parameters | Response (example) |
|---|---|---|
| `services` | — | `[{"service":42,"name":"…","type":"Default","category":"…","rate":"1.20","min":100,"max":50000,"dripfeed":false,"refill":true,"cancel":false}]` |
| `add` | `service`, `link`, `quantity` (optional `runs`, `interval` for drip-feed) | `{"order":7391}` |
| `status` | `order` or `orders=1,2,3` (max. 100) | `{"charge":"1.200000","start_count":4820,"status":"In progress","remains":643,"currency":"USD"}` |
| `balance` | — | `{"balance":"48.530000","currency":"USD"}` |
| `refill` | `order` or `orders=1,2` (max. 100) | `{"refill":"9910"}` |
| `cancel` | `orders=1,2` (max. 100) | `[{"order":7391,"cancel":1}]` |
| `refill_status` | — | always `{"error":"Refill status is not supported"}` |

- `rate` is your price per 1,000 units in USD.
- Order statuses: `Pending`, `In progress`, `Completed`, `Partial`, `Canceled`, `Failed`.
- `refill` works only when the service has `refill: true` and its refill period is still active
  (one request every 24 h per order).
- `cancel` works only for orders that have not started yet, on services with `cancel: true` and without
  drip-feed. When the order becomes `Canceled`, the charge goes back to your balance.
- If the balance is insufficient or the quantity is out of range, no order is created and nothing is charged.

### Errors

As with standard panels, errors return **HTTP 200** with an `error` field (messages in English). The
exceptions are `429` (rate limit exceeded; wait for `Retry-After`) and `500` (internal error; retry later).

### Examples

- [curl](examples/curl/ejemplos.sh)
- [Python](examples/python/falcongrow_api.py) (standard library only)
- [JavaScript / Node.js 18+](examples/javascript/falcongrow-api.mjs) (native `fetch`)

Tip: cache the `services` response; the catalog and prices change a few times a day.

### Links

- Full documentation (Spanish): <https://www.falcongrow.com/api-docs>
- Website: <https://www.falcongrow.com/en>
- Measured delivery times: <https://www.falcongrow.com/tiempos-de-entrega>
- Contact: soporte@falcongrow.com

---

FalconGrow is not affiliated with Instagram, TikTok, YouTube, Spotify, Meta, Twitch or Kick.
FalconGrow no está afiliado a Instagram, TikTok, YouTube, Spotify, Meta, Twitch ni Kick.

License: [MIT](LICENSE).
