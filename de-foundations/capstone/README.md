# Phase 1 capstone — a tested Python ingestion script

This is the second half of the Phase 1 milestone. **No solution is provided, on
purpose.** It's the first thing in this course that is entirely yours, and the first
thing you'll put on your CV and talk about in interviews.

## The job

Pull every order from the fake orders API, which fails on purpose, and land it in a
local SQLite "warehouse" correctly, repeatably and observably.

```
python capstone/fake_api.py        # terminal 1: start the API (see its docstring)
python -m orders_ingest --since 2025-01-01   # terminal 2: your script
```

## Requirements

### Extract
- [ ] Page through `/orders` until `total_pages` (page_size 200).
- [ ] Every request has a timeout (≤ 3 s), sends `X-API-Key`, and goes through retry
      with exponential backoff + jitter for 429/5xx/timeouts. 429 honours `Retry-After`.
- [ ] 400/401/404 fail immediately with a clear error. No retrying.
- [ ] API key read from an environment variable (`ORDERS_API_KEY`), never hard-coded.

### Transform
- [ ] Flatten into two tables at clear grains: `stg_orders` (one row per order) and
      `stg_order_items` (one row per order line, with `order_id`).
- [ ] Typed with dataclasses; computed `net_amount` per line.
- [ ] Invalid records (e.g. quantity ≤ 0, unknown status) go to a `rejected` list with
      a reason — counted and logged, not silently dropped.

### Load
- [ ] Write to `data/warehouse.db`. Create tables if they don't exist, with primary keys.
- [ ] **Idempotent:** running twice gives the same row counts as running once. Use
      upsert (`INSERT … ON CONFLICT(order_id) DO UPDATE …`), not blind inserts.
- [ ] **Incremental:** `--since YYYY-MM-DD` loads only orders from that date (the API's
      `updated_since`). Store the high-watermark of the last successful run in a
      `_load_state` table and use it when `--since` isn't given.
- [ ] Load each run in a single transaction: a crash halfway leaves the previous state intact.

### Operate
- [ ] `logging` (not print): pages fetched, retries, rows loaded, rows rejected, duration.
- [ ] Exit code 0 on success, non-zero on failure (so a scheduler can alert on it).
- [ ] Reconciliation at the end: total `net_amount` in `stg_order_items` for completed
      orders must equal the SQL 03 q4 total from `shop.db`. Log PASS/FAIL.

### Engineer
- [ ] Project layout from Python 05 (`src/orders_ingest/{extract,transform,load,cli}.py`,
      `tests/`, `pyproject.toml`), dependencies managed with `uv` or `venv` + `requirements.txt`.
- [ ] `pytest` tests for: pagination, retry (fake sleep — no real waiting), transform
      edge cases, idempotent load (run twice against a `tmp_path` database), incremental
      watermark. Tests must not need the API running — inject a fake fetcher.
- [ ] A README: how to run, design decisions (why upsert, why this grain, why these
      retries), and what you'd change for 100× the data.
- [ ] In its own GitHub repo, built through small PRs with conventional commits.

## Done means

```
pytest                                   # all green, < 5 seconds
python -m orders_ingest --since 2024-01-01   # with --chaos 0.3 on the API: still succeeds
python -m orders_ingest --since 2024-01-01   # again: identical row counts
```

and you can explain every line to an interviewer without notes.

## Interview questions this project must let you answer

1. What happens if your script dies on page 7 of 10? What happens on the re-run?
2. Why exponential backoff and not "retry every second"? What's jitter for?
3. What would change if the API used cursors instead of page numbers? Why are cursors safer?
4. How do you know the data you loaded is complete and correct?
5. An order's status changes from `pending` to `completed` a week later. Does your
   incremental load pick it up? (Hint: think about what `updated_since` should really
   filter on — this is Phase 2's CDC topic.)
