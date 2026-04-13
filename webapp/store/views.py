import pyodbc
from django.shortcuts import render

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=HPVICTUS;'
        'DATABASE=ECommerce;'
        'Trusted_Connection=yes;'
    )
    return conn

def home(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_amount) FROM orders')
    revenue = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM customers')
    total_customers = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]
    conn.close()
    return render(request, 'store/home.html', {
        'revenue': revenue,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
    })

def products(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.product_id, p.product_name, p.price, c.category_name
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
    ''')
    products = cursor.fetchall()
    conn.close()
    return render(request, 'store/products.html', {'products': products})

def customers(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT customer_id, name, email, phone, address, created_at FROM customers')
    customers = cursor.fetchall()
    conn.close()
    return render(request, 'store/customers.html', {'customers': customers})

def orders(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.order_id, c.name, o.order_date, o.order_status, o.total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
    ''')
    orders = cursor.fetchall()
    conn.close()
    return render(request, 'store/orders.html', {'orders': orders})

def inventory(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.product_id, p.product_name, c.category_name, p.price,
               i.stock_quantity, i.last_updated
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY i.stock_quantity ASC
    ''')
    inventory = cursor.fetchall()
    conn.close()
    return render(request, 'store/inventory.html', {'inventory': inventory})

def payments(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.payment_id, o.order_id, c.name, p.payment_method,
               p.payment_status, p.payment_date, o.total_amount
        FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY p.payment_date DESC
    ''')
    payments = cursor.fetchall()
    conn.close()
    return render(request, 'store/payments.html', {'payments': payments})

def reviews(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.review_id, c.name, p.product_name, r.rating, r.review_date
        FROM reviews r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN products p ON r.product_id = p.product_id
        ORDER BY r.review_date DESC
    ''')
    reviews = cursor.fetchall()
    conn.close()
    return render(request, 'store/reviews.html', {'reviews': reviews})

def dashboard(request):
    conn = get_connection()
    cursor = conn.cursor()

    # Existing queries
    cursor.execute('SELECT SUM(total_amount) FROM orders')
    revenue = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM customers')
    total_customers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]

    # New stat cards
    cursor.execute('SELECT ROUND(AVG(total_amount), 2) FROM orders')
    avg_order_value = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM reviews')
    total_reviews = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM inventory WHERE stock_quantity < 10')
    low_stock_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status = 'Delivered'")
    delivered_orders = cursor.fetchone()[0]

    # Existing charts
    cursor.execute('''
        SELECT order_status, COUNT(*)
        FROM orders
        GROUP BY order_status
    ''')
    order_status = cursor.fetchall()

    cursor.execute('''
        SELECT TOP 5 p.product_name, SUM(oi.quantity) AS total_qty
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_qty DESC
    ''')
    top_products = cursor.fetchall()

    cursor.execute('''
        SELECT MONTH(order_date), SUM(total_amount)
        FROM orders
        GROUP BY MONTH(order_date)
        ORDER BY MONTH(order_date)
    ''')
    monthly_revenue = cursor.fetchall()

    # New charts
    cursor.execute('''
        SELECT c.category_name,
               SUM(oi.price * oi.quantity) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY revenue DESC
    ''')
    category_revenue = cursor.fetchall()

    cursor.execute('''
        SELECT payment_method, COUNT(*) AS total
        FROM payments
        GROUP BY payment_method
        ORDER BY total DESC
    ''')
    payment_methods = cursor.fetchall()

    cursor.execute('''
        SELECT TOP 5 c.name, SUM(o.total_amount) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.name
        ORDER BY total_spent DESC
    ''')
    top_customers = cursor.fetchall()

    cursor.execute('''
        SELECT shipping_status, COUNT(*) AS total
        FROM shipping
        GROUP BY shipping_status
    ''')
    shipping_status = cursor.fetchall()

    # Recent 5 orders
    cursor.execute('''
        SELECT TOP 5 o.order_id, c.name,
               o.order_date, o.order_status, o.total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
    ''')
    recent_orders = cursor.fetchall()

    # Low stock products
    cursor.execute('''
        SELECT TOP 5 p.product_name, i.stock_quantity
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.stock_quantity < 10
        ORDER BY i.stock_quantity ASC
    ''')
    low_stock = cursor.fetchall()

    conn.close()

    return render(request, 'store/dashboard.html', {
        'revenue': revenue,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'total_reviews': total_reviews,
        'low_stock_count': low_stock_count,
        'delivered_orders': delivered_orders,
        'order_status_labels': [row[0] for row in order_status],
        'order_status_values': [row[1] for row in order_status],
        'top_product_labels': [row[0] for row in top_products],
        'top_product_values': [int(row[1]) for row in top_products],
        'monthly_labels': [str(row[0]) for row in monthly_revenue],
        'monthly_values': [float(row[1]) for row in monthly_revenue],
        'category_labels': [row[0] for row in category_revenue],
        'category_values': [float(row[1]) for row in category_revenue],
        'payment_labels': [row[0] for row in payment_methods],
        'payment_values': [row[1] for row in payment_methods],
        'top_customer_labels': [row[0] for row in top_customers],
        'top_customer_values': [float(row[1]) for row in top_customers],
        'shipping_labels': [row[0] for row in shipping_status],
        'shipping_values': [row[1] for row in shipping_status],
        'low_stock': low_stock,
    })


from django.contrib import messages
from django.shortcuts import redirect
import hashlib

def signup(request):
    if request.method == 'POST':
        name     = request.POST['name']
        email    = request.POST['email']
        phone    = request.POST['phone']
        address  = request.POST['address']
        password = request.POST['password']
        role     = request.POST['role']

        hashed = hashlib.sha256(password.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM customers WHERE email = ?', email)
        existing = cursor.fetchone()

        if existing:
            messages.error(request, 'Email already registered!')
            conn.close()
            return redirect('signup')

        cursor.execute('''
            INSERT INTO customers (name, email, phone, address, created_at, password, role)
            VALUES (?, ?, ?, ?, GETDATE(), ?, ?)
        ''', name, email, phone, address, hashed, role)
        conn.commit()
        conn.close()

        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'store/signup.html')


def login_view(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        role     = request.POST['role']
        hashed   = hashlib.sha256(password.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE email = ?', email)
        customer = cursor.fetchone()
        conn.close()

        if customer and customer[6] == hashed and customer[7] == role:
            request.session['customer_id']   = customer[0]
            request.session['customer_name'] = customer[1]
            request.session['customer_role'] = customer[7]
            messages.success(request, f'Welcome back, {customer[1]}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email, password or role!')
            return redirect('login')

    return render(request, 'store/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def add_product(request):
    if not request.session.get('customer_id'):
        return redirect('login')

    if request.session.get('customer_role') != 'admin':
        messages.error(request, 'Access Denied! Only admins can add products.')
        return redirect('products')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT category_id, category_name FROM categories')
    categories = cursor.fetchall()

    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_id  = request.POST['category_id']
        price        = request.POST['price']

        cursor.execute('''
            INSERT INTO products (product_name, category_id, price, created_at)
            VALUES (?, ?, ?, GETDATE())
        ''', product_name, category_id, price)
        conn.commit()
        conn.close()

        messages.success(request, 'Product added successfully!')
        return redirect('products')

    conn.close()
    return render(request, 'store/add_product.html', {'categories': categories})

def add_review(request):
    if not request.session.get('customer_id'):
        messages.error(request, 'Please login to add a review!')
        return redirect('login')

    # Prevent admin from accessing review page
    if request.session.get('customer_role') == 'admin':
        messages.error(request, 'Admins are not allowed to add reviews.')
        return redirect('home')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT product_id, product_name FROM products')
    products = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.POST['product_id']
        rating = request.POST['rating']
        customer_id = request.session['customer_id']

        cursor.execute('''
            SELECT * FROM reviews
            WHERE customer_id = ? AND product_id = ?
        ''', customer_id, product_id)

        existing = cursor.fetchone()

        if existing:
            messages.error(request, 'You have already reviewed this product!')
            conn.close()
            return redirect('add_review')

        cursor.execute('''
            INSERT INTO reviews (customer_id, product_id, rating, review_date)
            VALUES (?, ?, ?, GETDATE())
        ''', customer_id, product_id, rating)

        conn.commit()
        conn.close()

        messages.success(request, 'Review submitted successfully!')
        return redirect('reviews')

    conn.close()
    return render(request, 'store/add_review.html', {'products': products})

def database(request):
    return render(request, 'store/database.html')