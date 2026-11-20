"""FalconGrow API v2 — cliente mínimo en Python (solo biblioteca estándar).

Minimal FalconGrow API v2 client in Python (standard library only).
Docs: https://www.falcongrow.com/api-docs

Uso / usage:
    FALCONGROW_API_KEY=... python falcongrow_api.py
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://www.falcongrow.com/api/v2"


class FalconGrowError(Exception):
    """La API respondió con un campo "error" / the API returned an "error" field."""


class FalconGrowAPI:
    def __init__(self, api_key: str, timeout: float = 30.0):
        self.api_key = api_key
        self.timeout = timeout

    def _call(self, action: str, **params):
        data = {"key": self.api_key, "action": action}
        data.update({k: v for k, v in params.items() if v is not None})
        body = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(API_URL, data=body, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    result = json.loads(resp.read().decode())
                break
            except urllib.error.HTTPError as exc:
                # 429: límite de 120 req/min por clave / 120 req/min per key
                if exc.code == 429 and attempt < 2:
                    time.sleep(int(exc.headers.get("Retry-After", "5")))
                    continue
                raise
        # Los errores llegan con HTTP 200 / errors come with HTTP 200
        if isinstance(result, dict) and "error" in result:
            raise FalconGrowError(result["error"])
        return result

    def services(self):
        return self._call("services")

    def balance(self):
        return self._call("balance")

    def add(self, service: int, link: str, quantity: int, runs: int = None, interval: int = None):
        return self._call("add", service=service, link=link, quantity=quantity, runs=runs, interval=interval)

    def status(self, order: int):
        return self._call("status", order=order)

    def multi_status(self, orders):
        return self._call("status", orders=",".join(str(o) for o in orders))

    def refill(self, order: int):
        return self._call("refill", order=order)

    def cancel(self, orders):
        return self._call("cancel", orders=",".join(str(o) for o in orders))


if __name__ == "__main__":
    api = FalconGrowAPI(os.environ.get("FALCONGROW_API_KEY", "YOUR_API_KEY"))
    print("balance:", api.balance())
    catalog = api.services()
    print(f"{len(catalog)} services; first:", catalog[0] if catalog else None)
    # Crear un pedido cobra de tu saldo / creating an order charges your balance:
    # order = api.add(service=42, link="https://www.instagram.com/yourname/", quantity=1000)
    # print(api.status(order["order"]))
