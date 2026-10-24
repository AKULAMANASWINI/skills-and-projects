# Python 03 — Functions properly, and handling errors

**Goal:** write functions that survive bad input — because every real source sends
bad input. Exercises: `ex03_functions_errors.py`.

## Arguments

```python
def load(table, *, schema="raw", dry_run=False):   # after * : keyword-only
    ...

load("orders", schema="staging")    # clear at the call site
load("orders", "staging")           # TypeError — forced to name it. Good.
```

- Positional args, defaults, keyword-only args (after `*`).
- `*args` collects extra positional args into a tuple; `**kwargs` collects extra
  keyword args into a dict. You'll read these more than write them.
- Return several values as a tuple: `return good_rows, bad_rows` → `good, bad = split(rows)`.

## Scope

Variables created inside a function exist only inside it. Functions should take
inputs as arguments and give outputs via `return` — not read and modify global
variables. That's what makes them testable (lesson 06).

## Exceptions

When something goes wrong Python **raises** an exception and stops, unless you
**catch** it:

```python
try:
    amount = float(raw)
except ValueError:
    amount = None
```

Common ones: `ValueError` (bad value: `int("abc")`), `KeyError` (missing dict key),
`TypeError` (wrong type: `"a" + 1`), `FileNotFoundError`, `ZeroDivisionError`.

Rules a reviewer will hold you to:

1. **Catch the specific exception**, never bare `except:` — it also swallows typos
   and Ctrl+C.
2. **Don't silently swallow.** If you skip a bad row, count it or log it. A pipeline
   that "succeeds" by dropping 30% of rows is worse than one that crashes.
3. **Raise your own** when input breaks a contract:

```python
def parse_quantity(raw: str) -> int:
    q = int(raw)
    if q <= 0:
        raise ValueError(f"quantity must be positive, got {q}")
    return q
```

`try / except / else / finally`: `else` runs if nothing failed, `finally` always runs
(cleanup — closing connections).

## Reading a traceback

```
Traceback (most recent call last):
  File "ingest.py", line 12, in <module>
    total += float(row["amount"])
ValueError: could not convert string to float: 'N/A'
```

Read from the **bottom**: the error type and message, then the line that raised it.
Then work upward to see how you got there.

## Parsing strings — the daily work

```python
raw = " 1,299.50 "
float(raw.strip().replace(",", ""))     # 1299.5

from datetime import datetime, date
datetime.strptime("24/01/2028", "%d/%m/%Y").date()   # date(2028, 1, 24)
date.fromisoformat("2028-01-24")
d.isoformat()                                         # "2028-01-24"
```

`strptime` = string **p**arse time; `strftime` = string **f**ormat time (same codes
as SQLite's `strftime` in SQL 02).

## Exercises

`python python/check.py ex03`
