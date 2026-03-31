CREATE TABLE order_items
(
  order_item_id INT PRIMARY KEY,
  product_id INT,
  order_id INT,
  price DECIMAL(10,2),
  quantity INT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id)
);