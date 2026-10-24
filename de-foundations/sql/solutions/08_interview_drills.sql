-- Reference solutions. Only open after a real attempt.
-- Mixed problems in interview style: the question doesn't tell you which technique to use.
-- Time-box each to 15 minutes.

-- @q1
-- Second-highest distinct unit_price among products. One value.
SELECT MAX(unit_price) FROM products
WHERE unit_price < (SELECT MAX(unit_price) FROM products);

-- @q2
-- Duplicate check: (first_name, last_name) pairs shared by more than one customer.
-- Columns: first_name, last_name, n.
SELECT first_name, last_name, COUNT(*) AS n
FROM customers
GROUP BY first_name, last_name
HAVING COUNT(*) > 1;

-- @q3
-- Customers whose first-ever order (any status) was cancelled. Column: customer_id.
-- First = earliest order_date, ties broken by lowest order_id.
WITH ranked AS (
  SELECT customer_id, status,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
)
SELECT customer_id FROM ranked WHERE rn = 1 AND status = 'cancelled';

-- @q4
-- Best-selling product (by units, completed orders) in each category; ties -> lowest product_id.
-- Columns: category, product_id, units.
WITH u AS (
  SELECT p.category, p.product_id, SUM(i.quantity) AS units
  FROM order_items i
  JOIN orders o ON o.order_id = i.order_id
  JOIN products p ON p.product_id = i.product_id
  WHERE o.status = 'completed'
  GROUP BY p.category, p.product_id
),
r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY units DESC, product_id) AS rn FROM u
)
SELECT category, product_id, units FROM r WHERE rn = 1;

-- @q5
-- Orders that contain more than one distinct category. Column: order_id.
SELECT i.order_id
FROM order_items i
JOIN products p ON p.product_id = i.product_id
GROUP BY i.order_id
HAVING COUNT(DISTINCT p.category) > 1;

-- @q6
-- Customers who ordered in every one of the 3 channels. Column: customer_id.
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT channel) = 3;

-- @q7
-- Repeat-purchase rate: % of customers with >= 1 completed order who have >= 2 completed orders.
-- One value rounded to 1.
WITH n AS (
  SELECT customer_id, COUNT(*) AS c FROM orders WHERE status = 'completed' GROUP BY customer_id
)
SELECT ROUND(100.0 * SUM(CASE WHEN c >= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) FROM n;

-- @q8
-- Slow starters: customers whose first order came more than 180 days after they signed up.
-- (Orders start on 2024-01-01, so measure from the later of signup_date and '2024-01-01'.)
-- Columns: customer_id, days_to_first_order (rounded to 0 decimals).
SELECT c.customer_id,
       ROUND(julianday(MIN(o.order_date)) - julianday(MAX(c.signup_date, '2024-01-01')), 0) AS days_to_first_order
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id
HAVING julianday(MIN(o.order_date)) - julianday(MAX(c.signup_date, '2024-01-01')) > 180;

-- @q9
-- Pivot: completed orders per year as columns. Columns: channel, orders_2024, orders_2025.
SELECT channel,
       SUM(CASE WHEN order_date LIKE '2024-%' THEN 1 ELSE 0 END) AS orders_2024,
       SUM(CASE WHEN order_date LIKE '2025-%' THEN 1 ELSE 0 END) AS orders_2025
FROM orders
WHERE status = 'completed'
GROUP BY channel;

-- @q10
-- Year-over-year price check: for each product, the average unit_price charged on
-- order lines in 2024 and in 2025 (rounded 2). Columns: product_id, avg_2024, avg_2025.
-- Only products sold in both years.
SELECT i.product_id,
       ROUND(AVG(CASE WHEN o.order_date LIKE '2024-%' THEN i.unit_price END), 2) AS avg_2024,
       ROUND(AVG(CASE WHEN o.order_date LIKE '2025-%' THEN i.unit_price END), 2) AS avg_2025
FROM order_items i
JOIN orders o ON o.order_id = i.order_id
GROUP BY i.product_id
HAVING COUNT(CASE WHEN o.order_date LIKE '2024-%' THEN 1 END) > 0
   AND COUNT(CASE WHEN o.order_date LIKE '2025-%' THEN 1 END) > 0;

-- @q11
-- Longest streak: the maximum number of CONSECUTIVE calendar days with at least one order
-- (whole shop, any status). One value. (Classic gaps-and-islands.)
WITH days AS (
  SELECT DISTINCT order_date AS d FROM orders
),
grp AS (
  SELECT d, julianday(d) - ROW_NUMBER() OVER (ORDER BY d) AS island FROM days
)
SELECT MAX(n) FROM (SELECT island, COUNT(*) AS n FROM grp GROUP BY island);

-- @q12
-- Days in 2025 with NO orders at all. Column: day. Order by day.
-- (Hint: generate the calendar with a recursive CTE.)
-- @ordered
WITH RECURSIVE cal(day) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(day, '+1 day') FROM cal WHERE day < '2025-12-31'
)
SELECT day FROM cal
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_date = cal.day)
ORDER BY day;

-- @q13
-- Top 3 customers by completed net revenue in EACH country (ties -> lower customer_id).
-- Columns: country, customer_id, revenue (rounded 2).
WITH rev AS (
  SELECT c.country, c.customer_id, SUM(i.quantity * i.unit_price * (1 - i.discount)) AS revenue
  FROM customers c
  JOIN orders o ON o.customer_id = c.customer_id
  JOIN order_items i ON i.order_id = o.order_id
  WHERE o.status = 'completed'
  GROUP BY c.country, c.customer_id
),
r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY revenue DESC, customer_id) AS rn FROM rev
)
SELECT country, customer_id, ROUND(revenue, 2) FROM r WHERE rn <= 3;

-- @q14
-- Referral value: for each referrer, how many people they referred and how many of
-- those placed at least one completed order. Columns: referrer_id, referred, converted.
SELECT c.referred_by AS referrer_id,
       COUNT(*) AS referred,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders o
                             WHERE o.customer_id = c.customer_id AND o.status = 'completed')
                THEN 1 ELSE 0 END) AS converted
FROM customers c
WHERE c.referred_by IS NOT NULL
GROUP BY c.referred_by;

-- @q15
-- Median number of items (order_items rows) per order. One value.
-- (SQLite has no MEDIAN: use ROW_NUMBER and COUNT windows.)
WITH n AS (
  SELECT order_id, COUNT(*) AS items FROM order_items GROUP BY order_id
),
r AS (
  SELECT items, ROW_NUMBER() OVER (ORDER BY items) AS rn, COUNT(*) OVER () AS cnt FROM n
)
SELECT AVG(items) * 1.0 FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2);
