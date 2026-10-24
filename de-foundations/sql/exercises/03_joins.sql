-- Write each answer under its question. Check with:  python sql/check.py 03

-- @q1
-- For each order placed on '2025-12-31': order_id, customer first_name, country.


-- @q2
-- Customers who have never placed an order: customer_id, first_name, last_name.


-- @q3
-- Number of orders per country (country of the customer). Columns: country, n_orders.


-- @q4
-- Net revenue of COMPLETED orders per product category, rounded to 2.
-- Columns: category, revenue. Order by revenue descending.


-- @q5
-- Every customer with their number of COMPLETED orders, including customers with 0.
-- Columns: customer_id, completed_orders.


-- @q6
-- Referred customers with the name of who referred them.
-- Columns: customer_id, customer_first_name, referrer_id, referrer_first_name.


-- @q7
-- Average order value per channel, counting each order once.
-- Order value = SUM(quantity * unit_price * (1 - discount)) over its items.
-- All statuses. Columns: channel, avg_order_value (rounded to 2).


-- @q8
-- Discontinued products (is_active = 0) that were still sold in a completed order in 2025.
-- Columns: product_id, name, units_sold_2025 (SUM of quantity).

