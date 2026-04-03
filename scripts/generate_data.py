from faker import Faker
import random
from datetime import timedelta

fake = Faker()

NUM_CATEGORIES  = 10
NUM_CUSTOMERS   = 100
NUM_PRODUCTS    = 50
NUM_ORDERS      = 200
NUM_REVIEWS     = 150

lines = []

def q(val):
    """Wrap a value in single quotes, or return NULL."""
    if val is None:
        return "NULL"
    return f"'{str(val).replace(chr(39), chr(39)+chr(39))}'"


# ---------------------------------------------------------------
# 1. CATEGORIES
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- CATEGORIES")
lines.append("-- ============================================================")

category_names = [
    "Electronics", "Clothing", "Home & Kitchen", "Sports & Outdoors",
    "Books", "Beauty & Personal Care", "Toys & Games", "Automotive",
    "Health & Wellness", "Office Supplies"
]

for i, name in enumerate(category_names[:NUM_CATEGORIES], start=1):
    lines.append(f"INSERT INTO categories (category_name) VALUES ('{name}');")

lines.append("")


# ---------------------------------------------------------------
# 2. CUSTOMERS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- CUSTOMERS")
lines.append("-- ============================================================")

customer_ids = list(range(1, NUM_CUSTOMERS + 1))

for i in customer_ids:
    name     = fake.name().replace("'", "''")
    email    = fake.unique.email()
    phone    = q(fake.phone_number()) if random.random() > 0.15 else "NULL"   # 15% NULL
    address  = q(fake.address().replace("\n", ", ")) if random.random() > 0.10 else "NULL"  # 10% NULL
    created  = fake.date_time_between(start_date="-3y", end_date="now")
    lines.append(
        f"INSERT INTO customers (name, email, phone, address, created_at) "
        f"VALUES ('{name}', '{email}', {phone}, {address}, '{created}');"
    )

lines.append("")


# ---------------------------------------------------------------
# 3. PRODUCTS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- PRODUCTS")
lines.append("-- ============================================================")

product_ids = list(range(1, NUM_PRODUCTS + 1))

product_pool = [
    "Wireless Headphones", "Running Shoes", "Coffee Maker", "Yoga Mat",
    "Stainless Steel Water Bottle", "Laptop Stand", "Bluetooth Speaker",
    "Desk Lamp", "Resistance Bands", "Air Fryer", "Sunscreen SPF 50",
    "Notebook Set", "Office Chair", "Mechanical Keyboard", "Phone Case",
    "Protein Powder", "Cooking Pan Set", "LED Strip Lights", "Backpack",
    "Smart Watch", "USB Hub", "Perfume", "Face Wash", "Board Game",
    "Car Phone Mount", "Vitamin C Supplements", "Wireless Mouse", "Jeans",
    "Thriller Novel", "Portable Charger", "Gym Gloves", "Hair Dryer",
    "Dumbbell Set", "Toothbrush Electric", "Hiking Boots", "Cookbook",
    "Webcam HD", "Kids Puzzle", "Sunglasses", "Tea Kettle",
    "Drawing Tablet", "Memory Foam Pillow", "Polo T-Shirt", "Action Figure",
    "Insect Repellent", "Stapler", "Jump Rope", "Whey Protein Bar",
    "Car Vacuum", "Sticky Notes Pack"
]

for i, pname in enumerate(product_pool[:NUM_PRODUCTS], start=1):
    cat_id   = random.randint(1, NUM_CATEGORIES)
    price    = round(random.uniform(5.99, 499.99), 2)
    created  = fake.date_time_between(start_date="-4y", end_date="-6M")
    lines.append(
        f"INSERT INTO products (product_name, category_id, created_at, price) "
        f"VALUES ('{pname}', {cat_id}, '{created}', {price});"
    )

lines.append("")


# ---------------------------------------------------------------
# 4. ORDERS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- ORDERS")
lines.append("-- ============================================================")

order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Refunded"]
order_ids      = list(range(1, NUM_ORDERS + 1))
order_dates    = {}

for i in order_ids:
    cust_id    = random.choice(customer_ids)
    order_date = fake.date_between(start_date="-2y", end_date="today")
    status     = random.choices(
        order_statuses,
        weights=[10, 15, 20, 40, 10, 5], k=1
    )[0]
    total      = round(random.uniform(10.00, 1500.00), 2)
    order_dates[i] = order_date
    lines.append(
        f"INSERT INTO orders (customer_id, order_date, order_status, total_amount) "
        f"VALUES ({cust_id}, '{order_date}', '{status}', {total});"
    )

lines.append("")


# ---------------------------------------------------------------
# 5. ORDER_ITEMS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- ORDER_ITEMS")
lines.append("-- ============================================================")

for order_id in order_ids:
    num_items = random.randint(1, 5)
    chosen_products = random.sample(product_ids, min(num_items, len(product_ids)))
    for prod_id in chosen_products:
        price    = round(random.uniform(5.99, 499.99), 2)
        quantity = random.randint(1, 5)
        lines.append(
            f"INSERT INTO order_items (product_id, order_id, price, quantity) "
            f"VALUES ({prod_id}, {order_id}, {price}, {quantity});"
        )

lines.append("")


# ---------------------------------------------------------------
# 6. INVENTORY
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- INVENTORY")
lines.append("-- ============================================================")

for prod_id in product_ids:
    stock       = random.randint(0, 500)
    last_updated = fake.date_between(start_date="-6M", end_date="today")
    lines.append(
        f"INSERT INTO inventory (product_id, stock_quantity, last_updated) "
        f"VALUES ({prod_id}, {stock}, '{last_updated}');"
    )

lines.append("")


# ---------------------------------------------------------------
# 7. PAYMENTS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- PAYMENTS")
lines.append("-- ============================================================")

payment_methods  = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]
payment_statuses = ["Completed", "Pending", "Failed", "Refunded"]

for order_id in order_ids:
    # ~10% of orders have no payment record yet (Pending orders)
    if random.random() < 0.10:
        continue
    method       = random.choice(payment_methods)
    status       = random.choices(payment_statuses, weights=[70, 10, 10, 10], k=1)[0]
    order_date   = order_dates[order_id]
    payment_date = order_date + timedelta(days=random.randint(0, 2))
    lines.append(
        f"INSERT INTO payments (order_id, payment_method, payment_status, payment_date) "
        f"VALUES ({order_id}, '{method}', '{status}', '{payment_date}');"
    )

lines.append("")


# ---------------------------------------------------------------
# 8. REVIEWS
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- REVIEWS")
lines.append("-- ============================================================")

used_pairs = set()

for _ in range(NUM_REVIEWS):
    cust_id  = random.choice(customer_ids)
    prod_id  = random.choice(product_ids)
    pair     = (cust_id, prod_id)
    if pair in used_pairs:
        continue
    used_pairs.add(pair)
    rating      = random.choices([1, 2, 3, 4, 5], weights=[5, 8, 15, 30, 42], k=1)[0]
    review_date = fake.date_between(start_date="-2y", end_date="today")
    lines.append(
        f"INSERT INTO reviews (customer_id, product_id, review_date, rating) "
        f"VALUES ({cust_id}, {prod_id}, '{review_date}', {rating});"
    )

lines.append("")


# ---------------------------------------------------------------
# 9. SHIPPING
# ---------------------------------------------------------------
lines.append("-- ============================================================")
lines.append("-- SHIPPING")
lines.append("-- ============================================================")

shipping_statuses = ["Processing", "Shipped", "Out for Delivery", "Delivered", "Returned"]

for order_id in order_ids:
    # Only shipped/delivered orders get a shipping record
    if random.random() < 0.12:
        continue
    address      = fake.address().replace("\n", ", ").replace("'", "''")
    order_date   = order_dates[order_id]
    shipped_date = q(order_date + timedelta(days=random.randint(1, 3))) if random.random() > 0.10 else "NULL"
    if shipped_date != "NULL":
        delivered = order_date + timedelta(days=random.randint(4, 14))
        delivered_date = q(delivered) if random.random() > 0.15 else "NULL"
    else:
        delivered_date = "NULL"
    status = random.choices(shipping_statuses, weights=[10, 20, 10, 50, 10], k=1)[0]
    lines.append(
        f"INSERT INTO shipping (order_id, shipping_address, shipped_date, delivered_date, shipping_status) "
        f"VALUES ({order_id}, '{address}', {shipped_date}, {delivered_date}, '{status}');"
    )

lines.append("")


# ---------------------------------------------------------------
# Write to file
# ---------------------------------------------------------------
output = "\n".join(lines)
with open("ecommerce_sample_data.sql", "w") as f:
    f.write(output)

print("Done! File saved as ecommerce_sample_data.sql")
print(f"  Categories : {NUM_CATEGORIES}")
print(f"  Customers  : {NUM_CUSTOMERS}")
print(f"  Products   : {NUM_PRODUCTS}")
print(f"  Orders     : {NUM_ORDERS}")
print(f"  Reviews    : up to {NUM_REVIEWS}")