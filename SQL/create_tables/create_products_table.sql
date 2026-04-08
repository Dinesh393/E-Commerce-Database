CREATE TABLE products
(
    product_id INT IDENTITY(1,1) PRIMARY KEY,
	product_name VARCHAR(50) NOT NULL,
	category_id INT,
	created_at DATETIME,
	price DECIMAL(20,2),
	FOREIGN KEY (category_id) REFERENCES categories(category_id)
);