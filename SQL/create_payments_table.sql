CREATE TABLE payments
(
  payment_id INT IDENTITY(1,1) PRIMARY KEY,
  order_id INT, 
  payment_method VARCHAR(30),
  payment_status VARCHAR(30),
  payment_date DATE,
  FOREIGN KEY(order_id) REFERENCES orders(order_id)
);