# SQL 02 — Summarising: aggregates, GROUP BY, HAVING, CASE

**Goal:** answer "how many / how much / per what" questions — 80% of real reporting.
**Time:** ~6 hours. Exercises: `sql/exercises/02_aggregate_group.sql` (8).

## Aggregate functions collapse many rows into one

```sql
SELECT COUNT(*)            AS orders,          -- counts rows
       COUNT(DISTINCT customer_id) AS buyers,   -- counts unique non-NULL values
       MIN(order_date)     AS first_order,
       MAX(order_date)     AS last_order
FROM orders;
```

`SUM`, `AVG`, `MIN`, `MAX` and `COUNT(column)` **ignore NULLs**. `COUNT(*)` does not.
So `COUNT(*) - COUNT(email)` = number of customers with no email.

## GROUP BY — one output row per group

```sql
SELECT status, COUNT(*) AS n
FROM orders
GROUP BY status
ORDER BY n DESC;
```

Rule: every column in SELECT must either be **in the GROUP BY** or **inside an
aggregate**. `SELECT status, channel, COUNT(*) … GROUP BY status` is an error in
Postgres/Snowflake/SQL Server (SQLite silently returns a random channel — don't
learn the bad habit).

Group by several columns to get one row per combination:

```sql
SELECT strftime('%Y', order_date) AS yr, channel, COUNT(*) AS n
FROM orders
GROUP BY yr, channel;
```

## Revenue in this database

Revenue for an order line = `quantity * unit_price * (1 - discount)`.
That expression lives on `order_items`. You'll join it to `orders` in lesson 03;
for now, aggregate it on its own:

```sql
SELECT product_id, ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
FROM order_items
GROUP BY product_id;
```

## HAVING — filter groups (WHERE filters rows)

```sql
SELECT customer_id, COUNT(*) AS n_orders
FROM orders
WHERE status = 'completed'     -- before grouping: which rows count
GROUP BY customer_id
HAVING COUNT(*) >= 20;          -- after grouping: which groups survive
```

Updated evaluation order — learn this cold:

**FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT**

## CASE — if/else inside a query

```sql
SELECT name,
       CASE
         WHEN unit_price < 30  THEN 'budget'
         WHEN unit_price < 100 THEN 'mid'
         ELSE 'premium'
       END AS price_band
FROM products;
```

The most useful trick in reporting is **conditional aggregation** — CASE inside SUM:

```sql
SELECT channel,
       COUNT(*)                                             AS orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_pct
FROM orders
GROUP BY channel;
```

Note `100.0` — integer division (`7 / 2 = 3`) is a classic silent bug. Make one side
a decimal.

## Dates in SQLite

SQLite stores our dates as ISO text. The functions you need:

| want | SQLite | Postgres / Snowflake equivalent |
|---|---|---|
| year | `strftime('%Y', d)` | `EXTRACT(YEAR FROM d)` |
| month bucket | `strftime('%Y-%m', d)` | `DATE_TRUNC('month', d)` |
| add days | `date(d, '+7 day')` | `d + INTERVAL '7 day'` |
| days between | `julianday(a) - julianday(b)` | `a - b` / `DATEDIFF` |

Every engine spells date functions differently. The concepts transfer; look up the
syntax per engine. Don't memorise all dialects.

## Exercises

`python sql/check.py 02`
