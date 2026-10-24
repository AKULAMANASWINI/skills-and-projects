-- Write each answer under its question. Check with:  python sql/check.py 02

-- @q1
-- How many customers are there, and how many of them have an email? (one row, two columns)


-- @q2
-- Number of orders per status. Columns: status, n.


-- @q3
-- Number of products and average unit_price (rounded to 2) per category.
-- Columns: category, n_products, avg_price. Order by avg_price descending.


-- @q4
-- Orders per year and channel. Columns: year (text 'YYYY'), channel, n.
-- Order by year, then channel.


-- @q5
-- Customers who placed at least 25 orders (any status). Columns: customer_id, n_orders.


-- @q6
-- Net revenue per product_id from order_items:
-- SUM(quantity * unit_price * (1 - discount)) rounded to 2.
-- Return only the 3 highest-revenue products. Columns: product_id, revenue. Order by revenue desc.


-- @q7
-- Per channel: total orders, cancelled orders, and cancellation percentage rounded to 1.
-- Columns: channel, orders, cancelled, cancel_pct.


-- @q8
-- Count products per price band: 'budget' (< 30), 'mid' (30 to < 100), 'premium' (>= 100).
-- Columns: price_band, n.

