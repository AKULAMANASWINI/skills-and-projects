-- Reference solutions. Only open after a real attempt.

-- @q1
-- How many customers are there, and how many of them have an email? (one row, two columns)
SELECT COUNT(*) AS customers, COUNT(email) AS with_email
FROM customers;

-- @q2
-- Number of orders per status. Columns: status, n.
SELECT status, COUNT(*) AS n
FROM orders
GROUP BY status;

-- @q3
-- Number of products and average unit_price (rounded to 2) per category.
-- Columns: category, n_products, avg_price. Order by avg_price descending.
-- @ordered
SELECT category, COUNT(*) AS n_products, ROUND(AVG(unit_price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;

-- @q4
-- Orders per year and channel. Columns: year (text 'YYYY'), channel, n.
-- Order by year, then channel.
-- @ordered
SELECT strftime('%Y', order_date) AS yr, channel, COUNT(*) AS n
FROM orders
GROUP BY yr, channel
ORDER BY yr, channel;

-- @q5
-- Customers who placed at least 25 orders (any status). Columns: customer_id, n_orders.
SELECT customer_id, COUNT(*) AS n_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 25;

-- @q6
-- Net revenue per product_id from order_items:
-- SUM(quantity * unit_price * (1 - discount)) rounded to 2.
-- Return only the 3 highest-revenue products. Columns: product_id, revenue. Order by revenue desc.
-- @ordered
SELECT product_id, ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
FROM order_items
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 3;

-- @q7
-- Per channel: total orders, cancelled orders, and cancellation percentage rounded to 1.
-- Columns: channel, orders, cancelled, cancel_pct.
SELECT channel,
       COUNT(*) AS orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_pct
FROM orders
GROUP BY channel;

-- @q8
-- Count products per price band: 'budget' (< 30), 'mid' (30 to < 100), 'premium' (>= 100).
-- Columns: price_band, n.
SELECT CASE
         WHEN unit_price < 30 THEN 'budget'
         WHEN unit_price < 100 THEN 'mid'
         ELSE 'premium'
       END AS price_band,
       COUNT(*) AS n
FROM products
GROUP BY price_band;
