CREATE TABLE inventory
(
   inventory_id INT IDENTITY(1,1) PRIMARY KEY,
   product_id INT,
   stock_quantity INT,
   last_updated DATE,
   FOREIGN KEY(product_id) REFERENCES products(product_id)
);