# Python 06 — Testing with pytest, and ingesting from APIs

Roadmap items: *paginated API ingestion, retries and backoff* + the "tested" in
"ship a tested Python ingestion script". Exercises: `ex06_api.py`.

## Why tests

A pipeline runs at 3am with nobody watching. Tests are how you know a change today
doesn't break the parsing you wrote last month. Interviewers for data engineering
roles ask "how did you test it?" about every project on your CV.

## pytest

```bash
pip install pytest        # or: uv add --dev pytest
pytest                    # finds tests/test_*.py, runs every def test_*()
pytest -k email -v        # only tests with "email" in the name, verbose
```

A test is a function that asserts:

```python
from transform import clean_email

def test_clean_email_lowercases_and_strips():
    assert clean_email("  A@B.COM ") == "a@b.com"

def test_clean_email_rejects_missing_at():
    assert clean_email("not-an-email") is None
```

Checking exceptions:

```python
import pytest

def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        parse_quantity("-1")
```

**Fixtures** give tests prepared inputs. `tmp_path` is built in — a fresh temporary
folder per test:

```python
def test_writes_clean_file(tmp_path):
    out = tmp_path / "clean.csv"
    clean_file("data/raw/customers_export.csv", out)
    assert out.exists()
```

The exercise files in this course are already pytest tests — once you've installed
pytest, `pytest python/tests` runs them all.

**What to test in a pipeline:** pure transform functions (most tests), edge cases
(empty input, NULLs, duplicates, bad dates), and one integration test that runs
the whole thing on a tiny fixture file. Don't hit real APIs in unit tests — inject a
fake (below).

## HTTP APIs

```python
import requests                       # pip install requests

resp = requests.get("https://api.example.com/orders", params={"page": 1}, timeout=10)
resp.raise_for_status()               # raise on 4xx/5xx
data = resp.json()
```

Always set `timeout` — without it a hung server hangs your pipeline forever.

Status codes that matter: `200` ok, `400` your request is wrong (don't retry),
`401/403` auth (don't retry), `404` not found, `429` rate-limited (retry, honour
`Retry-After`), `500/502/503/504` server trouble (retry).

## Pagination

APIs return data in pages. Three styles:

| style | request | stop when |
|---|---|---|
| page number | `?page=3&page_size=100` | empty page, or page > total_pages |
| offset | `?offset=200&limit=100` | fewer than limit rows returned |
| cursor | `?cursor=abc123` (from previous response's `next_cursor`) | `next_cursor` is null |

Cursor is the most robust: offsets shift if rows are inserted while you page.

## Retries with exponential backoff

```python
import time, random

def get_with_retry(fetch, max_attempts=5, base_delay=1.0):
    for attempt in range(1, max_attempts + 1):
        try:
            return fetch()
        except TransientError:
            if attempt == max_attempts:
                raise
            delay = base_delay * 2 ** (attempt - 1)        # 1, 2, 4, 8 ...
            time.sleep(delay + random.uniform(0, delay * 0.1))  # jitter
```

- Retry only **transient** failures (timeouts, 429, 5xx). Retrying a 400 just fails 5×.
- **Jitter** stops a thousand clients retrying at the exact same instant.
- Cap the attempts and total wait. Then fail loudly.

## Design for testability: inject dependencies

Notice `fetch` and (in the exercise) `sleep` are **arguments**. Tests pass a fake
fetch that fails twice then succeeds, and a fake sleep that records delays instead
of waiting. That's how you test retry logic in milliseconds.

## Exercises

`python python/check.py ex06` — then go to `capstone/`.
