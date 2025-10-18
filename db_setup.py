import os
import pandas as pd
from db_utils import get_connection

# CSV folder path
CSV_DIR = "csv_files"

# --- Step 1: Create Databases ---
def create_databases():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS order_db")
    cur.execute("CREATE DATABASE IF NOT EXISTS shipping_db")
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Databases created (order_db, shipping_db)")

# --- Step 2: Create Tables ---
def create_tables():
    # Orders
    conn = get_connection("order_db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT PRIMARY KEY,
            customer_id INT,
            order_status VARCHAR(50),
            payment_status VARCHAR(50),
            order_total DECIMAL(10,2),
            created_at DATETIME
        )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Order_Items (
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        sku VARCHAR(100),
        quantity INT,
        unit_price DECIMAL(10,2)
    )
""")
    conn.commit()
    conn.close()

    # Shipments
    conn = get_connection("shipping_db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Shipments (
            shipment_id INT PRIMARY KEY,
            order_id INT,
            carrier VARCHAR(100),
            status VARCHAR(50),
            tracking_no VARCHAR(100),
            shipped_at DATETIME,
            delivered_at DATETIME
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Tables created")

# --- Step 3: Load CSVs into Tables ---
def load_csv_to_table(csv_file, db_name, table_name):
    file_path = os.path.join(CSV_DIR, csv_file)
    df = pd.read_csv(file_path)
    print(f"📥 Loading {csv_file} ({len(df)} rows) into {db_name}.{table_name}")

    conn = get_connection(db_name)
    cur = conn.cursor()
    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))

    for _, row in df.iterrows():
        cur.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", tuple(row))
    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(df)} rows into {db_name}.{table_name}")

def main():
    create_databases()
    create_tables()
    load_csv_to_table("Orders.csv", "order_db", "Orders")
    load_csv_to_table("Order_Items.csv", "order_db", "Order_Items")
    load_csv_to_table("Shipments.csv", "shipping_db", "Shipments")
    print("🎉 All CSVs loaded successfully!")

'''
for dropping databases if needed
def drop_databases():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS order_db")
    cur.execute("DROP DATABASE IF EXISTS shipping_db")
    conn.commit()
    cur.close()
    conn.close()
    print("🗑️ Databases dropped (order_db, shipping_db)")
'''

if __name__ == "__main__":
    main()
