-- Reference solutions. Only open after a real attempt.

-- @q1
-- Each product with its price rank inside its category (most expensive = 1),
-- using DENSE_RANK. Columns: category, name, unit_price, price_rank.
SELECT category, name, unit_price,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY unit_price DESC) AS price_rank
FROM products;

-- @q2
-- The 2 most expensive products per category (ties broken by product_id ascending).
-- Columns: category, name.
WITH ranked AS (
  SELECT category, name,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY unit_price DESC, product_id) AS rn
  FROM products
)
SELECT category, name FROM ranked WHERE rn <= 2;

-- @q3
-- Each customer's most recent order (ties: highest order_id).
-- Columns: customer_id, order_id, order_date.
WITH ranked AS (
  SELECT customer_id, order_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
  FROM orders
)
SELECT customer_id, order_id, order_date FROM ranked WHERE rn = 1;

-- @q4
-- For customer_id 7: every order with the previous order's date.
-- Columns: order_id, order_date, prev_order_date. Order by order_date, order_id.
-- @ordered
SELECT order_id, order_date,
       LAG(order_date) OVER (ORDER BY order_date, order_id) AS prev_order_date
FROM orders
WHERE customer_id = 7
ORDER BY order_date, order_id;

-- @q5
-- Monthly completed-order count with a running total.
-- Columns: month ('YYYY-MM'), n, running_n. Order by month.
-- @ordered
WITH m AS (
  SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS n
  FROM orders
  WHERE status = 'completed'
  GROUP BY month
)
SELECT month, n, SUM(n) OVER (ORDER BY month) AS running_n
FROM m
ORDER BY month;

-- @q6
-- Monthly net revenue (completed orders, rounded 2) and its 3-month moving average
-- (this month + 2 previous, rounded 2). Columns: month, revenue, ma3. Order by month.
-- @ordered
WITH m AS (
  SELECT strftime('%Y-%m', o.order_date) AS month,
         SUM(i.quantity * i.unit_price * (1 - i.discount)) AS revenue
  FROM orders o
  JOIN order_items i ON i.order_id = o.order_id
  WHERE o.status = 'completed'
  GROUP BY month
)
SELECT month, ROUND(revenue, 2),
       ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS ma3
FROM m
ORDER BY month;

-- @q7
-- Month-over-month % change in completed-order count, rounded to 1 (NULL for the first month).
-- Columns: month, n, pct_change. Order by month.
-- @ordered
WITH m AS (
  SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS n
  FROM orders
  WHERE status = 'completed'
  GROUP BY month
)
SELECT month, n,
       ROUND(100.0 * (n - LAG(n) OVER (ORDER BY month)) / LAG(n) OVER (ORDER BY month), 1) AS pct_change
FROM m
ORDER BY month;

-- @q8
-- For each customer who ordered: first order date and last order date,
-- computed with FIRST_VALUE and LAST_VALUE (one row per customer).
-- Columns: customer_id, first_order, last_order.
SELECT DISTINCT customer_id,
       FIRST_VALUE(order_date) OVER w AS first_order,
       LAST_VALUE(order_date)  OVER w AS last_order
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY order_date
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);

-- @q9
-- Days between consecutive orders, per customer, averaged: customers with at least
-- 10 orders and their average gap in days rounded to 1.
-- Columns: customer_id, avg_gap_days.
WITH gaps AS (
  SELECT customer_id,
         julianday(order_date)
           - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id)) AS gap,
         COUNT(*) OVER (PARTITION BY customer_id) AS n
  FROM orders
)
SELECT customer_id, ROUND(AVG(gap), 1) AS avg_gap_days
FROM gaps
WHERE n >= 10
GROUP BY customer_id;

-- @q10
-- ROWS vs RANGE: for orders on '2025-03-01'..'2025-03-03' ordered by order_date,
-- return order_id, order_date, a ROWS running count and a RANGE running count.
-- Use ORDER BY order_date only inside both windows (no tiebreaker) for RANGE;
-- for ROWS use ORDER BY order_date, order_id. Order output by order_date, order_id.
-- @ordered
SELECT order_id, order_date,
       COUNT(*) OVER (ORDER BY order_date, order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_count,
       COUNT(*) OVER (ORDER BY order_date RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_count
FROM orders
WHERE order_date BETWEEN '2025-03-01' AND '2025-03-03'
ORDER BY order_date, order_id;
