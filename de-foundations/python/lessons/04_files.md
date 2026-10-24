# Python 04 — Files: paths, CSV, JSON, cleaning messy data

**Goal:** read a dirty file, clean it with explicit rules, write a clean one and
report what you rejected. That is ingestion in miniature.
Exercises: `ex04_files.py`, data in `data/raw/`.

## Paths

```python
from pathlib import Path

raw_dir = Path("data") / "raw"           # / joins paths on any OS
f = raw_dir / "customers_export.csv"
f.exists(), f.suffix, f.stem, f.name     # True, ".csv", "customers_export", "customers_export.csv"
list(raw_dir.glob("*.csv"))
f.read_text(encoding="utf-8")            # whole file as one string
```

Always pass `encoding="utf-8"` — the default differs on Windows and will bite you.

## with — files that always get closed

```python
with open(f, encoding="utf-8") as fh:
    for line in fh:              # one line at a time: works on files bigger than RAM
        ...
# fh is closed here, even if an exception happened
```

`with` is a **context manager** (lesson 05). Same pattern for DB connections and locks.

## CSV

Never `line.split(",")` — a quoted field `"Hyderabad, India"` breaks it. Use `csv`:

```python
import csv

with open(f, newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):      # each row is a dict keyed by the header
        print(row["EMAIL"])

with open("out.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["customer_id", "email"])
    w.writeheader()
    w.writerow({"customer_id": 1, "email": "a@b.com"})
```

Everything `csv` reads is a **string**. `"42"` is not `42`. Typing is your job.

## JSON

```python
import json
events = json.loads(Path("data/raw/events.json").read_text(encoding="utf-8"))  # str -> Python
json.dumps(obj, indent=2)                                                       # Python -> str
```

JSON maps to Python: object → dict, array → list, string → str, number → int/float,
true/false → True/False, null → None. APIs return nested JSON; warehouses want flat
rows. **Flattening** (`user.id` → `user_id`) is a core skill — exercise 4.

## Look at the mess first

Open `data/raw/customers_export.csv` in VS Code before writing any code. You'll find:

- headers with spaces and mixed case (`" First Name"`, `"last_name "`, `"EMAIL"`)
- names with stray whitespace and SHOUTING
- two date formats (`2024-03-05` and `05/03/2024`)
- `Lifetime Value` values like `""`, `"N/A"`, `"unknown"`
- a duplicate customer id, and a blank row

Real sources are like this. The rule: **decide each cleaning rule explicitly, write it
down, apply it in code, and count what each rule did.** Never "just fix it in Excel".

## Exercises

`python python/check.py ex04`. The last one writes `data/clean/customers.csv` — open
it and compare to the raw file.
