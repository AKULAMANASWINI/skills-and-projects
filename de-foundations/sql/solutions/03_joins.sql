-- Reference solutions. Only open after a real attempt.

-- @q1
-- For each order placed on '2025-12-31': order_id, customer first_name, country.
SELECT o.order_id, c.first_name, c.country
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_date = '2025-12-31';

-- @q2
-- Customers who have never placed an order: customer_id, first_name, last_name.
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;

-- @q3
-- Number of orders per country (country of the customer). Columns: country, n_orders.
SELECT c.country, COUNT(*) AS n_orders
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.country;

-- @q4
-- Net revenue of COMPLETED orders per product category, rounded to 2.
-- Columns: category, revenue. Order by revenue descending.
-- @ordered
SELECT p.category, ROUND(SUM(i.quantity * i.unit_price * (1 - i.discount)), 2) AS revenue
FROM order_items i
JOIN orders o ON o.order_id = i.order_id
JOIN products p ON p.product_id = i.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;

-- @q5
-- Every customer with their number of COMPLETED orders, including customers with 0.
-- Columns: customer_id, completed_orders.
SELECT c.customer_id, COUNT(o.order_id) AS completed_orders
FROM customers c
LEFT JOIN orders o
  ON o.customer_id = c.customer_id
 AND o.status = 'completed'
GROUP BY c.customer_id;

-- @q6
-- Referred customers with the name of who referred them.
-- Columns: customer_id, customer_first_name, referrer_id, referrer_first_name.
SELECT c.customer_id, c.first_name, r.customer_id, r.first_name
FROM customers c
JOIN customers r ON r.customer_id = c.referred_by;

-- @q7
-- Average order value per channel, counting each order once.
-- Order value = SUM(quantity * unit_price * (1 - discount)) over its items.
-- All statuses. Columns: channel, avg_order_value (rounded to 2).
WITH order_totals AS (
  SELECT order_id, SUM(quantity * unit_price * (1 - discount)) AS order_value
  FROM order_items
  GROUP BY order_id
)
SELECT o.channel, ROUND(AVG(t.order_value), 2) AS avg_order_value
FROM orders o
JOIN order_totals t ON t.order_id = o.order_id
GROUP BY o.channel;

-- @q8
-- Discontinued products (is_active = 0) that were still sold in a completed order in 2025.
-- Columns: product_id, name, units_sold_2025 (SUM of quantity).
SELECT p.product_id, p.name, SUM(i.quantity) AS units_sold_2025
FROM products p
JOIN order_items i ON i.product_id = p.product_id
JOIN orders o ON o.order_id = i.order_id
WHERE p.is_active = 0
  AND o.status = 'completed'
  AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01'
GROUP BY p.product_id, p.name;
