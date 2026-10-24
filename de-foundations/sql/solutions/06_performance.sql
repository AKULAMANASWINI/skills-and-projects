-- Reference solutions. Only open after a real attempt.
-- Each question gives a slow-shaped query. Rewrite it so it returns the SAME result
-- but could use an index / does less work. The checker only compares results, so
-- also run EXPLAIN QUERY PLAN on both versions yourself.

-- @q1
-- Rewrite without a function on order_date (sargable range instead):
--   SELECT order_id FROM orders WHERE strftime('%Y', order_date) = '2025';
SELECT order_id
FROM orders
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01';

-- @q2
-- Rewrite with EXISTS instead of IN, and without DISTINCT:
--   SELECT DISTINCT c.customer_id FROM customers c
--   WHERE c.customer_id IN (SELECT customer_id FROM orders WHERE channel = 'store');
SELECT c.customer_id
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.channel = 'store');

-- @q3
-- Rewrite so items are aggregated to order grain BEFORE joining (same output):
--   SELECT o.order_id, o.status, SUM(i.quantity) AS units
--   FROM orders o JOIN order_items i ON i.order_id = o.order_id
--   GROUP BY o.order_id, o.status;
WITH units AS (
  SELECT order_id, SUM(quantity) AS units
  FROM order_items
  GROUP BY order_id
)
SELECT o.order_id, o.status, u.units
FROM orders o
JOIN units u ON u.order_id = o.order_id;

-- @q4
-- Rewrite without the correlated subquery that runs once per row (use a join to an aggregate):
--   SELECT p.product_id,
--          (SELECT COUNT(*) FROM order_items i WHERE i.product_id = p.product_id) AS lines
--   FROM products p;
SELECT p.product_id, COALESCE(l.lines, 0) AS lines
FROM products p
LEFT JOIN (SELECT product_id, COUNT(*) AS lines FROM order_items GROUP BY product_id) l
  ON l.product_id = p.product_id;
