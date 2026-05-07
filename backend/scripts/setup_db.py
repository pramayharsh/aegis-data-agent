import sqlite3
import os

def setup():
    # Remove existing db to start fresh
    if os.path.exists('aegis_mock.db'):
        os.remove('aegis_mock.db')
        
    conn = sqlite3.connect('aegis_mock.db')
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT, join_date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total_amount REAL)''')
    # ADD THIS:
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                      (id INTEGER PRIMARY KEY, product_name TEXT, price REAL)''')

    # Insert Dummy Data
    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", [
        (1, 'Alice Smith', 'alice@example.com', '2023-01-01'),
        (2, 'Bob Jones', 'bob@example.com', '2023-02-15')
    ])
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", [
        (101, 1, '2023-03-01', 150.00),
        (102, 1, '2023-03-05', 50.00),
        (103, 2, '2023-03-10', 200.00)
    ])
    # ADD THIS:
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?)", [
        (1, 'Laptop', 1200.00),
        (2, 'Mouse', 25.00),
        (3, 'Monitor', 300.00)
    ])

    conn.commit()
    conn.close()
    print("Database 'aegis_mock.db' updated with products table.")

if __name__ == "__main__":
    setup()