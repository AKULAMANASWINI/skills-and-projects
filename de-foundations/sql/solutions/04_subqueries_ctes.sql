-- Reference solutions. Only open after a real attempt.

-- @q1
-- Products priced above the average product price: name, unit_price.
SELECT name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products);

-- @q2
-- Customers who have bought (any status) at least one product in the 'Books' category.
-- Column: customer_id. Each customer once.
SELECT DISTINCT o.customer_id
FROM orders o
WHERE EXISTS (
  SELECT 1
  FROM order_items i
  JOIN products p ON p.product_id = i.product_id
  WHERE i.order_id = o.order_id AND p.category = 'Books'
);

-- @q3
-- Customers who have never referred anyone. Use NOT EXISTS (NOT IN has a NULL trap here).
-- Column: customer_id.
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM customers x WHERE x.referred_by = c.customer_id);

-- @q4
-- Average number of orders per customer, among customers who ordered at all. Round to 2.
-- One value.
SELECT ROUND(AVG(n), 2)
FROM (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) AS t;

-- @q5
-- Cohorts: for each month of a customer's FIRST completed order ('YYYY-MM'),
-- how many customers had their first completed order then.
-- Columns: cohort, new_buyers. Order by cohort.
-- @ordered
WITH first_orders AS (
  SELECT customer_id, MIN(order_date) AS first_order
  FROM orders
  WHERE status = 'completed'
  GROUP BY customer_id
)
SELECT strftime('%Y-%m', first_order) AS cohort, COUNT(*) AS new_buyers
FROM first_orders
GROUP BY cohort
ORDER BY cohort;

-- @q6
-- customer_ids that ordered through the 'store' channel in 2024 but not in 2025. Use EXCEPT.
SELECT customer_id FROM orders WHERE channel = 'store' AND order_date LIKE '2024-%'
EXCEPT
SELECT customer_id FROM orders WHERE channel = 'store' AND order_date LIKE '2025-%';

-- @q7
-- Each customer's share of total net revenue from completed orders, as a percentage
-- rounded to 2. Return only customers with share >= 2%.
-- Columns: customer_id, revenue (rounded 2), pct. Order by pct descending.
-- @ordered
WITH rev AS (
  SELECT o.customer_id, SUM(i.quantity * i.unit_price * (1 - i.discount)) AS revenue
  FROM orders o
  JOIN order_items i ON i.order_id = o.order_id
  WHERE o.status = 'completed'
  GROUP BY o.customer_id
),
total AS (SELECT SUM(revenue) AS t FROM rev)
SELECT customer_id, ROUND(revenue, 2), ROUND(100.0 * revenue / t, 2) AS pct
FROM rev, total
WHERE 100.0 * revenue / t >= 2
ORDER BY pct DESC;
