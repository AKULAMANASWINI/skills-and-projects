-- Write each answer under its question. Check with:  python sql/check.py 04

-- @q1
-- Products priced above the average product price: name, unit_price.


-- @q2
-- Customers who have bought (any status) at least one product in the 'Books' category.
-- Column: customer_id. Each customer once.


-- @q3
-- Customers who have never referred anyone. Use NOT EXISTS (NOT IN has a NULL trap here).
-- Column: customer_id.


-- @q4
-- Average number of orders per customer, among customers who ordered at all. Round to 2.
-- One value.


-- @q5
-- Cohorts: for each month of a customer's FIRST completed order ('YYYY-MM'),
-- how many customers had their first completed order then.
-- Columns: cohort, new_buyers. Order by cohort.


-- @q6
-- customer_ids that ordered through the 'store' channel in 2024 but not in 2025. Use EXCEPT.


-- @q7
-- Each customer's share of total net revenue from completed orders, as a percentage
-- rounded to 2. Return only customers with share >= 2%.
-- Columns: customer_id, revenue (rounded 2), pct. Order by pct descending.

