# E-Commerce Database

A relational database schema for an e-commerce application, built using **Microsoft SQL Server**. This project defines the core tables, relationships, and constraints needed to manage products, customers, orders, and inventory.

---

## Database: `ECommerce`

```sql
CREATE DATABASE ECommerce;
USE ECommerce;
```

---

## Tables

### `categories`
Stores product categories.

```sql
CREATE TABLE categories
(
   category_id INT PRIMARY KEY,
   category_name VARCHAR(60)
);
```

---

### `products`
Stores product details. Each product belongs to a category.

```sql
CREATE TABLE products
(
    product_id INT PRIMARY KEY,
	product_name VARCHAR(50) NOT NULL,
	category_id INT,
	created_at DATETIME,
	price DECIMAL(20,2),
	FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```

---

### `customers`
Stores customer information.

```sql
CREATE TABLE customers
(
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(30) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(150),
    created_at DATETIME
);
```

---

### `orders`
Stores order records placed by customers.

```sql
CREATE TABLE orders
(
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_status VARCHAR(50),
    total_amount DECIMAL(20,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

---

### `order_items`
Stores individual line items within each order.

```sql
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
```

> The `price` column captures the product price **at the time of purchase**, so historical order data is not affected by future price changes.

---

### `inventory`
Tracks stock quantity for each product.

```sql
CREATE TABLE inventory
(
    inventory_id INT PRIMARY KEY,
    product_id INT,
    stock_quantity INT,
    last_updated DATE,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
```

---

You can see the entity relationship diagrams on ER_Diagrams folder to get a better understanding of the database structure.

| Relationship | Type |
|---|---|
| `categories` → `products` | One-to-Many |
| `customers` → `orders` | One-to-Many |
| `orders` → `order_items` | One-to-Many |
| `products` → `order_items` | One-to-Many |
| `products` → `inventory` | One-to-One |

---

## Key Design Decisions

- **`price` in `order_items`** is stored separately from `products.price` to preserve the price at the time of sale.
- **Foreign keys** are defined on all relationships to enforce referential integrity at the database level.

---

## File Structure

```
E-Commerce-Database/
│
├── create_database.sql
├── create_categories_table.sql
├── create_customers_table.sql
├── create_products_table.sql
├── create_orders_table.sql
├── create_order_items_table.sql
├── create_inventory_table.sql
├── ER_Diagram.png
└── README.md
```

---

## Getting Started

1. Open **SQL Server Management Studio (SSMS)** or **Azure Data Studio**
2. Run the scripts in this order:

```
1. create_database.sql
2. create_categories_table.sql
3. create_customers_table.sql
4. create_products_table.sql
5. create_orders_table.sql
6. create_order_items_table.sql
7. create_inventory_table.sql
```
