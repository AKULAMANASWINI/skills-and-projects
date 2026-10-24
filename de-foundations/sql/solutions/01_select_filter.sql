-- Reference solutions. Only open after a real attempt.

-- @q1
-- List the name and unit_price of every product in the 'Books' category.
SELECT name, unit_price
FROM products
WHERE category = 'Books';

-- @q2
-- List every distinct country customers come from.
SELECT DISTINCT country
FROM customers;

-- @q3
-- The 5 most expensive products: name and unit_price, order by unit_price descending.
-- @ordered
SELECT name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 5;

-- @q4
-- order_id and order_date of orders that were cancelled OR returned through the 'mobile' channel.
SELECT order_id, order_date
FROM orders
WHERE status IN ('cancelled', 'returned')
  AND channel = 'mobile';

-- @q5
-- customer_id, first_name, last_name of customers with no email on file.
SELECT customer_id, first_name, last_name
FROM customers
WHERE email IS NULL;

-- @q6
-- Product names containing the word 'Desk' (anywhere), plus their price with 18% tax
-- as a second column rounded to 2 decimals.
SELECT name, ROUND(unit_price * 1.18, 2) AS price_with_tax
FROM products
WHERE name LIKE '%Desk%';

-- @q7
-- customer_id and city for every customer NOT in the city 'London'.
-- Customers whose city is unknown (NULL) must be included. Show NULL city as 'unknown'.
SELECT customer_id, COALESCE(city, 'unknown') AS city
FROM customers
WHERE city <> 'London' OR city IS NULL;

-- @q8
-- order_id, order_date of completed 'web' orders placed in December 2025,
-- order by order_date then order_id.
-- @ordered
SELECT order_id, order_date
FROM orders
WHERE status = 'completed'
  AND channel = 'web'
  AND order_date BETWEEN '2025-12-01' AND '2025-12-31'
ORDER BY order_date, order_id;
