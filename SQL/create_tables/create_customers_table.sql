CREATE TABLE customers
(
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(30) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(150),
    created_at DATETIME
);