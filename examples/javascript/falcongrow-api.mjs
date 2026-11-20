// FalconGrow API v2 — cliente mínimo en JavaScript (Node.js 18+, fetch nativo).
// Minimal FalconGrow API v2 client in JavaScript (Node.js 18+, native fetch).
// Docs: https://www.falcongrow.com/api-docs
// Uso / usage: FALCONGROW_API_KEY=... node falcongrow-api.mjs

const API_URL = 'https://www.falcongrow.com/api/v2';

export class FalconGrowAPI {
  constructor(apiKey) {
    this.apiKey = apiKey;
  }

  async call(action, params = {}) {
    const body = new URLSearchParams({ key: this.apiKey, action });
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null) body.append(k, String(v));
    }
    for (let attempt = 0; attempt < 3; attempt++) {
      const res = await fetch(API_URL, { method: 'POST', body });
      if (res.status === 429 && attempt < 2) {
        // Límite de 120 req/min por clave / 120 req/min per key
        const wait = Number(res.headers.get('Retry-After') || 5);
        await new Promise((r) => setTimeout(r, wait * 1000));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // Los errores llegan con HTTP 200 / errors come with HTTP 200
      if (data && !Array.isArray(data) && data.error) throw new Error(data.error);
      return data;
    }
  }

  services() { return this.call('services'); }
  balance() { return this.call('balance'); }
  add({ service, link, quantity, runs, interval }) {
    return this.call('add', { service, link, quantity, runs, interval });
  }
  status(order) { return this.call('status', { order }); }
  multiStatus(orders) { return this.call('status', { orders: orders.join(',') }); }
  refill(order) { return this.call('refill', { order }); }
  cancel(orders) { return this.call('cancel', { orders: orders.join(',') }); }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const api = new FalconGrowAPI(process.env.FALCONGROW_API_KEY || 'YOUR_API_KEY');
  console.log('balance:', await api.balance());
  const catalog = await api.services();
  console.log(`${catalog.length} services; first:`, catalog[0]);
  // Crear un pedido cobra de tu saldo / creating an order charges your balance:
  // const { order } = await api.add({ service: 42, link: 'https://www.instagram.com/yourname/', quantity: 1000 });
  // console.log(await api.status(order));
}
