CREATE TABLE shipping
(
  shipping_id INT IDENTITY(1,1) PRIMARY KEY,
  order_id INT,
  shipping_address VARCHAR(200),
  shipped_date DATE,
  delivered_date DATE,
  shipping_status VARCHAR(30),
  FOREIGN KEY(order_id) REFERENCES orders(order_id)
);