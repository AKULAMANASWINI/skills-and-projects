# SQL 04 — Building queries in steps: subqueries, CTEs, set operations

**Goal:** break a hard question into small named steps — which is how every dbt
model you'll write in Phase 2 looks. Exercises: `sql/exercises/04_subqueries_ctes.sql` (7).

## Subqueries

A query inside a query. Three places they show up:

```sql
-- 1. A single value (scalar subquery)
SELECT name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products);

-- 2. A list for IN
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE channel = 'store');

-- 3. A table in FROM (a "derived table" — must have an alias)
SELECT AVG(n) FROM (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) AS t;
```

## EXISTS / NOT EXISTS

"Is there at least one matching row?" — the cleanest anti-join:

```sql
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

**Trap:** `NOT IN (subquery)` returns **zero rows** if the subquery contains a single
NULL. `NOT EXISTS` doesn't have that problem. Prefer `NOT EXISTS`.

```sql
-- referred_by contains NULLs, so this returns nothing:
SELECT * FROM customers WHERE customer_id NOT IN (SELECT referred_by FROM customers);
```

## CTEs — WITH … AS

Same power as a derived table, but named, top-to-bottom, readable:

```sql
WITH completed AS (
  SELECT * FROM orders WHERE status = 'completed'
),
per_customer AS (
  SELECT customer_id, COUNT(*) AS n_orders, MIN(order_date) AS first_order
  FROM completed
  GROUP BY customer_id
)
SELECT strftime('%Y-%m', first_order) AS cohort, COUNT(*) AS new_buyers
FROM per_customer
GROUP BY cohort
ORDER BY cohort;
```

Write hard queries this way: one CTE per idea, check each one's output
(`SELECT * FROM per_customer LIMIT 10`) before stacking the next. Debugging a
60-line query in one go is how afternoons disappear.

## Set operations

Stack results **vertically** (joins combine horizontally). Both sides need the same
number and types of columns.

| operator | result |
|---|---|
| `UNION ALL` | everything from both, duplicates kept — fast, use by default |
| `UNION` | duplicates removed (costs a sort/hash) |
| `INTERSECT` | rows in both |
| `EXCEPT` (`MINUS` in Oracle/Snowflake) | rows in the first but not the second |

`EXCEPT` is a data engineer's favourite test: `SELECT … FROM source EXCEPT SELECT … FROM target`
should be empty after a load.

## Exercises

`python sql/check.py 04`
