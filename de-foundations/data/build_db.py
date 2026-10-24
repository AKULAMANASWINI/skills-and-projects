"""Build the practice database (shop.db) and the messy raw files used by the course.

Run once from the de-foundations folder:

    python data/build_db.py

It is deterministic: the same seed always produces the same data, so the SQL
checker's expected answers never drift.
"""

import csv
import json
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "shop.db"
RAW_DIR = HERE / "raw"

rng = random.Random(42)

FIRST = ["Asha", "Ben", "Chen", "Divya", "Elena", "Farid", "Grace", "Hiro", "Isha", "Jonas",
         "Kavya", "Liam", "Maya", "Nikhil", "Olga", "Priya", "Quinn", "Ravi", "Sara", "Tomas",
         "Uma", "Vikram", "Wen", "Ximena", "Yusuf", "Zara"]
LAST = ["Akula", "Brown", "Chopra", "Diaz", "Evans", "Fischer", "Gupta", "Hansen", "Iyer",
        "Johnson", "Kim", "Lopez", "Menon", "Nair", "Okafor", "Patel", "Reddy", "Singh",
        "Tanaka", "Weber"]
CITIES = [("Hyderabad", "India"), ("Bengaluru", "India"), ("Pune", "India"),
          ("Seattle", "USA"), ("Austin", "USA"), ("New York", "USA"),
          ("London", "UK"), ("Manchester", "UK"), ("Berlin", "Germany"),
          ("Dublin", "Ireland")]
CATEGORIES = {
    "Electronics": [("Wireless Mouse", 25.0), ("Mechanical Keyboard", 89.0), ("USB-C Hub", 39.0),
                    ("27in Monitor", 249.0), ("Noise-Cancelling Headphones", 199.0),
                    ("Webcam HD", 59.0), ("Portable SSD 1TB", 109.0), ("Laptop Stand", 35.0)],
    "Books": [("SQL Cookbook", 45.0), ("Designing Data-Intensive Applications", 52.0),
              ("The Data Warehouse Toolkit", 60.0), ("Fluent Python", 55.0),
              ("Fundamentals of Data Engineering", 49.0), ("Python Crash Course", 32.0)],
    "Home": [("Desk Lamp", 29.0), ("Ergonomic Chair", 329.0), ("Standing Desk", 499.0),
             ("Plant Pot", 12.0), ("Wall Clock", 22.0), ("Throw Blanket", 40.0)],
    "Kitchen": [("Coffee Grinder", 79.0), ("French Press", 28.0), ("Chef Knife", 65.0),
                ("Cast Iron Pan", 45.0), ("Kettle", 38.0), ("Water Bottle", 18.0)],
    "Sports": [("Yoga Mat", 30.0), ("Dumbbell Set", 120.0), ("Running Shoes", 95.0),
               ("Resistance Bands", 20.0), ("Jump Rope", 10.0), ("Foam Roller", 25.0)],
}
STATUSES = ["completed"] * 80 + ["cancelled"] * 8 + ["returned"] * 6 + ["pending"] * 6
CHANNELS = ["web"] * 6 + ["mobile"] * 3 + ["store"]

START = date(2024, 1, 1)
END = date(2025, 12, 31)


def rand_date(lo: date, hi: date) -> date:
    return lo + timedelta(days=rng.randint(0, (hi - lo).days))


def build() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            first_name    TEXT NOT NULL,
            last_name     TEXT NOT NULL,
            email         TEXT,              -- can be NULL (never captured)
            city          TEXT,              -- can be NULL
            country       TEXT NOT NULL,
            signup_date   TEXT NOT NULL,     -- ISO date 'YYYY-MM-DD'
            referred_by   INTEGER REFERENCES customers(customer_id)  -- NULL = not referred
        );
        CREATE TABLE products (
            product_id    INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            category      TEXT NOT NULL,
            unit_price    REAL NOT NULL,
            is_active     INTEGER NOT NULL   -- 1 = still sold, 0 = discontinued
        );
        CREATE TABLE orders (
            order_id      INTEGER PRIMARY KEY,
            customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
            order_date    TEXT NOT NULL,     -- ISO date 'YYYY-MM-DD'
            status        TEXT NOT NULL,     -- completed / cancelled / returned / pending
            channel       TEXT NOT NULL      -- web / mobile / store
        );
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id      INTEGER NOT NULL REFERENCES orders(order_id),
            product_id    INTEGER NOT NULL REFERENCES products(product_id),
            quantity      INTEGER NOT NULL,
            unit_price    REAL NOT NULL,     -- price charged at the time of the order
            discount      REAL NOT NULL      -- fraction, e.g. 0.10 = 10% off
        );
        """
    )

    # Products
    products = []
    pid = 1
    for category, items in CATEGORIES.items():
        for name, price in items:
            products.append((pid, name, category, price, 0 if rng.random() < 0.12 else 1))
            pid += 1
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

    # Customers
    customers = []
    for cid in range(1, 201):
        first, last = rng.choice(FIRST), rng.choice(LAST)
        city, country = rng.choice(CITIES)
        email = None if rng.random() < 0.07 else f"{first}.{last}{cid}@example.com".lower()
        if rng.random() < 0.05:
            city = None
        referred_by = rng.randint(1, cid - 1) if cid > 10 and rng.random() < 0.25 else None
        signup = rand_date(START - timedelta(days=365), END - timedelta(days=60))
        customers.append((cid, first, last, email, city, country, signup.isoformat(), referred_by))
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", customers)

    # Orders + items. ~15 customers never order (useful for anti-joins).
    never_order = set(rng.sample(range(1, 201), 15))
    buyers = [c for c in customers if c[0] not in never_order]
    weights = [rng.paretovariate(1.5) for _ in buyers]  # a few heavy buyers
    order_rows, item_rows = [], []
    oid, iid = 1, 1
    for _ in range(2000):
        cust = rng.choices(buyers, weights=weights)[0]
        signup = date.fromisoformat(cust[6])
        lo = max(signup, START)
        odate = rand_date(lo, END)
        order_rows.append((oid, cust[0], odate.isoformat(), rng.choice(STATUSES), rng.choice(CHANNELS)))
        for prod in rng.sample(products, rng.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]):
            price = prod[3] if odate.year == 2024 else round(prod[3] * 1.05, 2)  # 5% price rise in 2025
            discount = rng.choice([0.0] * 7 + [0.05, 0.10, 0.20])
            item_rows.append((iid, oid, prod[0], rng.choices([1, 2, 3], weights=[75, 20, 5])[0], price, discount))
            iid += 1
        oid += 1
    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", order_rows)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)", item_rows)
    con.commit()
    con.close()

    build_raw_files(customers)
    print(f"Built {DB_PATH.name}: {len(customers)} customers, {len(products)} products, "
          f"{len(order_rows)} orders, {len(item_rows)} order items")
    print(f"Wrote messy raw files to {RAW_DIR.relative_to(HERE.parent)}/")


def build_raw_files(customers) -> None:
    """A deliberately dirty CSV export, the kind real source systems hand you."""
    RAW_DIR.mkdir(exist_ok=True)
    path = RAW_DIR / "customers_export.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Customer ID", " First Name", "last_name ", "EMAIL", "Signup Date", "Lifetime Value"])
        for c in customers[:60]:
            cid, first, last, email, _, _, signup, _ = c
            r = rng.random()
            if r < 0.1:
                first = f"  {first.upper()} "          # stray whitespace and case
            if r > 0.9:
                signup = date.fromisoformat(signup).strftime("%d/%m/%Y")  # wrong date format
            ltv = f"{rng.uniform(0, 3000):.2f}"
            if rng.random() < 0.08:
                ltv = rng.choice(["", "N/A", "unknown"])                  # junk numerics
            w.writerow([cid, first, last, email or "", signup, ltv])
        w.writerow([5, "Elena", "Evans", "dup@example.com", "2024-02-02", "10.00"])  # duplicate id
        w.writerow(["C-61", "Test", "User", "test@example", "2024-01-01", "5"])      # non-numeric id
        w.writerow([62, "Mei", "Tanaka", "MEI@EXAMPLE.COM ", "March 3rd", "12"])     # unparseable date
        w.writerow(["", "", "", "", "", ""])                                         # blank row

    events = []
    for i in range(1, 26):
        events.append({"event_id": i, "user": {"id": rng.randint(1, 200), "country": rng.choice(CITIES)[1]},
                       "type": rng.choice(["page_view", "add_to_cart", "purchase"]),
                       "ts": f"2025-06-{rng.randint(1, 30):02d}T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00Z",
                       "props": {"amount": round(rng.uniform(5, 300), 2)} if rng.random() < 0.4 else {}})
    (RAW_DIR / "events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build()
