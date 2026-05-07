import sqlite3

def setup():
    conn = sqlite3.connect('aegis_mock.db')
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT, join_date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total_amount REAL)''')

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

    conn.commit()
    conn.close()
    print("Database 'aegis_mock.db' created successfully.")

if __name__ == "__main__":
    setup()