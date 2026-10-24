-- Write each answer under its question. Check with:  python sql/check.py 08
-- Mixed problems in interview style: the question doesn't tell you which technique to use.
-- Time-box each to 15 minutes.

-- @q1
-- Second-highest distinct unit_price among products. One value.


-- @q2
-- Duplicate check: (first_name, last_name) pairs shared by more than one customer.
-- Columns: first_name, last_name, n.


-- @q3
-- Customers whose first-ever order (any status) was cancelled. Column: customer_id.
-- First = earliest order_date, ties broken by lowest order_id.


-- @q4
-- Best-selling product (by units, completed orders) in each category; ties -> lowest product_id.
-- Columns: category, product_id, units.


-- @q5
-- Orders that contain more than one distinct category. Column: order_id.


-- @q6
-- Customers who ordered in every one of the 3 channels. Column: customer_id.


-- @q7
-- Repeat-purchase rate: % of customers with >= 1 completed order who have >= 2 completed orders.
-- One value rounded to 1.


-- @q8
-- Slow starters: customers whose first order came more than 180 days after they signed up.
-- (Orders start on 2024-01-01, so measure from the later of signup_date and '2024-01-01'.)
-- Columns: customer_id, days_to_first_order (rounded to 0 decimals).


-- @q9
-- Pivot: completed orders per year as columns. Columns: channel, orders_2024, orders_2025.


-- @q10
-- Year-over-year price check: for each product, the average unit_price charged on
-- order lines in 2024 and in 2025 (rounded 2). Columns: product_id, avg_2024, avg_2025.
-- Only products sold in both years.


-- @q11
-- Longest streak: the maximum number of CONSECUTIVE calendar days with at least one order
-- (whole shop, any status). One value. (Classic gaps-and-islands.)


-- @q12
-- Days in 2025 with NO orders at all. Column: day. Order by day.
-- (Hint: generate the calendar with a recursive CTE.)


-- @q13
-- Top 3 customers by completed net revenue in EACH country (ties -> lower customer_id).
-- Columns: country, customer_id, revenue (rounded 2).


-- @q14
-- Referral value: for each referrer, how many people they referred and how many of
-- those placed at least one completed order. Columns: referrer_id, referred, converted.


-- @q15
-- Median number of items (order_items rows) per order. One value.
-- (SQLite has no MEDIAN: use ROW_NUMBER and COUNT windows.)

