# SQL 06 — Performance and execution plans

**Goal:** know *why* a query is slow and what to do about it, instead of guessing.
**Time:** ~5 hours. Exercises: `sql/exercises/06_performance.sql` (4 auto-checked
rewrites) plus the plan-reading tasks at the bottom of this file.

## How a database answers a query

You wrote *what*. The **query planner** picks *how*: which table to read first,
whether to use an index, which join algorithm. The result is an **execution plan**.
Reading plans is the skill; tuning is a consequence.

## Indexes

Without an index, finding `customer_id = 42` in `orders` means reading every row (a
**full table scan**). An index is a separate sorted structure (a **B-tree**) mapping
values → row locations, so the lookup takes a few steps instead of 2000.

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

| kind | what | when |
|---|---|---|
| B-tree (default) | sorted keys | `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix `LIKE 'abc%'` |
| composite | `(customer_id, order_date)` | filters on the first column, or both. Not the second alone (leftmost-prefix rule) |
| covering | index contains every column the query needs | the table itself never has to be read |
| partial | `CREATE INDEX … WHERE status = 'pending'` | you only ever query a small slice |

Indexes are not free: every INSERT/UPDATE must maintain them, and they take space.
In OLTP (app databases) you index carefully. In warehouses (Snowflake, BigQuery,
Fabric, Databricks — Phase 2/3) you mostly *don't* have B-tree indexes; you get
partitioning, clustering and file pruning instead. Same goal: **read less data**.

## Things that stop an index being used

```sql
WHERE strftime('%Y', order_date) = '2025'                     -- function on the column: scan
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01' -- range on raw column: index usable
WHERE name LIKE '%Mouse'                                       -- leading wildcard: scan
WHERE customer_id + 0 = 42                                     -- arithmetic on the column: scan
```

The rule: keep the indexed column **bare** on one side of the comparison
("sargable" predicates).

## Reading a plan

SQLite: `EXPLAIN QUERY PLAN <query>`. Postgres: `EXPLAIN ANALYZE <query>` (actually
runs it and shows real timings and row counts — the one you'll use most at work).

```
python sql/run.py "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42"
-- SCAN orders                     <- full scan

python sql/run.py "CREATE INDEX idx_orders_customer ON orders(customer_id)"
python sql/run.py "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42"
-- SEARCH orders USING INDEX idx_orders_customer (customer_id=?)
```

(Indexes you create persist in shop.db; `python data/build_db.py` resets everything.)

## Join algorithms

| algorithm | how | good when |
|---|---|---|
| nested loop | for each left row, look up matches on the right | one side small, or right side indexed on the join key |
| hash join | build a hash table from the smaller side, probe with the larger | big unsorted inputs, equality joins — the warehouse default |
| merge join | both sides sorted on the key, walk them together | inputs already sorted / indexed |

You don't pick the algorithm; the planner does, from **statistics**: row counts and
value distributions it keeps per table (`ANALYZE` refreshes them in SQLite/Postgres).
**Cardinality estimate** = the planner's guess at how many rows a step returns. Most
terrible plans come from a bad estimate — e.g. it thinks a filter keeps 10 rows,
picks a nested loop, and it actually keeps 2 million. In `EXPLAIN ANALYZE`, compare
`rows=` (estimate) to `actual rows=`; a 100× gap is your lead.

## Performance habits that matter more than tricks

1. Select only the columns you need (huge in columnar warehouses — lesson on file formats).
2. Filter early, aggregate before joining (lesson 03's fan-out fix is also a speed fix).
3. Prefer `UNION ALL` over `UNION` unless you need de-duplication.
4. Prefer `EXISTS` over `IN (big subquery)` / `COUNT(*) > 0`.
5. Measure. "I think it's faster" is not evidence; a plan and a timing are.

## Plan-reading tasks (not auto-checked — write your answers in your journal)

1. Run `EXPLAIN QUERY PLAN` on `SELECT * FROM orders WHERE customer_id = 42 AND order_date >= '2025-06-01'`.
   Create `(customer_id, order_date)` composite index. Run again. What changed?
2. With that index, does `WHERE order_date >= '2025-06-01'` alone use it? Why not?
3. Run the plan for the 3-table category revenue query from lesson 03. Which table
   is scanned, which are searched? Why that order?
4. Explain to an imaginary interviewer, in 4 sentences, what a covering index is and
   when it's a bad idea.
