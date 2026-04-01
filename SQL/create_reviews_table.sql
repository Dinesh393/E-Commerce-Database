CREATE TABLE reviews
(
  review_id INT IDENTITY(1,1) PRIMARY KEY,
  customer_id INT,
  product_id INT,
  review_date DATE,
  rating INT,
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id)
);
