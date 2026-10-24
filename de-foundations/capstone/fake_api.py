"""A deliberately unreliable local orders API for the capstone. Standard library only.

    python capstone/fake_api.py                # http://localhost:8765
    python capstone/fake_api.py --chaos 0.3    # fail more often
    python capstone/fake_api.py --chaos 0      # never fail (for debugging)

Endpoint
    GET /orders?page=1&page_size=100&updated_since=2025-06-01
    Header  X-API-Key: dev-key        (anything else -> 401)

Response 200
    {"data": [{"order_id": 1, "customer_id": 7, "order_date": "...", "status": "...",
               "channel": "...", "items": [{"product_id": 3, "quantity": 1,
               "unit_price": 25.0, "discount": 0.0}, ...]}, ...],
     "page": 1, "page_size": 100, "total_pages": 20, "total_rows": 2000}

Misbehaviour (random, controlled by --chaos):
    503 Service Unavailable
    429 Too Many Requests with a Retry-After header (seconds)
    a response that takes 5 seconds (use a client timeout!)
    page_size above 200 -> 400 Bad Request (don't retry that)
"""

import argparse
import json
import random
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DB = Path(__file__).resolve().parent.parent / "data" / "shop.db"
API_KEY = "dev-key"


def load_orders(updated_since: str | None) -> list[dict]:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    where, params = "", []
    if updated_since:
        where, params = "WHERE order_date >= ?", [updated_since]
    orders = [dict(r) for r in con.execute(
        f"SELECT order_id, customer_id, order_date, status, channel FROM orders {where} ORDER BY order_id", params)]
    items: dict[int, list] = {}
    for r in con.execute("SELECT order_id, product_id, quantity, unit_price, discount FROM order_items ORDER BY order_item_id"):
        items.setdefault(r["order_id"], []).append(
            {"product_id": r["product_id"], "quantity": r["quantity"], "unit_price": r["unit_price"], "discount": r["discount"]})
    for o in orders:
        o["items"] = items.get(o["order_id"], [])
    return orders


class Handler(BaseHTTPRequestHandler):
    chaos = 0.15

    def send_json(self, status: int, body: dict, headers: dict | None = None) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):  # noqa: N802 (http.server naming)
        url = urlparse(self.path)
        if url.path == "/health":
            return self.send_json(200, {"status": "ok"})
        if url.path != "/orders":
            return self.send_json(404, {"error": "not found"})
        if self.headers.get("X-API-Key") != API_KEY:
            return self.send_json(401, {"error": "missing or wrong X-API-Key"})
        q = parse_qs(url.query)
        try:
            page = int(q.get("page", ["1"])[0])
            page_size = int(q.get("page_size", ["100"])[0])
        except ValueError:
            return self.send_json(400, {"error": "page and page_size must be integers"})
        if page < 1 or not 1 <= page_size <= 200:
            return self.send_json(400, {"error": "page >= 1 and 1 <= page_size <= 200"})

        roll = random.random()
        if roll < self.chaos * 0.5:
            return self.send_json(503, {"error": "service unavailable, try again"})
        if roll < self.chaos * 0.8:
            return self.send_json(429, {"error": "rate limited"}, {"Retry-After": str(random.randint(1, 3))})
        if roll < self.chaos:
            time.sleep(5)

        rows = load_orders(q.get("updated_since", [None])[0])
        total_pages = max(1, -(-len(rows) // page_size))
        start = (page - 1) * page_size
        self.send_json(200, {"data": rows[start:start + page_size], "page": page, "page_size": page_size,
                             "total_pages": total_pages, "total_rows": len(rows)})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--chaos", type=float, default=0.15, help="probability a request misbehaves (0-1)")
    args = ap.parse_args()
    if not DB.exists():
        raise SystemExit("data/shop.db is missing. Run:  python data/build_db.py")
    Handler.chaos = args.chaos
    print(f"Fake orders API on http://localhost:{args.port}/orders  (chaos={args.chaos}, key={API_KEY})")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
