import duckdb

def init_db(db_path="bank_demo.duckdb"):
    """
    Creates a connection to a DuckDB file.
    If the file does not exist, it will be created automatically.
    """
    conn = duckdb.connect(db_path)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER,
            name VARCHAR,
            email VARCHAR,
            PRIMARY KEY (customer_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER,
            customer_id INTEGER,
            account_type VARCHAR,      -- t.ex. 'savings', 'checking', 'credit'
            balance DECIMAL(10,2),
            PRIMARY KEY (account_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER,
            account_id INTEGER,
            amount DECIMAL(10,2),
            transaction_type VARCHAR,  -- t.ex. 'deposit', 'withdrawal', 'payment'
            timestamp TIMESTAMP,
            PRIMARY KEY (transaction_id)
        )
    """)
    
    return conn


def seed_data(conn):
    """
    Fills the database with some sample data.
    """
    conn.execute("""
        INSERT INTO customers (customer_id, name, email)
        VALUES
            (1, 'Alice Andersson', 'alice@example.com'),
            (2, 'Bertil Bengtsson', 'bertil@example.com'),
            (3, 'Cecilia Carlsson', 'cecilia@example.com')
    """)

    conn.execute("""
        INSERT INTO accounts (account_id, customer_id, account_type, balance)
        VALUES
            (101, 1, 'savings', 15000.50),
            (102, 1, 'checking', 1200.00),
            (201, 2, 'checking', 500.00),
            (202, 2, 'credit', -2500.00),
            (301, 3, 'savings', 100000.00)
    """)

    conn.execute("""
        INSERT INTO transactions (transaction_id, account_id, amount, transaction_type, timestamp)
        VALUES
            (10001, 101, 500.00, 'deposit', '2025-01-10 10:00:00'),
            (10002, 101, -200.00, 'withdrawal', '2025-01-15 08:30:00'),
            (10003, 102, 1200.00, 'deposit', '2025-01-20 14:00:00'),
            (20001, 201, -100.00, 'payment', '2025-01-22 09:00:00'),
            (20002, 202, -500.00, 'payment', '2025-01-22 11:00:00'),
            (30001, 301, 10000.00, 'deposit', '2025-01-25 16:00:00')
    """)


def example_queries(conn):
    """
    Examples of how to read and use data from the database.
    """
    print("=== Lista på kunder ===")
    results = conn.execute("SELECT * FROM customers").fetchall()
    for row in results:
        print(row)
    
    print("\n=== Sammanlagt saldo för Alice (kund_id=1) ===")
    query_balance = """
        SELECT c.name,
               SUM(a.balance) AS total_balance
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        WHERE c.customer_id = 1
        GROUP BY c.name
    """
    res_balance = conn.execute(query_balance).fetchone()
    print(f"Namn: {res_balance[0]}, Totalt saldo: {res_balance[1]}")
    
    print("\n=== Transaktioner större än 500 SEK ===")
    query_transactions = """
        SELECT t.transaction_id, t.account_id, t.amount, t.transaction_type, t.timestamp
        FROM transactions t
        WHERE ABS(t.amount) > 500
        ORDER BY t.timestamp DESC
    """
    res_tx = conn.execute(query_transactions).fetchall()
    for tx in res_tx:
        print(tx)

def get_total_balance(customer_id, conn=None):
    """
    Returns the total balance for the specified customer.
    If the customer or their accounts are not found, returns 0.0.
    """
    if conn == None:
        conn = init_db()
    
    query = """
        SELECT SUM(a.balance) AS total_balance
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        WHERE c.customer_id = ?
    """
    result = conn.execute(query, (customer_id,)).fetchone()
    conn.close()
    
    # 'result' will be a tuple (total_balance,) or (None,) if no data is found.
    if result and result[0] is not None:
        return float(result[0])
    else:
        return 0.0


if __name__ == "__main__":
    conn = init_db()    
    
    # You can run this the first time. Comment it out next time if you don't want to duplicate data:
    #seed_data(conn)
    
    example_queries(conn)
    print(get_total_balance(conn,5))
    conn.close()
