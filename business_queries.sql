-- =========================================================
-- E-COMMERCE BUSINESS ANALYSIS
-- Business SQL Queries
-- =========================================================


-- ---------------------------------------------------------
-- QUERY 1: TOTAL NET REVENUE
-- Calculates total revenue after applying discounts.
-- ---------------------------------------------------------

SELECT
    SUM(
        quantity * unit_price * (1 - discount)
    ) AS total_net_revenue
FROM orders
WHERE quantity > 0
  AND unit_price > 0
  AND date(order_date) IS NOT NULL;



-- ---------------------------------------------------------
-- QUERY 2: TOP 10 CUSTOMERS BY TOTAL SPENDING
-- Shows the highest-value customers.
-- ---------------------------------------------------------

SELECT
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS number_of_orders,
    SUM(
        o.quantity *
        o.unit_price *
        (1 - o.discount)
    ) AS total_spending

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

WHERE o.quantity > 0
  AND o.unit_price > 0
  AND date(o.order_date) IS NOT NULL

GROUP BY
    c.customer_id,
    c.customer_name,
    c.city

ORDER BY
    total_spending DESC

LIMIT 10;



-- ---------------------------------------------------------
-- QUERY 3: CATEGORY-WISE BUSINESS PERFORMANCE
-- Shows revenue, order count and quantity sold by category.
-- ---------------------------------------------------------

SELECT
    LOWER(TRIM(p.category)) AS category,

    SUM(
        o.quantity *
        o.unit_price *
        (1 - o.discount)
    ) AS net_revenue,

    COUNT(
        DISTINCT o.order_id
    ) AS order_count,

    SUM(
        o.quantity
    ) AS quantity_sold

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

WHERE o.quantity > 0
  AND o.unit_price > 0
  AND date(o.order_date) IS NOT NULL

GROUP BY
    LOWER(TRIM(p.category))

ORDER BY
    net_revenue DESC;



-- ---------------------------------------------------------
-- QUERY 4: MONTHLY NET REVENUE TREND
-- Shows how net revenue changes over time.
-- ---------------------------------------------------------

SELECT
    strftime(
        '%Y-%m',
        order_date
    ) AS month,

    SUM(
        quantity *
        unit_price *
        (1 - discount)
    ) AS net_revenue

FROM orders

WHERE quantity > 0
  AND unit_price > 0
  AND date(order_date) IS NOT NULL

GROUP BY
    month

ORDER BY
    month;



-- ---------------------------------------------------------
-- QUERY 5: TOP 5 PRODUCTS BY NET REVENUE
-- Identifies the five highest revenue-generating products.
-- ---------------------------------------------------------

SELECT
    p.product_name,
    p.category,

    SUM(
        o.quantity *
        o.unit_price *
        (1 - o.discount)
    ) AS net_revenue

FROM orders o

JOIN products p
    ON o.product_id = p.product_id

WHERE o.quantity > 0
  AND o.unit_price > 0
  AND date(o.order_date) IS NOT NULL

GROUP BY
    p.product_id,
    p.product_name,
    p.category

ORDER BY
    net_revenue DESC

LIMIT 5;