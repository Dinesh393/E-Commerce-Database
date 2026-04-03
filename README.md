# E-Commerce Database

A relational database schema for an e-commerce application, built using **Microsoft SQL Server**. This project defines the core tables, relationships, constraints, and sample data required to manage products, customers, orders, inventory, payments, shipping, and reviews.

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
   category_id INT IDENTITY(1,1) PRIMARY KEY,
   category_name VARCHAR(60)
);
```

---

### `products`
Stores product details. Each product belongs to a category.

```sql
CREATE TABLE products
(
    product_id INT IDENTITY(1,1) PRIMARY KEY,
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
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
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
    order_id INT IDENTITY(1,1) PRIMARY KEY,
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
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
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
    inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT,
    stock_quantity INT,
    last_updated DATE,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
```

---

### `payments`
Stores payment information for each order.

```sql
CREATE TABLE payments
(
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT,
    payment_method VARCHAR(30),
    payment_status VARCHAR(30),
    payment_date DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

---

### `reviews`
Stores customer reviews and ratings for products.

```sql
CREATE TABLE reviews
(
    review_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT,
    product_id INT,
    review_date DATE,
    rating INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

---

### `shipping`
Tracks shipping details and delivery status for each order.

```sql
CREATE TABLE shipping
(
    shipping_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT,
    shipping_address VARCHAR(200),
    shipped_date DATE,
    delivered_date DATE,
    shipping_status VARCHAR(30),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

---

## Entity Relationship Overview

| Relationship | Type |
|---|---|
| `categories` → `products` | One-to-Many |
| `customers` → `orders` | One-to-Many |
| `orders` → `order_items` | One-to-Many |
| `products` → `order_items` | One-to-Many |
| `products` → `inventory` | One-to-One |
| `orders` → `payments` | One-to-One |
| `customers` → `reviews` | One-to-Many |
| `products` → `reviews` | One-to-Many |
| `orders` → `shipping` | One-to-One |

---

## Key Design Decisions

- **`price` in `order_items`** is stored separately from `products.price` to preserve historical order pricing.
- **Foreign keys** are used throughout the schema to enforce referential integrity.
- **IDENTITY columns** are used for auto-incrementing primary keys.
- Inventory quantities are updated based on order transactions. :contentReference[oaicite:0]{index=0}
- Order totals are validated against `order_items` data. 

---

## File Structure

```text
E-Commerce-Database/
│
├── sql/
│   ├── create_database.sql
│   ├── create_categories_table.sql
│   ├── create_customers_table.sql
│   ├── create_products_table.sql
│   ├── create_orders_table.sql
│   ├── create_order_items_table.sql
│   ├── create_inventory_table.sql
│   ├── create_payments_table.sql
│   ├── create_shipping_table.sql
│   ├── create_reviews_table.sql
│   │
│   ├── insert_data/
│   │   ├── insert_categories.sql
│   │   ├── insert_customers.sql
│   │   ├── insert_products.sql
│   │   ├── insert_orders.sql
│   │   ├── insert_order_items.sql
│   │   └── insert_inventory.sql
│
├── scripts/
│   └── generate_data.py
│
├── ER_Diagram.png
└── README.md
```

---

## Getting Started

### Step 1: Create Database and Tables

Run the scripts in this order:

```text
1. create_database.sql
2. create_categories_table.sql
3. create_customers_table.sql
4. create_products_table.sql
5. create_orders_table.sql
6. create_order_items_table.sql
7. create_inventory_table.sql
8. create_payments_table.sql
9. create_shipping_table.sql
10. create_reviews_table.sql
```

---

### Step 2: Insert Sample Data

Run the data insertion scripts in this order:

```text
1. insert_data/insert_categories.sql
2. insert_data/insert_customers.sql
3. insert_data/insert_products.sql
4. insert_data/insert_orders.sql
5. insert_data/insert_order_items.sql
6. insert_data/insert_inventory.sql
```

Sample data files include:
- Categories: Electronics, Clothing, Home & Kitchen, Sports & Outdoors, Books, Beauty & Personal Care, Toys & Games, Automotive, Health & Wellness, Office Supplies
- Products: Range includes electronics (headphones, speakers, laptops), clothing (shoes, jeans, shirts), home goods (coffee makers, air fryers), and more
- Customers: Realistic customer profiles with names, emails, phone numbers, and addresses
- Orders: Orders from 2023-2026 with various statuses (Delivered, Processing, Shipped, Cancelled, Refunded, Pending)
- Inventory: Stock levels ranging from 0-500 units with recent update timestamps

---

## Features

- Fully normalized relational database design
- Real-world e-commerce workflow support
- Historical price tracking
- Inventory management
- Order and shipping tracking
- Customer review management
- Sample dataset for testing SQL queries and analytics

---

## Data Generation (Python Script)

The sample data in `sql/insert_data/` was generated using Python with the **Faker** library to ensure realistic, synthetic data.

### Why Use Generated Data?

- **No real customer data** - All data is synthetic and safe for public repositories
- **Consistent format** - Follows database schema constraints
- **Realistic relationships** - Maintains referential integrity
- **Edge cases included** - NULL values, various statuses, date ranges
- **Reproducible** - Anyone can regenerate with different parameters

### Regenerate Sample Data

1. Install Faker:
   ```bash
   pip install faker

### Steps to use the python script
- Create a generate_data.py file in the main folder.
- Paste the given code into the file and run it.
- It will generate a file called **ecommerce_sample_data.sql**, where all the insert statements are included.
- You can run those insert statements on sql server to insert the data into tables.
- You can increase the volume of data by modifying the **generate_data.py**
  ```generate_data.py
    NUM_CATEGORIES = 10      # Number of categories
    NUM_CUSTOMERS  = 100     # Number of customers
    NUM_PRODUCTS   = 50      # Number of products
    NUM_ORDERS     = 200     # Number of orders
    NUM_REVIEWS    = 150     # Number of reviews
  ```
- Just change the numbers according to the volume of data you required and run it.

## Tools Used

- **Microsoft SQL Server**
- **SQL Server Management Studio (SSMS)**
- **GitHub**

---

## Author

**Dinesh**
