#!/usr/bin/env bash
# FalconGrow API v2 — ejemplos con curl / curl examples
# Docs: https://www.falcongrow.com/api-docs
# Uso / usage: FALCONGROW_API_KEY=... bash ejemplos.sh
set -euo pipefail

API_URL="https://www.falcongrow.com/api/v2"
KEY="${FALCONGROW_API_KEY:-YOUR_API_KEY}"

# Saldo / balance
curl -s -X POST "$API_URL" -d key="$KEY" -d action=balance; echo

# Catálogo / services (cachéalo / cache it)
curl -s -X POST "$API_URL" -d key="$KEY" -d action=services | head -c 600; echo

# Crear pedido / create order (JSON body). Descomenta para usarlo: cobra de tu saldo.
# Uncomment to use: it charges your balance.
# curl -s -X POST "$API_URL" \
#   -H "Content-Type: application/json" \
#   -d '{"key": "'"$KEY"'", "action": "add", "service": 42, "link": "https://www.instagram.com/yourname/", "quantity": 1000}'

# Estado de un pedido / single order status
# curl -s -X POST "$API_URL" -d key="$KEY" -d action=status -d order=7391

# Estado de varios pedidos (máx. 100) / multiple orders (max. 100)
# curl -s -X POST "$API_URL" -d key="$KEY" -d action=status -d orders=7391,7392,7393

# Reposición / refill (si el servicio tiene refill: true)
# curl -s -X POST "$API_URL" -d key="$KEY" -d action=refill -d order=7391

# Cancelar / cancel (pedidos no iniciados, servicios con cancel: true)
# curl -s -X POST "$API_URL" -d key="$KEY" -d action=cancel -d orders=7391,7392
