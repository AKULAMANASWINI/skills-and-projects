-- Write each answer under its question. Check with:  python sql/check.py 06
-- Each question gives a slow-shaped query. Rewrite it so it returns the SAME result
-- but could use an index / does less work. The checker only compares results, so
-- also run EXPLAIN QUERY PLAN on both versions yourself.

-- @q1
-- Rewrite without a function on order_date (sargable range instead):
--   SELECT order_id FROM orders WHERE strftime('%Y', order_date) = '2025';

-- @q2
-- Rewrite with EXISTS instead of IN, and without DISTINCT:
--   SELECT DISTINCT c.customer_id FROM customers c
--   WHERE c.customer_id IN (SELECT customer_id FROM orders WHERE channel = 'store');

-- @q3
-- Rewrite so items are aggregated to order grain BEFORE joining (same output):
--   SELECT o.order_id, o.status, SUM(i.quantity) AS units
--   FROM orders o JOIN order_items i ON i.order_id = o.order_id
--   GROUP BY o.order_id, o.status;

-- @q4
-- Rewrite without the correlated subquery that runs once per row (use a join to an aggregate):
--   SELECT p.product_id,
--          (SELECT COUNT(*) FROM order_items i WHERE i.product_id = p.product_id) AS lines
--   FROM products p;

