CREATE TABLE orders
(
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  order_status VARCHAR(50),
  total_amount DECIMAL(20,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);