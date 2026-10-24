# Python 05 — Idiomatic Python for data engineering

Roadmap item: *type hints, dataclasses, generators, context managers, virtualenv/uv,
project layout, logging over print*. Exercises: `ex05_idiomatic.py`.

## Virtual environments and uv

Each project gets its own isolated set of packages, so project A's `pandas 1.5`
doesn't break project B's `pandas 2.2`.

```bash
# the standard way
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install requests pytest
pip freeze > requirements.txt

# the modern way (much faster, what newer teams use)
pip install uv                   # or the installer at docs.astral.sh/uv
uv init my_pipeline && cd my_pipeline
uv add requests pytest           # writes pyproject.toml + uv.lock
uv run pytest
```

Never `pip install` into your system Python. Never commit `.venv/`.

## Project layout

```
my_pipeline/
  pyproject.toml          # name, dependencies, tool config
  src/my_pipeline/
    __init__.py
    extract.py            # one module per responsibility
    transform.py
    load.py
    cli.py                # entry point: parse args, call the above
  tests/
    test_transform.py
  README.md
```

A **module** is a `.py` file; `import transform` / `from transform import clean_row`.
Code that should only run when executed directly goes under:

```python
if __name__ == "__main__":
    main()
```

## Type hints

```python
def clean_email(raw: str | None) -> str | None: ...
def load(rows: list[dict[str, str]], table: str) -> int: ...
```

Python doesn't enforce them at runtime. They document intent, power editor
autocomplete, and `mypy`/`pyright` catch bugs with them. Write them on every function.

## dataclasses — a typed record

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)          # frozen = immutable, like a row should be
class Customer:
    customer_id: int
    email: str | None
    signup_date: date

c = Customer(1, "a@b.com", date(2024, 1, 5))
c.email                           # attribute access, autocomplete, typo-safe
```

Better than dicts once the shape is known: `c.emial` is caught by your editor,
`row["emial"]` explodes at 3am.

## Generators — process data that doesn't fit in memory

A function with `yield` produces values **one at a time, on demand**:

```python
def read_rows(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n")

for row in read_rows("huge.csv"):    # never holds the whole file
    ...
```

Generator expressions: `total = sum(r["amount"] for r in rows)` (round brackets, no list built).
This is the core idea behind streaming and chunked processing — and behind Airflow/Spark
being lazy.

## Context managers

Anything used with `with`. Write your own for setup/teardown:

```python
from contextlib import contextmanager
import time

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label} took {time.perf_counter() - start:.2f}s")

with timed("load"):
    load_everything()
```

## logging, not print

```python
import logging
log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log.info("loaded %d rows into %s", n, table)      # lazy formatting
log.warning("skipped %d rows with bad dates", bad)
log.exception("load failed")                       # inside except: includes traceback
```

Logs have timestamps and levels, go to files or log platforms, and can be turned up
or down without editing code. In production, `print` is invisible noise.

## Exercises

`python python/check.py ex05`
