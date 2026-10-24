# SQL 03 — Combining tables: JOINs

**Goal:** confidently combine tables and know exactly how many rows you'll get back.
**Time:** ~7 hours. This is the lesson that separates people who "know SQL" from
people who can be trusted with a pipeline. Exercises: `sql/exercises/03_joins.sql` (8).

## Why tables are split

`orders` stores `customer_id`, not the customer's name. If a customer changes their
email, you update **one** row in `customers`, not 40 rows in `orders`. The price
of that design: you must join to get the full picture. (Lesson 07 covers why.)

## INNER JOIN — only matching rows

```sql
SELECT o.order_id, o.order_date, c.first_name, c.country
FROM orders AS o
JOIN customers AS c            -- JOIN = INNER JOIN
  ON c.customer_id = o.customer_id;
```

- `o` and `c` are **table aliases**. Always prefix columns once you have >1 table.
- Rows with no match on the other side **disappear**.

## LEFT JOIN — keep everything on the left

```sql
SELECT c.customer_id, c.first_name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id;
```

Customers with no orders still appear, with `o.order_id` = NULL. That gives you the
**anti-join** — "rows in A with no match in B":

```sql
SELECT c.customer_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```

**Trap:** filtering the right table in WHERE turns a LEFT JOIN back into an INNER JOIN:

```sql
-- Loses customers with no completed orders, because their o.status is NULL:
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
-- Keeps them: put the right-table condition in ON
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
```

## Other joins (know they exist, rarely need)

- `RIGHT JOIN` — mirror of LEFT. Rewrite as LEFT; nobody likes reading RIGHT.
- `FULL OUTER JOIN` — keep unmatched from both sides. Used in reconciliation
  ("which ids are in source but not target, and vice versa").
- `CROSS JOIN` — every row × every row. Useful for building date × product grids.

## Self-join — a table joined to itself

`customers.referred_by` points at another customer:

```sql
SELECT c.first_name AS customer, r.first_name AS referrer
FROM customers AS c
JOIN customers AS r ON r.customer_id = c.referred_by;
```

## Row counts: the fan-out problem (the most important part)

Joining a one-row-per-order table to a many-rows-per-order table **multiplies** rows.

```sql
SELECT COUNT(*) FROM orders;                         -- 2000
SELECT COUNT(*) FROM orders o JOIN order_items i
  ON i.order_id = o.order_id;                         -- ~3400
```

Now `SUM` or `COUNT(*)` over that result counts orders more than once. Before any
join ask: **"what is the grain of each side — what does one row mean?"** and
**"what grain do I want out?"** If they differ, aggregate first, then join:

```sql
WITH order_totals AS (
  SELECT order_id, SUM(quantity * unit_price * (1 - discount)) AS order_value
  FROM order_items
  GROUP BY order_id
)
SELECT o.channel, COUNT(*) AS orders, ROUND(AVG(t.order_value), 2) AS avg_order_value
FROM orders o
JOIN order_totals t ON t.order_id = o.order_id
GROUP BY o.channel;
```

(`WITH … AS` is a CTE — lesson 04 — read it as "a named temporary result".)

In a real job, the same mistake produces a dashboard that over-reports revenue by
70% and nobody notices for a month. Checking row counts before/after every join is
a habit, not paranoia.

## Joining three or more tables

Chain them. Each `JOIN … ON` adds one table:

```sql
SELECT p.category, ROUND(SUM(i.quantity * i.unit_price * (1 - i.discount)), 2) AS revenue
FROM order_items i
JOIN orders   o ON o.order_id   = i.order_id
JOIN products p ON p.product_id = i.product_id
WHERE o.status = 'completed'
GROUP BY p.category;
```

## Exercises

`python sql/check.py 03`
