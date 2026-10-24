# SQL 01 — Reading data: SELECT, WHERE, ORDER BY

**Goal:** by the end you can pull any subset of rows and columns from one table.
**Time:** ~5 hours across 2–3 days. Exercises: `sql/exercises/01_select_filter.sql` (8).

## What a database is, in one paragraph

A relational database stores data in **tables**. A table has **columns** (fixed,
named, typed: `order_date TEXT`, `quantity INTEGER`) and **rows** (one record each).
SQL is the language you use to ask questions of those tables. You describe *what*
you want; the database works out *how* to get it. That last point matters later
(lesson 06) — for now, just ask clearly.

Our practice database `data/shop.db` is a small online shop:

| table | one row is… | key columns |
|---|---|---|
| `customers` | a person who signed up | `customer_id`, `email` (may be NULL), `city` (may be NULL), `country`, `signup_date`, `referred_by` |
| `products` | something we sell | `product_id`, `name`, `category`, `unit_price`, `is_active` |
| `orders` | one checkout | `order_id`, `customer_id`, `order_date`, `status`, `channel` |
| `order_items` | one product line inside an order | `order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price`, `discount` |

Look at it yourself before reading on:

```
python sql/run.py
sql> .tables
sql> .schema orders
sql> SELECT * FROM orders LIMIT 5;
```

## SELECT … FROM

```sql
SELECT name, category, unit_price     -- which columns
FROM products;                         -- which table
```

- `SELECT *` means every column. Fine for exploring, **never** in a pipeline:
  if someone adds a column upstream, your job silently changes shape.
- You can compute: `SELECT name, unit_price * 1.18 AS price_with_tax FROM products;`
  `AS` gives the output column a name (an **alias**).
- `SELECT DISTINCT country FROM customers;` removes duplicate rows from the output.

## WHERE — filter rows

```sql
SELECT order_id, order_date, status
FROM orders
WHERE status = 'completed'
  AND channel <> 'store'           -- <> means "not equal" (!= also works)
  AND order_date >= '2025-01-01';  -- ISO dates compare correctly as text
```

Operators you'll use daily:

| want | write |
|---|---|
| one of several values | `status IN ('cancelled', 'returned')` |
| range (inclusive both ends) | `unit_price BETWEEN 20 AND 50` |
| pattern | `name LIKE '%Python%'` — `%` = any characters, `_` = exactly one |
| combine | `AND`, `OR`, `NOT` — **use brackets when mixing AND/OR** |

The AND/OR trap:

```sql
-- WRONG: AND binds tighter, so this is  category='Books' OR (category='Home' AND price > 100)
WHERE category = 'Books' OR category = 'Home' AND unit_price > 100
-- RIGHT
WHERE (category = 'Books' OR category = 'Home') AND unit_price > 100
```

## NULL — the thing that trips everyone up

`NULL` means *unknown / missing*. It is not 0 and not `''`. Any comparison with NULL
gives NULL (neither true nor false), and WHERE only keeps rows that are **true**.

```sql
SELECT * FROM customers WHERE email = NULL;     -- returns nothing, ever
SELECT * FROM customers WHERE email IS NULL;    -- correct
SELECT * FROM customers WHERE email IS NOT NULL;
SELECT COALESCE(city, 'unknown') AS city FROM customers;  -- first non-NULL value
```

Sneaky version: `WHERE city <> 'London'` **drops** rows where city is NULL too,
because `NULL <> 'London'` is NULL, not true. Interviewers love this.

## ORDER BY and LIMIT

```sql
SELECT name, unit_price
FROM products
ORDER BY unit_price DESC, name ASC   -- ties on price broken by name
LIMIT 5;                              -- top 5
```

Without `ORDER BY`, row order is **not guaranteed** — even if it looks stable today.
A pipeline that relies on "the first row" without ORDER BY is a bug waiting to happen.

## The order SQL actually runs in

You *write* `SELECT … FROM … WHERE … ORDER BY … LIMIT`. The database *evaluates*:

1. `FROM` — pick the table
2. `WHERE` — filter rows
3. `SELECT` — compute output columns
4. `ORDER BY` — sort
5. `LIMIT` — cut

That is why you can't use a SELECT alias inside WHERE (it doesn't exist yet), but you
can use it in ORDER BY. This list grows in lesson 02 — memorise it then.

## Data-engineer habits starting today

- Format queries one clause per line, keywords in CAPS. Reviewers read SQL all day.
- Always check row counts: `SELECT COUNT(*) FROM …` before and after a filter.
- Before trusting a column, check its NULLs: `SELECT COUNT(*) FROM customers WHERE city IS NULL;`

## Exercises

Open `sql/exercises/01_select_filter.sql`, write each answer under its `-- @qN`
marker, then:

```
python sql/check.py 01
```

Don't open `sql/solutions/` until you've been stuck for 20 minutes *and* re-read
this lesson. Being stuck is the learning; reading the answer is not.
