-- Total Sales Revenue
SELECT SUM(total_amount) AS total_sales_revenue
FROM orders;

-- Daily Sales Report
SELECT order_date, SUM(total_amount) AS daily_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- Monthly Sales Report
SELECT YEAR(order_date) AS sales_year, DATENAME(MONTH, order_date) AS sales_month, SUM(total_amount) AS monthly_sales
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date), DATENAME(MONTH, order_date)
ORDER BY sales_year, sales_month;

-- Top Selling Products
SELECT p.product_name, SUM(oi.quantity) AS total_units_sold, SUM(oi.price * oi.quantity) AS total_revenue
FROM order_items AS oi
JOIN products AS p
    ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_units_sold DESC;

-- Revenue by Category
SELECT c.category_name, SUM(oi.price * oi.quantity) AS category_revenue
FROM order_items AS oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN categories AS c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY category_revenue DESC;

-- Sales by Order Status
SELECT order_status, COUNT(order_id) AS total_orders, SUM(total_amount) AS total_sales
FROM orders
GROUP BY order_status;

-- Top Customers by Spending
SELECT c.name, SUM(o.total_amount) AS total_spent
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.name
ORDER BY total_spent DESC;