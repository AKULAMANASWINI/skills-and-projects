# SQL 05 — Window functions (roadmap: "Advanced SQL")

**Goal:** rankings, running totals, previous/next row comparisons — the #1 topic in
data engineering SQL interviews. Exercises: `sql/exercises/05_window_functions.sql` (10).

## The idea

`GROUP BY` collapses rows. A **window function** computes across a set of related
rows but **keeps every row**:

```sql
SELECT order_id, customer_id, order_date,
       COUNT(*) OVER (PARTITION BY customer_id) AS customer_total_orders
FROM orders;
```

Every order row stays, and each one also carries its customer's total.

Anatomy: `function() OVER (PARTITION BY … ORDER BY … frame)`

- `PARTITION BY` — split rows into groups (like GROUP BY, without collapsing). Optional.
- `ORDER BY` — order inside each partition. Needed for ranking, LAG/LEAD, running totals.
- frame — which rows around the current one to include (below).

## Ranking

```sql
SELECT category, name, unit_price,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY unit_price DESC) AS rn,
       RANK()       OVER (PARTITION BY category ORDER BY unit_price DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY unit_price DESC) AS drnk
FROM products;
```

For prices 100, 90, 90, 80:

| | 100 | 90 | 90 | 80 |
|---|---|---|---|---|
| ROW_NUMBER | 1 | 2 | 3 | 4 |
| RANK | 1 | 2 | 2 | 4 |
| DENSE_RANK | 1 | 2 | 2 | 3 |

**Top-N per group** — you can't use a window function in WHERE (it's computed after
WHERE), so wrap it:

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY unit_price DESC) AS rn
  FROM products
)
SELECT category, name FROM ranked WHERE rn <= 2;
```

**Deduplication** — the pattern you'll use in almost every ingestion pipeline:
"keep the latest row per key":

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
  FROM orders
)
SELECT * FROM ranked WHERE rn = 1;   -- each customer's most recent order
```

Note the tie-breaker `order_id DESC`. Without it, two orders on the same day give a
non-deterministic result — the pipeline picks a different row each run.

## LAG / LEAD — look at the previous / next row

```sql
SELECT customer_id, order_date,
       LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS prev_order_date
FROM orders;
```

`LAG(col, 2)` goes back 2 rows; `LAG(col, 1, 0)` returns 0 instead of NULL for the
first row. Use for "days since last order", month-over-month change, gap detection.

## FIRST_VALUE / LAST_VALUE

```sql
FIRST_VALUE(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)  -- first order date
```

`LAST_VALUE` with only ORDER BY gives the *current* row, not the last — because of
the default frame. Read on.

## Frames: ROWS vs RANGE

When a window has `ORDER BY`, the default frame is
`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — "everything from the start up to me".
That's why `SUM(x) OVER (ORDER BY d)` is a **running total**.

```sql
-- running total
SUM(revenue) OVER (ORDER BY month)
-- 3-month moving average: this row and the 2 before it
AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
-- whole partition (fixes LAST_VALUE)
LAST_VALUE(x) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

**ROWS vs RANGE**: `ROWS` counts physical rows. `RANGE` treats rows with the **same
ORDER BY value as one peer group**. With duplicate dates, a `RANGE` running total
jumps by the whole day at once on every row of that day; a `ROWS` total increases
row by row. If your ORDER BY values can tie and you want row-by-row, say `ROWS`.

## Where window functions run

**FROM → WHERE → GROUP BY → HAVING → window functions → SELECT → ORDER BY → LIMIT**

So you can put a window *over an aggregate*:

```sql
SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS n,
       SUM(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', order_date)) AS running_n
FROM orders
GROUP BY month;
```

Legal, but hard to read. Prefer a CTE that aggregates, then the window on top.

## Exercises

`python sql/check.py 05`. Do these twice — once now, once a week later without
looking at your first answers.
