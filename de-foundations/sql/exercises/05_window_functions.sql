-- Write each answer under its question. Check with:  python sql/check.py 05

-- @q1
-- Each product with its price rank inside its category (most expensive = 1),
-- using DENSE_RANK. Columns: category, name, unit_price, price_rank.


-- @q2
-- The 2 most expensive products per category (ties broken by product_id ascending).
-- Columns: category, name.


-- @q3
-- Each customer's most recent order (ties: highest order_id).
-- Columns: customer_id, order_id, order_date.


-- @q4
-- For customer_id 7: every order with the previous order's date.
-- Columns: order_id, order_date, prev_order_date. Order by order_date, order_id.


-- @q5
-- Monthly completed-order count with a running total.
-- Columns: month ('YYYY-MM'), n, running_n. Order by month.


-- @q6
-- Monthly net revenue (completed orders, rounded 2) and its 3-month moving average
-- (this month + 2 previous, rounded 2). Columns: month, revenue, ma3. Order by month.


-- @q7
-- Month-over-month % change in completed-order count, rounded to 1 (NULL for the first month).
-- Columns: month, n, pct_change. Order by month.


-- @q8
-- For each customer who ordered: first order date and last order date,
-- computed with FIRST_VALUE and LAST_VALUE (one row per customer).
-- Columns: customer_id, first_order, last_order.


-- @q9
-- Days between consecutive orders, per customer, averaged: customers with at least
-- 10 orders and their average gap in days rounded to 1.
-- Columns: customer_id, avg_gap_days.


-- @q10
-- ROWS vs RANGE: for orders on '2025-03-01'..'2025-03-03' ordered by order_date,
-- return order_id, order_date, a ROWS running count and a RANGE running count.
-- Use ORDER BY order_date only inside both windows (no tiebreaker) for RANGE;
-- for ROWS use ORDER BY order_date, order_id. Order output by order_date, order_id.

